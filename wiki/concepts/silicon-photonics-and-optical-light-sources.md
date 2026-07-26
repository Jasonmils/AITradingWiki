---
page_type: concept
subject: "硅光与光学光源"
aliases:
  - "Silicon Photonics and Optical Light Sources"
  - "Silicon Photonics"
  - SiPh
  - "硅光"
  - "硅光与光学光源"
tags:
  - technology
  - silicon-photonics
  - optical-components
tickers: []
markets: []
asset_classes:
  - equity
industries:
  - semiconductors
  - optical-components
themes:
  - AI infrastructure
  - silicon photonics
  - optical networking
as_of: 2026-04-17
sources:
  - "[[goldman-sachs-global-tech-optical-networking-2026-04-17|高盛全球科技：光网络（2026-04-17）]]"
created: 2026-07-24
updated: 2026-07-24
---

# 硅光与光学光源

## 范围

本页记录报告对 silicon photonics（SiPh，硅光）光模块、基于 EML 的分立式光模块及光源选择的比较，不独立验证器件性能或供应商产能。

## 报告描述的硅光机制

报告展示了一种集成调制器、光电探测器、MUX/DEMUX、波导和耦合器的硅光芯片。报告认为，与基于 EML 的分立式模块相比，更高集成度可以降低体积、功耗和成本，尤其是在更高速率下。

来源同时预计 EML 将长期共存，因为其可靠性记录更长，并可能在长距离传输中更具优势。

## 光模块成本比较

以下数字是 PDF 第 18 页 Exhibits 28–29 中的高盛估算。

| 模块 | 路线 | BoM 合计 | ASP | 毛利率 | 发布日期 | 币种 | 单位 | 证据类型 |
|---|---|---:|---:|---:|---|---|---|---|
| 800G | EML | 310 | 430 | 28% | 2026-04-17 | USD | US$/module | source_opinion |
| 800G | 硅光 | 230 | 365 | 37% | 2026-04-17 | USD | US$/module | source_opinion |
| 1.6T | EML | 500 | 1,000 | 50% | 2026-04-17 | USD | US$/module | source_opinion |
| 1.6T | 硅光 | 341 | 800 | 57% | 2026-04-17 | USD | US$/module | source_opinion |

报告称 800G/1.6T SiPh 模块分别具有 26%/32% 的 BoM 优势和 15%/20% 的价格优势。这些并非已验证的供应商经济性数据。

## 渗透率预测

| 指标 | 起点 | 终点 | 期间 | 证据类型 | 来源 |
|---|---:|---:|---|---|---|
| 数据通信硅光渗透率 | 6% | 46% | 1Q24 至 4Q28E | disputed | 来源报告第 17 页 Exhibit 26 |
| 数据通信硅光渗透率 | 6% | 45% | 1Q24 至 4Q28E | disputed | 来源报告第 18 页正文 |

终点保留为 45%–46% 的冲突，不静默统一。

## CPO 光源选择

| 路线 | 能效 | 有效距离 | 延迟 | 单比特成本 | 技术成熟度 | 证据类型 |
|---|---|---:|---|---|---|---|
| SiPh + CW laser | 较低 | >1km | 低至中等 | 中等 | 高 | source_opinion |
| VCSEL | 高 | <100m | 低至中等 | 低 | 高 | source_opinion |
| MicroLED | 高 | <20m | 低 | 低 | 低 | source_opinion |

来源：PDF 第 20 页 Exhibit 36。报告称 CW laser 是光模块中采用最广泛的光源；VCSEL 可能适用于较短的 scale-up 连接；MicroLED 的技术成熟度较低。

## 供应约束

报告将 2026 年 EML/CW laser 供应紧张归因于 AI 服务器需求、速率迁移、光连接扩张、InP 衬底约束、中国出口管制/地缘政治紧张，以及扩产所需时间。

报告列出以下供应商计划，但尚未进行一手核验：

| 公司 | 报告所述计划 | 期间 | 证据类型 | PDF 证据 |
|---|---|---|---|---|
| VPEC | 将 InP MOCVD 设备从 60 台扩至 64 台 | 2H26 | company_statement | 第 19 页 |
| Landmark 与 YJ Semi | 大规模扩产 | 2026 | company_statement | 第 19 页 |
| Lumentum | 从 CY3Q25 至 CY2Q26 扩产 40% | CY3Q25–CY2Q26 | company_statement | 第 19 页 |
| Coherent | 产能翻倍 | 除来源上下文外未给出具体时间 | company_statement | 第 19 页 |

报告预计供应紧张将持续至 2027 年，并可能在 2H28 恢复平衡。这属于 `source_opinion`。

## 跟踪指标

- 不同速率和应用中的硅光占比。
- EML、CW laser 和 InP 衬底交期。
- 实际安装并完成认证的 MOCVD 产能。
- 各路线的激光器成本、光模块 BoM、ASP 和毛利率。
- 长距离可靠性和功耗要求。
- VCSEL 或 MicroLED 用于 CPO 的客户认证进展。

## 证据缺口与冲突

- 4Q28E 渗透率终点在 45% 与 46% 之间冲突。
- 产能计划和管理层承诺均为二手引用。
- 未提供经审计的供应商 BoM、良率、利用率或现金流数据。
- 更低的组件 BoM 不自动等于更高的供应商利润或现金流。
