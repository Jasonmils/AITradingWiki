---
name: equity-research
description: Build or update an evidence-grounded, market-aware dossier for one publicly traded security. Use for a deep dive, initiate coverage, "建立研究档案", "更新投资论点/模型", or whether one A-share or U.S.-listed stock is worth buying, initiating, adding, holding, reducing, or avoiding now. Work wiki-first, route by listing regime, re-verify current facts, and cover gaps, company and governance, business and industry, three-scenario modeling, valuation and sensitivity, thesis, catalysts, risks, invalidation, monitoring, and current-price tradability. Automatically archive every delivered research report, including partial or blocked work, as non-canonical Markdown under output/equity-research/. For an A-share dossier, use the shared D1–D4 research-data and C1–C5 technical-analysis contracts by default. Ask before any Canonical Wiki write. Do not use for multi-stock comparisons, raw ingestion, or wiki audits.
---

# Equity Research

Build or update one listed security's evidence-grounded research dossier.

## Boundaries

- Handle one publicly traded security per invocation.
- Route multi-security comparisons to `$second-brain-query`, raw sources to `$second-brain-ingest`, and full-wiki audits to `$second-brain-lint`.
- Read the wiki first. Never modify `raw/`.
- Do not guess a company-to-ticker mapping.
- Do not hard-code or assume any security conclusion.
- Do not automatically generate or execute buy/sell orders. Position language
  must remain conditional, evidence-bounded, and controlled by the user.
- Automatically archive every delivered `complete`, `partial`, or `blocked`
  research report under `output/equity-research/` before asking about
  Canonical Wiki writes.
- Treat report archiving as an authorized non-canonical output step. Keep every
  `wiki/`, `wiki/index.md`, and `wiki/log.md` write behind explicit curator
  approval.

Read `../second-brain/references/wiki-schema.md` before evaluating evidence or creating pages. Read the relevant file in `../../templates/` only when preparing a write.

## 1. Resolve scope

Identify:

- legal company or issuer;
- canonical exchange-prefixed ticker;
- selected listed security, security type or share class, and asset class;
- listing regime, issuer domicile, operating geographies, and policy
  jurisdictions;
- reporting standard, reporting currency, and trading currency;
- requested investment horizon;
- knowledge cutoff and current date;
- whether the task initiates coverage, refreshes a dossier, updates a Model or thesis, or evaluates a current position decision.

Clarify ambiguous securities or time horizons when they would materially change the analysis.

Select and read the market profile before analysis:

- `SSE:*`, `SZSE:*`, or `BJSE:*` → `a_share`; read
  `../second-brain/references/a-share-analysis.md`.
- `NASDAQ:*`, `NYSE:*`, `NYSEARCA:*`, or `AMEX:*` → `us_equity`; read
  `../second-brain/references/us-equity-analysis.md`.
- ADR, dual listing, or foreign issuer → `cross_market`; read
  `../second-brain/references/cross-market-analysis.md` plus every relevant
  underlying profile.

The dossier is for the selected security. Reuse operating-company evidence
where valid, but do not merge listing-specific shareholder rights, liquidity,
valuation, or tradability.

## 2. Audit existing coverage

Read `wiki/index.md`, locate the security Entity Hub, and follow linked Sources, Concepts, Events, Models, Syntheses, and Monitoring pages.

Classify each research module as `complete`, `partial`, `unverified`, `provisional`, or `stale`. Report:

- missing evidence;
- stale `as_of` or passed `review_after`;
- conflicting claims;
- rumor-only support;
- missing primary sources;
- Model or thesis not reconciled with newer Events.

Do not fill a gap with speculation.

## 3. Build the evidence map

Retrieve in this order:

1. Source;
2. Entity and Concept;
3. Event;
4. Model;
5. Synthesis.

Classify material assertions as `verified_fact`, `company_statement`, `source_opinion`, `market_consensus`, `non_consensus`, `market_rumor`, `model_assumption`, `codex_inference`, or `disputed`.

Keep supply-chain entry, certification, formal order, delivery, revenue, profit, and cash flow as separate milestones unless each link is evidenced.

## 4. Re-verify current facts

Re-check current price, latest earnings and guidance, material orders or certifications, transaction progress, ownership, management, regulation, litigation, and other current facts whenever they affect the conclusion.

Prefer primary sources. Record publication date, reporting period, retrieval date, currency, units, and source. Keep newly verified external facts separate from existing wiki knowledge. If verification is unavailable, mark the affected conclusion incomplete.

For current tradability, re-verify the selected market's mutable trading rules
and record `market_rules_as_of`. When converting currencies, record the FX
source and `fx_as_of`.

## 5. Add A-share shared research data and technical context

For `listing_regime: a_share`, invoke both shared Skills by default unless the
user explicitly narrows or excludes a module:

1. Invoke `$a-share-research-data` and run the complete D1–D4 contract.
2. Invoke `$a-share-technical-analysis` and run the complete C1–C5 contract.

Do not silently omit a failed module or replace it with an uncited web result.
Preserve every module's status, cutoff, retrieval time, providers, source
references, quality result, conflicts, and error boundary.

### D1–D4 research-data contract

- **D1 市场快照**：当前行情、PE、PB、总市值、流通市值，以及 stale
  或停牌判定。未通过时效和停牌门的数值不得支撑当前可交易性。
- **D2 市场与公司事件发现**：公告、解禁、分红、股东户数、大宗交易和
  两融。重要的第三方发现必须回查交易所、监管机构或发行人正式来源。
- **D3 财务与一致预期**：以正式报告为先，对照财务数据；一致预期必须保留
  预测年度、机构数和更新时间，不得与公司指引混合。
- **D4 软信息**：IR 问答作为 `company_statement`；新闻只作为可归因的
  线索或 `source_opinion`，不得自动晋级为事实。

### C1–C5 technical contract

- **C1 双引擎**：对同一份标准化、已完成 K 线同时运行 CZSC 和 chan.py；
  不允许引擎各自拉取不同的默认数据。
- **C2 结构状态**：完整保留 confirmed/provisional 的笔、线段和中枢；
  provisional 不得当作已确认事实。
- **C3 中性 BSP**：保留中性的 BSP 候选、稳定性和撤回历史；不把
  BSP 标签转换为自动买卖指令。
- **C4 稳定性**：输出静态图，并比较严格/宽松（schema 值 `strict`/`broad`）参数下的结构稳定性；
  对参数敏感的结论必须降权。
- **C5 多周期映射**：保留月、周、日父子映射和区间嵌套上下文。

For a week/month allocation horizon, use monthly structure as the primary
technical regime, weekly structure for position sizing and confirmation, and
daily structure only for execution timing. Preserve `technical_as_of`,
adjustment, providers, both engine versions, data and engine quality,
cross-engine differences, incomplete-bar exclusions, parameter stability, and
all provisional or withdrawn structures.

Apply the evidence boundary explicitly:

- promote timely, quality-gated official observations to `verified_fact` only
  when their provenance supports that classification;
- keep issuer explanations, guidance, and IR answers as `company_statement`;
- keep attributable third-party analysis and news interpretation as
  `source_opinion`;
- use `market_consensus` only for a dated, attributable consensus dataset with
  forecast year and institution count;
- classify technical structures, cross-engine synthesis, valuation bridges,
  and position implications as `codex_inference`.

If required D or C modules are `disputed`, `unavailable`, stale, or materially
conflicted, report the blocked conclusion. Never let a technical signal
override fundamentals, valuation, governance, regulation, liquidity, current
market rules, or a material Event.

## 6. Analyze the security

Cover, as evidence permits:

- company and listed security;
- ownership, control, governance, and related-party issues;
- legacy and new business segments;
- industry size, structure, competition, and mechanism;
- products, technology routes, certifications, customers, suppliers, and value-chain position;
- historical revenue, profit, margins, cash flow, receivables, inventory, capital expenditure, and segment data;
- management guidance and source forecasts, clearly classified.

Apply the selected profile's market-specific lens. For A shares this includes
controller and ownership structure, related parties, refinancing, unlocks,
pledges, recurring versus non-recurring profit, government grants, impairment,
and policy transmission when material. For U.S. equities this includes
GAAP/non-GAAP reconciliation, SBC and dilution, buybacks, RPO or deferred
revenue, dual-class control, insider filings, free cash flow, and applicable
rate, antitrust, tax, export-control, sanctions, or CFIUS mechanisms.

## 7. Build or reconcile the Model

Use conservative, base, and optimistic scenarios. Explicitly separate reported facts, company guidance, source opinion, and `model_assumption`.

When applicable, model:

- segment volume, price, revenue, and gross margin;
- research and development, selling, and administrative expenses;
- operating cash flow, working capital, and capital expenditure;
- consolidation date and listed-company ownership percentage;
- minority interests and attributable net profit;
- shares, earnings per share, net cash, and net debt;
- comparable companies, valuation multiples, and sensitivity.

Reconcile against the latest reported results. Mark unresolved Models `provisional` or `stale`.

Use market-appropriate valuation metrics and comparable securities; do not
apply one universal multiple. For cross-listed securities, normalize accounting
basis, fiscal period, currency, FX date, diluted shares, ADR ratio, enterprise
value, net debt, tax, and rights, then produce listing-specific valuation and
tradability outputs.

## 8. Form the investment view

Separate:

- verified facts;
- company or source statements;
- market consensus;
- non-consensus view;
- rumors and disputed claims;
- Codex inference.

Develop bull, base, and bear scenarios. State:

- core debate;
- catalysts and expected timing;
- principal risks;
- thesis invalidation conditions;
- monitoring indicators and next verification date;
- evidence gaps and conflicts.

Answer separately:

1. Is the industry attractive?
2. Is the security a priority for further research?
3. Is it tradable at the current price and horizon?

Do not give a current-price conclusion without current verification.

## 9. Deliver and archive before Canonical saving

Present:

1. resolved security, listing regime, applied market profile, horizon, wiki
   cutoff, reporting and trading currencies, and market-rule cutoff;
2. research coverage table;
3. evidence map and conflicts;
4. company, governance, business, industry, product, customer, and supplier analysis;
5. financial quality and three-scenario Model;
6. valuation and sensitivity;
7. thesis, catalysts, risks, invalidation, and monitoring;
8. selected-listing current-price tradability and market-specific constraints;
9. for A shares, a D1–D4 research-data coverage table and a C1–C5 technical
   coverage table, including every module status, cutoff, quality result,
   evidence classification, conflict, and invalidation condition;
10. missing evidence and next research actions;
11. exact pages proposed for creation or update.

Write the same delivered research to a non-canonical Markdown report before
asking about Wiki changes. Use `scripts/save_report.py` so the archive is
atomic, collision-safe, and kept outside `raw/` and `wiki/`:

```bash
python3 skills/equity-research/scripts/save_report.py \
  --ticker SSE:600519 \
  --as-of YYYY-MM-DD \
  --listing-regime a_share \
  --horizon 12-24m \
  --wiki-cutoff YYYY-MM-DD \
  --market-rules-as-of YYYY-MM-DD \
  --report-status complete \
  --body-file /absolute/path/to/completed-report-body.md
```

The body file must contain the report body without YAML frontmatter. Use the
actual research state for `--report-status`: `complete`, `partial`, or
`blocked`. The saver writes:

```text
output/equity-research/<ticker>-<as_of>-<utc-run-id>.md
```

The report frontmatter must retain `canonical: false`, the selected ticker and
listing regime, `as_of`, `generated_at`, horizon, Wiki and market-rule cutoffs,
research status, and `canonical_write_status_at_generation: pending_approval`.
Never overwrite an earlier report. If report generation fails, report the
failure and retry safely; do not substitute a Canonical Wiki write.
Do not declare the research handoff complete until the report path exists.

Return the absolute saved-report path with the research deliverable. Then ask
the user to approve, reject, or narrow the proposed Canonical Wiki writes.

## 10. Save Canonical pages after approval

Apply only the approved changes:

- create or update the Entity Hub and research-coverage table;
- create or update material Event pages;
- create or update the Model;
- create or update the investment-thesis and monitoring Syntheses;
- preserve and mark replaced pages `superseded` or `invalidated`;
- update `wiki/index.md`, including Active Theses and Monitoring;
- append an `equity-research` entry to `wiki/log.md`.

Populate the approved market metadata on Entity, Model, thesis, and monitoring
pages. Report every page changed, the final `as_of`, `market_rules_as_of` when
used, D1–D4 provenance, `technical_as_of`, C1–C5 engine provenance and
stability when saved, `review_after`, unresolved gaps, and the next
verification date.
