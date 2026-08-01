#!/usr/bin/env python3
"""Offline tests for the A-share technical-analysis skill."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "skills" / "a-share-technical-analysis" / "scripts"
sys.path.insert(0, str(SCRIPTS))
os.environ.setdefault("CZSC_HOME", str(REPO_ROOT / ".work" / "czsc-test"))

from czsc_bridge import analyze_multitimeframe, resample_bars  # noqa: E402
import market_data  # noqa: E402
from market_data import (  # noqa: E402
    AKSHARE_VOLUME_MULTIPLIER,
    MarketDataError,
    MarketDataResult,
    compare_sources,
    drop_unfinished_daily_bar,
    fetch_akshare,
    get_market_data,
    normalized_frame_digest,
    parse_ticker,
    save_cache,
    validate_bars,
)


def synthetic_bars(rows: int = 900) -> pd.DataFrame:
    dates = pd.bdate_range("2022-01-04", periods=rows)
    base = (
        100
        + np.linspace(0, 40, rows)
        + 8 * np.sin(np.linspace(0, 45 * np.pi, rows))
    )
    close = base + 0.5 * np.sin(np.linspace(0, 100 * np.pi, rows))
    open_ = close + 0.3 * np.cos(np.linspace(0, 70 * np.pi, rows))
    return pd.DataFrame(
        {
            "dt": dates,
            "symbol": "600519.SH",
            "open": open_,
            "close": close,
            "high": np.maximum(open_, close) + 1.2,
            "low": np.minimum(open_, close) - 1.2,
            "vol": np.linspace(1_000_000, 2_000_000, rows),
            "amount": np.linspace(100_000_000, 250_000_000, rows),
        }
    )


def offline_market_result(
    frame: pd.DataFrame,
    *,
    provider: str = "offline_fixture",
) -> MarketDataResult:
    return MarketDataResult(
        ticker="SSE:600519",
        data=frame,
        provider=provider,
        adjustment="qfq",
        requested_start="2022-01-01",
        requested_end="2026-01-01",
        fetched_at="2026-08-01T08:00:00+00:00",
        data_quality_status="degraded",
        quality_report={"status": "complete"},
        cross_check={"status": "unavailable", "overlap_rows": 0},
    )


class TickerAndDataContractTests(unittest.TestCase):
    def test_ticker_mapping(self) -> None:
        mapping = parse_ticker("SSE:600519")
        self.assertEqual(mapping.baostock_code, "sh.600519")
        self.assertEqual(mapping.czsc_symbol, "600519.SH")
        self.assertEqual(parse_ticker("SZSE:000001").baostock_code, "sz.000001")
        self.assertEqual(parse_ticker("BJSE:830799").baostock_code, "bj.830799")

    def test_ticker_rejects_missing_or_conflicting_exchange(self) -> None:
        for ticker in ("600519", "NYSE:600519", "SSE:000001", "SZSE:600519"):
            with self.assertRaises(ValueError):
                parse_ticker(ticker)

    def test_akshare_volume_is_converted_from_hands_to_shares(self) -> None:
        import akshare

        original = akshare.stock_zh_a_hist
        akshare.stock_zh_a_hist = lambda **_: pd.DataFrame(
            {
                "日期": [pd.Timestamp("2026-07-24").date()],
                "开盘": [10.0],
                "收盘": [10.2],
                "最高": [10.3],
                "最低": [9.9],
                "成交量": [1234],
                "成交额": [1_250_000],
            }
        )
        try:
            frame = fetch_akshare(
                "SSE:600519", "2026-07-24", "2026-07-24", "none", retries=0
            )
        finally:
            akshare.stock_zh_a_hist = original
        self.assertEqual(frame.iloc[0]["vol"], 1234 * AKSHARE_VOLUME_MULTIPLIER)

    def test_quality_gate_and_cross_source_dispute(self) -> None:
        frame = synthetic_bars(140)
        self.assertEqual(validate_bars(frame, 120)["status"], "complete")
        self.assertEqual(compare_sources(frame, frame.copy())["status"], "complete")

        changed = frame.copy()
        changed.loc[changed.index[-1], "close"] *= 1.05
        changed.loc[changed.index[-1], "high"] = changed.loc[changed.index[-1], "close"] + 1
        self.assertEqual(compare_sources(frame, changed)["status"], "disputed")

        invalid = frame.copy()
        invalid.loc[0, "high"] = invalid.loc[0, "low"] - 1
        self.assertEqual(validate_bars(invalid)["status"], "disputed")

    def test_primary_fallback_is_explicit(self) -> None:
        frame = synthetic_bars(140)

        def failed_primary(*_: object) -> pd.DataFrame:
            raise RuntimeError("primary unavailable")

        result = get_market_data(
            "SSE:600519",
            "2022-01-01",
            "2025-01-01",
            baostock_fetcher=failed_primary,
            akshare_fetcher=lambda *_: frame.copy(),
        )
        self.assertEqual(result.provider, "akshare")
        self.assertEqual(result.data_quality_status, "degraded")
        self.assertEqual(result.package_versions["baostock"], "0.9.3")
        self.assertEqual(result.package_versions["akshare"], "1.18.80")
        self.assertIn("baostock", result.provider_errors)
        self.assertTrue(any("降级" in warning for warning in result.warnings))

    def test_unadjusted_cross_check_cannot_upgrade_single_adjusted_series(self) -> None:
        frame = synthetic_bars(140)
        adjusted_supplement = frame.copy()
        adjusted_supplement[["open", "close", "high", "low"]] *= 1.02

        def primary(_: str, __: str, ___: str, adjustment: str) -> pd.DataFrame:
            return frame.copy()

        def supplement(_: str, __: str, ___: str, adjustment: str) -> pd.DataFrame:
            return (
                adjusted_supplement.copy()
                if adjustment == "qfq"
                else frame.copy()
            )

        actual_end = frame["dt"].max().date().isoformat()
        result = get_market_data(
            "SSE:600519",
            "2022-01-01",
            actual_end,
            baostock_fetcher=primary,
            akshare_fetcher=supplement,
        )
        self.assertEqual(result.data_quality_status, "degraded")
        self.assertEqual(result.cross_check["basis"], "unadjusted_fallback")
        self.assertEqual(result.cross_check["unadjusted_check"]["status"], "complete")

    def test_unfinished_today_bar_is_removed(self) -> None:
        frame = synthetic_bars(5)
        today = datetime(2026, 7, 28, 10, 0, tzinfo=ZoneInfo("Asia/Shanghai"))
        frame.loc[frame.index[-1], "dt"] = pd.Timestamp(today.date())
        trimmed, dropped = drop_unfinished_daily_bar(frame, now=today)
        self.assertTrue(dropped)
        self.assertEqual(len(trimmed), len(frame) - 1)

    def test_cache_identity_preserves_same_day_data_revisions(self) -> None:
        frame = synthetic_bars(140)
        first_result = offline_market_result(frame, provider="baostock")
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_dir = Path(temp_dir)
            first_paths = save_cache(first_result, cache_dir)
            first_digest = normalized_frame_digest(frame)
            first_manifest = json.loads(
                Path(first_paths["manifest"]).read_text(encoding="utf-8")
            )

            revised_frame = frame.copy()
            revised_frame.loc[revised_frame.index[-1], "close"] += 0.25
            revised_frame.loc[revised_frame.index[-1], "high"] = (
                revised_frame.loc[revised_frame.index[-1], "close"] + 1.2
            )
            revised_result = offline_market_result(revised_frame, provider="baostock")
            revised_paths = save_cache(revised_result, cache_dir)
            revised_digest = normalized_frame_digest(revised_frame)

            first_files_still_exist = all(Path(path).is_file() for path in first_paths.values())
            csv_rows = len(pd.read_csv(first_paths["csv"]))
            temp_files = list(cache_dir.glob(".*.tmp"))

        self.assertIn("baostock", Path(first_paths["parquet"]).name)
        self.assertIn(first_digest, Path(first_paths["parquet"]).name)
        self.assertEqual(first_manifest["input_digest"], first_digest)
        self.assertEqual(first_manifest["cache_identity"]["provider"], "baostock")
        self.assertEqual(
            set(first_manifest["cache_artifacts"]), {"parquet", "csv"}
        )
        self.assertNotEqual(first_digest, revised_digest)
        self.assertNotEqual(first_paths["parquet"], revised_paths["parquet"])
        self.assertTrue(first_files_still_exist)
        self.assertEqual(csv_rows, len(frame))
        self.assertEqual(temp_files, [])

    def test_cache_precommit_failure_leaves_no_partial_artifacts(self) -> None:
        result = offline_market_result(synthetic_bars(140), provider="offline_fixture")
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_dir = Path(temp_dir)
            with patch.object(
                market_data,
                "_file_sha256",
                side_effect=RuntimeError("injected manifest preparation failure"),
            ):
                with self.assertRaisesRegex(RuntimeError, "injected"):
                    save_cache(result, cache_dir)
            remaining = [
                path for path in cache_dir.iterdir() if path.suffix != ".lock"
            ]

        self.assertEqual(result.cache_paths, {})
        self.assertEqual(remaining, [])

    def test_cache_reuses_valid_identity_and_rejects_corruption(self) -> None:
        frame = synthetic_bars(140)
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_dir = Path(temp_dir)
            first = offline_market_result(frame, provider="baostock")
            first_paths = save_cache(first, cache_dir)
            mtimes = {
                name: Path(path).stat().st_mtime_ns
                for name, path in first_paths.items()
            }

            identical = offline_market_result(frame.copy(), provider="baostock")
            reused_paths = save_cache(identical, cache_dir)
            reused_mtimes = {
                name: Path(path).stat().st_mtime_ns
                for name, path in reused_paths.items()
            }

            Path(first_paths["csv"]).write_text("corrupted\n", encoding="utf-8")
            with self.assertRaisesRegex(MarketDataError, "完整性校验失败"):
                save_cache(
                    offline_market_result(frame.copy(), provider="baostock"),
                    cache_dir,
                )

        self.assertEqual(first_paths, reused_paths)
        self.assertEqual(mtimes, reused_mtimes)


class CzscBridgeTests(unittest.TestCase):
    def test_resampling_uses_last_actual_trading_date(self) -> None:
        frame = synthetic_bars(30)
        weekly = resample_bars(frame, "weekly")
        monthly = resample_bars(frame, "monthly")
        self.assertTrue(set(weekly["dt"]).issubset(set(frame["dt"])))
        self.assertTrue(set(monthly["dt"]).issubset(set(frame["dt"])))
        self.assertEqual(weekly.iloc[-1]["close"], frame.iloc[-1]["close"])

    def test_multitimeframe_output_contract(self) -> None:
        result = analyze_multitimeframe(synthetic_bars())
        self.assertEqual(result["engine"]["version"], "0.10.12")
        self.assertEqual(set(result["timeframes"]), {"monthly", "weekly", "daily"})
        self.assertEqual(result["evidence_type"], "codex_inference")
        self.assertEqual(
            result["technical_as_of"],
            synthetic_bars()["dt"].max().date().isoformat(),
        )
        for timeframe in result["timeframes"].values():
            self.assertIn("last_completed_bi", timeframe)
            self.assertIn("valid_three_bi_zone", timeframe)
            self.assertIn("indicators", timeframe)

    def test_offline_cli_writes_noncanonical_report_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fixture = root / "fixture.csv"
            output = root / "output"
            cache = root / "cache"
            state = root / "state"
            synthetic_bars().to_csv(fixture, index=False)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "technical_snapshot.py"),
                    "--ticker",
                    "SSE:600519",
                    "--offline-csv",
                    str(fixture),
                    "--output-dir",
                    str(output),
                    "--cache-dir",
                    str(cache),
                    "--state-dir",
                    str(state),
                    "--no-state-write",
                    "--no-audit-chart",
                ],
                check=True,
                capture_output=True,
                text=True,
                env={**os.environ, "CZSC_HOME": str(root / "czsc")},
            )
            summary = json.loads(completed.stdout)
            self.assertEqual(summary["status"], "ok")
            self.assertTrue(Path(summary["json"]).is_file())
            self.assertTrue(Path(summary["markdown"]).is_file())
            self.assertEqual(len(list(cache.glob("*.parquet"))), 1)
            self.assertEqual(len(list(cache.glob("*.manifest.json"))), 1)
            self.assertFalse(state.exists())
            report = Path(summary["markdown"]).read_text(encoding="utf-8")
            self.assertIn("月线主结构", report)
            self.assertIn("codex_inference", report)


if __name__ == "__main__":
    unittest.main(verbosity=2)
