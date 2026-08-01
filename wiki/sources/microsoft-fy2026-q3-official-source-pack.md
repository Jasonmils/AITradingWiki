---
page_type: source
subject: "Microsoft FY2026 Q3 官方披露资料包"
tags: [official-filing, earnings, cloud, ai-capex]
tickers: ["NASDAQ:MSFT"]
markets: [US]
asset_classes: [equity]
industries: [cloud-computing, software, data-center-infrastructure]
themes: [AI infrastructure, AI CAPEX, AI ROI]
as_of: 2026-03-31
sources:
  - "https://www.microsoft.com/en-us/investor/earnings/FY-2026-Q3/press-release-webcast"
  - "https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q3"
  - "https://www.sec.gov/Archives/edgar/data/789019/000119312526191507/msft-20260331.htm"
created: 2026-07-28
updated: 2026-07-28
---

# Microsoft FY2026 Q3 官方披露资料包

## 来源元数据

- 出版机构：Microsoft Corporation、U.S. SEC
- 来源类型：业绩发布、官方电话会文字稿、Form 10-Q
- 发布日期：2026-04-29
- 报告期间：截至 2026-03-31 的三个月及九个月
- 知识截止日：2026-04-29
- 本地源文件状态：`raw/` 永久保留；SHA-256 已复核

| 原始文件 | SHA-256 | 证据层级 |
|---|---|---|
| `raw/2026-04-29-microsoft-fy2026-q3-earnings-release.html` | `703aede98305b45ccf530856660a982cdb3febcde94d55067c550e2c7cc4621c` | 公司正式业绩发布 |
| `raw/2026-04-29-microsoft-fy2026-q3-earnings-call-transcript.html` | `6d08d88ca2fd80943ef48505e2fca6b3ffd4fa4bb257d961953aced5fa83ea9a` | 公司管理层陈述 |
| `raw/2026-04-29-microsoft-fy2026-q3-form-10-q.html` | `76945a2c148afb8521cff13adcd320e99a8c09bcb1a2541b5d0ed5a2b02adf2d` | SEC 监管申报 |

## 摘要

Microsoft FY2026 Q3 收入 US$82.9bn，同比增长 18%；Microsoft Cloud 收入 US$54.5bn，同比增长 29%，Azure 增长 40%。公司披露 AI 业务 ARR 超过 US$37bn、增长 123%，季度资本开支 US$31.9bn，另有 US$4.7bn 融资租赁；管理层预计 2026 自然年资本开支约 US$190bn。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| FY2026 Q3 收入 US$82.9bn，Azure 增长 40%。 | verified_fact | 2026-03-31 | 业绩发布与 10-Q | high | SEC 更正申报 |
| AI 业务 ARR 超过 US$37bn、同比增长 123%。 | company_statement | 2026-03-31 | 业绩发布 | medium | 公司重述定义或构成 |
| Q3 capex US$31.9bn，约三分之二用于寿命较短的 GPU/CPU。 | company_statement | 2026-03-31 | 电话会 | medium | 后续申报重分类 |
| 2026 自然年 capex 约 US$190bn，容量约束至少延续至年末。 | company_statement | 2026-04-29 | 电话会 | medium | 指引下调或项目延期 |

## 关联页面

- Entity：[[microsoft-corporation|Microsoft Corporation]]
- Event：[[microsoft-fy2026-q3-results-2026-04-29|Microsoft FY2026 Q3 业绩与资本开支更新]]
- Model：[[hyperscaler-ai-capex-roi-monitoring-model-2026|Hyperscaler AI CAPEX—ROI 监测模型（2026）]]
- Synthesis：[[cloud-and-compute-supply-chain-comparison-2026|云厂商与算力供应链比较（2026）]]

## 证据缺口与冲突

- AI ARR 是公司定义指标，未完整披露产品构成、收入确认和增量利润。
- RPO US$627bn 包含 OpenAI；总口径与剔除 OpenAI 后的增长不能混用。
- 现金购买、融资租赁、短寿命与长寿命资产须分层，不能与其他云厂商 capex 直接比较。
- 调整后结果剔除 OpenAI 投资影响；估值时须与 GAAP 口径勾稽。
