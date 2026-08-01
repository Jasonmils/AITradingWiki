---
page_type: concept
subject: "CPO 光引擎组成、成本与利润"
aliases: ["CPO BoM", "CPO unit economics", "Optical engine cost stack"]
tags: [technology, cpo, bom, unit-economics]
tickers: ["NASDAQ:AVGO", "NASDAQ:CSCO", "NASDAQ:INTC", "NASDAQ:MRVL", "NYSE:COHR", "NASDAQ:LITE"]
markets: [US, CN]
asset_classes: [equity]
industries: [semiconductors, optical-components, data-center-networking]
themes: [AI infrastructure, co-packaged optics, optical-io]
as_of: 2026-07-28
sources:
  - "[[cw-wdm-msa-technical-specifications-rev-1-0|CW-WDM MSA 技术规范 Rev 1.0（2021-06-04）]]"
  - "[[broadcom-200g-lane-cpo-2025-05-15|Broadcom 第三代 200G/lane CPO（2025-05-15）]]"
  - "[[cisco-cpo-system-ofc-2023-03-07|Cisco OFC 2023 CPO 系统演示（2023-03-07）]]"
  - "[[marvell-1-6t-silicon-photonics-light-engine-2025-03-31|Marvell 1.6T 硅光光引擎（2025-03-31）]]"
  - "[[intel-fully-integrated-optical-io-chiplet-2024-06-26|Intel 全集成 Optical I/O Chiplet（2024-06-26）]]"
  - "[[ayar-labs-teraphy-validation-three-generations-2025-08-28|Ayar Labs TeraPHY 三代工程验证（2025-08-28）]]"
  - "[[ayar-labs-supernova-light-source-2026-07-28|Ayar Labs SuperNova 多波长光源产品页快照（2026-07-28）]]"
created: 2026-07-28
updated: 2026-07-28
---

# CPO 光引擎组成、成本与利润

## 组件地图

CPO/optical I/O 不是单颗芯片，其良品成本与价值池至少包含：

| 层级 | 核心组成 | 主要成本/良率驱动 | 可能的价值池承接者 |
|---|---|---|---|
| Host compute/network | switch ASIC、CPU/GPU/XPU、SerDes | die size、先进制程、I/O 功耗 | ASIC/XPU 设计商、晶圆代工 |
| Package/interconnect | substrate、interposer、socket/LGA、power delivery | bump/attach 良率、翘曲、热应力 | 先进封装、OSAT、socket |
| PIC | waveguide、coupler、MRM/MZM、mux/demux、photodetector | 光刻、工艺偏差、耦合损耗、热调谐 | SiPh/InP 平台、光引擎商 |
| EIC | driver、TIA、CDR/DSP/retimer（按路线） | 高速模拟性能、功耗、die 良率 | 模拟/混合信号与 DSP 供应商 |
| Optical source | CW laser/ELS、integrated laser、SOA | laser yield、老化、温控、冗余 | 激光器/ELS/PIC 供应商 |
| Fiber attach | FAU、fiber、MPO/可拆卸连接器、fiber routing | 亚微米耦合、装配时间、插损 | 精密耦合、连接器、光纤厂商 |
| Control/thermal | MCU、firmware、monitoring、thermal tuning、cooling | 校准、控制软件、散热与电源 | 控制器、系统与散热厂商 |
| Manufacturing/test | wafer sort、known-good-die、EVT/DVT、burn-in、system test | test time、coverage、复合良率 | 测试设备、自动化、OSAT |
| Service | 冗余、备件、现场替换、warranty/RMA | FIT、MTTR、停机与库存 | ELS/系统商、服务体系 |

## 架构如何重新分配价值池

### External laser source

- 激光器远离高温 ASIC，便于冗余、监控和更换。
- 增加 ELS enclosure、连接器、光纤路由、管理与备件价值。
- 多源标准可能扩大可采购市场，也可能压低单一供应商 ASP 和份额。
- CW-WDM MSA 支持 modular 与 integrated source；标准本身不证明低成本。

### Integrated/on-chip laser

- 光源与 PIC 更紧密集成，可能减少外置光纤和独立 ELS。
- 将更多性能、良率和可靠性责任集中到 PIC 工艺和主封装。
- Intel 的片上激光制造历史是公司能力证据，不是所有 CPO 路线的行业良率。

### DSP/retimer 取舍

- Cisco 称缩短电气路径可移除额外 DSP；LPO 也减少重定时。
- 被移除器件的价值不是“新增 CPO TAM”，必须从增量毛利中扣除。
- 较弱的链路裕量可能把成本转移到系统调优、FEC、测试或维护。

### 高集成光引擎

- Marvell 称单封装整合 driver、TIA、SiPh、MCU 与大量光电元件。
- 离散件、PCB 和传统模块装配价值可能下降。
- advanced packaging、晶圆级测试、known-good-die 与整体报废风险可能上升。

## 良品成本公式

```text
单台良品成本
≈（PIC/EIC die
  + laser/ELS
  + driver/TIA/DSP
  + FAU/fiber/connectors
  + advanced packaging
  + wafer/package/system test
  + thermal/control/service hardware）
  ÷ composite yield
  + warranty/RMA
```

`composite yield` 不是单颗 die yield；它包含光、电、封装、耦合和系统测试的联乘效果。任何一个后段失效都可能报废此前已投入的高价值器件。

## 毛利与现金流桥

```text
增量毛利
= CPO/optical-I/O revenue × incremental gross margin
- 被替代的 pluggable/DSP/retimer/既有产品毛利
- qualification、低利用率和初期报废成本
```

```text
增量自由现金流
= 增量毛利
- 增量研发与销售支持
- 先进封装/测试 CAPEX
- 库存和应收占用
- warranty/RMA 与现场服务现金支出
```

公开来源没有经审计的 CPO 单品 ASP、BoM、毛利或 RMA；这些项必须标为 `model_assumption`。

## 代际升级的利润检查表

| 升级 | 可能的正向因素 | 可能的负向因素 |
|---|---|---|
| 100G→200G→400G per lane | 相同带宽所需 lane/engine 数下降，系统密度提升 | 单通道模拟性能、信号完整性、热与测试难度上升 |
| 更多 WDM wavelengths | 单纤带宽和 fiber density 提升 | laser array、mux/demux、热调谐和波长控制更复杂 |
| 更高集成度 | 减少离散器件、板面积和装配步骤 | 复合良率下降，单点失效报废价值增加 |
| external→integrated laser | 降低外部接口和 ELS 组件数 | 维修性下降，PIC/laser 联合良率风险增加 |
| prototype→volume | 学习曲线、利用率和采购规模改善 | 认证、库存、质保和现场问题开始显性化 |

## 厂商公开数据的可用边界

| 来源 | 可用于 | 不可直接用于 |
|---|---|---|
| Cisco 功耗声明 | 系统功耗敏感性方向 | 产品毛利或客户 TCO 结论 |
| Intel die-area/功耗/FIT 声明 | 集成激光路线的工艺假设 | OCI 商业收入、全行业良率 |
| Marvell `<5pJ/bit` | LPO engine 性能情景 | 完整交换系统功耗与毛利 |
| Ayar EVT/DVT 与 wafer sort | 测试流程和商业阶段 | 量产、产能或收入 |
| Broadcom OSAT/yield 改进 | 制造学习曲线的定性证据 | 具体良率百分比或单位成本 |
| CW-WDM/OIF 标准 | 接口、波长与架构边界 | 采用率、ASP、份额或利润 |

## 估值使用原则

- 先算 route-specific revenue，再算被替代收入和内部重复计量。
- 以良品成本而不是裸 die/器件采购价计算毛利。
- 把产能利用率、良率和 ASP 年降同时纳入，不用静态毛利率。
- 把 CAPEX、库存、质保和 RMA 从 EBITDA 桥接到 FCF。
- 技术规格、demo、sampling、EVT/DVT 使用不同商业化概率。
- 标准化既可能扩大 TAM，也可能降低议价权和 terminal margin。

## 关键缺口

- 产品级 ASP、BoM、gross margin、composite yield、test time、RMA/FIT。
- 客户 qualification 数量、volume ramp、取消率和价格条款。
- integrated laser 与 ELS 在同一平台、同一负载下的 TCO 比较。
- 高集成封装的报废价值、维修边界和现场寿命分布。

## 关联

- [[cpo-technology-routes-and-product-generations|CPO 技术路线与产品代际]]
- [[cpo-reliability-and-external-laser-source|CPO 可靠性与外置激光源]]
- [[cpo-product-architecture-cost-and-margin-model-2026-2031|CPO 产品架构、成本与利润模型（2026–2031）]]
- [[cpo-value-chain-and-company-exposure|CPO 价值链与公司暴露度]]
