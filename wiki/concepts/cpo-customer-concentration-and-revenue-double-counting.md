---
page_type: concept
subject: "CPO 客户集中度与产业链重复计量"
tags: [risk-framework, customer-concentration, cpo]
tickers: ["NYSE:FN", "SZSE:300394", "SZSE:300308", "NYSE:COHR", "NASDAQ:LITE"]
markets: [US, CN]
asset_classes: [equity]
industries: [optical-components, electronics-manufacturing]
themes: [AI infrastructure, co-packaged optics]
as_of: 2026-07-27
sources:
  - "[[fabrinet-form-10-k-fy2025|Fabrinet FY2025 Form 10-K]]"
  - "[[tfc-communication-annual-report-2025|天孚通信 2025 年年度报告]]"
  - "[[innolight-annual-report-2025|中际旭创 2025 年年度报告]]"
created: 2026-07-27
updated: 2026-07-27
---

# CPO 客户集中度与产业链重复计量

## 问题

同一终端 CPO/AI 网络需求可能依次形成器件供应商、合同制造商和平台公司的收入。把这些公司收入直接相加会把同一价值链多次计量。

## 已确认案例

- 天孚通信 2025 年对 Fabrinet 销售占收入 63.31%。
- Fabrinet 的 NVIDIA 与 Cisco 收入占比约 27.6% 和 18.2%。
- 中际旭创前五大客户占收入 75.98%。
- Lumentum Q3 FY2026 两个客户占 26% 和 12%。

## 模型规则

1. 行业 TAM 使用终端系统的最终价值量，只计算一次。
2. 公司收入使用各自交易层的销售额，可以同时存在，但不能再相加称为终端 TAM。
3. 供应链份额要按“直接客户份额 × 终端项目份额 × 产品内容”拆解。
4. 客户预付款、产能预订、采购承诺和已确认收入分别记录。
5. 对单一客户的价格让步、降价和库存调整需要加入敏感性。

## 估值折价因素

- 单一客户超过 25%。
- 前五大客户超过 75%。
- 直接客户本身依赖单一终端平台。
- 产品规格改变可导致库存、返工和价格压力。
- 高客户集中可能提高短期增长确定性，也可能降低长期议价能力。
