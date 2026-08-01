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
  a-share-research-data
  a-share-technical-analysis
  frontier-tech-research
  technology-to-investment
)

TEMPLATES=(
  source.md
  entity.md
  event.md
  model.md
  investment-thesis.md
  monitoring.md
  concept.md
  trend-thesis.md
  technology-model.md
  commercialization-model.md
  industry-opportunity-map.md
  technology-monitoring.md
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
grep -Fq "concept_type:" "$REPO_ROOT/templates/concept.md" \
  && grep -Fq "## 竞争或替代路线" "$REPO_ROOT/templates/concept.md" \
  && pass "Concept template covers technical route comparison" \
  || fail "Concept template is missing technical route comparison"
grep -Fq "synthesis_type: trend_thesis" "$REPO_ROOT/templates/trend-thesis.md" \
  && grep -Fq "technology_maturity:" "$REPO_ROOT/templates/trend-thesis.md" \
  && grep -Fq "## 关键未知项" "$REPO_ROOT/templates/trend-thesis.md" \
  && pass "Trend thesis template preserves maturity and unknowns" \
  || fail "Trend thesis template is missing maturity or unknowns"
grep -Fq "model_type: technology_trend" "$REPO_ROOT/templates/technology-model.md" \
  && grep -Fq "## Benchmark 归一化与复现状态" "$REPO_ROOT/templates/technology-model.md" \
  && pass "Technology model template preserves benchmark normalization" \
  || fail "Technology model template is missing benchmark normalization"
grep -Fq "commercialization_stage:" "$REPO_ROOT/templates/commercialization-model.md" \
  && grep -Fq "## 从 POC 到规模采用的漏斗" "$REPO_ROOT/templates/commercialization-model.md" \
  && pass "Commercialization template preserves stage gates" \
  || fail "Commercialization template is missing stage gates"
grep -Fq "synthesis_type: opportunity_map" "$REPO_ROOT/templates/industry-opportunity-map.md" \
  && grep -Fq "直接/间接/可选/伪相关" "$REPO_ROOT/templates/industry-opportunity-map.md" \
  && pass "Opportunity map separates exposure classes" \
  || fail "Opportunity map is missing exposure classes"

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
  && grep -Fq 'output/equity-research/' "$REPO_ROOT/skills/equity-research/SKILL.md" \
  && grep -Fq 'Ask before any Canonical Wiki write' "$REPO_ROOT/skills/equity-research/SKILL.md" \
  && grep -Fq "tradable at the current price" "$REPO_ROOT/skills/equity-research/SKILL.md" \
  && pass "equity-research enforces report archive, Canonical approval, and currentness gates" \
  || fail "equity-research is missing a required gate"

grep -Fq "independent reproduction" "$REPO_ROOT/skills/frontier-tech-research/SKILL.md" \
  && grep -Fq "Normalize technical comparisons" "$REPO_ROOT/skills/frontier-tech-research/SKILL.md" \
  && grep -Fq "wait for explicit curator approval" "$REPO_ROOT/skills/frontier-tech-research/SKILL.md" \
  && pass "frontier-tech-research preserves benchmark, maturity, and save gates" \
  || fail "frontier-tech-research is missing a required research gate"

grep -Fq "Problem validation" "$REPO_ROOT/skills/technology-to-investment/SKILL.md" \
  && grep -Fq "value creation from value capture" "$REPO_ROOT/skills/technology-to-investment/SKILL.md" \
  && grep -Fq 'Route a complete one-security dossier' "$REPO_ROOT/skills/technology-to-investment/SKILL.md" \
  && pass "technology-to-investment preserves commercialization and security boundaries" \
  || fail "technology-to-investment is missing a required opportunity gate"

grep -Fq "CNINFO" "$REPO_ROOT/skills/a-share-research-data/SKILL.md" \
  && grep -Fq "read-only" "$REPO_ROOT/skills/a-share-research-data/SKILL.md" \
  && grep -Fq "result_status=empty" "$REPO_ROOT/skills/a-share-research-data/references/data-contract.md" \
  && grep -Fq "raw_response_sha256" "$REPO_ROOT/skills/a-share-research-data/references/data-contract.md" \
  && pass "A-share research-data skill preserves official-first provenance and empty/error separation" \
  || fail "A-share research-data skill is missing a required evidence contract"

grep -Fq "BaoStock" "$REPO_ROOT/skills/a-share-technical-analysis/SKILL.md" \
  && grep -Fq "AkShare" "$REPO_ROOT/skills/a-share-technical-analysis/SKILL.md" \
  && grep -Fq "CZSC" "$REPO_ROOT/skills/a-share-technical-analysis/SKILL.md" \
  && grep -Fq "chan.py" "$REPO_ROOT/skills/a-share-technical-analysis/SKILL.md" \
  && grep -Fq "BSP" "$REPO_ROOT/skills/a-share-technical-analysis/SKILL.md" \
  && grep -Fq "monthly" "$REPO_ROOT/skills/a-share-technical-analysis/SKILL.md" \
  && grep -Fq "native_chan_charts" "$REPO_ROOT/skills/a-share-technical-analysis/SKILL.md" \
  && grep -Fq -- "--no-native-chan-charts" "$REPO_ROOT/skills/a-share-technical-analysis/SKILL.md" \
  && pass "A-share technical skill preserves providers, dual engines, BSP boundaries, multi-timeframe roles, and native charts" \
  || fail "A-share technical skill is missing a provider, engine, BSP, timeframe, or native-chart contract"

for requirement in baostock==0.9.3 akshare==1.18.80 czsc==0.10.12; do
  grep -Fxq "$requirement" "$REPO_ROOT/skills/a-share-technical-analysis/requirements.txt" \
    && pass "A-share technical dependency is pinned: $requirement" \
    || fail "A-share technical dependency is not pinned: $requirement"
done

grep -Fq '${VENV_DIR}；chan.py=${CHAN_COMMIT}' \
  "$REPO_ROOT/skills/a-share-technical-analysis/scripts/setup_env.sh" \
  && pass "A-share technical setup braces variables before non-ASCII punctuation" \
  || fail "A-share technical setup may parse a variable across non-ASCII punctuation"

grep -Fq '$a-share-research-data' "$REPO_ROOT/skills/second-brain-query/SKILL.md" \
  && grep -Fq '$a-share-research-data' "$REPO_ROOT/skills/equity-research/SKILL.md" \
  && grep -Fq '$a-share-technical-analysis' "$REPO_ROOT/skills/second-brain-query/SKILL.md" \
  && grep -Fq '$a-share-technical-analysis' "$REPO_ROOT/skills/equity-research/SKILL.md" \
  && pass "query and equity-research route A-share research data and technical analysis" \
  || fail "A-share research-data or technical routing is missing"

for field in technical_as_of data_providers adjustment technical_engine technical_engines \
  technical_config_hashes data_quality_status engine_consistency_status overall_technical_status \
  technical_state_receipt technical_state_sha256; do
  grep -Fq "$field" "$REPO_ROOT/skills/second-brain/references/wiki-schema.md" \
    && pass "schema defines optional technical field $field" \
    || fail "schema is missing technical field $field"
done

for field in research_tracks entity_type concept_type model_type synthesis_type \
  technology_horizon technology_maturity commercialization_stage; do
  grep -Fq "$field" "$REPO_ROOT/skills/second-brain/references/wiki-schema.md" \
    && grep -Fq "$field" "$REPO_ROOT/AGENTS.md" \
    && pass "frontier research field is defined: $field" \
    || fail "frontier research field is missing: $field"
done

grep -Fq '$frontier-tech-research' "$REPO_ROOT/skills/second-brain-query/SKILL.md" \
  && grep -Fq '$technology-to-investment' "$REPO_ROOT/skills/second-brain-query/SKILL.md" \
  && grep -Fq '$frontier-tech-research' "$REPO_ROOT/skills/second-brain-ingest/SKILL.md" \
  && grep -Fq '$technology-to-investment' "$REPO_ROOT/skills/second-brain-ingest/SKILL.md" \
  && pass "query and ingest route frontier technology and opportunity workflows" \
  || fail "frontier technology workflow routing is incomplete"

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

if git -C "$REPO_ROOT" check-ignore -q --no-index "output/equity-research/sse-600519-report.md"; then
  pass "non-canonical equity-research reports are ignored"
else
  fail "non-canonical equity-research reports are not ignored"
fi

if bash "$REPO_ROOT/tests/test_market_routing.sh" >/dev/null; then
  pass "market-aware A-share, U.S.-equity, and cross-market routing passes"
else
  fail "market-aware routing test failed"
fi

if bash "$REPO_ROOT/tests/test_a_share_research_data.sh" >/dev/null; then
  pass "offline A-share research-data contracts and CLI tests pass"
else
  fail "offline A-share research-data tests failed"
fi

if bash "$REPO_ROOT/tests/test_a_share_technical_analysis.sh" >/dev/null; then
  pass "offline A-share provider, quality-gate, CZSC, chan.py, and report tests pass"
else
  fail "offline A-share technical-analysis tests failed"
fi

if bash "$REPO_ROOT/tests/test_frontier_research.sh" >/dev/null; then
  pass "frontier technology, commercialization, and opportunity contracts pass"
else
  fail "frontier research contract test failed"
fi

if bash "$REPO_ROOT/tests/test_equity_research_report.sh" >/dev/null; then
  pass "equity-research automatically archives non-canonical reports safely"
else
  fail "equity-research report archive test failed"
fi

if bash "$REPO_ROOT/tests/test_skill_naming.sh" >/dev/null; then
  pass "Skill display names and workflow invocations use canonical English names"
else
  fail "Skill naming consistency test failed"
fi

echo "=== Results: $PASS passed, $FAIL failed ==="

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
