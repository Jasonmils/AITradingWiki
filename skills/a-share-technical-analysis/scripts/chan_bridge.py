#!/usr/bin/env python3
"""Read-only chan.py adapter over the same normalized bars used by CZSC.

The adapter intentionally never imports or invokes chan.py ``DataAPI``
implementations.  A pinned checkout is dynamically loaded and receives only
the already-normalized pandas frame through ``CChan.trigger_load``.
"""

from __future__ import annotations

import fcntl
import hashlib
import importlib
import json
import os
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

from czsc_bridge import resample_bars
from market_data import normalized_frame_digest as _market_frame_digest


REPO_ROOT = Path(__file__).resolve().parents[3]
EXPECTED_CHAN_COMMIT = "429d6ed3043e27c93a003ba2b10e70a05575e1f5"
DEFAULT_CHAN_ROOT = REPO_ROOT / ".work" / "vendor" / "chan.py"
STATE_SCHEMA_VERSION = 1
ADAPTER_SCHEMA_VERSION = 1
PROFILE_ORDER = ("strict", "broad")
TIMEFRAME_ORDER = ("monthly", "weekly", "daily")
NATIVE_PLOT_LAYERS = (
    "plot_kline",
    "plot_kline_combine",
    "plot_bi",
    "plot_seg",
    "plot_segseg",
    "plot_zs",
    "plot_segzs",
    "plot_bsp",
    "plot_segbsp",
    "plot_macd",
)

_BASE_PROFILE: dict[str, Any] = {
    "bi_algo": "normal",
    "gap_as_kl": False,
    "bi_end_is_peak": True,
    "seg_algo": "chan",
    "left_seg_method": "peak",
    "zs_algo": "normal",
    "zs_combine": True,
    "zs_combine_mode": "zs",
    "one_bi_zs": False,
    "trigger_step": True,
    "kl_data_check": False,
    "print_warning": False,
    "print_err_time": False,
    "bs_type": "1,1p,2,2s,3a,3b",
}

CHAN_PROFILES: dict[str, dict[str, Any]] = {
    "strict": {
        **_BASE_PROFILE,
        "bi_strict": True,
        "bi_fx_check": "strict",
        "bi_allow_sub_peak": False,
    },
    "broad": {
        **_BASE_PROFILE,
        "bi_strict": False,
        "bi_fx_check": "half",
        "bi_allow_sub_peak": True,
    },
}

_RUNTIME: dict[str, Any] | None = None
_RUNTIME_ROOT: Path | None = None


class ChanAdapterUnavailable(RuntimeError):
    """Raised when the pinned chan.py runtime cannot be loaded safely."""


def _json_hash(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _number(value: Any, digits: int = 6) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if pd.isna(number) or number in {float("inf"), float("-inf")}:
        return None
    return round(number, digits)


def _enum_direction(value: Any) -> str | None:
    if value is None:
        return None
    name = str(getattr(value, "name", value)).lower()
    if name.endswith("up") or name in {"向上", "up"}:
        return "up"
    if name.endswith("down") or name in {"向下", "down"}:
        return "down"
    return name


def _chan_date(value: Any) -> str | None:
    if value is None:
        return None
    if all(hasattr(value, field) for field in ("year", "month", "day")):
        return f"{value.year:04d}-{value.month:02d}-{value.day:02d}"
    try:
        return pd.Timestamp(value).date().isoformat()
    except Exception:
        return None


def normalized_frame_digest(frame: pd.DataFrame) -> str:
    """Hash the exact normalized bars shared by both structure engines."""
    return _market_frame_digest(frame)


def resolve_chan_root(explicit_path: Path | str | None = None) -> Path:
    raw = explicit_path or os.environ.get("CHAN_PY_PATH") or DEFAULT_CHAN_ROOT
    return Path(raw).expanduser().resolve()


def _read_checkout_commit(root: Path) -> str | None:
    if not (root / ".git").exists():
        return None
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip()


def _checkout_dirty_entries(root: Path) -> list[str] | None:
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return [line for line in result.stdout.splitlines() if line.strip()]


def _verify_chan_root(root: Path) -> str:
    required = (
        "Chan.py",
        "ChanConfig.py",
        "Common/CEnum.py",
        "Common/CTime.py",
        "KLine/KLine_Unit.py",
    )
    missing = [name for name in required if not (root / name).is_file()]
    if missing:
        raise ChanAdapterUnavailable(
            f"chan.py checkout 不完整，缺少: {', '.join(missing)}"
        )
    commit = _read_checkout_commit(root)
    if commit is None:
        raise ChanAdapterUnavailable(
            "无法验证 chan.py commit；checkout 必须保留 .git"
        )
    if commit != EXPECTED_CHAN_COMMIT:
        raise ChanAdapterUnavailable(
            f"chan.py commit 不匹配: expected={EXPECTED_CHAN_COMMIT}, actual={commit}"
        )
    dirty_entries = _checkout_dirty_entries(root)
    if dirty_entries is None:
        raise ChanAdapterUnavailable("无法审计 chan.py checkout 的 tracked/untracked changes")
    if dirty_entries:
        raise ChanAdapterUnavailable(
            "chan.py checkout 含 tracked/untracked changes，拒绝加载"
        )
    return commit


def _load_runtime(root: Path) -> dict[str, Any]:
    global _RUNTIME, _RUNTIME_ROOT
    commit = _verify_chan_root(root)
    if _RUNTIME is not None:
        if _RUNTIME_ROOT != root:
            raise ChanAdapterUnavailable(
                f"进程已从 {_RUNTIME_ROOT} 加载 chan.py，拒绝切换到 {root}"
            )
        return _RUNTIME

    existing = sys.modules.get("Chan")
    if existing is not None:
        origin = Path(getattr(existing, "__file__", "")).resolve()
        if root not in origin.parents:
            raise ChanAdapterUnavailable(
                f"检测到来自其他路径的 Chan 模块: {origin}"
            )

    if sys.pycache_prefix is None:
        sys.pycache_prefix = str(REPO_ROOT / ".work" / "pycache" / "chan-runtime")
    sys.path.insert(0, str(root))
    try:
        chan_module = importlib.import_module("Chan")
        config_module = importlib.import_module("ChanConfig")
        enum_module = importlib.import_module("Common.CEnum")
        time_module = importlib.import_module("Common.CTime")
        unit_module = importlib.import_module("KLine.KLine_Unit")
    except Exception as exc:
        raise ChanAdapterUnavailable(
            f"加载 chan.py 失败: {type(exc).__name__}: {exc}"
        ) from exc
    finally:
        if sys.path and sys.path[0] == str(root):
            sys.path.pop(0)

    _RUNTIME_ROOT = root
    _RUNTIME = {
        "CChan": chan_module.CChan,
        "CChanConfig": config_module.CChanConfig,
        "KL_TYPE": enum_module.KL_TYPE,
        "DATA_FIELD": enum_module.DATA_FIELD,
        "CTime": time_module.CTime,
        "CKLine_Unit": unit_module.CKLine_Unit,
        "commit": commit,
        "root": str(root),
    }
    return _RUNTIME


def _profile_hash(name: str, config: dict[str, Any]) -> str:
    return _json_hash(
        {
            "adapter_schema_version": ADAPTER_SCHEMA_VERSION,
            "upstream_commit": EXPECTED_CHAN_COMMIT,
            "profile": name,
            "config": config,
        }
    )


def _make_units(frame: pd.DataFrame, runtime: dict[str, Any]) -> list[Any]:
    data_field = runtime["DATA_FIELD"]
    units: list[Any] = []
    for _, row in frame.sort_values("dt").iterrows():
        stamp = pd.Timestamp(row["dt"])
        unit = runtime["CKLine_Unit"](
            {
                data_field.FIELD_TIME: runtime["CTime"](
                    stamp.year, stamp.month, stamp.day, 0, 0
                ),
                data_field.FIELD_OPEN: float(row["open"]),
                data_field.FIELD_CLOSE: float(row["close"]),
                data_field.FIELD_HIGH: float(row["high"]),
                data_field.FIELD_LOW: float(row["low"]),
                data_field.FIELD_VOLUME: float(row["vol"]),
                data_field.FIELD_TURNOVER: float(row["amount"]),
            }
        )
        units.append(unit)
    return units


def _build_analyzer(
    frame: pd.DataFrame,
    *,
    timeframe: str,
    profile_config: dict[str, Any],
    runtime: dict[str, Any],
) -> tuple[pd.DataFrame, Any, Any, Any]:
    """Build one local-only chan.py analyzer from normalized bars."""
    bars = resample_bars(frame, timeframe).reset_index(drop=True)
    level = {
        "daily": runtime["KL_TYPE"].K_DAY,
        "weekly": runtime["KL_TYPE"].K_WEEK,
        "monthly": runtime["KL_TYPE"].K_MON,
    }[timeframe]
    config = runtime["CChanConfig"](dict(profile_config))
    analyzer = runtime["CChan"](
        code=str(bars["symbol"].iloc[-1]),
        data_src="external-normalized-bars",
        lv_list=[level],
        config=config,
    )
    analyzer.trigger_load({level: _make_units(bars, runtime)})
    structure = analyzer.kl_datas[level]
    # ``trigger_step`` prevents provider loading.  A final calculation ensures
    # the last provisional structures are represented in the static snapshot.
    structure.cal_seg_and_zs()
    return bars, level, analyzer, structure


def _identity(element: dict[str, Any]) -> str:
    identity = {
        "engine": "chan.py",
        "profile": element["profile"],
        "timeframe": element["timeframe"],
        "layer": element["layer"],
        "index": element.get("index"),
        "start": element.get("start"),
        "direction": element.get("direction"),
        "bsp_types": element.get("bsp_types"),
    }
    return "chan-" + _json_hash(identity)[:20]


def _finalize_element(element: dict[str, Any]) -> dict[str, Any]:
    payload = dict(element)
    payload["element_id"] = _identity(payload)
    content = {
        key: value
        for key, value in payload.items()
        if key not in {"element_id", "first_seen", "last_changed", "withdrawn"}
    }
    payload["content_hash"] = _json_hash(content)
    return payload


def _line_element(
    line: Any,
    *,
    layer: str,
    profile: str,
    timeframe: str,
) -> dict[str, Any]:
    confirmed = bool(getattr(line, "is_sure", False))
    return _finalize_element(
        {
            "engine": "chan.py",
            "profile": profile,
            "timeframe": timeframe,
            "layer": layer,
            "index": int(getattr(line, "idx", -1)),
            "start": _chan_date(line.get_begin_klu().time),
            "end": _chan_date(line.get_end_klu().time),
            "direction": _enum_direction(getattr(line, "dir", None)),
            "start_value": _number(line.get_begin_val()),
            "end_value": _number(line.get_end_val()),
            "lower": _number(line._low()),
            "upper": _number(line._high()),
            "confirmed": confirmed,
            "status": "confirmed" if confirmed else "provisional",
            "confirmation_scope": "current_as_of_revision_or_withdrawal_possible",
        }
    )


def _zone_element(
    zone: Any,
    *,
    index: int,
    profile: str,
    timeframe: str,
    layer: str,
) -> dict[str, Any]:
    confirmed = bool(getattr(zone, "is_sure", False))
    return _finalize_element(
        {
            "engine": "chan.py",
            "profile": profile,
            "timeframe": timeframe,
            "layer": layer,
            "index": index,
            "start": _chan_date(zone.begin.time),
            "end": _chan_date(zone.end.time),
            "direction": None,
            "lower": _number(zone.low),
            "upper": _number(zone.high),
            "axis": _number(zone.mid),
            "peak_lower": _number(zone.peak_low),
            "peak_upper": _number(zone.peak_high),
            "begin_line_index": int(zone.begin_bi.idx),
            "end_line_index": int(zone.end_bi.idx),
            "confirmed": confirmed,
            "status": "confirmed" if confirmed else "provisional",
            "confirmation_scope": "current_as_of_revision_or_withdrawal_possible",
        }
    )


def _bsp_element(
    bsp: Any,
    *,
    index: int,
    profile: str,
    timeframe: str,
    layer: str,
) -> dict[str, Any]:
    line = bsp.bi
    confirmed = bool(getattr(line, "is_sure", False))
    bsp_types = sorted(
        {str(getattr(item, "value", item)) for item in getattr(bsp, "type", [])}
    )
    return _finalize_element(
        {
            "engine": "chan.py",
            "profile": profile,
            "timeframe": timeframe,
            "layer": layer,
            "index": index,
            "source_line_index": int(getattr(line, "idx", -1)),
            "start": _chan_date(bsp.klu.time),
            "end": _chan_date(bsp.klu.time),
            "direction": _enum_direction(getattr(line, "dir", None)),
            "price": _number(getattr(bsp.klu, "close", None)),
            "bsp_types": bsp_types,
            "morphology_side": (
                "lower_turning_structure"
                if bool(getattr(bsp, "is_buy", False))
                else "upper_turning_structure"
            ),
            "interpretation": "neutral_candidate_not_trade_signal",
            "confirmed": confirmed,
            "status": "confirmed" if confirmed else "provisional",
            "confirmation_scope": "current_as_of_revision_or_withdrawal_possible",
        }
    )


def _extract_timeframe(
    frame: pd.DataFrame,
    *,
    timeframe: str,
    profile: str,
    profile_config: dict[str, Any],
    runtime: dict[str, Any],
) -> dict[str, Any]:
    bars, _, _, structure = _build_analyzer(
        frame,
        timeframe=timeframe,
        profile_config=profile_config,
        runtime=runtime,
    )

    elements: list[dict[str, Any]] = []
    elements.extend(
        _line_element(
            line,
            layer="bi",
            profile=profile,
            timeframe=timeframe,
        )
        for line in structure.bi_list
    )
    elements.extend(
        _line_element(
            line,
            layer="segment",
            profile=profile,
            timeframe=timeframe,
        )
        for line in structure.seg_list
    )
    elements.extend(
        _line_element(
            line,
            layer="segment_of_segment",
            profile=profile,
            timeframe=timeframe,
        )
        for line in structure.segseg_list
    )
    elements.extend(
        _zone_element(
            zone,
            index=index,
            profile=profile,
            timeframe=timeframe,
            layer="zone",
        )
        for index, zone in enumerate(structure.zs_list)
    )
    elements.extend(
        _zone_element(
            zone,
            index=index,
            profile=profile,
            timeframe=timeframe,
            layer="segment_zone",
        )
        for index, zone in enumerate(structure.segzs_list)
    )
    bsp_values = sorted(
        structure.bs_point_lst.bsp_store_flat_dict.values(),
        key=lambda value: value.bi.idx,
    )
    elements.extend(
        _bsp_element(
            bsp,
            index=index,
            profile=profile,
            timeframe=timeframe,
            layer="bsp",
        )
        for index, bsp in enumerate(bsp_values)
    )
    segment_bsp_values = sorted(
        structure.seg_bs_point_lst.bsp_store_flat_dict.values(),
        key=lambda value: value.bi.idx,
    )
    elements.extend(
        _bsp_element(
            bsp,
            index=index,
            profile=profile,
            timeframe=timeframe,
            layer="segment_bsp",
        )
        for index, bsp in enumerate(segment_bsp_values)
    )

    counts: dict[str, dict[str, int]] = {}
    for layer in (
        "bi",
        "segment",
        "segment_of_segment",
        "zone",
        "segment_zone",
        "bsp",
        "segment_bsp",
    ):
        subset = [item for item in elements if item["layer"] == layer]
        counts[layer] = {
            "total": len(subset),
            "confirmed": sum(item["confirmed"] for item in subset),
            "provisional": sum(not item["confirmed"] for item in subset),
        }
    return {
        "status": "complete",
        "timeframe": timeframe,
        "bar_count": int(len(bars)),
        "as_of": pd.Timestamp(bars["dt"].max()).date().isoformat(),
        "counts": counts,
        "elements": elements,
    }


def _analyze_profile(
    frame: pd.DataFrame,
    *,
    profile: str,
    runtime: dict[str, Any],
) -> dict[str, Any]:
    config = CHAN_PROFILES[profile]
    timeframes: dict[str, Any] = {}
    errors: dict[str, str] = {}
    for timeframe in TIMEFRAME_ORDER:
        try:
            timeframes[timeframe] = _extract_timeframe(
                frame,
                timeframe=timeframe,
                profile=profile,
                profile_config=config,
                runtime=runtime,
            )
        except Exception as exc:
            errors[timeframe] = f"{type(exc).__name__}: {exc}"
            timeframes[timeframe] = {
                "status": "unavailable",
                "timeframe": timeframe,
                "reason": errors[timeframe],
                "elements": [],
            }
    return {
        "status": "complete" if not errors else "unavailable",
        "name": profile,
        "config": config,
        "config_hash": _profile_hash(profile, config),
        "timeframes": timeframes,
        "errors": errors,
    }


def _semantic_key(element: dict[str, Any]) -> str:
    keys = (
        "timeframe",
        "layer",
        "start",
        "end",
        "direction",
        "lower",
        "upper",
        "axis",
        "price",
        "bsp_types",
        "morphology_side",
        "confirmed",
    )
    return _json_hash({key: element.get(key) for key in keys})


def _all_elements(profile: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for timeframe in TIMEFRAME_ORDER:
        result.extend(profile["timeframes"].get(timeframe, {}).get("elements", []))
    return result


def compare_profiles(profiles: dict[str, Any]) -> dict[str, Any]:
    if any(profiles.get(name, {}).get("status") != "complete" for name in PROFILE_ORDER):
        return {
            "status": "unavailable",
            "reason": "strict 或 broad 参数运行不完整，无法计算稳定交集",
            "stable_elements": [],
            "layer_comparisons": [],
            "critical_direction_checks": [],
        }

    strict_elements = _all_elements(profiles["strict"])
    broad_elements = _all_elements(profiles["broad"])
    strict_by_key = {_semantic_key(item): item for item in strict_elements}
    broad_keys = {_semantic_key(item) for item in broad_elements}
    common_keys = set(strict_by_key).intersection(broad_keys)
    stable_elements = []
    for key in sorted(common_keys):
        item = dict(strict_by_key[key])
        item["stable_across_profiles"] = True
        item["profile_sources"] = list(PROFILE_ORDER)
        item["stable_key"] = key
        stable_elements.append(item)

    layer_comparisons: list[dict[str, Any]] = []
    for timeframe in TIMEFRAME_ORDER:
        for layer in ("bi", "segment", "zone", "bsp"):
            strict_keys = {
                _semantic_key(item)
                for item in strict_elements
                if item["timeframe"] == timeframe and item["layer"] == layer
            }
            broad_keys_for_layer = {
                _semantic_key(item)
                for item in broad_elements
                if item["timeframe"] == timeframe and item["layer"] == layer
            }
            common = strict_keys.intersection(broad_keys_for_layer)
            denominator = min(len(strict_keys), len(broad_keys_for_layer))
            layer_comparisons.append(
                {
                    "timeframe": timeframe,
                    "layer": layer,
                    "strict_count": len(strict_keys),
                    "broad_count": len(broad_keys_for_layer),
                    "stable_count": len(common),
                    "stable_coverage_of_smaller_set": (
                        round(len(common) / denominator, 6) if denominator else None
                    ),
                    "note": "数量差异本身不构成 disputed",
                }
            )

    critical_checks: list[dict[str, Any]] = []
    critical_disputed = False
    for timeframe in ("monthly", "weekly"):
        directions: dict[str, str | None] = {}
        for profile_name in PROFILE_ORDER:
            candidates = [
                item
                for item in _all_elements(profiles[profile_name])
                if item["timeframe"] == timeframe
                and item["layer"] == "bi"
                and item["confirmed"]
            ]
            directions[profile_name] = (
                sorted(candidates, key=lambda item: (item["end"] or "", item["index"]))[-1][
                    "direction"
                ]
                if candidates
                else None
            )
        if all(directions.values()) and len(set(directions.values())) > 1:
            check_status = "disputed"
            critical_disputed = True
        elif all(directions.values()):
            check_status = "complete"
        else:
            check_status = "degraded"
        critical_checks.append(
            {
                "timeframe": timeframe,
                "anchor": "latest_confirmed_bi_direction",
                "status": check_status,
                "values": directions,
            }
        )

    low_coverage = any(
        item["stable_coverage_of_smaller_set"] is not None
        and item["stable_coverage_of_smaller_set"] < 0.5
        for item in layer_comparisons
        if item["timeframe"] in {"monthly", "weekly"}
        and item["layer"] in {"bi", "segment", "zone"}
    )
    status = "disputed" if critical_disputed else ("degraded" if low_coverage else "complete")
    return {
        "status": status,
        "method": "semantic_intersection_not_count_equality",
        "stable_elements": stable_elements,
        "layer_comparisons": layer_comparisons,
        "critical_direction_checks": critical_checks,
    }


def analyze_chan_profiles(
    frame: pd.DataFrame,
    *,
    chan_path: Path | str | None = None,
) -> dict[str, Any]:
    root = resolve_chan_root(chan_path)
    input_digest = normalized_frame_digest(frame)
    try:
        runtime = _load_runtime(root)
    except Exception as exc:
        return {
            "status": "unavailable",
            "reason_code": "chan_runtime_unavailable",
            "reason": f"{type(exc).__name__}: {exc}",
            "expected_commit": EXPECTED_CHAN_COMMIT,
            "source_path": str(root),
            "input_digest": input_digest,
            "input_contract": "normalized_local_bars_only_no_chan_dataapi",
            "profiles": {},
            "profile_stability": {
                "status": "unavailable",
                "stable_elements": [],
                "reason": "chan.py runtime unavailable",
            },
        }

    profiles = {
        profile: _analyze_profile(frame, profile=profile, runtime=runtime)
        for profile in PROFILE_ORDER
    }
    stability = compare_profiles(profiles)
    status = (
        "unavailable"
        if any(item["status"] != "complete" for item in profiles.values())
        else stability["status"]
    )
    return {
        "status": status,
        "engine": {
            "name": "chan.py",
            "upstream_commit": runtime["commit"],
            "expected_commit": EXPECTED_CHAN_COMMIT,
            "source_path": runtime["root"],
            "adapter_schema_version": ADAPTER_SCHEMA_VERSION,
            "data_access": "trigger_load_from_normalized_local_bars",
            "upstream_dataapi_used": False,
        },
        "input_digest": input_digest,
        "input_contract": "same_normalized_frame_as_czsc",
        "profiles": profiles,
        "profile_stability": stability,
    }


def _state_identity(chan_result: dict[str, Any]) -> dict[str, Any]:
    profile_hashes = {
        name: chan_result.get("profiles", {}).get(name, {}).get("config_hash")
        or _profile_hash(name, CHAN_PROFILES[name])
        for name in PROFILE_ORDER
    }
    identity = {
        "adapter_schema_version": ADAPTER_SCHEMA_VERSION,
        "upstream_commit": chan_result.get("engine", {}).get(
            "upstream_commit", EXPECTED_CHAN_COMMIT
        ),
        "profile_config_hashes": profile_hashes,
    }
    return {**identity, "bundle_hash": _json_hash(identity)}


def _state_path(
    state_dir: Path,
    ticker: str,
    adjustment: str,
    bundle_hash: str,
) -> Path:
    safe_ticker = ticker.lower().replace(":", "-")
    return state_dir / (
        f"{safe_ticker}-{adjustment}-{bundle_hash[:16]}.structure-state.json"
    )


def _atomic_json_write(path: Path, value: Any) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = (
        json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n"
    ).encode("utf-8")
    content_sha256 = hashlib.sha256(encoded).hexdigest()
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as stream:
            stream.write(encoded.decode("utf-8"))
            stream.flush()
            os.fsync(stream.fileno())
            temporary_path = Path(stream.name)
        temporary_path.replace(path)
        try:
            directory_descriptor = os.open(path.parent, os.O_RDONLY)
        except OSError:
            directory_descriptor = None
        if directory_descriptor is not None:
            try:
                os.fsync(directory_descriptor)
            except OSError:
                pass
            finally:
                os.close(directory_descriptor)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()
    return content_sha256


@contextmanager
def _state_file_lock(path: Path) -> Iterable[Path]:
    """Serialize lifecycle read/compare/write across local processes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_suffix(path.suffix + ".lock")
    with lock_path.open("a+", encoding="utf-8") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try:
            yield lock_path
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def _empty_state(
    *,
    ticker: str,
    adjustment: str,
    state_identity: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "ticker": ticker,
        "adjustment": adjustment,
        "state_identity": state_identity,
        "technical_as_of": None,
        "active": {},
        "withdrawn": {},
    }


def _read_state_snapshot(
    path: Path,
    *,
    default: dict[str, Any],
    state_identity: dict[str, Any],
) -> tuple[dict[str, Any], str | None]:
    if not path.exists():
        return dict(default), None
    raw = path.read_bytes()
    state = json.loads(raw.decode("utf-8"))
    if state.get("schema_version") != STATE_SCHEMA_VERSION:
        raise ValueError("state schema version 不匹配")
    if (
        state.get("state_identity", {}).get("bundle_hash")
        != state_identity["bundle_hash"]
    ):
        raise ValueError("state identity 与当前 commit/config bundle 不匹配")
    return state, hashlib.sha256(raw).hexdigest()


def _lifecycle_failure(
    *,
    path: Path,
    state_identity: dict[str, Any],
    technical_as_of: str | None,
    source_run_identity: Any,
    reason: str,
    reason_code: str,
    previous_as_of: str | None = None,
    lock_path: Path | None = None,
) -> dict[str, Any]:
    result = {
        "status": "unavailable",
        "reason_code": reason_code,
        "state_path": str(path.resolve()),
        "state_identity": state_identity,
        "reason": reason,
        "technical_as_of": technical_as_of,
        "previous_technical_as_of": previous_as_of,
        "source_run_identity": source_run_identity,
        "active_elements": [],
        "withdrawn_elements": [],
        "write_performed": False,
    }
    if lock_path is not None:
        result["state_lock_path"] = str(lock_path.resolve())
    return result


def _apply_structure_lifecycle_once(
    chan_result: dict[str, Any],
    *,
    ticker: str,
    adjustment: str,
    path: Path,
    state_identity: dict[str, Any],
    observed_at: str,
    technical_as_of: str,
    write_state: bool,
    source_run_identity: Any,
    lock_path: Path | None,
) -> dict[str, Any]:
    default_state = _empty_state(
        ticker=ticker,
        adjustment=adjustment,
        state_identity=state_identity,
    )
    try:
        previous, baseline_cas = _read_state_snapshot(
            path,
            default=default_state,
            state_identity=state_identity,
        )
    except Exception as exc:
        return _lifecycle_failure(
            path=path,
            state_identity=state_identity,
            technical_as_of=technical_as_of,
            source_run_identity=source_run_identity,
            reason=f"状态文件不可解析，已停止写入: {type(exc).__name__}: {exc}",
            reason_code="state_read_failed",
            lock_path=lock_path,
        )

    previous_as_of = previous.get("technical_as_of")
    try:
        current_cutoff = pd.Timestamp(technical_as_of).date()
        previous_cutoff = pd.Timestamp(previous_as_of).date() if previous_as_of else None
    except Exception as exc:
        return _lifecycle_failure(
            path=path,
            state_identity=state_identity,
            technical_as_of=technical_as_of,
            source_run_identity=source_run_identity,
            reason=f"无法解析 state cutoff，已停止写入: {type(exc).__name__}: {exc}",
            reason_code="invalid_technical_as_of",
            previous_as_of=previous_as_of,
            lock_path=lock_path,
        )
    if current_cutoff is None:
        return _lifecycle_failure(
            path=path,
            state_identity=state_identity,
            technical_as_of=technical_as_of,
            source_run_identity=source_run_identity,
            reason="缺少 technical_as_of，已停止写入",
            reason_code="missing_technical_as_of",
            previous_as_of=previous_as_of,
            lock_path=lock_path,
        )
    if previous_cutoff is not None and current_cutoff < previous_cutoff:
        return _lifecycle_failure(
            path=path,
            state_identity=state_identity,
            technical_as_of=technical_as_of,
            source_run_identity=source_run_identity,
            reason="当前 cutoff 早于 state cutoff；拒绝历史回放污染现行生命周期",
            reason_code="out_of_order_cutoff",
            previous_as_of=previous_as_of,
            lock_path=lock_path,
        )

    data_revision = bool(
        previous_cutoff is not None
        and current_cutoff == previous_cutoff
        and previous.get("input_digest")
        and previous.get("input_digest") != chan_result.get("input_digest")
    )
    current_elements: list[dict[str, Any]] = []
    for profile_name in PROFILE_ORDER:
        profile = chan_result.get("profiles", {}).get(profile_name, {})
        current_elements.extend(_all_elements(profile) if profile else [])

    previous_active = previous.get("active", {})
    previous_withdrawn = previous.get("withdrawn", {})
    active: dict[str, Any] = {}
    changed_count = 0
    new_count = 0
    reappeared_count = 0
    for element in current_elements:
        element_id = element["element_id"]
        old = previous_active.get(element_id)
        reappeared = False
        if old is None and element_id in previous_withdrawn:
            old = previous_withdrawn[element_id]
            reappeared = True
            reappeared_count += 1
        if old is None:
            first_seen = observed_at
            last_changed = observed_at
            new_count += 1
        else:
            first_seen = old.get("first_seen", observed_at)
            if old.get("content_hash") == element["content_hash"] and not reappeared:
                last_changed = old.get("last_changed", first_seen)
            else:
                last_changed = observed_at
                changed_count += 1
        active[element_id] = {
            **element,
            "first_seen": first_seen,
            "last_changed": last_changed,
            "withdrawn": None,
            "reappeared": reappeared,
        }

    withdrawn: dict[str, Any] = {
        key: value
        for key, value in previous_withdrawn.items()
        if key not in active
    }
    newly_withdrawn = 0
    for element_id, old in previous_active.items():
        if element_id in active:
            continue
        withdrawn[element_id] = {
            **old,
            "withdrawn": old.get("withdrawn") or observed_at,
        }
        newly_withdrawn += 1

    state = {
        "schema_version": STATE_SCHEMA_VERSION,
        "state_revision": int(previous.get("state_revision", 0)) + 1,
        "ticker": ticker,
        "adjustment": adjustment,
        "state_identity": state_identity,
        "updated_at": observed_at,
        "technical_as_of": technical_as_of,
        "input_digest": chan_result.get("input_digest"),
        "data_revision": data_revision,
        "data_revision_count": int(previous.get("data_revision_count", 0))
        + int(data_revision),
        "source_run_identity": source_run_identity,
        "engine_commit": chan_result.get("engine", {}).get("upstream_commit"),
        "profile_config_hashes": {
            name: chan_result.get("profiles", {}).get(name, {}).get("config_hash")
            for name in PROFILE_ORDER
        },
        "active": active,
        "withdrawn": withdrawn,
    }

    committed_state_sha256: str | None = None
    if write_state:
        try:
            latest, latest_cas = _read_state_snapshot(
                path,
                default=default_state,
                state_identity=state_identity,
            )
            latest_as_of = latest.get("technical_as_of")
            latest_cutoff = pd.Timestamp(latest_as_of).date() if latest_as_of else None
        except Exception as exc:
            return _lifecycle_failure(
                path=path,
                state_identity=state_identity,
                technical_as_of=technical_as_of,
                source_run_identity=source_run_identity,
                reason=f"写前 state 重读失败: {type(exc).__name__}: {exc}",
                reason_code="state_cas_read_failed",
                previous_as_of=previous_as_of,
                lock_path=lock_path,
            )
        if latest_cutoff is not None and current_cutoff < latest_cutoff:
            return _lifecycle_failure(
                path=path,
                state_identity=state_identity,
                technical_as_of=technical_as_of,
                source_run_identity=source_run_identity,
                reason="写前发现更晚 cutoff；拒绝旧运行覆盖新状态",
                reason_code="out_of_order_cutoff",
                previous_as_of=latest_as_of,
                lock_path=lock_path,
            )
        if latest_cas != baseline_cas:
            return _lifecycle_failure(
                path=path,
                state_identity=state_identity,
                technical_as_of=technical_as_of,
                source_run_identity=source_run_identity,
                reason="写前 state CAS 已变化；拒绝基于过期快照提交",
                reason_code="state_cas_conflict",
                previous_as_of=latest_as_of,
                lock_path=lock_path,
            )
        try:
            committed_state_sha256 = _atomic_json_write(path, state)
        except Exception as exc:
            return _lifecycle_failure(
                path=path,
                state_identity=state_identity,
                technical_as_of=technical_as_of,
                source_run_identity=source_run_identity,
                reason=f"state 原子写入失败: {type(exc).__name__}: {exc}",
                reason_code="state_write_failed",
                previous_as_of=previous_as_of,
                lock_path=lock_path,
            )

    result = {
        "status": "complete",
        "state_path": str(path.resolve()),
        "state_identity": state_identity,
        "state_revision": state["state_revision"],
        "state_sha256": committed_state_sha256,
        "observed_at": observed_at,
        "technical_as_of": technical_as_of,
        "previous_technical_as_of": previous_as_of,
        "data_revision": data_revision,
        "source_run_identity": source_run_identity,
        "active_elements": list(active.values()),
        "withdrawn_elements": list(withdrawn.values()),
        "counts": {
            "active": len(active),
            "new": new_count,
            "changed": changed_count,
            "reappeared": reappeared_count,
            "newly_withdrawn": newly_withdrawn,
            "withdrawn_total": len(withdrawn),
        },
        "write_performed": write_state,
    }
    if lock_path is not None:
        result["state_lock_path"] = str(lock_path.resolve())
    return result


def apply_structure_lifecycle(
    chan_result: dict[str, Any],
    *,
    ticker: str,
    adjustment: str,
    state_dir: Path,
    write_state: bool = True,
    observed_at: str | None = None,
    technical_as_of: str | None = None,
    source_run_identity: Any = None,
) -> dict[str, Any]:
    observed_at = observed_at or datetime.now(timezone.utc).isoformat()
    if technical_as_of is None:
        technical_as_of = (
            chan_result.get("profiles", {})
            .get("strict", {})
            .get("timeframes", {})
            .get("daily", {})
            .get("as_of")
        )
    if technical_as_of is None:
        # Backward-compatible direct API fallback.  The production CLI always
        # passes the normalized daily-frame cutoff explicitly.
        technical_as_of = pd.Timestamp(observed_at).date().isoformat()
    state_identity = _state_identity(chan_result)
    path = _state_path(
        state_dir,
        ticker,
        adjustment,
        state_identity["bundle_hash"],
    )
    if chan_result.get("status") == "unavailable":
        return _lifecycle_failure(
            path=path,
            state_identity=state_identity,
            technical_as_of=technical_as_of,
            source_run_identity=source_run_identity,
            reason="chan.py 结构不可用，未变更持久化状态",
            reason_code="chan_runtime_unavailable",
        )

    common = {
        "chan_result": chan_result,
        "ticker": ticker,
        "adjustment": adjustment,
        "path": path,
        "state_identity": state_identity,
        "observed_at": observed_at,
        "technical_as_of": technical_as_of,
        "write_state": write_state,
        "source_run_identity": source_run_identity,
    }
    if not write_state:
        return _apply_structure_lifecycle_once(**common, lock_path=None)
    with _state_file_lock(path) as lock_path:
        return _apply_structure_lifecycle_once(**common, lock_path=lock_path)


def _period_parent_child(
    parent: pd.DataFrame,
    child: pd.DataFrame,
    parent_period: str,
) -> list[dict[str, Any]]:
    parent_rows = parent.copy()
    child_rows = child.copy()
    parent_rows["_period"] = pd.to_datetime(parent_rows["dt"]).dt.to_period(parent_period)
    child_rows["_period"] = pd.to_datetime(child_rows["dt"]).dt.to_period(parent_period)
    parent_map = {
        period: pd.Timestamp(group["dt"].iloc[-1]).date().isoformat()
        for period, group in parent_rows.groupby("_period", sort=True)
    }
    result = []
    for period, group in child_rows.groupby("_period", sort=True):
        result.append(
            {
                "period": str(period),
                "parent_as_of": parent_map.get(period),
                "children_as_of": [
                    pd.Timestamp(value).date().isoformat() for value in group["dt"]
                ],
                "child_count": int(len(group)),
            }
        )
    return result


def _latest_stable_zone(stable: Iterable[dict[str, Any]], timeframe: str) -> dict[str, Any] | None:
    candidates = [
        item
        for item in stable
        if item.get("timeframe") == timeframe
        and item.get("layer") == "zone"
        and item.get("confirmed")
    ]
    return sorted(candidates, key=lambda item: (item.get("end") or "", item.get("index", -1)))[-1] if candidates else None


def _zone_relation(parent: dict[str, Any] | None, child: dict[str, Any] | None) -> dict[str, Any]:
    if parent is None or child is None:
        return {
            "status": "unavailable",
            "relationship": "not_available",
            "reason": "父级或子级缺少跨参数稳定的已确认中枢",
        }
    pl, pu = parent.get("lower"), parent.get("upper")
    cl, cu = child.get("lower"), child.get("upper")
    if None in {pl, pu, cl, cu}:
        relationship = "not_available"
        status = "unavailable"
    elif cl >= pl and cu <= pu:
        relationship = "child_inside_parent"
        status = "complete"
    elif pl >= cl and pu <= cu:
        relationship = "child_contains_parent"
        status = "complete"
    elif max(pl, cl) <= min(pu, cu):
        relationship = "overlap"
        status = "complete"
    else:
        relationship = "disjoint"
        status = "complete"
    return {
        "status": status,
        "relationship": relationship,
        "parent_element_id": parent.get("element_id"),
        "child_element_id": child.get("element_id"),
        "parent_interval": [pl, pu],
        "child_interval": [cl, cu],
        "interpretation": "structural_context_not_directional_signal",
    }


def build_timeframe_context(frame: pd.DataFrame, chan_result: dict[str, Any]) -> dict[str, Any]:
    daily = resample_bars(frame, "daily")
    weekly = resample_bars(frame, "weekly")
    monthly = resample_bars(frame, "monthly")
    stable = chan_result.get("profile_stability", {}).get("stable_elements", [])
    monthly_zone = _latest_stable_zone(stable, "monthly")
    weekly_zone = _latest_stable_zone(stable, "weekly")
    daily_zone = _latest_stable_zone(stable, "daily")
    return {
        "mapping_method": "local_calendar_aggregation_over_same_normalized_daily_bars",
        "monthly_to_weekly": _period_parent_child(monthly, weekly, "M"),
        "weekly_to_daily": _period_parent_child(weekly, daily, "W-FRI"),
        "interval_nesting": {
            "monthly_weekly": _zone_relation(monthly_zone, weekly_zone),
            "weekly_daily": _zone_relation(weekly_zone, daily_zone),
        },
    }


def _latest_stable_bi(stable: Iterable[dict[str, Any]], timeframe: str) -> dict[str, Any] | None:
    candidates = [
        item
        for item in stable
        if item.get("timeframe") == timeframe
        and item.get("layer") == "bi"
        and item.get("confirmed")
    ]
    return sorted(candidates, key=lambda item: (item.get("end") or "", item.get("index", -1)))[-1] if candidates else None


def compare_engines(czsc_result: dict[str, Any], chan_result: dict[str, Any]) -> dict[str, Any]:
    if chan_result.get("status") == "unavailable":
        return {
            "status": "unavailable",
            "method": "semantic_anchor_comparison_not_structure_count_equality",
            "reason": chan_result.get("reason", "chan.py unavailable"),
            "comparisons": [],
        }
    stability = chan_result.get("profile_stability", {})
    if stability.get("status") == "disputed":
        return {
            "status": "disputed",
            "method": "semantic_anchor_comparison_not_structure_count_equality",
            "reason": "chan.py strict/broad 在关键方向锚点上冲突",
            "comparisons": stability.get("critical_direction_checks", []),
        }
    if stability.get("status") == "unavailable":
        return {
            "status": "unavailable",
            "method": "semantic_anchor_comparison_not_structure_count_equality",
            "reason": "chan.py 参数稳定性交集不可用",
            "comparisons": [],
        }

    stable = stability.get("stable_elements", [])
    comparisons: list[dict[str, Any]] = []
    critical_statuses: list[str] = []
    for timeframe in TIMEFRAME_ORDER:
        czsc_bi = czsc_result.get("timeframes", {}).get(timeframe, {}).get("last_completed_bi")
        chan_bi = _latest_stable_bi(stable, timeframe)
        if not czsc_bi or not chan_bi:
            status = "unavailable" if timeframe in {"monthly", "weekly"} else "degraded"
            reason = "至少一方缺少可比较的已确认笔锚点"
            endpoint_gap_days = None
        else:
            directions_match = czsc_bi.get("direction") == chan_bi.get("direction")
            endpoint_gap_days = abs(
                (pd.Timestamp(czsc_bi.get("end")) - pd.Timestamp(chan_bi.get("end"))).days
            )
            tolerance = {"daily": 10, "weekly": 45, "monthly": 95}[timeframe]
            if not directions_match:
                status = "disputed"
                reason = "双方最后已确认笔方向相反"
            elif endpoint_gap_days > tolerance:
                status = "degraded"
                reason = "方向一致，但结构端点日期差异超过周期容差"
            else:
                status = "complete"
                reason = "最后已确认笔方向一致，端点日期在周期容差内"
        comparisons.append(
            {
                "timeframe": timeframe,
                "status": status,
                "anchor": "latest_confirmed_bi_direction_and_endpoint",
                "czsc": czsc_bi,
                "chan_py_stable": chan_bi,
                "endpoint_gap_days": endpoint_gap_days,
                "reason": reason,
                "count_difference_used_for_status": False,
            }
        )
        if timeframe in {"monthly", "weekly"}:
            critical_statuses.append(status)

    if "disputed" in critical_statuses:
        overall = "disputed"
    elif "unavailable" in critical_statuses:
        overall = "unavailable"
    elif "degraded" in critical_statuses or stability.get("status") == "degraded":
        overall = "degraded"
    else:
        overall = "complete"
    return {
        "status": overall,
        "method": "semantic_anchor_comparison_not_structure_count_equality",
        "comparisons": comparisons,
        "profile_stability_status": stability.get("status"),
        "note": "保留双方结构；笔、线段或中枢数量差异本身不判 disputed。",
    }


def _path_is_within_casefold(path: Path, parent: Path) -> bool:
    """Resolve symlinks and conservatively protect case-insensitive aliases."""
    path_parts = tuple(part.casefold() for part in path.expanduser().resolve().parts)
    parent_parts = tuple(
        part.casefold() for part in parent.expanduser().resolve().parts
    )
    return path_parts[: len(parent_parts)] == parent_parts


def _protected_output_label(path: Path) -> str | None:
    for label, protected in (
        ("raw", REPO_ROOT / "raw"),
        ("wiki", REPO_ROOT / "wiki"),
    ):
        if _path_is_within_casefold(path, protected):
            return label
    return None


def _prepare_matplotlib_config_dir() -> Path:
    configured = os.environ.get("MPLCONFIGDIR")
    path = (
        Path(configured).expanduser()
        if configured
        else REPO_ROOT / ".work" / "matplotlib"
    )
    protected_label = _protected_output_label(path)
    if protected_label is not None:
        raise ChanAdapterUnavailable(
            "MPLCONFIGDIR 不得指向 "
            f"{protected_label}/ 或其大小写/符号链接别名: {path.resolve()}"
        )
    path = path.resolve()
    path.mkdir(parents=True, exist_ok=True)
    os.environ["MPLCONFIGDIR"] = str(path)
    return path


def _load_native_plot_driver(runtime: dict[str, Any]) -> tuple[Any, Any]:
    """Load the pinned static plot driver after forcing a headless backend."""
    root = Path(runtime["root"])
    required = ("Plot/PlotDriver.py", "Plot/PlotMeta.py")
    missing = [name for name in required if not (root / name).is_file()]
    if missing:
        raise ChanAdapterUnavailable(
            f"chan.py 静态绘图模块不完整，缺少: {', '.join(missing)}"
        )

    _prepare_matplotlib_config_dir()
    os.environ["MPLBACKEND"] = "Agg"
    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt

    existing = sys.modules.get("Plot.PlotDriver")
    if existing is not None:
        origin = Path(getattr(existing, "__file__", "")).resolve()
        if root not in origin.parents:
            raise ChanAdapterUnavailable(
                f"检测到来自其他路径的 Plot.PlotDriver 模块: {origin}"
            )

    sys.path.insert(0, str(root))
    try:
        plot_module = importlib.import_module("Plot.PlotDriver")
    except Exception as exc:
        raise ChanAdapterUnavailable(
            f"加载 chan.py 静态绘图模块失败: {type(exc).__name__}: {exc}"
        ) from exc
    finally:
        if sys.path and sys.path[0] == str(root):
            sys.path.pop(0)
    origin = Path(getattr(plot_module, "__file__", "")).resolve()
    if root not in origin.parents:
        raise ChanAdapterUnavailable(
            f"Plot.PlotDriver 来源路径不匹配: {origin}"
        )
    return plot_module.CPlotDriver, plt


def _atomic_save_figure(figure: Any, output_path: Path) -> tuple[str, int]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".png",
            delete=False,
        ) as stream:
            temporary_path = Path(stream.name)
        figure.savefig(
            temporary_path,
            dpi=150,
            format="png",
            bbox_inches="tight",
        )
        with temporary_path.open("rb+") as stream:
            stream.flush()
            os.fsync(stream.fileno())
        temporary_path.replace(output_path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()
    digest = hashlib.sha256(output_path.read_bytes()).hexdigest()
    return digest, output_path.stat().st_size


def render_native_chan_charts(
    frame: pd.DataFrame,
    output_paths: dict[str, Path],
    *,
    chan_path: Path | str | None = None,
    profile: str = "strict",
) -> dict[str, Any]:
    """Render three pinned CPlotDriver charts without invoking a DataAPI."""
    input_digest = normalized_frame_digest(frame)
    profile_config = CHAN_PROFILES.get(profile)
    config_hash = (
        _profile_hash(profile, profile_config) if profile_config is not None else None
    )
    artifact: dict[str, Any] = {
        "status": "unavailable",
        "renderer": "chan.py.Plot.PlotDriver.CPlotDriver",
        "profile": profile,
        "upstream_commit": EXPECTED_CHAN_COMMIT,
        "config_hash": config_hash,
        "input_digest": input_digest,
        "input_contract": "normalized_local_bars_only_no_chan_dataapi",
        "upstream_dataapi_used": False,
        "static": True,
        "animation": False,
        "interactive": False,
        "bsp_interpretation": "neutral_candidate_not_trade_signal",
        "plot_layers": list(NATIVE_PLOT_LAYERS),
        "charts": {},
    }
    unsafe_paths = {
        timeframe: (path, _protected_output_label(path))
        for timeframe, path in output_paths.items()
        if _protected_output_label(path) is not None
    }
    if unsafe_paths:
        details = ", ".join(
            f"{timeframe}=>{label}/"
            for timeframe, (_, label) in sorted(unsafe_paths.items())
        )
        reason = f"native chart 输出不得指向 raw/ 或 wiki/: {details}"
        artifact["reason_code"] = "unsafe_output_path"
        artifact["reason"] = reason
        for timeframe in TIMEFRAME_ORDER:
            path = output_paths.get(timeframe)
            artifact["charts"][timeframe] = {
                "status": "unavailable",
                "timeframe": timeframe,
                "path": None,
                "intended_path": str(path.resolve()) if path is not None else None,
                "reason": reason,
            }
        return artifact
    if profile_config is None:
        reason = f"未知 chan.py profile: {profile}"
        artifact["reason"] = reason
        for timeframe in TIMEFRAME_ORDER:
            path = output_paths.get(timeframe)
            artifact["charts"][timeframe] = {
                "status": "unavailable",
                "timeframe": timeframe,
                "path": None,
                "intended_path": str(path.resolve()) if path is not None else None,
                "reason": reason,
            }
        return artifact

    root = resolve_chan_root(chan_path)
    artifact["source_path"] = str(root)
    try:
        runtime = _load_runtime(root)
        plot_driver_class, plt = _load_native_plot_driver(runtime)
        artifact["upstream_commit"] = runtime["commit"]
    except Exception as exc:
        reason = f"{type(exc).__name__}: {exc}"
        artifact["reason"] = reason
        for timeframe in TIMEFRAME_ORDER:
            path = output_paths.get(timeframe)
            artifact["charts"][timeframe] = {
                "status": "unavailable",
                "timeframe": timeframe,
                "path": None,
                "intended_path": str(path.resolve()) if path is not None else None,
                "reason": reason,
            }
        return artifact

    plot_config = {layer: True for layer in NATIVE_PLOT_LAYERS}
    visible_bars = {"monthly": 120, "weekly": 180, "daily": 260}
    errors: dict[str, str] = {}
    for timeframe in TIMEFRAME_ORDER:
        output_path = output_paths.get(timeframe)
        if output_path is None:
            reason = f"缺少 {timeframe} 输出路径"
            errors[timeframe] = reason
            artifact["charts"][timeframe] = {
                "status": "unavailable",
                "timeframe": timeframe,
                "path": None,
                "intended_path": None,
                "reason": reason,
            }
            continue

        figure = None
        try:
            bars, _, analyzer, _ = _build_analyzer(
                frame,
                timeframe=timeframe,
                profile_config=profile_config,
                runtime=runtime,
            )
            plot_driver = plot_driver_class(
                analyzer,
                plot_config=plot_config,
                plot_para={
                    "figure": {
                        "w": 20,
                        "h": 10,
                        "x_range": visible_bars[timeframe],
                        "x_tick_num": 12,
                        "grid": "xy",
                    },
                    # Old zone labels are not clipped by the upstream driver.
                    # Keep values on the longer-horizon views, but avoid labels
                    # outside the visible one-year daily window.
                    "zs": {"show_text": timeframe != "daily"},
                },
            )
            figure = plot_driver.figure
            figure.suptitle(
                (
                    f"chan.py {profile} {timeframe} structure audit — "
                    "BSP labels are neutral morphology candidates, not trade signals"
                ),
                fontsize=13,
            )
            figure.text(
                0.01,
                0.005,
                (
                    f"commit={runtime['commit'][:12]}  "
                    f"config={config_hash[:12]}  input={input_digest[:12]}  "
                    "static/non-interactive"
                ),
                fontsize=8,
                color="#455a64",
            )
            digest, byte_count = _atomic_save_figure(figure, output_path)
            artifact["charts"][timeframe] = {
                "status": "complete",
                "timeframe": timeframe,
                "path": str(output_path.resolve()),
                "sha256": digest,
                "bytes": byte_count,
                "format": "png",
                "bar_count": int(len(bars)),
                "as_of": pd.Timestamp(bars["dt"].max()).date().isoformat(),
                "visible_bar_limit": visible_bars[timeframe],
            }
        except Exception as exc:
            reason = f"{type(exc).__name__}: {exc}"
            errors[timeframe] = reason
            artifact["charts"][timeframe] = {
                "status": "unavailable",
                "timeframe": timeframe,
                "path": None,
                "intended_path": str(output_path.resolve()),
                "reason": reason,
            }
        finally:
            if figure is not None:
                plt.close(figure)

    completed_count = sum(
        chart.get("status") == "complete"
        for chart in artifact["charts"].values()
    )
    if errors:
        artifact["status"] = "degraded" if completed_count else "unavailable"
        artifact["errors"] = errors
        artifact["reason"] = "一个或多个 chan.py 原生静态图生成失败"
    else:
        artifact["status"] = "complete"
    return artifact


def render_audit_chart(
    frame: pd.DataFrame,
    chan_result: dict[str, Any],
    output_path: Path,
) -> dict[str, Any]:
    """Render a static, non-trading audit chart for the strict profile."""
    protected_label = _protected_output_label(output_path)
    if protected_label is not None:
        return {
            "status": "unavailable",
            "reason_code": "unsafe_output_path",
            "path": None,
            "intended_path": str(output_path.resolve()),
            "reason": (
                "audit chart 输出不得指向 "
                f"{protected_label}/ 或其大小写/符号链接别名"
            ),
        }
    if chan_result.get("status") == "unavailable":
        return {
            "status": "unavailable",
            "path": None,
            "intended_path": str(output_path.resolve()),
            "reason": "chan.py 结构不可用",
        }
    try:
        _prepare_matplotlib_config_dir()
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.dates as mdates
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle
    except Exception as exc:
        return {
            "status": "unavailable",
            "path": None,
            "intended_path": str(output_path.resolve()),
            "reason": f"matplotlib 不可用: {type(exc).__name__}: {exc}",
        }

    strict = chan_result.get("profiles", {}).get("strict", {})
    fig, axes = plt.subplots(3, 1, figsize=(16, 14), constrained_layout=True)
    limits = {"monthly": 120, "weekly": 180, "daily": 260}
    for axis, timeframe in zip(axes, TIMEFRAME_ORDER):
        bars = resample_bars(frame, timeframe).tail(limits[timeframe]).copy()
        bars["dt"] = pd.to_datetime(bars["dt"])
        axis.plot(bars["dt"], bars["close"], color="#263238", linewidth=1.0, label="close")
        axis.vlines(
            bars["dt"],
            bars["low"],
            bars["high"],
            color="#90a4ae",
            linewidth=0.55,
            alpha=0.65,
        )
        elements = strict.get("timeframes", {}).get(timeframe, {}).get("elements", [])
        start_bound = bars["dt"].min()
        for element in elements:
            start = pd.Timestamp(element.get("start")) if element.get("start") else None
            end = pd.Timestamp(element.get("end")) if element.get("end") else None
            if end is not None and end < start_bound:
                continue
            confirmed = bool(element.get("confirmed"))
            linestyle = "-" if confirmed else "--"
            alpha = 0.9 if confirmed else 0.55
            if element.get("layer") in {"bi", "segment"} and start is not None and end is not None:
                axis.plot(
                    [start, end],
                    [element.get("start_value"), element.get("end_value")],
                    color="#1565c0" if element["layer"] == "bi" else "#6a1b9a",
                    linewidth=1.2 if element["layer"] == "bi" else 2.0,
                    linestyle=linestyle,
                    alpha=alpha,
                )
            elif element.get("layer") == "zone" and start is not None and end is not None:
                lower, upper = element.get("lower"), element.get("upper")
                if lower is not None and upper is not None:
                    left = mdates.date2num(max(start, start_bound))
                    right = mdates.date2num(end)
                    axis.add_patch(
                        Rectangle(
                            (left, lower),
                            max(right - left, 0.5),
                            upper - lower,
                            facecolor="#ffb300",
                            edgecolor="#ef6c00",
                            alpha=0.15 if confirmed else 0.08,
                            linestyle=linestyle,
                        )
                    )
            elif element.get("layer") == "bsp" and end is not None:
                marker = "^" if element.get("morphology_side") == "lower_turning_structure" else "v"
                axis.scatter(
                    [end],
                    [element.get("price")],
                    marker=marker,
                    s=34,
                    color="#2e7d32" if marker == "^" else "#c62828",
                    alpha=alpha,
                )
        axis.set_title(f"{timeframe} — strict profile (solid=confirmed, dashed=provisional)")
        axis.grid(alpha=0.18)
        axis.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        axis.set_ylabel("CNY/share")
    fig.suptitle(
        "Static structure audit — neutral BSP markers, not trading signals",
        fontsize=14,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".png",
            delete=False,
        ) as stream:
            temporary_path = Path(stream.name)
        fig.savefig(temporary_path, dpi=150, format="png")
        temporary_path.replace(output_path)
    finally:
        plt.close(fig)
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()
    digest = hashlib.sha256(output_path.read_bytes()).hexdigest()
    return {
        "status": "complete",
        "path": str(output_path.resolve()),
        "sha256": digest,
        "bytes": output_path.stat().st_size,
        "profile": "strict",
        "format": "png",
        "static": True,
        "animation": False,
        "bsp_interpretation": "neutral_candidate_not_trade_signal",
    }


__all__ = [
    "CHAN_PROFILES",
    "DEFAULT_CHAN_ROOT",
    "EXPECTED_CHAN_COMMIT",
    "NATIVE_PLOT_LAYERS",
    "analyze_chan_profiles",
    "apply_structure_lifecycle",
    "build_timeframe_context",
    "compare_engines",
    "normalized_frame_digest",
    "render_audit_chart",
    "render_native_chan_charts",
    "resolve_chan_root",
]
