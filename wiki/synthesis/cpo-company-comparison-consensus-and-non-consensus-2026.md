---
page_type: synthesis
synthesis_type: comparison
subject: "CPO 公司比较：共识、非共识与估值边界（2026）"
tags: [company-comparison, cpo, valuation]
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
  - "[[cpo-company-growth-and-valuation-scenarios-2027-2031|CPO 公司增长与估值情景（2027–2031）]]"
  - "[[cpo-technology-routes-and-product-generations|CPO 技术路线与产品代际]]"
  - "[[cpo-product-architecture-cost-and-margin-model-2026-2031|CPO 产品架构、成本与利润模型（2026–2031）]]"
created: 2026-07-27
updated: 2026-07-28
status: provisional
confidence: medium
horizon: 3-5y
review_after: 2026-10-31
---

# CPO 公司比较：共识、非共识与估值边界（2026）

## 结论与知识截止日

CPO 已从演示和路线图推进到部分交换平台的供应商生产/出货声明，但 LPO、switch CPO 与 XPU optical I/O 处在不同阶段，供应链公司的收入闭环仍不完整。行业研究优先级高；现阶段不能仅凭 TAM、带宽升级或生态名单形成当前价格交易结论。

## 已验证事实

- Broadcom 和 NVIDIA 已公开声称 CPO 交换平台进入 volume production/in production。
- OIF 已形成 CPO module、ELSFP 与管理接口规范。
- Marvell 已完成 Celestial AI 收购。
- Coherent 已展示多种 CPO 技术，并与 NVIDIA 宣布采购/投资合作。
- 本轮覆盖公司均未在监管财报中单列 CPO 收入。
- Broadcom 已公开 Gen 1–4 路线；Cisco 有 3.2T tile 系统演示；Marvell 1.6T SiPh engine 为 sampling；Intel OCI 为 prototype；Ayar Labs 为 EVT/DVT 与 preliminary specification。

## 市场共识

1. AI 集群带宽、功耗和电气连接距离会推动更多光学价值量。
2. CPO 可能先在高端交换机 scale-out 部署，再向 scale-up/XPU 扩展。
3. 高功率 CW laser、ELS、SiPh、FAU、光引擎、封装测试将受益。
4. Broadcom、Marvell、Coherent、Lumentum、Fabrinet、天孚通信等拥有不同环节暴露。

这些共识主要由公司材料和行业研究构成，不等于已实现财务结果。

## 非共识观点

1. **CPO TAM 可能被定义重复放大。** Goldman、Coherent 与 Lumentum 引用的市场口径无法直接勾稽。
2. **生产状态不等于供应链收入。** 平台量产后仍需客户部署、供应商交付和财报确认。
3. **CPO 对可插拔供应商可能同时是增量和替代。** 中际旭创等公司的净影响不能只算新增。
4. **设备弹性可能最大，但收入质量最脆弱。** 罗博特科/ficonTEC 需要经过交付、验收、回款和商誉测试。
5. **资本结构可能抵消业务增长。** Marvell 并购、Coherent 投资、Lumentum 稀释和高 SBC 都会改变每股价值。
6. **带宽升级不必然提高利润。** 200G/400G per lane 可减少 lane/engine 数，也会提高光电联合测试、封装、热和复合良率难度。
7. **集成度提升会重分配价值，不会让全产业链同比例受益。** integrated laser、ELS、DSP removal 与高集成 engine 会改变 laser/PIC/DSP/FAU/OSAT 的收入归属。
8. **标准化有双向影响。** CW-WDM/OIF 可能扩大生态，同时多源采购和接口统一也可能压低份额、ASP 和 terminal margin。

## 公司比较

| 公司 | CPO 角色 | 当前证据阶段 | 增长弹性 | 主要约束 | 合适估值框架 |
|---|---|---|---|---|---|
| Broadcom | ASIC/CPO 平台 | production/shipping 公司陈述 | 中 | 公司体量大、CPO 未单列 | SOTP、FCF |
| Marvell | switch、DSP、Photonic Fabric | 并购完成；远期指引 | 高 | 目标远期、稀释与费用 | SOTP、EV/Sales、DCF |
| Coherent | laser/PIC/FAU/ELS/module | 演示、订单陈述、战略合作 | 高 | 客户未具名、CAPEX 与债务 | EV/Sales、EV/EBITDA、DCF |
| Lumentum | CW laser/ELS | 技术与市场白皮书；财报未单列 | 高 | 预期高、可转债/优先股稀释 | diluted P/E、EV/Sales、DCF |
| Fabrinet | 制造/封装 | NVIDIA 生态；财报未单列 | 中 | 低毛利、客户集中 | P/E、FCF、制造业 EV/Sales |
| 天孚通信 | FAU/无源/engine | 1.6T 量产、CPO 研发 | 高 | Fabrinet 集中、毛利稀释 | P/E、FCF、分产品模型 |
| 中际旭创 | pluggable；潜在 CPO | CPO 未确认收入 | 中/双向 | 替代风险、估值预期 | P/E、FCF、净替代模型 |
| 罗博特科 | 封装测试设备 | 批量订单陈述、在手订单 | 极高但不稳定 | 验收、亏损、商誉 | 订单转化、P/S、情景 DCF |

## 技术路线参照（非本页估值覆盖）

| 公司 | 路线 | 产品/阶段 | 对估值模型的用途 | 不可推导 |
|---|---|---|---|---|
| [[cisco-systems|Cisco]] | switch CPO + ELS | G100、3.2T tile；2023 demo | 系统架构、DSP removal、可维护性情景 | 客户部署、收入、毛利 |
| [[intel-corporation|Intel]] | XPU/compute optical I/O + on-chip laser | 4Tbps 双向 OCI prototype | integrated-laser、工艺和 pJ/bit 情景 | 商业产品与公司整体估值 |
| [[ayar-labs|Ayar Labs]] | UCIe optical I/O + external ELS | TeraPHY 2T/4T/8T；EVT/DVT；规格 preliminary | 测试流程、产品代际、ELS/PIC 价值池 | 量产、产能、收入与私募估值 |
| Marvell | LPO/on-board bridge | 1.6T 8×200G sampling | route mix、engine 集成和 ASP 情景 | 直接并入 6.4T CPO 收入 |
| Broadcom | switch CPO | Gen 1–4；Gen 2 production 声明、Gen 3 发布 | 代际学习、自动化测试、良率方向 | 具体客户份额、产品毛利 |

## 乐观情景

- 102.4T CPO 在 2027–2028 快速规模部署。
- scale-up/XPU CPO 从 2028 起商业化。
- 现场可靠性和 TCO 达到或优于可插拔方案。
- Coherent/Lumentum/天孚等维持高份额且 ASP 降幅可控。

## 基准情景

- CPO 首先限于高端交换机，与可插拔/NPO 长期共存。
- 行业 2031 终端组件价值池约 US$34bn。
- 公司收入逐步兑现，但 R&D、CAPEX、降价和稀释吸收部分价值。

## 悲观情景

- 客户部署慢于产品发布，2028 前主要停留在小规模生产。
- 可插拔和铜连接继续改善 TCO。
- 良率、热、维修和可靠性问题导致采用延期。
- 光学产能扩张造成价格、库存和现金流压力。

## 催化剂

- NVIDIA/Broadcom 客户规模部署或端口数据。
- Coherent/NVIDIA 投资交割与采购收入确认。
- Marvell 204T 送样和 Celestial AI 客户/收入。
- OIF 后续规范及现场可靠性数据。
- 天孚、中际旭创、罗博特科首次单列 CPO 订单或收入。

## 主要风险与失效条件

- “量产”连续多个季度无法形成可观察收入。
- CPO TAM 预测下修或口径被证明重复。
- 客户集中引发降价、取消和库存调整。
- 并购、SBC、可转债、优先股和商誉显著稀释股东回报。

## 估值与当前价格可交易性

模型已给出隔离的增量 EV，但 2026-07-27 无法从统一可靠行情源取得全部公司同一时点的现价、市值和 EV。当前价格可交易性结论保持未完成。行业值得研究不等于当前价格值得买入。

## 证据缺口

- 公司级 CPO 收入、毛利、份额和 ASP。
- 客户认证、不可撤销订单、出货和部署数量。
- 同口径现场功耗、FIT、RMA、维修成本和 TCO。
- 同一时间点市场价格、完全稀释股本、净债务与一致预期。
- route-specific ASP、composite yield、test time、产能利用率和被替代产品毛利。

## 变更记录

- 2026-07-27：基于 31 份官方原件建立首版跨公司比较；保持 `provisional`。
- 2026-07-28：加入产品路线、代际、光源架构、复合良率、替代毛利和单位经济性约束；Cisco、Intel、Ayar Labs 仅作为技术参照。
