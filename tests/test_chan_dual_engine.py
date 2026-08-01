#!/usr/bin/env python3
"""Offline tests for the CZSC/chan.py C1-C5 integration contract."""

from __future__ import annotations

import hashlib
import io
import json
import math
import multiprocessing
import os
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "skills" / "a-share-technical-analysis" / "scripts"
sys.path.insert(0, str(SCRIPTS))
os.environ.setdefault("CZSC_HOME", "/private/tmp/a-share-czsc-tests")

import chan_bridge  # noqa: E402
from chan_bridge import (  # noqa: E402
    analyze_chan_profiles,
    apply_structure_lifecycle,
    build_timeframe_context,
    compare_engines,
    compare_profiles,
    normalized_frame_digest,
    render_audit_chart,
)
import technical_snapshot  # noqa: E402


def synthetic_bars(rows: int = 320) -> pd.DataFrame:
    dates = pd.bdate_range("2025-01-02", periods=rows)
    close = [100 + index * 0.04 + 4 * math.sin(index / 9) for index in range(rows)]
    open_ = [value + 0.3 * math.cos(index / 7) for index, value in enumerate(close)]
    return pd.DataFrame(
        {
            "dt": dates,
            "symbol": "002135.SZ",
            "open": open_,
            "close": close,
            "high": [max(o, c) + 0.8 for o, c in zip(open_, close)],
            "low": [min(o, c) - 0.8 for o, c in zip(open_, close)],
            "vol": [1_000_000 + index * 1_000 for index in range(rows)],
            "amount": [10_000_000 + index * 10_000 for index in range(rows)],
        }
    )


def profile_with(elements: list[dict[str, object]]) -> dict[str, object]:
    timeframes = {
        timeframe: {
            "status": "complete",
            "timeframe": timeframe,
            "elements": [
                dict(element)
                for element in elements
                if element.get("timeframe") == timeframe
            ],
        }
        for timeframe in ("monthly", "weekly", "daily")
    }
    return {"status": "complete", "config_hash": "fixture-config", "timeframes": timeframes}


def chan_result(
    elements: list[dict[str, object]],
    *,
    commit: str = "fixture-commit",
    strict_hash: str = "fixture-strict-config",
    broad_hash: str = "fixture-broad-config",
    input_digest: str = "fixture-bars",
) -> dict[str, object]:
    result = {
        "status": "complete",
        "engine": {"upstream_commit": commit},
        "input_digest": input_digest,
        "profiles": {
            "strict": profile_with(elements),
            "broad": profile_with([]),
        },
        "profile_stability": {"status": "complete", "stable_elements": elements},
    }
    result["profiles"]["strict"]["config_hash"] = strict_hash
    result["profiles"]["broad"]["config_hash"] = broad_hash
    return result


def structure_element(
    element_id: str,
    *,
    content_hash: str = "content-v1",
    timeframe: str = "weekly",
    layer: str = "bi",
) -> dict[str, object]:
    return {
        "element_id": element_id,
        "content_hash": content_hash,
        "engine": "chan.py",
        "profile": "strict",
        "timeframe": timeframe,
        "layer": layer,
        "index": 1,
        "start": "2026-06-01",
        "end": "2026-07-20",
        "direction": "up",
        "confirmed": True,
        "status": "confirmed",
    }


class _FakeKLType:
    K_MON = "monthly"
    K_WEEK = "weekly"
    K_DAY = "daily"


class _FakeDataField:
    FIELD_TIME = "time"
    FIELD_OPEN = "open"
    FIELD_CLOSE = "close"
    FIELD_HIGH = "high"
    FIELD_LOW = "low"
    FIELD_VOLUME = "volume"
    FIELD_TURNOVER = "turnover"


class _FakeCTime:
    def __init__(self, year: int, month: int, day: int, hour: int, minute: int):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute


class _FakeKLineUnit:
    def __init__(self, values: dict[str, object]):
        self.values = values


class _FakeChanConfig:
    def __init__(self, config: dict[str, object]):
        self.config = dict(config)
        self.trigger_step = bool(config.get("trigger_step"))


class _FakeBSPList:
    @staticmethod
    def bsp_iter():
        return iter(())


class _FakeStructure:
    def __init__(self) -> None:
        self.bi_list: list[object] = []
        self.seg_list: list[object] = []
        self.segseg_list: list[object] = []
        self.zs_list: list[object] = []
        self.segzs_list: list[object] = []
        self.bs_point_lst = _FakeBSPList()
        self.seg_bs_point_lst = _FakeBSPList()
        self.finalized = False

    def cal_seg_and_zs(self) -> None:
        self.finalized = True


class _FakeChan:
    data_sources: list[str] = []
    triggered_levels: list[str] = []

    def __init__(
        self,
        *,
        code: str,
        data_src: str,
        lv_list: list[str],
        config: _FakeChanConfig,
        **_: object,
    ) -> None:
        if data_src != "external-normalized-bars":
            raise AssertionError("native chart attempted to use upstream DataAPI")
        self.code = code
        self.data_src = data_src
        self.lv_list = list(lv_list)
        self.conf = config
        self.kl_datas = {level: _FakeStructure() for level in self.lv_list}
        self.triggered: dict[str, list[_FakeKLineUnit]] = {}
        self.data_sources.append(data_src)

    def trigger_load(self, values: dict[str, list[_FakeKLineUnit]]) -> None:
        self.triggered = values
        self.triggered_levels.extend(values)


class _FakePlotDriver:
    calls: list[dict[str, object]] = []
    fail_level: str | None = None

    def __init__(
        self,
        chan: _FakeChan,
        plot_config: dict[str, bool],
        plot_para: dict[str, object],
    ) -> None:
        level = chan.lv_list[0]
        self.calls.append(
            {
                "level": level,
                "data_src": chan.data_src,
                "plot_config": dict(plot_config),
                "plot_para": dict(plot_para),
            }
        )
        if self.fail_level == level:
            raise RuntimeError(f"injected {level} native chart failure")
        from matplotlib.figure import Figure

        self.figure = Figure(figsize=(2, 1))
        axis = self.figure.subplots()
        axis.plot([0, 1], [0, 1])

    def save2img(self, path: str | Path) -> None:
        self.figure.savefig(path, format="png")


class _FakePyplot:
    closed_count = 0

    @classmethod
    def close(cls, _: object) -> None:
        cls.closed_count += 1


def fake_chan_runtime() -> dict[str, object]:
    return {
        "CChan": _FakeChan,
        "CChanConfig": _FakeChanConfig,
        "KL_TYPE": _FakeKLType,
        "DATA_FIELD": _FakeDataField,
        "CTime": _FakeCTime,
        "CKLine_Unit": _FakeKLineUnit,
        "commit": chan_bridge.EXPECTED_CHAN_COMMIT,
        "root": "/fixture/pinned-chan.py",
    }


def reset_native_chart_fakes() -> None:
    _FakeChan.data_sources = []
    _FakeChan.triggered_levels = []
    _FakePlotDriver.calls = []
    _FakePlotDriver.fail_level = None
    _FakePyplot.closed_count = 0


def native_chart_paths(root: Path) -> dict[str, Path]:
    return {
        timeframe: root / f"fixture.chan-native-{timeframe}.png"
        for timeframe in ("monthly", "weekly", "daily")
    }


def minimal_snapshot_payload(frame: pd.DataFrame) -> dict[str, object]:
    input_digest = normalized_frame_digest(frame)
    return {
        "ticker": "SZSE:002135",
        "listing_regime": "a_share",
        "technical_as_of": pd.Timestamp(frame["dt"].max()).date().isoformat(),
        "adjustment": "qfq",
        "market_data": {"cache_paths": {}},
        "data_quality_status": "degraded",
        "engine_consistency_status": "complete",
        "chan_structure_status": "complete",
        "profile_stability_status": "complete",
        "overall_technical_status": "degraded",
        "directional_conclusion_allowed": True,
        "analysis": {
            "normalized_input": {"digest_sha256": input_digest},
            "engine": {"name": "CZSC", "version": "fixture"},
            "chan_py": {
                "engine": {
                    "name": "chan.py",
                    "upstream_commit": chan_bridge.EXPECTED_CHAN_COMMIT,
                },
                "profiles": {
                    "strict": {"config_hash": "strict-fixture"},
                    "broad": {"config_hash": "broad-fixture"},
                },
            },
            "structure_lifecycle": {
                "status": "complete",
                "write_performed": False,
                "state_identity": {"bundle_hash": "a" * 64},
            },
        },
        "artifacts": {},
    }


def _lifecycle_process_worker(
    state_dir: str,
    cutoff: str,
    input_digest: str,
    write_delay: float,
    barrier: object,
    queue: object,
) -> None:
    if write_delay:
        original_write = chan_bridge._atomic_json_write

        def delayed_write(path: Path, value: object) -> str:
            time.sleep(write_delay)
            return original_write(path, value)

        chan_bridge._atomic_json_write = delayed_write
    barrier.wait()
    result = apply_structure_lifecycle(
        chan_result(
            [structure_element("concurrent-weekly-bi")],
            input_digest=input_digest,
        ),
        ticker="SZSE:002135",
        adjustment="qfq",
        state_dir=Path(state_dir),
        observed_at=f"{cutoff}T08:00:00Z",
        technical_as_of=cutoff,
        source_run_identity={"run": input_digest},
    )
    queue.put(
        {
            "cutoff": cutoff,
            "input_digest": input_digest,
            "status": result["status"],
            "reason_code": result.get("reason_code"),
            "source_run_identity": result.get("source_run_identity"),
        }
    )


class ChanDualEngineContractTests(unittest.TestCase):
    def test_normalized_digest_is_deterministic_and_data_sensitive(self) -> None:
        frame = synthetic_bars()
        original = normalized_frame_digest(frame)
        reordered = normalized_frame_digest(frame.sample(frac=1, random_state=7))
        changed = frame.copy()
        changed.loc[changed.index[-1], "close"] += 0.01

        self.assertEqual(original, reordered)
        self.assertNotEqual(original, normalized_frame_digest(changed))

    def test_missing_chan_runtime_fails_closed_without_aborting_czsc_workflow(self) -> None:
        frame = synthetic_bars()
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "missing-chan-checkout"
            result = analyze_chan_profiles(frame, chan_path=missing)

        self.assertEqual(result["status"], "unavailable")
        self.assertEqual(result["reason_code"], "chan_runtime_unavailable")
        self.assertEqual(result["input_digest"], normalized_frame_digest(frame))
        self.assertEqual(result["profiles"], {})
        self.assertEqual(result["profile_stability"]["status"], "unavailable")
        self.assertEqual(
            compare_engines({"timeframes": {}}, result)["status"], "unavailable"
        )

    def test_chan_runtime_rejects_tracked_and_untracked_dirty_checkout(self) -> None:
        required = (
            "Chan.py",
            "ChanConfig.py",
            "Common/CEnum.py",
            "Common/CTime.py",
            "KLine/KLine_Unit.py",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            checkout = Path(temp_dir)
            for relative in required:
                path = checkout / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"# {relative}\n", encoding="utf-8")
            subprocess.run(["git", "init", "-q", str(checkout)], check=True)
            subprocess.run(["git", "-C", str(checkout), "add", "."], check=True)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(checkout),
                    "-c",
                    "user.name=Codex Test",
                    "-c",
                    "user.email=codex-test@example.invalid",
                    "commit",
                    "-q",
                    "-m",
                    "fixture",
                ],
                check=True,
            )
            commit = subprocess.run(
                ["git", "-C", str(checkout), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            with patch.object(chan_bridge, "EXPECTED_CHAN_COMMIT", commit):
                self.assertEqual(chan_bridge._verify_chan_root(checkout), commit)

                rogue = checkout / "untracked.py"
                rogue.write_text("# untracked\n", encoding="utf-8")
                with self.assertRaisesRegex(
                    chan_bridge.ChanAdapterUnavailable, "tracked/untracked"
                ):
                    chan_bridge._verify_chan_root(checkout)
                rogue.unlink()

                (checkout / "Chan.py").write_text("# tracked change\n", encoding="utf-8")
                with self.assertRaisesRegex(
                    chan_bridge.ChanAdapterUnavailable, "tracked/untracked"
                ):
                    chan_bridge._verify_chan_root(checkout)

    def test_structure_lifecycle_tracks_withdrawal_and_reappearance_in_temp_state(self) -> None:
        element = structure_element("chan-fixture-weekly-bi")
        with tempfile.TemporaryDirectory() as temp_dir:
            state_dir = Path(temp_dir)
            first = apply_structure_lifecycle(
                chan_result([element]),
                ticker="SZSE:002135",
                adjustment="qfq",
                state_dir=state_dir,
                observed_at="2026-07-20T08:00:00Z",
            )
            second = apply_structure_lifecycle(
                chan_result([]),
                ticker="SZSE:002135",
                adjustment="qfq",
                state_dir=state_dir,
                observed_at="2026-07-21T08:00:00Z",
            )
            third = apply_structure_lifecycle(
                chan_result([element]),
                ticker="SZSE:002135",
                adjustment="qfq",
                state_dir=state_dir,
                observed_at="2026-07-22T08:00:00Z",
            )

        self.assertEqual(first["counts"]["new"], 1)
        self.assertEqual(first["active_elements"][0]["first_seen"], "2026-07-20T08:00:00Z")
        self.assertEqual(second["counts"]["newly_withdrawn"], 1)
        self.assertEqual(
            second["withdrawn_elements"][0]["withdrawn"], "2026-07-21T08:00:00Z"
        )
        self.assertEqual(third["counts"]["reappeared"], 1)
        self.assertTrue(third["active_elements"][0]["reappeared"])
        self.assertEqual(third["active_elements"][0]["first_seen"], "2026-07-20T08:00:00Z")
        self.assertEqual(third["active_elements"][0]["last_changed"], "2026-07-22T08:00:00Z")

    def test_confirmed_is_cutoff_specific_and_lifecycle_records_change(self) -> None:
        original = structure_element("chan-confirmed-weekly-bi", content_hash="v1")
        revised = {
            **structure_element("chan-confirmed-weekly-bi", content_hash="v2"),
            "end": "2026-07-31",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            state_dir = Path(temp_dir)
            first = apply_structure_lifecycle(
                chan_result([original], input_digest="prefix-800"),
                ticker="SZSE:002135",
                adjustment="qfq",
                state_dir=state_dir,
                observed_at="2026-07-20T08:00:00Z",
                technical_as_of="2026-07-20",
            )
            changed = apply_structure_lifecycle(
                chan_result([revised], input_digest="prefix-900"),
                ticker="SZSE:002135",
                adjustment="qfq",
                state_dir=state_dir,
                observed_at="2026-07-31T08:00:00Z",
                technical_as_of="2026-07-31",
            )
            withdrawn = apply_structure_lifecycle(
                chan_result([], input_digest="prefix-950"),
                ticker="SZSE:002135",
                adjustment="qfq",
                state_dir=state_dir,
                observed_at="2026-08-07T08:00:00Z",
                technical_as_of="2026-08-07",
            )

        self.assertTrue(first["active_elements"][0]["confirmed"])
        self.assertEqual(changed["counts"]["changed"], 1)
        self.assertEqual(changed["active_elements"][0]["first_seen"], "2026-07-20T08:00:00Z")
        self.assertEqual(changed["active_elements"][0]["last_changed"], "2026-07-31T08:00:00Z")
        self.assertEqual(withdrawn["counts"]["newly_withdrawn"], 1)
        self.assertTrue(withdrawn["withdrawn_elements"][0]["confirmed"])
        self.assertEqual(
            withdrawn["withdrawn_elements"][0]["withdrawn"],
            "2026-08-07T08:00:00Z",
        )

    def test_state_identity_isolated_by_commit_and_profile_config(self) -> None:
        element = structure_element("chan-fixture-weekly-bi")
        with tempfile.TemporaryDirectory() as temp_dir:
            state_dir = Path(temp_dir)
            base = apply_structure_lifecycle(
                chan_result([element], commit="commit-a"),
                ticker="SZSE:002135",
                adjustment="qfq",
                state_dir=state_dir,
                write_state=False,
                technical_as_of="2026-07-20",
            )
            changed_commit = apply_structure_lifecycle(
                chan_result([element], commit="commit-b"),
                ticker="SZSE:002135",
                adjustment="qfq",
                state_dir=state_dir,
                write_state=False,
                technical_as_of="2026-07-20",
            )
            changed_profile = apply_structure_lifecycle(
                chan_result([element], commit="commit-a", strict_hash="strict-v2"),
                ticker="SZSE:002135",
                adjustment="qfq",
                state_dir=state_dir,
                write_state=False,
                technical_as_of="2026-07-20",
            )

        bundle_hashes = {
            result["state_identity"]["bundle_hash"]
            for result in (base, changed_commit, changed_profile)
        }
        state_paths = {
            result["state_path"] for result in (base, changed_commit, changed_profile)
        }
        self.assertEqual(len(bundle_hashes), 3)
        self.assertEqual(len(state_paths), 3)

    def test_lifecycle_rejects_cutoff_regression_and_marks_same_cutoff_revision(self) -> None:
        element = structure_element("chan-fixture-weekly-bi")
        with tempfile.TemporaryDirectory() as temp_dir:
            state_dir = Path(temp_dir)
            apply_structure_lifecycle(
                chan_result([element], input_digest="bars-v1"),
                ticker="SZSE:002135",
                adjustment="qfq",
                state_dir=state_dir,
                technical_as_of="2026-07-20",
            )
            revised = apply_structure_lifecycle(
                chan_result([element], input_digest="bars-v2"),
                ticker="SZSE:002135",
                adjustment="qfq",
                state_dir=state_dir,
                technical_as_of="2026-07-20",
            )
            revised_bytes = Path(revised["state_path"]).read_bytes()
            revised_state = json.loads(revised_bytes.decode("utf-8"))
            regressed = apply_structure_lifecycle(
                chan_result([element], input_digest="older-bars"),
                ticker="SZSE:002135",
                adjustment="qfq",
                state_dir=state_dir,
                technical_as_of="2026-07-19",
            )

        self.assertTrue(revised["data_revision"])
        self.assertEqual(
            revised["state_sha256"], hashlib.sha256(revised_bytes).hexdigest()
        )
        self.assertEqual(revised_state["data_revision_count"], 1)
        self.assertEqual(regressed["status"], "unavailable")
        self.assertEqual(regressed["reason_code"], "out_of_order_cutoff")
        self.assertFalse(regressed["write_performed"])

    def test_lifecycle_lock_prevents_concurrent_old_cutoff_overwrite(self) -> None:
        method = "fork" if "fork" in multiprocessing.get_all_start_methods() else "spawn"
        context = multiprocessing.get_context(method)
        with tempfile.TemporaryDirectory() as temp_dir:
            barrier = context.Barrier(2)
            queue = context.Queue()
            older = context.Process(
                target=_lifecycle_process_worker,
                args=(temp_dir, "2026-07-20", "older-run", 0.35, barrier, queue),
            )
            newer = context.Process(
                target=_lifecycle_process_worker,
                args=(temp_dir, "2026-07-21", "newer-run", 0.0, barrier, queue),
            )
            older.start()
            newer.start()
            older.join(10)
            newer.join(10)
            self.assertEqual(older.exitcode, 0)
            self.assertEqual(newer.exitcode, 0)
            results = [queue.get(timeout=2), queue.get(timeout=2)]
            state_path = next(Path(temp_dir).glob("*.structure-state.json"))
            state = json.loads(state_path.read_text(encoding="utf-8"))

        self.assertEqual(state["technical_as_of"], "2026-07-21")
        self.assertEqual(state["input_digest"], "newer-run")
        self.assertEqual(state["source_run_identity"], {"run": "newer-run"})
        self.assertTrue(any(item["status"] == "complete" for item in results))
        for item in results:
            self.assertEqual(
                item["source_run_identity"], {"run": item["input_digest"]}
            )

    def test_lifecycle_write_before_cas_rereads_newer_cutoff(self) -> None:
        element = structure_element("cas-weekly-bi")
        with tempfile.TemporaryDirectory() as temp_dir:
            state_dir = Path(temp_dir)
            seeded = apply_structure_lifecycle(
                chan_result([element], input_digest="seed"),
                ticker="SZSE:002135",
                adjustment="qfq",
                state_dir=state_dir,
                technical_as_of="2026-07-20",
            )
            state_path = Path(seeded["state_path"])
            real_read = chan_bridge._read_state_snapshot
            read_count = 0

            def inject_newer_state(*args: object, **kwargs: object) -> object:
                nonlocal read_count
                read_count += 1
                if read_count == 2:
                    external = json.loads(state_path.read_text(encoding="utf-8"))
                    external["technical_as_of"] = "2026-07-22"
                    external["input_digest"] = "external-newer"
                    external["source_run_identity"] = {"run": "external"}
                    external["state_revision"] += 1
                    chan_bridge._atomic_json_write(state_path, external)
                return real_read(*args, **kwargs)

            with patch.object(
                chan_bridge,
                "_read_state_snapshot",
                side_effect=inject_newer_state,
            ):
                stale = apply_structure_lifecycle(
                    chan_result([element], input_digest="stale"),
                    ticker="SZSE:002135",
                    adjustment="qfq",
                    state_dir=state_dir,
                    technical_as_of="2026-07-21",
                    source_run_identity={"run": "stale"},
                )
            final_state = json.loads(state_path.read_text(encoding="utf-8"))

        self.assertEqual(stale["status"], "unavailable")
        self.assertEqual(stale["reason_code"], "out_of_order_cutoff")
        self.assertFalse(stale["write_performed"])
        self.assertEqual(final_state["technical_as_of"], "2026-07-22")
        self.assertEqual(final_state["source_run_identity"], {"run": "external"})

    def test_bsp_remains_a_neutral_candidate_not_a_trade_order(self) -> None:
        bsp = structure_element(
            "chan-fixture-daily-bsp", timeframe="daily", layer="bsp"
        )
        bsp.update(
            {
                "bsp_types": ["1", "2"],
                "morphology_side": "lower_turning_structure",
                "interpretation": "neutral_candidate_not_trade_signal",
            }
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            lifecycle = apply_structure_lifecycle(
                chan_result([bsp]),
                ticker="SZSE:002135",
                adjustment="qfq",
                state_dir=Path(temp_dir),
                write_state=False,
                observed_at="2026-07-20T08:00:00Z",
            )

        self.assertFalse(lifecycle["write_performed"])
        self.assertEqual(
            lifecycle["active_elements"][0]["interpretation"],
            "neutral_candidate_not_trade_signal",
        )

    def test_timeframe_context_maps_parent_children_and_zone_nesting(self) -> None:
        stable_zones = [
            {
                **structure_element(
                    "monthly-zone", timeframe="monthly", layer="zone"
                ),
                "lower": 95.0,
                "upper": 115.0,
            },
            {
                **structure_element("weekly-zone", timeframe="weekly", layer="zone"),
                "lower": 100.0,
                "upper": 110.0,
            },
            {
                **structure_element("daily-zone", timeframe="daily", layer="zone"),
                "lower": 108.0,
                "upper": 118.0,
            },
        ]
        context = build_timeframe_context(
            synthetic_bars(),
            {"profile_stability": {"stable_elements": stable_zones}},
        )

        self.assertTrue(context["monthly_to_weekly"])
        self.assertTrue(context["weekly_to_daily"])
        self.assertTrue(
            all(item["child_count"] > 0 for item in context["weekly_to_daily"])
        )
        self.assertEqual(
            context["interval_nesting"]["monthly_weekly"]["relationship"],
            "child_inside_parent",
        )
        self.assertEqual(
            context["interval_nesting"]["weekly_daily"]["relationship"], "overlap"
        )
        self.assertEqual(
            context["interval_nesting"]["monthly_weekly"]["interpretation"],
            "structural_context_not_directional_signal",
        )

    def test_engine_comparison_uses_semantic_anchors_not_structure_counts(self) -> None:
        stable_bi = [
            {
                **structure_element(
                    f"{timeframe}-bi", timeframe=timeframe, layer="bi"
                ),
                "end": end,
            }
            for timeframe, end in (
                ("monthly", "2026-06-30"),
                ("weekly", "2026-07-17"),
                ("daily", "2026-07-20"),
            )
        ]
        czsc = {
            "timeframes": {
                timeframe: {
                    "last_completed_bi": {"direction": "up", "end": end}
                }
                for timeframe, end in (
                    ("monthly", "2026-06-30"),
                    ("weekly", "2026-07-17"),
                    ("daily", "2026-07-20"),
                )
            }
        }
        chan = {
            "status": "complete",
            "profile_stability": {
                "status": "complete",
                "stable_elements": stable_bi,
            },
        }

        comparison = compare_engines(czsc, chan)

        self.assertEqual(comparison["status"], "complete")
        self.assertTrue(
            all(
                not item["count_difference_used_for_status"]
                for item in comparison["comparisons"]
            )
        )
        self.assertIn("数量差异本身不判 disputed", comparison["note"])

    def test_profile_critical_direction_disagreement_is_disputed(self) -> None:
        strict = structure_element("strict-monthly", timeframe="monthly")
        broad = {
            **structure_element("broad-monthly", timeframe="monthly"),
            "profile": "broad",
            "direction": "down",
        }
        stability = compare_profiles(
            {"strict": profile_with([strict]), "broad": profile_with([broad])}
        )

        self.assertEqual(stability["status"], "disputed")
        monthly = next(
            item
            for item in stability["critical_direction_checks"]
            if item["timeframe"] == "monthly"
        )
        self.assertEqual(monthly["status"], "disputed")
        self.assertEqual(monthly["values"], {"strict": "up", "broad": "down"})

    def test_overall_status_uses_weakest_gate_and_blocks_directional_conclusion(self) -> None:
        class StubMarketResult:
            ticker = "SZSE:002135"
            adjustment = "qfq"
            data_quality_status = "complete"
            data = synthetic_bars()

            @staticmethod
            def manifest() -> dict[str, object]:
                return {"provider": "offline_fixture", "data_quality_status": "complete"}

        czsc = {
            "technical_as_of": "2026-03-25",
            "engine": {"name": "CZSC", "version": "fixture"},
            "timeframes": {},
        }
        chan = chan_result([])
        chan["profile_stability"] = {
            "status": "disputed",
            "stable_elements": [],
        }
        with (
            patch.object(technical_snapshot, "analyze_multitimeframe", return_value=czsc),
            patch.object(technical_snapshot, "analyze_chan_profiles", return_value=chan),
            patch.object(
                technical_snapshot,
                "compare_engines",
                return_value={"status": "disputed", "comparisons": []},
            ),
            patch.object(technical_snapshot, "build_timeframe_context", return_value={}),
            patch.object(
                technical_snapshot,
                "apply_structure_lifecycle",
                return_value={"status": "complete", "write_performed": False},
            ),
        ):
            payload = technical_snapshot.build_payload(
                StubMarketResult(), state_dir=Path("/unused"), write_state=False
            )

        self.assertEqual(payload["overall_technical_status"], "disputed")
        self.assertFalse(payload["directional_conclusion_allowed"])
        self.assertIn(
            {"layer": "engine_consistency_status", "status": "disputed"},
            payload["directional_conclusion_blockers"],
        )
        self.assertIn(
            {"layer": "profile_stability_status", "status": "disputed"},
            payload["directional_conclusion_blockers"],
        )

    def test_static_audit_chart_is_png_and_labels_bsp_as_neutral(self) -> None:
        zone = {
            **structure_element("monthly-zone", timeframe="monthly", layer="zone"),
            "start": "2025-06-02",
            "end": "2026-02-27",
            "lower": 98.0,
            "upper": 112.0,
        }
        bsp = {
            **structure_element("daily-bsp", timeframe="daily", layer="bsp"),
            "start": "2026-02-20",
            "end": "2026-02-20",
            "price": 108.0,
            "morphology_side": "lower_turning_structure",
            "interpretation": "neutral_candidate_not_trade_signal",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output_path = root / "audit.png"
            with patch.dict(os.environ, {"MPLCONFIGDIR": str(root / "mpl")}, clear=False):
                artifact = render_audit_chart(
                    synthetic_bars(), chan_result([zone, bsp]), output_path
                )
            signature = output_path.read_bytes()[:8]

        self.assertEqual(artifact["status"], "complete")
        self.assertEqual(signature, b"\x89PNG\r\n\x1a\n")
        self.assertTrue(artifact["static"])
        self.assertFalse(artifact["animation"])
        self.assertEqual(
            artifact["bsp_interpretation"], "neutral_candidate_not_trade_signal"
        )

    def test_native_static_charts_render_three_timeframes_from_fixture_runtime(self) -> None:
        frame = synthetic_bars()
        reset_native_chart_fakes()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            paths = native_chart_paths(root)
            with (
                patch.object(
                    chan_bridge, "_load_runtime", return_value=fake_chan_runtime()
                ),
                patch.object(
                    chan_bridge,
                    "_load_native_plot_driver",
                    return_value=(_FakePlotDriver, _FakePyplot),
                ),
                patch.dict(
                    os.environ, {"MPLCONFIGDIR": str(root / "mpl")}, clear=False
                ),
            ):
                artifact = chan_bridge.render_native_chan_charts(frame, paths)

            artifact_copy = json.loads(json.dumps(artifact))
            file_observations = {
                timeframe: {
                    "exists": path.is_file(),
                    "magic": path.read_bytes()[:8],
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "bytes": path.stat().st_size,
                }
                for timeframe, path in paths.items()
            }

        self.assertEqual(artifact_copy["status"], "complete")
        self.assertEqual(artifact_copy["profile"], "strict")
        self.assertEqual(
            artifact_copy["upstream_commit"], chan_bridge.EXPECTED_CHAN_COMMIT
        )
        self.assertEqual(
            artifact_copy["config_hash"],
            chan_bridge._profile_hash("strict", chan_bridge.CHAN_PROFILES["strict"]),
        )
        self.assertEqual(artifact_copy["input_digest"], normalized_frame_digest(frame))
        self.assertTrue(artifact_copy["static"])
        self.assertFalse(artifact_copy["animation"])
        self.assertFalse(artifact_copy["interactive"])
        self.assertFalse(artifact_copy["upstream_dataapi_used"])
        self.assertEqual(
            artifact_copy["bsp_interpretation"],
            "neutral_candidate_not_trade_signal",
        )
        self.assertEqual(
            set(artifact_copy["plot_layers"]), set(chan_bridge.NATIVE_PLOT_LAYERS)
        )
        self.assertEqual(
            set(artifact_copy["charts"]), {"monthly", "weekly", "daily"}
        )
        for timeframe, observation in file_observations.items():
            chart = artifact_copy["charts"][timeframe]
            self.assertEqual(chart["status"], "complete")
            self.assertEqual(chart["timeframe"], timeframe)
            self.assertEqual(Path(chart["path"]), paths[timeframe].resolve())
            self.assertEqual(chart["format"], "png")
            self.assertTrue(observation["exists"])
            self.assertEqual(observation["magic"], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(chart["sha256"], observation["sha256"])
            self.assertEqual(chart["bytes"], observation["bytes"])
            self.assertGreater(chart["bytes"], 8)
        self.assertEqual(
            _FakeChan.data_sources, ["external-normalized-bars"] * 3
        )
        self.assertEqual(
            set(_FakeChan.triggered_levels), {"monthly", "weekly", "daily"}
        )
        self.assertEqual(len(_FakePlotDriver.calls), 3)
        self.assertEqual(_FakePyplot.closed_count, 3)
        for call in _FakePlotDriver.calls:
            self.assertEqual(call["data_src"], "external-normalized-bars")
            enabled = {
                key for key, value in call["plot_config"].items() if value
            }
            self.assertEqual(enabled, set(chan_bridge.NATIVE_PLOT_LAYERS))
            self.assertEqual(
                call["plot_para"]["zs"]["show_text"],
                call["level"] != "daily",
            )

    def test_native_chart_runtime_failure_is_structured_and_has_no_fake_paths(self) -> None:
        frame = synthetic_bars()
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = native_chart_paths(Path(temp_dir))
            with patch.object(
                chan_bridge,
                "_load_runtime",
                side_effect=RuntimeError("injected pinned runtime failure"),
            ):
                artifact = chan_bridge.render_native_chan_charts(frame, paths)
            existing = [path for path in paths.values() if path.exists()]

        self.assertEqual(artifact["status"], "unavailable")
        self.assertEqual(artifact["profile"], "strict")
        self.assertEqual(artifact["input_digest"], normalized_frame_digest(frame))
        self.assertFalse(artifact["upstream_dataapi_used"])
        self.assertEqual(existing, [])
        for timeframe, chart in artifact["charts"].items():
            self.assertEqual(chart["status"], "unavailable")
            self.assertEqual(chart["timeframe"], timeframe)
            self.assertIsNone(chart.get("path"))
            self.assertEqual(
                Path(chart["intended_path"]), paths[timeframe].resolve()
            )
            self.assertIn("injected pinned runtime failure", chart["reason"])

    def test_one_native_chart_failure_degrades_only_that_timeframe(self) -> None:
        frame = synthetic_bars()
        reset_native_chart_fakes()
        _FakePlotDriver.fail_level = "weekly"
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                paths = native_chart_paths(root)
                with (
                    patch.object(
                        chan_bridge,
                        "_load_runtime",
                        return_value=fake_chan_runtime(),
                    ),
                    patch.object(
                        chan_bridge,
                        "_load_native_plot_driver",
                        return_value=(_FakePlotDriver, _FakePyplot),
                    ),
                    patch.dict(
                        os.environ,
                        {"MPLCONFIGDIR": str(root / "mpl")},
                        clear=False,
                    ),
                ):
                    artifact = chan_bridge.render_native_chan_charts(frame, paths)
                files_exist = {
                    timeframe: path.exists() for timeframe, path in paths.items()
                }
        finally:
            _FakePlotDriver.fail_level = None

        self.assertEqual(artifact["status"], "degraded")
        self.assertEqual(artifact["charts"]["monthly"]["status"], "complete")
        self.assertEqual(artifact["charts"]["daily"]["status"], "complete")
        weekly = artifact["charts"]["weekly"]
        self.assertEqual(weekly["status"], "unavailable")
        self.assertIsNone(weekly.get("path"))
        self.assertEqual(Path(weekly["intended_path"]), paths["weekly"].resolve())
        self.assertIn("injected weekly native chart failure", weekly["reason"])
        self.assertEqual(
            files_exist, {"monthly": True, "weekly": False, "daily": True}
        )

    def test_native_chart_output_paths_under_raw_or_wiki_fail_closed(self) -> None:
        frame = synthetic_bars()
        for protected in (
            REPO_ROOT / "raw",
            REPO_ROOT / "wiki",
            REPO_ROOT / "RAW",
            REPO_ROOT / "WIKI",
        ):
            leaf = protected / f".native-chart-contract-{os.getpid()}"
            paths = native_chart_paths(leaf)
            self.assertFalse(leaf.exists())
            with self.subTest(protected=protected), patch.object(
                chan_bridge,
                "_load_runtime",
                side_effect=AssertionError("runtime must not load for unsafe paths"),
            ) as runtime_loader:
                artifact = chan_bridge.render_native_chan_charts(frame, paths)
            runtime_loader.assert_not_called()
            self.assertEqual(artifact["status"], "unavailable")
            self.assertEqual(artifact["reason_code"], "unsafe_output_path")
            self.assertFalse(leaf.exists())
            self.assertTrue(
                all(chart.get("path") is None for chart in artifact["charts"].values())
            )
            self.assertTrue(
                all(
                    chart.get("intended_path")
                    for chart in artifact["charts"].values()
                )
            )

    def test_audit_chart_output_paths_under_raw_or_wiki_fail_closed(self) -> None:
        frame = synthetic_bars()
        for protected in (
            REPO_ROOT / "raw",
            REPO_ROOT / "wiki",
            REPO_ROOT / "RAW",
            REPO_ROOT / "WIKI",
        ):
            output_path = (
                protected
                / f".audit-chart-contract-{os.getpid()}"
                / "audit.png"
            )
            self.assertFalse(output_path.parent.exists())
            with self.subTest(protected=protected):
                artifact = render_audit_chart(frame, chan_result([]), output_path)
            self.assertEqual(artifact["status"], "unavailable")
            self.assertEqual(artifact["reason_code"], "unsafe_output_path")
            self.assertIsNone(artifact.get("path"))
            self.assertEqual(
                Path(artifact["intended_path"]), output_path.resolve()
            )
            self.assertFalse(output_path.parent.exists())

    def test_matplotlib_config_dir_rejects_protected_aliases_without_writes(self) -> None:
        candidates = (
            REPO_ROOT / "raw",
            REPO_ROOT / "wiki",
            REPO_ROOT / "RAW",
            REPO_ROOT / "WIKI",
        )
        for protected in candidates:
            config_dir = protected / f".mpl-contract-{os.getpid()}"
            self.assertFalse(config_dir.exists())
            with (
                self.subTest(protected=protected),
                patch.dict(
                    os.environ,
                    {"MPLCONFIGDIR": str(config_dir)},
                    clear=False,
                ),
                self.assertRaisesRegex(
                    chan_bridge.ChanAdapterUnavailable,
                    "MPLCONFIGDIR 不得指向",
                ),
            ):
                chan_bridge._prepare_matplotlib_config_dir()
            self.assertFalse(config_dir.exists())

        with tempfile.TemporaryDirectory() as temp_dir:
            alias = Path(temp_dir) / "protected-alias"
            alias.symlink_to(REPO_ROOT / "raw", target_is_directory=True)
            config_dir = alias / f".mpl-contract-{os.getpid()}"
            with (
                patch.dict(
                    os.environ,
                    {"MPLCONFIGDIR": str(config_dir)},
                    clear=False,
                ),
                self.assertRaisesRegex(
                    chan_bridge.ChanAdapterUnavailable,
                    "MPLCONFIGDIR 不得指向",
                ),
            ):
                chan_bridge._prepare_matplotlib_config_dir()
            self.assertFalse(config_dir.exists())

    def test_protected_matplotlib_config_degrades_audit_and_native_artifacts(self) -> None:
        frame = synthetic_bars()
        config_dir = REPO_ROOT / "RAW" / f".mpl-contract-{os.getpid()}"
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            audit_path = root / "audit.png"
            with patch.dict(
                os.environ,
                {"MPLCONFIGDIR": str(config_dir)},
                clear=False,
            ):
                audit = render_audit_chart(frame, chan_result([]), audit_path)

            paths = native_chart_paths(root)

            def guarded_plot_loader(_: dict[str, object]) -> tuple[object, object]:
                chan_bridge._prepare_matplotlib_config_dir()
                raise AssertionError("protected MPLCONFIGDIR should fail first")

            with (
                patch.object(
                    chan_bridge,
                    "_load_runtime",
                    return_value=fake_chan_runtime(),
                ),
                patch.object(
                    chan_bridge,
                    "_load_native_plot_driver",
                    side_effect=guarded_plot_loader,
                ),
                patch.dict(
                    os.environ,
                    {"MPLCONFIGDIR": str(config_dir)},
                    clear=False,
                ),
            ):
                native = chan_bridge.render_native_chan_charts(frame, paths)

        self.assertEqual(audit["status"], "unavailable")
        self.assertIsNone(audit.get("path"))
        self.assertEqual(Path(audit["intended_path"]), audit_path.resolve())
        self.assertFalse(audit_path.exists())
        self.assertIn("MPLCONFIGDIR 不得指向", audit["reason"])
        self.assertEqual(native["status"], "unavailable")
        for chart in native["charts"].values():
            self.assertIsNone(chart.get("path"))
            self.assertIn("MPLCONFIGDIR 不得指向", chart["reason"])
        self.assertFalse(config_dir.exists())

    def test_native_chart_partial_failure_does_not_abort_report_or_manifest(self) -> None:
        frame = synthetic_bars()
        expected_input_digest = normalized_frame_digest(frame)

        def degraded_native_charts(
            _: pd.DataFrame,
            output_paths: dict[str, Path],
            **__: object,
        ) -> dict[str, object]:
            self.assertEqual(set(output_paths), {"monthly", "weekly", "daily"})
            for timeframe, path in output_paths.items():
                self.assertTrue(path.name.endswith(f".chan-native-{timeframe}.png"))
            charts: dict[str, dict[str, object]] = {}
            for timeframe, path in output_paths.items():
                if timeframe == "weekly":
                    charts[timeframe] = {
                        "status": "unavailable",
                        "timeframe": timeframe,
                        "path": None,
                        "intended_path": str(path.resolve()),
                        "reason": "injected single-chart failure",
                    }
                    continue
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"\x89PNG\r\n\x1a\nfixture")
                charts[timeframe] = {
                    "status": "complete",
                    "timeframe": timeframe,
                    "path": str(path.resolve()),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "bytes": path.stat().st_size,
                    "format": "png",
                }
            return {
                "status": "degraded",
                "renderer": "chan.py.Plot.PlotDriver.CPlotDriver",
                "profile": "strict",
                "upstream_commit": chan_bridge.EXPECTED_CHAN_COMMIT,
                "config_hash": "strict-fixture",
                "input_digest": expected_input_digest,
                "input_contract": "normalized_local_bars_only_no_chan_dataapi",
                "upstream_dataapi_used": False,
                "static": True,
                "animation": False,
                "interactive": False,
                "bsp_interpretation": "neutral_candidate_not_trade_signal",
                "plot_layers": list(chan_bridge.NATIVE_PLOT_LAYERS),
                "reason": "一个或多个 chan.py 原生静态图生成失败",
                "charts": charts,
            }

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fixture_csv = root / "bars.csv"
            output_dir = root / "output"
            frame.to_csv(fixture_csv, index=False)
            argv = [
                str(SCRIPTS / "technical_snapshot.py"),
                "--ticker",
                "SZSE:002135",
                "--offline-csv",
                str(fixture_csv),
                "--start",
                pd.Timestamp(frame["dt"].min()).date().isoformat(),
                "--end",
                pd.Timestamp(frame["dt"].max()).date().isoformat(),
                "--output-dir",
                str(output_dir),
                "--cache-dir",
                str(root / "cache"),
                "--state-dir",
                str(root / "state"),
                "--no-state-write",
            ]
            stdout = io.StringIO()
            with (
                patch.object(
                    technical_snapshot,
                    "build_payload",
                    return_value=minimal_snapshot_payload(frame),
                ),
                patch.object(
                    technical_snapshot,
                    "save_cache",
                    return_value={},
                ),
                patch.object(
                    technical_snapshot,
                    "render_markdown",
                    return_value="# fixture report\n",
                ),
                patch.object(
                    technical_snapshot,
                    "render_audit_chart",
                    return_value={
                        "status": "unavailable",
                        "path": None,
                        "reason": "fixture audit unavailable",
                    },
                ),
                patch.object(
                    technical_snapshot,
                    "render_native_chan_charts",
                    side_effect=degraded_native_charts,
                ),
                patch.object(sys, "argv", argv),
                redirect_stdout(stdout),
            ):
                exit_code = technical_snapshot.main()
            summary = json.loads(stdout.getvalue().strip().splitlines()[-1])
            payload = json.loads(Path(summary["json"]).read_text(encoding="utf-8"))
            manifest = json.loads(
                Path(summary["manifest"]).read_text(encoding="utf-8")
            )
            report_files_exist = {
                "json": Path(summary["json"]).is_file(),
                "markdown": Path(summary["markdown"]).is_file(),
                "manifest": Path(summary["manifest"]).is_file(),
            }

        self.assertEqual(exit_code, 0)
        self.assertEqual(report_files_exist, {"json": True, "markdown": True, "manifest": True})
        self.assertEqual(summary["status"], "ok")
        self.assertEqual(summary["native_chan_charts"]["status"], "degraded")
        native_payload = payload["artifacts"]["native_chan_charts"]
        native_manifest = manifest["artifacts"]["native_chan_charts"]
        for artifact in (native_payload, native_manifest):
            self.assertEqual(artifact["status"], "degraded")
            self.assertEqual(artifact["profile"], "strict")
            self.assertEqual(
                artifact["upstream_commit"], chan_bridge.EXPECTED_CHAN_COMMIT
            )
            self.assertEqual(artifact["config_hash"], "strict-fixture")
            self.assertEqual(artifact["input_digest"], expected_input_digest)
            self.assertEqual(
                artifact["bsp_interpretation"],
                "neutral_candidate_not_trade_signal",
            )
            self.assertFalse(artifact["animation"])
            self.assertFalse(artifact["interactive"])
            weekly = artifact["charts"]["weekly"]
            self.assertIsNone(weekly.get("path"))
            self.assertTrue(weekly["intended_path"].endswith(".chan-native-weekly.png"))

    def test_offline_fixture_enforces_cutoff_and_ticker_identity(self) -> None:
        frame = synthetic_bars()
        cutoff = pd.Timestamp(frame.iloc[199]["dt"]).date().isoformat()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fixture_csv = root / "bars.csv"
            frame.to_csv(fixture_csv, index=False)
            result = technical_snapshot._offline_result(
                "SZSE:002135",
                fixture_csv,
                pd.Timestamp(frame.iloc[0]["dt"]).date().isoformat(),
                cutoff,
                "qfq",
            )

            mismatched = frame.copy()
            mismatched["symbol"] = "600519.SH"
            mismatched_csv = root / "wrong-symbol.csv"
            mismatched.to_csv(mismatched_csv, index=False)
            with self.assertRaisesRegex(ValueError, "symbol"):
                technical_snapshot._offline_result(
                    "SZSE:002135",
                    mismatched_csv,
                    pd.Timestamp(frame.iloc[0]["dt"]).date().isoformat(),
                    cutoff,
                    "qfq",
                )

        self.assertEqual(len(result.data), 200)
        self.assertEqual(pd.Timestamp(result.data["dt"].max()).date().isoformat(), cutoff)
        self.assertEqual(result.data_quality_status, "degraded")

    def test_technical_cli_rejects_derived_paths_under_raw_or_wiki(self) -> None:
        safe_root = Path(tempfile.gettempdir()) / "a-share-safe-output"
        for protected in (
            REPO_ROOT / "raw",
            REPO_ROOT / "wiki",
            REPO_ROOT / "RAW",
            REPO_ROOT / "WIKI",
        ):
            with self.subTest(protected=protected), self.assertRaisesRegex(
                ValueError, "不得指向"
            ):
                technical_snapshot._assert_safe_derived_directories(
                    output_dir=protected / "should-not-exist",
                    cache_dir=safe_root / "cache",
                    state_dir=safe_root / "state",
                )

    def test_offline_cli_keeps_state_and_artifacts_inside_temp_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fixture_csv = root / "bars.csv"
            output_dir = root / "output"
            cache_dir = root / "cache"
            state_dir = root / "state"
            synthetic_bars().to_csv(fixture_csv, index=False)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "technical_snapshot.py"),
                    "--ticker",
                    "SZSE:002135",
                    "--offline-csv",
                    str(fixture_csv),
                    "--output-dir",
                    str(output_dir),
                    "--cache-dir",
                    str(cache_dir),
                    "--state-dir",
                    str(state_dir),
                    "--chan-py-path",
                    str(root / "missing-chan"),
                    "--no-audit-chart",
                ],
                check=True,
                capture_output=True,
                text=True,
                env={
                    **os.environ,
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "MPLCONFIGDIR": str(root / "mpl"),
                },
            )
            summary = json.loads(completed.stdout)
            payload = json.loads(Path(summary["json"]).read_text(encoding="utf-8"))
            manifest = json.loads(
                Path(summary["manifest"]).read_text(encoding="utf-8")
            )
            state_receipt = json.loads(
                Path(summary["state_commit_receipt"]).read_text(encoding="utf-8")
            )
            native_files = list(output_dir.glob("*.chan-native-*.png"))

            self.assertEqual(summary["status"], "ok")
            self.assertEqual(summary["overall_technical_status"], "unavailable")
            self.assertFalse(summary["directional_conclusion_allowed"])
            self.assertTrue(Path(summary["json"]).is_relative_to(output_dir.resolve()))
            self.assertTrue(Path(summary["manifest"]).is_relative_to(output_dir.resolve()))
            self.assertTrue(
                Path(summary["state_commit_receipt"]).is_relative_to(
                    output_dir.resolve()
                )
            )
            self.assertFalse(state_dir.exists())
            self.assertEqual(
                state_receipt["state_commit"]["reason_code"],
                "market_data_quality_not_complete",
            )
            self.assertEqual(state_receipt["receipt_status"], "final")
            self.assertFalse(state_receipt["state_commit"]["write_performed"])
            self.assertEqual(
                payload["artifacts"]["audit_chart"]["status"], "not_generated"
            )
            self.assertIsNone(payload["artifacts"]["audit_chart"].get("path"))
            self.assertTrue(
                payload["artifacts"]["audit_chart"]["intended_path"].endswith(
                    ".audit.png"
                )
            )
            self.assertIsNone(manifest["artifacts"]["audit_chart"].get("path"))
            self.assertTrue(
                manifest["artifacts"]["audit_chart"]["intended_path"].endswith(
                    ".audit.png"
                )
            )
            native_payload = payload["artifacts"]["native_chan_charts"]
            native_manifest = manifest["artifacts"]["native_chan_charts"]
            self.assertEqual(native_payload["status"], "not_generated")
            self.assertEqual(native_payload["reason"], "CLI --no-audit-chart")
            self.assertEqual(native_manifest["status"], "not_generated")
            self.assertEqual(native_files, [])
            for timeframe in ("monthly", "weekly", "daily"):
                payload_chart = native_payload["charts"][timeframe]
                manifest_chart = native_manifest["charts"][timeframe]
                self.assertIsNone(payload_chart.get("path"))
                self.assertIsNone(manifest_chart.get("path"))
                self.assertTrue(payload_chart["intended_path"].endswith(
                    f".chan-native-{timeframe}.png"
                ))
                self.assertTrue(manifest_chart["intended_path"].endswith(
                    f".chan-native-{timeframe}.png"
                ))
            self.assertFalse(
                payload["analysis"]["structure_lifecycle"]["write_performed"]
            )

    def test_no_native_chart_flag_keeps_audit_path_but_skips_all_native_files(self) -> None:
        frame = synthetic_bars()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fixture_csv = root / "bars.csv"
            output_dir = root / "output"
            frame.to_csv(fixture_csv, index=False)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "technical_snapshot.py"),
                    "--ticker",
                    "SZSE:002135",
                    "--offline-csv",
                    str(fixture_csv),
                    "--start",
                    pd.Timestamp(frame["dt"].min()).date().isoformat(),
                    "--end",
                    pd.Timestamp(frame["dt"].max()).date().isoformat(),
                    "--output-dir",
                    str(output_dir),
                    "--cache-dir",
                    str(root / "cache"),
                    "--state-dir",
                    str(root / "state"),
                    "--chan-py-path",
                    str(root / "missing-chan"),
                    "--no-state-write",
                    "--no-native-chan-charts",
                ],
                check=True,
                capture_output=True,
                text=True,
                env={
                    **os.environ,
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "MPLCONFIGDIR": str(root / "mpl"),
                },
            )
            summary = json.loads(completed.stdout)
            payload = json.loads(Path(summary["json"]).read_text(encoding="utf-8"))
            manifest = json.loads(
                Path(summary["manifest"]).read_text(encoding="utf-8")
            )
            native_files = list(output_dir.glob("*.chan-native-*.png"))

        self.assertEqual(summary["status"], "ok")
        self.assertNotEqual(
            payload["artifacts"]["audit_chart"]["status"], "not_generated"
        )
        native_payload = payload["artifacts"]["native_chan_charts"]
        native_manifest = manifest["artifacts"]["native_chan_charts"]
        self.assertEqual(native_payload["status"], "not_generated")
        self.assertEqual(native_payload["reason"], "CLI --no-native-chan-charts")
        self.assertEqual(native_manifest["status"], "not_generated")
        self.assertEqual(native_files, [])
        for timeframe in ("monthly", "weekly", "daily"):
            payload_chart = native_payload["charts"][timeframe]
            manifest_chart = native_manifest["charts"][timeframe]
            self.assertIsNone(payload_chart.get("path"))
            self.assertIsNone(manifest_chart.get("path"))
            self.assertTrue(
                payload_chart["intended_path"].endswith(
                    f".chan-native-{timeframe}.png"
                )
            )
            self.assertTrue(
                manifest_chart["intended_path"].endswith(
                    f".chan-native-{timeframe}.png"
                )
            )

    @unittest.skipUnless(
        os.environ.get("CHAN_PY_SMOKE_PATH"),
        "set CHAN_PY_SMOKE_PATH for the opt-in pinned chan.py prefix smoke",
    )
    def test_opt_in_real_chan_prefixes_respect_each_cutoff(self) -> None:
        frame = synthetic_bars(900)
        prefix_800 = frame.iloc[:800].copy()
        prefix_900 = frame.iloc[:900].copy()
        first = analyze_chan_profiles(
            prefix_800, chan_path=Path(os.environ["CHAN_PY_SMOKE_PATH"])
        )
        second = analyze_chan_profiles(
            prefix_900, chan_path=Path(os.environ["CHAN_PY_SMOKE_PATH"])
        )

        self.assertNotEqual(first["input_digest"], second["input_digest"])
        for result, cutoff in (
            (first, prefix_800["dt"].max()),
            (second, prefix_900["dt"].max()),
        ):
            self.assertNotEqual(result["status"], "unavailable")
            for profile in result["profiles"].values():
                for timeframe in profile["timeframes"].values():
                    self.assertLessEqual(pd.Timestamp(timeframe["as_of"]), cutoff)
                    for element in timeframe["elements"]:
                        for key in ("start", "end"):
                            if element.get(key):
                                self.assertLessEqual(pd.Timestamp(element[key]), cutoff)

    @unittest.skipUnless(
        os.environ.get("CHAN_PY_SMOKE_PATH"),
        "set CHAN_PY_SMOKE_PATH for the opt-in pinned chan.py native-chart smoke",
    )
    def test_opt_in_real_pinned_chan_renders_three_native_pngs(self) -> None:
        frame = synthetic_bars(900)
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            paths = native_chart_paths(root)
            with patch.dict(
                os.environ,
                {
                    "MPLBACKEND": "Agg",
                    "MPLCONFIGDIR": str(root / "mpl"),
                },
                clear=False,
            ):
                artifact = chan_bridge.render_native_chan_charts(
                    frame,
                    paths,
                    chan_path=Path(os.environ["CHAN_PY_SMOKE_PATH"]),
                )
            observations = {
                timeframe: {
                    "magic": path.read_bytes()[:8],
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "bytes": path.stat().st_size,
                }
                for timeframe, path in paths.items()
            }

        self.assertEqual(artifact["status"], "complete")
        self.assertEqual(artifact["profile"], "strict")
        self.assertEqual(
            artifact["upstream_commit"], chan_bridge.EXPECTED_CHAN_COMMIT
        )
        self.assertFalse(artifact["upstream_dataapi_used"])
        self.assertFalse(artifact["animation"])
        self.assertFalse(artifact["interactive"])
        for timeframe, observation in observations.items():
            chart = artifact["charts"][timeframe]
            self.assertEqual(chart["status"], "complete")
            self.assertEqual(observation["magic"], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(chart["sha256"], observation["sha256"])
            self.assertEqual(chart["bytes"], observation["bytes"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
