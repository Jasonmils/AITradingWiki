---
page_type: source
subject: "高盛全球科技：光网络"
aliases:
  - "Goldman Sachs Global Tech Optical Networking (2026-04-17)"
  - "高盛全球科技：光网络（2026-04-17）"
tags:
  - third-party-research
  - sell-side-research
  - optical-networking
  - ai-infrastructure
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
  - optical circuit switching
as_of: 2026-04-17
sources:
  - "raw/CPO-report-GoldmanSachs.pdf"
created: 2026-07-24
updated: 2026-07-24
---

# 高盛全球科技：光网络（2026-04-17）

## 来源元数据

- 原始文件：`raw/CPO-report-GoldmanSachs.pdf`
- 完整标题：*Global Tech: Optical Networking — The next mega trend in AI infrastructure*
- 来源类型：第三方卖方股票研究；全球科技主题报告
- 出版机构：Goldman Sachs Global Investment Research
- 封面主要分析师：Allen Chang；Verena Jeng；James Schneider, Ph.D.；Mark Delaney, CFA；Ryo Harada
- 参与作者：报告在 PDF 第 2 页列出 26 名作者
- 发布日期：2026-04-17，2:11 AM HKT
- 覆盖期间：从 2024 年历史观察到 2028E 预测；核心 TAM 预测覆盖 2026E–2028E
- 知识截止日：2026-04-17
- 主要主题：作为 AI 基础设施扩展层的光网络，包括 scale-up、scale-out 和 scale-across 连接
- 报告中的 CPO 全称：Co-Packaged Optics（共封装光学）
- 文件完整性：当前 PDF 包含 31 个可读 PDF 页面。封面称其为原 34 页报告的 redacted version；策展人确认提供的文件是本次摄入所使用的完整版本。
- 下文页码均指当前可见 PDF 页码。

## 数据口径与免责声明

- `E` 表示报告预测；`GSe` 表示 Goldman Sachs estimates（高盛估算）。
- 标注为 `US$m`、`US$k` 和 `k units` 的数值保留报告原始单位。
- 多个 Exhibit 同时引用“Company data”和 Goldman Sachs Global Investment Research，但未提供底层公司文件，因此这些论断不升级为 `verified_fact`。
- Goldman Sachs 声明其与所覆盖公司存在或寻求业务关系，这可能形成利益冲突。
- 报告称其认为公开信息可靠，但不保证准确或完整；观点、估算和预测截至报告日期，后续可能变化。
- 报告不是个性化投资建议，本页不据此形成任何当前价格判断。

## 摘要

1. Goldman Sachs 认为，随着机架带宽、集群规模和机架间连接提升，光网络正成为 AI 基础设施的重要价值量来源。其高价值配置估算 Rubin Ultra NVL576 全生命周期的 scale-up 加 scale-out TAM 为 US$154.313bn，而 GB300 NVL72 为 US$15.070bn。这是建立在 `model_assumption` 上的 `source_opinion`，不是历史市场事实。
2. 报告将 CPO 描述为一种把光引擎靠近交换 ASIC 或 XPU、缩短电气路径、降低延迟和功耗并支持更高带宽的方案。由于集成度、可维护性和组件生命周期不匹配会约束采用，报告预计可插拔模块、NPO 与 CPO 将长期共存。
3. 报告高端情景假设 CPO 在 Rubin Ultra NVL576 的 US$154bn 价值 TAM 中贡献约 US$91bn，占 59%。核心假设包括 25%–29% 的 scale-out CPO 渗透率，以及特定的 NVIDIA 机架出货和架构估算。
4. 报告预计硅光渗透率将在 2028E 前显著提高，并认为集成度和激光器降本可以降低光模块 BoM。报告同时预计 EML 与 CW laser 供应在 2027 年前仍将紧张，可能在 2H28 恢复平衡。
5. 报告将 Optical Circuit Switch（OCS，光路交换机）视为互补的全光路线，认为其在带宽、功耗和升级周期方面具有优势，同时指出各路线在技术成熟度、插入损耗、可靠性和采用速度方面存在差异。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| 光网络将成为 AI 基础设施的下一个重要价值量来源。 | source_opinion | 2026-04-17 | PDF 第 1、3 页 | medium | 新 GPU 平台的机架网络支出、配比或光学价值量未增长。 |
| 从 GB300 NVL72 到 Rubin Ultra NVL576，单计算单元的 scale-out 价值量可能增长 16 倍，scale-up 可能增长 45 倍。 | source_opinion | 2026-04-17 | PDF 第 3 页 | low | 产品架构、出货量或 ASP 假设与报告存在重大差异。 |
| 当光连接从 scale-out 扩展到 scale-up 时，光模块和光引擎的可服务市场可能扩大 13 倍。 | source_opinion | 2026-04-17 | PDF 第 3 页 | low | CPO/NPO 在 scale-up 中的采用延迟，或铜连接/PCB 路线继续占主导。 |
| 高端情景下，2026E–2028E CPO TAM 合计约 US$97bn。 | model_assumption | 2026-04-17 | PDF 第 11 页 Exhibit 10 | low | CPO 渗透率、机架出货量、光引擎数量或 ASP 低于报告高端情景。 |
| CPO 应先与交换 ASIC 集成，之后再与 XPU 集成。 | source_opinion | 2026-04-17 | PDF 第 14–16 页 Exhibits 18–20 | medium | 商业部署遵循不同的集成路径。 |
| CPO 的优势包括更短电气路径、更低延迟和功耗、更小体积，以及可能减少 DSP/retimer。 | source_opinion | 2026-04-17 | PDF 第 15–16 页 | medium | 系统级测量显示，计入封装和冷却开销后没有这些净收益。 |
| 更高集成度、3D 封装、可维护性和可靠性风险会约束 CPO 采用。 | source_opinion | 2026-04-17 | PDF 第 8、15–16 页 | medium | 现场可靠性和维护成本与可插拔架构趋同。 |
| 在持续的速率迁移过程中，可插拔光模块、NPO 和 CPO 将共存。 | source_opinion | 2026-04-17 | PDF 第 16 页 | medium | 某一种架构比报告预期更快地取代其他架构。 |
| 数据通信光模块中的硅光渗透率从 1Q24 的 6% 上升至 4Q28E 的 45%–46%。 | disputed | 2026-04-17 | PDF 第 17–18 页 Exhibit 26 | low | 一手模型数据解决报告中 45% 与 46% 的不一致。 |
| 光源供应紧张将持续至 2027 年，并可能在 2H28 恢复平衡。 | source_opinion | 2026-04-17 | PDF 第 19–20 页 Exhibit 34 | low | 产能、需求、出口管制或技术组合更早发生变化。 |
| OCS 可以在不更换交换机的情况下通过多种光信号速率，并可能提高带宽和能效。 | source_opinion | 2026-04-17 | PDF 第 22–23 页 Exhibits 40–43 | medium | 部署经济性或插损/可靠性限制抵消这些优势。 |
| 采用速度取决于设施折旧、基础设施准备度、降本进度和技术方向不确定性。 | source_opinion | 2026-04-17 | PDF 第 24 页 Exhibit 46 | medium | 客户部署并不受这些因素影响。 |

## 重要数字

以下数值均抄录自报告。预测和假设不是历史事实。

| 指标 | 原始数值 | 期间 | 发布日期 | 币种 | 单位 | 历史或预测 | PDF 证据 | 证据类型 | 报告来源 |
|---|---:|---|---|---|---|---|---|---|---|
| GB300 NVL72 scale-up 加 scale-out TAM | 15,070 | 全产品生命周期，主要在 2026 年 | 2026-04-17 | USD | US$m | 预测 | 第 10 页 Exhibit 8 | model_assumption | Company data；Goldman Sachs GIR |
| Vera Rubin NVL72 Spec A TAM | 28,291 | 全产品生命周期，2H26–2027 | 2026-04-17 | USD | US$m | 预测 | 第 10 页 Exhibit 8 | model_assumption | Company data；Goldman Sachs GIR |
| Vera Rubin NVL72 Spec B TAM | 29,158 | 全产品生命周期，2H26–2027 | 2026-04-17 | USD | US$m | 预测 | 第 10 页 Exhibit 8 | model_assumption | Company data；Goldman Sachs GIR |
| Rubin Ultra NVL144 Spec A TAM | 73,458 | 全产品生命周期，2H27–2028 | 2026-04-17 | USD | US$m | 预测 | 第 10 页 Exhibit 8 | model_assumption | Company data；Goldman Sachs GIR |
| Rubin Ultra NVL576 Spec B TAM | 154,313 | 全产品生命周期，2H27–2028 | 2026-04-17 | USD | US$m | 预测 | 第 10 页 Exhibit 8 | model_assumption | Company data；Goldman Sachs GIR |
| Rubin Ultra NVL576 Spec B scale-up TAM | 105,970 | 全产品生命周期，2H27–2028 | 2026-04-17 | USD | US$m | 预测 | 第 10 页 Exhibit 8 | model_assumption | Company data；Goldman Sachs GIR |
| Rubin Ultra NVL576 Spec B scale-out TAM | 48,344 | 全产品生命周期，2H27–2028 | 2026-04-17 | USD | US$m | 预测 | 第 10 页 Exhibit 8 | model_assumption | Company data；Goldman Sachs GIR |
| CPO 在 Rubin Ultra NVL576 Spec B TAM 中的贡献 | 约 91,000；59% | 全产品生命周期，主要在 2028 年 | 2026-04-17 | USD | US$m 和 % | 预测 | 第 3 页 | source_opinion | Goldman Sachs GIR |
| CPO TAM 高端情景 | 1,024 / 24,840 / 70,881 | 2026E / 2027E / 2028E | 2026-04-17 | USD | US$m | 预测 | 第 11 页 Exhibit 10 | model_assumption | Company data；Goldman Sachs GIR |
| CPO TAM 低端情景 | 0 / 3,557 / 12,093 | 2026E / 2027E / 2028E | 2026-04-17 | USD | US$m | 预测 | 第 11 页 Exhibit 10 | model_assumption | Company data；Goldman Sachs GIR |
| NVIDIA AI 机架出货量 | 50 / 77 / 121 | 2026E / 2027E / 2028E | 2026-04-17 | — | 千台机架 | 预测 | 第 11 页 Exhibits 10–11 | model_assumption | Company data；Goldman Sachs GIR |
| Scale-out CPO 渗透率，高端情景 | 5% / 25% / 29% | 2026E / 2027E / 2028E | 2026-04-17 | — | % | 预测 | 第 11 页 Exhibit 11 | model_assumption | Company data；Goldman Sachs GIR |
| Scale-out CPO 交换机需求，高端情景 | 15 / 88 / 110 | 2026E / 2027E / 2028E | 2026-04-17 | — | 千台交换机 | 预测 | 第 11 页 Exhibit 11 | model_assumption | Company data；Goldman Sachs GIR |
| CPO 交换机 BoM | 75,803 | 截至 2026-04-17 的模型估算 | 2026-04-17 | USD | US$/switch | 预测 | 第 17 页 Exhibit 22 | model_assumption | Company data；Goldman Sachs GIR |
| CPO 交换机售价 | 130,000 | 截至 2026-04-17 的模型估算 | 2026-04-17 | USD | US$/switch | 预测 | 第 17 页 Exhibit 22 | disputed | Company data；Goldman Sachs GIR |
| 硅光渗透率 | 6% 至 45%–46% | 1Q24 至 4Q28E | 2026-04-17 | — | 数据通信光模块市场占比 | 历史起点与预测终点 | 第 17–18 页 Exhibit 26 | disputed | Company data；Goldman Sachs GIR |
| 800G 光模块 BoM 合计，EML 对比 SiPh | 310 / 230 | 截至 2026-04-17 的模型估算 | 2026-04-17 | USD | US$/module | 预测估算 | 第 18 页 Exhibit 28 | source_opinion | Company data；Goldman Sachs GIR |
| 1.6T 光模块 BoM 合计，EML 对比 SiPh | 500 / 341 | 截至 2026-04-17 的模型估算 | 2026-04-17 | USD | US$/module | 预测估算 | 第 18 页 Exhibit 29 | source_opinion | Company data；Goldman Sachs GIR |
| 光模块供应商毛利率 | 48%–55% | 预计产品组合迁移期；未给出具体年份 | 2026-04-17 | — | % | 预测 | 第 18 页正文 | source_opinion | Goldman Sachs GIR |
| Lumentum OCS backlog | 超过 400 | 2026 年 2 月 | 2026-04-17 | USD | US$m | 二手转述的公司陈述 | 第 22 页 Exhibit 42 | company_statement | Goldman Sachs GIR 引用的 Company data |
| Robotechnik OCS 封装产线订单 | 7.7 | 报告截止日前宣布 | 2026-04-17 | EUR | EURm | 二手转述的公司陈述 | 第 22 页 | company_statement | Goldman Sachs GIR 引用的 Company data |
| OCS 交换机 ASP 区间 | 50–200 | 截至 2026 年 4 月 | 2026-04-17 | USD | US$k/switch | 估算 | 第 23 页 Exhibit 44 | source_opinion | Company data；Goldman Sachs GIR |
| 传统交换机 ASP 区间 | 10–100 | 截至 2026 年 4 月 | 2026-04-17 | USD | US$k/switch | 估算 | 第 23 页 Exhibit 44 | source_opinion | Company data；Goldman Sachs GIR |

## 技术架构与机制

### 连接层级

- Scale-up（纵向扩展）：在一个系统或紧耦合 supernode 内连接更多 GPU 和计算资源；报告也包括跨机架 scale-up。
- Scale-out（横向扩展）：通过交换技术连接更多系统；报告称现代 AI 集群可连接超过 10 万个 GPU。
- Scale-across（跨数据中心扩展）：连接不同地点数据中心内的服务器。
- 详见[[ai-data-center-interconnect-architecture|AI 数据中心互连架构]]。

### CPO 架构

- 报告把光引擎放置在交换 ASIC 或 XPU 附近，以把电气路径从厘米级缩短到毫米级。
- 图示光路包括光引擎、PIC、调制器、光电探测器、MUX/DEMUX、driver/TIA、FAU、外置激光源、光纤/MPO 和 shufflebox。
- 报告同时讨论 CPO with switch ASIC，以及后续的 CPO with XPU。
- 详见[[co-packaged-optics|共封装光学（CPO）]]和[[cpo-switch-commercialization-roadmap-2025-2027|CPO 交换机商业化路线图（2025–2027）]]。

### CPO 与可插拔光模块、NPO 的比较

| 路线 | 报告描述的位置与维护方式 | 报告描述的优势 | 报告描述的约束 | 证据类型 |
|---|---|---|---|---|
| 可插拔光模块 | 位于封装交换机/XPU 外部的可更换模块 | 可维护性成熟；可靠性记录较长 | 高带宽下受电气路径、功耗和密度约束 | source_opinion |
| NPO/on-board optics | 光学器件安装在交换机板卡上 | 电气路径短于可插拔模块 | 光学故障可能需要更换交换机 PCB | source_opinion |
| CPO with switch | 光学器件与交换 ASIC 共封装 | 密度更高、路径更短、能效更好 | 故障可能影响交换 ASIC；封装和维护更复杂 | source_opinion |
| CPO with XPU | 光学器件与 GPU/CPU/NPU 等 XPU 共封装 | 潜在的 scale-up 带宽和密度优势 | 故障可能影响高价值 XPU；采用时间仍不明确 | source_opinion |

### 报告覆盖的 CPO 组件

报告明确覆盖光引擎、PIC/EIC、调制器、光电探测器、MUX/DEMUX、FAU、ELS/CW laser、光纤与 MPO 连接、shufflebox、交换 ASIC、DSP、retimer 以及 3D/半导体级封装。报告讨论了能效、维护、可靠性和封装，但没有提供量化冷却模型、量化良率模型或一手可靠性测试数据。

## 产品、公司与竞争关系

### 核心关联 Entity

- [[nvidia|NVIDIA Corporation（英伟达）]]：GB300、Vera Rubin、Rubin Ultra、Quantum-X Photonics 和 Spectrum-X Photonics 的架构假设。
- [[broadcom|Broadcom Inc.（博通）]]：报告描述的 Bailly 和 Davisson CPO 交换机路线图。
- [[marvell-technology|Marvell Technology, Inc.（迈威尔科技）]]：报告描述的 CPO 以太网交换机和面向 XPU 的路线图。

### 保留在本 Source 页面的其他公司与产品

- 客户/平台方：Google、Amazon、Meta、Microsoft、Oracle、Huawei、Biren 及中国 CSP。
- CPO/NPO 与光学供应商：Ranovus、MediaTek、Ruijie、Innolight、Robotechnik、Lumentum、Coherent、VPEC、Landmark、YJ Semi 和 Accelink。
- 报告未提供这些公司的证券代码。若不存在持续研究需要和有证据支持的标识符，则不创建独立 Entity。

### 竞争路线

- CPO 对比可插拔光模块和 NPO。
- 硅光对比基于 EML 的分立式光模块。
- CPO 光源中的 CW laser、VCSEL 与 MicroLED。
- OCS 中的 MEMS、LC/LCoS、Piezo/DLBS 和 SiPh 路线。
- 在不同距离、速率、功耗和成本要求下，铜连接/PCB 路线对比光学路线。

## 催化剂、风险与跟踪指标

### 报告描述的催化剂

- CPO 交换机实现商业可用并向客户交付。
- 光速率从 800G 迁移至 1.6T，之后再向 3.2T 迁移。
- Vera Rubin 与 Rubin Ultra 机架出货。
- CPO 在 scale-out 和跨机架 scale-up 中的采用。
- 客户部署 OCS，以及供应商订单/backlog 增长。
- InP、EML 和 CW laser 产能扩张。

### 报告描述的主要风险

- 新数据中心基础设施、电网和散热条件未准备就绪，可能延迟采用。
- 客户可能等待现有资产折旧完毕，或等待新技术成本下降。
- CPO、可插拔、NPO 与 OCS 之间的技术方向仍不确定。
- 高集成度、封装、维护和可靠性风险可能减缓 CPO 采用。
- InP 衬底、EML 和 CW laser 产能约束可能限制出货。
- 报告假设可能过于乐观；报告明确称其 CPO 渗透率观点是“optimistic perspective”。

### 可验证或推翻报告的指标

- 分别跟踪 CPO 交换机的实际可用性、客户认证、正式订单、交付、已确认收入、利润和现金流。
- NVIDIA 机架实际出货量，对比 2026E/2027E/2028E 的 50k/77k/121k。
- CPO scale-out 实际渗透率，对比报告高端情景的 5%/25%/29% 路径。
- 单 GPU 的光模块与光引擎配比。
- 1.6T 和 3.2T 模块组合及硅光渗透率。
- CPO 实测功耗、延迟、可维护性、热表现、良率和现场可靠性。
- 光引擎、ELS、FAU、光纤/MPO 和 shufflebox ASP。
- InP 衬底、EML 和 CW laser 产能与交期。
- OCS 客户部署、供应商 backlog 转化和已确认收入。

## 实体

- [[nvidia|NVIDIA Corporation（英伟达）]]
- [[broadcom|Broadcom Inc.（博通）]]
- [[marvell-technology|Marvell Technology, Inc.（迈威尔科技）]]

## 概念

- [[co-packaged-optics|共封装光学（CPO）]]
- [[ai-data-center-interconnect-architecture|AI 数据中心互连架构]]
- [[silicon-photonics-and-optical-light-sources|硅光与光学光源]]
- [[optical-circuit-switch|光路交换机（OCS）]]

## 事件

- [[cpo-switch-commercialization-roadmap-2025-2027|CPO 交换机商业化路线图（2025–2027）]]

OCS 订单、backlog 和客户接洽论断保留在本 Source 页面和[[optical-circuit-switch|光路交换机（OCS）]]中。由于未提供一手公告，不将其升级为独立 Event。

## 提及的模型或假设

- [[goldman-sachs-ai-optical-networking-tam-2026-2028e|高盛 AI 光网络 TAM 与 CPO 渗透模型（2026–2028E）]]

报告未提供完整的公司三情景财务模型、目标价表或可审计的当前估值。因此未创建投资论点或交易建议。

## 证据缺口与冲突

1. **页数冲突（`disputed`）**：文件包含 31 个 PDF 页面；封面称其为原 34 页报告的 redacted version；策展人确认提供的版本可作为完整摄入版本。本 Source 页面只覆盖当前可见内容。
2. **Exhibit 编号缺口**：当前可见 Exhibit 缺少 4、13、21、33、35、37、48 和 49，无法重建其内容。
3. **价值量单位冲突（`disputed`）**：PDF 第 3 页称单计算单元从 US$315k 增长 29 倍至 US$9.4bn。29 倍计算及第 9 页机架表均无法与 `bn` 单位勾稽，因此保留原文，不静默修正。
4. **硅光渗透率冲突（`disputed`）**：第 17 页 Exhibit 26 写 4Q28E 为 46%，第 18 页正文写 45%。
5. **CPO 交换机算术冲突（`disputed`）**：Exhibit 22 列示 BoM US$75,803、markup US$62,220、售价 US$130,000，所列组件无法直接算术勾稽。
6. **缺少一手支持**：公司产品日期、交付、backlog、订单、产能计划、架构细节和管理层陈述均未对照一手公告核验。
7. **没有明确市场共识**：报告没有明确标识 market-consensus 预测。其关于 CPO 的“optimistic perspective”标记为 `source_opinion`，而不是 `market_consensus` 或 `non_consensus`。
8. **里程碑严格分离**：发布、送样、认证、订单、交付、已确认收入、利润和现金流保持独立；报告没有证明每一步转换。
