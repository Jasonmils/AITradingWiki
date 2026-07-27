#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BRIDGE="$REPO_ROOT/skills/second-brain-ingest/scripts/video_to_html.py"
FINALIZER="$REPO_ROOT/skills/second-brain-ingest/scripts/finalize_video_ingest.py"
TEST_ROOT="$(mktemp -d)"
VAULT="$TEST_ROOT/vault"
TOOL="$TEST_ROOT/Video2Skill_Invest"

cleanup() {
  rm -rf "$TEST_ROOT"
}
trap cleanup EXIT

mkdir -p "$VAULT/raw" "$TOOL/src/invest_lecture_digest" "$TOOL/.venv/bin" "$TOOL/configs"
printf '%s' "immutable-video" > "$VAULT/raw/sample.MP4"
printf '%s\n' "HF_TOKEN=test-only" "DEEPSEEK_API_KEY=test-only" > "$VAULT/.env.video-ingest.local"
printf '%s\n' "# fake cli" > "$TOOL/src/invest_lecture_digest/cli.py"
printf '%s\n' "{}" > "$TOOL/configs/lecture.production.macos.json"
printf '%s\n' "{}" > "$TOOL/configs/lecture.production.macos.accelerated.json"
printf '%s\n' "{}" > "$TOOL/configs/transcript.refinement.json"

printf '%s\n' \
  '#!/usr/bin/env bash' \
  'set -euo pipefail' \
  'ROOT=""' \
  'while [ "$#" -gt 0 ]; do' \
  '  if [ "$1" = "--root" ]; then' \
  '    ROOT="$2"' \
  '    shift 2' \
  '  else' \
  '    shift' \
  '  fi' \
  'done' \
  'OUT="$ROOT/jobs/fake/output"' \
  'mkdir -p "$OUT"' \
  'printf '\''%s\n'\'' '\''{"source":{},"slides":[]}'\'' > "$OUT/timeline.json"' \
  'printf '\''%s\n'\'' '\''<html>original</html>'\'' > "$OUT/timeline.html"' \
  'printf '\''%s\n'\'' '\''<html>refined</html>'\'' > "$OUT/timeline.deepseek.html"' \
  'printf '\''{"production_job_id":"fake","status":"succeeded","stage":"render","refinement_status":"completed","artifacts":{"timeline_json":"%s","timeline_html":"%s","timeline_deepseek_html":"%s"}}\n'\'' "$OUT/timeline.json" "$OUT/timeline.html" "$OUT/timeline.deepseek.html"' \
  > "$TOOL/.venv/bin/python"
chmod +x "$TOOL/.venv/bin/python"

BEFORE="$(shasum -a 256 "$VAULT/raw/sample.MP4" | awk '{print $1}')"

python3 "$BRIDGE" "$VAULT/raw/sample.MP4" \
  --vault-root "$VAULT" \
  --video2skill-root "$TOOL" \
  --preflight-only \
  | grep -Fq '"status": "ready"'

if python3 "$BRIDGE" "$VAULT/raw/sample.MP4" \
  --vault-root "$VAULT" \
  --video2skill-root "$TOOL" >/dev/null 2>&1; then
  echo "bridge accepted remote processing without approval" >&2
  exit 1
fi

RESULT="$(python3 "$BRIDGE" "$VAULT/raw/sample.MP4" \
  --vault-root "$VAULT" \
  --video2skill-root "$TOOL" \
  --allow-remote-processing)"

printf '%s' "$RESULT" | grep -Fq '"status": "completed"'
printf '%s' "$RESULT" | grep -Fq '"ingest_input_html"'
printf '%s' "$RESULT" | grep -Fq '"raw_video_modified": false'
printf '%s' "$RESULT" | grep -Fq '"video2skill_revision":'

AFTER="$(shasum -a 256 "$VAULT/raw/sample.MP4" | awk '{print $1}')"
[ "$BEFORE" = "$AFTER" ]
MANIFEST="$(find "$VAULT/output/video-ingest/manifests" -name '*.json' -type f)"
[ -n "$MANIFEST" ]

mkdir -p "$VAULT/wiki/sources"
SOURCE_PAGE="$VAULT/wiki/sources/sample-video.md"
printf '%s\n' \
  '---' \
  'page_type: source' \
  'subject: "Sample video"' \
  'as_of: 2026-07-26' \
  'created: 2026-07-26' \
  'updated: 2026-07-26' \
  "source_sha256: \"$BEFORE\"" \
  '---' \
  '' \
  '# Sample video' \
  '' \
  '- 原始文件：`raw/sample.MP4`' \
  '- 原始 ASR/OCR：`output/video-ingest/production/jobs/fake/output/timeline.html`' \
  '- DeepSeek 精炼：`output/video-ingest/production/jobs/fake/output/timeline.deepseek.html`' \
  > "$SOURCE_PAGE"
printf '%s\n' \
  '# Log' \
  '' \
  '## 2026-07-26 ingest | Sample video' \
  'Processed `raw/sample.MP4` into the canonical Wiki.' \
  > "$VAULT/wiki/log.md"

CHECK_RESULT="$(python3 "$FINALIZER" "$MANIFEST" \
  --vault-root "$VAULT" \
  --source-page "$SOURCE_PAGE" \
  --check-only)"
printf '%s' "$CHECK_RESULT" | grep -Fq '"status": "eligible"'
[ -f "$VAULT/raw/sample.MP4" ]
[ -d "$VAULT/output/video-ingest/production/jobs/fake" ]

if python3 "$FINALIZER" "$MANIFEST" \
  --vault-root "$VAULT" \
  --source-page "$SOURCE_PAGE" >/dev/null 2>&1; then
  echo "finalizer deleted without an explicit confirmation mode" >&2
  exit 1
fi

FINAL_RESULT="$(python3 "$FINALIZER" "$MANIFEST" \
  --vault-root "$VAULT" \
  --source-page "$SOURCE_PAGE" \
  --confirm-delete-source-video)"
printf '%s' "$FINAL_RESULT" | grep -Fq '"status": "completed"'
printf '%s' "$FINAL_RESULT" | grep -Fq '"source_video_deleted": true'
printf '%s' "$FINAL_RESULT" | grep -Fq '"production_job_deleted": true'
[ ! -e "$VAULT/raw/sample.MP4" ]
[ ! -e "$VAULT/output/video-ingest/production/jobs/fake" ]

SHORT_SHA="${BEFORE%${BEFORE#????????????}}"
RETAINED_DIR="$VAULT/output/video-ingest/transcripts/sample-$SHORT_SHA"
[ -s "$RETAINED_DIR/timeline.html" ]
[ -s "$RETAINED_DIR/timeline.deepseek.html" ]
[ "$(find "$RETAINED_DIR" -type f | wc -l | tr -d ' ')" = "2" ]
grep -Fq 'source_file_status: "deleted_after_confirmed_ingest"' "$SOURCE_PAGE"
grep -Fq 'output/video-ingest/transcripts/sample-' "$SOURCE_PAGE"
grep -Fq '视频源文件终态清理' "$VAULT/wiki/log.md"
grep -Fq '"status": "wiki_ingested_source_deleted"' "$MANIFEST"

mkdir -p "$VAULT/output/video-ingest/production/jobs/fake"
printf '%s' "icloud-race" \
  > "$VAULT/output/video-ingest/production/jobs/fake/.DS_Store"
python3 - "$MANIFEST" <<'PY'
import json
from pathlib import Path
import sys

path = Path(sys.argv[1])
payload = json.loads(path.read_text(encoding="utf-8"))
payload["status"] = "completed"
payload["cleanup"]["status"] = "deletion_in_progress"
payload["cleanup"].pop("completed_at", None)
path.write_text(
    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
PY

RECOVERY_RESULT="$(python3 "$FINALIZER" "$MANIFEST" \
  --vault-root "$VAULT" \
  --source-page "$SOURCE_PAGE" \
  --confirm-delete-source-video)"
printf '%s' "$RECOVERY_RESULT" | grep -Fq '"resumed_from": "deletion_in_progress"'
[ ! -e "$VAULT/output/video-ingest/production/jobs/fake" ]

REPEAT_RESULT="$(python3 "$FINALIZER" "$MANIFEST" \
  --vault-root "$VAULT" \
  --source-page "$SOURCE_PAGE" \
  --confirm-delete-source-video)"
printf '%s' "$REPEAT_RESULT" | grep -Fq '"status": "already_finalized"'

echo "video ingest bridge tests passed"
