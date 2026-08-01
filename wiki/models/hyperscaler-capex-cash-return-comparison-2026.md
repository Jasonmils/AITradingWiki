---
page_type: model
subject: "Hyperscaler 资本开支与现金回报比较（2026）"
tags: [model, ai-capex, cash-flow, cloud]
tickers: ["NASDAQ:MSFT", "NASDAQ:GOOGL", "NASDAQ:AMZN", "NASDAQ:META", "NYSE:ORCL"]
markets: [US]
analysis_regimes: [us_equity]
policy_jurisdictions: [US, EU, CN]
reporting_currencies: [USD]
asset_classes: [equity]
industries: [cloud-computing, internet, software, data-center-infrastructure]
themes: [AI CAPEX, AI ROI, free cash flow]
as_of: 2026-07-23
sources:
  - "[[microsoft-fy2026-q3-official-source-pack|Microsoft FY2026 Q3 官方披露资料包]]"
  - "[[alphabet-q2-2026-official-source-pack|Alphabet Q2 2026 官方披露资料包]]"
  - "[[amazon-q1-2026-official-source-pack|Amazon Q1 2026 官方披露资料包]]"
  - "[[meta-q1-2026-official-source-pack|Meta Q1 2026 官方披露资料包]]"
  - "[[oracle-q4-fy2026-official-source-pack|Oracle Q4/FY2026 官方披露资料包]]"
created: 2026-07-28
updated: 2026-07-28
status: provisional
confidence: medium
horizon: 12-24m
review_after: 2026-10-31
base_currency: USD
units: "US$bn、百分比；原始口径另行注明"
---

# Hyperscaler 资本开支与现金回报比较（2026）

## 目的与范围

本模型比较 Microsoft、Alphabet、Amazon、Meta、Oracle 的资本开支、云业务增长与现金回报。它不把全公司 capex 当作纯 AI 投入，也不把 backlog/RPO 当作收入。

## 历史与最新输入

| 公司 | 指标 | 期间 | 数值 | 证据类型 | 来源 |
|---|---|---|---:|---|---|
| Microsoft | 收入 | FY2026 Q3 | US$82.9bn | verified_fact | [[microsoft-fy2026-q3-official-source-pack|MSFT]] |
| Microsoft | Microsoft Cloud 收入 | FY2026 Q3 | US$54.5bn | verified_fact | [[microsoft-fy2026-q3-official-source-pack|MSFT]] |
| Microsoft | Q3 cash PP&E / 融资租赁 | FY2026 Q3 | US$30.9bn / US$4.7bn | verified_fact | [[microsoft-fy2026-q3-official-source-pack|MSFT]] |
| Alphabet | Cloud 收入 / 营业利润 | Q2 2026 | US$24.8bn / US$8.8bn | verified_fact | [[alphabet-q2-2026-official-source-pack|GOOGL]] |
| Alphabet | capex / FCF | Q2 2026 | US$44.9bn / -US$5.9bn | verified_fact / codex_inference | [[alphabet-q2-2026-official-source-pack|GOOGL]] |
| Amazon | AWS 收入 / 营业利润 | Q1 2026 | US$37.6bn / US$14.2bn | verified_fact | [[amazon-q1-2026-official-source-pack|AMZN]] |
| Amazon | PP&E 购买 / FCF | TTM Q1 2026 | US$147.3bn / US$1.2bn | verified_fact / company-defined | [[amazon-q1-2026-official-source-pack|AMZN]] |
| Meta | 收入 / 营业利润率 | Q1 2026 | US$56.31bn / 41% | verified_fact | [[meta-q1-2026-official-source-pack|META]] |
| Meta | capex / FCF | Q1 2026 | US$19.84bn / US$12.39bn | verified_fact | [[meta-q1-2026-official-source-pack|META]] |
| Oracle | OCI 收入 / FCF | FY2026 | US$18.1bn / -US$23.7bn | verified_fact / company-defined | [[oracle-q4-fy2026-official-source-pack|ORCL]] |
| Oracle | capex / 未入表租赁承诺 | FY2026/期末 | US$55.7bn / 约 US$260bn | verified_fact | [[oracle-q4-fy2026-official-source-pack|ORCL]] |

## 指引输入

| 公司 | 2026 capex 指引或基线 | 口径 | 证据类型 | 置信度 |
|---|---:|---|---|---|
| Microsoft | 约 US$190bn | 2026 自然年；另有融资租赁 | company_statement | medium |
| Alphabet | US$195–205bn | 2026 年；服务器约 60% | company_statement | medium |
| Amazon | 约 US$200bn | 全公司，非纯 AWS/AI | company_statement | medium |
| Meta | US$125–145bn | 含融资租赁本金 | company_statement | medium |
| Oracle | 未给可直接比较的 2026 自然年区间 | FY2026 capex US$55.7bn；未来上升 | verified_fact / company_statement | low-comparability |

## 口径调整桥

`报告 capex + 融资租赁新增资产 + 尚未开始租赁的承诺 + 客户供货/预付设备调整 = 经济资本承诺`

该等式是框架，不是已完成的数值计算。缺失输入保持 `model_assumption` 或空白。

| 调整项 | 重要性 | 数据状态 |
|---|---|---|
| 现金 PP&E | 所有公司 | 已部分披露 |
| 融资租赁新增资产及本金 | MSFT/META/AMZN | 口径不统一 |
| 尚未入表租赁 | ORCL 最显著 | ORCL 已披露约 US$260bn |
| 客户供货 GPU/预付款 | ORCL 重要 | 金额拆分不足 |
| 非 AI 资本开支 | AMZN/META/GOOGL/MSFT | 纯 AI 比例未披露 |

## 回报质量评分框架

| 维度 | 低风险 | 中性 | 高风险 |
|---|---|---|---|
| 云收入增长 | 加速且可比 | 高但有 mix 变化 | 放缓或重分类 |
| 云营业利润 | 同步改善 | 改善低于收入 | 利润率下降 |
| capex/OCF | 稳定或下降 | 快速上升但 OCF 增长 | capex 接近/超过 OCF |
| FCF | 正且改善 | 正但下降 | 负或接近零 |
| backlog/RPO | 短期可确认、多客户 | 中长期 | 长期、集中、融资复杂 |
| 折旧与租赁 | 被增量毛利覆盖 | 尚待验证 | 增长快于毛利 |

## 三种情景

| 情景 | model_assumption | 可观察结果 |
|---|---|---|
| 保守 | 云增速下行、价格竞争、利用率低；折旧和租赁快速上升 | FCF 持续承压，供应链订单后移 |
| 基准 | 云收入保持较高增长；新增容量逐步投运，毛利覆盖大部分折旧 | FCF 在 12–24 个月企稳 |
| 乐观 | AI 用量和软件变现加速，单位算力成本下降快于价格 | 云利润和 FCF 同步扩张 |

## 与最新披露结果的勾稽

- Microsoft、Meta：仍有明显正 FCF，但需要观察折旧滞后。
- Alphabet：Cloud 利润加速，单季 FCF 转负，TPU system mix 需拆分。
- Amazon：AWS 利润强，TTM FCF 接近零；全公司 capex 口径最难拆。
- Oracle：RPO 最强、期限最长，FCF、租赁与融资压力也最显著。

## 风险、局限与失效条件

- 不同财年、自由现金流和租赁定义使横向排名只能作方向性比较。
- 缺少纯 AI capex、容量利用率、AI 增量毛利和折旧资产组。
- 若使用本模型做估值，必须重新核验当前价格、净债务、股数和一致预期。
- 任一公司后续重述 cloud/AI 指标或 capex 定义，须回溯更新。

## 变更记录

- 2026-07-28：基于五家公司最新官方披露建立首版 capex—现金回报比较；未给目标价或现价交易结论。
