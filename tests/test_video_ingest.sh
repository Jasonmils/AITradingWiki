#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BRIDGE="$REPO_ROOT/skills/second-brain-ingest/scripts/video_to_html.py"
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
find "$VAULT/output/video-ingest/manifests" -name '*.json' -type f | grep -q .

echo "video ingest bridge tests passed"
