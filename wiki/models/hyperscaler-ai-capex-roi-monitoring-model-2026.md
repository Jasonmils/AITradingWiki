---
page_type: model
subject: "Hyperscaler AI CAPEX—ROI 监测模型（2026）"
aliases:
  - "Hyperscaler AI CAPEX ROI Monitoring Model 2026"
  - "超大规模云服务商 AI 资本开支回报模型"
tags:
  - monitoring-model
  - ai-capex
  - ai-roi
tickers:
  - "NASDAQ:MSFT"
  - "NASDAQ:GOOGL"
  - "NASDAQ:AMZN"
  - "NASDAQ:META"
  - "NYSE:ORCL"
markets:
  - US
  - Global
  - China
analysis_regimes: [us_equity]
policy_jurisdictions: [US, EU, CN]
reporting_currencies: [USD]
asset_classes:
  - equity
industries:
  - internet
  - cloud-computing
  - semiconductors
  - data-center-infrastructure
themes:
  - AI CAPEX
  - AI ROI
  - hyperscalers
as_of: 2026-07-23
sources:
  - "[[microsoft-fy2026-q3-official-source-pack|Microsoft FY2026 Q3 官方披露资料包]]"
  - "[[alphabet-q2-2026-official-source-pack|Alphabet Q2 2026 官方披露资料包]]"
  - "[[amazon-q1-2026-official-source-pack|Amazon Q1 2026 官方披露资料包]]"
  - "[[meta-q1-2026-official-source-pack|Meta Q1 2026 官方披露资料包]]"
  - "[[oracle-q4-fy2026-official-source-pack|Oracle Q4/FY2026 官方披露资料包]]"
  - "[[jpmorgan-mid-year-investment-outlook-2026-06|J.P. Morgan Asset Management：2026 年中投资展望]]"
  - "[[citi-productivity-ai-revolution-2025-09-10|Citi：生产率的 AI 革命]]"
  - "[[morgan-stanley-mapping-ai-rate-of-change-2026-02-11|Morgan Stanley：映射 AI 变化率]]"
  - "[[bofa-ai-ten-secret-ingredients-2026-06-16|BofA：AI 的十种秘密原料]]"
created: 2026-07-27
updated: 2026-07-28
status: provisional
confidence: medium
horizon: 6-12m
review_after: 2026-08-31
base_currency: USD
units: "US$bn、百分比、百分点；按各表注明"
---

# Hyperscaler AI CAPEX—ROI 监测模型（2026）

## 目的与边界

本页把 AI 基础设施从资本开支计划连接到现金回报，作为滚动监测框架。2026-07-28 已加入五家公司最新官方财报与申报文件，但仍不虚构纯 AI capex 拆分、DCF、目标价或投资组合权重。

## 来源基线

| 指标 | 数值 | 期间 | 证据类型 | 来源 |
|---|---:|---|---|---|
| 五家美国 hyperscaler CAPEX | US$697bn | 2026E | market_consensus | J.P. Morgan |
| 年初以来 CAPEX 预测上调 | US$173bn | 2026E | market_consensus | J.P. Morgan |
| AI CAPEX / hyperscaler 经营现金流 | 33% | 2023 | source_opinion | J.P. Morgan |
| AI CAPEX / hyperscaler 经营现金流 | 93% | 2026E | market_consensus | J.P. Morgan |
| 支付 AI 订阅费的公司比例 | >50% | 2026 年中 | source_opinion | J.P. Morgan 引用 Ramp |
| 一年前支付比例 | 约 40% | 约 2025 年中 | source_opinion | J.P. Morgan 引用 Ramp |
| 半导体盈利增长 | 98% | 2026E | market_consensus | J.P. Morgan |

US$697bn 是时间敏感的市场一致预期，保留为历史基线，不被后续公司指引静默覆盖。

## 公司官方输入

| 公司 | 最新报告期 | 云/相关收入 | 2026 capex 指引或基线 | 最新现金回报 | 证据类型 | 来源 |
|---|---|---:|---:|---:|---|---|
| Microsoft | FY2026 Q3 | Microsoft Cloud US$54.5bn；Azure +40% | 约 US$190bn | Q3 FCF 约 US$15.8bn | verified_fact / company_statement | [[microsoft-fy2026-q3-official-source-pack|MSFT 资料包]] |
| Alphabet | Q2 2026 | Cloud US$24.8bn，利润 US$8.8bn | US$195–205bn | Q2 FCF 约 -US$5.9bn | verified_fact / company_statement | [[alphabet-q2-2026-official-source-pack|GOOGL 资料包]] |
| Amazon | Q1 2026 | AWS US$37.6bn，利润 US$14.2bn | 约 US$200bn（全公司） | TTM FCF 约 US$1.2bn | verified_fact / company_statement | [[amazon-q1-2026-official-source-pack|AMZN 资料包]] |
| Meta | Q1 2026 | 公司收入 US$56.31bn；AI 增量未单列 | US$125–145bn | Q1 FCF US$12.39bn | verified_fact / company_statement | [[meta-q1-2026-official-source-pack|META 资料包]] |
| Oracle | FY2026 | OCI US$18.1bn | FY2026 capex US$55.7bn；上升趋势继续 | FY2026 FCF 约 -US$23.7bn | verified_fact / company_statement | [[oracle-q4-fy2026-official-source-pack|ORCL 资料包]] |

### 四家公司 2026 capex 指引机械加总

Microsoft、Alphabet、Amazon、Meta 的最新公司指引合计为：

`US$190bn + US$195–205bn + US$200bn + US$125–145bn = US$710–740bn`

- 证据类型：`codex_inference`
- 不是纯 AI capex；Amazon 为全公司口径，Meta 含融资租赁本金，Microsoft 另披露融资租赁。
- Oracle 的财年、租赁、客户供货 GPU 和融资结构不同，未纳入机械加总。
- 该结果不能与 J.P. Morgan 的五家公司 US$697bn `market_consensus` 做无调整差额解释。

## 资本开支口径桥

| 层级 | Microsoft | Alphabet | Amazon | Meta | Oracle |
|---|---|---|---|---|---|
| 现金 PP&E | 单列 | 单列 | 强调 PP&E 购买 | 需与总 capex 勾稽 | 单列 |
| 融资租赁 | Q3 US$4.7bn | 未用同一口径披露 | FCF 不完整包含 | capex 定义包含本金 | 大量租赁承诺 |
| 客户供货设备 | OpenAI 相关需核验 | TPU 系统销售另行识别 | 未单列 | 未单列 | 大型 AI 合同中重要 |
| 未入表承诺 | 需按 10-Q 更新 | 需按 10-Q 更新 | 租赁/采购承诺 | 租赁/采购承诺 | 约 US$260bn 租赁承诺 |
| 纯 AI 比例 | 未披露 | 未披露 | 未披露 | 未披露 | 未披露 |

## 回报链

`CAPEX 指引 → 正式订单 → 设备交付 → 数据中心投运 → 可用容量 → 利用率 → 付费使用 → AI 收入 → 增量毛利 → 经营现金流 → 自由现金流`

每一层都需要独立证据。报告中的 US$697bn 是资本开支预期，不等同于已下单、已交付或已形成收入。

## 监测表

| 层级 | 关键指标 | 正向证据 | 警戒信号 |
|---|---|---|---|
| CAPEX | 指引、同比、占经营现金流 | 上调且现金流同步增长 | CAPEX 增速远高于经营现金流 |
| 订单 | 供应商订单、backlog | 多客户、可取消性低 | 单一客户、推迟或取消 |
| 投运 | 上架容量、电力、网络 | 按期投运 | 电力、材料、设备交期限制 |
| 利用 | GPU/加速器利用率 | 稳定提升 | 闲置、折扣、云价格下跌 |
| 付费 | 客户数、用量、续费、ARPU | 用量和留存同时增长 | 只增试用或席位 |
| 收入 | AI 云/模型/软件收入 | 可量化且增速稳定 | 披露模糊、收入重分类 |
| 利润 | 增量毛利、费用率 | 毛利覆盖折旧和研发 | 价格竞争、折旧上升 |
| 现金 | 经营/自由现金流 | 自由现金流回升 | 现金流持续被 CAPEX 压制 |

## 三种状态

| 状态 | 判定 | 含义 |
|---|---|---|
| 回报兑现 | 利用率、付费用量、收入、毛利和自由现金流同步改善 | CAPEX 已逐步穿透到现金回报 |
| 建设领先 | 订单与投运强，但付费和现金回报落后 | 景气仍在，但回报时滞扩大 |
| 资本过度 | CAPEX 继续上升，利用率、价格、收入和现金流恶化 | 供给领先需求或竞争侵蚀回报 |

当前状态标为 `provisional`：官方财报支持“建设领先、云收入增长、现金回报分化”。Microsoft、Meta 仍有较强 FCF；Alphabet 单季、Amazon TTM 与 Oracle FY 的 FCF 更受建设压制。由于纯 AI capex、利用率和增量毛利未完整披露，尚不足以确认行业整体“回报兑现”。

## 公司级回报判定

| 公司 | 当前状态 | 支持证据 | 尚缺证据 |
|---|---|---|---|
| Microsoft | 建设领先，部分回报兑现 | Azure +40%、Cloud 收入和 FCF | AI ARR 增量毛利、OpenAI 影响 |
| Alphabet | 收入与利润加速，现金建设领先 | Cloud +82%、利润率 35.6% | TPU 系统销售拆分、持续 FCF |
| Amazon | 建设领先，现金回报滞后 | AWS +28%、营业利润强 | AWS/非 AWS capex、融资租赁 |
| Meta | 广告现金流覆盖大部分建设 | 收入 +33%、利润率 41%、FCF 正 | AI 广告增量归因、折旧滞后 |
| Oracle | 合同领先，融资与现金压力高 | RPO US$638bn、OCI +77% | 长期确认率、租赁、稀释和 FCF |

## 上游与材料约束

[[bofa-ai-ten-secret-ingredients-2026-06-16|BofA：AI 的十种秘密原料]]提示关键材料和设备交期可能约束投运。材料短缺会：

- 延后设备交付与收入确认；
- 推高建设成本；
- 使 CAPEX 计划与实际可用容量偏离；
- 在部分环节形成价格上行，但不保证上市公司利润受益。

## 采用者侧交叉验证

[[morgan-stanley-mapping-ai-rate-of-change-2026-02-11|Morgan Stanley：映射 AI 变化率]]显示 AI 收益当前更多来自成本效率。对 hyperscaler ROI 的交叉验证应观察：

- 客户是否从试点转生产；
- 客户能否量化成本或收入收益；
- 订阅之外的使用量和续费；
- 采用者利润率是否在行业中性后改善。

## 失效条件

- hyperscaler 下调 CAPEX 或项目延期，同时供应商订单恶化。
- AI 云和模型价格下降快于单位成本。
- 利用率、付费使用和续费无法跟上投运容量。
- CAPEX 占经营现金流持续高位，自由现金流显著恶化。
- 半导体盈利增长预期下修，库存和价格周期转弱。
- RPO/backlog 增长但未来 12 个月收入确认比例持续下降。
- 融资租赁、未入表租赁和客户供货设备使 headline capex 低估真实资本承诺。

## 当前可交易性边界

本模型没有当前股价、逐公司估值、最新财报或风险预算，不能回答具体证券是否值得交易。完成交易判断前需按 Entity/个股重建收入、利润、现金流和估值。

## 变更记录

- 2026-07-28：加入五家云厂商最新官方财报、申报和电话会材料；建立 capex 口径桥与公司级现金回报判定，保留 US$697bn 市场一致预期历史基线。
- 2026-07-27：以 2026 年中来源基线建立 provisional 监测模型；未创建虚构的 hyperscaler 公司拆分或估值。
