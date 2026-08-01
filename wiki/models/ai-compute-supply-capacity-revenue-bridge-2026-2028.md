---
page_type: model
subject: "AI 算力供给容量—收入桥（2026–2028）"
tags: [model, ai-infrastructure, capacity, revenue-bridge]
tickers: ["NASDAQ:NVDA", "NASDAQ:AMD", "TWSE:2330", "NYSE:TSM", "NASDAQ:MU", "NASDAQ:ASML", "Euronext:ASML", "NASDAQ:AMAT"]
markets: [US, TW, NL, Global]
analysis_regimes: [us_equity, cross_market, other]
policy_jurisdictions: [US, TW, EU, CN]
reporting_currencies: [USD, TWD, EUR]
asset_classes: [equity]
industries: [semiconductors, memory, foundry, semiconductor-equipment]
themes: [AI infrastructure, accelerators, HBM, advanced nodes]
as_of: 2026-07-16
sources:
  - "[[nvidia-q1-fy2027-official-source-pack|NVIDIA Q1 FY2027 官方披露资料包]]"
  - "[[amd-q1-2026-official-source-pack|AMD Q1 2026 官方披露资料包]]"
  - "[[tsmc-q2-2026-official-source-pack|TSMC Q2 2026 官方披露资料包]]"
  - "[[micron-q3-fy2026-official-source-pack|Micron Q3 FY2026 官方披露资料包]]"
  - "[[asml-q2-2026-official-source-pack|ASML Q2 2026 官方披露资料包]]"
  - "[[applied-materials-q2-fy2026-official-source-pack|Applied Materials Q2 FY2026 官方披露资料包]]"
created: 2026-07-28
updated: 2026-07-28
status: provisional
confidence: medium
horizon: 12-24m
review_after: 2026-10-31
base_currency: USD
units: "GW、units、GB、wafer starts、systems、US$bn；缺失值保持 assumption"
---

# AI 算力供给容量—收入桥（2026–2028）

## 目的与范围

把云厂商容量计划连接到 accelerator、HBM、晶圆代工、EUV 和半导体设备收入。模型只定义桥接关系；公开材料未披露的 accelerator ASP、HBM GB/system、wafer die yield、封装良率和设备强度均保持 `model_assumption`。

## 证据阶段

`容量规划（GW） → 技术认证/客户 forecast → 正式订单 → 采购承诺 → 生产/出货 → 客户部署 → 收入 → 毛利 → FCF`

任何一层都不能自动跨越到下一层。

## 已报告输入

| 环节 | 公司 | 指标 | 期间 | 数值 | 证据类型 | 来源 |
|---|---|---|---|---:|---|---|
| accelerator/network | NVIDIA | Data Center 收入 | Q1 FY2027 | US$75.2bn | verified_fact | [[nvidia-q1-fy2027-official-source-pack|NVDA]] |
| accelerator/CPU | AMD | Data Center 收入 | Q1 2026 | US$5.8bn | verified_fact | [[amd-q1-2026-official-source-pack|AMD]] |
| foundry | TSMC | 7nm 及以下晶圆收入占比 | Q2 2026 | 77% | verified_fact | [[tsmc-q2-2026-official-source-pack|TSMC]] |
| memory | Micron | Cloud Memory / Core DC 收入 | Q3 FY2026 | US$13.769bn / US$11.524bn | verified_fact | [[micron-q3-fy2026-official-source-pack|MU]] |
| lithography | ASML | Q2 净销售额 | Q2 2026 | €9.3bn | verified_fact | [[asml-q2-2026-official-source-pack|ASML]] |
| equipment | AMAT | Semiconductor Systems 收入 | Q2 FY2026 | US$5.965bn | verified_fact | [[applied-materials-q2-fy2026-official-source-pack|AMAT]] |

## 公司规划输入

| 规划 | 证据类型 | 当前阶段 | 不可推断事项 |
|---|---|---|---|
| AMD/Meta 最高 6GW，首个 1GW MI450 | company_statement | customer program / sampling | 正式订单、ASP、收入和毛利 |
| NVIDIA Vera Rubin 路线图 | company_statement | roadmap | 客户部署和收入 |
| Micron HBM4 HVM、HBM4E 2027 量产 | company_statement | shipment / samples / roadmap | 最终份额、ASP 和稳态毛利 |
| ASML 2027 Low-NA EUV 产能接近订单覆盖 | company_statement | order coverage / capacity plan | 验收和收入 |
| AMAT CY2026 设备业务 >30% 增长 | company_statement | guidance | 订单和分部利润 |

## 计算结构

### Accelerator

`accelerator units = deployed MW × accelerators per MW`

`accelerator revenue = units × blended system or chip ASP × recognized-delivery probability`

### HBM

`HBM demand GB = accelerator units × HBM GB per accelerator`

`HBM revenue = HBM GB × ASP/GB × yield-adjusted sellable rate`

### Foundry 与先进封装

`required wafers = good dies needed ÷ dies per wafer ÷ die yield`

`foundry revenue = wafer starts × wafer ASP + packaging/test value`

### EUV 与 WFE

`equipment revenue = incremental fab capacity × equipment intensity × shipment/acceptance probability`

以上变量中的 units/MW、ASP、yield、设备强度和确认概率均未被本期资料公开披露，默认是 `model_assumption`。

## 情景假设

| 变量 | 保守 | 基准 | 乐观 | 证据类型 |
|---|---|---|---|---|
| 容量规划兑现率 | 低，项目延期 | 分阶段兑现 | 快于计划 | model_assumption |
| accelerator ASP | 竞争下降 | mix 稳定 | 高端 mix 支撑 | model_assumption |
| HBM ASP/供给 | 周期回落 | 紧平衡 | 供不应求 | model_assumption |
| foundry 良率 | ramp 较慢 | 按计划 | 超预期 | model_assumption |
| 设备验收 | 客户延期 | 正常 | 提前 | model_assumption |

## 去重规则

- NVIDIA/AMD Data Center 收入不能与 TSMC/Micron/ASML/AMAT 收入相加为终端 TAM；它们是同一资本链不同收入层。
- Cloud provider 的 capex 是采购方投入，供应商收入是接收方收入；跨层加总只适合现金流追踪，不适合市场规模。
- TSMC 先进制程占比包括非 AI；Micron data center 也不等于纯 HBM。

## 与最新披露勾稽

- NVIDIA/AMD 已有收入，但新产品规划仍需订单与交付核验。
- Micron 已反映强价格周期，不能仅用容量推导收入。
- TSMC 先进节点和 ASML/AMAT 设备需求验证扩产链，但交付/验收存在时间差。

## 风险、局限与失效条件

- GW 缺少统一功率边界，可能包含不同 IT load/PUE。
- accelerator system、chip、rack ASP 口径不同。
- HBM、wafer、packaging 的良率和复合 yield 未公开。
- 出口控制、地缘、客户集中、库存和双重预订会使订单不兑现。
- 当前模型不用于目标价；估值前需公司级股数、净债务、当前价格和正常化 FCF。

## 变更记录

- 2026-07-28：基于六家公司最新官方披露建立首版容量—收入桥和去重规则。
