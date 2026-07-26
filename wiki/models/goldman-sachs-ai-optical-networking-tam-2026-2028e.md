---
page_type: model
subject: "高盛 AI 光网络 TAM 与 CPO 渗透模型（2026-2028E）"
aliases:
  - "Goldman Sachs AI Optical Networking TAM and CPO Adoption Model 2026–2028E"
  - "高盛 AI 光网络 TAM 与 CPO 渗透模型（2026–2028E）"
tags:
  - third-party-model
  - tam
  - co-packaged-optics
  - optical-networking
tickers:
  - "NASDAQ:NVDA"
  - "NASDAQ:AVGO"
  - "NASDAQ:MRVL"
markets:
  - US
asset_classes:
  - equity
industries:
  - semiconductors
  - optical-components
  - data-center-networking
themes:
  - AI infrastructure
  - co-packaged optics
  - silicon photonics
as_of: 2026-04-17
sources:
  - "[[goldman-sachs-global-tech-optical-networking-2026-04-17|高盛全球科技：光网络（2026-04-17）]]"
created: 2026-07-24
updated: 2026-07-24
status: provisional
confidence: low
horizon: 12-24m
review_after: 2026-10-17
base_currency: USD
units: "US$m unless stated"
---

# 高盛 AI 光网络 TAM 与 CPO 渗透模型（2026–2028E）

## 目的与范围

本页保存[[goldman-sachs-global-tech-optical-networking-2026-04-17|高盛全球科技：光网络（2026-04-17）]]中的第三方市场模型，**不是** Wiki 已采纳的预测。

报告建模内容包括：

- 机架网络连接价值量；
- scale-up 与 scale-out TAM；
- CPO 渗透率与交换机数量；
- 光模块、光引擎/FAU、ELS、光纤/MPO 和 shufflebox 的组件价值量；
- 相关硅光渗透率与模块成本假设。

报告提供高端 Spec B 和低端 Spec A 情景，但没有提供完整独立的基准情景、公司利润表、现金流模型、目标价或估值敏感性分析。

## 历史输入

报告未包含经审计的历史财务报表。1Q24 硅光渗透率起点被归因于“Global Optical Module TAM”，但未附底层数据集。

| 指标 | 业务板块 | 期间 | 数值 | 币种 | 单位 | 证据类型 | 来源 |
|---|---|---|---:|---|---|---|---|
| 硅光渗透率 | 数据通信光模块 | 1Q24 | 6 | — | % | source_opinion | 来源报告第 17–18 页 Exhibit 26 |

## 核心假设

| 假设 | 业务板块 | 情景 | 数值 | 期间 | 币种 | 单位 | 证据类型 | 来源 | 置信度 |
|---|---|---|---:|---|---|---|---|---|---|
| NVIDIA AI 机架出货量 | 所有建模机架 | 报告高低端情景 | 50 / 77 / 121 | 2026E / 2027E / 2028E | — | 千台机架 | model_assumption | 来源报告第 11 页 Exhibits 10–11 | low |
| Scale-out CPO 渗透率 | 高端 Spec B | high | 5 / 25 / 29 | 2026E / 2027E / 2028E | — | % | model_assumption | 来源报告第 11 页 Exhibit 11 | low |
| Scale-out CPO 渗透率 | 低端 Spec A | low | 0 / 11 / 27 | 2026E / 2027E / 2028E | — | % | model_assumption | 来源报告第 11 页 Exhibit 11 | low |
| 单台 scale-out CPO 交换机的光引擎数量 | CPO 交换机 | 高低端情景 | 72 | 2026E–2028E | — | 个/台交换机 | model_assumption | 来源报告第 11 页 Exhibit 11 注释 | low |
| GB300 全生命周期机架出货量 | GB300 NVL72 | 报告情景 | 48 | 2H25–2026 | — | 千台机架 | model_assumption | 来源报告第 10 页 Exhibit 8 | low |
| Vera Rubin 全生命周期机架出货量 | Vera Rubin NVL72 | Spec A/Spec B | 58 | 2H26–2027 | — | 千台机架 | model_assumption | 来源报告第 10 页 Exhibit 8 | low |
| Rubin Ultra 全生命周期机架出货量 | Rubin Ultra NVL144 | Spec A | 66 | 2H27–2028 | — | 千台机架 | model_assumption | 来源报告第 10 页 Exhibit 8 | low |
| Rubin Ultra 全生命周期机架出货量 | Rubin Ultra NVL576 | Spec B | 132 | 2H27–2028 | — | 千台机架 | model_assumption | 来源报告第 10 页 Exhibit 8 | low |

## 单机架网络连接价值量

来源：PDF 第 9 页 Exhibit 6。数值单位为每机架 US$k，采用报告中的数量和 ASP 假设。

| 配置 | 出货期间 | 网络连接总成本 | Scale-up | Scale-out | 币种 | 单位 | 证据类型 |
|---|---|---:|---:|---:|---|---|---|
| GB300 NVL72 | 2H25–2026 | 315 | 140 | 175 | USD | US$k/rack | model_assumption |
| Vera Rubin NVL72 Spec A | 2H26–2027 | 489 | 140 | 349 | USD | US$k/rack | model_assumption |
| Vera Rubin NVL72 Spec B | 2H26–2027 | 504 | 140 | 364 | USD | US$k/rack | model_assumption |
| Rubin Ultra NVL144 Spec A | 2H27–2028 | 1,113 | 381 | 732 | USD | US$k/rack | model_assumption |
| Rubin Ultra NVL576 Spec B, per rack | 2H27–2028 | 1,169 | 803 | 366 | USD | US$k/rack | model_assumption |

第 3 页正文称单计算单元价值量从 US$315k 增长 29 倍至 US$9.4bn。由于 Rubin Ultra NVL576 按 8 个机架建模，第 9 页机架表无法支持 `bn` 单位，因此原文保留为 `disputed`。

## 全生命周期 Scale-up 与 Scale-out TAM

来源：PDF 第 10 页 Exhibit 8。

| 配置 | Scale-up TAM | Scale-out TAM | TAM 合计 | 期间 | 币种 | 单位 | 证据类型 |
|---|---:|---:|---:|---|---|---|---|
| GB300 NVL72 | 6,702 | 8,367 | 15,070 | 全生命周期，主要在 2026 年 | USD | US$m | model_assumption |
| Vera Rubin NVL72 Spec A | 8,090 | 20,200 | 28,291 | 全生命周期，2H26–2027 | USD | US$m | model_assumption |
| Vera Rubin NVL72 Spec B | 8,090 | 21,067 | 29,158 | 全生命周期，2H26–2027 | USD | US$m | model_assumption |
| Rubin Ultra NVL144 Spec A | 25,114 | 48,344 | 73,458 | 全生命周期，2H27–2028 | USD | US$m | model_assumption |
| Rubin Ultra NVL576 Spec B | 105,970 | 48,344 | 154,313 | 全生命周期，主要在 2028 年 | USD | US$m | model_assumption |

由于四舍五入，部分显示的小计与合计相差 US$1m。

## Rubin Ultra NVL576 Spec B 组件 TAM

来源：PDF 第 10 页 Exhibit 8。数值覆盖报告的全生命周期情景。

| 组件 | 数值 | 期间 | 币种 | 单位 | 证据类型 |
|---|---:|---|---|---|---|
| 铜缆—backplane | 20,529 | 2H27–2028 全生命周期 | USD | US$m | model_assumption |
| 铜缆—交换托盘 flyover | 10,264 | 2H27–2028 全生命周期 | USD | US$m | model_assumption |
| 光模块 | 32,390 | 2H27–2028 全生命周期 | USD | US$m | model_assumption |
| 光引擎与 FAU | 55,998 | 2H27–2028 全生命周期 | USD | US$m | model_assumption |
| ELS | 10,207 | 2H27–2028 全生命周期 | USD | US$m | model_assumption |
| 光纤线缆与 MPO | 20,956 | 2H27–2028 全生命周期 | USD | US$m | model_assumption |
| Shufflebox | 3,970 | 2H27–2028 全生命周期 | USD | US$m | model_assumption |

报告在 PDF 第 3 页将 CPO 相关组件汇总为约 US$91bn，占 US$154bn 总额的 59%。

## 分年度 CPO TAM

来源：PDF 第 11 页 Exhibit 10。

| 情景 | 2026E | 2027E | 2028E | 2026E–2028E 合计 | 币种 | 单位 | 证据类型 |
|---|---:|---:|---:|---:|---|---|---|
| 高端 Spec B | 1,024 | 24,840 | 70,881 | 96,745；报告概括为 US$97bn | USD | US$m | model_assumption |
| 低端 Spec A | 0 | 3,557 | 12,093 | 15,650 | USD | US$m | model_assumption |

## 分年度 CPO 交换机需求

来源：PDF 第 11 页 Exhibit 11。

| 情景 | 2026E | 2027E | 2028E | 单位 | 证据类型 |
|---|---:|---:|---:|---|---|
| 高端 Spec B | 15 | 88 | 110 | 千台交换机 | model_assumption |
| 低端 Spec A | 0 | 26 | 89 | 千台交换机 | model_assumption |

## 相关硅光输入

| 指标 | 800G | 1.6T | 期间 | 币种 | 单位 | 证据类型 | 来源 |
|---|---:|---:|---|---|---|---|---|
| EML 模块 BoM | 310 | 500 | 截至 2026-04-17 | USD | US$/module | source_opinion | 来源报告第 18 页 Exhibits 28–29 |
| 硅光模块 BoM | 230 | 341 | 截至 2026-04-17 | USD | US$/module | source_opinion | 来源报告第 18 页 Exhibits 28–29 |
| EML 模块 ASP | 430 | 1,000 | 截至 2026-04-17 | USD | US$/module | source_opinion | 来源报告第 18 页 Exhibits 28–29 |
| 硅光模块 ASP | 365 | 800 | 截至 2026-04-17 | USD | US$/module | source_opinion | 来源报告第 18 页 Exhibits 28–29 |

4Q28E 硅光渗透率终点为 `disputed`：Exhibit 26 写 46%，第 18 页正文写 45%。

报告还预计，在更高速率和硅光产品组合迁移过程中，光模块供应商毛利率将达到 48%–55%，但未给出明确预测年份。该论断保留为 `source_opinion`，不作为 Wiki 已采纳的毛利率假设。

## 利润表

无可用数据。报告提到潜在 EPS 影响，但当前可见页面没有提供完整的逐公司利润表或可审计的 EPS 桥接。

## 现金流、营运资本与资本开支

无可用数据。

## 并表、持股比例与少数股东权益

不适用于本市场 TAM 模型。模型未纳入并购会计处理。

## 股本、EPS、净现金与净债务

无可用数据。

## 估值

来源当前可见页面未提供完整目标价或现价估值表，因此未采纳任何估值结果。

## 情景与敏感性分析

报告的敏感性主要来自 Spec A 与 Spec B 的差异：

- 机架连接架构；
- CPO 渗透率；
- 分年度机架出货分配；
- 单台交换机的光引擎数量；
- 组件 ASP；
- scale-up 与 scale-out 的组合。

一个可持续使用的 Wiki 模型需要以一手出货量、客户认证、ASP、良率以及功耗/TCO 数据为基础建立保守、基准和乐观情景；本页不虚构这些情景。

## 与最新披露结果的勾稽

尚未执行。模型标记为 `provisional`，原因包括：

- 来源截止日为 2026-04-17；
- NVIDIA 机架出货和产品可用性尚未与当前一手披露核对；
- 供应商订单、交付和收入尚未勾稽；
- 报告未附“Company data”的底层输入。

## 风险、局限与失效条件

- CPO 渗透率可能显著低于 25%–29%。
- 机架出货量可能更低，或在不同架构之间发生转移。
- 可插拔、铜连接、PCB、NPO 或 OCS 路线可能保留更高份额。
- ASP 下滑速度可能快于销量增长。
- 封装良率、热表现、维护和现场可靠性可能延迟采用。
- 产品可用性、送样和交付可能无法转化为已确认收入、利润或现金流。
- 仍存在内部冲突：第 3 页 US$9.4bn 单位；45% 与 46% 的 SiPh 渗透率；CPO 交换机 BoM 算术关系。

## 变更记录

- 2026-07-24：忠实记录高盛来源模型，并标记为 provisional；没有把任何预测采纳为 Wiki 自身观点。
- 2026-07-24：正文、章节和表头改为中文；数字、页码、单位和证据分类保持不变。
