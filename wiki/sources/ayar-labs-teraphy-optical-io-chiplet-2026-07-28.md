---
page_type: source
subject: "Ayar Labs TeraPHY Optical I/O Chiplet 产品页快照"
tags: [company-product-page, optical-io, chiplet]
tickers: []
markets: [US]
asset_classes: [private-company]
industries: [semiconductors, optical-components, data-center-networking]
themes: [AI infrastructure, co-packaged optics, optical-io]
as_of: 2026-07-28
sources:
  - "raw/2026-07-28-ayar-labs-teraphy-optical-io-chiplet.html"
created: 2026-07-28
updated: 2026-07-28
---

# Ayar Labs TeraPHY Optical I/O Chiplet 产品页快照（2026-07-28）

## 来源元数据

- 来源类型：公司当前产品页快照
- 发布机构：Ayar Labs
- 页面抓取与知识截止日：2026-07-28
- 页面未标示独立发布日期
- 原始文件：`raw/2026-07-28-ayar-labs-teraphy-optical-io-chiplet.html`
- 本地源文件状态：不可变原始 HTML；SHA-256 `d806750807fc12b0dc31b29adc817095f285d5095fc84faa0afc81abdb0e2f9f`

## 摘要

产品页把 TeraPHY 描述为 UCIe optical I/O chiplet，标称 8Tbps 双向带宽、8 个全双工端口和每端口 16 个 WDM slices。页面明确说明公开规格为 preliminary、完整 roadmap 受 NDA 限制，因此这些数字不能视为最终商用规格。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| 页面标称 8Tbps 双向带宽、8 个全双工端口、每端口 16 个 WDM slices。 | company_statement | 2026-07-28 | 公司产品页 | medium | 正式数据表或后续页面更新。 |
| 每端口标称 512Gbps，即每方向合计 4Tbps。 | company_statement | 2026-07-28 | 公司规格表 | medium | 正式规格改变。 |
| 页面标称 NRZ、无 FEC、BER 小于 `1e-12`，距离覆盖毫米至公里。 | company_statement | 2026-07-28 | 公司产品页 | low | 独立或客户级测试不支持。 |
| 页面标称 chiplet 延迟约 10ns，不含光纤传播时间。 | company_statement | 2026-07-28 | 公司规格脚注 | medium | 同口径测试不支持。 |
| TeraPHY 采用 UCIe 接口定位 optical retimer chiplet。 | company_statement | 2026-07-28 | 公司产品架构说明 | high | 正式产品路线更改。 |
| 页面明确说明公开规格是 preliminary，完整 roadmap 需 NDA。 | verified_fact | 2026-07-28 | 产品页注释 | high | 公司发布正式替代规格。 |

## 实体

- [[ayar-labs|Ayar Labs]]

## 概念

- [[cpo-technology-routes-and-product-generations|CPO 技术路线与产品代际]]
- [[cpo-optical-engine-components-cost-and-margin|CPO 光引擎组成、成本与利润]]

## 事件

- [[cpo-switch-commercialization-roadmap-2025-2027|CPO 与光学 I/O 商业化路线图]]

## 提及的模型或假设

- 公开规格可用于架构上限和敏感性情景，不能直接作为量产出货、ASP 或良率假设。

## 证据缺口与冲突

- 缺少正式数据表、客户认证、量产状态、价格、产能与财务贡献。
- “毫米至公里”不是单一标准化链路条件，不能与交换机光模块距离直接横比。
- 产品页性能提升幅度均为公司陈述。
