---
page_type: source
subject: "NVIDIA Q1 FY2027 官方披露资料包"
tags: [official-filing, earnings, gpu, networking]
tickers: ["NASDAQ:NVDA"]
markets: [US]
asset_classes: [equity]
industries: [semiconductors, data-center-networking]
themes: [AI infrastructure, accelerators, AI networking]
as_of: 2026-04-26
sources:
  - "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000051/nvda-20260520.htm"
  - "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000051/q1fy27pr.htm"
  - "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000051/q1fy27cfocommentary.htm"
  - "https://s201.q4cdn.com/141608511/files/doc_financials/2027/Q127/NVDA-F1Q27-Quarterly-Presentation-FINAL.pdf"
  - "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000052/nvda-20260426.htm"
created: 2026-07-28
updated: 2026-07-28
---

# NVIDIA Q1 FY2027 官方披露资料包

## 来源元数据

- 出版机构：NVIDIA Corporation、U.S. SEC
- 来源类型：业绩发布、CFO commentary、季度演示、Form 8-K、Form 10-Q
- 发布日期：2026-05-20
- 报告期间：截至 2026-04-26 的季度
- 知识截止日：2026-05-20

| 原始文件 | SHA-256 |
|---|---|
| `raw/2026-05-20-nvidia-q1-fy2027-earnings-release.html` | `736c5d15dc63b5110455150e76a796a912a44ae0c0c03928b4326299a84bb618` |
| `raw/2026-05-20-nvidia-q1-fy2027-cfo-commentary.html` | `08d93b6aa1c22dfdfb8ad2ad1f95dff0608ae5adb98b7a686e4b07a1b88a0276` |
| `raw/2026-05-20-nvidia-q1-fy2027-quarterly-presentation.pdf` | `1a5e03959643eebe566a996a68e71e66d527bde8029e18cc8dcfc00c9be047e3` |
| `raw/2026-05-20-nvidia-q1-fy2027-form-8-k.html` | `cbaae792d95be96e6237553b43980eb1486394304068756b5e1a5585886aaea0` |
| `raw/2026-05-20-nvidia-q1-fy2027-form-10-q.html` | `1b5de37b973da4a3f1cd31a09aa455c01c519ea7cc409c73de2250ad156f99e4` |

## 摘要

Q1 FY2027 收入 US$81.615bn，同比增长 85%；Data Center 收入 US$75.2bn，其中旧框架下 compute US$60.4bn、networking US$14.8bn。GAAP 毛利率 74.9%；Q2 收入指引 US$91bn ±2%，未假设中国数据中心计算收入。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| Q1 收入 US$81.615bn，Data Center US$75.2bn。 | verified_fact | 2026-04-26 | 发布与 10-Q | high | SEC 更正申报 |
| Q2 收入指引 US$91bn ±2%，不含中国数据中心计算收入。 | company_statement | 2026-05-20 | 发布 | medium | 后续指引更新 |
| Vera Rubin 按计划于 Q3/下半年推进。 | company_statement | 2026-05-20 | 演示材料 | medium | 路线图延期 |
| 新报告框架将 Data Center 拆分为 Hyperscale 与 ACIE 等类别。 | verified_fact | 2026-05-20 | CFO commentary | high | 公司再次重述 |

## 关联页面

- Entity：[[nvidia|NVIDIA Corporation（英伟达）]]
- Event：[[nvidia-q1-fy2027-results-2026-05-20|NVIDIA Q1 FY2027 业绩与披露口径变更]]
- Model：[[ai-supply-chain-normalized-margin-scenarios-2026-2028|AI 算力供应链正常化利润率情景（2026–2028）]]
- Synthesis：[[cloud-and-compute-supply-chain-comparison-2026|云厂商与算力供应链比较（2026）]]

## 证据缺口与冲突

- Data Center 同时包含计算与网络，不是纯 GPU 收入。
- GAAP 毛利率同比改善很大程度来自上年 H20 相关 US$4.5bn 费用不再重复。
- FY2027 起 non-GAAP 不再剔除 SBC；历史虽重述，仍须标记口径变化。
- 路线图、adoption、production、客户部署和确认收入必须保持分层。
- 公司未提供官方电话会逐字稿；CFO commentary 不能覆盖完整问答。
