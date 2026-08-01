---
name: second-brain-query
description: Answer factual and connection questions from the existing wiki first across technology, commercialization, industry, and market-aware A-share, U.S.-equity, or cross-market research, with [[wikilink]] citations, evidence labels, as_of dates, conflicts, gaps, and current-data verification when needed. Use for factual questions, exploring connections, asking "我的知识库里…", reviewing an existing view, or comparing multiple securities or claims. For A shares, keep pure factual lookups wiki-first, use shared D1–D4 research data only as current facts require, and add the C1–C5 technical contract only for views, comparisons, position reviews, or week/month allocation. Default to read-only. Use frontier-tech-research for a complete technology-topic or trend study, technology-to-investment for a new industry opportunity map, equity-research for a complete one-security dossier or current position decision, and second-brain-ingest for raw documents.
---

# Second Brain Query

Answer from the existing knowledge base before using raw evidence or external research.

## Route the request

- Use this skill for wiki questions, connection exploration, existing-view summaries, and multi-security comparisons.
- Route a complete frontier-technology explanation, route comparison, maturity
  audit, or forward trend thesis to `$frontier-tech-research`.
- Route a new commercialization, value-pool, beneficiary, or industry
  opportunity map to `$technology-to-investment`.
- Route one-security initiation, a full dossier, thesis or model updates, and "buy or build a position now" decisions to `$equity-research`.
- Route new raw documents to `$second-brain-ingest`.
- Remain read-only unless the user later approves saving a synthesis.
- Do not automatically generate or execute buy/sell orders. Keep any position
  language conditional and under the user's control.

## Parse the question

Identify:

- company or subject;
- requested `research_tracks`: `technology`, `commercialization`, or
  `investment`;
- technology version, maturity, commercialization stage, and requested
  technology horizon when applicable;
- canonical exchange-prefixed ticker and listed security, if applicable;
- listing regime, issuer domicile, operating geographies, and policy
  jurisdictions;
- reporting standard, reporting currency, and trading currency;
- requested investment horizon;
- requested comparison dimensions;
- whether the answer depends on current price or current facts.

Do not guess an ambiguous company or ticker. Ask for resolution when it materially changes the answer.

## Select the market regime

Route from the listed security, not from the company name or `markets` alone:

- `SSE:*`, `SZSE:*`, or `BJSE:*` → `a_share`; read
  `../second-brain/references/a-share-analysis.md`.
- `NASDAQ:*`, `NYSE:*`, `NYSEARCA:*`, or `AMEX:*` → `us_equity`; read
  `../second-brain/references/us-equity-analysis.md`.
- ADR, dual listing, foreign issuer, or comparison across regimes →
  `cross_market`; read
  `../second-brain/references/cross-market-analysis.md` and every relevant
  underlying market profile.

If a company has multiple securities, resolve which security the question asks
about. Shared operating facts may be reused, but current valuation, liquidity,
shareholder rights, and tradability must be judged for the selected security.

## Search sequence

1. Read `wiki/index.md`, including Sources, Entities, Concepts, Events, Models, Synthesis, Active Theses, and Monitoring.
2. Find the relevant technical Entity or Concept, trend thesis, opportunity
   map, or security Entity Hub and inspect its links or research coverage.
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

- latest paper, preprint revision, code release, model card, product version,
  standard, benchmark, independent reproduction, or technical roadmap;
- current technical maturity, pilot, production deployment, scaled adoption,
  commercialization stage, customer evidence, or unit economics;
- current price or valuation;
- latest earnings, guidance, or financial statements;
- current orders, certification, delivery, or transaction progress;
- current ownership, regulation, litigation, or management;
- whether a security is tradable at the current price.

Prefer primary sources and record publication date, covered period, currency, units, and retrieval date. Keep external current facts separate from wiki facts. If current verification is unavailable, state that a current-price conclusion cannot be completed.

For a technical comparison, also preserve the task, model, dataset, hardware,
software, precision, workload, baseline, and version. If material conditions
remain mismatched, report the comparison as `disputed` or unavailable instead
of choosing the favorable result.

For a market-sensitive answer, also state `market_rules_as_of` and re-verify
mutable listing, settlement, halt, shorting, connect, session, or other trading
rules used in the conclusion. Do not substitute a profile's examples for a
current rule check.

## Route A-share shared research data and technical context

For a resolved `SSE:*`, `SZSE:*`, or `BJSE:*` security, keep the following
cost-aware routing boundary:

- For a purely factual Wiki lookup that the current Wiki can answer, invoke
  neither `$a-share-research-data` nor `$a-share-technical-analysis`.
- When the answer depends on current market facts or Events, invoke only the
  necessary `$a-share-research-data` modules:
  - D1 for current price, PE, PB, total/free-float market capitalization, stale
    data, or suspension status;
  - D2 for announcements, lockups, dividends, holder counts, block trades, or
    margin-financing discovery, with important third-party records rechecked
    against an official source;
  - D3 for formal-report-first financials, financial cross-checks, or dated
    consensus with forecast year, institution count, and update time;
  - D4 for IR answers and attributable news leads.
- Invoke `$a-share-technical-analysis` and its complete C1–C5 contract only for
  a security view, comparison, research update, position review, or week/month
  allocation decision. Do not invoke it merely because an A-share ticker is
  mentioned.

The C1–C5 contract uses the same normalized completed bars for CZSC and chan.py,
preserves confirmed/provisional pens, segments, and centers, retains neutral
BSP candidates and withdrawal history, reports strict/broad parameter and
static-chart stability, and preserves monthly/weekly/daily parent-child and
interval-nesting context.

Preserve each requested module's result status, cutoff, retrieval time,
providers, official-recheck flag, quality result, conflicts, and limitations.
An empty result is not a provider error; a provider error is not evidence that
the event did not occur.

Classify the returned material without promotion:

- quality-gated official observations may be `verified_fact`;
- issuer guidance, explanations, and IR answers are `company_statement`;
- attributable third-party analysis and news interpretation are
  `source_opinion`;
- a dated, attributable consensus dataset is `market_consensus`;
- Chan/CZSC structures, cross-engine synthesis, valuation bridges, and position
  implications are `codex_inference`.

If a required module is stale, `disputed`, `unavailable`, or materially
conflicted, state what is blocked instead of choosing the favorable source or
engine. For the default non-intraday horizon, interpret monthly structure
first, weekly structure for sizing, and daily structure only for execution
timing. Never turn BSP, a technical label, or a consensus target into an
automatic buy/sell instruction, and never let it override fundamentals,
valuation, Events, liquidity, or current market rules.

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

For technology or commercialization questions, keep technical promise,
independent reproduction, production readiness, commercial adoption, company
financial materiality, and security valuation as separate conclusions.

For cross-market comparison, normalize before judging:

- fiscal periods and accounting standards;
- reporting and trading currencies, with FX source and `fx_as_of` when
  converted;
- diluted shares, share class, ADR ratio, enterprise value, and net debt;
- ownership rights, policy exposure, and listing-specific liquidity.

Do not transfer an A-share policy or liquidity premium to a U.S. security, or a
U.S. options or short-interest signal to an A-share security, without an
explicit mechanism.

## Answer contract

Include:

1. Direct answer, selected `research_tracks`, Wiki cutoff, external verification
   cutoff, and, when relevant, selected listed security, `listing_regime`,
   applied analysis profile, reporting and trading currencies, and
   `market_rules_as_of`.
2. Wiki pages actually used, cited as `[[Page Title]]`.
3. Evidence-classified findings.
4. Conflicts, stale information, and rumor-only claims.
5. Research coverage and missing data.
6. Current external verification, when required, including every requested
   D1–D4 module's status, cutoff, provenance, official-recheck requirement, and
   evidence classification.
7. Codex inference and its assumptions.
8. Listing-specific valuation and tradability, including normalization choices
   for comparisons.
9. For an applicable A-share security view, a C1–C5 technical module with
   `technical_as_of`, data and engine quality, confirmed/provisional boundary,
   stability, withdrawal history, evidence boundary, conflicts, and
   invalidation conditions.
10. Catalysts, risks, monitoring indicators, and invalidation conditions when
    relevant.
11. Technology maturity, commercialization stage, benchmark boundary, and the
    missing transition evidence when those dimensions are relevant.

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
