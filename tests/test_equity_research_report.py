#!/usr/bin/env python3
"""Tests for automatic non-canonical equity-research report archiving."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "equity-research" / "scripts" / "save_report.py"
SPEC = importlib.util.spec_from_file_location("save_equity_report", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class EquityResearchReportTests(unittest.TestCase):
    def test_default_output_directory_is_canonical_safe_archive(self) -> None:
        self.assertEqual(
            MODULE.DEFAULT_OUTPUT_DIR,
            REPO_ROOT / "output" / "equity-research",
        )

    def test_report_is_noncanonical_atomic_and_never_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            output_dir = Path(temporary_dir) / "reports"
            kwargs = {
                "body": "## 研究结论\n\n测试报告正文。",
                "ticker": "SSE:600519",
                "as_of": "2026-08-01",
                "listing_regime": "a_share",
                "horizon": "12-24m",
                "wiki_cutoff": "2026-07-31",
                "market_rules_as_of": "2026-08-01",
                "report_status": "complete",
                "generated_at": "2026-08-01T12:34:56Z",
                "output_dir": output_dir,
            }

            first = MODULE.save_report(**kwargs)
            second = MODULE.save_report(**kwargs)

            self.assertNotEqual(first, second)
            self.assertEqual(first.name, "sse-600519-2026-08-01-20260801T123456Z.md")
            self.assertEqual(second.name, "sse-600519-2026-08-01-20260801T123456Z-2.md")
            content = first.read_text(encoding="utf-8")
            self.assertIn("canonical: false", content)
            self.assertIn('ticker: "SSE:600519"', content)
            self.assertIn('listing_regime: "a_share"', content)
            self.assertIn('report_status: "complete"', content)
            self.assertIn(
                'canonical_write_status_at_generation: "pending_approval"',
                content,
            )
            self.assertIn("## 研究结论", content)
            self.assertEqual(list(output_dir.glob("*.tmp")), [])

    def test_rejects_raw_and_wiki_destinations(self) -> None:
        kwargs = {
            "body": "## 报告\n\n正文。",
            "ticker": "NASDAQ:NVDA",
            "as_of": "2026-08-01",
        }
        for forbidden in (REPO_ROOT / "raw" / "report", REPO_ROOT / "wiki" / "report"):
            with self.subTest(forbidden=forbidden):
                with self.assertRaises(ValueError):
                    MODULE.save_report(output_dir=forbidden, **kwargs)
                self.assertFalse(forbidden.exists())

    def test_rejects_invalid_metadata_or_embedded_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            output_dir = Path(temporary_dir)
            with self.assertRaises(ValueError):
                MODULE.save_report(
                    body="正文", ticker="600519", as_of="2026-08-01", output_dir=output_dir
                )
            with self.assertRaises(ValueError):
                MODULE.save_report(
                    body="---\ntitle: duplicate\n---\n正文",
                    ticker="SSE:600519",
                    as_of="2026-08-01",
                    output_dir=output_dir,
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
