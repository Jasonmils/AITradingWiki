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
tickers: ["NASDAQ:INTC", "NASDAQ:MRVL"]
markets: [US]
asset_classes:
  - equity
industries:
  - semiconductors
  - optical-components
themes:
  - AI infrastructure
  - silicon photonics
  - optical networking
as_of: 2026-07-28
sources:
  - "[[goldman-sachs-global-tech-optical-networking-2026-04-17|高盛全球科技：光网络（2026-04-17）]]"
  - "[[cw-wdm-msa-technical-specifications-rev-1-0|CW-WDM MSA 技术规范 Rev 1.0（2021-06-04）]]"
  - "[[intel-fully-integrated-optical-io-chiplet-2024-06-26|Intel 全集成 Optical I/O Chiplet（2024-06-26）]]"
  - "[[marvell-1-6t-silicon-photonics-light-engine-2025-03-31|Marvell 1.6T 硅光光引擎（2025-03-31）]]"
  - "[[ayar-labs-supernova-light-source-2026-07-28|Ayar Labs SuperNova 多波长光源产品页快照（2026-07-28）]]"
created: 2026-07-24
updated: 2026-07-28
---

# 硅光与光学光源

## 范围

本页记录 silicon photonics（SiPh，硅光）光模块、基于 EML 的分立式光模块，以及 external/integrated optical source 的技术与经济边界。高盛数字保留为第三方估算；Intel、Marvell 与 Ayar Labs 的性能数据保留为 `company_statement`。

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

## External 与 integrated light source

| 路线 | 一手例证 | 可能优势 | 主要成本/估值风险 |
|---|---|---|---|
| Modular external source | CW-WDM MSA 单端口单波长定义 | 多源组合、故障隔离 | 光纤/连接器/管理和装配数量增加 |
| Integrated external source | CW-WDM MSA 单端口多波长；Ayar SuperNova | 多波长阵列、可现场替换 | 阵列良率、冗余、温控和封装成本 |
| Integrated/on-chip laser | Intel OCI PIC | 减少独立 ELS 和部分外部接口 | PIC/laser 联合良率、主封装失效与维修风险 |

CW-WDM Rev 1.0 还给出 dual ELS 8+8 的 informative 示例；它是架构可能性，不是市场采用或成本下降证据。

## 产品级硅光证据

- Marvell 1.6T engine 采用 8×200G PAM4 DR8，集成 linear driver、TIA、SiPh、MCU 与固件；公司称典型条件下含激光 `<5pJ/bit`，并处于 select-customer sampling。
- Intel OCI prototype 把 on-chip lasers 和 optical amplifiers 集成进 PIC；公司称 4Tbps 双向、约 5pJ/bit。
- 两组 pJ/bit 的产品边界、传输模式和系统范围不同，不能直接比较毛利或完整 TCO。

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
- external/integrated laser 的采用比例、冗余、耦合良率和 RMA。
- wavelength 数、热调谐功耗、wafer sort 与 known-good-die 结果。
- 长距离可靠性和功耗要求。
- VCSEL 或 MicroLED 用于 CPO 的客户认证进展。

## 证据缺口与冲突

- 4Q28E 渗透率终点在 45% 与 46% 之间冲突。
- 产能计划和管理层承诺均为二手引用。
- 未提供经审计的供应商 BoM、良率、利用率或现金流数据。
- 更低的组件 BoM 不自动等于更高的供应商利润或现金流。
- 厂商 pJ/bit、die-area、FIT 和封装成本声明缺少统一第三方测试。
- 标准化可能扩大生态，也可能通过多源采购压低 ASP 与份额。

## 关联

- [[cpo-reliability-and-external-laser-source|CPO 可靠性与外置激光源]]
- [[cpo-optical-engine-components-cost-and-margin|CPO 光引擎组成、成本与利润]]
- [[cpo-technology-routes-and-product-generations|CPO 技术路线与产品代际]]
