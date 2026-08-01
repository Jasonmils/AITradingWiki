---
page_type: concept
subject: "共封装光学（CPO）"
aliases:
  - "Co-Packaged Optics"
  - CPO
  - "共封装光学"
tags:
  - technology
  - optical-networking
  - packaging
tickers:
  - "NASDAQ:NVDA"
  - "NASDAQ:AVGO"
  - "NASDAQ:MRVL"
  - "NASDAQ:INTC"
  - "NASDAQ:CSCO"
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
as_of: 2026-07-28
sources:
  - "[[goldman-sachs-global-tech-optical-networking-2026-04-17|高盛全球科技：光网络（2026-04-17）]]"
  - "[[oif-co-packaging-framework-01-0|OIF Co-Packaging Framework 01.0]]"
  - "[[oif-co-packaging-3-2t-module-01-0|OIF 3.2Tb/s CPO Module Implementation Agreement 01.0]]"
  - "[[oif-elsfp-02-0|OIF ELSFP Implementation Agreement 02.0]]"
  - "[[cw-wdm-msa-technical-specifications-rev-1-0|CW-WDM MSA 技术规范 Rev 1.0（2021-06-04）]]"
  - "[[broadcom-200g-lane-cpo-2025-05-15|Broadcom 第三代 200G/lane CPO（2025-05-15）]]"
  - "[[cisco-cpo-system-ofc-2023-03-07|Cisco OFC 2023 CPO 系统演示（2023-03-07）]]"
  - "[[marvell-1-6t-silicon-photonics-light-engine-2025-03-31|Marvell 1.6T 硅光光引擎（2025-03-31）]]"
  - "[[intel-fully-integrated-optical-io-chiplet-2024-06-26|Intel 全集成 Optical I/O Chiplet（2024-06-26）]]"
created: 2026-07-24
updated: 2026-07-28
---

# 共封装光学（CPO）

## 定义

来源报告中的 CPO 全称为 **Co-Packaged Optics（共封装光学）**：将光引擎放置在交换 ASIC 附近并与其共同封装，后续架构还可能与 XPU 共同封装。其目标是把电气路径从厘米级缩短到毫米级，并让更多高带宽连接进入光域。

本页结合[[goldman-sachs-global-tech-optical-networking-2026-04-17|高盛来源报告]]与 OIF 一手框架/IA。OIF 文件验证架构与接口，但不验证任何公司的市场份额、量产、订单或收入。

后续公司一手资料进一步表明，CPO 需要与 LPO/on-board optics 和 XPU optical I/O 分开。完整归一化见[[cpo-technology-routes-and-product-generations|CPO 技术路线与产品代际]]。

## 报告描述的架构

报告中的 CPO 数据路径和 BoM 包括：

- 交换 ASIC 或 XPU；
- 光引擎；
- PIC 与 EIC；
- 调制器、光电探测器和 MUX/DEMUX；
- driver 与 TIA；
- FAU；
- 包括 CW laser 在内的外置激光源；
- 光纤及 MPO 连接器/线缆；
- shufflebox；
- 半导体级及 3D 封装。

报告称，更短的电气路径可能降低延迟和功耗，并在部分设计中减少 DSP 与 retimer 的使用。在取得系统级一手测量前，这些论断均为 `source_opinion`。

## 技术路线比较

| 路线 | 布置位置 | 报告描述的故障与维护后果 | 预期角色 | 证据类型 |
|---|---|---|---|---|
| 可插拔光模块 | 连接交换机/服务器的可更换模块 | 模块故障时可只替换模块，交换机保持完整 | 在速率迁移过程中继续存在，并与 NPO/CPO 共存 | source_opinion |
| NPO/on-board optics | 光引擎位于交换机 PCB 上 | 故障可能需要更换交换机 PCB | 中间形态的集成路线 | source_opinion |
| CPO with switch | 光引擎与交换 ASIC 共封装 | 故障可能影响交换 ASIC | 初期商业化 CPO 路线 | source_opinion |
| CPO with XPU | 光引擎与 GPU/CPU/NPU 等 XPU 共封装 | 故障可能影响高价值 XPU | 后续 scale-up 路线；时间尚不明确 | source_opinion |

### 一手产品路线补充

- Cisco 2023 系统演示把 3.2T optical tile 放到交换 ASIC 附近，并采用 external laser source。
- Broadcom 公开代际从 Gen 1 供应链学习、Gen 2 100G/lane 到 Gen 3 200G/lane，Gen 4 400G/lane 仍属于 roadmap。
- Marvell 1.6T 8×200G engine 是 LPO/on-board 形态，公司称其为 6.4T CPO engine 的四分之一规模版本。
- Intel OCI 与 Ayar Labs TeraPHY 属 XPU/compute optical I/O 路线；前者为 prototype，后者公开规格 preliminary 且处于 EVT/DVT 路径。

这些带宽、产品层级和阶段不能合并为一个“CPO 出货量”。

## 采用驱动因素

- 1.6T、3.2T、6.4T 及更高速率带来的带宽要求。
- 随机架和 supernode 带宽提升，电气连接的有效距离缩短。
- 潜在的功耗、延迟和体积优势。
- 当可插拔模块受限时，可能体现总体拥有成本（TCO）优势。
- 光连接从 scale-out 向 scale-up 扩展。
- 单 GPU 和单机架的光学价值量提升。

以上均为报告的 `source_opinion`。

## 约束与故障模式

- 更高的集成度以及半导体级/3D 封装要求。
- 当光学故障影响交换机或 XPU 时，维护成本更高、故障影响范围更大。
- PIC 与 EIC 生命周期不同；报告称 PIC 更脆弱。
- 技术迁移涉及整个系统，而不是单一器件升级。
- 客户基础设施准备度、折旧周期以及对最终胜出路线的不确定性。
- 按报告估算，现阶段 CPO 成本仍较高。
- 来源未提供量化的良率、冷却、热循环或现场可靠性数据，这些均为明确的证据缺口。

## CPO 交换机 BoM 估算

下表抄录自 PDF 第 17 页 Exhibit 22，属于高盛估算，不是已验证的供应商成本结构。

| 组件 | 数量 | ASP | 价值 | 币种 | 单位 | 期间 | 证据类型 | 来源 |
|---|---:|---:|---:|---|---|---|---|---|
| Switch ASIC | 4 | 3,000 | 12,000 | USD | US$/switch | 截至 2026-04-17 | model_assumption | [[goldman-sachs-global-tech-optical-networking-2026-04-17|来源报告]]，第 17 页 Exhibit 22 |
| 1.6T 光引擎 | 72 | 450 | 32,400 | USD | US$/switch | 截至 2026-04-17 | model_assumption | [[goldman-sachs-global-tech-optical-networking-2026-04-17|来源报告]]，第 17 页 Exhibit 22 |
| FAU | 72 | 50 | 3,600 | USD | US$/switch | 截至 2026-04-17 | model_assumption | [[goldman-sachs-global-tech-optical-networking-2026-04-17|来源报告]]，第 17 页 Exhibit 22 |
| ELS | 18 | 400 | 7,200 | USD | US$/switch | 截至 2026-04-17 | model_assumption | [[goldman-sachs-global-tech-optical-networking-2026-04-17|来源报告]]，第 17 页 Exhibit 22 |
| ELS 中的 300mw CW laser | 144 | 30 | 4,320 | USD | US$/switch | 截至 2026-04-17 | model_assumption | [[goldman-sachs-global-tech-optical-networking-2026-04-17|来源报告]]，第 17 页 Exhibit 22 |
| Shufflebox | 1 | 2,500 | 2,500 | USD | US$/switch | 截至 2026-04-17 | model_assumption | [[goldman-sachs-global-tech-optical-networking-2026-04-17|来源报告]]，第 17 页 Exhibit 22 |
| MPO 连接器/线缆 | 144 | 40 | 5,760 | USD | US$/switch | 截至 2026-04-17 | model_assumption | [[goldman-sachs-global-tech-optical-networking-2026-04-17|来源报告]]，第 17 页 Exhibit 22 |
| 单模光纤 | 1,152 | 11 | 12,343 | USD | US$/switch | 截至 2026-04-17 | model_assumption | [[goldman-sachs-global-tech-optical-networking-2026-04-17|来源报告]]，第 17 页 Exhibit 22 |
| 报告所列 BoM 合计 | — | — | 75,803 | USD | US$/switch | 截至 2026-04-17 | disputed | [[goldman-sachs-global-tech-optical-networking-2026-04-17|来源报告]]，第 17 页 Exhibit 22 |
| 报告所列 markup | — | — | 62,220 | USD | US$/switch | 截至 2026-04-17 | disputed | [[goldman-sachs-global-tech-optical-networking-2026-04-17|来源报告]]，第 17 页 Exhibit 22 |
| 报告所列售价 | — | — | 130,000 | USD | US$/switch | 截至 2026-04-17 | disputed | [[goldman-sachs-global-tech-optical-networking-2026-04-17|来源报告]]，第 17 页 Exhibit 22 |

上述三个汇总数字无法直接勾稽，因此保留为 `disputed`。

## 产业结构与价值量分配

报告描述的价值链包括：

1. switch ASIC/XPU；
2. 光引擎和 FAU；
3. ELS 与激光器件；
4. 光纤与 MPO 连接；
5. shufflebox 与封装；
6. 机架/服务器集成；
7. 云端或 AI 集群部署。

高端 Rubin Ultra NVL576 情景将较大价值量分配给光引擎/FAU、ELS 和光纤/MPO；详见[[goldman-sachs-ai-optical-networking-tam-2026-2028e|高盛 AI 光网络 TAM 与 CPO 渗透模型（2026–2028E）]]。

## 重要论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| CPO 缩短电气路径，并可能降低延迟和功耗。 | source_opinion | 2026-04-17 | 来源报告第 15–16 页 | medium | 一手系统测试显示，计入封装、热管理和控制开销后没有净收益。 |
| 报告预计 CPO with switch 先于 CPO with XPU。 | source_opinion | 2026-04-17 | 来源报告第 14–16 页 | medium | XPU CPO 先于交换机 CPO 实现规模商业部署。 |
| 可插拔光模块、NPO 和 CPO 将长期共存。 | source_opinion | 2026-04-17 | 来源报告第 16 页 | medium | 其中一条路线显著更快地取代其他路线。 |
| 高价值平台情景采用 25%–29% 的 scale-out CPO 渗透率。 | model_assumption | 2026-04-17 | 来源报告第 7–11 页 | low | 实际平台组合和客户认证与假设不同。 |
| Cisco 展示 3.2T tile 的 CPO system，并称可移除额外 DSP。 | company_statement | 2023-03-07 | [[cisco-cpo-system-ofc-2023-03-07|Cisco 来源]] | medium | 正式产品或同口径系统测试不支持。 |
| Marvell 1.6T engine 可用于 LPO/on-board，并被公司定义为后续 CPO 基础。 | company_statement | 2025-03-31 | [[marvell-1-6t-silicon-photonics-light-engine-2025-03-31|Marvell 来源]] | medium | 客户采用不同路线或产品未商业化。 |
| Intel 4Tbps 双向 OCI 是工作原型，不是量产产品。 | verified_fact | 2024-06-26 | [[intel-fully-integrated-optical-io-chiplet-2024-06-26|Intel 来源]] | high | 后续正式产品状态替代。 |

## 关联实体与事件

- [[nvidia|NVIDIA Corporation（英伟达）]]
- [[broadcom|Broadcom Inc.（博通）]]
- [[marvell-technology|Marvell Technology, Inc.（迈威尔科技）]]
- [[intel-corporation|Intel Corporation（英特尔）]]
- [[cisco-systems|Cisco Systems, Inc.（思科）]]
- [[ayar-labs|Ayar Labs]]
- [[cpo-switch-commercialization-roadmap-2025-2027|CPO 交换机商业化路线图（2025–2027）]]
- [[coherent|Coherent Corp.]]
- [[lumentum|Lumentum Holdings Inc.]]
- [[fabrinet|Fabrinet]]
- [[tfc-communication|天孚通信]]
- [[innolight|中际旭创]]
- [[robotechnik-ficontec|罗博特科与 ficonTEC]]

## 研究框架

- [[cpo-commercialization-evidence-stages|CPO 商业化证据分层]]
- [[cpo-value-chain-and-company-exposure|CPO 价值链与公司暴露度]]
- [[cpo-reliability-and-external-laser-source|CPO 可靠性与外置激光源（ELS）]]
- [[cpo-customer-concentration-and-revenue-double-counting|CPO 客户集中度与产业链重复计量]]
- [[cpo-technology-routes-and-product-generations|CPO 技术路线与产品代际]]
- [[cpo-optical-engine-components-cost-and-margin|CPO 光引擎组成、成本与利润]]
- [[cpo-product-architecture-cost-and-margin-model-2026-2031|CPO 产品架构、成本与利润模型（2026–2031）]]

## 跟踪指标

- 分别跟踪产品发布、客户认证、正式订单、交付、收入确认、利润和现金流。
- 单 GPU/机架的 CPO 端口和光引擎数量。
- 光引擎、ELS、FAU、光纤/MPO 和封装 ASP。
- 单比特功耗、延迟、热裕量和端到端 TCO。
- 封装良率和现场故障率。
- 光学故障后的维修时间与更换成本。
- scale-out 与 scale-up 的 CPO 渗透率。

## 证据缺口与冲突

- 已摄入 OIF 架构与接口规范，但现场功耗、热、良率和可靠性仍缺少公开一手数据。
- 已补充厂商产品代际、LPO 与 XPU optical I/O 路线，但 performance 和 cost 数据仍主要是 `company_statement`。
- 产品和客户路线图已有部分公司一手声明，仍缺客户验收和可勾稽收入。
- 公开资料未披露可审计的 CPO 单品 ASP、BoM、composite yield、毛利或 RMA。
- 第 17 页 BoM、markup 和售价之间存在内部算术不一致。
- 认证、订单、交付、收入、利润和现金流不可互相替代。
