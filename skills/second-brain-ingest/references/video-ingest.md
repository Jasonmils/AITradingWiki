# MP4 video ingest

Use this reference only for an MP4 source.

## Data and evidence boundaries

- Keep the MP4 under `raw/` byte-for-byte through conversion, review, and the
  Canonical Wiki write. Never copy it into the upstream inbox or let an
  upstream archive step move it.
- Run the upstream single-file `production-run`, not `run_all.sh`.
- Local stages parse media, detect PPT changes, run OCR, transcribe speech, align speakers, and render the authoritative `timeline.json` plus original `timeline.html`.
- The refinement stage sends transcript text and relevant PPT OCR text to DeepSeek. It does not send the MP4, audio, or slide images.
- In the quality-checked Apple Silicon accelerated path, audio/diarization may
  overlap visual work. After general OCR is stable and aligned ASR finishes,
  DeepSeek response prefetch may overlap table/chart structure OCR. Raw,
  unaligned ASR is never sent early because its segment boundaries and IDs are
  not yet authoritative.
- Derived HTML and DeepSeek input group adjacent ASR fragments only when the
  speaker, visual context, pause, duration, character count, and part-count
  gates remain safe. Every original utterance, source segment, and word
  timestamp stays unchanged in `timeline.json`.
- Derived transcript/OCR display plus DeepSeek input and output are normalized
  to Simplified Chinese with OpenCC `t2s`; authoritative raw ASR/OCR JSON
  remains unchanged for audit.
- The default refinement profile is cost-aware:
  `deepseek-v4-flash`, non-thinking mode, a compact optional-field response
  schema, and a bounded output allowance. Use the upstream explicit quality
  profile only for selected high-risk review; do not make V4-Pro
  Thinking=max the batch default.
- Require `metadata/performance.json` and
  `metadata/refinement_prefetch.json` when the upstream result advertises
  those artifacts. A completed prefetch must report
  `input_matches_final=true`; a failed prefetch may be retried only from the
  authoritative final timeline.
- Audit `provider_details`, `successful_remote_usage`, and `request_metrics`
  when present. These distinguish local response-cache reuse from successful
  remote work. Provider billing remains authoritative because a response
  completed remotely but lost during transport can still be charged.
- Require explicit curator approval before adding `--allow-remote-processing`.
- Treat ASR, OCR, speaker mapping, and DeepSeek edits as derived evidence. Never promote them automatically to `verified_fact`.
- Use `timeline.deepseek.html` for semantic ingestion. Record links to the
  original MP4, authoritative `timeline.json`, and both HTML files on the Source
  page before any storage finalization.

## One-time setup

From the vault root:

```bash
bash skills/second-brain-ingest/scripts/setup_video2skill.sh "$PWD"
```

This installs the upstream checkout under `.work/tools/Video2Skill_Invest` and creates the ignored local file `.env.video-ingest.local`. Fill:

```dotenv
HF_TOKEN=
DEEPSEEK_API_KEY=
```

Do not print, commit, or paste either value into a prompt.

To align an existing clean checkout with the latest upstream `main` and refresh
its Python dependencies:

```bash
bash skills/second-brain-ingest/scripts/setup_video2skill.sh "$PWD" update
```

The updater refuses a modified upstream checkout and uses a fast-forward-only
merge. It never resets or overwrites local changes.

## Preflight and conversion

Run preflight without remote processing:

```bash
python3 skills/second-brain-ingest/scripts/video_to_html.py \
  raw/example.mp4 \
  --vault-root "$PWD" \
  --preflight-only
```

After the curator explicitly approves sending derived text to DeepSeek:

```bash
python3 skills/second-brain-ingest/scripts/video_to_html.py \
  raw/example.mp4 \
  --vault-root "$PWD" \
  --allow-remote-processing
```

On Apple Silicon, add `--accelerated` only if the upstream accelerated ASR configuration has been quality-checked on representative Chinese investment content.

The command returns JSON. Continue Phase 1 using `ingest_input_html`. Record the manifest path and all four evidence layers on the proposed Source page:

1. source MP4, immutable until post-Wiki finalization;
2. authoritative `timeline.json`;
3. original ASR/OCR `timeline.html`;
4. DeepSeek-refined `timeline.deepseek.html`.

Generated, non-canonical artifacts stay under `output/video-ingest/`. The manifest records the source SHA-256, derived HTML SHA-256, upstream Git revision, configurations, and artifact paths.

Changing provider, model, prompt protocol, thinking mode, or output limit
creates a new response-cache identity. Existing v2/v3 cache files remain
untouched, but they do not satisfy the cost-aware v4 request. Never add
`--force` or `--refresh` merely to adopt the new default for an already
complete report.

## Post-Wiki storage finalization

Rendering is not enough to delete a video. First finish the coverage audit,
obtain approval for the Canonical Wiki write, create/update the Source page, and
append the ingest entry to `wiki/log.md`.

Check one exact completed ingest without deleting:

```bash
python3 skills/second-brain-ingest/scripts/finalize_video_ingest.py \
  output/video-ingest/manifests/example-0123456789ab.json \
  --vault-root "$PWD" \
  --source-page wiki/sources/example.md \
  --check-only
```

The check must report `status=eligible`, the exact source path and SHA-256, both
retained HTML paths, and estimated reclaimable bytes. After the curator
explicitly confirms this exact cleanup:

```bash
python3 skills/second-brain-ingest/scripts/finalize_video_ingest.py \
  output/video-ingest/manifests/example-0123456789ab.json \
  --vault-root "$PWD" \
  --source-page wiki/sources/example.md \
  --confirm-delete-source-video
```

The finalizer copies `timeline.html` and `timeline.deepseek.html` into
`output/video-ingest/transcripts/<video>-<sha12>/`, verifies their hashes,
deletes the exact MP4, and removes that video's production job. It preserves the
small manifest as the cleanup receipt, updates the Source page with storage
status and retained paths, and appends `wiki/log.md`.

Add `--keep-intermediates` only when resumable audio, frames, OCR, timeline JSON,
or other processing checkpoints must remain. Non-video raw files and
`raw/assets/` are never eligible for this cleanup.

## Failure rule

Do not begin Wiki extraction when setup, preflight, local processing, DeepSeek refinement, artifact validation, or coverage review fails. Report the failed stage and preserve all cached checkpoints for a resumable retry. Do not run storage finalization when the completed manifest, Source provenance, ingest log, or curator confirmation is missing.
