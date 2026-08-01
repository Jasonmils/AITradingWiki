---
page_type: model
subject: "CPO 公司增长与估值情景（2027–2031）"
tags: [valuation, cpo, scenario-analysis]
tickers: ["NASDAQ:AVGO", "NASDAQ:MRVL", "NYSE:COHR", "NASDAQ:LITE", "NYSE:FN", "SZSE:300394", "SZSE:300308", "SZSE:300757"]
markets: [US, CN]
analysis_regimes: [a_share, us_equity]
policy_jurisdictions: [CN, US]
reporting_currencies: [CNY, USD]
asset_classes: [equity]
industries: [semiconductors, optical-components, data-center-networking]
themes: [AI infrastructure, co-packaged optics]
as_of: 2026-07-28
sources:
  - "[[cpo-industry-volume-value-model-2026-2031|CPO 行业量价与价值池模型（2026–2031）]]"
  - "[[cpo-company-financial-baseline-2025-2026|CPO 公司财务基线与资本结构（2025–2026）]]"
  - "[[cpo-product-architecture-cost-and-margin-model-2026-2031|CPO 产品架构、成本与利润模型（2026–2031）]]"
  - "[[cpo-technology-routes-and-product-generations|CPO 技术路线与产品代际]]"
created: 2026-07-27
updated: 2026-07-28
status: provisional
confidence: low
horizon: 3-5y
review_after: 2026-10-31
base_currency: "USD and CNY"
units: "as stated"
---

# CPO 公司增长与估值情景（2027–2031）

## 目的与范围

本模型估计 CPO 对各公司 2031 年收入和企业价值的潜在增量。所有公司均未单列 CPO 收入，因此下表只属于 `model_assumption` 压力测试，不是目标价。

## 通用公式

```text
公司 CPO 增量收入
= CPO 终端价值池
× 公司可服务环节占比
× 公司份额
× 收入确认率
- 被替代的原有产品收入
```

```text
增量企业价值
= Σ 概率加权增量 FCF ÷ (1 + WACC)^t
+ terminal value
- stranded CAPEX
```

原有 EV/Sales 仍可作隔离敏感性，但只有在产品毛利和 FCF 无法获得时使用，且不能直接加到当前市值。

## 技术路线对公司输入的修正

| 变量 | 必须如何修正公司模型 | 主要影响 |
|---|---|---|
| Route mix | 分开 LPO/on-board、switch CPO、XPU optical I/O | TAM、收入起点、概率 |
| Product generation | 100G/200G/400G per lane 与 engine/system 带宽分开 | 数量、ASP 年降、研发周期 |
| Light source | ELS 与 integrated laser 分场景 | laser/ELS/PIC/connector 价值归属 |
| Composite yield | 光、电、封装、耦合和 final test 联乘 | 良品成本与爬坡毛利 |
| Testing stage | demo/sampling/EVT/DVT/order/revenue 分概率 | 折现期与失败概率 |
| Substitution | 扣除 pluggable/DSP/retimer 被替代毛利 | 净增量利润 |
| Serviceability | 冗余、备件、MTTR、warranty/RMA | OPEX、现金流和风险溢价 |
| Capital intensity | advanced packaging、test CAPEX、库存和应收 | FCF 转换 |

## 2031 增量收入压力测试

以下百分比均以各公司最近年度或季度年化收入为基准：

| 公司 | 保守 | 基准 | 乐观 | 核心变量 |
|---|---:|---:|---:|---|
| Broadcom | 0%–1% | 1%–3% | 3%–5% | CPO 平台份额；整公司体量大 |
| Marvell | 2%–4% | 5%–10% | 10%–20% | scale-out switch、scale-up optics、Photonic Fabric |
| Coherent | 2%–5% | 10%–20% | 20%–35% | laser/PIC/FAU/ELS/module 垂直价值量 |
| Lumentum | 3%–8% | 15%–30% | 30%–50% | CW laser/ELS 份额与 ASP |
| Fabrinet | 2%–5% | 8%–15% | 15%–25% | 制造份额、良率和客户集中 |
| 天孚通信 | 3%–8% | 15%–25% | 25%–40% | FAU/无源/engine 内容与 Fabrinet 链条 |
| 中际旭创 | -5%–5% | 5%–15% | 15%–25% | CPO 新增与可插拔替代的净额 |
| 罗博特科 | 5%–15% | 30%–60% | 60%–100% | 设备订单转收入、验收和行业 CAPEX |

## 基准情景的增量收入与价值区间

| 公司 | 基准收入起点 | 基准 CPO 增量收入 | 估值倍数假设 | 隔离的增量 EV | 币种 |
|---|---:|---:|---:|---:|---|
| Broadcom | 63.887bn | 0.64–1.92bn | 4×–8× Sales | 2.6–15.4bn | USD |
| Marvell | 约 8.0bn 年收入量级 | 0.40–0.80bn | 4×–8× Sales | 1.6–6.4bn | USD |
| Coherent | 7.22bn 季度年化 | 0.72–1.44bn | 4×–8× Sales | 2.9–11.6bn | USD |
| Lumentum | 3.23bn 季度年化 | 0.48–0.97bn | 5×–10× Sales | 2.4–9.7bn | USD |
| Fabrinet | 4.86bn 季度年化 | 0.39–0.73bn | 1.5×–3× Sales | 0.6–2.2bn | USD |
| 天孚通信 | 51.63 亿元 | 7.7–12.9 亿元 | 4×–8× Sales | 31–103 亿元 | CNY |
| 中际旭创 | 382.40 亿元 | 19.1–57.4 亿元 | 4×–8× Sales | 76–459 亿元 | CNY |
| 罗博特科 | 9.50 亿元 | 2.9–5.7 亿元 | 2×–5× Sales | 5.7–28.5 亿元 | CNY |

## 解读限制

“隔离的增量 EV”不能直接加到当前市值：

- 部分 CPO 收入会替代现有 pluggable、DSP 或其他产品。
- 公司需要投入 R&D、CAPEX、营运资本和客户支持。
- 同一终端价值可能在器件、制造和平台公司之间重复出现。
- Broadcom、Marvell 等综合公司需要 SOTP；Fabrinet 应采用制造业倍数。
- Marvell、Coherent、Lumentum 和罗博特科还需调整并购、稀释、债务和商誉。
- 厂商公布的 pJ/bit、带宽、die-area 或体积优势不能直接替代产品级 gross margin。
- Broadcom 的 Gen 2 production、Marvell 的 sampling、Intel 的 prototype 和 Ayar 的 EVT/DVT 必须使用不同概率。

## 利润率敏感性

| 公司类型 | 增量毛利率压力测试 | 估值方法 |
|---|---|---|
| 平台/ASIC | 55%–75% | SOTP、EV/EBITDA、FCF |
| PIC/laser/engine | 35%–60% | EV/Sales、P/E、DCF |
| 无源器件 | 40%–65% | P/E、EV/EBITDA、FCF |
| 合同制造 | 10%–15% | EV/Sales、P/E、FCF |
| 封装设备 | 30%–45%，但周期性高 | EV/Sales、P/E、订单转化 |

全部为 `model_assumption`，并非公司指引。

## 毛利率区间的再约束

上表原有毛利率区间仅是类型级压力测试。落到单家公司时必须由以下成本桥重新计算：

```text
product gross margin
= 1
- [(component/package/test cost ÷ composite yield)
   + fulfillment + RMA] ÷ ASP
```

若无法取得 composite yield、ASP 和 RMA，估值结果应降低置信度，不得因公司整体毛利率较高而假定 CPO 新产品具有相同毛利率。

## 当前价格与可交易性

2026-07-27 复核时，官方交易所页面未返回完整实时数据，第三方搜索结果的日期和报价不一致。因此本页不写当前价格、目标价或上行空间。只有在同一时间点取得可靠的现价、市值、完全稀释股数和净债务后，才能把增量 EV 转换为每股价值。

## 情景失效条件

- CPO 平台生产未转化为客户规模部署。
- 价格下降快于出货增长。
- 可靠性、热、良率或维护问题延迟采用。
- 客户集中导致降价、订单取消或库存修正。
- XPU CPO 未进入量产，或可插拔/NPO/铜路线保持主导。
- 公司份额、股数、债务或并购会计与假设显著变化。
- integrated/external laser、MRM/MZM、LPO/CPO 等路线变化导致公司可服务环节缩小。
- 规模收入增长但 composite yield、RMA、CAPEX 或营运资本使 FCF 未兑现。

## 变更记录

- 2026-07-27：建立 2031 公司增量收入和隔离增量 EV 压力测试；因当前价格无法可靠统一复核，保持 `provisional` 且不输出目标价。
- 2026-07-28：加入 route mix、产品代际、光源架构、composite yield、测试阶段、替代毛利和 FCF 概率折现约束；原 EV/Sales 结果降格为敏感性而非估值结论。
