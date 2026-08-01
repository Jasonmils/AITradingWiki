---
name: second-brain-lint
description: Audit wiki structure and technology, commercialization, industry-opportunity, and investment-research integrity, including links, orphans, index drift, required metadata, review dates, source versions, benchmark comparability, maturity and commercialization stages, evidence classification, ticker and numeric consistency, Event status, Model reconciliation, trend and investment thesis completeness, and Entity Hub coverage. Use when the user asks to lint, audit, health-check, inspect stale claims, find problems, or "检查知识库". Report severity, file and line evidence, and a proposed fix before changing anything; apply fixes only after approval.
---

# Second Brain Lint

Audit the wiki without silently repairing or filling research gaps.

## Prepare

1. Read `wiki/index.md`.
2. Scan Markdown files in `wiki/sources/`, `wiki/entities/`, `wiki/concepts/`, `wiki/events/`, `wiki/models/`, and `wiki/synthesis/`.
3. Read `../second-brain/references/wiki-schema.md`.
4. Keep non-video `raw/` sources immutable. Treat a missing MP4 as valid only
   when its Source page and completed cleanup manifest record an audited
   post-ingest deletion.

## Structural checks

- Broken or ambiguous `[[wikilinks]]`.
- Orphan pages with no inbound link.
- Near-duplicate Entities, Concepts, Events, or ticker aliases.
- Pages missing from the correct index section.
- Index entries that point to missing pages.
- Events or Models absent from their index sections.
- Active theses or monitoring pages absent from `Active Theses` or `Monitoring`.
- Existing pages that violate filename, title, or wikilink conventions.

## Metadata and currentness checks

- Missing `page_type`, `subject`, `tags`, `tickers`, `markets`, `asset_classes`, `industries`, `themes`, `as_of`, `sources`, `created`, or `updated`.
- New or updated pages missing `research_tracks`, or using values other than
  `technology`, `commercialization`, or `investment`.
- Entity, Concept, Model, or Synthesis pages whose durable routing depends on a
  missing or invalid `entity_type`, `concept_type`, `model_type`, or
  `synthesis_type`.
- Technology or commercialization judgments missing applicable
  `technology_horizon`, `technology_maturity`, `commercialization_stage`, or
  `review_after`.
- Models, theses, monitoring, or current judgments missing `status`, `confidence`, `horizon`, or `review_after`.
- Listed-company Entities missing `primary_ticker`, `listing_regime`,
  `analysis_regimes`, `security_type`, `issuer_domicile`,
  `reporting_standard`, `reporting_currency`, `trading_currency`,
  `policy_jurisdictions`, `operating_geographies`, or
  `cross_listed_tickers`.
- Exchange-to-regime mismatch: `SSE:*`, `SZSE:*`, or `BJSE:*` not routed to
  `a_share`, or `NASDAQ:*`, `NYSE:*`, `NYSEARCA:*`, or `AMEX:*` not routed to
  `us_equity`, unless an explicitly documented `cross_market` Entity applies.
- Ticker aliases incorrectly stored as cross listings, or a material ADR,
  secondary listing, security type, share class, or ADR ratio omitted.
- Models or Syntheses spanning listed securities missing `analysis_regimes`,
  `policy_jurisdictions`, or `reporting_currencies`.
- Current tradability or listing-rule conclusions missing
  `market_rules_as_of`; currency-normalized conclusions missing `fx_as_of`.
- Saved A-share technical snapshots or technical thesis sections missing
  `technical_as_of`, `data_providers`, `adjustment`, `technical_engine`, or
  `data_quality_status`.
- `active` pages whose `review_after` date has passed.
- Current conclusions whose `as_of` is absent or stale.
- Inconsistent ticker formats or multiple aliases treated as separate securities.
- Financial or valuation numbers missing period, date, currency, units, or source.
- Market comparison that mixes fiscal periods, accounting standards,
  reporting or trading currencies, diluted shares, enterprise value, net debt,
  share classes, or ADR ratios without reconciliation.

## Evidence-integrity checks

- Paper, preprint, repository, patent, standard, model card, benchmark, product
  document, roadmap, or demo claim missing a material version, date, task,
  comparison boundary, or source type.
- Vendor benchmark, roadmap, product claim, or demo promoted to
  `verified_fact` without authoritative raw evidence and reproducible
  conditions.
- A paper treated as independent reproduction, a patent treated as a working
  product, or a standard treated as implementation or adoption.
- Benchmark comparisons that mix model, task, dataset, quality target,
  hardware, software, precision, workload, baseline, latency, throughput,
  power, or cost boundaries without normalization or disclosure.
- Research release treated as reproduction, prototype as pilot, pilot as
  production deployment, or production deployment as scaled adoption without
  evidence.
- Rumor, author opinion, management guidance, or Model assumption presented as `verified_fact`.
- Material assertions missing an evidence type or citation.
- Conflicting claims not retained or marked `disputed`.
- Certification treated as an order, order as delivery, delivery as revenue, or revenue as profit or cash flow without evidence.
- Missing invalidation conditions for material non-consensus views or Codex inferences.
- CZSC structure, moving-average interpretation, or technical position language
  presented as `verified_fact` instead of `codex_inference`.
- A technical conclusion marked usable despite `data_quality_status:
  disputed | unavailable`, or a fallback from BaoStock to AkShare not disclosed.

## Event checks

- Missing `event_type`, `event_status`, announcement date, expected date, or next review.
- Research, model, product, open-source, benchmark, standard, pilot,
  deployment, or adoption Event missing the current technical/commercial stage
  or the next evidence required for stage promotion when applicable.
- Pending Events whose milestone or `review_after` has passed.
- Completed, delayed, cancelled, or disputed Events still marked pending.
- Transaction, order, certification, earnings, or regulatory status not reconciled with newer evidence.

## Model checks

- Technology Model missing system boundary, benchmark normalization, observed
  versus assumed inputs, competing routes, scenarios, sensitivities, dated
  milestones, or invalidation.
- Commercialization or unit-economics Model missing customer, buyer/user/payer,
  adoption funnel, price/volume/utilization, value capture, competition,
  scenarios, sensitivities, or invalidation.
- TAM, SAM, or SOM treated as obtainable revenue without adoption, share,
  pricing, timing, or capacity assumptions.
- `model_assumption` without a source, period, units, or confidence.
- Reported facts, company guidance, source forecasts, and Codex assumptions mixed together.
- Missing conservative, base, or optimistic scenarios.
- Missing valuation or sensitivity analysis when the Model supports a valuation conclusion.
- Missing consolidation date, ownership percentage, minority interests, or attributable profit when relevant.
- Historical financials, cash flow, receivables, inventory, or capital expenditure inconsistent with the latest ingested report.
- Model not reconciled with the latest financial statements.

## Thesis and Entity Hub checks

- Trend thesis missing scope, technical state, competing routes, benchmark or
  reproduction boundary, drivers, bottlenecks, critical unknowns, scenarios,
  dated milestones, monitoring indicators, review date, or invalidation.
- Opportunity map collapsing technical benefit, customer benefit, value
  creation, value capture, company exposure, financial materiality, valuation,
  or current-price tradability.
- Company labeled a direct beneficiary without evidenced product, customer,
  deployment, order, delivery, revenue, or other explicit economic bridge.
- Technology attention, a single benchmark, supply-chain association, or a
  large TAM used as an automatic security recommendation.
- Investment thesis missing knowledge cutoff, catalysts, risks, monitoring indicators, or invalidation conditions.
- Superseded or failed thesis still marked active instead of `superseded` or `invalidated`.
- Current-price conclusion based on stale price or valuation.
- Industry attractiveness treated as equivalent to research priority or current-price tradability.
- A-share policy, price-limit, connect, settlement, or liquidity assumptions
  applied to a U.S. security, or U.S. options, short-interest, session, or
  liquidity assumptions applied to an A-share security without an explicit
  cross-market mechanism.
- Official policy existence and issuer-level financial effect collapsed into
  one `verified_fact`.
- An A-share week/month position view driven only by daily structure, or a
  current technical view missing monthly, weekly, and daily cutoffs.
- Listed-security Entity Hub missing coverage status for governance, segments, industry, products, customers, historical financials, Model, valuation, or thesis.
- Coverage marked complete despite missing, stale, conflicting, or rumor-only support.

## Report

Group findings:

- **Errors**: broken structure, false evidence promotion, material contradictions, invalid index entries, or unsafe current conclusions.
- **Warnings**: stale pages, missing metadata, unreconciled Models or Events, incomplete theses, or weak Entity coverage.
- **Info**: useful cross-links, optional consolidation, or research gaps.

For every finding include:

- what;
- severity;
- file and line;
- evidence;
- proposed fix;
- whether external verification or user judgment is required.

Finish with counts and ask which fixes the user approves. Do not invent missing facts and do not change files before approval.

## After approved fixes

Apply only the approved set. Preserve superseded or invalidated history. Update `wiki/index.md` where needed and append:

```markdown
## [YYYY-MM-DD] lint | Health check
Found N errors, N warnings, and N info items. Fixed: [...].
```

Report files changed, findings left unresolved, and any required re-verification.
