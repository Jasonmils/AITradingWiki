---
page_type: concept
subject: "AI 数据中心互连架构"
aliases:
  - "AI Data Center Interconnect Architecture"
  - "AI 数据中心互连架构"
tags:
  - technology
  - data-center-networking
  - optical-networking
tickers:
  - "NASDAQ:NVDA"
markets:
  - US
asset_classes:
  - equity
industries:
  - semiconductors
  - data-center-networking
  - optical-components
themes:
  - AI infrastructure
  - scale-up
  - scale-out
  - scale-across
as_of: 2026-04-17
sources:
  - "[[goldman-sachs-global-tech-optical-networking-2026-04-17|高盛全球科技：光网络（2026-04-17）]]"
created: 2026-07-24
updated: 2026-07-24
---

# AI 数据中心互连架构

## 范围

本页对[[goldman-sachs-global-tech-optical-networking-2026-04-17|高盛全球科技：光网络（2026-04-17）]]描述的连接层级和路线选择机制进行规范化整理，不增加独立技术预测。

## 连接层级

| 层级 | 报告定义 | 报告示例 | 证据类型 |
|---|---|---|---|
| Scale-up（纵向扩展） | 在一台设备或紧耦合 supernode 内增加 GPU 和计算资源，也可能跨机架延伸 | Vera Rubin 机架；Rubin Ultra NVL576 跨机架第二层 scale-up | source_opinion |
| Scale-out（横向扩展） | 增加更多设备，并通过交换技术连接 | 支持 10 万个以上 GPU 连接的 AI 集群 | source_opinion |
| Scale-across（跨数据中心扩展） | 连接不同地点数据中心内的服务器 | NVIDIA 自研以太网交换机和 NIC 路线 | source_opinion |

来源：PDF 第 25 页 Exhibit 47。

## 按距离划分的连接路线

报告采用以下近似距离划分。这些数值是来源中的描述性工程区间，不是已经验证的标准。

| 路线 | 距离 | 报告中的典型用途 | 成本位置 | PDF 证据 | 证据类型 |
|---|---:|---|---|---|---|
| PCB traces | <1m | 同一 tray 内 GPU-to-GPU | 最低 | 第 13 页 Exhibit 15 | source_opinion |
| PCB midplane | <1m | 机架内 GPU-to-GPU | 高于 PCB traces | 第 13 页 Exhibit 15 | source_opinion |
| DAC | 0.5–3m | 机架内 GPU-to-GPU/ToR | 低 | 第 13 页 Exhibit 15 | source_opinion |
| ACC | 7–15m | 机架内/机架间 | 低 | 第 13 页 Exhibit 15 | source_opinion |
| AEC | 5–30m | 机架内/机架间 GPU/ToR | 中等 | 第 13 页 Exhibit 15 | source_opinion |
| AOC | 30–100m | 机架内/机架间 | 较高 | 第 13 页 Exhibit 15 | source_opinion |
| DR transceiver + fiber | 30–500m | 机架间及楼内 | 较高 | 第 13 页 Exhibit 15 | source_opinion |
| FR transceiver + fiber | 500m–2km | Spine 到 super-spine/楼宇间 | 较高 | 第 13 页 Exhibit 15 | source_opinion |

## 路线选择机制

- PCB 和铜连接在短距离下成本和功耗较低，但报告称信号完整性会随距离和速率提升而恶化。
- 随着带宽和距离增加，光连接更具优势。
- 铜连接从 DAC 向 ACC、AEC 演进，以延长有效距离。
- PCB midplane 可能从 tray 内连接扩展到机架内连接。
- 光连接通过 AOC、NPO 和[[co-packaged-optics|共封装光学（CPO）]]，由 scale-out 向 scale-up 扩展。
- [[optical-circuit-switch|光路交换机（OCS）]]被描述为部分架构中的全光交换替代路线。

以上均为 `source_opinion`。

## 报告描述的速率与配比迁移

- 报告预计 800G 将在 2026 年向 1.6T 迁移，并在之后至 2028E 逐步迈向 3.2T 及更高速度。
- NVIDIA GB300 在 1.6T 下的光模块配比为 1:2–3；VR200 在 1.6T 下为 1:4–6。
- Google 和 Amazon ASIC 架构约为 1:4；Meta Minerva 为 1:8–12；Huawei Cloud Matrix 384 为 1:18。
- 这些数字来自 PDF 第 21 页 Exhibit 38，属于 GSe 或公司数据推导，并非已经验证的客户部署事实。

## 采用驱动因素与约束

| 驱动因素或约束 | 作用机制 | 证据类型 | PDF 证据 |
|---|---|---|---|
| 计算规模 | 更多 GPU 和更大集群需要更多端口与交换层级 | source_opinion | 第 3、21、25 页 |
| 带宽迁移 | 更高端口速率提高光学价值量，并缩短电连接有效距离 | source_opinion | 第 14、21 页 |
| 折旧/利用率 | 尚未折旧完毕的设施会抑制快速迁移 | source_opinion | 第 24 页 |
| 基础设施准备度 | 建筑、电网和散热条件可能延迟采用 | source_opinion | 第 24 页 |
| 成本曲线 | 客户可能等待量产带来的降本 | source_opinion | 第 24 页 |
| 技术不确定性 | 多条路线并存会形成早期投资搁浅风险 | source_opinion | 第 24 页 |

## 跟踪指标

- GPU/机架出货量与集群规模。
- 网络层数和单 GPU 光端口数量。
- 800G、1.6T 和 3.2T 产品组合。
- 各 scale-up/scale-out 层级中的铜连接、PCB、可插拔模块、NPO、CPO 与 OCS 占比。
- 设施供电、电网和冷却准备度。
- 客户折旧周期和新数据中心投运进度。

## 证据缺口与冲突

- 架构表混合了公司数据、高盛供应链调研和推断。
- 客户采用表未披露底层一手文件。
- “已采用”和“采用进展”并不能证明订单、交付、已确认收入、利润或现金流。
