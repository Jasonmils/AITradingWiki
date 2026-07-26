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
as_of: 2026-04-17
sources:
  - "[[goldman-sachs-global-tech-optical-networking-2026-04-17|高盛全球科技：光网络（2026-04-17）]]"
created: 2026-07-24
updated: 2026-07-24
---

# 共封装光学（CPO）

## 定义

来源报告中的 CPO 全称为 **Co-Packaged Optics（共封装光学）**：将光引擎放置在交换 ASIC 附近并与其共同封装，后续架构还可能与 XPU 共同封装。其目标是把电气路径从厘米级缩短到毫米级，并让更多高带宽连接进入光域。

本页记录[[goldman-sachs-global-tech-optical-networking-2026-04-17|高盛全球科技：光网络（2026-04-17）]]所描述的机制，不代表已经独立验证的行业标准。

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

## 关联实体与事件

- [[nvidia|NVIDIA Corporation（英伟达）]]
- [[broadcom|Broadcom Inc.（博通）]]
- [[marvell-technology|Marvell Technology, Inc.（迈威尔科技）]]
- [[cpo-switch-commercialization-roadmap-2025-2027|CPO 交换机商业化路线图（2025–2027）]]

## 跟踪指标

- 分别跟踪产品发布、客户认证、正式订单、交付、收入确认、利润和现金流。
- 单 GPU/机架的 CPO 端口和光引擎数量。
- 光引擎、ELS、FAU、光纤/MPO 和封装 ASP。
- 单比特功耗、延迟、热裕量和端到端 TCO。
- 封装良率和现场故障率。
- 光学故障后的维修时间与更换成本。
- scale-out 与 scale-up 的 CPO 渗透率。

## 证据缺口与冲突

- 未摄入系统功耗、延迟、热、良率或可靠性的一手证据。
- 产品和客户路线图属于二手公司陈述或高盛推断。
- 第 17 页 BoM、markup 和售价之间存在内部算术不一致。
- 认证、订单、交付、收入、利润和现金流不可互相替代。
