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

SCHEMA="$REPO_ROOT/skills/second-brain/references/wiki-schema.md"

for field in research_tracks entity_type concept_type model_type synthesis_type \
  technology_horizon technology_maturity commercialization_stage; do
  grep -Fq "$field" "$SCHEMA" \
    && pass "schema field exists: $field" \
    || fail "schema field missing: $field"
done

grep -Fq "Research result → independent reproduction → prototype → pilot → production deployment → scaled adoption" "$SCHEMA" \
  && pass "schema preserves the technology maturity chain" \
  || fail "schema is missing the technology maturity chain"

grep -Fq "Problem validation → demo/POC → paid pilot → formal order → delivery → recognized revenue → profit → FCF" "$SCHEMA" \
  && pass "schema preserves the commercialization chain" \
  || fail "schema is missing the commercialization chain"

for template in concept.md trend-thesis.md technology-model.md \
  commercialization-model.md industry-opportunity-map.md \
  technology-monitoring.md; do
  grep -Fq "research_tracks:" "$REPO_ROOT/templates/$template" \
    && pass "template declares research tracks: $template" \
    || fail "template is missing research tracks: $template"
done

grep -Fq "independently_reproduced" "$REPO_ROOT/templates/trend-thesis.md" \
  && grep -Fq "## Benchmark、复现与可比边界" "$REPO_ROOT/templates/trend-thesis.md" \
  && pass "trend thesis distinguishes maturity and benchmark boundaries" \
  || fail "trend thesis is missing a maturity or benchmark boundary"

grep -Fq "direct" "$REPO_ROOT/skills/technology-to-investment/SKILL.md" \
  && grep -Fq "spurious" "$REPO_ROOT/skills/technology-to-investment/SKILL.md" \
  && grep -Fq "current-price" "$REPO_ROOT/skills/technology-to-investment/SKILL.md" \
  && pass "opportunity workflow separates exposure and tradability" \
  || fail "opportunity workflow collapses exposure or tradability"

grep -Fq "frontier-tech-research" "$REPO_ROOT/scripts/setup_codex.sh" \
  && grep -Fq "technology-to-investment" "$REPO_ROOT/scripts/setup_codex.sh" \
  && pass "setup exposes both frontier research skills" \
  || fail "setup is missing a frontier research skill"

echo "=== Results: $PASS passed, $FAIL failed ==="

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
