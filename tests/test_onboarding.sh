#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ONBOARDING="$REPO_ROOT/skills/second-brain/scripts/onboarding.sh"
TEST_DIR="$(mktemp -d)"
TEST_VAULT="$TEST_DIR/test-vault"

cleanup() {
  rm -rf "$TEST_DIR"
}
trap cleanup EXIT

PASS=0
FAIL=0

pass() {
  echo "  PASS: $1"
  PASS=$((PASS + 1))
}

fail() {
  echo "  FAIL: $1"
  FAIL=$((FAIL + 1))
}

assert_dir() {
  if [ -d "$1" ]; then
    pass "directory exists — $1"
  else
    fail "directory missing — $1"
  fi
}

assert_file() {
  if [ -f "$1" ]; then
    pass "file exists — $1"
  else
    fail "file missing — $1"
  fi
}

assert_contains() {
  if grep -Fq "$2" "$1" 2>/dev/null; then
    pass "file contains '$2' — $1"
  else
    fail "file does not contain '$2' — $1"
  fi
}

file_digest() {
  cksum "$1" | awk '{print $1 ":" $2}'
}

tree_manifest() {
  local root="$1"
  find "$root" -type f -print | LC_ALL=C sort | while IFS= read -r path; do
    printf '%s ' "${path#"$root"/}"
    file_digest "$path"
  done
}

echo "=== Test: onboarding.sh ==="

echo "Test 1: Fresh investment-research vault scaffolding"
OUTPUT="$(bash "$ONBOARDING" "$TEST_VAULT" 2>/dev/null)"

for dir in \
  raw \
  raw/assets \
  wiki \
  wiki/sources \
  wiki/entities \
  wiki/concepts \
  wiki/events \
  wiki/models \
  wiki/synthesis \
  templates \
  output; do
  assert_dir "$TEST_VAULT/$dir"
done

for template in \
  source.md \
  entity.md \
  event.md \
  model.md \
  investment-thesis.md \
  monitoring.md \
  concept.md \
  trend-thesis.md \
  technology-model.md \
  commercialization-model.md \
  industry-opportunity-map.md \
  technology-monitoring.md; do
  assert_file "$TEST_VAULT/templates/$template"
done

echo "Test 2: Index and log scaffolding"
assert_file "$TEST_VAULT/wiki/index.md"
assert_file "$TEST_VAULT/wiki/log.md"

for section in \
  "## Sources" \
  "## Entities" \
  "## Concepts" \
  "## Events" \
  "## Models" \
  "## Synthesis" \
  "## Trend Theses" \
  "## Opportunity Maps" \
  "## Active Theses" \
  "## Monitoring" \
  "## Technology Monitoring"; do
  assert_contains "$TEST_VAULT/wiki/index.md" "$section"
done
assert_contains "$TEST_VAULT/wiki/log.md" "# Log"

echo "Test 3: Idempotency and immutable-content protection"
printf '\n# Custom index content\n' >> "$TEST_VAULT/wiki/index.md"
printf '\n## Custom log content\n' >> "$TEST_VAULT/wiki/log.md"
printf '%s\n' "existing event page" > "$TEST_VAULT/wiki/events/existing-event.md"
printf '%s\n' "existing template" > "$TEST_VAULT/templates/custom.md"
printf '%s\n' "immutable source" > "$TEST_VAULT/raw/source.md"
printf '%s\n' "immutable attachment" > "$TEST_VAULT/raw/assets/chart.txt"

INDEX_BEFORE="$(file_digest "$TEST_VAULT/wiki/index.md")"
LOG_BEFORE="$(file_digest "$TEST_VAULT/wiki/log.md")"
WIKI_BEFORE="$(tree_manifest "$TEST_VAULT/wiki")"
TEMPLATES_BEFORE="$(tree_manifest "$TEST_VAULT/templates")"
RAW_BEFORE="$(tree_manifest "$TEST_VAULT/raw")"

bash "$ONBOARDING" "$TEST_VAULT" >/dev/null 2>&1

[ "$INDEX_BEFORE" = "$(file_digest "$TEST_VAULT/wiki/index.md")" ] \
  && pass "existing index preserved byte-for-byte" \
  || fail "existing index changed"
[ "$LOG_BEFORE" = "$(file_digest "$TEST_VAULT/wiki/log.md")" ] \
  && pass "existing log preserved byte-for-byte" \
  || fail "existing log changed"
[ "$WIKI_BEFORE" = "$(tree_manifest "$TEST_VAULT/wiki")" ] \
  && pass "existing wiki files preserved" \
  || fail "existing wiki files changed"
[ "$TEMPLATES_BEFORE" = "$(tree_manifest "$TEST_VAULT/templates")" ] \
  && pass "existing templates preserved" \
  || fail "existing templates changed"
[ "$RAW_BEFORE" = "$(tree_manifest "$TEST_VAULT/raw")" ] \
  && pass "raw source and attachment preserved" \
  || fail "raw source or attachment changed"

echo "Test 4: JSON output"
if printf '%s' "$OUTPUT" | python3 -m json.tool >/dev/null 2>&1; then
  pass "output is valid JSON"
else
  fail "output is not valid JSON"
fi

for json_path in \
  "wiki/events/" \
  "wiki/models/" \
  "templates/"; do
  if printf '%s' "$OUTPUT" | grep -Fq "\"$json_path\""; then
    pass "JSON lists $json_path"
  else
    fail "JSON does not list $json_path"
  fi
done

echo "=== Results: $PASS passed, $FAIL failed ==="

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
