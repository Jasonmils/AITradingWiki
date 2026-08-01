---
page_type: synthesis
synthesis_type: comparison
subject: "云厂商与算力供应链比较（2026）"
tags: [synthesis, comparison, cloud, ai-infrastructure]
tickers: ["NASDAQ:MSFT", "NASDAQ:GOOGL", "NASDAQ:AMZN", "NASDAQ:META", "NYSE:ORCL", "NASDAQ:NVDA", "NASDAQ:AMD", "TWSE:2330", "NASDAQ:MU", "NASDAQ:ASML", "NASDAQ:AMAT"]
markets: [US, TW, NL, Global]
analysis_regimes: [us_equity, cross_market, other]
policy_jurisdictions: [US, TW, EU, CN]
reporting_currencies: [USD, TWD, EUR]
asset_classes: [equity]
industries: [cloud-computing, semiconductors, memory, foundry, semiconductor-equipment]
themes: [AI CAPEX, AI ROI, AI infrastructure]
as_of: 2026-07-23
sources:
  - "[[hyperscaler-capex-cash-return-comparison-2026|Hyperscaler 资本开支与现金回报比较（2026）]]"
  - "[[ai-compute-supply-capacity-revenue-bridge-2026-2028|AI 算力供给容量—收入桥（2026–2028）]]"
  - "[[ai-supply-chain-normalized-margin-scenarios-2026-2028|AI 算力供应链正常化利润率情景（2026–2028）]]"
created: 2026-07-28
updated: 2026-07-28
status: provisional
confidence: medium
horizon: 12-24m
review_after: 2026-10-31
---

# 云厂商与算力供应链比较（2026）

## 结论与知识截止日

截至 2026-07-23，AI 基础设施投入和上游收入仍在加速，但投资链已经从“是否建设”转向“谁先确认收入、谁承担现金流、谁能维持正常化利润率”。行业研究优先级高；当前价格是否值得交易仍未完成。

## 因果链

`云厂商 capex/租赁 → accelerator/network 订单 → HBM/wafer/packaging → EUV/WFE → 出货/验收 → 云容量投运 → 付费使用 → 云收入/利润 → FCF`

上游供应商可以在云厂商 FCF 兑现前确认收入；这解释了“供应链盈利强、购买方现金回报分化”，但不保证上游利润率永久维持高位。

## 云厂商比较

| 公司 | 收入兑现 | 资本投入 | 现金回报 | 当前证据状态 |
|---|---|---|---|---|
| Microsoft | Azure +40%；AI ARR >US$37bn | 2026 capex 约 US$190bn | Q3 FCF 正 | 部分回报兑现；AI ARR 边界不清 |
| Alphabet | Cloud +82%、利润率 35.6% | US$195–205bn | Q2 FCF 负 | 利润兑现、现金建设领先；TPU mix |
| Amazon | AWS +28%、营业利润强 | 约 US$200bn 全公司 | TTM FCF 接近零 | 建设领先；AWS/非 AWS 难拆 |
| Meta | 收入 +33%、利润率 41% | US$125–145bn | Q1 FCF 正 | 广告现金流覆盖；AI 增量未单列 |
| Oracle | OCI +77%、RPO US$638bn | capex/租赁/融资强 | FY FCF 负 | 合同领先；融资与长期确认风险最高 |

## 供应链比较

| 公司 | 链条位置 | 最新兑现 | 关键非共识变量 | 最大估值风险 |
|---|---|---|---|---|
| NVIDIA | accelerator/network | Data Center US$75.2bn | 网络与系统 mix 可否抵消 chip 竞争 | 出口、客户集中、毛利正常化 |
| AMD | accelerator/CPU | Data Center US$5.8bn | MI450/Meta 是否从规划转订单 | 执行、软件、采购承诺 |
| TSMC | foundry | 先进节点 77% | 2nm 与 AI mix 能否覆盖海外厂稀释 | 地缘、客户集中、汇率 |
| Micron | HBM/memory | 毛利率 84.6% | 长协是否延长周期、HBM mix 是否结构化 | ASP 周期反转 |
| ASML | lithography | Q2 €9.3bn；2027 订单覆盖 | EUV 稀缺性与验收节奏 | 出口、客户延期、扩产 |
| AMAT | WFE/packaging | Semi Systems US$5.965bn | 先进封装和 memory 扩产持续性 | WFE 周期、重述和 FCF |

## 共识

| 判断 | 证据类型 | 置信度 |
|---|---|---|
| 2026 AI/data-center 建设仍强。 | market_consensus + company_statement | high |
| accelerator、HBM、先进制程和设备收入均已受益。 | verified_fact | high |
| 云收入正在加速，终端 ROI 仍需继续验证。 | codex_inference | high |
| 出口、电力、HBM、先进封装和设备交期是主要约束。 | company_statement | medium-high |

## 非共识与待验证

| 判断 | 证据类型 | 支持逻辑 | 失效条件 |
|---|---|---|---|
| 云厂商的估值分化将更多由 FCF/租赁而非云收入增速决定。 | non_consensus | capex 与现金回报已分化 | FCF 快速同步改善 |
| Oracle RPO 的估值质量低于相同金额的短期、现金轻合同。 | codex_inference | 确认期长、租赁和融资复杂 | 预付款覆盖资金且确认提前 |
| Micron 当前利润率不应按结构性稳态资本化。 | non_consensus | 存储价格周期显著 | 长协锁定价格且供给持续紧张 |
| 上游最优研究对象未必是收入增速最高者，而是正常化 FCF 兑现最清晰者。 | non_consensus | 估值取决于利润质量和资本强度 | 高增速长期转化为稳定 FCF |

## 公司里程碑不得混用

| 里程碑 | 示例 | 当前可确认 |
|---|---|---|
| roadmap/sampling | NVIDIA Rubin、AMD MI450、Micron HBM4E | 产品计划或样品 |
| capacity/contract | AMD/Meta 6GW、Oracle RPO、ASML 订单覆盖 | 需求可见度 |
| shipment/production | Micron HBM4 HVM、accelerator 出货 | 供给输出 |
| recognized revenue | Cloud/OCI/Data Center/设备收入 | 会计收入 |
| profit/FCF | 分部利润、OCF、FCF | 股东回报前置指标 |

## 催化剂

- 云厂商后续季度 capex、折旧、Cloud/AWS/OCI 利润和 FCF。
- AMD MI450 正式订单/交付；NVIDIA Rubin/新披露框架。
- Micron HBM4/HBM4E 客户认证、ASP 与长协执行。
- TSMC 2nm ramp、先进封装和海外厂毛利。
- ASML 订单、验收和中国许可证；AMAT 重述后分部和 OCF。

## 风险

- 云需求增速低于容量增长，利用率和价格下降。
- 客户双重预订、订单延后或取消。
- 存储与设备周期反转。
- 出口控制和地缘事件改变可服务市场。
- 会计口径、一次性收益和租赁使 headline 指标失真。

## 失效条件

- 云 capex 下调且供应商订单/收入同步恶化。
- 云收入加速但连续多个季度无法覆盖折旧、租赁和 capex。
- 上游库存、应收和采购承诺持续快于收入。
- 规划/订单未按期进入交付、收入和 FCF。

## 当前价格可交易性

未核验同一时点的股价、EV、完全稀释股数、一致预期与拥挤度。本页只确定研究优先级与证据链，不给买卖结论。

## 证据缺口

- 纯 AI capex、利用率、产品级 ASP/BoM/yield 和云端增量毛利。
- 多家公司官方电话会文字稿缺失。
- 各市场币种、会计期和风险溢价未统一。

## 变更记录

- 2026-07-28：基于 11 家公司最新官方材料建立云—算力供应链比较。
