---
page_type: model
subject: "Citi 美国 AI 生产率情景模型（2025）"
aliases:
  - "Citi US AI Productivity Scenario Model 2025"
  - "美国 AI 生产率情景"
tags:
  - third-party-model
  - ai-productivity
  - macroeconomics
tickers: []
markets:
  - US
analysis_regimes: [us_equity]
policy_jurisdictions: [US]
reporting_currencies: [USD]
asset_classes:
  - equity
  - rates
  - fx
industries:
  - diversified-industries
themes:
  - AI productivity
  - AI adoption
  - macro transmission
as_of: 2025-09-10
sources:
  - "[[citi-productivity-ai-revolution-2025-09-10|Citi：生产率的 AI 革命]]"
created: 2026-07-27
updated: 2026-07-28
status: provisional
confidence: low
horizon: 3-5y
review_after: 2026-09-30
base_currency: USD
units: "百分比、百分点、US$bn；按各表注明"
---

# Citi 美国 AI 生产率情景模型（2025）

## 目的与边界

本页保存[[citi-productivity-ai-revolution-2025-09-10|Citi：生产率的 AI 革命]]中的宏观情景，并给出可复核的机械桥接。它是第三方模型档案，不代表 Wiki 已采纳预测。

模型回答“如果任务可自动化比例和单位任务节省达到来源假设，潜在生产率增益是多少”，不回答具体公司利润或当前资产价格。

## 核心公式

`潜在生产率水平增益 ≈ 可自动化任务占比 × 每项自动化任务的劳动力成本节省`

该简化公式忽略：

- 模型、云、数据、集成、监督和返工成本；
- 被节省劳动力是否重新配置；
- 行业之间的任务权重和采用速度；
- 资本深化、宏观需求、竞争和价格传导；
- 技术收益是否重复计算。

## 情景输入与机械输出

| 情景 | 可自动化任务 | 单任务劳动力成本节省 | 机械乘积 | 来源分类 |
|---|---:|---:|---:|---|
| 保守 | 20% | 30% | 6.0% | model_assumption |
| 中点 | 30% | 35% | 10.5% | codex_inference，仅为区间中点 |
| 乐观 | 40% | 40% | 16.0% | model_assumption |

6% 和 16% 是 Citi 区间端点；10.5% 是为了可复核性而给出的机械中点，不是 Citi 明示的基准情景。

## 来源给出的扩散速度

| 指标 | 保守端 | 乐观端 | 期间 | 证据类型 |
|---|---:|---:|---|---|
| 生产率水平增益 | 6% | 16% | 长期 | model_assumption |
| 年均生产率增速增量 | 0.5ppt | 1.5ppt | 约十年扩散 | model_assumption |

简单把 6%–16% 除以十年会得到约 0.6–1.6ppt/年；Citi 报告给出的正式区间是 0.5–1.5ppt/年。本页保留报告口径，不以机械除法替换。

## 当前投资脉冲输入

| 指标 | 2023Q4 | 2024Q4 | 2025Q2 | 币种/单位 | 证据类型 |
|---|---:|---:|---:|---|---|
| AI 相关投资，年化 | 60 | 150 | 255 | USD / US$bn | source_opinion |

报告估算 AI 投资对总需求的脉冲约为 20–40bp。该项是短期需求效应，不等同于长期生产率供给效应。

## 采用率约束

来源称仅约 5% 的 GenAI 项目已全面规模化。模型因此必须区分：

1. 技术可自动化比例；
2. 企业开始试点的比例；
3. 生产部署比例；
4. 实际任务覆盖率；
5. 扣除全部成本后的净节省。

若只观察第一项，模型会系统性高估近期宏观影响。

## 宏观传导

| 变量 | 来源的方向性观点 | 主要抵消项 |
|---|---|---|
| 实际增长 | 上升 | 扩散时滞、组织重构 |
| 实际利率 | 上升 | 货币政策、储蓄和风险偏好 |
| 美元 | 偏强 | 相对生产率、政策与估值 |
| 黄金 | 偏弱 | 地缘风险、央行需求、实际利率 |
| 股票 | 偏强 | 起始估值、利润归属、资本成本 |

以上全部是条件性 `source_opinion`，不能直接形成仓位。

## 验证与更新清单

- 美国行业与宏观劳动生产率是否出现广泛且持续的上修。
- 生产部署比例是否明显高于 5%。
- 企业披露的单位任务净节省，是否扣除模型、集成和监督成本。
- 采用者利润率改善是否在行业中性后仍然存在。
- AI 投资是否从 CAPEX 继续传导到付费使用、收入和自由现金流。

## 失效条件

- 企业规模化采用长期停滞。
- 单位任务净收益接近零或为负。
- 宏观生产率在多个行业和多个年度均无加速。
- 所谓效率收益主要来自裁员、周期或价格，而非 AI 工作流。
- 资产价格已完全反映乐观端，导致基本面兑现仍无法提供合理回报。

## 变更记录

- 2026-07-27：按来源区间建立 provisional 情景档案；新增的 10.5% 中点明确标为 `codex_inference`，未把来源预测升级为事实。
