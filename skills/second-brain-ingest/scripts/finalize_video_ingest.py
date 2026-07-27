#!/usr/bin/env python3
"""Finalize a confirmed video ingest and reclaim local media storage."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
from typing import Any


class FinalizeError(RuntimeError):
    pass


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _relative(path: Path, vault: Path) -> str:
    try:
        return path.relative_to(vault).as_posix()
    except ValueError as exc:
        raise FinalizeError(f"path is outside the vault: {path}") from exc


def _load_manifest(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FinalizeError(f"cannot read manifest {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise FinalizeError(f"manifest must contain a JSON object: {path}")
    return payload


def _atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    _atomic_text(
        path,
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
    )


def _tree_size(path: Path) -> int:
    if not path.exists():
        return 0
    if path.is_file():
        return path.stat().st_size
    total = 0
    for candidate in path.rglob("*"):
        if candidate.is_file():
            total += candidate.stat().st_size
    return total


def _copy_verified(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if not destination.is_file() or _sha256(destination) != _sha256(source):
            raise FinalizeError(
                f"refusing to overwrite a different retained transcript: {destination}"
            )
        return
    shutil.copy2(source, destination)
    if destination.stat().st_size == 0 or _sha256(destination) != _sha256(source):
        raise FinalizeError(f"retained transcript verification failed: {destination}")


def _remove_tree_resilient(path: Path, parent: Path) -> None:
    if not _inside(path, parent) or path == parent:
        raise FinalizeError(f"refusing unsafe production job deletion: {path}")
    for _attempt in range(5):
        if not path.exists():
            return
        try:
            shutil.rmtree(path)
        except OSError:
            if not path.exists():
                return
            remaining = sorted(
                path.rglob("*"),
                key=lambda candidate: len(candidate.parts),
                reverse=True,
            )
            if any(
                candidate.is_file() and candidate.name != ".DS_Store"
                for candidate in remaining
            ):
                raise
            for candidate in remaining:
                try:
                    if candidate.is_file() or candidate.is_symlink():
                        candidate.unlink()
                    elif candidate.is_dir():
                        candidate.rmdir()
                except FileNotFoundError:
                    continue
                except OSError:
                    pass
            try:
                path.rmdir()
            except FileNotFoundError:
                return
            except OSError:
                continue
        else:
            return
    raise FinalizeError(
        f"production job could not be removed after bounded retries: {path}"
    )


def _frontmatter_scalar(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*[\"']?([^\"'\n]+)", text)
    return match.group(1).strip() if match else None


def _upsert_frontmatter(text: str, fields: dict[str, str]) -> str:
    if not text.startswith("---\n"):
        raise FinalizeError("Source page has no YAML frontmatter")
    closing = text.find("\n---\n", 4)
    if closing < 0:
        raise FinalizeError("Source page has malformed YAML frontmatter")
    frontmatter = text[4:closing]
    for key, value in fields.items():
        rendered = f"{key}: {json.dumps(value, ensure_ascii=False)}"
        pattern = re.compile(rf"(?m)^{re.escape(key)}:.*$")
        if pattern.search(frontmatter):
            frontmatter = pattern.sub(rendered, frontmatter, count=1)
        else:
            frontmatter = frontmatter.rstrip() + "\n" + rendered
    return "---\n" + frontmatter + text[closing:]


def _source_title(text: str, fallback: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    return match.group(1).strip() if match else fallback


def _resume_in_progress_cleanup(
    *,
    vault: Path,
    manifest_path: Path,
    source_page: Path,
    log_path: Path,
    manifest: dict[str, Any],
    output_root: Path,
    jobs_root: Path,
) -> int:
    cleanup = manifest.get("cleanup")
    if not isinstance(cleanup, dict) or cleanup.get("status") != "deletion_in_progress":
        raise FinalizeError("manifest has no resumable cleanup receipt")
    source_relative = cleanup.get("deleted_source_video")
    retained = cleanup.get("retained_transcript_html")
    source_page_relative = _relative(source_page, vault)
    if cleanup.get("source_page") != source_page_relative:
        raise FinalizeError("Source page does not match the cleanup receipt")
    if not isinstance(source_relative, str) or not source_relative:
        raise FinalizeError("cleanup receipt has no deleted source path")
    source_video = (vault / source_relative).resolve()
    if source_video.exists():
        raise FinalizeError(
            "cleanup receipt is in progress but the source video still exists; "
            "run a fresh eligibility check"
        )
    if (
        not isinstance(retained, list)
        or len(retained) != 2
        or not all(isinstance(value, str) and value for value in retained)
    ):
        raise FinalizeError("cleanup receipt has no retained transcript pair")
    retained_original = (vault / retained[0]).resolve()
    retained_refined = (vault / retained[1]).resolve()
    transcript_root = (output_root / "transcripts").resolve()
    for transcript in (retained_original, retained_refined):
        if (
            not _inside(transcript, transcript_root)
            or not transcript.is_file()
            or transcript.stat().st_size == 0
        ):
            raise FinalizeError(
                f"cannot resume without the retained transcript: {transcript}"
            )

    purged_job_relative = cleanup.get("purged_production_job")
    job_root: Path | None = None
    if isinstance(purged_job_relative, str) and purged_job_relative:
        job_root = (vault / purged_job_relative).resolve()
        _remove_tree_resilient(job_root, jobs_root)

    source_sha256 = manifest.get("source_sha256")
    timeline_sha256 = cleanup.get("removed_timeline_json_sha256")
    if not isinstance(source_sha256, str) or not source_sha256:
        raise FinalizeError("manifest has no source SHA-256")
    if not isinstance(timeline_sha256, str) or not timeline_sha256:
        raise FinalizeError("cleanup receipt has no removed timeline SHA-256")

    old_original_raw = manifest.get("original_transcript_html")
    old_refined_raw = manifest.get("ingest_input_html")
    if not isinstance(old_original_raw, str) or not isinstance(old_refined_raw, str):
        raise FinalizeError("manifest has no original transcript paths")
    old_original_relative = _relative(Path(old_original_raw).resolve(), vault)
    old_refined_relative = _relative(Path(old_refined_raw).resolve(), vault)
    retained_original_relative = _relative(retained_original, vault)
    retained_refined_relative = _relative(retained_refined, vault)
    manifest_relative = _relative(manifest_path, vault)
    completed_at = datetime.now(timezone.utc)
    completed_at_iso = completed_at.isoformat()

    cleanup["status"] = "completed"
    cleanup["completed_at"] = completed_at_iso
    cleanup["source_video_exists_after_cleanup"] = False
    manifest["status"] = "wiki_ingested_source_deleted"
    manifest["source_video_deleted_after_ingest"] = True
    manifest["source_video_deleted_at"] = completed_at_iso
    manifest["raw_video_modified"] = False
    manifest["original_transcript_html"] = retained_original.as_posix()
    manifest["original_transcript_html_sha256"] = _sha256(retained_original)
    manifest["ingest_input_html"] = retained_refined.as_posix()
    manifest["ingest_input_sha256"] = _sha256(retained_refined)
    if job_root is not None:
        manifest["authoritative_timeline_json"] = None
        manifest["authoritative_timeline_json_removed_sha256"] = timeline_sha256
    _atomic_json(manifest_path, manifest)

    source_text = source_page.read_text(encoding="utf-8")
    source_text = source_text.replace(
        old_original_relative,
        retained_original_relative,
    )
    source_text = source_text.replace(
        old_refined_relative,
        retained_refined_relative,
    )
    source_text = _upsert_frontmatter(
        source_text,
        {
            "updated": completed_at.date().isoformat(),
            "source_file_status": "deleted_after_confirmed_ingest",
            "source_deleted_at": completed_at.date().isoformat(),
            "video_ingest_manifest": manifest_relative,
        },
    )
    if "## 本地存储终态" not in source_text:
        source_text = source_text.rstrip() + (
            "\n\n## 本地存储终态\n\n"
            f"- 原始 MP4：已于 {completed_at.date().isoformat()} 在转录与 Wiki "
            f"摄入确认后删除；原路径为 `{source_relative}`，SHA-256 为 "
            f"`{source_sha256}`。\n"
            f"- 保留原始 ASR/OCR HTML：`{retained_original_relative}`。\n"
            f"- 保留 DeepSeek 精炼 HTML：`{retained_refined_relative}`。\n"
            f"- 结构化时间轴与处理缓存已删除；删除前 `timeline.json` 的 "
            f"SHA-256 为 `{timeline_sha256}`。\n"
            f"- 终态清理记录：`{manifest_relative}`。\n"
        )
    _atomic_text(source_page, source_text)

    log_text = log_path.read_text(encoding="utf-8")
    if not (
        "视频源文件终态清理" in log_text
        and manifest_relative in log_text
    ):
        title = _source_title(source_text, source_page.stem)
        reclaimed_mib = float(cleanup.get("estimated_reclaimable_bytes", 0)) / (
            1024 * 1024
        )
        log_entry = (
            f"\n## {completed_at.date().isoformat()} maintenance | 视频源文件终态清理\n"
            f"在策展人确认完成转录与 Canonical Wiki 摄入后，删除 "
            f"`{source_relative}`，保留原始与 DeepSeek 精炼转录 HTML，并在 "
            f"`{manifest_relative}` 记录源文件 SHA-256 与清理状态。"
            f"同时删除该视频的本地音频、帧、OCR、时间轴及其他处理中间文件。"
            f"关联来源：[[{source_page.stem}|{title}]]；预计释放 "
            f"{reclaimed_mib:.1f} MiB。\n"
        )
        _atomic_text(log_path, log_text.rstrip() + "\n" + log_entry)

    print(
        json.dumps(
            {
                "status": "completed",
                "resumed_from": "deletion_in_progress",
                "source_video": source_relative,
                "source_video_deleted": True,
                "production_job_deleted": (
                    not job_root.exists() if job_root is not None else False
                ),
                "retained_transcript_html": retained,
                "completed_at": completed_at_iso,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Verify that an MP4 has completed transcription and canonical Wiki "
            "ingest, retain the two transcript HTML files, then delete the source "
            "video and, by default, its heavyweight processing intermediates."
        )
    )
    parser.add_argument("manifest", help="Bridge manifest under output/video-ingest/manifests/")
    parser.add_argument("--vault-root", default=".")
    parser.add_argument(
        "--source-page",
        required=True,
        help="Canonical Source page under wiki/sources/ that records this ingest",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--check-only",
        action="store_true",
        help="Validate cleanup eligibility and report reclaimable bytes without deleting",
    )
    mode.add_argument(
        "--confirm-delete-source-video",
        action="store_true",
        help="Confirm deletion after the curator approved canonical Wiki ingestion",
    )
    parser.add_argument(
        "--keep-intermediates",
        action="store_true",
        help="Delete only the source MP4 and preserve the production job directory",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    vault = Path(args.vault_root).expanduser().resolve()
    raw_root = (vault / "raw").resolve()
    output_root = (vault / "output" / "video-ingest").resolve()
    manifest_root = (output_root / "manifests").resolve()
    jobs_root = (output_root / "production" / "jobs").resolve()
    source_root = (vault / "wiki" / "sources").resolve()
    manifest_path = Path(args.manifest).expanduser().resolve()
    source_page = Path(args.source_page).expanduser().resolve()
    log_path = (vault / "wiki" / "log.md").resolve()

    if not vault.is_dir():
        raise FinalizeError(f"vault root does not exist: {vault}")
    if not _inside(manifest_path, manifest_root) or not manifest_path.is_file():
        raise FinalizeError(
            f"manifest must be an existing file under {manifest_root}: {manifest_path}"
        )
    if not _inside(source_page, source_root) or not source_page.is_file():
        raise FinalizeError(
            f"Source page must be an existing file under {source_root}: {source_page}"
        )
    if not log_path.is_file():
        raise FinalizeError(f"Wiki log is missing: {log_path}")

    manifest = _load_manifest(manifest_path)
    cleanup = manifest.get("cleanup")
    if (
        manifest.get("status") == "completed"
        and isinstance(cleanup, dict)
        and cleanup.get("status") == "deletion_in_progress"
    ):
        if not args.confirm_delete_source_video:
            raise FinalizeError(
                "cleanup is already in progress; rerun with "
                "--confirm-delete-source-video to resume from its receipt"
            )
        return _resume_in_progress_cleanup(
            vault=vault,
            manifest_path=manifest_path,
            source_page=source_page,
            log_path=log_path,
            manifest=manifest,
            output_root=output_root,
            jobs_root=jobs_root,
        )
    if (
        manifest.get("status") == "wiki_ingested_source_deleted"
        and isinstance(cleanup, dict)
        and cleanup.get("status") == "completed"
    ):
        print(
            json.dumps(
                {
                    "status": "already_finalized",
                    "manifest": manifest_path.as_posix(),
                    "cleanup": cleanup,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    if manifest.get("status") != "completed":
        raise FinalizeError(
            "manifest status must be completed before Wiki finalization; "
            f"found {manifest.get('status')!r}"
        )

    source_video_raw = manifest.get("source_video")
    source_sha256 = manifest.get("source_sha256")
    original_html_raw = manifest.get("original_transcript_html")
    refined_html_raw = manifest.get("ingest_input_html")
    timeline_json_raw = manifest.get("authoritative_timeline_json")
    if not all(
        isinstance(value, str) and value
        for value in (
            source_video_raw,
            source_sha256,
            original_html_raw,
            refined_html_raw,
            timeline_json_raw,
        )
    ):
        raise FinalizeError("manifest is missing required source or transcript provenance")

    source_video = Path(source_video_raw).expanduser().resolve()
    original_html = Path(original_html_raw).expanduser().resolve()
    refined_html = Path(refined_html_raw).expanduser().resolve()
    timeline_json = Path(timeline_json_raw).expanduser().resolve()
    if (
        source_video.suffix.lower() != ".mp4"
        or not _inside(source_video, raw_root)
        or not source_video.is_file()
    ):
        raise FinalizeError(
            f"source video must be an existing MP4 under {raw_root}: {source_video}"
        )
    if source_video.is_symlink():
        raise FinalizeError(f"refusing a symlinked source video: {source_video}")
    actual_source_sha256 = _sha256(source_video)
    if actual_source_sha256 != source_sha256:
        raise FinalizeError(
            "source video SHA-256 does not match the completed bridge manifest"
        )

    job_result = manifest.get("video2skill_result")
    job_id = (
        job_result.get("production_job_id")
        if isinstance(job_result, dict)
        else None
    )
    if not isinstance(job_id, str) or not job_id or "/" in job_id:
        raise FinalizeError("manifest has no safe production_job_id")
    job_root = (jobs_root / job_id).resolve()
    artifact_dir = (job_root / "output").resolve()
    for artifact, expected_name in (
        (original_html, "timeline.html"),
        (refined_html, "timeline.deepseek.html"),
        (timeline_json, "timeline.json"),
    ):
        if (
            artifact.parent != artifact_dir
            or artifact.name != expected_name
            or not artifact.is_file()
            or artifact.stat().st_size == 0
        ):
            raise FinalizeError(
                f"required job artifact is missing or outside the expected job: {artifact}"
            )

    source_text = source_page.read_text(encoding="utf-8")
    log_text = log_path.read_text(encoding="utf-8")
    source_relative = _relative(source_video, vault)
    original_relative = _relative(original_html, vault)
    refined_relative = _relative(refined_html, vault)
    timeline_relative = _relative(timeline_json, vault)
    manifest_relative = _relative(manifest_path, vault)
    if _frontmatter_scalar(source_text, "page_type") != "source":
        raise FinalizeError(f"canonical page is not page_type=source: {source_page}")
    for required_value, label in (
        (source_sha256, "source SHA-256"),
        (source_relative, "source video path"),
        (refined_relative, "refined transcript path"),
    ):
        if required_value not in source_text:
            raise FinalizeError(f"Source page does not record the {label}: {required_value}")
    if source_relative not in log_text:
        raise FinalizeError(
            f"wiki/log.md has no completed ingest entry for {source_relative}"
        )

    retained_root = (
        output_root
        / "transcripts"
        / f"{source_video.stem}-{source_sha256[:12]}"
    ).resolve()
    if not _inside(retained_root, output_root / "transcripts"):
        raise FinalizeError(f"unsafe retained transcript directory: {retained_root}")
    retained_original = retained_root / "timeline.html"
    retained_refined = retained_root / "timeline.deepseek.html"
    retained_original_relative = _relative(retained_original, vault)
    retained_refined_relative = _relative(retained_refined, vault)
    source_bytes = source_video.stat().st_size
    job_bytes = _tree_size(job_root)
    retained_bytes = original_html.stat().st_size + refined_html.stat().st_size
    reclaimable_bytes = source_bytes
    if not args.keep_intermediates:
        reclaimable_bytes += max(0, job_bytes - retained_bytes)

    eligibility = {
        "status": "eligible",
        "source_video": source_relative,
        "source_sha256": source_sha256,
        "source_page": _relative(source_page, vault),
        "manifest": manifest_relative,
        "retained_transcript_html": [
            retained_original_relative,
            retained_refined_relative,
        ],
        "source_video_bytes": source_bytes,
        "production_job_bytes": job_bytes,
        "estimated_reclaimable_bytes": reclaimable_bytes,
        "purge_intermediates": not args.keep_intermediates,
    }
    if args.check_only:
        print(json.dumps(eligibility, ensure_ascii=False, indent=2))
        return 0

    _copy_verified(original_html, retained_original)
    _copy_verified(refined_html, retained_refined)
    finalized_at = datetime.now(timezone.utc)
    finalized_at_iso = finalized_at.isoformat()
    timeline_sha256 = _sha256(timeline_json)
    original_html_sha256 = _sha256(retained_original)
    refined_html_sha256 = _sha256(retained_refined)
    cleanup_record = {
        "status": "deletion_in_progress",
        "confirmed_at": finalized_at_iso,
        "source_page": _relative(source_page, vault),
        "source_sha256_verified_before_delete": True,
        "deleted_source_video": source_relative,
        "purged_production_job": (
            _relative(job_root, vault) if not args.keep_intermediates else None
        ),
        "retained_transcript_html": [
            retained_original_relative,
            retained_refined_relative,
        ],
        "removed_timeline_json_sha256": (
            timeline_sha256 if not args.keep_intermediates else None
        ),
        "estimated_reclaimable_bytes": reclaimable_bytes,
    }
    manifest["cleanup"] = cleanup_record
    _atomic_json(manifest_path, manifest)

    source_video.unlink()
    if not args.keep_intermediates:
        _remove_tree_resilient(job_root, jobs_root)

    cleanup_record["status"] = "completed"
    cleanup_record["completed_at"] = datetime.now(timezone.utc).isoformat()
    cleanup_record["source_video_exists_after_cleanup"] = source_video.exists()
    manifest["status"] = "wiki_ingested_source_deleted"
    manifest["source_video_deleted_after_ingest"] = True
    manifest["source_video_deleted_at"] = cleanup_record["completed_at"]
    manifest["raw_video_modified"] = False
    manifest["original_transcript_html"] = retained_original.as_posix()
    manifest["original_transcript_html_sha256"] = original_html_sha256
    manifest["ingest_input_html"] = retained_refined.as_posix()
    manifest["ingest_input_sha256"] = refined_html_sha256
    if not args.keep_intermediates:
        manifest["authoritative_timeline_json"] = None
        manifest["authoritative_timeline_json_removed_sha256"] = timeline_sha256
    _atomic_json(manifest_path, manifest)

    source_text = source_text.replace(original_relative, retained_original_relative)
    source_text = source_text.replace(refined_relative, retained_refined_relative)
    source_text = _upsert_frontmatter(
        source_text,
        {
            "updated": finalized_at.date().isoformat(),
            "source_file_status": "deleted_after_confirmed_ingest",
            "source_deleted_at": finalized_at.date().isoformat(),
            "video_ingest_manifest": manifest_relative,
        },
    )
    if "## 本地存储终态" not in source_text:
        source_text = source_text.rstrip() + (
            "\n\n## 本地存储终态\n\n"
            f"- 原始 MP4：已于 {finalized_at.date().isoformat()} 在转录与 Wiki "
            f"摄入确认后删除；原路径为 `{source_relative}`，SHA-256 为 "
            f"`{source_sha256}`。\n"
            f"- 保留原始 ASR/OCR HTML：`{retained_original_relative}`。\n"
            f"- 保留 DeepSeek 精炼 HTML：`{retained_refined_relative}`。\n"
            + (
                f"- 结构化时间轴与处理缓存已删除；删除前 `timeline.json` 的 "
                f"SHA-256 为 `{timeline_sha256}`。\n"
                if not args.keep_intermediates
                else f"- 处理缓存仍保留在 `{_relative(job_root, vault)}`。\n"
            )
            + f"- 终态清理记录：`{manifest_relative}`。\n"
        )
    _atomic_text(source_page, source_text)

    title = _source_title(source_text, source_page.stem)
    reclaimed_mib = reclaimable_bytes / (1024 * 1024)
    log_entry = (
        f"\n## {finalized_at.date().isoformat()} maintenance | 视频源文件终态清理\n"
        f"在策展人确认完成转录与 Canonical Wiki 摄入后，删除 "
        f"`{source_relative}`，保留原始与 DeepSeek 精炼转录 HTML，并在 "
        f"`{manifest_relative}` 记录源文件 SHA-256 与清理状态。"
        + (
            f"同时删除该视频的本地音频、帧、OCR、时间轴及其他处理中间文件。"
            if not args.keep_intermediates
            else "处理阶段中间文件按命令参数继续保留。"
        )
        + f"关联来源：[[{source_page.stem}|{title}]]；预计释放 {reclaimed_mib:.1f} MiB。\n"
    )
    _atomic_text(log_path, log_text.rstrip() + "\n" + log_entry)

    result = {
        **eligibility,
        "status": "completed",
        "source_video_deleted": not source_video.exists(),
        "production_job_deleted": (
            not job_root.exists() if not args.keep_intermediates else False
        ),
        "completed_at": cleanup_record["completed_at"],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FinalizeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
