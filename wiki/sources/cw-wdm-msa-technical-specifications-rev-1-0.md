---
page_type: source
subject: "CW-WDM MSA 技术规范 Rev 1.0"
tags: [industry-standard, cw-wdm, external-laser-source]
tickers: []
markets: []
asset_classes: []
industries: [optical-components, data-center-networking]
themes: [AI infrastructure, co-packaged optics, optical-io]
as_of: 2021-06-04
sources:
  - "raw/2021-06-04-cw-wdm-msa-technical-specifications-rev-1-0.pdf"
created: 2026-07-28
updated: 2026-07-28
---

# CW-WDM MSA 技术规范 Rev 1.0（2021-06-04）

## 来源元数据

- 来源类型：行业多源协议技术规范
- 发布机构：CW-WDM MSA
- 发布日期与知识截止日：2021-06-04
- 原始文件：`raw/2021-06-04-cw-wdm-msa-technical-specifications-rev-1-0.pdf`
- 本地源文件状态：不可变原件；25 页；SHA-256 `a5cfb39adf28906956acc062714c94ad14942d25a04074696050c3202826d39a`

## 摘要

Rev 1.0 为 AI、机器学习、光计算和高密度 CPO 应用定义 O-band 连续波 WDM（CW-WDM）波长网格及部分光学参数。规范同时容纳 modular optical source（单端口单波长）与 integrated optical source（单端口承载多波长），但不规定机械外形、电源、管理接口或硬件引脚。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| Rev 1.0 定义 8 组 O-band 网格，覆盖 8+1、16+1 与 32+1 波长配置及 9nm、18nm、36nm 三类跨度。 | verified_fact | 2021-06-04 | 规范表 3-1 至 3-8 | high | 后续版本正式取代该版本。 |
| modular source 的每个端口输出一个波长；integrated source 的一个端口可输出网格内全部波长。 | verified_fact | 2021-06-04 | 第 2.1–2.2 节 | high | 后续版本更改定义。 |
| dual ELS 8+8 示例可把两个物理 8 波长光源组合为 16 波长，并跳过 L0。 | verified_fact | 2021-06-04 | Appendix B informative example | high | 后续正式规范否定该示例。 |
| 规范不定义机械外形、电气功率、管理接口或硬件引脚。 | verified_fact | 2021-06-04 | 第 1.2 节范围说明 | high | 后续版本补充这些接口。 |
| 标准化能够自动带来低成本、多源采购或规模采用。 | source_opinion | 2021-06-04 | 规范未提供采购、成本或采用数据 | low | 独立采购、量产和成本证据出现。 |

## 实体

- CW-WDM MSA

## 概念

- [[silicon-photonics-and-optical-light-sources|硅光与光学光源]]
- [[cpo-reliability-and-external-laser-source|CPO 可靠性与外置激光源]]
- [[cpo-optical-engine-components-cost-and-margin|CPO 光引擎组成、成本与利润]]

## 事件

本规范不是客户认证、订单、交付或收入事件。

## 提及的模型或假设

- 波长数、端口数、光源冗余和封装接口可作为 BoM 与良率模型的结构输入。
- 规范没有提供 ASP、BoM、良率、RMA 或毛利数据。

## 证据缺口与冲突

- Appendix B 为 informative 示例，不等同于所有 CPO 系统的强制架构。
- 规范没有证明任何供应商已量产、被客户采用或实现财务贡献。
- 温度跟踪、冗余和多源兼容仍需系统级实现与验证。
