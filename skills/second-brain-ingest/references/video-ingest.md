# MP4 video ingest

Use this reference only for an MP4 source.

## Data and evidence boundaries

- Keep the MP4 under `raw/` byte-for-byte. Never copy it into the upstream inbox or let an upstream archive step move it.
- Run the upstream single-file `production-run`, not `run_all.sh`.
- Local stages parse media, detect PPT changes, run OCR, transcribe speech, align speakers, and render the authoritative `timeline.json` plus original `timeline.html`.
- The refinement stage sends transcript text and relevant PPT OCR text to DeepSeek. It does not send the MP4, audio, or slide images.
- Require explicit curator approval before adding `--allow-remote-processing`.
- Treat ASR, OCR, speaker mapping, and DeepSeek edits as derived evidence. Never promote them automatically to `verified_fact`.
- Use `timeline.deepseek.html` for semantic ingestion, but retain links to the original MP4, authoritative `timeline.json`, and original `timeline.html` on the Source page.

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

1. immutable source MP4;
2. authoritative `timeline.json`;
3. original ASR/OCR `timeline.html`;
4. DeepSeek-refined `timeline.deepseek.html`.

Generated, non-canonical artifacts stay under `output/video-ingest/`. The manifest records the source SHA-256, derived HTML SHA-256, upstream Git revision, configurations, and artifact paths.

## Failure rule

Do not begin Wiki extraction when setup, preflight, local processing, DeepSeek refinement, artifact validation, or coverage review fails. Report the failed stage and preserve all cached checkpoints for a resumable retry.
