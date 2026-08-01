---
page_type: source
subject: "Amazon Q1 2026 官方披露资料包"
tags: [official-filing, earnings, cloud, ai-capex]
tickers: ["NASDAQ:AMZN"]
markets: [US]
asset_classes: [equity]
industries: [cloud-computing, internet, data-center-infrastructure]
themes: [AI infrastructure, AI CAPEX, Trainium]
as_of: 2026-03-31
sources:
  - "https://s2.q4cdn.com/299287126/files/doc_earnings/2025/q4/earnings-result/AMZN-Q4-2025-Earnings-Release.pdf"
  - "https://s2.q4cdn.com/299287126/files/doc_earnings/2026/q1/earnings-result/AMZN-Q1-2026-Earnings-Release.pdf"
  - "https://s2.q4cdn.com/299287126/files/doc_earnings/2026/q1/presentation/Webslides_Q126.pdf"
  - "https://www.sec.gov/Archives/edgar/data/1018724/000101872426000014/amzn-20260331.htm"
created: 2026-07-28
updated: 2026-07-28
---

# Amazon Q1 2026 官方披露资料包

## 来源元数据

- 出版机构：Amazon.com, Inc.、U.S. SEC
- 来源类型：Q4 2025 全年 capex 基线、Q1 2026 业绩发布、webcast slides、Form 10-Q
- 发布日期：2026-02-05、2026-04-29 至 2026-04-30
- 报告期间：截至 2026-03-31 的三个月
- 知识截止日：2026-04-30

| 原始文件 | SHA-256 | 用途 |
|---|---|---|
| `raw/2026-02-05-amazon-q4-2025-earnings-release.pdf` | `ad8d84cbcc0a4ce35b803b93e8186c29ea0b06b4455d04fb584ab5ad29c42915` | 2026 年 capex 基线 |
| `raw/2026-04-29-amazon-q1-2026-earnings-release.pdf` | `abd500d48f7a87cd6a02b6a7dac6cc748ba310513d123d0e4d30b47dfc0aafe0` | Q1 正式业绩 |
| `raw/2026-04-29-amazon-q1-2026-webcast-slides.pdf` | `defb6de7df0a7c7c98dc894d194c7283c9a9991617135b9d0aa1643922fb4bdb` | 公司演示与 AI 芯片指标 |
| `raw/2026-04-30-amazon-q1-2026-form-10-q.html` | `bfc025c92bd7ed07daac4210020764854242103002ac7bb59ccb28bf058f04e3` | SEC 监管申报 |

## 摘要

Q1 净销售额 US$181.5bn，同比增长 17%；AWS 销售额 US$37.6bn，同比增长 28%，营业利润 US$14.2bn。过去十二个月经营现金流 US$148.5bn，自由现金流约 US$1.2bn；公司维持 2026 年全公司 capex 约 US$200bn 的基线。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| AWS Q1 销售额 US$37.6bn、营业利润 US$14.2bn。 | verified_fact | 2026-03-31 | Q1 发布与 10-Q | high | SEC 更正申报 |
| 2026 年全公司 capex 约 US$200bn。 | company_statement | 2026-02-05 | Q4 2025 发布 | medium | 后续指引更新 |
| 芯片业务收入 run rate 超过 US$20bn，保持三位数增长。 | company_statement | 2026-03-31 | webcast slides | medium | 定义或组合重述 |
| 过去十二个月 landed 超过 210 万颗 AI 芯片，超过一半为 Trainium。 | company_statement | 2026-03-31 | webcast slides | medium | 出货口径重述 |

## 关联页面

- Entity：[[amazon-com-inc|Amazon.com, Inc.]]
- Event：[[amazon-q1-2026-results-2026-04-29|Amazon Q1 2026 业绩、AWS 芯片与现金回报]]
- Model：[[hyperscaler-capex-cash-return-comparison-2026|Hyperscaler 资本开支与现金回报比较（2026）]]
- Synthesis：[[cloud-and-compute-supply-chain-comparison-2026|云厂商与算力供应链比较（2026）]]

## 证据缺口与冲突

- US$200bn 是 Amazon 全公司 capex，不是 AWS 或纯 AI capex。
- 芯片 run rate 包含 Graviton、Trainium 和 Nitro，不是 accelerator-only 收入。
- “landed”、宣布部署、客户承诺、正式订单、收入确认是不同阶段。
- 自由现金流为公司定义指标，未完整反映融资租赁和部分收购现金流。
- 公司未发布官方电话会逐字稿；本页未使用第三方 transcript。
