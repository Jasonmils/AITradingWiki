---
page_type: concept
subject: "CPO 商业化证据分层"
tags: [research-framework, cpo, evidence-quality]
tickers: ["NASDAQ:NVDA", "NASDAQ:AVGO", "NASDAQ:MRVL", "NYSE:COHR", "NASDAQ:LITE", "NYSE:FN", "SZSE:300394", "SZSE:300308", "SZSE:300757"]
markets: [US, CN]
asset_classes: [equity]
industries: [semiconductors, optical-components, data-center-networking]
themes: [AI infrastructure, co-packaged optics]
as_of: 2026-07-27
sources:
  - "[[nvidia-spectrum-x-photonics-production-2026-05-31|NVIDIA Spectrum-X Photonics 进入生产（2026-05-31）]]"
  - "[[broadcom-tomahawk-6-davisson-cpo-2025-10-08|Broadcom Tomahawk 6 Davisson 102.4T CPO（2025-10-08）]]"
  - "[[robotechnik-annual-report-2025|罗博特科 2025 年年度报告]]"
created: 2026-07-27
updated: 2026-07-27
---

# CPO 商业化证据分层

## 定义

CPO 商业化不是单点事件。研究时必须保留以下状态机：

> 技术展示 → 样品/送样 → 客户认证 → 正式订单 → 生产 → 交付 → 客户部署 → 已确认收入 → 利润 → 经营现金流

## 证据等级

| 阶段 | 可接受证据 | 不能自动推导 |
|---|---|---|
| 技术展示 | 公司公告、展会演示 | 客户采用、量产 |
| 送样 | 公司公告、客户确认 | 认证通过、订单 |
| 客户认证 | 客户或双方公告 | 正式订单 |
| 正式订单 | 合同、不可撤销订单披露 | 已交付、已确认收入 |
| 生产 | 公司称 `in production` 或 `volume production` | 客户验收、供应商收入 |
| 交付 | 公司/客户交付证据 | 最终部署、收入确认 |
| 已确认收入 | 财报或监管申报 | 可持续利润、现金回款 |
| 利润与现金流 | 分部利润、现金流勾稽 | 未来持续增长 |

## 当前案例

- NVIDIA：Spectrum-X Photonics 已由预计可用推进到 `in production`。
- Broadcom：Bailly/Davisson 由公司描述为 volume production/向客户出货。
- Coherent：存在演示和未具名客户多年订单陈述。
- 罗博特科：存在在手订单和 CPO 测试设备批量订单陈述。
- 天孚通信：1.6T 光引擎规模生产与 CPO 配套研发仍需分别验证。

这些状态不能互相替代。

## 模型用法

- 只有已确认收入可直接进入历史收入。
- 订单可作为 backlog 转化假设，但必须引入取消、延期、验收和收入确认概率。
- 生产或技术展示只能影响情景概率，不能直接记为收入。

## 失效条件

若公司后续披露取消、延期、未通过认证、订单转化差或收入未兑现，应下调相应阶段和模型概率，不得保留旧的“量产”叙事。
