---
name: a-share-research-data
description: Retrieve read-only, provenance-rich research data for one canonical SSE, SZSE, or BJSE security. Use when equity-research or second-brain-query needs current quote and valuation observations, stale or possible-suspension checks, official CNINFO filings, restricted-share unlocks, dividends, holder counts, block trades, margin data, official-first financial discovery, third-party financial or consensus cross-checks, investor-relations replies, or news leads. Do not use for technical-chart analysis, intraday trading signals, raw-source ingestion, or writing Canonical Wiki pages.
---

# A-Share Research Data

Use this Skill as a shared read-only data layer for `$equity-research` and
`$second-brain-query`.

## Run

Require an exchange-prefixed ticker; never infer one from a company name or a
bare six-digit code.

```bash
python3 skills/a-share-research-data/scripts/research_snapshot.py \
  --ticker SSE:600519 \
  --modules d1,d2,d3,d4
```

The CLI writes non-canonical reports to `output/a-share-research-data/` and
HTTP cache entries to `.work/a-share-research-data/`. Use `--fixture FILE` for
offline, network-free runs. Import `ResearchDataClient` from
`scripts/research_data.py` to inject a custom transport in tests or callers.

## Modules

- D1: quote/valuation observations plus stale and possible-suspension checks.
- D2: official announcements plus unlock, dividend, holder-count, block-trade,
  and margin discovery.
- D3: official-first financial filings, financial cross-checks, and consensus.
- D4: company IR answers and news leads.

## Boundaries

- Treat CNINFO filings as the primary document-discovery route. Read the actual
  filing before promoting a material claim to `verified_fact`.
- Treat Sina financials and Eastmoney/THS datasets as cross-checks or discovery
  only. Reconcile material items with an official filing.
- Treat company IR answers as `company_statement`; investor questions and news
  are leads, not facts.
- Preserve provider values and units. Do not add a universal P/E target, PEG
  rule, buy/sell signal, or inferred “main-force” behavior.
- Do not write `wiki/`, `raw/`, `wiki/index.md`, or `wiki/log.md`.
- Report errors and partial pagination explicitly. Never reinterpret a failed
  request as a true empty result.

Read [references/data-contract.md](references/data-contract.md) when consuming
or extending the output schema.
