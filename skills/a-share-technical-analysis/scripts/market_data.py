#!/usr/bin/env python3
"""BaoStock-first A-share daily market data with AkShare fallback and checks."""

from __future__ import annotations

import importlib.metadata
import fcntl
import hashlib
import json
import math
import os
import re
import tempfile
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime, time as clock_time, timezone
from pathlib import Path
from typing import Any, Callable, Iterator
from zoneinfo import ZoneInfo

import pandas as pd


STANDARD_COLUMNS = ["dt", "symbol", "open", "close", "high", "low", "vol", "amount"]
PRICE_COLUMNS = ["open", "close", "high", "low"]
AKSHARE_VOLUME_MULTIPLIER = 100.0
SUPPORTED_ADJUSTMENTS = {"none", "qfq"}


class MarketDataError(RuntimeError):
    """Raised when a provider cannot supply a usable series."""


@dataclass(frozen=True)
class TickerMapping:
    ticker: str
    exchange: str
    code: str
    baostock_code: str
    akshare_code: str
    czsc_symbol: str


@dataclass
class MarketDataResult:
    ticker: str
    data: pd.DataFrame
    provider: str
    adjustment: str
    requested_start: str
    requested_end: str
    fetched_at: str
    data_quality_status: str
    quality_report: dict[str, Any]
    cross_check: dict[str, Any]
    package_versions: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    provider_errors: dict[str, str] = field(default_factory=dict)
    cache_paths: dict[str, str] = field(default_factory=dict)

    def manifest(self) -> dict[str, Any]:
        payload = asdict(self)
        payload.pop("data", None)
        payload["input_digest"] = normalized_frame_digest(self.data)
        payload["row_count"] = int(len(self.data))
        payload["actual_start"] = _date_text(self.data["dt"].min()) if len(self.data) else None
        payload["actual_end"] = _date_text(self.data["dt"].max()) if len(self.data) else None
        payload["columns"] = list(self.data.columns)
        return payload


def parse_ticker(ticker: str) -> TickerMapping:
    value = ticker.strip().upper()
    match = re.fullmatch(r"(SSE|SZSE|BJSE):(\d{6})", value)
    if not match:
        raise ValueError("A 股代码必须使用 SSE:600519、SZSE:000001 或 BJSE:xxxxxx 格式")

    exchange, code = match.groups()
    expected_first_digits = {
        "SSE": {"6"},
        "SZSE": {"0", "3"},
        "BJSE": {"4", "8", "9"},
    }
    if code[0] not in expected_first_digits[exchange]:
        raise ValueError(f"{value} 的交易所前缀与常见 A 股证券代码不一致")
    prefixes = {
        "SSE": ("sh", "SH"),
        "SZSE": ("sz", "SZ"),
        "BJSE": ("bj", "BJ"),
    }
    bao_prefix, suffix = prefixes[exchange]
    return TickerMapping(
        ticker=value,
        exchange=exchange,
        code=code,
        baostock_code=f"{bao_prefix}.{code}",
        akshare_code=code,
        czsc_symbol=f"{code}.{suffix}",
    )


def _validate_adjustment(adjustment: str) -> str:
    value = adjustment.lower()
    if value not in SUPPORTED_ADJUSTMENTS:
        raise ValueError(f"adjustment 必须是 {sorted(SUPPORTED_ADJUSTMENTS)}")
    return value


def _date_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return pd.Timestamp(value).date().isoformat()


def sanitize_provider_error(error: BaseException | str, limit: int = 500) -> str:
    """Remove request URLs and cap provider errors before persistence."""
    text = str(error)
    text = re.sub(r"https?://\S+", "[request-url-omitted]", text)
    if len(text) > limit:
        text = text[: limit - 1] + "…"
    return text


def normalized_frame_digest(frame: pd.DataFrame) -> str:
    """Hash normalized bars independently of their incoming row order."""
    data = frame.loc[:, STANDARD_COLUMNS].copy().sort_values("dt").reset_index(drop=True)
    data["dt"] = pd.to_datetime(data["dt"]).dt.strftime("%Y-%m-%d")
    for column in PRICE_COLUMNS + ["vol", "amount"]:
        data[column] = pd.to_numeric(data[column]).map(lambda value: f"{value:.12g}")
    return hashlib.sha256(
        data.to_csv(index=False, lineterminator="\n").encode("utf-8")
    ).hexdigest()


def _normalize_frame(frame: pd.DataFrame, symbol: str) -> pd.DataFrame:
    result = frame.copy()
    result["dt"] = pd.to_datetime(result["dt"], errors="coerce")
    result["symbol"] = symbol
    for column in PRICE_COLUMNS + ["vol", "amount"]:
        result[column] = pd.to_numeric(result[column], errors="coerce")
    result = result[STANDARD_COLUMNS].sort_values("dt").reset_index(drop=True)
    return result


def drop_unfinished_daily_bar(
    frame: pd.DataFrame,
    now: datetime | None = None,
) -> tuple[pd.DataFrame, bool]:
    """Remove today's bar before the conservative 15:10 Asia/Shanghai cutoff."""
    if frame.empty:
        return frame, False
    local_now = now or datetime.now(ZoneInfo("Asia/Shanghai"))
    if local_now.tzinfo is None:
        local_now = local_now.replace(tzinfo=ZoneInfo("Asia/Shanghai"))
    else:
        local_now = local_now.astimezone(ZoneInfo("Asia/Shanghai"))
    last_date = pd.Timestamp(frame["dt"].max()).date()
    if last_date == local_now.date() and local_now.time() < clock_time(15, 10):
        trimmed = frame.loc[
            pd.to_datetime(frame["dt"]).dt.date < last_date
        ].reset_index(drop=True)
        return trimmed, True
    return frame, False


def fetch_baostock(
    ticker: str,
    start: str,
    end: str,
    adjustment: str = "qfq",
) -> pd.DataFrame:
    """Fetch daily bars from BaoStock and normalize volume to shares."""
    import baostock as bs

    mapping = parse_ticker(ticker)
    adjustment = _validate_adjustment(adjustment)
    login = bs.login()
    if login.error_code != "0":
        raise MarketDataError(f"BaoStock login {login.error_code}: {login.error_msg}")

    try:
        fields = "date,code,open,high,low,close,volume,amount,adjustflag"
        result = bs.query_history_k_data_plus(
            mapping.baostock_code,
            fields,
            start_date=start,
            end_date=end,
            frequency="d",
            adjustflag="2" if adjustment == "qfq" else "3",
        )
        if result.error_code != "0":
            raise MarketDataError(
                f"BaoStock query {result.error_code}: {result.error_msg}"
            )
        rows: list[list[str]] = []
        while result.next():
            rows.append(result.get_row_data())
        if not rows:
            raise MarketDataError("BaoStock 返回空数据")
        raw = pd.DataFrame(rows, columns=result.fields).rename(
            columns={"date": "dt", "volume": "vol"}
        )
        return _normalize_frame(raw, mapping.czsc_symbol)
    finally:
        bs.logout()


def fetch_akshare(
    ticker: str,
    start: str,
    end: str,
    adjustment: str = "qfq",
    retries: int = 2,
    timeout: float = 20,
) -> pd.DataFrame:
    """Fetch Eastmoney daily bars through AkShare; normalize hands to shares."""
    import akshare as ak

    mapping = parse_ticker(ticker)
    adjustment = _validate_adjustment(adjustment)
    start_text = start.replace("-", "")
    end_text = end.replace("-", "")
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            raw = ak.stock_zh_a_hist(
                symbol=mapping.akshare_code,
                period="daily",
                start_date=start_text,
                end_date=end_text,
                adjust="qfq" if adjustment == "qfq" else "",
                timeout=timeout,
            )
            if raw is None or raw.empty:
                raise MarketDataError("AkShare 返回空数据")
            frame = raw.rename(
                columns={
                    "日期": "dt",
                    "开盘": "open",
                    "收盘": "close",
                    "最高": "high",
                    "最低": "low",
                    "成交量": "vol",
                    "成交额": "amount",
                }
            )
            frame["vol"] = pd.to_numeric(frame["vol"], errors="coerce") * AKSHARE_VOLUME_MULTIPLIER
            return _normalize_frame(frame, mapping.czsc_symbol)
        except Exception as exc:  # provider errors vary by AkShare release
            last_error = exc
            if attempt < retries:
                time.sleep(0.5 * (attempt + 1))
    raise MarketDataError(f"AkShare 请求失败: {type(last_error).__name__}: {last_error}")


def validate_bars(
    frame: pd.DataFrame,
    minimum_rows: int = 1,
    expected_end: str | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if frame.empty:
        return {
            "status": "unavailable",
            "errors": ["无可用 K 线"],
            "warnings": [],
            "row_count": 0,
            "actual_start": None,
            "actual_end": None,
            "freshness_gap_days": None,
        }
    missing = [column for column in STANDARD_COLUMNS if column not in frame.columns]
    if missing:
        return {
            "status": "unavailable",
            "errors": [f"缺少字段: {', '.join(missing)}"],
            "warnings": [],
            "row_count": int(len(frame)),
        }

    if len(frame) < minimum_rows:
        warnings.append(f"样本仅 {len(frame)} 行，低于建议值 {minimum_rows}")
    if frame["dt"].isna().any():
        errors.append("存在无法解析的交易日期")
    if frame["dt"].duplicated().any():
        errors.append("存在重复交易日期")
    if not frame["dt"].is_monotonic_increasing:
        errors.append("交易日期未严格升序")
    if frame[PRICE_COLUMNS + ["vol", "amount"]].isna().any().any():
        errors.append("价格、成交量或成交额存在空值/非数值")

    valid_numeric = frame.dropna(subset=PRICE_COLUMNS + ["vol", "amount"])
    if not valid_numeric.empty:
        bad_high = valid_numeric["high"] < valid_numeric[["open", "close", "low"]].max(axis=1)
        bad_low = valid_numeric["low"] > valid_numeric[["open", "close", "high"]].min(axis=1)
        if bad_high.any() or bad_low.any():
            errors.append("OHLC 高低价约束不成立")
        if (valid_numeric[["vol", "amount"]] < 0).any().any():
            errors.append("成交量或成交额为负")

    freshness_gap_days: int | None = None
    if expected_end and len(frame) and not frame["dt"].isna().all():
        freshness_gap_days = (
            pd.Timestamp(expected_end).date() - pd.Timestamp(frame["dt"].max()).date()
        ).days
        if freshness_gap_days > 14:
            warnings.append(
                f"最后交易日距请求截止日 {freshness_gap_days} 天，"
                "需核验停牌或数据滞后"
            )

    status = "disputed" if errors else ("degraded" if warnings else "complete")
    return {
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "row_count": int(len(frame)),
        "actual_start": _date_text(frame["dt"].min()) if len(frame) else None,
        "actual_end": _date_text(frame["dt"].max()) if len(frame) else None,
        "freshness_gap_days": freshness_gap_days,
    }


def compare_sources(
    primary: pd.DataFrame,
    supplement: pd.DataFrame,
    price_tolerance: float = 0.001,
    volume_tolerance: float = 0.02,
    amount_tolerance: float = 0.001,
) -> dict[str, Any]:
    """Compare normalized overlapping rows without averaging disagreements."""
    comparison_columns = ["dt"] + PRICE_COLUMNS + ["vol", "amount"]
    missing_primary = [column for column in comparison_columns if column not in primary]
    missing_supplement = [
        column for column in comparison_columns if column not in supplement
    ]
    if missing_primary or missing_supplement:
        return {
            "status": "unavailable",
            "overlap_rows": 0,
            "reason": (
                f"主源缺少 {missing_primary}；补充源缺少 {missing_supplement}"
            ),
        }
    if primary["dt"].duplicated().any() or supplement["dt"].duplicated().any():
        return {
            "status": "disputed",
            "overlap_rows": 0,
            "reason": "至少一个数据源存在重复交易日",
        }

    left = primary[comparison_columns].copy()
    right = supplement[comparison_columns].copy()
    merged = left.merge(right, on="dt", suffixes=("_primary", "_supplement"))
    if merged.empty:
        return {
            "status": "unavailable",
            "overlap_rows": 0,
            "reason": "双源没有重叠交易日",
        }

    numeric_columns = [
        f"{column}_{side}"
        for column in PRICE_COLUMNS + ["vol", "amount"]
        for side in ("primary", "supplement")
    ]
    if merged[numeric_columns].isna().any().any():
        return {
            "status": "disputed",
            "overlap_rows": int(len(merged)),
            "reason": "双源重叠区间存在非数值或空值",
        }

    metrics: dict[str, float] = {}
    for column in PRICE_COLUMNS + ["vol", "amount"]:
        denominator = merged[f"{column}_primary"].abs().clip(lower=1e-12)
        relative_error = (
            merged[f"{column}_primary"] - merged[f"{column}_supplement"]
        ).abs() / denominator
        metrics[f"{column}_max_relative_error"] = float(relative_error.max())
        metrics[f"{column}_median_relative_error"] = float(relative_error.median())

    price_disputed = any(
        metrics[f"{column}_max_relative_error"] > price_tolerance
        for column in PRICE_COLUMNS
    )
    volume_disputed = metrics["vol_max_relative_error"] > volume_tolerance
    amount_disputed = metrics["amount_max_relative_error"] > amount_tolerance
    return {
        "status": (
            "disputed"
            if price_disputed or volume_disputed or amount_disputed
            else "complete"
        ),
        "overlap_rows": int(len(merged)),
        "first_overlap": _date_text(merged["dt"].min()),
        "last_overlap": _date_text(merged["dt"].max()),
        "price_tolerance": price_tolerance,
        "volume_tolerance": volume_tolerance,
        "amount_tolerance": amount_tolerance,
        "metrics": metrics,
    }


def get_market_data(
    ticker: str,
    start: str,
    end: str,
    adjustment: str = "qfq",
    minimum_rows: int = 120,
    cross_check: bool = True,
    baostock_fetcher: Callable[..., pd.DataFrame] = fetch_baostock,
    akshare_fetcher: Callable[..., pd.DataFrame] = fetch_akshare,
) -> MarketDataResult:
    """Use BaoStock first, then AkShare fallback; never hide a provider switch."""
    parse_ticker(ticker)
    adjustment = _validate_adjustment(adjustment)
    fetched_at = datetime.now(timezone.utc).isoformat()
    provider_errors: dict[str, str] = {}
    frames: dict[str, pd.DataFrame] = {}
    warnings: list[str] = []

    for name, fetcher in (
        ("baostock", baostock_fetcher),
        ("akshare", akshare_fetcher),
    ):
        if name == "akshare" and not cross_check and "baostock" in frames:
            continue
        try:
            frame = fetcher(ticker, start, end, adjustment)
            frame, dropped = drop_unfinished_daily_bar(frame)
            if frame.empty:
                raise MarketDataError("排除未完成日 K 后无可用数据")
            frames[name] = frame
            if dropped:
                warnings.append(f"{name} 的当日未完成日 K 已排除")
        except Exception as exc:
            provider_errors[name] = (
                f"{type(exc).__name__}: {sanitize_provider_error(exc)}"
            )

    if "baostock" in frames:
        provider = "baostock"
        data = frames["baostock"]
    elif "akshare" in frames:
        provider = "akshare"
        data = frames["akshare"]
        warnings.append("BaoStock 不可用，已明确降级为 AkShare")
    else:
        raise MarketDataError(
            "BaoStock 与 AkShare 均不可用: " + json.dumps(provider_errors, ensure_ascii=False)
        )

    quality = validate_bars(data, minimum_rows=minimum_rows, expected_end=end)
    if "baostock" in frames and "akshare" in frames:
        cross_result = compare_sources(frames["baostock"], frames["akshare"])
    else:
        cross_result = {
            "status": "unavailable",
            "overlap_rows": 0,
            "reason": "仅一个行情源可用",
        }
        warnings.append("无法完成双源交叉核对")

    if adjustment == "qfq" and cross_result["status"] != "complete":
        unadjusted_frames: dict[str, pd.DataFrame] = {}
        for name, fetcher in (
            ("baostock", baostock_fetcher),
            ("akshare", akshare_fetcher),
        ):
            try:
                raw_frame = fetcher(ticker, start, end, "none")
                raw_frame, dropped = drop_unfinished_daily_bar(raw_frame)
                if raw_frame.empty:
                    raise MarketDataError("排除未完成日 K 后无可用数据")
                unadjusted_frames[name] = raw_frame
                if dropped:
                    warnings.append(f"{name} 未复权序列的当日未完成日 K 已排除")
            except Exception as exc:
                provider_errors[f"{name}:none"] = (
                    f"{type(exc).__name__}: {sanitize_provider_error(exc)}"
                )

        if {"baostock", "akshare"}.issubset(unadjusted_frames):
            unadjusted_check = compare_sources(
                unadjusted_frames["baostock"],
                unadjusted_frames["akshare"],
            )
            adjusted_check = cross_result
            if unadjusted_check["status"] == "complete":
                cross_result = {
                    "status": "degraded",
                    "basis": "unadjusted_fallback",
                    "reason": (
                        "未复权行情核对通过，"
                        "但前复权分析序列未通过双源完整核对"
                    ),
                    "analysis_adjustment_check": adjusted_check,
                    "unadjusted_check": unadjusted_check,
                    "overlap_rows": unadjusted_check["overlap_rows"],
                }
                warnings.append(
                    "未复权双源核对通过；前复权分析序列仍按降级状态使用"
                )
            elif unadjusted_check["status"] == "disputed":
                cross_result = {
                    "status": "disputed",
                    "basis": "unadjusted_fallback",
                    "reason": "未复权行情仍存在双源争议",
                    "analysis_adjustment_check": adjusted_check,
                    "unadjusted_check": unadjusted_check,
                    "overlap_rows": unadjusted_check["overlap_rows"],
                }

    if quality["status"] == "unavailable":
        status = "unavailable"
    elif quality["status"] == "disputed" or cross_result["status"] == "disputed":
        status = "disputed"
    elif (
        provider != "baostock"
        or quality["status"] == "degraded"
        or cross_result["status"] != "complete"
    ):
        status = "degraded"
    else:
        status = "complete"

    warnings.extend(quality.get("warnings", []))
    return MarketDataResult(
        ticker=ticker.upper(),
        data=data,
        provider=provider,
        adjustment=adjustment,
        requested_start=start,
        requested_end=end,
        fetched_at=fetched_at,
        data_quality_status=status,
        quality_report=quality,
        cross_check=cross_result,
        package_versions={
            package: importlib.metadata.version(package)
            for package in ("baostock", "akshare")
        },
        warnings=warnings,
        provider_errors=provider_errors,
    )


def _temporary_peer(path: Path) -> Path:
    with tempfile.NamedTemporaryFile(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as stream:
        return Path(stream.name)


def _fsync_file(path: Path) -> None:
    with path.open("rb") as stream:
        os.fsync(stream.fileno())


def _fsync_directory(path: Path) -> None:
    try:
        descriptor = os.open(path, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(descriptor)
    except OSError:
        pass
    finally:
        os.close(descriptor)


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@contextmanager
def _cache_identity_lock(cache_dir: Path, stem: str) -> Iterator[Path]:
    lock_path = cache_dir / f".{stem}.lock"
    with lock_path.open("a+", encoding="utf-8") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try:
            yield lock_path
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def _existing_cache_bundle_is_valid(
    final_paths: dict[str, Path],
    cache_identity: dict[str, Any],
) -> bool:
    exists = {name: path.is_file() for name, path in final_paths.items()}
    if not any(exists.values()):
        return False
    if not all(exists.values()):
        raise MarketDataError(
            "cache identity 已存在不完整 bundle；拒绝覆盖，需先人工审计"
        )
    try:
        manifest = json.loads(final_paths["manifest"].read_text(encoding="utf-8"))
        if manifest.get("cache_identity") != cache_identity:
            raise ValueError("cache identity mismatch")
        artifacts = manifest.get("cache_artifacts")
        if not isinstance(artifacts, dict):
            raise ValueError("cache_artifacts missing")
        for name in ("parquet", "csv"):
            expected = artifacts.get(name)
            if not isinstance(expected, dict):
                raise ValueError(f"{name} integrity entry missing")
            if expected.get("sha256") != _file_sha256(final_paths[name]):
                raise ValueError(f"{name} sha256 mismatch")
            if int(expected.get("bytes", -1)) != final_paths[name].stat().st_size:
                raise ValueError(f"{name} size mismatch")
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        raise MarketDataError(
            f"cache identity 已存在但完整性校验失败；拒绝覆盖: {exc}"
        ) from exc
    return True


def save_cache(result: MarketDataResult, cache_dir: Path) -> dict[str, str]:
    """Commit immutable-identity Parquet/CSV caches, then manifest last."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_frame = result.data.sort_values("dt").reset_index(drop=True)
    input_digest = normalized_frame_digest(cache_frame)
    safe_ticker = result.ticker.lower().replace(":", "-")
    safe_provider = re.sub(r"[^a-z0-9._-]+", "-", result.provider.lower()).strip("-")
    safe_provider = safe_provider or "unknown-provider"
    actual_end = _date_text(cache_frame["dt"].max())
    stem = (
        f"{safe_ticker}-{result.adjustment}-{actual_end}-"
        f"{safe_provider}-{input_digest}"
    )
    final_paths = {
        "parquet": cache_dir / f"{stem}.parquet",
        "csv": cache_dir / f"{stem}.csv",
        "manifest": cache_dir / f"{stem}.manifest.json",
    }
    cache_identity = {
        "ticker": result.ticker,
        "adjustment": result.adjustment,
        "actual_end": actual_end,
        "provider": result.provider,
        "input_digest": input_digest,
        "stem": stem,
    }
    with _cache_identity_lock(cache_dir, stem):
        resolved_paths = {
            name: str(path.resolve()) for name, path in final_paths.items()
        }
        if _existing_cache_bundle_is_valid(final_paths, cache_identity):
            result.cache_paths = resolved_paths
            return result.cache_paths

        temporary_paths: dict[str, Path] = {}
        previous_cache_paths = dict(result.cache_paths)
        result.cache_paths = resolved_paths
        try:
            temporary_paths["parquet"] = _temporary_peer(final_paths["parquet"])
            cache_frame.to_parquet(temporary_paths["parquet"], index=False)
            _fsync_file(temporary_paths["parquet"])

            temporary_paths["csv"] = _temporary_peer(final_paths["csv"])
            cache_frame.to_csv(
                temporary_paths["csv"],
                index=False,
                date_format="%Y-%m-%d",
                lineterminator="\n",
            )
            _fsync_file(temporary_paths["csv"])

            manifest_payload = result.manifest()
            manifest_payload["cache_identity"] = cache_identity
            manifest_payload["cache_artifacts"] = {
                name: {
                    "path": str(final_paths[name].resolve()),
                    "sha256": _file_sha256(temporary_paths[name]),
                    "bytes": temporary_paths[name].stat().st_size,
                }
                for name in ("parquet", "csv")
            }
            temporary_paths["manifest"] = _temporary_peer(final_paths["manifest"])
            with temporary_paths["manifest"].open("w", encoding="utf-8") as stream:
                stream.write(
                    json.dumps(
                        manifest_payload,
                        ensure_ascii=False,
                        indent=2,
                        default=_json_default,
                    )
                    + "\n"
                )
                stream.flush()
                os.fsync(stream.fileno())

            for name in ("parquet", "csv", "manifest"):
                temporary_paths[name].replace(final_paths[name])
            _fsync_directory(cache_dir)
        except Exception:
            result.cache_paths = previous_cache_paths
            for path in final_paths.values():
                if path.exists():
                    path.unlink()
            raise
        finally:
            for path in temporary_paths.values():
                if path.exists():
                    path.unlink()

    return result.cache_paths


def _json_default(value: Any) -> Any:
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    if hasattr(value, "item"):
        return value.item()
    raise TypeError(f"无法序列化 {type(value).__name__}")


__all__ = [
    "AKSHARE_VOLUME_MULTIPLIER",
    "MarketDataError",
    "MarketDataResult",
    "STANDARD_COLUMNS",
    "compare_sources",
    "drop_unfinished_daily_bar",
    "fetch_akshare",
    "fetch_baostock",
    "get_market_data",
    "normalized_frame_digest",
    "parse_ticker",
    "sanitize_provider_error",
    "save_cache",
    "validate_bars",
]
