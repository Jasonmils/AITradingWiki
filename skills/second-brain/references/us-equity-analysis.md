# 美股分析 Profile

Use this profile for securities listed on NASDAQ, NYSE, NYSE Arca, or NYSE
American. It supplements the shared Wiki schema.

## 1. Official-source order

Prefer current primary evidence in this order:

1. SEC EDGAR filings, including 10-K, 10-Q, 8-K, proxy statements, Form 4,
   Schedule 13D, and Schedule 13G as applicable;
2. company investor-relations releases, presentations, and earnings-call
   materials;
3. official U.S. regulator, court, exchange, and government publications;
4. precisely attributed sell-side, market-data, and industry sources at the
   appropriate evidence level.

Current official entry points include:

- [SEC EDGAR search](https://www.sec.gov/search-filings)
- [SEC filing information](https://www.sec.gov/submit-filings)
- [FINRA equity short interest](https://www.finra.org/finra-data/browse-catalog/equity-short-interest)

Short interest and short-sale volume are different datasets and must not be
treated as interchangeable.

## 2. Required company lens

Check, when material:

- GAAP to non-GAAP reconciliation and recurring versus acquisition-related
  adjustments;
- stock-based compensation, diluted shares, repurchases, issuance, and net
  dilution;
- deferred revenue, remaining performance obligations, segment economics,
  working capital, capital expenditure, and free cash flow;
- dual-class control, board independence, executive compensation, related
  parties, Form 4 activity, and activist or beneficial ownership filings;
- acquisition accounting, goodwill, impairments, tax effects, and net debt.

Use US GAAP unless the issuer's filing states another basis. Preserve fiscal
year and quarter conventions rather than forcing calendar periods.

## 3. Policy and event reasoning

Apply rates, antitrust, export controls, sanctions, tax rules, CFIUS, or other
policy mechanisms only when relevant to the issuer. The existence and effective
date of an official rule may be `verified_fact`; the issuer-level earnings
effect remains `company_statement`, `codex_inference`, or `model_assumption`
unless directly reported.

## 4. Valuation and tradability

Select metrics that fit the business and maturity: EV/Sales, EV/EBITDA, P/E,
FCF yield, forward consensus, or a segment-based framework. Reconcile diluted
shares, net cash or debt, and the consensus period. Do not impose one universal
multiple.

For a current trade judgment, re-verify price, liquidity, exchange or SEC halt
status, options availability and implied volatility, short interest and borrow
conditions, corporate actions, and pre-market or after-hours context when
material. Record `market_rules_as_of`.

## 5. Minimum output

State:

- `listing_regime: us_equity`;
- primary ticker, security or share class, reporting and trading currencies;
- wiki cutoff and market-rule cutoff;
- GAAP/non-GAAP and dilution treatment;
- U.S.-specific policy, governance, valuation, liquidity, options, and short
  positioning considerations;
- missing or stale evidence that blocks a current-price conclusion.
