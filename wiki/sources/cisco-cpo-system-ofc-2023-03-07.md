---
page_type: source
subject: "Cisco OFC 2023 CPO 系统演示"
tags: [company-blog, cpo, ethernet-switch]
tickers: ["NASDAQ:CSCO"]
markets: [US]
asset_classes: [equity]
industries: [networking-equipment, data-center-networking]
themes: [AI infrastructure, co-packaged optics]
as_of: 2023-03-07
sources:
  - "raw/2023-03-07-cisco-cpo-system-ofc-2023.html"
created: 2026-07-28
updated: 2026-07-28
---

# Cisco OFC 2023 CPO 系统演示（2023-03-07）

## 来源元数据

- 来源类型：公司技术博客
- 发布机构：Cisco Systems, Inc.
- 发布日期与知识截止日：2023-03-07
- 原始文件：`raw/2023-03-07-cisco-cpo-system-ofc-2023.html`
- 本地源文件状态：不可变原始 HTML；SHA-256 `2c7d2b03beecfffffb868b61a9ce174702220791a3b5226c67b379d331ab0993`

## 摘要

Cisco 展示基于 Silicon One G100 的 CPO 系统，把 3.2T optical tile 放到交换 ASIC 附近，并用外置激光源供光。来源解释了缩短电气路径、移除额外 DSP、光源可维护性与系统热设计，但属于演示与公司性能陈述。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| Cisco 在 OFC 2023 展示基于 Silicon One G100 的 CPO 系统。 | verified_fact | 2023-03-07 | 公司博客与系统照片 | high | 公司更正演示记录。 |
| 单个 optical tile 为 3.2T，集成 TIA、driver、modulator、mux/demux 等功能。 | company_statement | 2023-03-07 | 公司架构说明 | high | 正式产品规格改变。 |
| 演示覆盖 64×400G FR4 与 128×400G 机箱配置。 | company_statement | 2023-03-07 | 系统演示说明 | high | 后续勘误。 |
| 外置激光源远离高温 ASIC，可支持效率、可替换与多源采购。 | company_statement | 2023-03-07 | 公司路线说明 | medium | 现场可靠性或供应链实践不支持。 |
| 公司称互连功耗最高可降 50%，固定系统功耗最高可降 25%–30%。 | company_statement | 2023-03-07 | 公司系统比较 | medium | 独立同口径测试无法复现。 |
| Cisco 当时预期 51.2T 周期开始 trials，并在原文所写“101.2Tb”节点扩大采用。 | company_statement | 2023-03-07 | 公司路线图；保留原文数字 | low | 后续路线图或勘误替代。 |
| 来源未披露正式订单、规模部署、收入或利润。 | verified_fact | 2023-03-07 | 博客全文 | high | 后续一手披露补充。 |

## 实体

- [[cisco-systems|Cisco Systems, Inc.（思科）]]

## 概念

- [[co-packaged-optics|共封装光学（CPO）]]
- [[cpo-reliability-and-external-laser-source|CPO 可靠性与外置激光源]]
- [[cpo-optical-engine-components-cost-and-margin|CPO 光引擎组成、成本与利润]]

## 事件

- [[cpo-switch-commercialization-roadmap-2025-2027|CPO 与光学 I/O 商业化路线图]]

## 提及的模型或假设

- DSP 移除、电气路径缩短和系统功耗下降可以影响价值池与 TCO，但来源不提供可审计 BoM 或毛利。

## 证据缺口与冲突

- 系统演示不等于客户认证、订单、交付、收入、利润或现金流。
- 原文使用“101.2Tb”；本页不擅自改写为其他容量节点。
- 功耗比较缺少端口利用率、冷却、维护和完整系统边界。
