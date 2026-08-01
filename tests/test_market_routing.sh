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

require_text() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if grep -Fq "$pattern" "$file"; then
    pass "$label"
  else
    fail "$label"
  fi
}

for profile in a-share-analysis.md us-equity-analysis.md cross-market-analysis.md; do
  if [ -f "$REPO_ROOT/skills/second-brain/references/$profile" ]; then
    pass "market profile exists: $profile"
  else
    fail "market profile missing: $profile"
  fi
done

SCHEMA="$REPO_ROOT/skills/second-brain/references/wiki-schema.md"
for field in \
  primary_ticker \
  listing_regime \
  analysis_regimes \
  issuer_domicile \
  reporting_standard \
  reporting_currency \
  trading_currency \
  policy_jurisdictions \
  operating_geographies \
  cross_listed_tickers \
  market_rules_as_of \
  fx_as_of; do
  require_text "$SCHEMA" "$field" "schema defines $field"
done

QUERY="$REPO_ROOT/skills/second-brain-query/SKILL.md"
EQUITY="$REPO_ROOT/skills/equity-research/SKILL.md"
RESEARCH_DATA="$REPO_ROOT/skills/a-share-research-data/SKILL.md"
TECHNICAL="$REPO_ROOT/skills/a-share-technical-analysis/SKILL.md"
INGEST="$REPO_ROOT/skills/second-brain-ingest/SKILL.md"
LINT="$REPO_ROOT/skills/second-brain-lint/SKILL.md"

for workflow in "$QUERY" "$EQUITY"; do
  require_text "$workflow" "SSE:*" "$(basename "$(dirname "$workflow")") routes SSE"
  require_text "$workflow" "NASDAQ:*" "$(basename "$(dirname "$workflow")") routes NASDAQ"
  require_text "$workflow" "a-share-analysis.md" "$(basename "$(dirname "$workflow")") loads A-share profile"
  require_text "$workflow" "us-equity-analysis.md" "$(basename "$(dirname "$workflow")") loads U.S. profile"
  require_text "$workflow" "cross-market-analysis.md" "$(basename "$(dirname "$workflow")") loads cross-market profile"
done

for skill_file in "$RESEARCH_DATA" "$TECHNICAL"; do
  if [ -f "$skill_file" ]; then
    pass "shared A-share skill exists: $(basename "$(dirname "$skill_file")")"
  else
    fail "shared A-share skill missing: $skill_file"
  fi
done

for workflow in "$QUERY" "$EQUITY"; do
  workflow_name="$(basename "$(dirname "$workflow")")"
  require_text "$workflow" '$a-share-research-data' \
    "$workflow_name routes applicable current facts to shared research data"
  require_text "$workflow" '$a-share-technical-analysis' \
    "$workflow_name routes applicable security views to technical analysis"
  require_text "$workflow" 'verified_fact' "$workflow_name preserves verified facts"
  require_text "$workflow" 'company_statement' "$workflow_name preserves company statements"
  require_text "$workflow" 'source_opinion' "$workflow_name preserves source opinions"
  require_text "$workflow" 'market_consensus' "$workflow_name preserves market consensus"
  require_text "$workflow" 'codex_inference' "$workflow_name preserves Codex inference"
  require_text "$workflow" 'Do not automatically generate or execute buy/sell orders.' \
    "$workflow_name forbids automatic trading orders"
done

require_text "$EQUITY" 'run the complete D1–D4 contract' \
  "equity-research defaults to the complete D1-D4 contract"
require_text "$EQUITY" 'run the complete C1–C5 contract' \
  "equity-research defaults to the complete C1-C5 contract"
for module in D1 D2 D3 D4 C1 C2 C3 C4 C5; do
  require_text "$EQUITY" "**$module " \
    "equity-research defines A-share module $module"
done

require_text "$QUERY" 'purely factual Wiki lookup' \
  "query keeps purely factual Wiki lookups local"
require_text "$QUERY" 'necessary `$a-share-research-data` modules:' \
  "query requests only needed current-data modules"
require_text "$QUERY" 'Do not invoke it merely because an A-share ticker is' \
  "query does not trigger technical analysis from ticker presence alone"
require_text "$QUERY" 'security view, comparison, research update, position review, or week/month' \
  "query limits technical analysis to views, comparisons, positions, or allocation"
require_text "$QUERY" 'An empty result is not a provider error' \
  "query distinguishes empty provider results from errors"

for module in D1 D2 D3 D4; do
  require_text "$RESEARCH_DATA" "$module" \
    "shared research-data skill defines module $module"
done
for module in C1 C2 C3 C4 C5; do
  require_text "$TECHNICAL" "$module" \
    "shared technical skill defines module $module"
done
require_text "$REPO_ROOT/skills/second-brain/references/a-share-analysis.md" \
  "monthly structure as the primary regime" "A-share profile defines non-intraday timeframe roles"

require_text "$INGEST" "primary_ticker" "ingest populates market-routing metadata"
require_text "$INGEST" "ticker alone." "ingest preserves domicile evidence boundary"
require_text "$LINT" "Exchange-to-regime mismatch" "lint detects exchange-to-regime mismatch"
require_text "$LINT" "market_rules_as_of" "lint checks market-rule cutoff"

for template in entity.md model.md investment-thesis.md monitoring.md; do
  require_text "$REPO_ROOT/templates/$template" "analysis_regimes:" "$template contains analysis regimes"
done
require_text "$REPO_ROOT/templates/entity.md" "listing_regime:" "Entity template contains listing regime"
require_text "$REPO_ROOT/templates/model.md" "## 市场路由与口径统一" "Model template separates market routing"
require_text "$REPO_ROOT/templates/investment-thesis.md" "### 分市场判断" "Thesis template separates market judgment"
require_text "$REPO_ROOT/templates/monitoring.md" "## 分市场监测" "Monitoring template separates market monitoring"

for file in "$REPO_ROOT"/wiki/entities/*.md; do
  if grep -Eq '(SSE|SZSE|BJSE|NASDAQ|NYSE|NYSEARCA|AMEX|TWSE|Euronext):' "$file"; then
    for field in \
      primary_ticker \
      listing_regime \
      analysis_regimes \
      security_type \
      issuer_domicile \
      reporting_standard \
      reporting_currency \
      trading_currency \
      policy_jurisdictions \
      operating_geographies \
      cross_listed_tickers; do
      if ! grep -Eq "^${field}:" "$file"; then
        fail "$(basename "$file") missing $field"
      fi
    done
  fi

  if grep -Eq '^primary_ticker: "(SSE|SZSE|BJSE):' "$file"; then
    grep -Eq '^listing_regime: a_share$' "$file" \
      && pass "$(basename "$file") routes to a_share" \
      || fail "$(basename "$file") does not route to a_share"
  fi

  if grep -Eq '^primary_ticker: "(NASDAQ|NYSE|NYSEARCA|AMEX):' "$file" \
    && ! grep -Eq '^listing_regime: cross_market$' "$file"; then
    grep -Eq '^listing_regime: us_equity$' "$file" \
      && pass "$(basename "$file") routes to us_equity" \
      || fail "$(basename "$file") does not route to us_equity"
  fi
done

for file in "$REPO_ROOT"/wiki/models/*.md "$REPO_ROOT"/wiki/synthesis/*.md; do
  if grep -Eq '(SSE|SZSE|BJSE|NASDAQ|NYSE|NYSEARCA|AMEX|TWSE|Euronext):' "$file"; then
    for field in analysis_regimes policy_jurisdictions reporting_currencies; do
      if ! grep -Eq "^${field}:" "$file"; then
        fail "$(basename "$file") missing $field"
      fi
    done
  fi
done

require_text "$REPO_ROOT/wiki/entities/taiwan-semiconductor-manufacturing.md" \
  "listing_regime: cross_market" "TSMC is cross-market"
require_text "$REPO_ROOT/wiki/entities/taiwan-semiconductor-manufacturing.md" \
  'cross_listed_tickers: ["NYSE:TSM"]' "TSMC ADR is preserved"
require_text "$REPO_ROOT/wiki/entities/asml-holding.md" \
  "listing_regime: cross_market" "ASML is cross-market"
require_text "$REPO_ROOT/wiki/entities/asml-holding.md" \
  'cross_listed_tickers: ["NASDAQ:ASML"]' "ASML U.S. listing is preserved"

echo "=== Results: $PASS passed, $FAIL failed ==="

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
