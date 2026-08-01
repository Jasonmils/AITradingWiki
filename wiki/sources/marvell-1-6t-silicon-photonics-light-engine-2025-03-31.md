---
page_type: source
subject: "Marvell 1.6T 硅光光引擎"
tags: [company-release, silicon-photonics, optical-engine]
tickers: ["NASDAQ:MRVL"]
markets: [US]
asset_classes: [equity]
industries: [semiconductors, optical-components, data-center-networking]
themes: [AI infrastructure, co-packaged optics, linear-pluggable-optics]
as_of: 2025-03-31
sources:
  - "raw/2025-03-31-marvell-1-6t-silicon-photonics-light-engine.html"
created: 2026-07-28
updated: 2026-07-28
---

# Marvell 1.6T 硅光光引擎（2025-03-31）

## 来源元数据

- 来源类型：公司产品公告
- 发布机构：Marvell Technology, Inc.
- 发布日期与知识截止日：2025-03-31
- 原始文件：`raw/2025-03-31-marvell-1-6t-silicon-photonics-light-engine.html`
- 本地源文件状态：不可变原始 HTML；SHA-256 `da8d6789778054ee362c7edb2ba638f0fcc4a8a9bb0d2605456f3b58d4aed9a1`

## 摘要

Marvell 发布第二款 SiPh light engine，在 OSFP LPO 中以 8×200G PAM4 实现 1.6T DR8。公司把它描述为此前 6.4T CPO 光引擎的四分之一规模版本，可用于 LPO、on-board optics 或直接系统集成，并称其为后续 CPO 的基础。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| 1.6T engine 采用 8×200G PAM4、DR8，并在 OSFP LPO 中展示。 | company_statement | 2025-03-31 | 公司产品公告 | high | 正式规格更改。 |
| 单封装集成 linear driver、TIA、SiPh、MCU 与固件。 | company_statement | 2025-03-31 | 公司架构说明 | high | 产品拆分改变。 |
| 公司把 1.6T engine 定义为 6.4T CPO engine 的四分之一规模版本。 | company_statement | 2025-03-31 | 公司产品路线说明 | high | 后续路线图更改。 |
| 公司称典型条件下、包含激光的能耗低于 5pJ/bit。 | company_statement | 2025-03-31 | 公司规格比较 | medium | 独立同口径测试无法复现。 |
| 公司称单封装整合数百个调制器、探测器、driver、TIA、MCU 与无源元件。 | company_statement | 2025-03-31 | 公司产品说明 | medium | BoM 或拆解证据不支持。 |
| 产品正在向 select customers sampling。 | company_statement | 2025-03-31 | 公告状态说明 | medium | 后续状态更新。 |
| sampling 不证明客户认证、规模量产、收入或毛利。 | verified_fact | 2025-03-31 | 公告未披露这些里程碑 | high | 后续一手文件补充。 |

## 实体

- [[marvell-technology|Marvell Technology, Inc.（迈威尔科技）]]

## 概念

- [[cpo-technology-routes-and-product-generations|CPO 技术路线与产品代际]]
- [[cpo-optical-engine-components-cost-and-margin|CPO 光引擎组成、成本与利润]]
- [[silicon-photonics-and-optical-light-sources|硅光与光学光源]]

## 事件

- [[cpo-switch-commercialization-roadmap-2025-2027|CPO 与光学 I/O 商业化路线图]]

## 提及的模型或假设

- 高集成可以减少离散器件和传统组装，但不自动降低良品成本；封装、耦合、测试和复合良率仍需建模。
- pJ/bit 口径不等于完整系统 TCO 或产品毛利。

## 证据缺口与冲突

- 未披露客户、送样数量、ASP、BoM、良率、RMA、收入与利润。
- 1.6T LPO/板载光引擎与 6.4T CPO 的 TAM 和商业阶段不能合并。
- “CPO 基础”是路线图表述，不等于已经产生 CPO 收入。
