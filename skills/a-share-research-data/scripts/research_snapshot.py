#!/usr/bin/env python3
"""CLI for a read-only A-share research-data snapshot."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from research_data import (
    CachingTransport,
    FixtureTransport,
    ResearchDataClient,
    SecurityId,
    UrllibTransport,
    build_snapshot,
)


def _vault_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _atomic_write(path: Path, content: str) -> None:
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
            os.fsync(stream.fileno())
            temporary_path = Path(stream.name)
        temporary_path.replace(path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _validate_noncanonical_paths(output_dir: Path, cache_dir: Path) -> None:
    vault_root = _vault_root().resolve()
    forbidden = ((vault_root / "raw").resolve(), (vault_root / "wiki").resolve())
    for label, candidate in (("output-dir", output_dir), ("cache-dir", cache_dir)):
        resolved = candidate.expanduser().resolve()
        if any(_is_within(resolved, parent) for parent in forbidden):
            raise ValueError(
                f"--{label} must not point to raw/ or wiki/: {resolved}"
            )


def _markdown(snapshot: Mapping[str, Any]) -> str:
    lines = [
        f"# A 股研究数据快照：{snapshot['canonical_ticker']}",
        "",
        f"- generated_at: `{snapshot['generated_at']}`",
        f"- timezone: `{snapshot['timezone']}`",
        f"- modules: `{', '.join(snapshot['modules'])}`",
        "- Canonical Wiki 写入：否",
        "",
        "> 第三方结果仅作发现或交叉检查；重大事项须回查交易所或公司正式披露。",
        "",
    ]
    for name, result in snapshot["results"].items():
        lines.extend(
            [
                f"## {name}",
                "",
                f"- status: `{result['result_status']}`",
                f"- data_quality_status: `{result['data_quality_status']}`",
                f"- provider: `{result['provider']}`",
                f"- as_of: `{result.get('as_of') or 'unknown'}`",
                f"- records: `{result['record_count']}`",
                f"- evidence_class_hint: `{result['evidence_class_hint']}`",
                f"- source: {result['source_url']}",
            ]
        )
        if result.get("error_type"):
            lines.extend(
                [
                    f"- error_type: `{result['error_type']}`",
                    f"- error: {result.get('error_message') or ''}",
                ]
            )
        for note in result.get("notes", []):
            lines.append(f"- note: {note}")
        lines.append("")
        if result.get("records"):
            lines.extend(["```json", json.dumps(result["records"], ensure_ascii=False, indent=2), "```", ""])
    return "\n".join(lines).rstrip() + "\n"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch a provenance-rich, read-only A-share research snapshot."
    )
    parser.add_argument("--ticker", required=True, help="Canonical ticker such as SSE:600519")
    parser.add_argument(
        "--modules",
        default="d1,d2,d3,d4",
        help="Comma-separated d1,d2,d3,d4, all, or granular module names",
    )
    parser.add_argument(
        "--fixture",
        type=Path,
        help="Offline fixture JSON. When supplied, no network transport is created.",
    )
    parser.add_argument(
        "--format", choices=("json", "markdown", "both"), default="both"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=_vault_root() / "output" / "a-share-research-data",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=_vault_root() / ".work" / "a-share-research-data",
    )
    parser.add_argument("--cache-ttl-seconds", type=int, default=900)
    parser.add_argument(
        "--print-json", action="store_true", help="Also print the complete snapshot to stdout"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        security = SecurityId.parse(args.ticker)
        _validate_noncanonical_paths(args.output_dir, args.cache_dir)
        if args.fixture:
            transport = FixtureTransport.from_file(args.fixture)
        else:
            transport = CachingTransport(
                UrllibTransport(), args.cache_dir, ttl_seconds=args.cache_ttl_seconds
            )
        snapshot = build_snapshot(
            ResearchDataClient(transport=transport), security.canonical, args.modules
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    stem = f"{security.exchange.lower()}-{security.code}-{stamp}"
    written: list[Path] = []
    if args.format in {"json", "both"}:
        path = args.output_dir / f"{stem}.json"
        _atomic_write(path, json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
        written.append(path)
    if args.format in {"markdown", "both"}:
        path = args.output_dir / f"{stem}.md"
        _atomic_write(path, _markdown(snapshot))
        written.append(path)

    summary = {
        "canonical_ticker": security.canonical,
        "modules": snapshot["modules"],
        "written": [path.resolve().as_posix() for path in written],
        "errors": {
            name: result["error_type"]
            for name, result in snapshot["results"].items()
            if result["result_status"] == "error"
        },
        "canonical_wiki_written": False,
    }
    print(json.dumps(snapshot if args.print_json else summary, ensure_ascii=False, indent=2))
    return 2 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
