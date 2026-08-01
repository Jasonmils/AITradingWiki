---
page_type: source
subject: "Intel 全集成 Optical I/O Chiplet"
tags: [company-release, optical-io, silicon-photonics]
tickers: ["NASDAQ:INTC"]
markets: [US]
asset_classes: [equity]
industries: [semiconductors, data-center-networking]
themes: [AI infrastructure, co-packaged optics, optical-io]
as_of: 2024-06-26
sources:
  - "raw/2024-06-26-intel-fully-integrated-optical-io-chiplet.pdf"
created: 2026-07-28
updated: 2026-07-28
---

# Intel 全集成 Optical I/O Chiplet（2024-06-26）

## 来源元数据

- 来源类型：公司新闻稿与技术说明
- 发布机构：Intel Corporation
- 发布日期与知识截止日：2024-06-26
- 原始文件：`raw/2024-06-26-intel-fully-integrated-optical-io-chiplet.pdf`
- 本地源文件状态：不可变原件；7 页；SHA-256 `1a6b3c569e8b11b11391e489c3ed62da021493b6ecf94658b9431b61117803ac`

## 摘要

Intel 披露与 CPU 共封装的 fully integrated optical compute interconnect（OCI）chiplet 原型。演示为 4Tbps 双向、64 个 32Gbps 通道，并把片上激光器和 optical amplifier 集成进 PIC。该来源证明工作原型和公司历史制造经验，不证明商业产品、订单或收入。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| Intel 在 OFC 2024 展示与 Intel CPU 共封装的 OCI chiplet 工作原型。 | verified_fact | 2024-06-26 | 公司发布材料与演示照片 | high | 公司撤回或更正。 |
| 原型提供 4Tbps 双向带宽：每方向 64×32Gbps，通过 8 对光纤、每纤 8 个 DWDM 波长传输。 | company_statement | 2024-06-26 | 公司规格表 | high | 独立测试或正式产品规格不一致。 |
| 公司称 OCI 能耗约 5pJ/bit，而可插拔光模块约 15pJ/bit。 | company_statement | 2024-06-26 | 公司新闻稿比较 | medium | 同口径系统测试无法复现。 |
| PIC 集成 on-chip lasers 与 optical amplifiers，并与 EIC 共封装。 | company_statement | 2024-06-26 | 架构图与正文 | high | 正式产品采用不同光源路线。 |
| Intel 称历史累计出货超过 800 万颗 PIC、集成超过 3,200 万颗片上激光器，激光 FIT 低于 0.1。 | company_statement | 2024-06-26 | 公司历史制造陈述 | medium | 经审计或第三方数据不支持。 |
| 200G/lane PIC 面向 800G/1.6T 应用仍处于开发。 | company_statement | 2024-06-26 | 公司路线图描述 | medium | 后续产品状态更新。 |
| 该 OCI 是 prototype，且来源未披露订单、量产、收入或毛利。 | verified_fact | 2024-06-26 | 公告全文 | high | 后续一手披露补充。 |

## 实体

- [[intel-corporation|Intel Corporation（英特尔）]]

## 概念

- [[cpo-technology-routes-and-product-generations|CPO 技术路线与产品代际]]
- [[silicon-photonics-and-optical-light-sources|硅光与光学光源]]
- [[cpo-optical-engine-components-cost-and-margin|CPO 光引擎组成、成本与利润]]

## 事件

- [[cpo-switch-commercialization-roadmap-2025-2027|CPO 与光学 I/O 商业化路线图]]

## 提及的模型或假设

- 公司称新 SiPh 工艺使相关 die area 降幅超过 40%、功耗降幅超过 15%；这是公司陈述，不是可审计单位成本。
- 原型 pJ/bit 不能直接转换为产品毛利、系统 TCO 或自由现金流。

## 证据缺口与冲突

- “与 select customers 合作”不能升级为客户认证、订单或量产。
- 100m 为演示能力上限表述；公司同时指出实际使用通常是数十米，估值模型应使用具体场景。
- 缺少良率、封装成本、ASP、RMA、客户名单与商业化时间。
