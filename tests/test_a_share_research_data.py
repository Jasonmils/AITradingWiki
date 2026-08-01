#!/usr/bin/env python3
"""Offline contract tests for the shared A-share research-data adapters."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "skills" / "a-share-research-data" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from research_data import (  # noqa: E402
    ALL_MODULES,
    CachingTransport,
    FixtureTransport,
    HttpResponse,
    ResearchDataClient,
    SecurityId,
    build_snapshot,
)


ENVELOPE_FIELDS = {
    "canonical_ticker",
    "provider",
    "endpoint",
    "source_url",
    "queried_at",
    "response_fetched_at",
    "as_of",
    "timezone",
    "raw_response_sha256",
    "field_units",
    "evidence_class_hint",
    "data_quality_status",
    "error_type",
    "result_status",
    "record_count",
    "records",
    "from_cache",
}


def fixture(body: object, *, fetched_at: str = "2026-08-01T08:00:00Z") -> dict[str, object]:
    return {
        "status": 200,
        "headers": {"content-type": "application/json; charset=utf-8"},
        "body": body,
        "fetched_at": fetched_at,
    }


def quote_body(
    code: str,
    *,
    timestamp: str = "20260720093000",
    price: str = "10.20",
    previous_close: str = "10.00",
    amount: str = "123.45",
) -> str:
    values = [""] * 53
    values[1] = "测试公司"
    values[2] = code
    values[3] = price
    values[4] = previous_close
    values[5] = "10.05"
    values[30] = timestamp
    values[31] = "0.20"
    values[32] = "2.00"
    values[33] = "10.50"
    values[34] = "9.90"
    values[37] = amount
    values[38] = "1.23"
    values[39] = "15.60"
    values[44] = "98.70"
    values[45] = "123.40"
    values[46] = "1.80"
    values[47] = "11.00"
    values[48] = "9.00"
    values[52] = "16.20"
    return f'v_{code}="{"~".join(values)}";'


def tree_state(path: Path) -> list[tuple[str, int, int]]:
    return [
        (item.relative_to(path).as_posix(), item.stat().st_size, item.stat().st_mtime_ns)
        for item in sorted(path.rglob("*"))
        if item.is_file()
    ]


class RecordingFixtureTransport(FixtureTransport):
    def __init__(self, fixtures: dict[str, object]):
        super().__init__(fixtures)
        self.requests: list[dict[str, object]] = []

    def request(self, method: str, url: str, **kwargs: object) -> HttpResponse:
        self.requests.append({"method": method, "url": url, **kwargs})
        return super().request(method, url, **kwargs)


class ResearchDataContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.network_guard = patch(
            "urllib.request.urlopen",
            side_effect=AssertionError("offline contract test attempted network access"),
        )
        self.write_guard = patch(
            "pathlib.Path.write_text",
            side_effect=AssertionError("research-data contract test attempted a file write"),
        )
        self.network_guard.start()
        self.write_guard.start()

    def tearDown(self) -> None:
        self.write_guard.stop()
        self.network_guard.stop()

    def assert_envelope(self, result: dict[str, object]) -> None:
        self.assertTrue(ENVELOPE_FIELDS.issubset(result))
        self.assertEqual(result["canonical_ticker"], "SZSE:002135")
        self.assertEqual(result["timezone"], "Asia/Shanghai")
        self.assertIn(result["result_status"], {"ok", "empty", "error"})
        self.assertIn(
            result["data_quality_status"],
            {"complete", "degraded", "disputed", "unavailable"},
        )

    def test_exchange_prefixed_ticker_is_canonical_and_conflicts_fail_closed(self) -> None:
        security = SecurityId.parse("szse:002135")
        self.assertEqual(security.canonical, "SZSE:002135")
        self.assertEqual(security.tencent, "sz002135")
        bjse = SecurityId.parse("BJSE:920982")
        self.assertEqual(bjse.tencent, "bj920982")
        self.assertEqual(bjse.eastmoney_secid, "0.920982")
        self.assertEqual(bjse.sina, "bj920982")
        self.assertFalse(bjse.legacy_bjse)
        legacy = SecurityId.parse("BJSE:830799")
        self.assertEqual(legacy.code, "830799")
        self.assertTrue(legacy.legacy_bjse)
        for ticker in ("002135", "NYSE:002135", "SSE:002135", "SZSE:600519"):
            with self.subTest(ticker=ticker), self.assertRaises(ValueError):
                SecurityId.parse(ticker)

    def test_d1_quote_preserves_units_valuation_fields_and_stale_gate(self) -> None:
        result = ResearchDataClient(
            FixtureTransport({"quote": fixture(quote_body("002135"))})
        ).quote("SZSE:002135", max_age_hours=0.01)

        self.assert_envelope(result)
        self.assertEqual(result["result_status"], "ok")
        record = result["records"][0]
        self.assertEqual(record["price"], 10.2)
        self.assertEqual(record["pe_ttm"], 15.6)
        self.assertEqual(record["pe_static"], 16.2)
        self.assertEqual(record["pb"], 1.8)
        self.assertEqual(record["float_market_cap_100m_cny"], 98.7)
        self.assertEqual(record["total_market_cap_100m_cny"], 123.4)
        self.assertTrue(record["is_stale"])
        self.assertIn("older", record["stale_reason"])
        self.assertTrue(record["official_recheck_required"])
        self.assertEqual(result["field_units"]["price"], "CNY/share")
        self.assertEqual(
            result["field_units"]["total_market_cap_100m_cny"], "100m CNY"
        )

    def test_d1_missing_price_fails_closed_and_future_clock_is_stale(self) -> None:
        missing_price = ResearchDataClient(
            FixtureTransport({"quote": fixture(quote_body("002135", price=""))})
        ).quote("SZSE:002135")
        future_quote = ResearchDataClient(
            FixtureTransport(
                {
                    "quote": fixture(
                        quote_body("002135", timestamp="20990101000000")
                    )
                }
            )
        ).quote("SZSE:002135")

        self.assertEqual(missing_price["result_status"], "error")
        self.assertEqual(missing_price["error_type"], "schema_error")
        self.assertEqual(future_quote["result_status"], "ok")
        record = future_quote["records"][0]
        self.assertTrue(record["is_stale"])
        self.assertGreater(record["future_clock_skew_seconds"], 300)
        self.assertIn("future", record["stale_reason"])
        self.assertTrue(record["official_recheck_required"])

    def test_nonpositive_pagination_is_error_without_provider_request(self) -> None:
        cases = (
            ("announcements", lambda client: client.announcements("SZSE:002135", max_pages=0)),
            ("lockups", lambda client: client.lockups("SZSE:002135", page_size=0)),
            ("ir", lambda client: client.ir("SZSE:002135", max_pages=-1)),
            ("news", lambda client: client.news("SZSE:002135", page_size=False)),
        )
        for name, invoke in cases:
            with self.subTest(adapter=name):
                transport = FixtureTransport({})
                result = invoke(ResearchDataClient(transport))
                self.assertEqual(result["result_status"], "error")
                self.assertEqual(result["error_type"], "invalid_request")
                self.assertEqual(result["record_count"], 0)
                self.assertEqual(transport.calls, [])

    def test_missing_fixture_is_a_structured_error_not_an_empty_result(self) -> None:
        result = ResearchDataClient(FixtureTransport({})).quote("SZSE:002135")

        self.assert_envelope(result)
        self.assertEqual(result["result_status"], "error")
        self.assertEqual(result["error_type"], "fixture_missing")
        self.assertEqual(result["record_count"], 0)
        self.assertEqual(result["data_quality_status"], "unavailable")

    def test_cache_uses_unique_atomic_temp_and_reuses_valid_response(self) -> None:
        class InnerTransport:
            calls = 0

            def request(self, method: str, url: str, **kwargs: object) -> HttpResponse:
                del method, kwargs
                self.calls += 1
                return HttpResponse(
                    status=200,
                    headers={},
                    body=quote_body("002135").encode(),
                    url=url,
                    fetched_at="2026-08-01T08:00:00Z",
                )

        with tempfile.TemporaryDirectory() as temp_dir:
            cache_dir = Path(temp_dir) / "cache"
            inner = InnerTransport()
            client = ResearchDataClient(CachingTransport(inner, cache_dir, 900))
            first = client.quote("SZSE:002135")
            second = client.quote("SZSE:002135")

            self.assertEqual(inner.calls, 1)
            self.assertFalse(first["from_cache"])
            self.assertTrue(second["from_cache"])
            self.assertEqual(len(list(cache_dir.glob("*.json"))), 1)
            self.assertEqual(list(cache_dir.glob("*.tmp")), [])

    def test_official_empty_announcement_result_remains_empty_not_error(self) -> None:
        transport = FixtureTransport(
            {
                "cninfo_org_map": fixture(
                    {"stockList": [{"code": "002135", "orgId": "990000001"}]}
                ),
                "announcements:1": fixture(
                    {"announcements": [], "totalAnnouncement": 0}
                ),
            }
        )
        result = ResearchDataClient(transport).announcements("SZSE:002135")

        self.assert_envelope(result)
        self.assertEqual(result["result_status"], "empty")
        self.assertIsNone(result["error_type"])
        self.assertEqual(result["record_count"], 0)
        self.assertEqual(result["data_quality_status"], "complete")
        self.assertEqual(
            result["evidence_class_hint"],
            "verified_fact_candidate_from_official_filing",
        )
        self.assertEqual(transport.calls, ["cninfo_org_map", "announcements:1"])

    def test_nonempty_malformed_rows_are_schema_errors_not_empty(self) -> None:
        discovery = ResearchDataClient(
            FixtureTransport(
                {
                    "lockups:1": fixture(
                        {
                            "success": True,
                            "result": {"pages": 1, "data": ["schema-drift"]},
                        }
                    )
                }
            )
        ).lockups("SZSE:002135")
        announcements = ResearchDataClient(
            FixtureTransport(
                {
                    "cninfo_org_map": fixture(
                        {"stockList": [{"code": "002135", "orgId": "org-1"}]}
                    ),
                    "announcements:1": fixture(
                        {
                            "totalAnnouncement": 1,
                            "announcements": [
                                {
                                    "announcementId": "a-1",
                                    "announcementTitle": "",
                                    "announcementTime": "2026-07-20",
                                }
                            ],
                        }
                    ),
                }
            )
        ).announcements("SZSE:002135")
        ir = ResearchDataClient(
            FixtureTransport(
                {
                    "ir:lookup": fixture(
                        {"data": [{"stockCode": "002135", "secid": "org-1"}]}
                    ),
                    "ir:1": fixture(
                        {
                            "rows": [
                                {
                                    "stockCode": "999999",
                                    "questionId": "q-1",
                                    "mainContent": "question",
                                    "pubDate": "2026-07-20",
                                }
                            ]
                        }
                    ),
                }
            )
        ).ir("SZSE:002135")
        news_body = (
            'researchDataCallback({"result":{"cmsArticleWebOld":'
            '["schema-drift"]}})'
        )
        news = ResearchDataClient(
            FixtureTransport({"news:1": fixture(news_body)})
        ).news("SZSE:002135")

        for name, result in (
            ("discovery", discovery),
            ("announcements", announcements),
            ("ir", ir),
            ("news", news),
        ):
            with self.subTest(adapter=name):
                self.assertEqual(result["result_status"], "error")
                self.assertEqual(result["error_type"], "schema_error")
                self.assertEqual(result["record_count"], 0)

    def test_d2_discovery_record_requires_official_recheck(self) -> None:
        transport = FixtureTransport(
            {
                "lockups:1": fixture(
                    {
                        "success": True,
                        "result": {
                            "pages": 1,
                            "data": [
                                {
                                    "SECURITY_CODE": "002135",
                                    "FREE_DATE": "2026-07-20",
                                    "FREE_SHARES_TYPE": "首发限售股份",
                                    "FREE_SHARES": 1_000_000,
                                    "ABLE_FREE_SHARES": 900_000,
                                    "FREE_RATIO": 0.01,
                                }
                            ],
                        },
                    }
                )
            }
        )
        result = ResearchDataClient(transport).lockups("SZSE:002135")

        self.assert_envelope(result)
        self.assertEqual(result["result_status"], "ok")
        self.assertEqual(result["data_quality_status"], "degraded")
        self.assertEqual(
            result["evidence_class_hint"],
            "third_party_discovery_requires_official_recheck",
        )
        self.assertTrue(result["records"][0]["official_recheck_required"])

    def test_pagination_limit_is_error_with_partial_records_not_empty(self) -> None:
        transport = FixtureTransport(
            {
                "cninfo_org_map": fixture(
                    {"stockList": [{"code": "002135", "orgId": "990000001"}]}
                ),
                "announcements:1": fixture(
                    {
                        "totalAnnouncement": 2,
                        "announcements": [
                            {
                                "announcementId": "a-1",
                                "announcementTitle": "重大事项公告",
                                "announcementTypeName": "其他",
                                "announcementTime": "2026-07-20",
                                "adjunctUrl": "finalpage/fixture.pdf",
                            }
                        ],
                    }
                ),
            }
        )
        result = ResearchDataClient(transport).announcements(
            "SZSE:002135", page_size=1, max_pages=1
        )

        self.assert_envelope(result)
        self.assertEqual(result["result_status"], "error")
        self.assertEqual(result["error_type"], "pagination_limit")
        self.assertEqual(result["record_count"], 1)
        self.assertEqual(result["data_quality_status"], "degraded")
        self.assertEqual(result["as_of"], "2026-07-20")

    def test_partial_schema_error_preserves_record_as_of(self) -> None:
        result = ResearchDataClient(
            FixtureTransport(
                {
                    "cninfo_org_map": fixture(
                        {"stockList": [{"code": "002135", "orgId": "org-1"}]}
                    ),
                    "announcements:1": fixture(
                        {
                            "totalAnnouncement": 2,
                            "announcements": [
                                {
                                    "announcementId": "a-1",
                                    "announcementTitle": "第一条公告",
                                    "announcementTime": "2026-07-20",
                                }
                            ],
                        }
                    ),
                    "announcements:2": fixture(
                        {
                            "totalAnnouncement": 2,
                            "announcements": ["schema-drift"],
                        }
                    ),
                }
            )
        ).announcements("SZSE:002135", page_size=1, max_pages=2)

        self.assertEqual(result["result_status"], "error")
        self.assertEqual(result["error_type"], "schema_error")
        self.assertEqual(result["record_count"], 1)
        self.assertEqual(result["as_of"], "2026-07-20")

    def test_d3_keeps_official_filing_primary_and_consensus_coverage_dated(self) -> None:
        official_transport = FixtureTransport(
            {
                "cninfo_org_map": fixture(
                    {"stockList": [{"code": "002135", "orgId": "990000001"}]}
                ),
                "announcements:1": fixture(
                    {
                        "totalAnnouncement": 1,
                        "announcements": [
                            {
                                "announcementId": "annual-2025",
                                "announcementTitle": "2025年年度报告",
                                "announcementTypeName": "年度报告",
                                "announcementTime": "2026-04-28",
                                "adjunctUrl": "finalpage/annual-2025.pdf",
                            }
                        ],
                    }
                ),
            }
        )
        filing = ResearchDataClient(official_transport).financial_filings(
            "SZSE:002135"
        )
        consensus_html = """
        <html><body><table>
          <tr><th>年度</th><th>EPS均值</th><th>预测机构数</th><th>更新时间</th></tr>
          <tr><td>2027</td><td>1.23</td><td>2</td><td>2026-07-31</td></tr>
        </table></body></html>
        """
        consensus = ResearchDataClient(
            FixtureTransport(
                {
                    "consensus": fixture(
                        consensus_html, fetched_at="2026-08-01T08:00:00Z"
                    )
                }
            )
        ).consensus("SZSE:002135")

        self.assertEqual(filing["result_status"], "ok")
        self.assertEqual(filing["provider"], "CNINFO")
        self.assertTrue(filing["records"][0]["primary_source"])
        self.assertTrue(filing["records"][0]["official_document_must_be_read"])
        self.assertIn("official", filing["evidence_class_hint"])
        self.assertEqual(consensus["result_status"], "ok")
        self.assertEqual(
            consensus["evidence_class_hint"],
            "market_consensus_with_coverage_caveat",
        )
        self.assertEqual(consensus["as_of"], "2026-07-31")
        self.assertEqual(consensus["records"][0]["institution_count"], 2)
        self.assertTrue(consensus["records"][0]["coverage_warning"])
        self.assertEqual(consensus["records"][0]["forecast_year"], "2027")
        self.assertEqual(consensus["records"][0]["update_time"], "2026-07-31")

    def test_consensus_missing_coverage_warns_and_uses_table_update_as_of(self) -> None:
        consensus_html = """
        <table>
          <tr><th>年度</th><th>EPS均值</th><th>预测机构数</th><th>更新时间</th></tr>
          <tr><td>2027E</td><td>1.23</td><td>-</td><td>2025-01-02</td></tr>
        </table>
        """
        result = ResearchDataClient(
            FixtureTransport(
                {
                    "consensus": fixture(
                        consensus_html, fetched_at="2026-08-01T08:00:00Z"
                    )
                }
            )
        ).consensus("SZSE:002135")

        self.assertEqual(result["result_status"], "ok")
        self.assertEqual(result["as_of"], "2025-01-02")
        self.assertIsNone(result["records"][0]["institution_count"])
        self.assertTrue(result["records"][0]["coverage_warning"])

    def test_financial_filings_query_is_narrowed_by_category_and_date(self) -> None:
        transport = RecordingFixtureTransport(
            {
                "cninfo_org_map": fixture(
                    {"stockList": [{"code": "002135", "orgId": "org-1"}]}
                ),
                "announcements:1": fixture(
                    {"announcements": [], "totalAnnouncement": 0}
                ),
            }
        )
        result = ResearchDataClient(transport).financial_filings("SZSE:002135")

        self.assertEqual(result["result_status"], "empty")
        announcement_request = next(
            request
            for request in transport.requests
            if request.get("fixture_key") == "announcements:1"
        )
        form = announcement_request["form"]
        self.assertIn("category_ndbg_szsh", form["category"])
        self.assertIn("category_sjdbg_szsh", form["category"])
        start_date, end_date = form["seDate"].split("~")
        self.assertRegex(start_date, r"^20\d{2}-\d{2}-\d{2}$")
        self.assertRegex(end_date, r"^20\d{2}-\d{2}-\d{2}$")
        self.assertLess(start_date, end_date)

    def test_d4_ir_answers_and_investor_questions_keep_distinct_evidence(self) -> None:
        transport = FixtureTransport(
            {
                "ir:lookup": fixture(
                    {"data": [{"stockCode": "002135", "secid": "990000001"}]}
                ),
                "ir:1": fixture(
                    {
                        "rows": [
                            {
                                "stockCode": "002135",
                                "questionId": "q-1",
                                "companyShortName": "测试公司",
                                "mainContent": "投资者未经核验的问题",
                                "attachedContent": "公司公开回复",
                                "attachedAuthor": "证券部",
                                "pubDate": "2026-07-20 10:00:00",
                                "attachedPubDate": "2026-07-21 11:00:00",
                            }
                        ]
                    }
                ),
            }
        )
        result = ResearchDataClient(transport).ir("SZSE:002135")

        self.assert_envelope(result)
        self.assertEqual(result["result_status"], "ok")
        self.assertEqual(
            result["evidence_class_hint"], "company_statement_for_answers_only"
        )
        record = result["records"][0]
        self.assertEqual(record["question_evidence"], "unverified_investor_question")
        self.assertEqual(record["answer_evidence"], "company_statement")

    def test_complete_d1_to_d4_snapshot_expands_modules_without_canonical_write(self) -> None:
        calls: list[tuple[str, str]] = []

        class StubClient:
            def __getattr__(self, module: str):
                if module not in ALL_MODULES:
                    raise AttributeError(module)

                def run(ticker: str) -> dict[str, object]:
                    calls.append((module, ticker))
                    return {"endpoint": module, "result_status": "empty"}

                return run

        snapshot = build_snapshot(StubClient(), "SZSE:002135", "d1,d2,d3,d4")

        self.assertEqual(snapshot["modules"], list(ALL_MODULES))
        self.assertEqual(list(snapshot["results"]), list(ALL_MODULES))
        self.assertEqual(calls, [(module, "SZSE:002135") for module in ALL_MODULES])
        self.assertFalse(snapshot["canonical_wiki_written"])

    def test_fixture_cli_writes_only_to_explicit_temp_output(self) -> None:
        raw_before = tree_state(REPO_ROOT / "raw")
        wiki_before = tree_state(REPO_ROOT / "wiki")
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fixture_path = root / "fixture.json"
            output_dir = root / "output"
            cache_dir = root / "cache"
            with fixture_path.open("w", encoding="utf-8") as handle:
                json.dump(
                    {"responses": {"quote": fixture(quote_body("002135"))}},
                    handle,
                    ensure_ascii=False,
                )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "research_snapshot.py"),
                    "--ticker",
                    "SZSE:002135",
                    "--modules",
                    "d1",
                    "--fixture",
                    str(fixture_path),
                    "--format",
                    "json",
                    "--output-dir",
                    str(output_dir),
                    "--cache-dir",
                    str(cache_dir),
                ],
                check=True,
                capture_output=True,
                text=True,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
            summary = json.loads(completed.stdout)
            self.assertFalse(summary["canonical_wiki_written"])
            self.assertEqual(summary["modules"], ["quote"])
            self.assertEqual(len(summary["written"]), 1)
            self.assertTrue(
                Path(summary["written"][0]).is_relative_to(output_dir.resolve())
            )
            self.assertEqual(list(output_dir.rglob("*.tmp")), [])
            self.assertFalse(cache_dir.exists())

        self.assertEqual(tree_state(REPO_ROOT / "raw"), raw_before)
        self.assertEqual(tree_state(REPO_ROOT / "wiki"), wiki_before)

    def test_cli_rejects_output_or_cache_under_raw_and_wiki(self) -> None:
        raw_before = tree_state(REPO_ROOT / "raw")
        wiki_before = tree_state(REPO_ROOT / "wiki")
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fixture_path = root / "fixture.json"
            with fixture_path.open("w", encoding="utf-8") as handle:
                json.dump(
                    {"responses": {"quote": fixture(quote_body("002135"))}},
                    handle,
                    ensure_ascii=False,
                )
            commands = (
                (
                    REPO_ROOT / "raw" / "forbidden-research-output",
                    root / "cache",
                ),
                (
                    root / "output",
                    REPO_ROOT / "wiki" / "forbidden-research-cache",
                ),
            )
            for output_dir, cache_dir in commands:
                with self.subTest(output=output_dir, cache=cache_dir):
                    completed = subprocess.run(
                        [
                            sys.executable,
                            str(SCRIPTS / "research_snapshot.py"),
                            "--ticker",
                            "SZSE:002135",
                            "--modules",
                            "d1",
                            "--fixture",
                            str(fixture_path),
                            "--format",
                            "json",
                            "--output-dir",
                            str(output_dir),
                            "--cache-dir",
                            str(cache_dir),
                        ],
                        check=False,
                        capture_output=True,
                        text=True,
                        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                    )
                    self.assertEqual(completed.returncode, 2)
                    self.assertIn("must not point to raw/ or wiki/", completed.stderr)

        self.assertEqual(tree_state(REPO_ROOT / "raw"), raw_before)
        self.assertEqual(tree_state(REPO_ROOT / "wiki"), wiki_before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
