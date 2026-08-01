#!/usr/bin/env python3
"""Safely archive one non-canonical equity-research Markdown report."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import tempfile


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "output" / "equity-research"
TICKER_RE = re.compile(r"^[A-Z][A-Z0-9]{1,15}:[A-Z0-9][A-Z0-9._-]{0,31}$")


def _iso_date(value: str, label: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise ValueError(f"{label} must use YYYY-MM-DD: {value}") from exc


def _utc_timestamp(value: str | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"generated-at must be ISO 8601: {value}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _is_within(candidate: Path, parent: Path) -> bool:
    return candidate == parent or parent in candidate.parents


def _validate_output_dir(output_dir: Path) -> Path:
    resolved = output_dir.expanduser().resolve()
    for forbidden_name in ("raw", "wiki"):
        forbidden = (REPO_ROOT / forbidden_name).resolve()
        if _is_within(resolved, forbidden):
            raise ValueError(
                f"non-canonical report output cannot be under {forbidden_name}/: "
                f"{resolved}"
            )
    return resolved


def _derived_listing_regime(ticker: str) -> str:
    exchange = ticker.split(":", 1)[0]
    if exchange in {"SSE", "SZSE", "BJSE"}:
        return "a_share"
    if exchange in {"NASDAQ", "NYSE", "NYSEARCA", "AMEX"}:
        return "us_equity"
    return "other"


def _yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _frontmatter(
    *,
    ticker: str,
    listing_regime: str,
    as_of: str,
    generated_at: str,
    horizon: str,
    wiki_cutoff: str,
    market_rules_as_of: str,
    report_status: str,
) -> str:
    values = {
        "report_type": "equity_research",
        "canonical": False,
        "ticker": ticker,
        "listing_regime": listing_regime,
        "as_of": as_of,
        "generated_at": generated_at,
        "horizon": horizon,
        "wiki_cutoff": wiki_cutoff,
        "market_rules_as_of": market_rules_as_of,
        "report_status": report_status,
        "canonical_write_status_at_generation": "pending_approval",
    }
    lines = ["---"]
    for key, value in values.items():
        rendered = "false" if value is False else _yaml_string(value)
        lines.append(f"{key}: {rendered}")
    lines.extend(["---", ""])
    return "\n".join(lines)


def _safe_slug(ticker: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", ticker.lower()).strip("-")


def _atomic_unique_write(output_dir: Path, stem: str, content: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        dir=output_dir, prefix=f".{stem}-", suffix=".tmp"
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())

        suffix = 1
        while True:
            filename = f"{stem}.md" if suffix == 1 else f"{stem}-{suffix}.md"
            destination = output_dir / filename
            try:
                os.link(temporary_path, destination)
                break
            except FileExistsError:
                suffix += 1
        temporary_path.unlink()
        return destination
    finally:
        temporary_path.unlink(missing_ok=True)


def save_report(
    *,
    body: str,
    ticker: str,
    as_of: str,
    listing_regime: str | None = None,
    horizon: str = "",
    wiki_cutoff: str = "",
    market_rules_as_of: str = "",
    report_status: str = "partial",
    title: str | None = None,
    generated_at: str | None = None,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> Path:
    ticker = ticker.strip().upper()
    if not TICKER_RE.fullmatch(ticker):
        raise ValueError(f"ticker must be exchange-prefixed and canonical: {ticker}")

    body = body.strip()
    if not body:
        raise ValueError("report body is empty")
    if body.startswith("---"):
        raise ValueError("report body must not contain YAML frontmatter")

    as_of = _iso_date(as_of, "as-of")
    if wiki_cutoff:
        wiki_cutoff = _iso_date(wiki_cutoff, "wiki-cutoff")
    if market_rules_as_of:
        market_rules_as_of = _iso_date(
            market_rules_as_of, "market-rules-as-of"
        )
    if report_status not in {"complete", "partial", "blocked"}:
        raise ValueError("report-status must be complete, partial, or blocked")

    run_time = _utc_timestamp(generated_at)
    generated_at_value = run_time.replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )
    regime = listing_regime or _derived_listing_regime(ticker)
    if regime not in {"a_share", "us_equity", "cross_market", "other"}:
        raise ValueError(
            "listing-regime must be a_share, us_equity, cross_market, or other"
        )

    report_title = title.strip() if title else f"股票研究报告 — {ticker}"
    content = _frontmatter(
        ticker=ticker,
        listing_regime=regime,
        as_of=as_of,
        generated_at=generated_at_value,
        horizon=horizon,
        wiki_cutoff=wiki_cutoff,
        market_rules_as_of=market_rules_as_of,
        report_status=report_status,
    )
    content += f"# {report_title}\n\n{body}\n"

    output_dir = _validate_output_dir(output_dir)
    run_id = run_time.strftime("%Y%m%dT%H%M%SZ")
    stem = f"{_safe_slug(ticker)}-{as_of}-{run_id}"
    return _atomic_unique_write(output_dir, stem, content)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--as-of", required=True)
    parser.add_argument(
        "--listing-regime",
        choices=("a_share", "us_equity", "cross_market", "other"),
    )
    parser.add_argument("--horizon", default="")
    parser.add_argument("--wiki-cutoff", default="")
    parser.add_argument("--market-rules-as-of", default="")
    parser.add_argument(
        "--report-status",
        choices=("complete", "partial", "blocked"),
        default="partial",
    )
    parser.add_argument("--title")
    parser.add_argument("--generated-at", help=argparse.SUPPRESS)
    parser.add_argument("--body-file", required=True, help="Markdown body or - for stdin")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.body_file == "-":
            body = sys.stdin.read()
        else:
            body = Path(args.body_file).expanduser().read_text(encoding="utf-8")
        path = save_report(
            body=body,
            ticker=args.ticker,
            as_of=args.as_of,
            listing_regime=args.listing_regime,
            horizon=args.horizon,
            wiki_cutoff=args.wiki_cutoff,
            market_rules_as_of=args.market_rules_as_of,
            report_status=args.report_status,
            title=args.title,
            generated_at=args.generated_at,
            output_dir=args.output_dir,
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(path.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
