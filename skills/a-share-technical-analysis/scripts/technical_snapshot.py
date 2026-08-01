#!/usr/bin/env python3
"""Generate auditable JSON and Markdown A-share technical snapshots."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

import pandas as pd

from czsc_bridge import analyze_multitimeframe
from chan_bridge import (
    EXPECTED_CHAN_COMMIT,
    NATIVE_PLOT_LAYERS,
    analyze_chan_profiles,
    apply_structure_lifecycle,
    build_timeframe_context,
    compare_engines,
    normalized_frame_digest,
    render_audit_chart,
    render_native_chan_charts,
)
from market_data import (
    MarketDataResult,
    drop_unfinished_daily_bar,
    get_market_data,
    parse_ticker,
    sanitize_provider_error,
    save_cache,
    validate_bars,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
STATUS_PRIORITY = {"complete": 0, "degraded": 1, "disputed": 2, "unavailable": 3}


def _json_default(value: Any) -> Any:
    if isinstance(value, (pd.Timestamp, date)):
        return value.isoformat()
    if hasattr(value, "item"):
        return value.item()
    raise TypeError(f"无法序列化 {type(value).__name__}")


def _offline_result(
    ticker: str,
    csv_path: Path,
    start: str,
    end: str,
    adjustment: str,
) -> MarketDataResult:
    mapping = parse_ticker(ticker)
    frame = pd.read_csv(csv_path)
    if "dt" not in frame.columns:
        raise ValueError("offline CSV 缺少 dt 字段")
    try:
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
    except ValueError as exc:
        raise ValueError("--start/--end 必须使用 YYYY-MM-DD") from exc
    if start_date > end_date:
        raise ValueError("--start 不能晚于 --end")

    frame["dt"] = pd.to_datetime(frame["dt"], errors="coerce")
    if frame["dt"].isna().any():
        raise ValueError("offline CSV 含无法解析的 dt")
    if "symbol" not in frame:
        frame["symbol"] = mapping.czsc_symbol
    else:
        symbols = {
            str(value).strip().upper()
            for value in frame["symbol"].dropna().tolist()
        }
        if frame["symbol"].isna().any() or symbols != {mapping.czsc_symbol}:
            raise ValueError(
                "offline CSV symbol 与 --ticker 不一致："
                f"expected={mapping.czsc_symbol}, actual={sorted(symbols)}"
            )
        frame["symbol"] = mapping.czsc_symbol

    dates = frame["dt"].dt.date
    frame = frame.loc[(dates >= start_date) & (dates <= end_date)].reset_index(drop=True)
    if frame.empty:
        raise ValueError("offline CSV 在请求的 --start/--end 区间内没有 K 线")
    frame, unfinished_removed = drop_unfinished_daily_bar(frame)
    if frame.empty:
        raise ValueError("移除未完成的当日日 K 后没有可用 K 线")
    quality = validate_bars(frame, minimum_rows=120, expected_end=end)
    return MarketDataResult(
        ticker=mapping.ticker,
        data=frame,
        provider="offline_fixture",
        adjustment=adjustment,
        requested_start=start,
        requested_end=end,
        fetched_at=pd.Timestamp.now(tz="UTC").isoformat(),
        data_quality_status="degraded" if quality["status"] == "complete" else quality["status"],
        quality_report=quality,
        cross_check={
            "status": "unavailable",
            "overlap_rows": 0,
            "reason": "offline fixture 未进行在线双源核对",
        },
        package_versions={},
        warnings=[
            "离线 fixture 仅用于复现或测试，不代表当前行情",
            *(
                ["已移除 15:10 Asia/Shanghai 前的未完成当日日 K"]
                if unfinished_removed
                else []
            ),
        ],
    )


def build_payload(
    result: MarketDataResult,
    *,
    chan_path: Path | str | None = None,
    state_dir: Path | None = None,
    write_state: bool = False,
) -> dict[str, Any]:
    """Build a dual-engine payload without fetching data or persisting state.

    ``write_state`` records the caller's persistence intent.  The CLI commits
    an eligible lifecycle state only after the immutable run artifacts exist.
    """
    czsc_analysis = analyze_multitimeframe(result.data)
    chan_analysis = analyze_chan_profiles(result.data, chan_path=chan_path)
    engine_consistency = compare_engines(czsc_analysis, chan_analysis)
    timeframe_context = build_timeframe_context(result.data, chan_analysis)
    if state_dir is None:
        lifecycle = {
            "status": "not_persisted",
            "reason": "build_payload 未提供 state_dir",
            "write_performed": False,
            "active_elements": [],
            "withdrawn_elements": [],
        }
    else:
        lifecycle = apply_structure_lifecycle(
            chan_analysis,
            ticker=result.ticker,
            adjustment=result.adjustment,
            state_dir=state_dir,
            write_state=False,
            technical_as_of=czsc_analysis["technical_as_of"],
        )
        lifecycle["state_write_requested"] = write_state
        lifecycle["state_write_eligible"] = bool(
            write_state and result.data_quality_status == "complete"
        )
        lifecycle["commit_phase"] = "deferred_until_after_analysis_artifacts"
        if write_state and result.data_quality_status != "complete":
            lifecycle["write_blocked_reason"] = (
                "lifecycle state requires data_quality_status=complete; "
                f"actual={result.data_quality_status}"
            )

    analysis = {
        **czsc_analysis,
        "normalized_input": {
            "digest_sha256": normalized_frame_digest(result.data),
            "row_count": int(len(result.data)),
            "adjustment": result.adjustment,
            "contract": "one normalized frame shared by CZSC and chan.py",
        },
        "chan_py": chan_analysis,
        "profile_stability": chan_analysis.get("profile_stability", {}),
        "engine_consistency": engine_consistency,
        "timeframe_context": timeframe_context,
        "structure_lifecycle": lifecycle,
    }

    status_checks = {
        "data_quality_status": result.data_quality_status,
        "engine_consistency_status": engine_consistency["status"],
        "chan_structure_status": chan_analysis["status"],
        "profile_stability_status": chan_analysis.get("profile_stability", {}).get(
            "status", "unavailable"
        ),
    }
    if lifecycle.get("status") == "unavailable":
        status_checks["structure_lifecycle_status"] = "unavailable"
    blockers = [
        {"layer": layer, "status": status}
        for layer, status in status_checks.items()
        if status in {"disputed", "unavailable"}
    ]
    directional_allowed = not blockers
    overall_status = max(
        status_checks.values(),
        key=lambda value: STATUS_PRIORITY.get(value, STATUS_PRIORITY["unavailable"]),
    )
    return {
        "ticker": result.ticker,
        "listing_regime": "a_share",
        "technical_as_of": analysis["technical_as_of"],
        "adjustment": result.adjustment,
        "market_data": result.manifest(),
        "analysis": analysis,
        "data_quality_status": result.data_quality_status,
        "engine_consistency_status": engine_consistency["status"],
        "chan_structure_status": chan_analysis["status"],
        "profile_stability_status": chan_analysis.get("profile_stability", {}).get(
            "status", "unavailable"
        ),
        "overall_technical_status": overall_status,
        "directional_conclusion_allowed": directional_allowed,
        "directional_conclusion_blockers": blockers,
        "evidence_boundary": {
            "market_data": (
                "verified_fact"
                if result.data_quality_status == "complete"
                else "not_promoted_to_verified_fact"
            ),
            "technical_interpretation": "codex_inference",
            "chan_bsp": "neutral_structure_candidate_not_trade_signal",
        },
        "limitations": [
            "默认只使用已完成日 K；不用于日内交易。",
            (
                "当前周线/月线由已完成日 K 合成，但当周/当月聚合 K "
                "可能尚未完成；只把已完成笔用于结构确认。"
            ),
            (
                "技术结构不能替代基本面、估值、公司事件、"
                "流动性与市场规则核验。"
            ),
            "CZSC 与 chan.py 的笔、线段、中枢只描述历史结构，不保证未来收益。",
            (
                "chan.py 1/1p/2/2s/3a/3b 仅作为中性形态候选，"
                "不翻译为交易动作。"
            ),
            (
                "confirmed 仅表示当前 technical_as_of 下被引擎确认；"
                "追加 K 线后仍可能延长、改变或撤回，必须结合生命周期 state 审计。"
            ),
        ],
        "invalidation_conditions": [
            "新完成的月线或周线笔改变当前方向",
            "价格有效越过报告中的重叠区间边界",
            "除权除息导致前复权历史重算",
            "双源差异扩大、行情过期或数据质量降为 disputed/unavailable",
            "基本面、治理、监管或重大事件改变投资论点",
            "chan.py strict/broad 的关键稳定交集消失或双方引擎方向锚点冲突",
        ],
        "artifacts": {},
    }


def _fmt(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return str(value)


def _relative_markdown_image(path: str, alt_text: str) -> str:
    filename = quote(Path(path).name, safe="._-")
    return f"![{alt_text}](<./{filename}>)"


def render_markdown(payload: dict[str, Any]) -> str:
    market = payload["market_data"]
    analysis = payload["analysis"]
    status = market["data_quality_status"]
    chan = analysis["chan_py"]
    consistency = analysis["engine_consistency"]
    stability = analysis["profile_stability"]
    lifecycle = analysis["structure_lifecycle"]
    conclusion = (
        analysis["allocation_context"]
        if payload["directional_conclusion_allowed"]
        else (
            "关键质量门不允许方向性仓位结论；"
            "仅保留双方结构与差异，等待数据或结构引擎修复。"
        )
    )
    lines = [
        f"# {payload['ticker']} A 股多周期技术面快照",
        "",
        "## 范围与数据质量",
        "",
        f"- Listing Regime：`{payload['listing_regime']}`",
        f"- 技术面截止日：`{payload['technical_as_of']}`",
        f"- 行情源：`{market['provider']}`（BaoStock 主源，AkShare 补充/交叉核对）",
        f"- 复权口径：`{payload['adjustment']}`",
        f"- 数据质量：`{status}`（只描述行情数据）",
        f"- 总体技术状态：`{payload['overall_technical_status']}`（按最弱质量门汇总）",
        f"- 引擎一致性：`{payload['engine_consistency_status']}`（与数据质量分离）",
        f"- chan.py 结构状态：`{payload['chan_structure_status']}`",
        f"- strict/broad 稳定性：`{payload['profile_stability_status']}`",
        (
            f"- 行情区间：`{market.get('actual_start')}` 至 "
            f"`{market.get('actual_end')}`，共 {market.get('row_count')} 根日 K"
        ),
        f"- CZSC：`{analysis['engine']['version']}`，公共接口",
        (
            f"- chan.py：固定 commit `{EXPECTED_CHAN_COMMIT}`；"
            f"状态 `{chan.get('status')}`；不使用上游 DataAPI"
        ),
        f"- 共享归一化输入 SHA-256：`{analysis['normalized_input']['digest_sha256']}`",
        (
            f"- 运行 identity：`{payload.get('run_identity', {}).get('stem', 'not_assigned')}`；"
            f"method bundle `{payload.get('run_identity', {}).get('method_bundle_hash', 'not_assigned')}`"
        ),
        (
            "- 周/月聚合：当前周期可能尚未完成；"
            "已完成笔与当前聚合 K 已分开。"
        ),
        "",
        "## 面向周/月调仓的结论",
        "",
        conclusion,
        (
            "- 方向结论门：`allowed`。"
            if payload["directional_conclusion_allowed"]
            else "- 方向结论门：`blocked`。"
        ),
        "",
        f"- 月线主结构：{analysis['monthly_primary']}",
        f"- 周线仓位节奏：{analysis['weekly_sizing']}",
        f"- 日线执行层：{analysis['daily_execution']}",
        "",
        "## 多周期明细",
        "",
        "| 周期 | 截止日 | 最后完成笔 | MA20 | MA60 | MA120 | ATR14 | 20期量比 | 有效三笔重叠区间 | 价格位置 |",
        "|---|---|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for key in ("monthly", "weekly", "daily"):
        item = analysis["timeframes"][key]
        bi = item["last_completed_bi"] or {}
        zone = item["valid_three_bi_zone"]
        zone_text = (
            f"{_fmt(zone['lower'])}–{_fmt(zone['upper'])}" if zone else "未识别"
        )
        indicator = item["indicators"]
        lines.append(
            "| "
            + " | ".join(
                [
                    item["freq"],
                    item["as_of"],
                    _fmt(bi.get("direction")),
                    _fmt(indicator["ma20"]),
                    _fmt(indicator["ma60"]),
                    _fmt(indicator["ma120"]),
                    _fmt(indicator["atr14"]),
                    _fmt(indicator["volume_ratio_20"]),
                    zone_text,
                    item["position_vs_zone"],
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## 双引擎结构审计",
            "",
            (
                f"- engine_consistency_status：`{consistency.get('status')}`；"
                "使用最后已确认笔的方向与端点语义锚点，不按结构数量简单判争议。"
            ),
            (
                f"- strict/broad 稳定交集：`{stability.get('status')}`；"
                f"稳定元素 {len(stability.get('stable_elements', []))} 个。"
            ),
            (
                f"- 生命周期状态：`{lifecycle.get('status')}`；"
                f"本报告阶段状态写入 `{lifecycle.get('write_performed', False)}`；"
                "最终提交结果见同 stem 的 `.state-commit.json`。"
            ),
        ]
    )
    if chan.get("status") == "unavailable":
        lines.append(f"- chan.py 不可用原因：{chan.get('reason')}")
    for comparison in consistency.get("comparisons", []):
        lines.append(
            f"- {comparison.get('timeframe')}：`{comparison.get('status')}`；"
            f"{comparison.get('reason')}"
        )
    for blocker in payload.get("directional_conclusion_blockers", []):
        lines.append(
            f"- 方向结论阻断：`{blocker['layer']}` = `{blocker['status']}`。"
        )

    nesting = analysis["timeframe_context"].get("interval_nesting", {})
    lines.extend(
        [
            "",
            "## 周期父子映射与区间嵌套",
            "",
            (
                "- 月→周映射期数："
                f"{len(analysis['timeframe_context'].get('monthly_to_weekly', []))}；"
                "周→日映射期数："
                f"{len(analysis['timeframe_context'].get('weekly_to_daily', []))}。"
            ),
            (
                "- 月/周中枢区间关系："
                f"`{nesting.get('monthly_weekly', {}).get('relationship', 'not_available')}`。"
            ),
            (
                "- 周/日中枢区间关系："
                f"`{nesting.get('weekly_daily', {}).get('relationship', 'not_available')}`。"
            ),
            "- 区间嵌套仅作多周期上下文，不产生方向或交易信号。",
            "",
            "## 数据核对与证据边界",
            "",
            (
                f"- 双源核对：`{market['cross_check'].get('status')}`；"
                f"重叠 {market['cross_check'].get('overlap_rows', 0)} 个交易日。"
            ),
            f"- 行情事实层：`{payload['evidence_boundary']['market_data']}`。",
            "- 双引擎结构、中枢、均线含义和仓位解释：`codex_inference`。",
            (
                "- chan.py BSP 1/1p/2/2s/3a/3b："
                "`neutral_structure_candidate_not_trade_signal`。"
            ),
        ]
    )
    for warning in market.get("warnings", []):
        lines.append(f"- 数据警告：{warning}")
    for provider, error in market.get("provider_errors", {}).items():
        lines.append(f"- {provider} 错误：{sanitize_provider_error(error, limit=240)}")

    lines.extend(["", "## 失效条件", ""])
    lines.extend(f"- {item}" for item in payload["invalidation_conditions"])
    lines.extend(["", "## 限制", ""])
    lines.extend(f"- {item}" for item in payload["limitations"])
    chart = payload.get("artifacts", {}).get("audit_chart")
    native_charts = payload.get("artifacts", {}).get("native_chan_charts")
    if chart or native_charts:
        lines.extend(
            [
                "",
                "## 审计产物",
                "",
            ]
        )
    if chart:
        chart_detail = (
            chart.get("path")
            or chart.get("reason")
            or chart.get("intended_path")
            or "not available"
        )
        lines.append(f"- 静态结构图：`{chart.get('status')}`；`{chart_detail}`")
        if chart.get("status") == "complete" and chart.get("path"):
            lines.extend(
                [
                    "",
                    _relative_markdown_image(
                        chart["path"], "月线、周线、日线综合结构审计图"
                    ),
                    "",
                ]
            )
    if native_charts:
        lines.append(
            "- chan.py CPlotDriver 静态图："
            f"`{native_charts.get('status')}`；profile "
            f"`{native_charts.get('profile')}`；BSP "
            f"`{native_charts.get('bsp_interpretation')}`。"
        )
        for timeframe in ("monthly", "weekly", "daily"):
            item = native_charts.get("charts", {}).get(timeframe, {})
            if item.get("status") == "complete" and item.get("path"):
                lines.extend(
                    [
                        f"- {timeframe}：`complete`；`{item['path']}`",
                        "",
                        _relative_markdown_image(
                            item["path"],
                            f"chan.py strict {timeframe} 静态结构图",
                        ),
                        "",
                    ]
                )
            else:
                detail = (
                    item.get("reason")
                    or item.get("intended_path")
                    or "not available"
                )
                lines.append(
                    f"- {timeframe}："
                    f"`{item.get('status', 'unavailable')}`；`{detail}`"
                )
    lines.append("")
    return "\n".join(lines)


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _portable_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(REPO_ROOT))
    except ValueError:
        return str(resolved)


def _is_within(path: Path, parent: Path) -> bool:
    path_parts = tuple(part.casefold() for part in path.expanduser().resolve().parts)
    parent_parts = tuple(
        part.casefold() for part in parent.expanduser().resolve().parts
    )
    return path_parts[: len(parent_parts)] == parent_parts


def _assert_safe_derived_directories(**directories: Path) -> None:
    protected = {
        "raw": REPO_ROOT / "raw",
        "wiki": REPO_ROOT / "wiki",
    }
    for label, path in directories.items():
        for protected_label, protected_path in protected.items():
            if _is_within(path, protected_path):
                raise ValueError(
                    f"{label} 不得指向 {protected_label}/ 或其子目录: "
                    f"{path.resolve()}"
                )


def _atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
            stream.write(content)
            stream.flush()
            temporary_path = Path(stream.name)
        temporary_path.replace(path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def _method_bundle_hash(payload: dict[str, Any]) -> str:
    lifecycle_identity = payload["analysis"]["structure_lifecycle"].get(
        "state_identity", {}
    )
    if lifecycle_identity.get("bundle_hash"):
        return lifecycle_identity["bundle_hash"]
    chan = payload["analysis"]["chan_py"]
    identity = {
        "upstream_commit": chan.get("engine", {}).get(
            "upstream_commit", EXPECTED_CHAN_COMMIT
        ),
        "profile_config_hashes": {
            name: chan.get("profiles", {}).get(name, {}).get("config_hash")
            for name in ("strict", "broad")
        },
    }
    return hashlib.sha256(
        json.dumps(identity, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _manifest_chart(chart: dict[str, Any] | None) -> dict[str, Any] | None:
    if chart is None:
        return None
    result = dict(chart)
    if result.get("path"):
        result["path"] = _portable_path(Path(result["path"]))
    if result.get("intended_path"):
        result["intended_path"] = _portable_path(Path(result["intended_path"]))
    return result


def _manifest_native_chan_charts(
    artifact: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if artifact is None:
        return None
    result = dict(artifact)
    result["charts"] = {}
    for timeframe, chart in artifact.get("charts", {}).items():
        chart_result = dict(chart)
        if chart_result.get("path"):
            chart_result["path"] = _portable_path(Path(chart_result["path"]))
        if chart_result.get("intended_path"):
            chart_result["intended_path"] = _portable_path(
                Path(chart_result["intended_path"])
            )
        result["charts"][timeframe] = chart_result
    return result


def build_analysis_manifest(
    payload: dict[str, Any],
    *,
    json_path: Path,
    markdown_path: Path,
    manifest_path: Path,
    state_receipt_path: Path,
) -> dict[str, Any]:
    chan = payload["analysis"]["chan_py"]
    lifecycle = payload["analysis"]["structure_lifecycle"]
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ticker": payload["ticker"],
        "technical_as_of": payload["technical_as_of"],
        "adjustment": payload["adjustment"],
        "normalized_input_sha256": payload["analysis"]["normalized_input"][
            "digest_sha256"
        ],
        "market_data_cache": payload["market_data"].get("cache_paths", {}),
        "statuses": {
            "data_quality_status": payload["data_quality_status"],
            "engine_consistency_status": payload["engine_consistency_status"],
            "chan_structure_status": payload["chan_structure_status"],
            "profile_stability_status": payload["profile_stability_status"],
            "overall_technical_status": payload["overall_technical_status"],
            "directional_conclusion_allowed": payload[
                "directional_conclusion_allowed"
            ],
        },
        "engines": {
            "czsc": payload["analysis"]["engine"],
            "chan_py": chan.get("engine", {
                "name": "chan.py",
                "expected_commit": EXPECTED_CHAN_COMMIT,
                "status": "unavailable",
            }),
        },
        "profile_config_hashes": {
            name: chan.get("profiles", {}).get(name, {}).get("config_hash")
            for name in ("strict", "broad")
        },
        "run_identity": payload.get("run_identity"),
        "state_identity": lifecycle.get("state_identity"),
        "state_path": (
            _portable_path(Path(lifecycle["state_path"]))
            if lifecycle.get("state_path")
            else None
        ),
        "artifacts": {
            "json": {
                "path": _portable_path(json_path),
                "sha256": _file_sha256(json_path),
                "bytes": json_path.stat().st_size,
            },
            "markdown": {
                "path": _portable_path(markdown_path),
                "sha256": _file_sha256(markdown_path),
                "bytes": markdown_path.stat().st_size,
            },
            "audit_chart": _manifest_chart(
                payload.get("artifacts", {}).get("audit_chart")
            ),
            "native_chan_charts": _manifest_native_chan_charts(
                payload.get("artifacts", {}).get("native_chan_charts")
            ),
            "state_commit_receipt": {
                "path": _portable_path(state_receipt_path),
                "publish_phase": "after_analysis_artifacts_and_state_commit",
            },
            "manifest": _portable_path(manifest_path),
        },
    }


def _state_commit_summary(result: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "status",
        "reason_code",
        "reason",
        "state_path",
        "state_identity",
        "state_revision",
        "state_sha256",
        "state_lock_path",
        "observed_at",
        "technical_as_of",
        "previous_technical_as_of",
        "data_revision",
        "counts",
        "write_performed",
        "source_run_identity",
    )
    return {key: result.get(key) for key in keys if key in result}


def _native_charts_not_generated(
    payload: dict[str, Any],
    output_paths: dict[str, Path],
    *,
    reason: str,
) -> dict[str, Any]:
    chan = payload["analysis"]["chan_py"]
    strict = chan.get("profiles", {}).get("strict", {})
    return {
        "status": "not_generated",
        "renderer": "chan.py.Plot.PlotDriver.CPlotDriver",
        "profile": "strict",
        "upstream_commit": chan.get("engine", {}).get(
            "upstream_commit", EXPECTED_CHAN_COMMIT
        ),
        "config_hash": strict.get("config_hash"),
        "input_digest": payload["analysis"]["normalized_input"]["digest_sha256"],
        "input_contract": "normalized_local_bars_only_no_chan_dataapi",
        "upstream_dataapi_used": False,
        "static": True,
        "animation": False,
        "interactive": False,
        "bsp_interpretation": "neutral_candidate_not_trade_signal",
        "plot_layers": list(NATIVE_PLOT_LAYERS),
        "reason": reason,
        "charts": {
            timeframe: {
                "status": "not_generated",
                "timeframe": timeframe,
                "path": None,
                "intended_path": str(path.resolve()),
                "reason": reason,
            }
            for timeframe, path in output_paths.items()
        },
    }


def main() -> int:
    today = date.today()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--start", default=(today - timedelta(days=365 * 5)).isoformat())
    parser.add_argument("--end", default=today.isoformat())
    parser.add_argument("--adjustment", choices=["none", "qfq"], default="qfq")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "output" / "technical-analysis",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=REPO_ROOT / ".work" / "market-data",
    )
    parser.add_argument(
        "--state-dir",
        type=Path,
        default=REPO_ROOT / ".work" / "technical-structure-state",
        help="chan.py 结构生命周期状态目录",
    )
    parser.add_argument(
        "--chan-py-path",
        type=Path,
        help="固定 commit 的 chan.py checkout；默认使用 CHAN_PY_PATH 或 .work/vendor/chan.py",
    )
    parser.add_argument("--offline-csv", type=Path)
    parser.add_argument("--no-cross-check", action="store_true")
    parser.add_argument(
        "--no-state-write",
        action="store_true",
        help="比较已有状态但不持久化本次结构",
    )
    parser.add_argument(
        "--no-audit-chart",
        action="store_true",
        help="不生成任何静态审计图（包括 audit.png 与 chan.py 原生图）",
    )
    parser.add_argument(
        "--no-native-chan-charts",
        action="store_true",
        help="保留 audit.png，但不生成三张 chan.py CPlotDriver 静态图",
    )
    args = parser.parse_args()

    _assert_safe_derived_directories(
        output_dir=args.output_dir,
        cache_dir=args.cache_dir,
        state_dir=args.state_dir,
    )
    parse_ticker(args.ticker)
    if args.offline_csv:
        result = _offline_result(
            args.ticker, args.offline_csv, args.start, args.end, args.adjustment
        )
    else:
        result = get_market_data(
            args.ticker,
            args.start,
            args.end,
            adjustment=args.adjustment,
            minimum_rows=120,
            cross_check=not args.no_cross_check,
        )
    save_cache(result, args.cache_dir)
    payload = build_payload(
        result,
        chan_path=args.chan_py_path,
        state_dir=args.state_dir,
        write_state=not args.no_state_write,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    safe_ticker = args.ticker.lower().replace(":", "-")
    input_identity = payload["analysis"]["normalized_input"]["digest_sha256"][:8]
    method_bundle_hash = _method_bundle_hash(payload)
    method_identity = method_bundle_hash[:8]
    run_timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    stem = (
        f"{safe_ticker}-{payload['technical_as_of']}-{payload['adjustment']}-"
        f"{input_identity}-{method_identity}-{run_timestamp}"
    )
    payload["run_identity"] = {
        "stem": stem,
        "run_timestamp_utc": run_timestamp,
        "normalized_input_sha256": payload["analysis"]["normalized_input"][
            "digest_sha256"
        ],
        "method_bundle_hash": method_bundle_hash,
    }
    json_path = args.output_dir / f"{stem}.json"
    markdown_path = args.output_dir / f"{stem}.md"
    manifest_path = args.output_dir / f"{stem}.manifest.json"
    chart_path = args.output_dir / f"{stem}.audit.png"
    native_chart_paths = {
        timeframe: args.output_dir / f"{stem}.chan-native-{timeframe}.png"
        for timeframe in ("monthly", "weekly", "daily")
    }
    state_receipt_path = args.output_dir / f"{stem}.state-commit.json"
    payload["artifacts"]["state_commit_receipt"] = {
        "path": str(state_receipt_path.resolve()),
        "purpose": "records the post-artifact lifecycle commit result",
    }
    if args.no_audit_chart:
        payload["artifacts"]["audit_chart"] = {
            "status": "not_generated",
            "path": None,
            "intended_path": str(chart_path.resolve()),
            "reason": "CLI --no-audit-chart",
        }
        payload["artifacts"]["native_chan_charts"] = _native_charts_not_generated(
            payload,
            native_chart_paths,
            reason="CLI --no-audit-chart",
        )
    else:
        try:
            payload["artifacts"]["audit_chart"] = render_audit_chart(
                result.data,
                payload["analysis"]["chan_py"],
                chart_path,
            )
        except Exception as exc:
            payload["artifacts"]["audit_chart"] = {
                "status": "unavailable",
                "path": None,
                "intended_path": str(chart_path.resolve()),
                "reason": (
                    "静态结构审计图生成失败: "
                    f"{type(exc).__name__}: {sanitize_provider_error(exc)}"
                ),
            }
        if args.no_native_chan_charts:
            payload["artifacts"]["native_chan_charts"] = (
                _native_charts_not_generated(
                    payload,
                    native_chart_paths,
                    reason="CLI --no-native-chan-charts",
                )
            )
        else:
            payload["artifacts"]["native_chan_charts"] = (
                render_native_chan_charts(
                    result.data,
                    native_chart_paths,
                    chan_path=args.chan_py_path,
                    profile="strict",
                )
            )
    _atomic_write_text(
        json_path,
        json.dumps(payload, ensure_ascii=False, indent=2, default=_json_default) + "\n",
    )
    _atomic_write_text(markdown_path, render_markdown(payload))
    manifest = build_analysis_manifest(
        payload,
        json_path=json_path,
        markdown_path=markdown_path,
        manifest_path=manifest_path,
        state_receipt_path=state_receipt_path,
    )
    _atomic_write_text(
        manifest_path,
        json.dumps(manifest, ensure_ascii=False, indent=2, default=_json_default) + "\n",
    )

    receipt_base = {
        "schema_version": 1,
        "run_identity": payload["run_identity"],
        "analysis_manifest": {
            "path": _portable_path(manifest_path),
            "sha256": _file_sha256(manifest_path),
        },
    }
    _atomic_write_text(
        state_receipt_path,
        json.dumps(
            {
                **receipt_base,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "receipt_status": "pending_state_commit",
                "state_commit": {
                    "status": "pending",
                    "write_performed": False,
                },
                "state_sha256": None,
            },
            ensure_ascii=False,
            indent=2,
            default=_json_default,
        )
        + "\n",
    )

    lifecycle_preview = payload["analysis"]["structure_lifecycle"]
    if args.no_state_write:
        state_commit = {
            "status": "not_persisted",
            "reason_code": "disabled_by_cli",
            "reason": "CLI --no-state-write",
            "state_path": lifecycle_preview.get("state_path"),
            "write_performed": False,
        }
    elif result.data_quality_status != "complete":
        state_commit = {
            "status": "not_persisted",
            "reason_code": "market_data_quality_not_complete",
            "reason": (
                "生命周期 state 只接受 data_quality_status=complete；"
                f"actual={result.data_quality_status}"
            ),
            "state_path": lifecycle_preview.get("state_path"),
            "write_performed": False,
        }
    else:
        state_commit = apply_structure_lifecycle(
            payload["analysis"]["chan_py"],
            ticker=result.ticker,
            adjustment=result.adjustment,
            state_dir=args.state_dir,
            write_state=True,
            technical_as_of=payload["technical_as_of"],
            source_run_identity=payload["run_identity"],
        )

    state_summary = _state_commit_summary(state_commit)
    state_receipt = {
        **receipt_base,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "receipt_status": "final",
        "state_commit": state_summary,
        "state_sha256": state_summary.get("state_sha256"),
    }
    _atomic_write_text(
        state_receipt_path,
        json.dumps(state_receipt, ensure_ascii=False, indent=2, default=_json_default)
        + "\n",
    )
    print(json.dumps(
        {
            "status": "ok",
            "data_quality_status": result.data_quality_status,
            "engine_consistency_status": payload["engine_consistency_status"],
            "chan_structure_status": payload["chan_structure_status"],
            "profile_stability_status": payload["profile_stability_status"],
            "overall_technical_status": payload["overall_technical_status"],
            "directional_conclusion_allowed": payload[
                "directional_conclusion_allowed"
            ],
            "technical_as_of": payload["technical_as_of"],
            "run_identity": payload["run_identity"],
            "json": str(json_path.resolve()),
            "markdown": str(markdown_path.resolve()),
            "manifest": str(manifest_path.resolve()),
            "state_commit_receipt": str(state_receipt_path.resolve()),
            "audit_chart": payload["artifacts"]["audit_chart"].get("path"),
            "native_chan_charts": payload["artifacts"]["native_chan_charts"],
            "state": state_summary,
        },
        ensure_ascii=False,
    ))
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
    except Exception as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "data_quality_status": "unavailable",
                    "error_type": type(exc).__name__,
                    "error": sanitize_provider_error(exc),
                },
                ensure_ascii=False,
            )
        )
        exit_code = 2
    raise SystemExit(exit_code)
