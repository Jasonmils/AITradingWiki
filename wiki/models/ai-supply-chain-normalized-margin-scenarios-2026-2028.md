---
page_type: model
subject: "AI 算力供应链正常化利润率情景（2026–2028）"
tags: [model, normalized-margin, ai-infrastructure, semiconductors]
tickers: ["NASDAQ:NVDA", "NASDAQ:AMD", "TWSE:2330", "NYSE:TSM", "NASDAQ:MU", "NASDAQ:ASML", "Euronext:ASML", "NASDAQ:AMAT"]
markets: [US, TW, NL, Global]
analysis_regimes: [us_equity, cross_market, other]
policy_jurisdictions: [US, TW, EU, CN]
reporting_currencies: [USD, TWD, EUR]
asset_classes: [equity]
industries: [semiconductors, memory, foundry, semiconductor-equipment]
themes: [AI infrastructure, margins, cycle normalization]
as_of: 2026-07-16
sources:
  - "[[nvidia-q1-fy2027-official-source-pack|NVIDIA Q1 FY2027 官方披露资料包]]"
  - "[[amd-q1-2026-official-source-pack|AMD Q1 2026 官方披露资料包]]"
  - "[[tsmc-q2-2026-official-source-pack|TSMC Q2 2026 官方披露资料包]]"
  - "[[micron-q3-fy2026-official-source-pack|Micron Q3 FY2026 官方披露资料包]]"
  - "[[asml-q2-2026-official-source-pack|ASML Q2 2026 官方披露资料包]]"
  - "[[applied-materials-q2-fy2026-official-source-pack|Applied Materials Q2 FY2026 官方披露资料包]]"
created: 2026-07-28
updated: 2026-07-28
status: provisional
confidence: low
horizon: 12-24m
review_after: 2026-10-31
base_currency: USD
units: "百分比、百分点；ASML 原始财务为 EUR，TSMC 部分为 NT$"
---

# AI 算力供应链正常化利润率情景（2026–2028）

## 目的与范围

把当前报告利润率拆成结构性因素、周期因素、会计/基数因素和产品 mix，避免把景气高点直接资本化为长期估值。公开资料不足以给出精确长期利润率，故本页采用方向性情景而非点估计。

## 最新报告输入

| 公司 | 最新利润指标 | 期间 | 主要调整 | 证据类型 |
|---|---:|---|---|---|
| NVIDIA | GAAP 毛利率 74.9% | Q1 FY2027 | 上年 H20 US$4.5bn 费用基数；non-GAAP SBC 口径变化 | verified_fact |
| AMD | GAAP 毛利率 53% | Q1 2026 | Data Center CPU/GPU mix；收购摊销的 non-GAAP 调整 | verified_fact |
| TSMC | 毛利率 67.7% | Q2 2026 | 先进节点 mix、汇率、海外厂与 TIFRS | verified_fact |
| Micron | GAAP 毛利率 84.6% | Q3 FY2026 | 存储 ASP 周期、HBM mix、客户长协 | verified_fact |
| ASML | 毛利率 54.0% | Q2 2026 | 新系统/installed base mix、验收时点 | verified_fact |
| AMAT | GAAP 毛利率 49.9% | Q2 FY2026 | 分部重述；投资收益影响利润而非毛利 | verified_fact |

## 正常化桥

`报告利润率`

`- 一次性费用/收益与异常基数`

`- 周期性 ASP 超额`

`- 暂时性供给溢价`

`+ 可持续产品 mix/规模效率`

`- 海外厂、扩产、折旧与研发负担`

`= 正常化利润率区间`

该桥是 `codex_inference` 框架；缺少可审计数据时不填数字。

## 公司级驱动

| 公司 | 结构性支撑 | 正常化下行风险 | 关键验证 |
|---|---|---|---|
| NVIDIA | 全栈平台、accelerator/networking mix | 竞争、出口、客户集中、供应价格 | 新框架毛利、库存与供给承诺 |
| AMD | Data Center mix 提升 | 规模、软件、采购承诺和竞争定价 | MI450 订单/出货及毛利 |
| TSMC | 先进节点、技术领先 | 海外厂成本、汇率、客户议价 | 2nm 良率、capex 和毛利 |
| Micron | HBM mix、长协 | 存储 ASP 周期反转、供给扩张 | ASP、bit shipment、库存、毛利 |
| ASML | EUV 稀缺性、installed base | 验收时点、出口、扩产成本 | 系统 mix、订单取消和服务收入 |
| AMAT | foundry/logic 与 DRAM 扩产 | WFE 周期、出口、分部重述 | 订单、OCF、重述后分部利润 |

## 三种情景

| 情景 | accelerator | memory | foundry | equipment | 估值含义 |
|---|---|---|---|---|---|
| 保守 | 竞争导致 ASP/毛利下降 | 供给扩张、ASP 回落 | 海外厂稀释 | 客户验收延后 | 当前高利润不能资本化 |
| 基准 | 高端 mix 抵消部分降价 | HBM 强、普通 DRAM 正常化 | 先进节点支撑 | 订单按期转收入 | 使用周期中枢利润率 |
| 乐观 | 平台定价权延续 | HBM 供给持续紧张 | 2nm ramp 顺利 | EUV/WFE 提前确认 | 高利润更具持续性 |

情景只给方向，不给未经证据支持的点估计。

## 利润质量检查

| 检查项 | 正向信号 | 预警 |
|---|---|---|
| 毛利率与现金流 | 同步改善 | 毛利高但 OCF/FCF 弱 |
| 库存与应收 | 不高于收入增速 | 连续快于收入 |
| 价格与销量 | 量增、价格稳定 | 价格下跌抵消出货 |
| 客户集中 | 多客户扩散 | 单一客户/项目依赖 |
| capex 与折旧 | 回报覆盖 | 扩产后利用率不足 |
| 会计口径 | 可比且稳定 | 重述、一次性收益或非 GAAP 变化 |

## 与最新披露结果的勾稽

- NVIDIA：需剔除 H20 基数并适配新分部/non-GAAP 口径。
- Micron：84.6% 毛利率明确作为周期高位，不做长期默认。
- TSMC：先进节点 mix 支撑高毛利，但海外厂与汇率待验证。
- ASML：订单与收入之间保留验收概率。
- AMAT：投资收益不进入经营利润率正常化，分部比较使用重述数据。

## 风险、局限与失效条件

- 缺少产品级 ASP、BoM、良率、RMA 和客户价格条款。
- 报告期、币种和会计准则不统一。
- 若后续披露显示高利润来自可持续合同和技术优势，可提高基准区间；若库存、ASP 和取消恶化，切换保守情景。
- 当前模型不包含当前价格或估值倍数，不能形成交易结论。

## 变更记录

- 2026-07-28：建立首版供应链正常化利润率框架；所有缺失点估计保持 `model_assumption`。
