# A 股分析 Profile

Use this profile for securities listed on SSE, SZSE, or BJSE. It supplements
the common Wiki schema; it does not replace the shared evidence chain.

## 1. Official-source order

Prefer current primary evidence in this order:

1. 中国证监会（CSRC）法规、处罚和信息披露规则；
2. 上海证券交易所、深圳证券交易所、北京证券交易所业务规则与问询文件；
3. 公司定期报告、临时公告、问询回复、招股或再融资申报文件；
4. 国务院、部委、地方政府及其他有权限机关的正式政策文件；
5. 公司官网与投资者关系材料；
6. 可归因的卖方研究、媒体或行业资料，按较低证据等级使用。

Current official entry points include:

- [中国证监会上市公司信息披露规则（2025）](https://www.csrc.gov.cn/shanghai/c105565/c7549909/content.shtml)
- [上海证券交易所股票上市规则（2026）](https://www.sse.com.cn/lawandrules/sselawsrules2025/stocks/mainipo/c/c_20260424_10816589.shtml)
- [深圳证券交易所股票上市规则（2026）](https://www.szse.cn/lawrules/rule/allrules/bussiness/t20260424_620193.html)
- [北京证券交易所 2026 年业务规则更新](https://www.bse.cn/important_news/200028221.html)

Re-open the current rule text when a conclusion depends on it. A cached rule
date proves only what was checked at that cutoff.

## 2. Required company lens

Check, when material:

- actual controller, state-owned or private ownership, related parties, and
  parent-subsidiary interests;
- asset injection, restructuring, equity pledge, shareholder reduction,
  restricted-share unlock, refinancing, and dilution;
- goodwill, government grants, non-recurring gains, capitalized costs, and
  impairment;
- consolidated versus parent-company statements;
- receivables, inventory, contract assets, cash conversion, customer and
  supplier concentration, and contingent liabilities.

Use PRC GAAP unless the issuer's filing states otherwise. Distinguish total net
profit, attributable net profit, recurring attributable net profit, operating
cash flow, and free cash flow.

## 3. Policy and event reasoning

An official policy's publication, effective date, and applicable scope may be
`verified_fact`. Its effect on one company is not automatically a fact:

- management's claimed effect is `company_statement`;
- an evidence-linked interpretation is `codex_inference`;
- a numerical transmission path is `model_assumption`;
- unsupported theme extrapolation remains a gap.

Keep policy announcement, company eligibility, implementation, order,
delivery, revenue, profit, and cash flow as separate milestones.

## 4. Valuation and tradability

Use company history, comparable A-share securities, earnings and cash-flow
quality, free float, turnover, ownership structure, and policy or theme premium
only when evidenced. Do not impose one universal P/E threshold.

For a current trade judgment, re-verify the applicable price-limit and
risk-warning regime, suspension status, settlement cycle, shorting eligibility,
Stock Connect status, liquidity, restricted-share calendar, and corporate
actions. Record `market_rules_as_of`; do not treat these mutable rules as
permanent.

## 5. Minimum output

State:

- `listing_regime: a_share`;
- primary ticker, board, reporting and trading currencies;
- wiki cutoff and market-rule cutoff;
- official policy facts versus inferred company effects;
- A-share-specific valuation, liquidity, governance, and event risks;
- missing or stale evidence that blocks a current-price conclusion.

## 6. Current research-data routing

Use `$a-share-research-data` when an A-share dossier or current query needs
market, announcement, event, financial, consensus, investor-Q&A, or news data
that is not current in the Wiki. Skip providers and modules that the question
does not need.

- Keep `empty` separate from `error`; a failed provider does not prove that no
  announcement, event, forecast, or Q&A exists.
- Use official filings as the authority for material Events and financial
  facts. Treat third-party event feeds, financial tables, and news as discovery
  or cross-check data until the official record is verified.
- Classify a company IR answer as `company_statement`; do not treat the
  investor's question as evidence that its premise is true.
- Preserve provider, endpoint, retrieval time, source date or reporting period,
  timezone, response hash, units, evidence-class hint, quality status, and the
  need for an official recheck.
- Do not apply fixed P/E, PEG, fund-flow, or shareholder-count heuristics as
  investment conclusions.

The research-data report is read-only evidence staging. It does not authorize a
Canonical Wiki write and does not replace opening the cited announcement or
filing before promoting a material assertion to `verified_fact`.

## 7. Technical-analysis routing

For a security-level view, research update, position review, or week/month
allocation decision, invoke `$a-share-technical-analysis`. Skip it for a purely
factual Wiki lookup.

- BaoStock supplies the primary completed daily bars.
- AkShare supplies a fallback and cross-source check; disclose every fallback.
- CZSC extracts the stable baseline structure through its public API. The
  pinned public chan.py revision is a second structural audit engine that uses
  the same normalized bars; it does not fetch its own market data.
- Use front-adjusted (`qfq`) data for continuous structure and retain the
  adjustment in provenance.
- Use monthly structure as the primary regime, weekly structure for sizing, and
  daily structure only for execution timing.
- Preserve `technical_as_of`, data providers, both engine revisions,
  configuration hashes, `data_quality_status`, `engine_consistency_status`,
  and any excluded incomplete daily, weekly, or monthly structure.
- Keep confirmed and provisional pens, segments, centers, and BSP candidates
  distinct. Record withdrawn candidates; never translate BSP into an automatic
  order or position instruction.
- Only `complete` market data may advance the technical lifecycle state. State
  commits occur after analysis artifacts, use a cross-process cutoff/CAS guard,
  and retain a run-linked commit receipt. Derived output/cache/state paths must
  not point into `raw/` or `wiki/`.
- Use cross-engine agreement as methodology context, not as a new market-data
  fact. Preserve disagreements instead of selecting the more favorable engine.

Technical structure and position meaning are `codex_inference`. A
`disputed` or `unavailable` data or engine status blocks a directional technical
conclusion. Technical analysis never replaces price, valuation, fundamentals,
governance, regulation, liquidity, or Event verification.
