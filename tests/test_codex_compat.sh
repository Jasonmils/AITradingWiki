#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

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

SKILLS=(
  second-brain
  second-brain-ingest
  second-brain-query
  second-brain-lint
  equity-research
)

TEMPLATES=(
  source.md
  entity.md
  event.md
  model.md
  investment-thesis.md
  monitoring.md
)

INDEX_BEFORE="$(file_digest "$REPO_ROOT/wiki/index.md")"
LOG_BEFORE="$(file_digest "$REPO_ROOT/wiki/log.md")"
RAW_BEFORE="$(tree_manifest "$REPO_ROOT/raw")"
WIKI_FILES_BEFORE="$(tree_manifest "$REPO_ROOT/wiki")"

bash "$REPO_ROOT/scripts/setup_codex.sh" >/dev/null
bash "$REPO_ROOT/scripts/setup_codex.sh" >/dev/null

[ "$INDEX_BEFORE" = "$(file_digest "$REPO_ROOT/wiki/index.md")" ] \
  && pass "setup preserves wiki/index.md across repeated runs" \
  || fail "setup changed wiki/index.md"
[ "$LOG_BEFORE" = "$(file_digest "$REPO_ROOT/wiki/log.md")" ] \
  && pass "setup preserves wiki/log.md across repeated runs" \
  || fail "setup changed wiki/log.md"
[ "$RAW_BEFORE" = "$(tree_manifest "$REPO_ROOT/raw")" ] \
  && pass "setup preserves raw/ and raw/assets/" \
  || fail "setup changed raw/ or raw/assets/"
[ "$WIKI_FILES_BEFORE" = "$(tree_manifest "$REPO_ROOT/wiki")" ] \
  && pass "setup preserves existing wiki pages" \
  || fail "setup changed existing wiki pages"

for dir in wiki/events wiki/models templates; do
  [ -d "$REPO_ROOT/$dir" ] \
    && pass "directory exists: $dir" \
    || fail "directory missing: $dir"
done

for template in "${TEMPLATES[@]}"; do
  [ -f "$REPO_ROOT/templates/$template" ] \
    && pass "template exists: $template" \
    || fail "template missing: $template"
done

grep -Fq "## 关键论断" "$REPO_ROOT/templates/source.md" \
  && pass "Source template contains assertion evidence structure" \
  || fail "Source template is missing assertion evidence structure"
grep -Fq "## 研究覆盖" "$REPO_ROOT/templates/entity.md" \
  && pass "Entity template contains Hub coverage structure" \
  || fail "Entity template is missing Hub coverage structure"
grep -Fq "event_status:" "$REPO_ROOT/templates/event.md" \
  && grep -Fq "expected_date:" "$REPO_ROOT/templates/event.md" \
  && pass "Event template contains lifecycle and time fields" \
  || fail "Event template is missing lifecycle or time fields"
grep -Fq "## 情景与敏感性分析" "$REPO_ROOT/templates/model.md" \
  && grep -Fq "少数股东权益" "$REPO_ROOT/templates/model.md" \
  && pass "Model template contains scenario, sensitivity, and ownership structure" \
  || fail "Model template is missing required modeling structure"
grep -Fq "## 论点失效条件" "$REPO_ROOT/templates/investment-thesis.md" \
  && grep -Fq "## 估值与当前价格可交易性" "$REPO_ROOT/templates/investment-thesis.md" \
  && pass "Investment thesis template contains invalidation and tradability" \
  || fail "Investment thesis template is missing required sections"
grep -Fq "## 跟踪面板" "$REPO_ROOT/templates/monitoring.md" \
  && grep -Fq "## 下次复核" "$REPO_ROOT/templates/monitoring.md" \
  && pass "Monitoring template contains indicators and next review" \
  || fail "Monitoring template is missing required sections"

for skill in "${SKILLS[@]}"; do
  source_dir="$REPO_ROOT/skills/$skill"
  link="$REPO_ROOT/.agents/skills/$skill"
  expected="../../skills/$skill"

  [ -f "$source_dir/SKILL.md" ] \
    && pass "skill source exists: $skill" \
    || fail "skill source missing: $skill"
  [ -f "$source_dir/agents/openai.yaml" ] \
    && pass "skill metadata exists: $skill" \
    || fail "skill metadata missing: $skill"
  [ -L "$link" ] \
    && pass "Codex link exists: $skill" \
    || fail "Codex link missing: $skill"
  [ "$(readlink "$link" 2>/dev/null || true)" = "$expected" ] \
    && pass "Codex link is relative: $skill" \
    || fail "unexpected Codex link target: $skill"
  [ -f "$link/SKILL.md" ] \
    && pass "skill is readable through Codex link: $skill" \
    || fail "skill is unreadable through Codex link: $skill"
done

for section in \
  "## Events" \
  "## Models" \
  "## Active Theses" \
  "## Monitoring"; do
  grep -Fq "$section" "$REPO_ROOT/wiki/index.md" \
    && pass "index contains $section" \
    || fail "index missing $section"
done

for evidence_type in \
  verified_fact \
  company_statement \
  source_opinion \
  market_consensus \
  non_consensus \
  market_rumor \
  model_assumption \
  codex_inference \
  disputed; do
  grep -Fq "$evidence_type" "$REPO_ROOT/AGENTS.md" \
    && pass "AGENTS contains evidence type $evidence_type" \
    || fail "AGENTS missing evidence type $evidence_type"
done

for rule in \
  as_of \
  review_after \
  superseded \
  invalidated \
  "current price" \
  "research priority" \
  "tradability" \
  "SZSE:300767"; do
  grep -Fq "$rule" "$REPO_ROOT/AGENTS.md" \
    && pass "AGENTS contains rule $rule" \
    || fail "AGENTS missing rule $rule"
done

grep -Fq "Event" "$REPO_ROOT/skills/second-brain-ingest/SKILL.md" \
  && grep -Fq "Model" "$REPO_ROOT/skills/second-brain-ingest/SKILL.md" \
  && grep -Fq "3–5" "$REPO_ROOT/skills/second-brain-ingest/SKILL.md" \
  && pass "ingest contains evidence preview and Event/Model routing" \
  || fail "ingest is missing the upgraded workflow"

grep -Fq "Source;" "$REPO_ROOT/skills/second-brain-query/SKILL.md" \
  && grep -Fq "Currentness gate" "$REPO_ROOT/skills/second-brain-query/SKILL.md" \
  && grep -Fq "knowledge cutoff" "$REPO_ROOT/skills/second-brain-query/SKILL.md" \
  && pass "query contains ordered retrieval and currentness checks" \
  || fail "query is missing the upgraded workflow"

grep -Fq "active" "$REPO_ROOT/skills/second-brain-lint/SKILL.md" \
  && grep -Fq "event_status" "$REPO_ROOT/skills/second-brain-lint/SKILL.md" \
  && grep -Fq "Model" "$REPO_ROOT/skills/second-brain-lint/SKILL.md" \
  && grep -Fq "Entity Hub" "$REPO_ROOT/skills/second-brain-lint/SKILL.md" \
  && pass "lint contains metadata, Event, Model, and Entity Hub checks" \
  || fail "lint is missing the upgraded workflow"

grep -Fq "three-scenario Model" "$REPO_ROOT/skills/equity-research/SKILL.md" \
  && grep -Fq "Ask the user" "$REPO_ROOT/skills/equity-research/SKILL.md" \
  && grep -Fq "tradable at the current price" "$REPO_ROOT/skills/equity-research/SKILL.md" \
  && pass "equity-research is discoverable and enforces save/currentness gates" \
  || fail "equity-research is missing a required gate"

if git -C "$REPO_ROOT" check-ignore -q --no-index "skills/equity-research/SKILL.md"; then
  fail "skills/ is ignored by .gitignore"
else
  pass "skills/ is not ignored"
fi

if git -C "$REPO_ROOT" check-ignore -q --no-index ".agents/skills/equity-research"; then
  fail ".agents/skills links are ignored by .gitignore"
else
  pass ".agents/skills links are not ignored"
fi

if git -C "$REPO_ROOT" check-ignore -q --no-index ".env"; then
  pass ".env is ignored"
else
  fail ".env is not ignored"
fi

if git -C "$REPO_ROOT" check-ignore -q --no-index "credentials.json"; then
  pass "credential files are ignored"
else
  fail "credential files are not ignored"
fi

if git -C "$REPO_ROOT" check-ignore -q --no-index "raw/local-source.mp4"; then
  pass "raw source files are ignored"
else
  fail "raw source files are not ignored"
fi

if git -C "$REPO_ROOT" check-ignore -q --no-index "output/video-ingest/timeline.json"; then
  pass "generated output files are ignored"
else
  fail "generated output files are not ignored"
fi

echo "=== Results: $PASS passed, $FAIL failed ==="

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
