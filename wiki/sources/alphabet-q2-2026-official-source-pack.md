---
page_type: source
subject: "Alphabet Q2 2026 官方披露资料包"
tags: [official-filing, earnings, cloud, ai-capex]
tickers: ["NASDAQ:GOOGL"]
ticker_aliases: ["NASDAQ:GOOG", GOOGL, GOOG]
markets: [US]
asset_classes: [equity]
industries: [internet, cloud-computing, data-center-infrastructure]
themes: [AI infrastructure, AI CAPEX, TPU]
as_of: 2026-06-30
sources:
  - "https://s206.q4cdn.com/479360582/files/doc_financials/2026/q2/2026q2-alphabet-earnings-release.pdf"
  - "https://s206.q4cdn.com/479360582/files/doc_events/2026/Jul/22/2026_Q2_Earnings_Transcript.pdf"
  - "https://www.sec.gov/Archives/edgar/data/1652044/000165204426000071/goog-20260630.htm"
created: 2026-07-28
updated: 2026-07-28
---

# Alphabet Q2 2026 官方披露资料包

## 来源元数据

- 出版机构：Alphabet Inc.、U.S. SEC
- 来源类型：业绩发布、官方电话会文字稿、Form 10-Q
- 发布日期：2026-07-22 至 2026-07-23
- 报告期间：截至 2026-06-30 的三个月及六个月
- 知识截止日：2026-07-23

| 原始文件 | SHA-256 | 证据层级 |
|---|---|---|
| `raw/2026-07-22-alphabet-q2-2026-earnings-release.pdf` | `65f35a2e9c287112121f736321c7526d603ba8e0dae27acac56c7d7357602aa8` | 公司正式业绩发布 |
| `raw/2026-07-22-alphabet-q2-2026-earnings-call-transcript.pdf` | `de938411f77818b147ff51d8ca2f70081f9a44401d396f1779ab5b5adfbd9123` | 公司管理层陈述 |
| `raw/2026-07-23-alphabet-q2-2026-form-10-q.html` | `fecfbc2683f630380b17937278ce3745eca150eb90e21a945fd6b78fe19728c7` | SEC 监管申报 |

## 摘要

Q2 收入 US$119.8bn，同比增长 24%；Google Cloud 收入 US$24.8bn，同比增长 82%，营业利润 US$8.8bn、利润率 35.6%，Cloud backlog 为 US$514bn。Q2 capex US$44.9bn，管理层将 2026 年 capex 指引上调至 US$195–205bn。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| Google Cloud Q2 收入 US$24.8bn、营业利润 US$8.8bn。 | verified_fact | 2026-06-30 | 业绩发布与 10-Q | high | SEC 更正申报 |
| Cloud backlog 为 US$514bn。 | company_statement | 2026-06-30 | 业绩发布 | medium | 取消、重谈或确认周期变化 |
| Q2 capex US$44.9bn，约 60% 为服务器、40% 为数据中心和网络。 | company_statement | 2026-06-30 | 电话会与 10-Q | medium-high | 资产分类重述 |
| 2026 年 capex 指引为 US$195–205bn。 | company_statement | 2026-07-22 | 电话会 | medium | 后续指引更新 |
| Q2 首次确认客户数据中心 TPU 系统收入。 | company_statement | 2026-06-30 | 电话会 | medium | 后续未持续确认或重分类 |

## 关联页面

- Entity：[[alphabet-inc|Alphabet Inc.]]
- Event：[[alphabet-q2-2026-results-2026-07-22|Alphabet Q2 2026 业绩、TPU 系统收入与 capex 上调]]
- Model：[[hyperscaler-capex-cash-return-comparison-2026|Hyperscaler 资本开支与现金回报比较（2026）]]
- Synthesis：[[ai-capex-capacity-and-cash-return-monitoring-2026|AI CAPEX、容量与现金回报监测（2026）]]

## 证据缺口与冲突

- Cloud 增长包含 TPU 系统销售；公司称剔除后仍加速，但未披露金额。
- Backlog 不是收入，有限协议中的大部分收入预计 2027 年确认。
- token、客户采用和 Fortune 100 渗透不是独立变现或 ROIC 证据。
- 约 US$98bn OI&E/约 US$99bn 权益投资收益显著抬高净利润与 EPS。
