---
name: second-brain-query
description: Answer questions from the existing wiki first with [[wikilink]] citations, evidence labels, as_of dates, conflicts, gaps, and current-data verification when needed. Use for factual questions, exploring connections, asking "我的知识库里…", reviewing an existing view, or comparing multiple securities or claims. Default to read-only. Use equity-research for a complete one-security dossier, thesis or model update, or current position decision; use second-brain-ingest for raw documents.
---

# Second Brain — Query

Answer from the existing knowledge base before using raw evidence or external research.

## Route the request

- Use this skill for wiki questions, connection exploration, existing-view summaries, and multi-security comparisons.
- Route one-security initiation, a full dossier, thesis or model updates, and "buy or build a position now" decisions to `$equity-research`.
- Route new raw documents to `$second-brain-ingest`.
- Remain read-only unless the user later approves saving a synthesis.

## Parse the question

Identify:

- company or subject;
- canonical ticker and market, if applicable;
- requested investment horizon;
- requested comparison dimensions;
- whether the answer depends on current price or current facts.

Do not guess an ambiguous company or ticker. Ask for resolution when it materially changes the answer.

## Search sequence

1. Read `wiki/index.md`, including Sources, Entities, Concepts, Events, Models, Synthesis, Active Theses, and Monitoring.
2. Find the security Entity Hub and inspect its research-coverage table.
3. Flag missing, partial, unverified, stale, conflicting, and rumor-only modules.
4. Retrieve evidence in this order:
   - Source;
   - Entity and Concept;
   - Event;
   - Model;
   - Synthesis.
5. Follow relevant `[[wikilinks]]`.
6. Use `qmd search "<terms>" --path wiki/` when `qmd` is available and the index is insufficient.
7. Read files in `raw/` only as a last resort, and never modify them.

Read `../second-brain/references/wiki-schema.md` when evaluating evidence classifications, currentness, Models, or investment theses.

## Currentness gate

State the wiki knowledge cutoff. Re-verify time-sensitive claims when the question depends on:

- current price or valuation;
- latest earnings, guidance, or financial statements;
- current orders, certification, delivery, or transaction progress;
- current ownership, regulation, litigation, or management;
- whether a security is tradable at the current price.

Prefer primary sources and record publication date, covered period, currency, units, and retrieval date. Keep external current facts separate from wiki facts. If current verification is unavailable, state that a current-price conclusion cannot be completed.

## Synthesize

Separate:

- `verified_fact`;
- `company_statement`;
- `source_opinion`;
- `market_consensus`;
- `non_consensus`;
- `market_rumor`;
- `model_assumption`;
- `codex_inference`;
- `disputed`.

For company or security questions, cover only the dimensions supported by evidence:

- company, security, ownership, and governance;
- business segments and growth drivers;
- industry structure and competition;
- product, technology, customers, suppliers, and value-chain position;
- historical financials, cash flow, receivables, inventory, and capital expenditure;
- Models, valuation, and sensitivity;
- catalysts, risks, monitoring indicators, and invalidation conditions.

Distinguish industry attractiveness, research priority, and tradability at the current price.

## Answer contract

Include:

1. Direct answer and knowledge cutoff.
2. Wiki pages actually used, cited as `[[Page Title]]`.
3. Evidence-classified findings.
4. Conflicts, stale information, and rumor-only claims.
5. Research coverage and missing data.
6. Current external verification, when required.
7. Codex inference and its assumptions.
8. Catalysts, risks, monitoring indicators, and invalidation conditions when relevant.

Do not fill gaps with speculation.

## Optional save

If the answer creates a durable comparison or synthesis:

1. propose a target page and show what would be saved;
2. wait for user approval;
3. use the appropriate template in `../../templates/`;
4. save under `wiki/synthesis/`;
5. update `wiki/index.md`;
6. append a query entry to `wiki/log.md`.

Never convert a read-only query into a write without approval.
