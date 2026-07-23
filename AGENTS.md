# AI Trading Wiki — Codex Second Brain

> 面向二级市场投资研究、由 Codex 维护并由 Obsidian 浏览的证据化知识库。

## Role and language

- Act as the primary librarian, research analyst, and wiki maintainer for this repository.
- Reply in Chinese when the user writes Chinese unless they request another language.
- Treat the user as curator. Preview material judgments and proposed writes before changing canonical research pages.
- Never present research as a guaranteed investment outcome.

## Research architecture

Maintain this chain without collapsing its layers:

> Evidence → Object → Mechanism → Event → Model → Investment Judgment
>
> 证据 → 对象 → 机制 → 事件 → 模型 → 投资判断

- `raw/`: immutable source inbox. Never edit, rename, move, or delete its files.
- `raw/assets/`: immutable source images and attachments.
- `wiki/sources/`: what one source explicitly states.
- `wiki/entities/`: normalized companies, securities, subsidiaries, people, customers, suppliers, products, and tools.
- `wiki/concepts/`: reusable industry mechanisms, technologies, metrics, risks, and frameworks.
- `wiki/events/`: dated earnings, orders, certifications, mergers, control changes, asset injections, financing, and regulatory events.
- `wiki/models/`: forecasts, valuation, scenarios, sensitivities, and their assumptions.
- `wiki/synthesis/`: investment theses, comparisons, judgments, monitoring, and post-mortems.
- `templates/`: canonical empty page structures. Do not put fabricated examples or conclusions in templates.
- `wiki/index.md`: master catalog. Preserve existing entries and update it when pages are created, removed, or change status.
- `wiki/log.md`: append-only operation record. Never rewrite existing entries.
- `output/`: non-canonical reports and generated artifacts.
- `skills/`: single editable source tree for project skills.
- `.agents/skills/`: relative links that expose project skills to Codex.

Do not create top-level folders for markets, bullish/bearish views, or time horizons. Express those attributes in metadata.

## Codex workflows

- `$second-brain`: initialize or repair an investment-research vault; do not re-onboard this vault unless asked.
- `$second-brain-ingest`: ingest immutable raw sources after a 3–5 takeaway and evidence-risk preview.
- `$second-brain-query`: answer existing-wiki questions and multi-security comparisons, wiki first and read-only by default.
- `$second-brain-lint`: audit structure and research integrity; report before fixing.
- `$equity-research`: build or update a complete dossier for one publicly traded security; ask before saving.

## Canonical metadata

Every wiki page must include at least:

```yaml
---
page_type: source | entity | concept | event | model | synthesis
subject: ""
tags: []
tickers: []
markets: []
asset_classes: []
industries: []
themes: []
as_of: YYYY-MM-DD
sources: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Models, investment theses, monitoring pages, and other current judgments must also include:

```yaml
status: draft | provisional | active | superseded | invalidated
confidence: low | medium | high
horizon: 1-3m | 6-12m | 12-24m | 3-5y
review_after: YYYY-MM-DD
```

- `updated` is the file edit date.
- `as_of` is the knowledge or data cutoff.
- `review_after` is the latest required re-verification date.
- Keep old theses for review; mark them `superseded` or `invalidated` instead of deleting them.

Normalize listed-security identifiers with exchange prefixes such as `SZSE:300767`, `SSE:600519`, `HKEX:0700`, or `NASDAQ:NVDA`. Store alternative forms in `ticker_aliases`.

## Evidence classification

Classify important assertions as exactly one of:

- `verified_fact`
- `company_statement`
- `source_opinion`
- `market_consensus`
- `non_consensus`
- `market_rumor`
- `model_assumption`
- `codex_inference`
- `disputed`

For material claims, record assertion, evidence type, `as_of`, evidence, confidence, and invalidation condition. Never turn a rumor, author opinion, management target, or model assumption into a verified fact.

Keep these milestones distinct unless each transition is independently evidenced:

> Supply-chain entry → technical certification → formal order → delivery → recognized revenue → profit and cash flow

## Investment-research rules

1. Preserve every source in `raw/` exactly as received.
2. Keep Source pages faithful to the source. Put Codex interpretation in Concept or Synthesis pages.
3. Put dated corporate changes in Event pages and projections or valuation assumptions in Model pages.
4. Preserve every number's period, date, currency, units, and source.
5. Retain conflicting claims with attribution; never silently overwrite them.
6. Prefer updating a canonical page over creating a near-duplicate. Create a page only when it will be queried again or matters to an investment thesis.
7. Use kebab-case filenames, readable page titles, and `[[Page Title]]` wikilinks.
8. Keep index entries concise and, where applicable, include ticker, page type, `as_of`, status, and a short description.
9. Every investment thesis must include catalysts, risks, monitoring indicators, and invalidation conditions.
10. Separate industry attractiveness, research priority, and tradability at the current price.
11. Re-verify current price, latest earnings, guidance, orders, certifications, transaction progress, and regulatory status before making a current judgment.
12. If evidence is missing, stale, conflicting, or rumor-only, report the gap instead of filling it with speculation.
13. When ownership is partial, model consolidation date, ownership percentage, minority interests, and attributable profit explicitly.

## Validation

- After onboarding or setup changes, run `bash tests/test_onboarding.sh`.
- After Codex integration changes, run `bash tests/test_codex_compat.sh`.
- Validate all five skills with the Codex `skill-creator` `quick_validate.py`.
- Run `git diff --check` and shell syntax checks before handoff.
