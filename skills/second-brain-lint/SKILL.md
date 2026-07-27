---
name: second-brain-lint
description: Audit wiki structure and investment-research integrity, including links, orphans, index drift, required metadata, review dates, evidence classification, ticker and numeric consistency, Event status, Model reconciliation, thesis completeness, and Entity Hub coverage. Use when the user asks to lint, audit, health-check, inspect stale claims, find problems, or "检查知识库". Report severity, file and line evidence, and a proposed fix before changing anything; apply fixes only after approval.
---

# Second Brain — Lint

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
- Models, theses, monitoring, or current judgments missing `status`, `confidence`, `horizon`, or `review_after`.
- `active` pages whose `review_after` date has passed.
- Current conclusions whose `as_of` is absent or stale.
- Inconsistent ticker formats or multiple aliases treated as separate securities.
- Financial or valuation numbers missing period, date, currency, units, or source.

## Evidence-integrity checks

- Rumor, author opinion, management guidance, or Model assumption presented as `verified_fact`.
- Material assertions missing an evidence type or citation.
- Conflicting claims not retained or marked `disputed`.
- Certification treated as an order, order as delivery, delivery as revenue, or revenue as profit or cash flow without evidence.
- Missing invalidation conditions for material non-consensus views or Codex inferences.

## Event checks

- Missing `event_type`, `event_status`, announcement date, expected date, or next review.
- Pending Events whose milestone or `review_after` has passed.
- Completed, delayed, cancelled, or disputed Events still marked pending.
- Transaction, order, certification, earnings, or regulatory status not reconciled with newer evidence.

## Model checks

- `model_assumption` without a source, period, units, or confidence.
- Reported facts, company guidance, source forecasts, and Codex assumptions mixed together.
- Missing conservative, base, or optimistic scenarios.
- Missing valuation or sensitivity analysis when the Model supports a valuation conclusion.
- Missing consolidation date, ownership percentage, minority interests, or attributable profit when relevant.
- Historical financials, cash flow, receivables, inventory, or capital expenditure inconsistent with the latest ingested report.
- Model not reconciled with the latest financial statements.

## Thesis and Entity Hub checks

- Investment thesis missing knowledge cutoff, catalysts, risks, monitoring indicators, or invalidation conditions.
- Superseded or failed thesis still marked active instead of `superseded` or `invalidated`.
- Current-price conclusion based on stale price or valuation.
- Industry attractiveness treated as equivalent to research priority or current-price tradability.
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
