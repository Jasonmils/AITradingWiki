---
page_type: concept
subject: "CPO 可靠性与外置激光源（ELS）"
tags: [technology, cpo, els, reliability]
tickers: ["NYSE:COHR", "NASDAQ:LITE", "NASDAQ:CSCO"]
markets: [US]
asset_classes: [equity]
industries: [optical-components, data-center-networking]
themes: [AI infrastructure, co-packaged optics]
as_of: 2026-07-28
sources:
  - "[[oif-co-packaging-framework-01-0|OIF Co-Packaging Framework 01.0]]"
  - "[[oif-elsfp-02-0|OIF ELSFP Implementation Agreement 02.0]]"
  - "[[oif-cpo-external-laser-management-whitepaper|OIF CPO 外置激光源管理白皮书]]"
  - "[[lumentum-els-cpo-reliability-whitepaper-2026-06|Lumentum CPO 外置激光源可靠性白皮书（2026-06）]]"
  - "[[cw-wdm-msa-technical-specifications-rev-1-0|CW-WDM MSA 技术规范 Rev 1.0（2021-06-04）]]"
  - "[[cisco-cpo-system-ofc-2023-03-07|Cisco OFC 2023 CPO 系统演示（2023-03-07）]]"
  - "[[ayar-labs-supernova-light-source-2026-07-28|Ayar Labs SuperNova 多波长光源产品页快照（2026-07-28）]]"
created: 2026-07-27
updated: 2026-07-28
---

# CPO 可靠性与外置激光源（ELS）

## 机制

External Laser Source（ELS，外置激光源）把寿命较短、发热或需要维护的 CW laser 从高价值 CPO engine 中拆出，使激光可以冗余、监控和更换。ELSFP 是可插拔形态之一，不代表所有 CPO 都采用同一形态。

## OIF 证据

- Co-Packaging Framework 的 51.2Tb/s 示例目标：CPO engine 10 FIT、3.2Tb/s laser source 50 FIT，并以约 300 FIT 可插拔模块作比较。
- 原文同时说明 CPO 实施可靠性仍需进一步研究。
- ELSFP 02.0 定义 form factor、热、电气、光学和 CMIS 管理接口。
- 管理白皮书描述 host controller 对 CW source 的状态、告警和冗余管理。

## CW-WDM 与厂商架构补充

- CW-WDM Rev 1.0 区分 modular source（每端口单波长）与 integrated source（每端口多波长），并覆盖 8/16/32 wavelength grid。
- dual ELS 8+8 是 informative 示例：两个 8 波长物理光源可组合为 16 波长，并要求近似温度跟踪；这不是强制实现。
- Cisco 2023 CPO 演示把 ELS 移出高温 ASIC 区域，强调效率、可替换和多源采购。
- Ayar Labs SuperNova 被公司描述为 disaggregated、field-replaceable、最多 16 波长/16 光纤的 ELS。
- 上述厂商性能、合规和成本优势仍是 `company_statement`。

## 不能成立的推导

- 50 FIT 不是当前行业现场平均值。
- 接口标准不是客户认证。
- 外置激光可更换不自动等于系统 TCO 更低。
- Lumentum 白皮书中的 30W→9W 是特定架构比较，不是所有系统实测。
- CW-WDM/OIF 接口标准不证明采购多源化已经实现。
- “field-replaceable”不提供现场 MTTR、备件率或停机成本。
- integrated laser 可能减少 ELS 组件数，但把良率和维修风险集中到 PIC/主封装；两者需情景建模。

## 估值输入

| 输入 | 保守处理 |
|---|---|
| 每个 CPO engine 的 laser 数量 | 按架构情景，不用单一固定值 |
| 冗余 | 纳入额外数量和成本 |
| ASP | 考虑速率提升与年降 |
| 故障率 | 使用情景区间，不把目标当实测 |
| 更换成本 | 纳入备件、人工、停机和库存 |
| 毛利率 | 与产能利用率、良率和竞争绑定 |
| ELS 架构 | 区分 modular、integrated external 与 on-chip laser |
| 波长/光纤 | 保留方向、冗余和 WDM 口径 |
| 现场服务 | 纳入备件、MTTR、停机、RMA 与返修故障域 |

## 跟踪指标

- OIF 后续 IA/勘误。
- 客户现场 FIT、RMA 与服务寿命。
- ELSFP 与板载/集成激光的采用比例。
- Coherent、Lumentum 的实际出货、ASP 和毛利。
- Cisco/Ayar 等系统中的 ELS redundancy、现场替换和多源兼容结果。
- integrated/on-chip laser 与 ELS 在同负载下的系统 TCO。

## 关联

- [[cpo-optical-engine-components-cost-and-margin|CPO 光引擎组成、成本与利润]]
- [[silicon-photonics-and-optical-light-sources|硅光与光学光源]]
- [[cpo-product-architecture-cost-and-margin-model-2026-2031|CPO 产品架构、成本与利润模型（2026–2031）]]
