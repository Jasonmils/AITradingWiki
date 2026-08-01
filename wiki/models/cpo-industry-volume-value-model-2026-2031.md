---
page_type: model
subject: "CPO 行业量价与价值池模型（2026–2031）"
tags: [tam, cpo, scenario-analysis]
tickers: ["NASDAQ:NVDA", "NASDAQ:AVGO", "NASDAQ:MRVL", "NYSE:COHR", "NASDAQ:LITE"]
markets: [US, CN]
analysis_regimes: [a_share, us_equity]
policy_jurisdictions: [CN, US]
reporting_currencies: [CNY, USD]
asset_classes: [equity]
industries: [semiconductors, optical-components, data-center-networking]
themes: [AI infrastructure, co-packaged optics]
as_of: 2026-07-28
sources:
  - "[[goldman-sachs-ai-optical-networking-tam-2026-2028e|高盛 AI 光网络 TAM 与 CPO 渗透模型（2026–2028E）]]"
  - "[[coherent-ofc-investor-event-2026-03-17|Coherent OFC 2026 Investor Event]]"
  - "[[lumentum-els-cpo-reliability-whitepaper-2026-06|Lumentum CPO 外置激光源可靠性白皮书（2026-06）]]"
  - "[[oif-co-packaging-3-2t-module-01-0|OIF 3.2Tb/s CPO Module Implementation Agreement 01.0]]"
  - "[[cpo-technology-routes-and-product-generations|CPO 技术路线与产品代际]]"
  - "[[cpo-product-architecture-cost-and-margin-model-2026-2031|CPO 产品架构、成本与利润模型（2026–2031）]]"
created: 2026-07-27
updated: 2026-07-28
status: provisional
confidence: low
horizon: 3-5y
review_after: 2026-10-31
base_currency: USD
units: "US$bn unless stated"
---

# CPO 行业量价与价值池模型（2026–2031）

## 目的与范围

本模型把 CPO 市场拆为交换机/XPU 数量、CPO 渗透率、每系统光引擎数量、单引擎价值量和 ASP 下降。它用于压力测试，不采纳任何单一机构 TAM 作为事实。

模型必须先将 retimed pluggable、LPO/LRO/on-board、switch CPO 与 XPU optical I/O 分桶。Marvell 1.6T LPO sampling、Broadcom/NVIDIA 交换平台生产声明和 Intel/Ayar optical I/O prototype/validation 不共享同一商业化概率。

## 核心公式

```text
CPO 价值池
= 系统出货量
× CPO 渗透率
× 每系统 CPO engine 数量
× 每 engine 价值量
× 收入确认率
```

再按组件拆分：

```text
平台价值 + PIC/EIC/engine + laser/ELS + FAU/MPO/fiber
+ 封装制造 + 测试设备 - 产业链内部重复计量
```

新增 route-specific 约束：

```text
行业净增量价值池
= Σ route revenue
- 被替代 pluggable/DSP/retimer 价值
- 上下游内部重复计量
```

## 已验证边界

- Broadcom 和 NVIDIA 已公开声称 CPO 平台进入 volume production/in production。
- OIF 已定义 3.2Tb/s CPO module、ELSFP 和管理接口。
- 这些证据不能提供出货量、客户份额、ASP 和已确认收入。
- Cisco demo、Marvell sampling、Intel prototype 与 Ayar EVT/DVT 验证了更早的产品阶段，不得按 production 收入概率处理。

## 外部预测对照

| 来源 | 2027E | 2028E | 2030E | 2031E | 口径 | 证据类型 |
|---|---:|---:|---:|---:|---|---|
| Goldman 低端 | 3.557 | 12.093 | — | — | CPO TAM | model_assumption |
| Goldman 高端 | 24.840 | 70.881 | — | — | CPO TAM | model_assumption |
| Coherent/LightCounting | — | — | >15 | — | CPO SAM | source_opinion |
| Lumentum/LightCounting | — | — | — | 52.1 | AI optics，不等同于 CPO | source_opinion |
| Lumentum/LightCounting | — | — | — | 约 3m ports | CPO ports | source_opinion |

不同来源的市场定义明显不一致。Goldman 高端 2028 CPO TAM 已高于 Lumentum 引用的 2031 全部 AI optics 预测，说明不能把这些数字直接拼接成时间序列。

## Wiki 规范化压力测试

为避免沿用极端来源，本模型采用较窄的“终端 CPO 组件价值池”区间：

| 情景 | 2027E | 2028E | 2029E | 2030E | 2031E | 证据类型 |
|---|---:|---:|---:|---:|---:|---|
| 保守 | 3.0 | 8.0 | 11.0 | 15.0 | 18.0 | model_assumption |
| 基准 | 6.0 | 15.0 | 21.0 | 28.0 | 34.0 | model_assumption |
| 乐观 | 12.0 | 30.0 | 40.0 | 50.0 | 60.0 | model_assumption |

这些数字不是预测结论，只是估值敏感性输入：

- 保守情景接近 Goldman 低端并延伸至 Coherent 的 US$15bn+ 2030 SAM。
- 基准情景假设 CPO 从交换机 scale-out 逐步进入部分 scale-up。
- 乐观情景仍低于 Goldman 2028 高端值，并假设 ASP 下滑被端口和系统数量抵消。

## 关键假设

| 假设 | 保守 | 基准 | 乐观 | 证据类型 |
|---|---|---|---|---|
| 商业化状态 | 主要限于高端交换机 | 交换机规模采用，部分 scale-up | scale-out 与 scale-up 同时快速采用 | model_assumption |
| ASP 年降 | 15%–20% | 10%–15% | 5%–10% | model_assumption |
| 良率/认证 | 改善缓慢 | 逐年改善 | 快速成熟 | model_assumption |
| 可插拔共存 | 长期占主导 | 与 CPO 分层共存 | 高端场景被 CPO 快速替代 | model_assumption |
| XPU CPO | 2031 后 | 2029–2031 逐步导入 | 2028 起快速导入 | model_assumption |
| LPO/on-board route mix | 较高，延缓 switch CPO | 与 switch CPO 分层共存 | 作为 CPO 快速导入桥梁 | model_assumption |
| External laser mix | 高，强调可维护性 | ELS/集成激光分场景 | 集成激光快速提升 | model_assumption |
| Composite yield | 改善慢 | 代际学习改善 | wafer sort/自动化测试快速成熟 | model_assumption |
| RMA/服务成本 | 高于预期 | 可控 | 接近成熟平台 | model_assumption |

## 价值池分配压力测试

| 环节 | 保守占比 | 基准占比 | 乐观占比 | 说明 |
|---|---:|---:|---:|---|
| 平台/交换 ASIC | 20% | 18% | 15% | 集成度提高但光学价值量增长 |
| PIC/EIC/光引擎 | 35% | 38% | 40% | 核心光电转换 |
| laser/ELS | 10% | 12% | 12% | 受冗余、功率和降价影响 |
| FAU/MPO/fiber | 20% | 18% | 18% | 数量增长与 ASP 年降并存 |
| 制造、封装与测试 | 15% | 14% | 15% | 不与上游器件收入重复计量 |

所有比例均为 `model_assumption`，只用于公司暴露敏感性。

## 单位经济性勾稽

价值池分配不能直接作为供应商毛利。对每条路线还需计算：

```text
good-unit cost
= yield-bearing component/package/test cost ÷ composite yield
+ post-yield fulfillment + warranty/RMA
```

```text
industry incremental gross profit
= new-route revenue × gross margin
- displaced-product gross profit
- qualification and ramp losses
```

详细输入与良率凸性见[[cpo-product-architecture-cost-and-margin-model-2026-2031|CPO 产品架构、成本与利润模型（2026–2031）]]。

## 失效条件

- 客户部署未从生产推进到规模出货。
- 可插拔/铜/NPO 在 102.4T 及以上继续满足 TCO。
- CPO 现场可靠性、热、良率或维修成本显著差于假设。
- 组件 ASP 下滑快于系统与端口增长。
- 不同报告的 TAM 定义无法归一化。
- route mix、带宽方向和产品层级被错误合并。
- 良率、测试、RMA 与替代毛利使收入价值池无法转化为 FCF。

## 变更记录

- 2026-07-27：建立官方产品、OIF 规范和三组外部预测之间的规范化压力测试；模型保持 `provisional`。
- 2026-07-28：加入 LPO/on-board、switch CPO、XPU optical I/O 分桶，以及光源路线、composite yield、RMA 和替代毛利约束。
