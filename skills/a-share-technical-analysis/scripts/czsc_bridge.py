#!/usr/bin/env python3
"""Stable CZSC bridge for daily, weekly, and monthly A-share snapshots."""

from __future__ import annotations

import importlib.metadata
import math
import os
from pathlib import Path
from typing import Any

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[3]
os.environ.setdefault("CZSC_HOME", str(REPO_ROOT / ".work" / "czsc"))


def resample_bars(frame: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    if timeframe == "daily":
        return frame.copy().sort_values("dt").reset_index(drop=True)
    if timeframe not in {"weekly", "monthly"}:
        raise ValueError("timeframe 必须是 daily、weekly 或 monthly")

    data = frame.copy().sort_values("dt")
    data["dt"] = pd.to_datetime(data["dt"])
    period = (
        data["dt"].dt.to_period("W-FRI")
        if timeframe == "weekly"
        else data["dt"].dt.to_period("M")
    )
    data["_period"] = period
    rows: list[dict[str, Any]] = []
    for _, group in data.groupby("_period", sort=True):
        rows.append(
            {
                "dt": group["dt"].max(),
                "symbol": group["symbol"].iloc[-1],
                "open": float(group["open"].iloc[0]),
                "close": float(group["close"].iloc[-1]),
                "high": float(group["high"].max()),
                "low": float(group["low"].min()),
                "vol": float(group["vol"].sum()),
                "amount": float(group["amount"].sum()),
            }
        )
    return pd.DataFrame(rows)


def _enum_text(value: Any) -> str | None:
    if value is None:
        return None
    raw = getattr(value, "value", value)
    text = str(raw)
    mapping = {
        "向上": "up",
        "向下": "down",
        "Direction.Up": "up",
        "Direction.Down": "down",
        "Up": "up",
        "Down": "down",
    }
    return mapping.get(text, text)


def _value(obj: Any, name: str) -> Any:
    try:
        value = getattr(obj, name)
        return value() if callable(value) and name.startswith("is_") else value
    except Exception:
        return None


def _number(value: Any, digits: int = 6) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return round(number, digits)


def _date(value: Any) -> str | None:
    if value is None:
        return None
    return pd.Timestamp(value).date().isoformat()


def _indicators(frame: pd.DataFrame) -> dict[str, Any]:
    close = frame["close"].astype(float)
    high = frame["high"].astype(float)
    low = frame["low"].astype(float)
    previous_close = close.shift(1)
    true_range = pd.concat(
        [
            high - low,
            (high - previous_close).abs(),
            (low - previous_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    ma = {
        period: _number(close.rolling(period).mean().iloc[-1])
        if len(close) >= period
        else None
        for period in (20, 60, 120)
    }
    last_close = float(close.iloc[-1])
    if ma[20] is not None and ma[60] is not None:
        if last_close > ma[20] > ma[60]:
            trend = "bullish"
        elif last_close < ma[20] < ma[60]:
            trend = "bearish"
        else:
            trend = "mixed"
    else:
        trend = "insufficient"

    previous_volume = frame["vol"].astype(float).iloc[-21:-1]
    volume_ratio = (
        _number(float(frame["vol"].iloc[-1]) / float(previous_volume.mean()))
        if len(previous_volume) == 20 and float(previous_volume.mean()) > 0
        else None
    )
    return {
        "close": _number(last_close),
        "ma20": ma[20],
        "ma60": ma[60],
        "ma120": ma[120],
        "atr14": _number(true_range.rolling(14).mean().iloc[-1])
        if len(frame) >= 14
        else None,
        "volume_ratio_20": volume_ratio,
        "return_20": _number(last_close / float(close.iloc[-21]) - 1)
        if len(close) >= 21
        else None,
        "trend_state": trend,
    }


def analyze_timeframe(frame: pd.DataFrame, timeframe: str) -> dict[str, Any]:
    try:
        # CZSC 0.10.x stable public module.
        from czsc.core import CZSC, ZS, format_standard_kline
    except ModuleNotFoundError:
        # CZSC 1.0 prereleases expose the same objects at package top level.
        from czsc import CZSC, ZS, format_standard_kline

    freq_text = {"daily": "日线", "weekly": "周线", "monthly": "月线"}[timeframe]
    bars_frame = resample_bars(frame, timeframe).reset_index(drop=True)
    bars = format_standard_kline(bars_frame, freq_text)
    analyzer = CZSC(bars)
    bis = list(analyzer.bi_list)

    last_bi: dict[str, Any] | None = None
    if bis:
        bi = bis[-1]
        last_bi = {
            "direction": _enum_text(_value(bi, "direction")),
            "start": _date(_value(bi, "sdt")),
            "end": _date(_value(bi, "edt")),
            "high": _number(_value(bi, "high")),
            "low": _number(_value(bi, "low")),
            "length": int(_value(bi, "length")) if _value(bi, "length") is not None else None,
            "power_price": _number(_value(bi, "power_price")),
            "power_volume": _number(_value(bi, "power_volume")),
        }

    zone: dict[str, Any] | None = None
    if len(bis) >= 3:
        candidate = ZS(bis[-3:])
        valid = _value(candidate, "is_valid")
        if bool(valid):
            zone = {
                "start": _date(_value(candidate, "sdt")),
                "end": _date(_value(candidate, "edt")),
                "upper": _number(_value(candidate, "zg")),
                "lower": _number(_value(candidate, "zd")),
                "axis": _number(_value(candidate, "zz")),
                "source": "last_three_completed_bis",
            }

    indicators = _indicators(bars_frame)
    close = indicators["close"]
    if zone and close is not None:
        if close > zone["upper"]:
            zone_position = "above"
        elif close < zone["lower"]:
            zone_position = "below"
        else:
            zone_position = "inside"
    else:
        zone_position = "not_available"

    unfinished_direction = None
    if last_bi and close is not None:
        endpoint = last_bi["low"] if last_bi["direction"] == "down" else last_bi["high"]
        if endpoint is not None:
            unfinished_direction = (
                "up"
                if close > endpoint
                else ("down" if close < endpoint else "flat")
            )

    return {
        "timeframe": timeframe,
        "freq": freq_text,
        "bar_count": int(len(bars_frame)),
        "as_of": _date(bars_frame["dt"].max()),
        "current_aggregate_may_be_incomplete": timeframe in {"weekly", "monthly"},
        "completed_bi_count": int(len(bis)),
        "last_completed_bi": last_bi,
        "valid_three_bi_zone": zone,
        "position_vs_zone": zone_position,
        "unfinished_price_direction": unfinished_direction,
        "indicators": indicators,
    }


def _timeframe_sentence(label: str, result: dict[str, Any]) -> str:
    trend_map = {
        "bullish": "均线结构偏强",
        "bearish": "均线结构偏弱",
        "mixed": "均线结构混合",
        "insufficient": "均线样本不足",
    }
    last_bi = result.get("last_completed_bi") or {}
    direction_map = {"up": "向上", "down": "向下"}
    direction = direction_map.get(last_bi.get("direction"), "未识别")
    zone = result.get("position_vs_zone")
    zone_map = {
        "above": "价格在有效三笔重叠区间上方",
        "inside": "价格在有效三笔重叠区间内",
        "below": "价格在有效三笔重叠区间下方",
        "not_available": "未识别有效三笔重叠区间",
    }
    return (
        f"{label}最后已完成笔{direction}，"
        f"{trend_map[result['indicators']['trend_state']]}，{zone_map[zone]}。"
    )


def analyze_multitimeframe(frame: pd.DataFrame) -> dict[str, Any]:
    ordered = {
        timeframe: analyze_timeframe(frame, timeframe)
        for timeframe in ("monthly", "weekly", "daily")
    }
    monthly = ordered["monthly"]
    weekly = ordered["weekly"]
    daily = ordered["daily"]

    mt = monthly["indicators"]["trend_state"]
    wt = weekly["indicators"]["trend_state"]
    if mt == wt == "bullish":
        alignment = "bullish_alignment"
        allocation_context = (
            "月线与周线趋势同向偏强；仓位判断仍需估值、基本面和事件确认。"
        )
    elif mt == wt == "bearish":
        alignment = "bearish_alignment"
        allocation_context = (
            "月线与周线趋势同向偏弱；技术面不支持仅凭短期反弹扩大仓位。"
        )
    else:
        alignment = "conflicted"
        allocation_context = (
            "月线与周线未形成同向确认；周/月调仓宜缩小技术信号权重。"
        )

    return {
        "technical_as_of": daily["as_of"],
        "engine": {
            "name": "czsc",
            "version": importlib.metadata.version("czsc"),
            "api": "czsc.core public API",
            "czsc_home": os.environ["CZSC_HOME"],
        },
        "timeframes": ordered,
        "alignment": alignment,
        "allocation_context": allocation_context,
        "monthly_primary": _timeframe_sentence("月线", monthly),
        "weekly_sizing": _timeframe_sentence("周线", weekly),
        "daily_execution": _timeframe_sentence("日线", daily),
        "evidence_type": "codex_inference",
    }


__all__ = ["analyze_multitimeframe", "analyze_timeframe", "resample_bars"]
