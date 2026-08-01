---
page_type: source
subject: "Ayar Labs TeraPHY 三代工程验证"
tags: [company-blog, optical-io, product-validation]
tickers: []
markets: [US]
asset_classes: [private-company]
industries: [semiconductors, optical-components, data-center-networking]
themes: [AI infrastructure, co-packaged optics, optical-io]
as_of: 2025-08-28
sources:
  - "raw/2025-08-28-ayar-labs-teraphy-three-generations-validation.html"
created: 2026-07-28
updated: 2026-07-28
---

# Ayar Labs TeraPHY 三代工程验证（2025-08-28）

## 来源元数据

- 来源类型：公司工程博客
- 发布机构：Ayar Labs
- 发布日期与知识截止日：2025-08-28
- 原始文件：`raw/2025-08-28-ayar-labs-teraphy-three-generations-validation.html`
- 本地源文件状态：不可变原始 HTML；SHA-256 `8aa795c96e4594540021b94408050b34edc51f35e1ac68ad479a75ad5dfde0be`

## 摘要

Ayar Labs 以 2T、4T、8T 三代 TeraPHY chiplet 说明从多芯片封装演示、wafer sort 与 bring-up，到 EVT/DVT 和系统集成的验证路径。来源的主要价值是揭示光电联合测试、热验证、误码率和 known-good-die 对量产良率的重要性；它不是量产或财务披露。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| 2T 代主要用于多芯片封装集成与技术演示。 | company_statement | 2025-08-28 | 公司三代路线回顾 | medium | 公司更正代际定义。 |
| 4T 代经历 wafer sort、bring-up、EVT/DVT、多芯片封装和系统集成。 | company_statement | 2025-08-28 | 公司工程流程说明 | high | 后续文件修订状态。 |
| 8T 代进一步采用电光 wafer sort 与 EVT，并描述 16 波长 microring、UCIe optical retimer。 | company_statement | 2025-08-28 | 公司产品验证说明 | high | 正式产品规格不同。 |
| 公司描述 30–80°C 热测试、BER 和 link-margin 验证。 | company_statement | 2025-08-28 | 公司测试说明 | medium | 独立测试无法复现。 |
| 公司称已完成 EVT，正在收尾 DVT。 | company_statement | 2025-08-28 | 博客发布时状态 | medium | 后续状态更新或审计不支持。 |
| EVT/DVT 完成不等于客户认证、量产、交付、收入或利润。 | verified_fact | 2025-08-28 | 来源未披露后续商业里程碑 | high | 后续一手披露补充。 |

## 实体

- [[ayar-labs|Ayar Labs]]

## 概念

- [[cpo-technology-routes-and-product-generations|CPO 技术路线与产品代际]]
- [[cpo-optical-engine-components-cost-and-margin|CPO 光引擎组成、成本与利润]]
- [[cpo-reliability-and-external-laser-source|CPO 可靠性与外置激光源]]

## 事件

- [[cpo-switch-commercialization-roadmap-2025-2027|CPO 与光学 I/O 商业化路线图]]

## 提及的模型或假设

- wafer sort、known-good-die、EVT/DVT 和系统测试应作为 composite yield、测试成本与爬坡速度的模型变量。
- 来源未提供可直接代入估值的良率百分比或单位成本。

## 证据缺口与冲突

- 测试流程和结果均来自公司自述，缺少客户或第三方独立验证。
- 公开材料没有客户、订单、产能、ASP、毛利和现金流。
- 代际带宽与完整商用产品的功耗、封装和服务边界仍需正式数据表确认。
