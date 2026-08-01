# 跨市场分析 Profile

Use this profile for cross-listed issuers, ADRs, foreign private issuers, or
comparisons that include more than one listing regime.

## 1. Separate the object from the security

Operating-company facts can be shared across listings. Tradability, shareholder
rights, liquidity, settlement, disclosure timing, policy exposure, and
valuation can differ by listed security. Resolve:

- legal issuer and issuer domicile;
- primary listing, secondary listing, ADR or depositary receipt;
- security type, share class, voting rights, and fungibility;
- ADR ratio and depositary fees where applicable;
- reporting standard, fiscal period, and reporting currency;
- each security's trading currency and listing regime.

Do not treat ticker aliases as cross listings, and do not infer identical
economic rights from a shared issuer name.

## 2. Apply all relevant profiles

- Apply `a-share-analysis.md` to an A-share leg.
- Apply `us-equity-analysis.md` to a U.S.-listed leg.
- Use the applicable official exchange, regulator, and issuer evidence for
  other primary markets.

For foreign issuers with U.S. listings, combine the issuer's home-market
accounting and policy evidence with U.S. security, disclosure, liquidity, and
tradability rules.

## 3. Normalize before comparison

Record and reconcile:

- fiscal period and accounting standard;
- reporting and trading currencies, FX source, and `fx_as_of`;
- diluted shares, ADR ratio, share class, ownership, and voting rights;
- enterprise value, net cash or debt, tax, minority interests, and
  attributable earnings;
- price and valuation cutoff;
- primary versus secondary market liquidity and corporate actions.

Use one operating model if appropriate, but produce listing-specific valuation
and tradability outputs. Do not hide FX, ADR, tax, or liquidity effects inside
an unexplained premium or discount.

## 4. Policy mapping

Keep issuer domicile, operating geographies, and policy jurisdictions separate.
Export controls, sanctions, data rules, antitrust, investment screening, or
geopolitical restrictions may affect operations differently from the listed
security. Classify policy existence separately from company impact.

## 5. Minimum output

State:

- `listing_regime: cross_market` and every applied `analysis_regime`;
- primary and cross-listed tickers, security forms, currencies, and ADR ratio
  if applicable;
- wiki, price, FX, and market-rule cutoffs;
- normalized operating comparison followed by listing-specific valuation and
  tradability;
- unresolved rights, fungibility, accounting, policy, or liquidity gaps.
