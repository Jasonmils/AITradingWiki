# AI Trading Wiki

[中文部署与使用指南](README.zh-CN.md)

AI Trading Wiki is a Codex-native, evidence-grounded vault for AI frontier-
technology learning, commercialization and industry-opportunity tracking, and
investment research, designed for browsing in Obsidian. It turns immutable
text, Markdown, and PDF sources plus locally staged MP4 videos into linked
Source, Entity, Concept, Event, Model, and Synthesis pages while preserving
provenance and evidence classes.

> Evidence → Object → Mechanism → Technology Maturity → Commercialization → Industry Value Pool → Company Exposure → Model → Investment Judgment

The repository includes all Codex skills, templates, integration scripts, and
tests required for document ingestion, video preprocessing, frontier-
technology research, opportunity mapping, wiki queries, quality audits, and
one-security equity research. Local source files, secrets, model weights,
caches, and generated video artifacts are intentionally excluded from Git.

![Second Brain Overview](docs/assets/second-brain-overview.png)

## Capabilities

| Workflow | Input or question | Entry point |
|---|---|---|
| Document ingest | Markdown, text, PDF, transcripts, research notes | `$second-brain-ingest` |
| Video ingest | MP4 with local ASR, PPT detection/OCR, diarization, and DeepSeek text refinement | `$second-brain-ingest` |
| Wiki query | Existing knowledge, claim comparison, or multi-security questions | `$second-brain-query` |
| Wiki audit | Links, metadata, stale claims, evidence classes, Events, Models, and Entity Hubs | `$second-brain-lint` |
| Frontier technology study | Mechanisms, competing routes, benchmarks, maturity, bottlenecks, and milestones | `$frontier-tech-research` |
| Technology-to-investment map | Commercialization, adoption, value pools, company exposure, and research priority | `$technology-to-investment` |
| Equity dossier | One listed security, scenarios, valuation, thesis, and current-price tradability | `$equity-research` |
| A-share research data | Current market, announcements, events, financials, consensus, IR Q&A, and news evidence candidates | `$a-share-research-data` |
| A-share technical audit | BaoStock/AkShare quality gates plus CZSC × chan.py monthly, weekly, and daily structure | `$a-share-technical-analysis` |
| Vault setup | Initialize or repair a compatible frontier-technology and investment-research vault | `$second-brain` |

Every delivered `$equity-research` run, including a partial or blocked one,
automatically archives its consolidated Markdown report under
`output/equity-research/`. The report is non-canonical; Entity, Event, Model,
thesis, monitoring, index, and log writes still require explicit curator
approval.

## Canonical Skill Names

Skill names are English-only. Use the canonical invocation exactly; do not
translate it or create aliases.

| Display name | Invocation |
|---|---|
| Second Brain Setup | `$second-brain` |
| Second Brain Ingest | `$second-brain-ingest` |
| Second Brain Query | `$second-brain-query` |
| Second Brain Lint | `$second-brain-lint` |
| Equity Research | `$equity-research` |
| A-Share Research Data | `$a-share-research-data` |
| A-Share Technical Analysis | `$a-share-technical-analysis` |
| Frontier Tech Research | `$frontier-tech-research` |
| Technology to Investment | `$technology-to-investment` |

## Deploy from Git

### 1. Clone and expose the Codex project skills

```bash
git clone https://github.com/Jasonmils/AITradingWiki.git
cd AITradingWiki
bash scripts/setup_codex.sh
```

Start a new Codex task from the repository root after setup. The script is
idempotent: it creates the local vault structure and relative links under
`.agents/skills/` without overwriting existing `raw/` or Wiki content.

Open the same folder as an Obsidian vault if you want local browsing, backlinks,
and graph view.

### 2. Optional: install the MP4 pipeline

Document and PDF ingestion needs no project API key. MP4 ingestion currently
uses the macOS Video2Skill_Invest integration and requires:

- macOS;
- Git;
- Python 3.11 or 3.12;
- an `HF_TOKEN` for the pyannote model;
- a `DEEPSEEK_API_KEY` for transcript refinement.

Install it with:

```bash
bash skills/second-brain-ingest/scripts/setup_video2skill.sh "$PWD"
```

The installer clones
[Video2Skill_Invest](https://github.com/Jasonmils/Video2Skill_Invest) into the
ignored `.work/tools/Video2Skill_Invest/` directory, installs its local
environment, and creates:

```text
.env.video-ingest.local
```

Fill the two empty values in that local file:

```dotenv
HF_TOKEN=
DEEPSEEK_API_KEY=
```

Never commit or paste these values into a prompt. The video workflow processes
the MP4, audio, and slide images locally. Only transcript text and relevant PPT
OCR text are sent to DeepSeek after explicit curator approval.

### 3. Optional: install the enhanced A-share analysis pipeline

The A-share research-data workflow does not require iWenCai or an API key. It
keeps provider failures separate from genuine empty results and treats
third-party event, financial, consensus, and news data as discovery or
cross-check evidence until the applicable official filing is verified.

Install the isolated technical environment and pinned public chan.py revision:

```bash
bash skills/a-share-technical-analysis/scripts/setup_env.sh
```

Example read-only runs:

```bash
python3 skills/a-share-research-data/scripts/research_snapshot.py \
  --ticker SSE:600519 --modules d1,d2,d3,d4

.work/venvs/a-share-ta/bin/python \
  skills/a-share-technical-analysis/scripts/technical_snapshot.py \
  --ticker SSE:600519
```

The research-data and technical reports are non-canonical artifacts under
`output/`. The technical workflow feeds the same normalized bars to CZSC and
chan.py, preserves provisional and withdrawn structures, and never converts a
BSP candidate into an automatic trade instruction. Each default technical run
also writes one summary audit PNG plus pinned chan.py strict-profile monthly,
weekly, and daily PNGs with candlesticks, Chan structures, neutral BSP markers,
and MACD. These static, non-interactive images are recorded with SHA-256 hashes
in the analysis manifest; `--no-native-chan-charts` keeps only the summary
image, while `--no-audit-chart` disables all images. Lifecycle state is updated
only from `complete` market data, after the analysis artifacts exist; the
matching `.state-commit.json` records the final commit result.

## Ingest Sources

Put local sources in `raw/`. They are ignored by Git by default. Documents and
attachments remain immutable; an MP4 remains immutable until its transcript,
coverage audit, Canonical Wiki write, and ingest log are complete.

### Markdown, text, PDF, transcripts, and notes

```text
$second-brain-ingest process raw/example-report.pdf.

Read the complete source, classify material claims, and show 3–5 takeaways,
evidence risks, and proposed Wiki writes. Wait for my approval before writing.
```

### MP4

```text
$second-brain-ingest process raw/example-course.mp4.

Run MP4 preflight first. I allow transcript text and relevant PPT OCR text to
be sent to DeepSeek; do not send the original video, audio, or slide images.

After Video2Skill finishes, audit timeline coverage, ASR coverage, OCR gaps,
and important unreadable slides. Use timeline.deepseek.html to show 3–5
takeaways, evidence risks, and proposed Wiki pages. Wait for my approval before
writing the Wiki.
```

MP4 ingestion initially keeps four provenance layers:

1. source MP4 in `raw/`;
2. authoritative `timeline.json`;
3. original ASR/OCR `timeline.html`;
4. DeepSeek-refined `timeline.deepseek.html`.

Generated video artifacts live under ignored `output/video-ingest/`. ASR, OCR,
speaker mapping, and LLM edits remain derived evidence and are never promoted
automatically to `verified_fact`.

After the Wiki write has been explicitly approved and completed, check whether
one exact video is eligible for storage finalization:

```bash
python3 skills/second-brain-ingest/scripts/finalize_video_ingest.py \
  output/video-ingest/manifests/example-0123456789ab.json \
  --vault-root "$PWD" \
  --source-page wiki/sources/example.md \
  --check-only
```

After confirming the reported MP4, Source page, hashes, retained HTML, and
reclaimable bytes, replace `--check-only` with
`--confirm-delete-source-video`. The finalizer retains `timeline.html`,
`timeline.deepseek.html`, and a small audit manifest; it deletes the exact MP4
and that video's heavyweight local processing job. Add `--keep-intermediates`
when resumable audio, frames, OCR, or timeline JSON must remain.

## Repository Layout

```text
AITradingWiki/
├── .agents/skills/              # Relative links discovered by Codex
├── skills/                      # Single editable source tree for nine skills
├── scripts/setup_codex.sh       # Idempotent project setup
├── config/                      # Secret-free configuration examples
├── templates/                   # Canonical Wiki page templates
├── raw/                         # Local source inbox; ignored by Git
├── output/                      # Local generated artifacts; ignored by Git
├── wiki/
│   ├── sources/
│   ├── entities/
│   ├── concepts/
│   ├── events/
│   ├── models/
│   ├── synthesis/
│   ├── index.md
│   └── log.md
├── tests/
├── AGENTS.md
└── README.zh-CN.md
```

## Update from an older version

Start from the AITradingWiki repository root. Check local work first; a normal
upgrade must not overwrite uncommitted research or code:

```bash
git status --short
git remote get-url origin

git pull --ff-only
bash scripts/setup_codex.sh
```

The expected `origin` is `https://github.com/Jasonmils/AITradingWiki.git`. If
`git status --short` prints anything, commit or back up those changes before
pulling. Do not use `git reset --hard` or `git checkout --` as an upgrade
shortcut. A rejected fast-forward means the histories need manual review.

If the MP4 pipeline is installed, update it only after the Vault update
completes:

```bash
git -C .work/tools/Video2Skill_Invest status --short
bash skills/second-brain-ingest/scripts/setup_video2skill.sh "$PWD" update
```

The Video2Skill updater requires a clean upstream checkout and uses a
fast-forward-only merge. It refreshes the embedded Python environment without
deleting `.env.video-ingest.local`, `raw/`, Wiki pages, model weights, video
caches, or completed reports. If the embedded status command prints anything,
preserve those changes first instead of forcing the update.

Confirm the upgraded installation:

```bash
bash tests/test_codex_compat.sh
bash tests/test_video_ingest.sh
git -C .work/tools/Video2Skill_Invest log -1 --oneline
.work/tools/Video2Skill_Invest/.venv/bin/python -m pip check
```

The current default refinement profile is cost-aware
`deepseek-v4-flash + Thinking=disabled`. Existing v2/v3 response caches remain
on disk but have a different cache identity; do not add `--refresh` merely to
finish an upgrade.

## Validate

```bash
bash tests/test_onboarding.sh
bash tests/test_codex_compat.sh
bash tests/test_a_share_research_data.sh
bash tests/test_a_share_technical_analysis.sh
bash tests/test_frontier_research.sh
bash tests/test_equity_research_report.sh
bash tests/test_skill_naming.sh
bash tests/test_video_ingest.sh
git diff --check
```

## Git and Data Boundary

Tracked:

- Codex skills and metadata;
- setup and video bridge scripts;
- configuration examples;
- templates and tests;
- canonical Wiki pages, index, and append-only log.

Local and ignored:

- `raw/` source documents, videos, and attachments;
- `.env*` secrets;
- `.work/` tools, virtual environments, model weights, and caches;
- `output/` generated reports and video artifacts.

Before publishing a fork, review canonical Wiki pages for licensed, private, or
personally identifying material. The default ignore rules protect raw files,
but they cannot classify prose that has already been written into the Wiki.

## Evidence Rules

Material claims use one of:

`verified_fact`, `company_statement`, `source_opinion`, `market_consensus`,
`non_consensus`, `market_rumor`, `model_assumption`, `codex_inference`, or
`disputed`.

Certification, orders, delivery, recognized revenue, profit, and cash flow are
separate milestones. Industry attractiveness, research priority, and
tradability at the current price are also separate conclusions.

Research publication, independent reproduction, prototype, pilot, production
deployment, scaled adoption, paid use, revenue, profit, and FCF are separate
milestones. A vendor benchmark, patent, roadmap, demo, large TAM, or thematic
association is not an automatic commercialization or security conclusion.

## Acknowledgements

- [NicholasSpisak/second-brain](https://github.com/NicholasSpisak/second-brain)
- [Jasonmils/Video2Skill_Invest](https://github.com/Jasonmils/Video2Skill_Invest)
- [simonlin1212/a-stock-data](https://github.com/simonlin1212/a-stock-data) — endpoint catalog and adapter research
- [Vespa314/chan.py](https://github.com/Vespa314/chan.py) — optional pinned Chan-structure audit engine
- [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Agent Skills open standard](https://agentskills.io)
