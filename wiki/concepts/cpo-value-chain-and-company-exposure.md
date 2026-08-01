---
page_type: concept
subject: "CPO 价值链与公司暴露度"
tags: [industry-framework, cpo, value-chain]
tickers: ["NASDAQ:NVDA", "NASDAQ:AVGO", "NASDAQ:MRVL", "NYSE:COHR", "NASDAQ:LITE", "NYSE:FN", "SZSE:300394", "SZSE:300308", "SZSE:300757"]
markets: [US, CN]
asset_classes: [equity]
industries: [semiconductors, optical-components, data-center-networking]
themes: [AI infrastructure, co-packaged optics]
as_of: 2026-07-27
sources:
  - "[[coherent-ofc-investor-event-2026-03-17|Coherent OFC 2026 Investor Event]]"
  - "[[oif-co-packaging-3-2t-module-01-0|OIF 3.2Tb/s CPO Module Implementation Agreement 01.0]]"
created: 2026-07-27
updated: 2026-07-27
---

# CPO 价值链与公司暴露度

## 价值链

| 环节 | 主要价值量 | 代表公司 | 估值关注点 |
|---|---|---|---|
| 平台/交换 ASIC | switch ASIC、系统平台 | NVIDIA、Broadcom、Marvell | 平台份额、SOTP、软件/其他业务混合 |
| PIC/EIC/光引擎 | SiPh/InP、driver/TIA、engine | Coherent、Marvell、天孚通信 | ASP、良率、集成度、份额 |
| 激光与 ELS | CW laser、ELSFP | Coherent、Lumentum | 功率、可靠性、冗余、降价 |
| FAU/无源器件 | FAU、MPO、光纤、shuffle | 天孚通信等 | 单机价值量、客户集中、毛利 |
| 制造与封装 | 精密装配、封装、测试 | Fabrinet、ficonTEC | 利用率、良率、验收、制造毛利 |
| 可插拔替代/共存 | 高速 pluggable modules | 中际旭创等 | 增量与被替代需求必须同时建模 |

## 暴露度分层

1. **已确认 CPO 收入**：财报明确单列。
2. **CPO 相关收入**：产品同时服务 CPO 与其他光学路线。
3. **CPO 潜在收入**：已有订单/认证但未确认收入。
4. **技术或生态暴露**：研发、展示或伙伴名单。

截至 2026-07-27，本轮公司普遍没有单列第 1 层数据。因此任何逐公司 CPO 收入预测都必须标为 `model_assumption`。

## 估值含义

- 平台公司应用 SOTP，不能用整公司市值除以 CPO TAM。
- 器件公司需要用 CPO 单机价值量 × 份额 × 毛利率。
- 制造公司收入弹性可能大，但毛利率通常低于器件供应商。
- 设备公司应以订单转收入、验收和周期性建模。
- 可插拔供应商既可能受益于 AI 光网络，也可能受 CPO 替代。
