# AI Frontier Technology and Trading Wiki Schema

This is the canonical schema for the AI frontier-technology, commercialization,
industry-opportunity, and investment-research vault. Apply it when creating,
updating, querying, or auditing wiki pages.

## Contents

1. Architecture
2. Language conventions
3. Research tracks
4. Canonical skill names
5. Canonical metadata
6. Market-aware metadata and routing
7. Evidence classification
8. Technology and commercialization evidence
9. Page responsibilities
10. Entity Hub and research coverage
11. Event rules
12. Model rules
13. Trend thesis and opportunity map rules
14. A-share technical snapshots
15. Investment thesis rules
16. Index and log
17. Staleness, conflicts, and invalidation

## Architecture

Maintain the research chain:

> Evidence → Object → Mechanism → Technology Maturity → Commercialization → Industry Value Pool → Company Exposure → Model → Investment Judgment

- `raw/`: source inbox. Non-video documents are immutable. Keep an MP4
  byte-for-byte until its transcript and Canonical Wiki ingest are confirmed;
  then only the audited video-finalization workflow may delete that exact MP4.
- `raw/assets/`: immutable images and attachments referenced by sources.
- `wiki/sources/`: factual summaries of individual sources.
- `wiki/entities/`: normalized companies, securities, subsidiaries,
  laboratories, people, customers, suppliers, products, models, standards,
  projects, and tools.
- `wiki/concepts/`: reusable mechanisms, technologies, metrics, risks, and frameworks.
- `wiki/events/`: dated changes such as research releases, independent
  reproductions, model or product launches, benchmarks, pilots, deployments,
  adoption, earnings, orders, certifications, mergers, financing, and regulation.
- `wiki/models/`: technology, commercialization, unit-economics, financial,
  valuation, scenario, and sensitivity models with explicit assumptions.
- `wiki/synthesis/`: trend theses, opportunity maps, comparisons, investment
  theses, monitoring, judgments, and post-mortems.
- `templates/`: empty canonical page structures.
- `output/`: non-canonical reports and generated artifacts, including automatic
  consolidated equity reports under `output/equity-research/`.

Do not organize top-level directories by market, asset view, or horizon. Represent those attributes in metadata.

## Language conventions

- Canonical Wiki page titles, headings, prose, table headers, index descriptions, and newly appended log entries should be written primarily in Chinese unless the curator requests another language.
- Retain English for legal company names, tickers and exchange-prefixed identifiers, official product/source titles, metadata keys and enums, evidence labels, units, acronyms, and domain-specific terms whose English form is more precise or commonly queried.
- Common retained terms include CPO, OCS, ASIC, XPU, DSP, FAU, ELS, BoM, TAM, EPS, NPO, SiPh, EML, CW laser, MOCVD, scale-up, scale-out and scale-across. Add a concise Chinese explanation at first use when useful.
- Do not force-translate an English proper noun or technical term when that would introduce ambiguity. Preserve exact source wording when the wording is itself material evidence.
- Translation must preserve every number, date, period, currency, unit, source, attribution, confidence, invalidation condition and evidence type. Never upgrade or downgrade evidence because of translation.
- Keep kebab-case filenames and machine-readable frontmatter stable. Use Chinese readable titles and Chinese display text in `[[target|中文标题]]` wikilinks.

## Research tracks

Use one evidence base with one or more `research_tracks`:

- `technology`: problem definition, mechanism, competing technical routes,
  benchmarks, maturity, bottlenecks, and dated forward milestones;
- `commercialization`: product feasibility, deployment, customer adoption,
  willingness to pay, unit economics, value-chain role, and value capture;
- `investment`: company exposure, financial materiality, valuation, catalysts,
  risks, invalidation, and current-price tradability.

Route from the user's requested decision, not merely from a mentioned company
or ticker. A question about how a technology works stays in `technology`; a
question about customers and value capture adds `commercialization`; a
complete one-security decision adds `investment` and routes to
`$equity-research`.

Do not collapse these conclusions:

> Technically promising ≠ independently reproduced ≠ production-ready ≠ commercially adopted ≠ financially material ≠ attractively priced

## Canonical skill names

Use exactly these English display names and invocation identifiers:

| Display Name | Invocation |
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

Use the invocation identifier exactly in every Skill body, routing rule,
`default_prompt`, README example, test, and generated agent configuration. Do
not translate, capitalize, insert spaces into, or create an alias for it.
Chinese explanatory prose may surround the identifier but must not become part
of the Skill name.

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
research_tracks: []
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

Use subtype fields when applicable:

```yaml
entity_type: company | security | lab | person | product | model | standard | project | tool
concept_type: technology | architecture | metric | industry_mechanism | business_framework
model_type: technology_trend | commercialization | unit_economics | financial | valuation
synthesis_type: trend_thesis | opportunity_map | monitoring | investment_thesis | comparison | post_mortem
```

Technology or commercialization judgments should also record applicable fields:

```yaml
technology_horizon: 0-2y | 2-5y | 5-10y | 10y+
technology_maturity: research | prototype | independently_reproduced | pilot | production | scaled
commercialization_stage: none | demo | poc | paid_pilot | order | delivery | revenue | profit | fcf
```

- `technology_horizon` describes the expected time to a stated technical or
  adoption milestone, not an investment holding period.
- `technology_maturity` records the highest evidenced technical state.
- `commercialization_stage` records the highest evidenced commercial state.
- Omit an inapplicable field instead of fabricating a value.
- Cite the basis for every maturity or stage classification and retain
  conflicts as `disputed`.

## Market-aware metadata and routing

Market routing follows the listed security, while company analysis also
preserves the issuer's economic and regulatory context. Do not infer the
analysis regime from `markets` alone.

Listed-company Entities require:

```yaml
primary_ticker: "NASDAQ:NVDA"
listing_regime: a_share | us_equity | cross_market | private | other
analysis_regimes: [us_equity]
security_type: common_stock
issuer_domicile: US
reporting_standard: US_GAAP
reporting_currency: USD
trading_currency: USD
policy_jurisdictions: [US, CN]
operating_geographies: [US, CN, Global]
cross_listed_tickers: []
```

- `primary_ticker`: security used as the Entity Hub's primary listing.
- `listing_regime`: rule set for the primary security. Use `a_share` for
  `SSE:*`, `SZSE:*`, or `BJSE:*`; `us_equity` for `NASDAQ:*`, `NYSE:*`,
  `NYSEARCA:*`, or `AMEX:*`; and `cross_market` when multiple listing regimes
  are material to the Entity.
- `analysis_regimes`: every regime required for the page's analysis. Valid
  values are `a_share`, `us_equity`, `cross_market`, and `other`.
- `security_type`: legal security form, such as `common_stock`, `adr`, or
  another precisely sourced form.
- `issuer_domicile`: issuer's legal domicile using a stable country or region
  code.
- `reporting_standard`: primary reporting framework, such as `PRC_GAAP`,
  `US_GAAP`, `IFRS`, or `TIFRS`.
- `reporting_currency`: currency of primary financial reporting.
- `trading_currency`: currency in which the primary listed security trades.
- `policy_jurisdictions`: jurisdictions whose rules can materially affect the
  issuer, its products, or its listed security.
- `operating_geographies`: material business or production geographies.
- `cross_listed_tickers`: exchange-prefixed related listings, ADRs, or
  secondary listings; do not place ordinary share-class aliases here.

A private-company Entity may use `listing_regime: private` and omit
listed-security-only fields that are genuinely unavailable.

Models and Syntheses spanning listed securities require:

```yaml
analysis_regimes: [a_share, us_equity]
policy_jurisdictions: [CN, US]
reporting_currencies: [CNY, USD]
market_rules_as_of: YYYY-MM-DD
fx_as_of: YYYY-MM-DD
```

`market_rules_as_of` is mandatory only when the page makes a current
tradability or listing-rule judgment. `fx_as_of` is mandatory only when
currencies are converted or normalized. Omit an inapplicable field rather than
fabricating a value.

Load the applicable profile before market-sensitive analysis:

- `a-share-analysis.md` for A shares;
- `us-equity-analysis.md` for U.S.-listed equities;
- `cross-market-analysis.md` for ADRs, dual listings, foreign issuers, or
  comparisons across regimes.

For cross-market comparisons, normalize accounting basis, fiscal period,
currency and FX date, diluted shares, enterprise value and net debt, security
rights and share class, and ADR ratio where applicable. Keep operating-company
facts separate from listing-specific liquidity, policy, and tradability.

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

## Technology and commercialization evidence

For papers, preprints, code repositories, patents, standards, model cards,
benchmarks, product documentation, conference presentations, and demos, retain
the exact source type, version or revision, publication date, covered task,
dataset, hardware, software, comparison baseline, and known limitations when
material.

Apply these boundaries:

- A paper can evidence its reported method and result under its stated
  conditions. A preprint is not peer review, and publication is not independent
  reproduction.
- A code repository can evidence the existence and revision of released code;
  it does not prove that reported results reproduce in another environment.
- A patent can evidence an application or grant; it does not prove a working
  product, freedom to operate, adoption, or economic value.
- A standard or specification can evidence agreed interfaces or requirements;
  it does not prove implementation or deployment.
- A vendor benchmark, product claim, roadmap, or demo is normally
  `company_statement` unless authoritative raw evidence and reproducible
  conditions support a stronger label.
- Record an independent reproduction as a separate assertion and Event. Do not
  silently merge it with the original author's result.

Before comparing benchmarks, normalize or explicitly disclose:

- task, model, checkpoint, dataset, quality or accuracy target;
- hardware count, memory, topology, numerical precision, sparsity, and power;
- software, compiler, kernel, framework, and version;
- input/output length, batch, concurrency, latency target, and availability;
- baseline implementation, measurement period, and excluded failures;
- cost boundary, currency, utilization, and amortization when making economic
  comparisons.

Keep both chains distinct:

> Research result → independent reproduction → prototype → pilot → production deployment → scaled adoption
>
> Problem validation → demo/POC → paid pilot → formal order → delivery → recognized revenue → profit → FCF

When the evidence does not establish a transition, report the gap instead of
promoting the maturity or commercialization stage.

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

Create a canonical research object for a company, security, subsidiary,
laboratory, person, customer, supplier, product, model, standard, project, or
tool. Set `entity_type` when it improves routing. Prefer updating an existing
Entity over creating aliases. A listed-company Entity should act as an Entity
Hub; a non-listed technical Entity must not fabricate ticker or market fields.

For a listed-company Entity Hub, preserve listing regime, issuer domicile,
operating geographies, policy jurisdictions, reporting basis, reporting
currency, trading currency, and cross-listing relationships as distinct fields.

### Concept

Store reusable mechanisms such as architectures, algorithms, scaling laws,
benchmarks, industry structure, technology routes, adoption mechanisms,
inventory cycles, operating leverage, accounting issues, or risk frameworks.
Record competing routes, boundary conditions, and unresolved questions. Keep
company-specific conclusions in Entity or Synthesis pages.

### Event

Store a dated change with a lifecycle, evidence, expected milestones, and
technology, commercialization, or investment relevance. Use Event pages for
research or model releases, independent reproductions, product launches,
benchmarks, standards, pilots, deployments, adoption, earnings, orders,
certifications, mergers, financing, and regulatory changes.

### Model

Store technology, commercialization, unit-economics, financial, or valuation
inputs, assumptions, scenarios, and sensitivities. Set `model_type`. Distinguish
observed facts, company guidance, source forecasts, model assumptions, and
Codex inference.

### Synthesis

Store cross-source judgments: trend theses, opportunity maps, company or
industry comparisons, investment theses, monitoring pages, and post-mortems.
Set `synthesis_type` and cite the underlying Source, Entity, Concept, Event,
and Model pages.

Create a standalone page only when the object is likely to be queried
repeatedly, changes a durable trend or opportunity map, or is material to an
investment thesis.

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
| Technical and multi-timeframe structure | unverified | YYYY-MM-DD |  |
| Investment thesis | draft | YYYY-MM-DD |  |
```

Use coverage states such as `complete`, `partial`, `unverified`, `provisional`, and `stale`. Do not fill missing modules with speculation.

## Event rules

Event metadata must include:

```yaml
event_type: research_release | independent_reproduction | model_release | product_launch | open_source_release | benchmark | standard | pilot | deployment | adoption | earnings | order | certification | merger | control_change | asset_injection | financing | regulatory | other
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
- technology, commercialization, and investment relevance as applicable;
- the next milestone required before promoting maturity or commercial stage;
- invalidation conditions.

Re-verify an Event when `review_after` passes or a milestone date arrives. Never infer that an announced transaction, certification, or order has completed.

## Model rules

Set `model_type` and apply the matching contract.

### Technology trend model

Cover, when applicable:

- problem, mechanism, competing routes, and explicit system boundary;
- observed inputs versus assumed scaling, learning-curve, cost, performance,
  reliability, energy, or capacity relationships;
- benchmark normalization and reproducibility gaps;
- conservative, base, and optimistic technical or adoption scenarios;
- dated milestones, sensitivities, critical unknowns, and invalidation.

Do not extend a lab result to production cost, reliability, or scale without an
explicit assumption and evidence boundary.

### Commercialization or unit-economics model

Cover, when applicable:

- customer problem, product or service boundary, buyer, user, and payer;
- adoption funnel from demo/POC through paid deployment and renewal;
- price, volume, utilization, gross margin, implementation, support, and
  customer-acquisition assumptions;
- TAM, SAM, and SOM without silently equating market size with obtainable
  revenue;
- value creation, bargaining power, competitive response, value capture, and
  profit-pool allocation;
- conservative, base, and optimistic scenarios, sensitivities, milestones,
  and invalidation.

### Financial or valuation model

Every material financial or valuation Model must cover, when applicable:

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

When a Model covers multiple listing regimes, produce listing-specific
valuation and tradability outputs after normalizing the operating inputs. Do
not apply an A-share policy or liquidity premium to a U.S. security, or a U.S.
options or short-interest signal to an A-share security, without an explicit
cross-market mechanism.

## Trend thesis and opportunity map rules

A `trend_thesis` must include:

1. question, scope, and knowledge cutoff;
2. current technical state and evidenced maturity;
3. competing routes and comparison boundary;
4. verified facts, company statements, source opinions, consensus,
   non-consensus, disputes, and Codex inference;
5. drivers, bottlenecks, dependencies, and critical unknowns;
6. conservative, base, and optimistic development paths;
7. dated milestones, leading indicators, review date, and invalidation;
8. commercialization implications without making an automatic security call.

An `opportunity_map` must separately analyze:

1. enabling technology and customer problem;
2. product boundary, buyer, user, payer, and adoption stage;
3. value chain, bottlenecks, substitutes, complements, and bargaining power;
4. value creation versus value capture and likely profit pools;
5. direct, indirect, optional, and spurious company exposure;
6. company-level revenue, margin, capital intensity, profit, and FCF
   materiality gaps;
7. policy, geographic, supply-chain, execution, and timing risks;
8. the evidence still required before a security dossier or current-price
   judgment.

Do not rank a security from technology appeal, media attention, a single
benchmark, a large TAM, or supply-chain association alone. Route a complete
one-security decision to `$equity-research`.

## Equity research reports

Every `$equity-research` invocation that reaches delivery must archive its full
`complete`, `partial`, or `blocked` research report under
`output/equity-research/` before requesting permission for Canonical Wiki
changes. This report is non-canonical, may be created without a separate write
approval, and must never substitute for or trigger an automatic write to
`wiki/`, `wiki/index.md`, or `wiki/log.md`.

Use `skills/equity-research/scripts/save_report.py`. Preserve a unique report
for every run; never overwrite an earlier report. Include `canonical: false`,
ticker, listing regime, `as_of`, `generated_at`, horizon, Wiki and market-rule
cutoffs, `report_status`, and
`canonical_write_status_at_generation: pending_approval`. Return the saved path
to the curator before presenting the proposed Canonical writes.

## A-share technical snapshots

An on-demand technical report in `output/technical-analysis/` is non-canonical.
Save it as `page_type: synthesis` only when it is durable, material to a thesis,
and the curator has approved the write. Use:

```yaml
synthesis_type: technical_snapshot
technical_as_of: YYYY-MM-DD
data_retrieved_at: YYYY-MM-DDTHH:MM:SSZ
data_providers: [baostock, akshare]
adjustment: qfq | none
technical_engine: "czsc 0.10.12" # compatibility baseline
technical_engines: ["czsc 0.10.12", "chan.py@429d6ed"]
technical_config_hashes: {}
data_quality_status: complete | degraded | disputed | unavailable
engine_consistency_status: complete | degraded | disputed | unavailable
overall_technical_status: complete | degraded | disputed | unavailable
technical_state_receipt: "output/technical-analysis/<run>.state-commit.json"
technical_state_sha256: ""
```

Retain the actual provider used, requested and actual date ranges, field/unit
normalization, cross-source result, excluded incomplete bars, engine revisions
and configuration hashes, confirmed versus provisional structures, package
versions, cache manifest, and the run-linked state commit receipt when lifecycle
state was advanced. Do not hide a BaoStock-to-AkShare fallback.

The normalized OHLCV observations may be `verified_fact` only when the
data-quality and cross-source gates pass. CZSC and chan.py pens, segments,
centers, BSP candidates, moving-average meaning, multi-timeframe alignment, and
allocation implications are `codex_inference`. A `disputed` or `unavailable`
data or engine state cannot support a directional technical conclusion.

For non-intraday A-share decisions, use monthly structure as primary, weekly
structure for sizing, and daily structure only for execution timing. Record
technical invalidation conditions and keep technical analysis subordinate to
fundamentals, valuation, governance, Events, liquidity, and current market
rules.

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
15. A-share multi-timeframe technical context, when applicable
16. Valuation and tradability at the current price
17. Evidence gaps and conflicting sources
18. Thesis change log

Separate:

- industry attractiveness;
- priority for further research;
- tradability at the current price.

Do not make a current-price judgment without re-verifying price, latest earnings, guidance, material orders, transaction progress, and regulatory status. If current verification is unavailable, state that the tradability conclusion cannot be completed.

Begin a market-sensitive thesis with the selected `listing_regime`,
`analysis_regimes`, reporting and trading currencies, wiki knowledge cutoff,
and `market_rules_as_of`. Apply the appropriate market profile and keep
official policy existence separate from inferred company impact.

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

When at least one approved page exists, add functional index views for
`Trend Theses`, `Opportunity Maps`, and technology monitoring without moving
the underlying files out of `wiki/synthesis/`.

Preserve existing entries. Each new entry should be one concise line and, where applicable, include ticker, page type, `as_of`, status, and a short description.

Append every ingest, saved synthesis, dossier update, and lint operation to `wiki/log.md`:

```markdown
## [YYYY-MM-DD] operation | Title
Brief description of pages created, updated, reviewed, or invalidated.
```

Never rewrite existing log entries.

## Staleness, conflicts, and invalidation

- Flag an `active` page as stale when `review_after` has passed.
- Flag a technology or commercialization judgment when its source version,
  benchmark, milestone, maturity, adoption state, or `review_after` has become
  stale.
- Preserve superseded or invalidated models and theses for later review.
- Add a dated change-log entry and links to the replacing page.
- Keep conflicting claims side by side with evidence and use `disputed` when appropriate.
- Never silently replace a historical value with a newer period.
- Update Event status when milestones occur; do not leave completed, delayed, or cancelled events as pending.
- Report missing, stale, conflicting, or rumor-only evidence instead of inventing a value.

## Images

Keep images in `raw/assets/`. When a chart or diagram is material, describe its evidence in text and cite the associated Source page. Never move or rewrite the original image.
