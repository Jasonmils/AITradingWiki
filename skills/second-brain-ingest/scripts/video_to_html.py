#!/usr/bin/env python3
"""Bridge one immutable raw MP4 through Video2Skill_Invest into ingestible HTML."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


class BridgeError(RuntimeError):
    pass


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _slug(value: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z\u3400-\u9fff._-]+", "-", value)
    return cleaned.strip("-._")[:120] or "video"


def _inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _read_env_names(path: Path) -> set[str]:
    names: set[str] = set()
    if not path.is_file():
        return names
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        name, separator, value = line.partition("=")
        if separator and name.strip() and value.strip().strip("'\""):
            names.add(name.strip())
    return names


def _git_revision(tool_root: Path) -> str:
    try:
        revision = subprocess.run(
            ["git", "-C", str(tool_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        status = subprocess.run(
            ["git", "-C", str(tool_root), "status", "--porcelain"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    value = revision.stdout.strip() or "unknown"
    return value + ("-dirty" if status.stdout.strip() else "")


def _extract_result(payload: Any) -> dict[str, Any]:
    if isinstance(payload, list):
        if len(payload) != 1 or not isinstance(payload[0], dict):
            raise BridgeError("Video2Skill returned an unexpected batch result")
        return payload[0]
    if not isinstance(payload, dict):
        raise BridgeError("Video2Skill returned an unexpected JSON result")
    return payload


def _decode_json_result(stdout: str) -> Any:
    """Decode a JSON result while tolerating library notices before it."""
    stripped = stdout.strip()
    try:
        return json.loads(stripped)
    except json.JSONDecodeError as direct_error:
        decoder = json.JSONDecoder()
        for index, character in enumerate(stdout):
            if character not in "[{":
                continue
            try:
                payload, end = decoder.raw_decode(stdout[index:])
            except json.JSONDecodeError:
                continue
            if stdout[index + end :].strip():
                continue
            return payload
        raise direct_error


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run Video2Skill_Invest for one immutable raw MP4 and return the "
            "DeepSeek-refined HTML path for second-brain ingestion."
        )
    )
    parser.add_argument("video", help="MP4 under <vault>/raw/")
    parser.add_argument("--vault-root", default=".")
    parser.add_argument(
        "--video2skill-root",
        help="Video2Skill_Invest checkout; defaults to VIDEO2SKILL_ROOT or .work/tools/",
    )
    parser.add_argument(
        "--env-file",
        help="Local secrets file; defaults to <vault>/.env.video-ingest.local",
    )
    parser.add_argument(
        "--accelerated",
        action="store_true",
        help="Use the upstream Apple Silicon accelerated configuration",
    )
    parser.add_argument(
        "--allow-remote-processing",
        action="store_true",
        help="Acknowledge that transcript and PPT OCR text may be sent to DeepSeek",
    )
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Validate paths, checkout, environment and secrets without processing",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    vault = Path(args.vault_root).expanduser().resolve()
    video = Path(args.video).expanduser().resolve()
    raw_root = (vault / "raw").resolve()
    tool_root = Path(
        args.video2skill_root
        or os.environ.get("VIDEO2SKILL_ROOT", "")
        or vault / ".work" / "tools" / "Video2Skill_Invest"
    ).expanduser().resolve()
    env_file = Path(
        args.env_file or vault / ".env.video-ingest.local"
    ).expanduser().resolve()

    if not vault.is_dir():
        raise BridgeError(f"vault root does not exist: {vault}")
    if not video.is_file():
        raise BridgeError(f"video does not exist: {video}")
    if video.suffix.lower() != ".mp4":
        raise BridgeError("video ingest currently accepts MP4 files only")
    if not _inside(video, raw_root):
        raise BridgeError(f"video must remain under the vault raw directory: {raw_root}")
    if not (tool_root / "src" / "invest_lecture_digest" / "cli.py").is_file():
        raise BridgeError(
            "Video2Skill_Invest is not installed at "
            f"{tool_root}; run scripts/setup_video2skill.sh first"
        )

    python = tool_root / ".venv" / "bin" / "python"
    if not python.is_file():
        raise BridgeError(
            f"Video2Skill Python environment is missing: {python}; "
            "run scripts/setup_video2skill.sh"
        )
    config_name = (
        "lecture.production.macos.accelerated.json"
        if args.accelerated
        else "lecture.production.macos.json"
    )
    config = tool_root / "configs" / config_name
    refinement = tool_root / "configs" / "transcript.refinement.json"
    for required in (config, refinement):
        if not required.is_file():
            raise BridgeError(f"required Video2Skill config is missing: {required}")

    available_keys = _read_env_names(env_file)
    missing_keys = sorted({"HF_TOKEN", "DEEPSEEK_API_KEY"} - available_keys)
    if missing_keys:
        raise BridgeError(
            f"fill {', '.join(missing_keys)} in {env_file}; values are never printed"
        )
    if not args.preflight_only and not args.allow_remote_processing:
        raise BridgeError(
            "remote processing is not approved; DeepSeek receives transcript and "
            "relevant PPT OCR text. Re-run with --allow-remote-processing only "
            "after the curator explicitly approves this transfer."
        )

    output_root = vault / "output" / "video-ingest"
    preflight = {
        "status": "ready",
        "source_video": video.as_posix(),
        "source_sha256": _sha256(video),
        "video2skill_root": tool_root.as_posix(),
        "video2skill_revision": _git_revision(tool_root),
        "pipeline_config": config.as_posix(),
        "refinement_config": refinement.as_posix(),
        "env_file": env_file.as_posix(),
        "remote_payload": "transcript text and relevant PPT OCR text",
        "raw_video_modified": False,
    }
    if args.preflight_only:
        print(json.dumps(preflight, ensure_ascii=False, indent=2))
        return 0

    command = [
        str(python),
        "-m",
        "invest_lecture_digest",
        "production-run",
        str(video),
        "-c",
        str(config),
        "--root",
        str(output_root / "production"),
        "--report-dir",
        str(output_root / "reports"),
        "--result-dir",
        str(output_root / "results"),
        "--refinement-config",
        str(refinement),
        "--until",
        "render",
        "--quiet",
        "--json",
    ]
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(tool_root / "src")
    environment["INVEST_DIGEST_ENV_FILE"] = str(env_file)
    completed = subprocess.run(
        command,
        cwd=tool_root,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise BridgeError(
            f"Video2Skill failed with exit code {completed.returncode}: {detail}"
        )
    try:
        result = _extract_result(_decode_json_result(completed.stdout))
    except json.JSONDecodeError as exc:
        raise BridgeError(
            "Video2Skill did not return valid JSON: " + completed.stdout[-1000:]
        ) from exc

    artifacts = result.get("artifacts")
    if not isinstance(artifacts, dict):
        raise BridgeError("Video2Skill result has no artifact map")
    final_raw = artifacts.get("timeline_deepseek_html")
    original_raw = artifacts.get("timeline_html")
    timeline_raw = artifacts.get("timeline_json")
    if not all(isinstance(value, str) for value in (final_raw, original_raw, timeline_raw)):
        raise BridgeError(
            "Video2Skill did not produce timeline.json, timeline.html and "
            "timeline.deepseek.html; Wiki ingest has not started"
        )
    final_html = Path(final_raw).expanduser().resolve()
    original_html = Path(original_raw).expanduser().resolve()
    timeline_json = Path(timeline_raw).expanduser().resolve()
    for artifact in (final_html, original_html, timeline_json):
        if not artifact.is_file() or artifact.stat().st_size == 0:
            raise BridgeError(f"required Video2Skill artifact is unavailable: {artifact}")
    optional_artifacts: dict[str, str] = {}
    for manifest_name, artifact_names in (
        ("performance_json", ("performance_run", "performance")),
        (
            "refinement_prefetch_json",
            ("refinement_prefetch_run", "refinement_prefetch"),
        ),
    ):
        raw_path = next(
            (
                artifacts.get(name)
                for name in artifact_names
                if isinstance(artifacts.get(name), str)
            ),
            None,
        )
        if not isinstance(raw_path, str):
            continue
        candidate = Path(raw_path).expanduser().resolve()
        if candidate.is_file() and candidate.stat().st_size > 0:
            if manifest_name == "refinement_prefetch_json":
                try:
                    prefetch = json.loads(candidate.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError) as exc:
                    raise BridgeError(
                        "refinement prefetch audit is invalid: "
                        f"{candidate}"
                    ) from exc
                if not isinstance(prefetch, dict):
                    raise BridgeError(
                        "refinement prefetch audit is not a JSON object"
                    )
                if (
                    prefetch.get("status") == "completed"
                    and prefetch.get("input_matches_final") is not True
                ):
                    raise BridgeError(
                        "refinement prefetch input does not match the "
                        "authoritative timeline"
                    )
            optional_artifacts[manifest_name] = candidate.as_posix()

    generated_at = datetime.now(timezone.utc).isoformat()
    manifest = {
        **preflight,
        "status": "completed",
        "generated_at": generated_at,
        "authoritative_timeline_json": timeline_json.as_posix(),
        "original_transcript_html": original_html.as_posix(),
        "ingest_input_html": final_html.as_posix(),
        "ingest_input_sha256": _sha256(final_html),
        **optional_artifacts,
        "video2skill_result": {
            key: result.get(key)
            for key in (
                "production_job_id",
                "status",
                "stage",
                "refinement_status",
                "refinement_prefetch_status",
            )
            if key in result
        },
    }
    manifest_path = (
        output_root
        / "manifests"
        / f"{_slug(video.stem)}-{preflight['source_sha256'][:12]}.json"
    )
    _atomic_json(manifest_path, manifest)
    manifest["manifest"] = manifest_path.as_posix()
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BridgeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
