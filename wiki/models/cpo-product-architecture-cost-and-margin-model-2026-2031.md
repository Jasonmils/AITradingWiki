---
page_type: model
subject: "CPO 产品架构、成本与利润模型（2026–2031）"
tags: [cpo, unit-economics, scenario-analysis, valuation]
tickers: ["NASDAQ:AVGO", "NASDAQ:CSCO", "NASDAQ:INTC", "NASDAQ:MRVL", "NYSE:COHR", "NASDAQ:LITE"]
markets: [US, CN]
analysis_regimes: [a_share, us_equity]
policy_jurisdictions: [CN, US]
reporting_currencies: [CNY, USD]
asset_classes: [equity]
industries: [semiconductors, optical-components, data-center-networking]
themes: [AI infrastructure, co-packaged optics, optical-io]
as_of: 2026-07-28
sources:
  - "[[cpo-technology-routes-and-product-generations|CPO 技术路线与产品代际]]"
  - "[[cpo-optical-engine-components-cost-and-margin|CPO 光引擎组成、成本与利润]]"
  - "[[cw-wdm-msa-technical-specifications-rev-1-0|CW-WDM MSA 技术规范 Rev 1.0（2021-06-04）]]"
  - "[[broadcom-200g-lane-cpo-2025-05-15|Broadcom 第三代 200G/lane CPO（2025-05-15）]]"
  - "[[cisco-cpo-system-ofc-2023-03-07|Cisco OFC 2023 CPO 系统演示（2023-03-07）]]"
  - "[[marvell-1-6t-silicon-photonics-light-engine-2025-03-31|Marvell 1.6T 硅光光引擎（2025-03-31）]]"
  - "[[intel-fully-integrated-optical-io-chiplet-2024-06-26|Intel 全集成 Optical I/O Chiplet（2024-06-26）]]"
  - "[[ayar-labs-teraphy-validation-three-generations-2025-08-28|Ayar Labs TeraPHY 三代工程验证（2025-08-28）]]"
created: 2026-07-28
updated: 2026-07-28
status: provisional
confidence: low
horizon: 3-5y
review_after: 2026-10-31
base_currency: USD
units: "US$ unless stated; indexed examples are unitless"
---

# CPO 产品架构、成本与利润模型（2026–2031）

## 目的与范围

本模型把技术路线转换为公司收入、毛利、CAPEX、自由现金流和估值概率。它不声称掌握厂商未披露的 CPO 单品毛利；所有 ASP、良率、RMA、成本占比和商业化概率均为 `model_assumption`，需要在公司披露后替换。

## 第一步：建立不重叠的产品桶

| 产品桶 | 数量驱动 | 单位 | 与其他桶的主要重叠风险 |
|---|---|---|---|
| Retimed pluggable | ports/modules | module | 被 CPO 替代时不能同时计入新增 TAM |
| LPO/LRO/on-board engine | ports/engines | engine/module | 与 1.6T pluggable 或 switch CPO 组件重复 |
| Switch CPO | switches × engines/switch | system/engine | ASIC、engine、ELS、fiber 的内部收入重复 |
| XPU optical I/O | XPU packages × chiplets/XPU | package/chiplet | 与整机或 accelerator ASP 重复 |
| ELS/laser | sources/system × redundancy | source/laser | integrated-laser 情景下不能再计完整 ELS |
| Packaging/test/service | good units × attach points/tests | service/value | 已包含在 engine ASP 时不能再次加总 |

## 第二步：从带宽推导物理数量

```text
required lanes
= target unidirectional bandwidth ÷ effective lane rate
```

```text
engines per system
= required optical bandwidth ÷ effective engine bandwidth
× redundancy factor
```

```text
fibers per system
= optical channels ÷ effective wavelengths per fiber
× direction/fiber-pair factor
× redundancy factor
```

`effective` 必须在扣除编码、FEC、spare lanes 与不可用端口后计算。双向 8T 不能不经转换直接与单向 1.6T engine 相加。

## 第三步：单位良品成本

```text
yield-bearing cost pool
= PIC + EIC + laser/ELS + driver/TIA/DSP
+ FAU/fiber/connectors + package/substrate
+ assembly + wafer/package test
```

```text
good-unit cost
= yield-bearing cost pool ÷ composite yield
+ post-yield fulfillment
+ warranty/RMA reserve
```

```text
composite yield
= optical die yield
× electrical die yield
× attach/package yield
× fiber-coupling yield
× final-system-test yield
```

### 纯示意的良率凸性

假定 yield-bearing cost pool 指数为 100、post-yield fulfillment 为 15、ASP 指数为 250；下表只展示数学敏感性，不是行业或公司预测。

| 情景 | composite yield | RMA 指数 | good-unit cost 指数 | 隐含毛利率 | 证据类型 |
|---|---:|---:|---:|---:|---|
| 压力 | 55% | 8 | 204.8 | 18.1% | model_assumption |
| 基准 | 70% | 4 | 161.9 | 35.2% | model_assumption |
| 成熟 | 85% | 2 | 134.6 | 46.2% | model_assumption |

结论仅为：当成本池已投入后，复合良率改善会非线性放大毛利；不能用该表倒推出任何厂商真实毛利。

## 第四步：ASP、收入与替代

```text
route revenue_t
= good units_t × ASP_t × recognized-revenue rate_t
```

```text
ASP_t
= ASP_(t-1) × (1 - annual price decline)
+ mix uplift from higher bandwidth/integration
```

```text
net incremental gross profit
= new-route revenue × new-route gross margin
- displaced pluggable/DSP/retimer revenue × displaced gross margin
- qualification and ramp losses
```

若同一公司同时销售 ASIC、DSP、optical engine 或 pluggable，必须计算 cannibalization；若上下游公司向同一终端系统销售，则行业价值池必须消除重复计量。

## 第五步：利润到自由现金流

```text
incremental operating profit
= net incremental gross profit
- incremental R&D
- sales/application engineering
- warranty/service expense
```

```text
incremental FCF
= operating profit × (1 - cash tax rate)
+ depreciation
- advanced-packaging/test CAPEX
- change in inventory and receivables
```

早期量产可能出现收入增长但 FCF 落后：产能爬坡、低利用率、长测试周期、备货和 RMA 会先占用现金。

## 第六步：路线情景

| 输入 | 保守 | 基准 | 乐观 | 证据类型 |
|---|---|---|---|---|
| Switch CPO 商业化 | 局限于少数高端系统 | 51.2T/102.4T 分层采用 | 高端 scale-out 快速采用 | model_assumption |
| XPU optical I/O | 2031 年后 | 2029–2031 小规模导入 | 2028 起加速 | model_assumption |
| LPO/on-board | 与 pluggable 长期并存 | 部分短距 1.6T 采用 | 成为 CPO 前的规模桥梁 | model_assumption |
| composite yield | 改善慢 | 随代际学习改善 | wafer sort/自动化测试快速成熟 | model_assumption |
| ASP 年降 | 快于 unit 增长 | 与带宽/数量增长大致平衡 | 高集成和稀缺产能保留溢价 | model_assumption |
| external laser mix | 高，强调可维护 | ELS 与集成激光分场景 | 集成激光份额快速提升 | model_assumption |
| RMA/服务 | 高于初始预计 | 可控 | 接近成熟半导体平台 | model_assumption |

## 第七步：公司价值量映射

| 公司类型 | 需要输入 | 容易高估的地方 |
|---|---|---|
| ASIC/platform | CPO attach rate、platform ASP、被替代产品毛利 | 把整个系统 TAM 计为公司收入 |
| PIC/engine | engine 数量、ASP、良率、封装归属 | 用带宽增长等比例推 ASP |
| laser/ELS | 每 source 波长/功率、冗余、integrated mix | 忽略多源采购和 ASP 年降 |
| FAU/fiber/connectors | fibers/engine、连接点、自动化程度 | 把工程样机高价值量外推到量产 |
| OSAT/test equipment | tool/line 数、利用率、服务收入 | 把客户 CAPEX 与供应商收入重复 |
| 系统商 | 终端系统 ASP、光学含量、替代效应 | 忽略售后、质保和被替代模块收入 |

## 第八步：概率加权估值

```text
probability-adjusted CPO value
= Σ [incremental FCF_t × milestone probability_t ÷ (1 + WACC)^t]
+ terminal value
- stranded CAPEX
```

里程碑概率必须单独设置：

- prototype/demo；
- sampling/EVT/DVT；
- technical certification；
- formal order；
- delivery；
- recognized revenue；
- normalized gross margin/FCF。

不能用一个“CPO 概率”覆盖所有阶段。

## 估值倍数桥

| 证据改善 | 可能的倍数影响 | 前提 |
|---|---|---|
| 客户从 demo 进入重复订单 | 降低收入概率折价 | 订单、交付和取消条款可验证 |
| 良率、RMA、毛利可复核 | 降低盈利不确定性 | 不是仅有公司目标 |
| 多客户、多路线兼容 | 降低集中度风险 | 不是同一终端需求的重复订单 |
| 标准化和多源采购 | 降低生态风险，也可能压缩份额/毛利 | TAM 与利润率需双向调整 |
| 专有 PIC/EIC、测试和量产 know-how | 可能提高持续性 | 客户切换成本和份额稳定可验证 |
| 路线延迟或 cannibalization | 提高折价、压低 terminal margin | 现有利润池受损或 CAPEX 沉没 |

## 最低可用数据集

正式计算公司估值前，至少需要：

1. route-specific units、ASP、revenue-recognition；
2. engine/ELS/fiber 数量及带宽口径；
3. composite yield、test time、产能利用率；
4. 产品毛利或可勾稽成本桥；
5. qualification、order、delivery、RMA；
6. 被替代 pluggable/DSP/retimer 毛利；
7. CAPEX、库存、应收和 warranty cash outflow；
8. 客户/平台集中度及双重计量消除；
9. current price 与 fully diluted shares（用于现价可交易性）。

当前公开资料不满足第 1–7 项，因此本模型保持 `provisional`、`confidence: low`。

## 风险、局限与失效条件

- pJ/bit、带宽和体积数据的系统边界不一致。
- 厂商技术声明没有经过统一第三方测试。
- ASP、良率、RMA 与产品毛利缺失，示意情景不能当作真实预测。
- 可插拔、铜、LPO/on-board、switch CPO 与 XPU optical I/O 的 TAM 可能重叠。
- 若客户规模部署或 FCF 未出现，不应仅因产品版本升级提高估值。

## 变更记录

- 2026-07-28：基于 CW-WDM MSA、Broadcom、Cisco、Intel、Marvell 与 Ayar Labs 一手资料建立 route-specific 单位经济性与概率加权估值桥。
