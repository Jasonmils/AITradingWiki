---
page_type: model
subject: "CPO 公司财务基线与资本结构（2025–2026）"
tags: [financial-model, cpo, capital-structure]
tickers: ["NASDAQ:AVGO", "NASDAQ:MRVL", "NYSE:COHR", "NASDAQ:LITE", "NYSE:FN", "SZSE:300394", "SZSE:300308", "SZSE:300757"]
markets: [US, CN]
analysis_regimes: [a_share, us_equity]
policy_jurisdictions: [CN, US]
reporting_currencies: [CNY, USD]
asset_classes: [equity]
industries: [semiconductors, optical-components, data-center-networking]
themes: [AI infrastructure, co-packaged optics]
as_of: 2026-05-27
sources:
  - "[[broadcom-form-10-k-fy2025|Broadcom FY2025 Form 10-K]]"
  - "[[marvell-q1-fy2027-results-2026-05-27|Marvell FY2027 Q1 财务与业务结果（2026-05-27）]]"
  - "[[coherent-q3-fy2026-earnings-release|Coherent FY2026 Q3 Earnings Release]]"
  - "[[lumentum-form-10-q-fy2026-q3|Lumentum FY2026 Q3 Form 10-Q]]"
  - "[[fabrinet-form-10-q-fy2026-q3|Fabrinet FY2026 Q3 Form 10-Q]]"
  - "[[tfc-communication-q1-report-2026|天孚通信 2026 年第一季度报告]]"
  - "[[innolight-q1-report-2026|中际旭创 2026 年第一季度报告]]"
  - "[[robotechnik-annual-report-2025|罗博特科 2025 年年度报告]]"
created: 2026-07-27
updated: 2026-07-28
status: provisional
confidence: high
horizon: 12-24m
review_after: 2026-10-31
base_currency: "USD and CNY"
units: "as stated"
---

# CPO 公司财务基线与资本结构（2025–2026）

## 目的与范围

本页统一保存后续增长和估值模型的最新可核验财务起点。由于报告期、币种、会计准则和业务模式不同，不计算简单行业平均。

## 历史与最新输入

| 公司 | 期间 | 收入 | 利润率/利润 | 现金与投资 | 债务 | 股数 | CPO 单列 |
|---|---|---:|---|---:|---:|---:|---|
| Broadcom | FY2025 | US$63.887bn | 毛利 US$43.294bn | US$16.178bn | 本金 US$67.120bn | 约 4.741bn | 否 |
| Marvell | Q1 FY2027 | US$2.418bn | GAAP GM 52.1% | US$3.844bn | US$4.961bn | Q2 指引约 915m diluted | 否 |
| Coherent | Q3 FY2026 | US$1.806bn | GAAP GM 37.7% | US$2.418bn | 约 US$3.194bn | 约 190.2m weighted | 否 |
| Lumentum | Q3 FY2026 | US$808.4m | 毛利 US$357.0m | US$3.172bn | US$3.282bn | 71.5m basic / 96.2m diluted | 否 |
| Fabrinet | Q3 FY2026 | US$1.214bn | GM 11.9% | US$945.2m | 无披露借款 | 35.829m diluted | 否 |
| 天孚通信 | 2025 | 人民币 51.63 亿元 | 归母净利润 20.17 亿元 | 2026 Q1 货币资金 30.27 亿元 | Q1 无短/长期借款 | 777.416m | 否 |
| 中际旭创 | 2025 | 人民币 382.40 亿元 | 归母净利润 107.97 亿元 | 见年报/季报 | 见年报/季报 | 约 1.111bn | 否 |
| 罗博特科 | 2025 | 人民币 9.50 亿元 | 归母亏损 0.66 亿元 | 见年报 | 见年报 | 167.608m | 否 |

## 资本结构调整

### Broadcom

- 净债务较高，且公司含软件业务。
- SBC US$7.568bn，估值应使用完全稀释口径和 SOTP。

### Marvell

- Celestial AI 增加 27.2m 公告口径股份、现金对价、earnout 和费用。
- Q1 GAAP/非 GAAP 经营利润率 14%/35%，必须分别建模。

### Coherent

- NVIDIA US$2bn 投资的最终交割、股数和资本开支待后续申报。
- 当前债务和投资使 EV 与市值差异不可忽略。

### Lumentum

- 可转债和优先股使稀释股数显著高于基础股数。
- 估值不得使用 71.5m 基础股数替代 96.2m 稀释口径。

### Fabrinet

- 近似净现金，但制造毛利率约 12%，不能套用高毛利器件倍数。

### A 股公司

- 天孚通信和中际旭创需使用归母净利润、人民币口径和最新股本。
- 罗博特科需分开母公司、ficonTEC 部分年度并表、商誉和业绩补偿。

## 与最新披露勾稽

- 财务数字来自监管申报或正式季度报告。
- 所有公司均未单列 CPO 收入，因此后续公司 CPO 收入均为 `model_assumption`。
- 下一次财报后必须更新现金、债务、股数、SBC、营运资本和最新季度。

## 风险与局限

- 不同财政年度和季度不可直接同比。
- GAAP、non-GAAP、中国会计准则指标不可混用。
- 经营收入、归母净利润、EPS、FCF 和 EV 的币种与股数必须在估值日统一。
