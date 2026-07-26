# AI Trading Wiki

[中文部署与使用指南](README.zh-CN.md)

AI Trading Wiki is a Codex-native, evidence-grounded investment-research vault
designed for browsing in Obsidian. It turns immutable text, Markdown, PDF, and
MP4 sources into linked Source, Entity, Concept, Event, Model, and Synthesis
pages while preserving provenance and evidence classes.

> Evidence → Object → Mechanism → Event → Model → Investment Judgment

The repository includes all Codex skills, templates, integration scripts, and
tests required for document ingestion, video preprocessing, wiki queries,
quality audits, and one-security equity research. Local source files, secrets,
model weights, caches, and generated video artifacts are intentionally excluded
from Git.

![Second Brain Overview](docs/assets/second-brain-overview.png)

## Capabilities

| Workflow | Input or question | Entry point |
|---|---|---|
| Document ingest | Markdown, text, PDF, transcripts, research notes | `$second-brain-ingest` |
| Video ingest | MP4 with local ASR, PPT detection/OCR, diarization, and DeepSeek text refinement | `$second-brain-ingest` |
| Wiki query | Existing knowledge, claim comparison, or multi-security questions | `$second-brain-query` |
| Wiki audit | Links, metadata, stale claims, evidence classes, Events, Models, and Entity Hubs | `$second-brain-lint` |
| Equity dossier | One listed security, scenarios, valuation, thesis, and current-price tradability | `$equity-research` |
| Vault setup | Initialize or repair a compatible investment-research vault | `$second-brain` |

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

## Ingest Sources

Put local sources in `raw/`. They are immutable evidence and ignored by Git by
default.

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

MP4 ingestion keeps four provenance layers:

1. immutable source MP4 in `raw/`;
2. authoritative `timeline.json`;
3. original ASR/OCR `timeline.html`;
4. DeepSeek-refined `timeline.deepseek.html`.

Generated video artifacts live under ignored `output/video-ingest/`. ASR, OCR,
speaker mapping, and LLM edits remain derived evidence and are never promoted
automatically to `verified_fact`.

## Repository Layout

```text
AITradingWiki/
├── .agents/skills/              # Relative links discovered by Codex
├── skills/                      # Single editable source tree for five skills
├── scripts/setup_codex.sh       # Idempotent project setup
├── config/                      # Secret-free configuration examples
├── templates/                   # Canonical Wiki page templates
├── raw/                         # Local immutable evidence; ignored by Git
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

## Update

```bash
git pull --ff-only
bash scripts/setup_codex.sh
```

If the MP4 pipeline is installed:

```bash
bash skills/second-brain-ingest/scripts/setup_video2skill.sh "$PWD" update
```

The Video2Skill updater requires a clean upstream checkout and uses a
fast-forward-only merge. It does not reset or overwrite local vault data.

## Validate

```bash
bash tests/test_onboarding.sh
bash tests/test_codex_compat.sh
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

## Acknowledgements

- [NicholasSpisak/second-brain](https://github.com/NicholasSpisak/second-brain)
- [Jasonmils/Video2Skill_Invest](https://github.com/Jasonmils/Video2Skill_Invest)
- [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Agent Skills open standard](https://agentskills.io)
