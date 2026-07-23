---
name: equity-research
description: Build or update an evidence-grounded research dossier for one publicly traded security. Use for a deep dive, initiate coverage, "建立研究档案", "更新投资论点/模型", or whether one stock is worth buying, initiating, adding, holding, reducing, or avoiding now. Work wiki-first, re-verify current facts, and cover gaps, company and governance, business and industry, three-scenario modeling, valuation and sensitivity, thesis, catalysts, risks, invalidation, monitoring, and current-price tradability. Ask before saving. Do not use for multi-stock comparisons, raw ingestion, or wiki audits.
---

# Equity Research

Build or update one listed security's evidence-grounded research dossier.

## Boundaries

- Handle one publicly traded security per invocation.
- Route multi-security comparisons to `$second-brain-query`, raw sources to `$second-brain-ingest`, and full-wiki audits to `$second-brain-lint`.
- Read the wiki first. Never modify `raw/`.
- Do not guess a company-to-ticker mapping.
- Do not hard-code or assume any security conclusion.
- Deliver the research and a proposed write plan before asking permission to save.

Read `../second-brain/references/wiki-schema.md` before evaluating evidence or creating pages. Read the relevant file in `../../templates/` only when preparing a write.

## 1. Resolve scope

Identify:

- legal company or issuer;
- canonical exchange-prefixed ticker;
- market and asset class;
- requested investment horizon;
- knowledge cutoff and current date;
- whether the task initiates coverage, refreshes a dossier, updates a Model or thesis, or evaluates a current position decision.

Clarify ambiguous securities or time horizons when they would materially change the analysis.

## 2. Audit existing coverage

Read `wiki/index.md`, locate the security Entity Hub, and follow linked Sources, Concepts, Events, Models, Syntheses, and Monitoring pages.

Classify each research module as `complete`, `partial`, `unverified`, `provisional`, or `stale`. Report:

- missing evidence;
- stale `as_of` or passed `review_after`;
- conflicting claims;
- rumor-only support;
- missing primary sources;
- Model or thesis not reconciled with newer Events.

Do not fill a gap with speculation.

## 3. Build the evidence map

Retrieve in this order:

1. Source;
2. Entity and Concept;
3. Event;
4. Model;
5. Synthesis.

Classify material assertions as `verified_fact`, `company_statement`, `source_opinion`, `market_consensus`, `non_consensus`, `market_rumor`, `model_assumption`, `codex_inference`, or `disputed`.

Keep supply-chain entry, certification, formal order, delivery, revenue, profit, and cash flow as separate milestones unless each link is evidenced.

## 4. Re-verify current facts

Re-check current price, latest earnings and guidance, material orders or certifications, transaction progress, ownership, management, regulation, litigation, and other current facts whenever they affect the conclusion.

Prefer primary sources. Record publication date, reporting period, retrieval date, currency, units, and source. Keep newly verified external facts separate from existing wiki knowledge. If verification is unavailable, mark the affected conclusion incomplete.

## 5. Analyze the security

Cover, as evidence permits:

- company and listed security;
- ownership, control, governance, and related-party issues;
- legacy and new business segments;
- industry size, structure, competition, and mechanism;
- products, technology routes, certifications, customers, suppliers, and value-chain position;
- historical revenue, profit, margins, cash flow, receivables, inventory, capital expenditure, and segment data;
- management guidance and source forecasts, clearly classified.

## 6. Build or reconcile the Model

Use conservative, base, and optimistic scenarios. Explicitly separate reported facts, company guidance, source opinion, and `model_assumption`.

When applicable, model:

- segment volume, price, revenue, and gross margin;
- research and development, selling, and administrative expenses;
- operating cash flow, working capital, and capital expenditure;
- consolidation date and listed-company ownership percentage;
- minority interests and attributable net profit;
- shares, earnings per share, net cash, and net debt;
- comparable companies, valuation multiples, and sensitivity.

Reconcile against the latest reported results. Mark unresolved Models `provisional` or `stale`.

## 7. Form the investment view

Separate:

- verified facts;
- company or source statements;
- market consensus;
- non-consensus view;
- rumors and disputed claims;
- Codex inference.

Develop bull, base, and bear scenarios. State:

- core debate;
- catalysts and expected timing;
- principal risks;
- thesis invalidation conditions;
- monitoring indicators and next verification date;
- evidence gaps and conflicts.

Answer separately:

1. Is the industry attractive?
2. Is the security a priority for further research?
3. Is it tradable at the current price and horizon?

Do not give a current-price conclusion without current verification.

## 8. Deliver before saving

Present:

1. resolved security, horizon, and knowledge cutoff;
2. research coverage table;
3. evidence map and conflicts;
4. company, governance, business, industry, product, customer, and supplier analysis;
5. financial quality and three-scenario Model;
6. valuation and sensitivity;
7. thesis, catalysts, risks, invalidation, and monitoring;
8. current-price tradability;
9. missing evidence and next research actions;
10. exact pages proposed for creation or update.

Ask the user to approve, reject, or narrow the proposed writes.

## 9. Save after approval

Apply only the approved changes:

- create or update the Entity Hub and research-coverage table;
- create or update material Event pages;
- create or update the Model;
- create or update the investment-thesis and monitoring Syntheses;
- preserve and mark replaced pages `superseded` or `invalidated`;
- update `wiki/index.md`, including Active Theses and Monitoring;
- append an `equity-research` entry to `wiki/log.md`.

Report every page changed, the final `as_of` and `review_after`, unresolved gaps, and the next verification date.
