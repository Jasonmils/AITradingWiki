#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SKILLS=(
  second-brain
  second-brain-ingest
  second-brain-query
  second-brain-lint
  equity-research
  a-share-research-data
  a-share-technical-analysis
  frontier-tech-research
  technology-to-investment
)

DISPLAY_NAMES=(
  "Second Brain Setup"
  "Second Brain Ingest"
  "Second Brain Query"
  "Second Brain Lint"
  "Equity Research"
  "A-Share Research Data"
  "A-Share Technical Analysis"
  "Frontier Tech Research"
  "Technology to Investment"
)

PASS=0
FAIL=0

pass() {
  echo "PASS: $1"
  PASS=$((PASS + 1))
}

fail() {
  echo "FAIL: $1" >&2
  FAIL=$((FAIL + 1))
}

is_canonical_skill() {
  local candidate="$1"
  local skill

  for skill in "${SKILLS[@]}"; do
    if [ "$candidate" = "$skill" ]; then
      return 0
    fi
  done
  return 1
}

for index in "${!SKILLS[@]}"; do
  skill="${SKILLS[$index]}"
  expected_display_name="${DISPLAY_NAMES[$index]}"
  skill_file="$REPO_ROOT/skills/$skill/SKILL.md"
  metadata_file="$REPO_ROOT/skills/$skill/agents/openai.yaml"

  declared_name="$(sed -n 's/^name: //p' "$skill_file" | head -n 1)"
  heading="$(sed -n 's/^# //p' "$skill_file" | head -n 1)"
  display_name="$(sed -n 's/^  display_name: "\(.*\)"$/\1/p' "$metadata_file" | head -n 1)"
  canonical_invocation="\$$skill"

  [ "$declared_name" = "$skill" ] \
    && pass "directory and frontmatter name match: $skill" \
    || fail "directory/frontmatter mismatch: $skill declares $declared_name"

  [ "$heading" = "$expected_display_name" ] \
    && pass "English Skill heading is canonical: $expected_display_name" \
    || fail "unexpected heading for $skill: $heading"

  [ "$display_name" = "$expected_display_name" ] \
    && pass "English display_name is canonical: $expected_display_name" \
    || fail "unexpected display_name for $skill: $display_name"

  if printf '%s' "$display_name" | LC_ALL=C grep -q '[^ -~]'; then
    fail "display_name contains non-ASCII characters: $skill"
  else
    pass "display_name is English-only: $skill"
  fi

  grep -Fq "$canonical_invocation" "$metadata_file" \
    && pass "default_prompt invokes canonical identifier: $canonical_invocation" \
    || fail "default_prompt does not invoke $canonical_invocation"
done

ROUTING_FILES=(
  "$REPO_ROOT/AGENTS.md"
  "$REPO_ROOT/README.md"
  "$REPO_ROOT/README.zh-CN.md"
  "$REPO_ROOT/skills/second-brain/references/wiki-schema.md"
  "$REPO_ROOT/skills/second-brain/references/agent-configs/codex.md"
)

while IFS= read -r skill_file; do
  ROUTING_FILES+=("$skill_file")
done < <(find "$REPO_ROOT/skills" -mindepth 2 -maxdepth 2 -name SKILL.md -type f | LC_ALL=C sort)

while IFS= read -r metadata_file; do
  ROUTING_FILES+=("$metadata_file")
done < <(find "$REPO_ROOT/skills" -mindepth 3 -maxdepth 3 -path '*/agents/openai.yaml' -type f | LC_ALL=C sort)

UNKNOWN_INVOCATIONS=()
while IFS= read -r invocation; do
  [ -n "$invocation" ] || continue
  candidate="${invocation#\$}"
  if ! is_canonical_skill "$candidate"; then
    UNKNOWN_INVOCATIONS+=("$invocation")
  fi
done < <(rg -o --no-filename '\$[a-z][a-z0-9-]*' "${ROUTING_FILES[@]}" | LC_ALL=C sort -u)

if [ "${#UNKNOWN_INVOCATIONS[@]}" -eq 0 ]; then
  pass "all routed Skill invocations use canonical English identifiers"
else
  fail "non-canonical Skill invocations found: ${UNKNOWN_INVOCATIONS[*]}"
fi

REGISTRY_FILES=(
  "$REPO_ROOT/AGENTS.md"
  "$REPO_ROOT/README.md"
  "$REPO_ROOT/README.zh-CN.md"
  "$REPO_ROOT/skills/second-brain/references/wiki-schema.md"
)

for skill in "${SKILLS[@]}"; do
  canonical_invocation="\$$skill"
  for registry_file in "${REGISTRY_FILES[@]}"; do
    grep -Fq "$canonical_invocation" "$registry_file" \
      || fail "missing $canonical_invocation in ${registry_file#"$REPO_ROOT"/}"
  done

  grep -Fxq "  $skill" "$REPO_ROOT/scripts/setup_codex.sh" \
    || fail "setup_codex.sh does not expose canonical Skill directory: $skill"
done

if [ "$FAIL" -eq 0 ]; then
  pass "all canonical names are registered in AGENTS, schema, READMEs, and setup"
fi

echo "=== Results: $PASS passed, $FAIL failed ==="

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
