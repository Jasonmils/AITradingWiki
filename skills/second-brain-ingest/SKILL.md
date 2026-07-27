---
name: second-brain-ingest
description: Process documents or MP4 videos from raw/ into evidence-classified Source, Entity, Concept, Event, and Model wiki updates. Use when the user asks to ingest, import, process, transcribe, summarize, or finalize storage for raw files, videos, earnings reports, transcripts, research notes, or all unprocessed sources, including "摄入资料", "处理 raw", "摄入财报", "处理视频", "摄入 MP4", or "视频转成 Wiki 后删除源文件". For MP4, run Video2Skill_Invest to produce a DeepSeek-refined HTML before normal ingestion, preserve the video through the Wiki approval gate, and delete it only through audited finalization after explicit curator confirmation. Present 3–5 takeaways plus evidence risks before any wiki write. Do not use for ordinary wiki questions, audits, or a complete single-stock dossier.
---

# Second Brain — Ingest

Convert raw evidence into selective, interlinked investment-research pages.

## Guardrails

- Never edit, rename, move, or delete non-video files in `raw/` or anything in
  `raw/assets/`.
- Keep an MP4 byte-for-byte through preprocessing, evidence review, and the
  Canonical Wiki write. Delete it only with
  `scripts/finalize_video_ingest.py` after the curator explicitly confirms
  storage finalization.
- Treat a file specified by the user as the source. Otherwise compare files directly under `raw/` with ingest entries in `wiki/log.md`; exclude `raw/assets/`.
- Read the source completely. Inspect referenced images only when they carry material evidence.
- Read `../second-brain/references/wiki-schema.md` before planning writes.
- Do not perform a complete security dossier or create a new trading recommendation. Route those requests to `$equity-research`.

## MP4 preprocessing

For an `.mp4` source, read `references/video-ingest.md` and follow it before Phase 1:

1. Keep the original MP4 unchanged under `raw/` until the post-Wiki storage
   finalization gate.
2. Run the bundled bridge preflight. If the upstream checkout or dependencies are missing, propose the one-time setup command; installation may download code, packages, and model weights, so obtain approval before running it.
3. Explain that local stages process the media, while DeepSeek receives transcript text and relevant PPT OCR text only. Wait for explicit approval before remote processing.
4. Run the bridge with `--allow-remote-processing` only after approval.
5. Require non-empty `timeline.json`, original `timeline.html`, refined `timeline.deepseek.html`, and the bridge manifest. Audit transcript/OCR coverage and important unreadable slides before extracting claims.
6. Use the manifest's `ingest_input_html` as the Phase 1 reading source. Preserve provenance to every evidence layer and classify ASR/OCR/LLM-derived assertions conservatively.
7. Do not delete the MP4 merely because rendering succeeded. Complete Phase 1,
   obtain Wiki-write approval, finish Phase 2, and register the ingest first.

Do not start Phase 1 or write the Wiki if conversion, refinement, artifact validation, or coverage review fails.

## Phase 1: Evidence preview

Before changing the wiki:

1. Identify the source title, author or publisher, source type, publication date, covered period, and knowledge cutoff. For video, also record duration, source SHA-256, upstream revision, original transcript path, refined HTML path, and known ASR/OCR gaps.
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

## MP4 storage finalization

After Phase 2, read `references/video-ingest.md` and use the bundled finalizer.

1. Run `--check-only` against the completed bridge manifest and Canonical Source
   page.
2. Require all checks to pass: exact MP4 SHA-256, completed manifest, nonempty
   original/refined HTML, Source-page provenance, and an ingest entry in
   `wiki/log.md`.
3. Show the exact MP4, retained HTML paths, processing directory, and estimated
   reclaimed bytes. Obtain explicit curator confirmation if it was not already
   given for this exact cleanup.
4. Run `--confirm-delete-source-video`. By default the command archives the
   original and DeepSeek-refined transcript HTML, deletes the exact source MP4,
   removes the heavyweight production job, updates the Source page and manifest,
   and appends a maintenance log entry.
5. Use `--keep-intermediates` only when the curator wants to retain local audio,
   frames, OCR, timeline JSON, and other resumable checkpoints.
6. Never substitute a guessed path, glob, broad directory, or manually issued
   recursive deletion for the finalizer.

## Report

Return:

- source and knowledge cutoff;
- pages created and updated;
- evidence classification highlights;
- Events and Models created or changed;
- conflicts, rumors, stale information, and missing evidence;
- items deliberately not promoted into standalone pages.
- MP4 storage status, retained transcript paths, and reclaimed space when
  finalization was executed.

Suggest `$second-brain-query`, `$equity-research`, or `$second-brain-lint` as the appropriate next workflow.
