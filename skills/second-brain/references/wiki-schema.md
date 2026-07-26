# AI Trading Wiki Schema

This is the canonical schema for the investment-research vault. Apply it when creating, updating, querying, or auditing wiki pages.

## Contents

1. Architecture
2. Language conventions
3. Canonical metadata
4. Evidence classification
5. Page responsibilities
6. Entity Hub and research coverage
7. Event rules
8. Model rules
9. Investment thesis rules
10. Index and log
11. Staleness, conflicts, and invalidation

## Architecture

Maintain the research chain:

> Evidence → Object → Mechanism → Event → Model → Investment Judgment

- `raw/`: immutable source documents. Read but never edit, move, rename, or delete them.
- `raw/assets/`: immutable images and attachments referenced by sources.
- `wiki/sources/`: factual summaries of individual sources.
- `wiki/entities/`: normalized companies, securities, subsidiaries, people, customers, suppliers, products, and tools.
- `wiki/concepts/`: reusable mechanisms, technologies, metrics, risks, and frameworks.
- `wiki/events/`: dated changes such as earnings, orders, certifications, mergers, control changes, asset injections, financing, and regulation.
- `wiki/models/`: forecasts, valuation, scenarios, sensitivities, and explicit assumptions.
- `wiki/synthesis/`: theses, comparisons, judgments, monitoring, and post-mortems.
- `templates/`: empty canonical page structures.
- `output/`: non-canonical reports and generated artifacts.

Do not organize top-level directories by market, asset view, or horizon. Represent those attributes in metadata.

## Language conventions

- Canonical Wiki page titles, headings, prose, table headers, index descriptions, and newly appended log entries should be written primarily in Chinese unless the curator requests another language.
- Retain English for legal company names, tickers and exchange-prefixed identifiers, official product/source titles, metadata keys and enums, evidence labels, units, acronyms, and domain-specific terms whose English form is more precise or commonly queried.
- Common retained terms include CPO, OCS, ASIC, XPU, DSP, FAU, ELS, BoM, TAM, EPS, NPO, SiPh, EML, CW laser, MOCVD, scale-up, scale-out and scale-across. Add a concise Chinese explanation at first use when useful.
- Do not force-translate an English proper noun or technical term when that would introduce ambiguity. Preserve exact source wording when the wording is itself material evidence.
- Translation must preserve every number, date, period, currency, unit, source, attribution, confidence, invalidation condition and evidence type. Never upgrade or downgrade evidence because of translation.
- Keep kebab-case filenames and machine-readable frontmatter stable. Use Chinese readable titles and Chinese display text in `[[target|中文标题]]` wikilinks.

## Canonical metadata

Every wiki page must include:

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

Use `ticker_aliases: []` when a security has common alternative identifiers. Normalize primary tickers with an exchange prefix, for example:

```text
SZSE:300767
SSE:600519
HKEX:0700
NASDAQ:NVDA
```

Models, investment theses, monitoring pages, and other current judgments also require:

```yaml
status: draft | provisional | active | superseded | invalidated
confidence: low | medium | high
horizon: 1-3m | 6-12m | 12-24m | 3-5y
review_after: YYYY-MM-DD
```

- `updated`: last file edit date.
- `as_of`: date through which the data or judgment is valid.
- `review_after`: latest date by which re-verification is required.
- `status`: lifecycle of the model or judgment.

Preserve the date, reporting period, currency, units, and source for every financial or valuation number.

## Evidence classification

Classify each material assertion as one of:

| Evidence Type | Meaning |
|---|---|
| `verified_fact` | Confirmed by primary or otherwise authoritative evidence |
| `company_statement` | Company or management statement, target, or guidance |
| `source_opinion` | Interpretation supplied by a source author |
| `market_consensus` | Identified market or analyst consensus |
| `non_consensus` | Evidence-based view that differs from consensus |
| `market_rumor` | Unconfirmed market report or hearsay |
| `model_assumption` | Explicit input used in a forecast or valuation |
| `codex_inference` | Reasoning derived by Codex from cited evidence |
| `disputed` | Materially conflicting or contested claims |

Use an assertion table for material claims:

```markdown
| Assertion | Evidence Type | As Of | Evidence | Confidence | Invalidation Condition |
|---|---|---|---|---|---|
|  | verified_fact | YYYY-MM-DD | [[Source Page]] | high |  |
```

Never convert management guidance, source opinion, rumor, or a model assumption into a verified fact. Keep the following milestones separate unless every transition is independently supported:

> Supply-chain entry → technical certification → formal order → delivery → recognized revenue → profit and cash flow

## Page responsibilities

### Source

Record only what one source explicitly states:

- source metadata and publication date;
- factual summary and key assertions;
- entities, concepts, events, and assumptions mentioned;
- evidence type for material claims;
- gaps, conflicts, and limitations.

Do not add an independent investment conclusion to a Source page.

### Entity

Create a canonical research object for a company, security, subsidiary, person, customer, supplier, product, or tool. Prefer updating an existing Entity over creating aliases. A listed-company Entity should act as an Entity Hub.

### Concept

Store reusable mechanisms such as industry structure, technology routes, inventory cycles, operating leverage, accounting issues, or risk frameworks. Keep company-specific conclusions in Entity or Synthesis pages.

### Event

Store a dated change with a lifecycle, evidence, expected milestones, and investment relevance. Use Event pages for earnings, orders, certifications, mergers, control changes, asset injections, financing, and regulatory changes.

### Model

Store historical inputs, assumptions, forecasts, valuation, scenarios, and sensitivities. Distinguish reported facts, company guidance, and Codex assumptions.

### Synthesis

Store cross-source judgments: investment theses, company or industry comparisons, monitoring pages, and post-mortems. Cite the underlying Source, Entity, Concept, Event, and Model pages.

Create a standalone page only when the object is likely to be queried repeatedly or is material to an investment thesis.

## Entity Hub and research coverage

For each covered security, maintain one Entity Hub that links to relevant Events, Models, Syntheses, and monitoring pages.

Include a coverage table:

```markdown
| Research Module | Status | As Of | Main Gap |
|---|---|---|---|
| Company and security | complete | YYYY-MM-DD |  |
| Ownership and governance | partial | YYYY-MM-DD |  |
| Business segments | unverified | YYYY-MM-DD |  |
| Industry and competition | unverified | YYYY-MM-DD |  |
| Products and technology | unverified | YYYY-MM-DD |  |
| Customers and suppliers | unverified | YYYY-MM-DD |  |
| Historical financials and cash flow | unverified | YYYY-MM-DD |  |
| Financial model | provisional | YYYY-MM-DD |  |
| Valuation | stale | YYYY-MM-DD |  |
| Investment thesis | draft | YYYY-MM-DD |  |
```

Use coverage states such as `complete`, `partial`, `unverified`, `provisional`, and `stale`. Do not fill missing modules with speculation.

## Event rules

Event metadata must include:

```yaml
event_type: earnings | order | certification | merger | control_change | asset_injection | financing | regulatory | other
event_status: announced | pending | completed | delayed | cancelled | disputed
announcement_date: YYYY-MM-DD
expected_date: YYYY-MM-DD
effective_date:
```

Record:

- what was announced and by whom;
- which facts are verified and which are only statements or rumors;
- the dated milestone sequence;
- expected completion or next verification date;
- investment relevance and invalidation conditions.

Re-verify an Event when `review_after` passes or a milestone date arrives. Never infer that an announced transaction, certification, or order has completed.

## Model rules

Every material Model must cover, when applicable:

- historical revenue and profit;
- business segments;
- volume and price assumptions;
- gross margin;
- research and development, selling, and administrative expenses;
- operating cash flow;
- accounts receivable and inventory;
- capital expenditure;
- consolidation date;
- listed-company ownership percentage;
- minority interests and attributable net profit;
- share count and earnings per share;
- net cash or net debt;
- conservative, base, and optimistic scenarios;
- valuation multiples and sensitivity analysis.

For each input, record period, value, currency, units, evidence type, source, and confidence. Explicitly separate:

- `verified_fact` from reported financial statements;
- `company_statement` from management guidance;
- `model_assumption` introduced for forecasting;
- `codex_inference` used to connect evidence.

Reconcile the Model with the latest reported results before using it. If reconciliation cannot be completed, mark the Model `provisional` or `stale` and report the gap.

## Investment thesis rules

Use this section order:

1. Conclusion and knowledge cutoff
2. Current company status
3. Verified facts
4. Market consensus
5. Non-consensus view
6. Codex inference
7. Core debate
8. Bull scenario
9. Base scenario
10. Bear scenario
11. Catalysts and expected timing
12. Principal risks
13. Thesis invalidation conditions
14. Monitoring indicators
15. Valuation and tradability at the current price
16. Evidence gaps and conflicting sources
17. Thesis change log

Separate:

- industry attractiveness;
- priority for further research;
- tradability at the current price.

Do not make a current-price judgment without re-verifying price, latest earnings, guidance, material orders, transaction progress, and regulatory status. If current verification is unavailable, state that the tradability conclusion cannot be completed.

## Index and log

`wiki/index.md` must include these sections:

- Sources
- Entities
- Concepts
- Events
- Models
- Synthesis
- Active Theses
- Monitoring

Preserve existing entries. Each new entry should be one concise line and, where applicable, include ticker, page type, `as_of`, status, and a short description.

Append every ingest, saved synthesis, dossier update, and lint operation to `wiki/log.md`:

```markdown
## [YYYY-MM-DD] operation | Title
Brief description of pages created, updated, reviewed, or invalidated.
```

Never rewrite existing log entries.

## Staleness, conflicts, and invalidation

- Flag an `active` page as stale when `review_after` has passed.
- Preserve superseded or invalidated models and theses for later review.
- Add a dated change-log entry and links to the replacing page.
- Keep conflicting claims side by side with evidence and use `disputed` when appropriate.
- Never silently replace a historical value with a newer period.
- Update Event status when milestones occur; do not leave completed, delayed, or cancelled events as pending.
- Report missing, stale, conflicting, or rumor-only evidence instead of inventing a value.

## Images

Keep images in `raw/assets/`. When a chart or diagram is material, describe its evidence in text and cite the associated Source page. Never move or rewrite the original image.
