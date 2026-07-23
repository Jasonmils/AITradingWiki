---
name: second-brain-ingest
description: Process one or more immutable documents from raw/ into evidence-classified Source, Entity, Concept, Event, and Model wiki updates. Use when the user asks to ingest, import, process, or summarize raw files, earnings reports, transcripts, research notes, or all unprocessed sources, including "摄入资料", "处理 raw", or "摄入财报". Preserve originals and present 3–5 takeaways plus evidence risks before any wiki write. Do not use for ordinary wiki questions, audits, or a complete single-stock dossier.
---

# Second Brain — Ingest

Convert immutable raw evidence into selective, interlinked investment-research pages.

## Guardrails

- Never edit, rename, move, or delete anything in `raw/` or `raw/assets/`.
- Treat a file specified by the user as the source. Otherwise compare files directly under `raw/` with ingest entries in `wiki/log.md`; exclude `raw/assets/`.
- Read the source completely. Inspect referenced images only when they carry material evidence.
- Read `../second-brain/references/wiki-schema.md` before planning writes.
- Do not perform a complete security dossier or create a new trading recommendation. Route those requests to `$equity-research`.

## Phase 1: Evidence preview

Before changing the wiki:

1. Identify the source title, author or publisher, source type, publication date, covered period, and knowledge cutoff.
2. Resolve mentioned companies and securities to canonical exchange-prefixed tickers when evidence supports the mapping. Do not guess an identifier.
3. Separate historical facts from forecasts, guidance, opinion, rumor, and inference.
4. Classify material assertions as:
   - `verified_fact`
   - `company_statement`
   - `source_opinion`
   - `market_consensus`
   - `non_consensus`
   - `market_rumor`
   - `model_assumption`
   - `codex_inference`
   - `disputed`
5. Identify potential Entities, Concepts, Events, and Models.
6. Present 3–5 key takeaways plus evidence risks, conflicts, stale dates, and missing primary support.
7. List the pages that would be created or updated.
8. Wait for explicit user approval before writing.

## Phase 2: Selective writes

After approval, use the matching file from `../../templates/`.

### Source

Create one Source page that faithfully records what the source states. Include source metadata, material assertions, evidence classifications, `as_of`, and limitations. Do not add an independent investment conclusion.

### Entity and Concept

Update a canonical Entity or Concept when the source adds material, reusable information. Create a new page only when the object will likely be queried again or matters to an investment thesis. Avoid aliases and near-duplicates.

### Event

Create or update an Event for dated changes such as:

- earnings or guidance;
- formal orders or deliveries;
- technical certification;
- merger, control change, or asset injection;
- financing or regulatory action.

Record announcement, expected, and effective dates separately. Preserve the difference between announcement, completion, delivery, recognized revenue, profit, and cash flow.

### Model

Create or update a Model only when the source contains material forecast or valuation inputs. Put revenue, margin, expense, cash-flow, capital-expenditure, ownership, consolidation, earnings, valuation, scenario, or sensitivity assumptions here—not in Source facts.

Label every forecast input as reported fact, company guidance, source opinion, or `model_assumption`. Do not silently adopt a source author's forecast as the wiki's model.

## Cross-link and register

1. Link related pages with `[[Page Title]]`.
2. Preserve every number's period, date, currency, units, and source.
3. Preserve conflicting claims with attribution and mark disputed assertions.
4. Add concise entries to the correct `wiki/index.md` sections. Include ticker, page type, `as_of`, status, and description when applicable.
5. Append an ingest entry to `wiki/log.md`; never edit older entries.

Use this log form:

```markdown
## [YYYY-MM-DD] ingest | Source Title
Processed source-file. Created: [...]. Updated: [...]. Evidence risks: [...].
```

## Report

Return:

- source and knowledge cutoff;
- pages created and updated;
- evidence classification highlights;
- Events and Models created or changed;
- conflicts, rumors, stale information, and missing evidence;
- items deliberately not promoted into standalone pages.

Suggest `$second-brain-query`, `$equity-research`, or `$second-brain-lint` as the appropriate next workflow.
