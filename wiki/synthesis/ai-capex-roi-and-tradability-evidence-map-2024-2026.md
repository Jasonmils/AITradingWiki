---
page_type: synthesis
subject: "AI CAPEX、ROI 与可交易性证据图谱（2024–2026）"
aliases:
  - "AI CAPEX, ROI and Tradability Evidence Map 2024–2026"
  - "AI 行业交易证据图谱"
tags:
  - synthesis
  - ai-capex
  - ai-roi
  - tradability
tickers:
  - "NASDAQ:MSFT"
  - "NASDAQ:GOOGL"
  - "NASDAQ:AMZN"
  - "NASDAQ:META"
  - "NYSE:ORCL"
  - "NASDAQ:NVDA"
  - "NASDAQ:AMD"
  - "TWSE:2330"
  - "NASDAQ:MU"
  - "NASDAQ:ASML"
  - "NASDAQ:AMAT"
markets:
  - Global
  - US
  - China
  - Hong Kong
  - Europe
  - Asia
analysis_regimes: [us_equity, cross_market, other]
policy_jurisdictions: [US, CN, TW, EU]
reporting_currencies: [USD, TWD, EUR]
asset_classes:
  - equity
  - rates
  - fx
  - commodity
industries:
  - semiconductors
  - software
  - internet
  - financial-services
  - data-center-infrastructure
themes:
  - AI CAPEX
  - AI productivity
  - AI ROI
  - AI trading
as_of: 2026-07-23
sources:
  - "[[microsoft-fy2026-q3-official-source-pack|Microsoft FY2026 Q3 官方披露资料包]]"
  - "[[alphabet-q2-2026-official-source-pack|Alphabet Q2 2026 官方披露资料包]]"
  - "[[amazon-q1-2026-official-source-pack|Amazon Q1 2026 官方披露资料包]]"
  - "[[meta-q1-2026-official-source-pack|Meta Q1 2026 官方披露资料包]]"
  - "[[oracle-q4-fy2026-official-source-pack|Oracle Q4/FY2026 官方披露资料包]]"
  - "[[nvidia-q1-fy2027-official-source-pack|NVIDIA Q1 FY2027 官方披露资料包]]"
  - "[[amd-q1-2026-official-source-pack|AMD Q1 2026 官方披露资料包]]"
  - "[[tsmc-q2-2026-official-source-pack|TSMC Q2 2026 官方披露资料包]]"
  - "[[micron-q3-fy2026-official-source-pack|Micron Q3 FY2026 官方披露资料包]]"
  - "[[asml-q2-2026-official-source-pack|ASML Q2 2026 官方披露资料包]]"
  - "[[applied-materials-q2-fy2026-official-source-pack|Applied Materials Q2 FY2026 官方披露资料包]]"
  - "[[citi-agentic-ai-finance-2025-01|Citi：Agentic AI 与金融业的“Do It For Me”经济]]"
  - "[[citi-productivity-ai-revolution-2025-09-10|Citi：生产率的 AI 革命]]"
  - "[[morgan-stanley-mapping-ai-rate-of-change-2026-02-11|Morgan Stanley：映射 AI 变化率]]"
  - "[[bofa-ai-ten-secret-ingredients-2026-06-16|BofA：AI 的十种秘密原料]]"
  - "[[hsbc-china-full-arc-ai-opportunity-2026-06-26|HSBC：中国分化经济中的全链条 AI 机会]]"
  - "[[jpmorgan-mid-year-investment-outlook-2026-06|J.P. Morgan Asset Management：2026 年中投资展望]]"
created: 2026-07-27
updated: 2026-07-28
status: provisional
confidence: medium
horizon: 6-12m
review_after: 2026-08-31
synthesis_type: industry_evidence_map
---

# AI CAPEX、ROI 与可交易性证据图谱（2024–2026）

## 结论先行

1. **行业值得继续研究**：六份机构研究与 11 家公司最新官方财报从资本开支、云变现、GPU/HBM/晶圆代工/设备和现金回报提供了相互补充的证据。
2. **当前最强证据仍在建设和上游收入端**：公司 capex 指引、云收入、GPU/HBM/foundry/设备收入已可见；纯 AI 增量利润、容量利用率和长期自由现金回报仍更弱。
3. **AI 收益首先偏向成本效率**：Morgan Stanley 调查认为约 80% 收益来自效率，Citi 也强调宏观生产率尚未确认结构性加速。
4. **CAPEX 与 ROI 之间存在长链条**：计划、订单、交付、投运、利用率、付费使用、收入、利润和现金流不能合并。
5. **当前价格是否值得交易尚未完成**：基本面证据已更新至 2026-07-23，但仍缺统一时点的当前价格、企业价值、盈利一致预期、拥挤度和风险预算。此页不能输出即时买卖结论。

## 官方财报层新增证据

### 云厂商

| 公司 | 最新增长/回报信号 | capex 或合同信号 | 主要风险 |
|---|---|---|---|
| Microsoft | Azure +40%；Q3 FCF 约 US$15.8bn | 2026 capex 约 US$190bn | OpenAI、租赁和 AI ARR 口径 |
| Alphabet | Cloud +82%、利润率 35.6%；Q2 FCF 为负 | 2026 capex US$195–205bn | TPU system mix、投资收益 |
| Amazon | AWS +28%、利润 US$14.2bn；TTM FCF 约 US$1.2bn | 2026 全公司 capex 约 US$200bn | AWS/非 AWS 拆分、租赁 |
| Meta | 收入 +33%、利润率 41%、FCF 正 | 2026 capex US$125–145bn | AI 广告增量未单列 |
| Oracle | OCI +77%；FY FCF 约 -US$23.7bn | RPO US$638bn；未入表租赁约 US$260bn | 长期确认、融资、稀释 |

Microsoft、Alphabet、Amazon、Meta 最新 2026 capex 指引机械合计为 US$710–740bn，证据类型为 `codex_inference`。它不是纯 AI capex，也不能与 US$697bn `market_consensus` 直接做“超预期”差额分析。

### 算力供应链

| 环节 | 官方结果 | 证据强度 | 正常化风险 |
|---|---|---|---|
| NVIDIA accelerator/networking | Data Center US$75.2bn | high | H20 基数、口径变化、出口 |
| AMD accelerator/CPU | Data Center US$5.8bn | high | CPU/GPU mix、6GW 尚非订单 |
| TSMC foundry | 先进节点占晶圆收入 77% | high | 非 AI 混合、海外厂、地缘 |
| Micron memory/HBM | Cloud Memory + Core DC US$25.293bn | high | 存储周期、长协执行 |
| ASML lithography | Q2 收入 €9.3bn | high | 订单—验收—收入时滞 |
| AMAT wafer equipment | Semi Systems US$5.965bn | high | 分部重述、投资收益、设备周期 |

## 因果链

`CAPEX 计划 → 正式订单 → 交付/建设 → 可用容量 → 利用率 → 付费使用 → 收入 → 毛利/利润 → 经营与自由现金流 → 估值与回报`

报告分别覆盖链条的不同位置：

| 环节 | 主要来源 | 当前证据强度 | 主要缺口 |
|---|---|---|---|
| CAPEX 计划 | J.P. Morgan、Citi | medium | 一致预期会变化 |
| 材料与设备约束 | BofA | low-medium | 公开版删节、份额需官方核验 |
| 订单与交付 | Oracle、Micron、ASML、AMD/NVIDIA 公司披露 | medium | RPO/订单/规划仍非收入 |
| 企业采用 | Citi Agentic、Morgan Stanley、J.P. Morgan | medium | 调查样本和定义差异 |
| 生产率 | Citi、Morgan Stanley | low-medium | 因果识别和宏观时滞 |
| 付费与收入 | J.P. Morgan | low | 客单价、用量、留存缺失 |
| 利润与现金流 | 11 家官方财报、Morgan Stanley、J.P. Morgan | medium | AI 归因、正常化与跨公司口径 |
| 当前估值与交易 | 本批来源不足 | incomplete | 需实时价格和最新披露 |

## 共识

| 判断 | 证据类型 | 证据 | 置信度 |
|---|---|---|---|
| AI 基础设施 CAPEX 仍在高位增长。 | market_consensus | 2026E 五家美国 hyperscaler CAPEX US$697bn | medium |
| 当前企业 AI 收益更多来自成本效率而非收入。 | source_opinion | Morgan Stanley 约 80% / 20% 划分 | medium |
| 规模化部署受数据、电力、组织、监管和供应链制约。 | source_opinion | Citi、BofA、J.P. Morgan | medium |
| 付费采用正在增加。 | source_opinion | Ramp 调查 >50%，一年前约 40% | low |
| 最终 ROI 仍未充分确认。 | source_opinion | Citi 宏观判断与 J.P. Morgan 现金回报边界 | high |
| 云厂商 capex 与现金回报正在分化。 | codex_inference | 五家云厂商最新官方财报 | high |
| 上游收入兑现强，但高利润率含周期、mix 和基数。 | codex_inference | NVIDIA、TSMC、Micron、ASML、AMAT | high |

## 非共识与待验证假设

| 判断 | 证据类型 | 为什么非共识 | 失效条件 |
|---|---|---|---|
| 采用者 2027 年利润率可能好于一致预期。 | non_consensus | Morgan Stanley 认为市场预期偏保守 | 采用者实际利润率不再领先 |
| AI 可在十年内提高 0.5–1.5ppt 年均生产率增速。 | model_assumption | 依赖任务和成本节省假设 | 规模化与宏观数据不支持 |
| CAPEX 接收方的盈利路径可能比支出方更顺畅。 | source_opinion | 收入确认更直接，但预期较高 | 订单、价格或毛利率下修 |
| 中国应以在岸硬件加离岸平台构建全链条暴露。 | source_opinion | 与单押硬件或平台的框架不同 | 相对盈利与估值不支持 |
| 材料成本虽低但可能成为系统瓶颈。 | source_opinion | 价值占比低、系统关键性高 | 替代、库存和扩产消除交期 |

## Codex 综合推论

以下不是来源原文：

- `codex_inference`：AI 产业链的盈利可见性目前呈“越靠近已确认 CAPEX 接收端越高、越靠近终端生产率越需要验证”的梯度。
- `codex_inference`：当 hyperscaler AI CAPEX 接近经营现金流时，自由现金流压力会使“收入增长”和“股东回报”出现分化。
- `codex_inference`：企业采用率上升若主要体现为低客单价订阅，而非用量、续费和单位经济性改善，可能高估软件层回报。
- `codex_inference`：关键材料的投资价值取决于公司级可销售产量、成本曲线和所有权，不应使用国家供应份额直接替代。
- `codex_inference`：Oracle 的 RPO、Micron 的客户承诺和 ASML 的订单覆盖提供不同期限的需求可见度，但资本化时必须按确认期、融资和取消风险折现。
- `codex_inference`：NVIDIA、Micron 和 TSMC 的当前报告利润率不能使用同一“AI 稀缺性”叙事解释；三者分别含产品/基数、存储价格周期和先进节点 mix。

## 研究优先级与可交易性

| 方向 | 研究优先级 | 当前证据 | 当前可交易性状态 |
|---|---|---|---|
| 半导体/网络/设备 | 高 | CAPEX 与盈利预期较强 | 未完成；需实时估值与订单验证 |
| 电力、材料与数据中心 | 高 | 约束逻辑成立，数据不完整 | 未完成；需官方份额和公司弹性 |
| 云、模型与软件 | 高 | 付费率提高，ROI 未完整 | 未完成；需用量、留存、毛利 |
| 企业采用者 | 中高 | 效率信号增加 | 未完成；需行业中性利润归因 |
| Agentic AI 金融应用 | 中 | 用例丰富、规模化有限 | 未完成；需生产部署和风险损失 |
| 中国全链条 AI | 高 | 市场与环节分化提供选择空间 | 未完成；需跨市场统一估值 |

“高研究优先级”只表示值得投入研究资源，不表示当前价格值得买入。

## 形成交易判断前的必需更新

- 当前股价、估值、盈利预期和拥挤度。
- 后续季度 CAPEX 指引、订单、交付、库存和客户集中度。
- hyperscaler 利用率、AI 收入、经营现金流和自由现金流。
- 软件/Agent 的付费使用、续费、价格、推理成本和毛利。
- 采用者的公司级节省、收入增量及其会计期间。
- 关键材料的官方供应份额、价格、库存、出口政策和公司成本曲线。
- 中国在岸/离岸公司的统一币种、会计期和风险溢价。

## 证据缺口

- 本次未取得可摄入的 Goldman Sachs 两份相关报告、UBS AI sizing/quarterly 报告和 CICC 两份报告的官方原始 PDF，因此不创建 Source 页，也不使用二手摘要填补。
- BofA 为删节版，HSBC 仅 3 页，Citi 生产率报告也是公开删节版。
- Morgan Stanley 的约 3,600 股票映射依赖分析师调查，没有逐公司一手证据包。
- J.P. Morgan 的 CAPEX 和 EPS 为时间敏感的一致预期。
- Amazon、Oracle、NVIDIA 未取得官方逐字稿；TSMC 官方 IR transcript 端点拒绝下载；Micron/AMAT 部分 IR 静态附件不可访问，未以第三方 transcript 填补。
- 各公司未统一披露纯 AI capex、容量利用率、AI 增量毛利和折旧资产组。

## 关联概念与模型

- [[agentic-ai-in-financial-services|金融服务中的 Agentic AI]]
- [[ai-productivity-diffusion-and-roi|AI 生产率扩散与 ROI]]
- [[ai-exposure-materiality-and-rate-of-change|AI 暴露、重要性与变化率]]
- [[ai-infrastructure-critical-material-bottlenecks|AI 基础设施关键材料瓶颈]]
- [[china-full-arc-ai-investment-chain|中国全链条 AI 投资链]]
- [[citi-us-ai-productivity-scenario-2025|Citi 美国 AI 生产率情景模型（2025）]]
- [[hyperscaler-ai-capex-roi-monitoring-model-2026|Hyperscaler AI CAPEX—ROI 监测模型（2026）]]
- [[hyperscaler-capex-cash-return-comparison-2026|Hyperscaler 资本开支与现金回报比较（2026）]]
- [[ai-compute-supply-capacity-revenue-bridge-2026-2028|AI 算力供给容量—收入桥（2026–2028）]]
- [[ai-supply-chain-normalized-margin-scenarios-2026-2028|AI 算力供应链正常化利润率情景（2026–2028）]]
- [[cloud-and-compute-supply-chain-comparison-2026|云厂商与算力供应链比较（2026）]]
- [[ai-capex-capacity-and-cash-return-monitoring-2026|AI CAPEX、容量与现金回报监测（2026）]]

## 变更记录

- 2026-07-28：加入 11 家云厂商与算力供应链公司的最新官方财报/申报/电话会材料，补齐公司级 capex、云收入、上游收入、利润率和现金回报；仍未形成当前价格交易结论。
- 2026-07-27：基于六份已保存的官方机构 PDF 建立跨报告证据图谱；未新增公司级即时交易结论。
