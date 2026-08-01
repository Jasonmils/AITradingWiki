---
page_type: synthesis
synthesis_type: monitoring
subject: "AI CAPEX、容量与现金回报监测（2026）"
tags: [monitoring, ai-capex, capacity, cash-flow]
tickers: ["NASDAQ:MSFT", "NASDAQ:GOOGL", "NASDAQ:AMZN", "NASDAQ:META", "NYSE:ORCL", "NASDAQ:NVDA", "NASDAQ:AMD", "TWSE:2330", "NASDAQ:MU", "NASDAQ:ASML", "NASDAQ:AMAT"]
markets: [US, TW, NL, Global]
analysis_regimes: [us_equity, cross_market, other]
policy_jurisdictions: [US, TW, EU, CN]
reporting_currencies: [USD, TWD, EUR]
asset_classes: [equity]
industries: [cloud-computing, semiconductors, memory, foundry, semiconductor-equipment]
themes: [AI CAPEX, AI ROI, AI infrastructure]
as_of: 2026-07-23
sources:
  - "[[cloud-and-compute-supply-chain-comparison-2026|云厂商与算力供应链比较（2026）]]"
  - "[[hyperscaler-capex-cash-return-comparison-2026|Hyperscaler 资本开支与现金回报比较（2026）]]"
  - "[[ai-compute-supply-capacity-revenue-bridge-2026-2028|AI 算力供给容量—收入桥（2026–2028）]]"
created: 2026-07-28
updated: 2026-07-28
status: active
confidence: medium
horizon: 12-24m
review_after: 2026-10-31
---

# AI CAPEX、容量与现金回报监测（2026）

## 当前研究引用

- [[ai-capex-roi-and-tradability-evidence-map-2024-2026|AI CAPEX、ROI 与可交易性证据图谱（2024–2026）]]
- [[cloud-and-compute-supply-chain-comparison-2026|云厂商与算力供应链比较（2026）]]
- [[hyperscaler-capex-cash-return-comparison-2026|Hyperscaler 资本开支与现金回报比较（2026）]]
- [[ai-supply-chain-normalized-margin-scenarios-2026-2028|AI 算力供应链正常化利润率情景（2026–2028）]]

## 跟踪面板

| 对象 | 当前状态 | 下次需核验 | 频率 | 下次检查 | 触发条件 |
|---|---|---|---|---|---|
| Microsoft | Azure +40%；2026 capex 约 US$190bn | AI ARR、Cloud GM、cash capex/租赁、FCF | 每季 | 2026-10-31 | capex/FCF 明显变化 |
| Alphabet | Cloud +82%；capex US$195–205bn | TPU system mix、Cloud margin、FCF | 每季 | 2026-10-31 | Cloud 增速或 FCF 拐点 |
| Amazon | AWS +28%；TTM FCF 约 US$1.2bn | AWS/非 AWS capex、Trainium、租赁 | 每季 | 2026-10-31 | FCF 转负或 AWS 放缓 |
| Meta | 广告现金流强；capex US$125–145bn | AI 广告增量、折旧、FCF | 每季 | 2026-10-31 | 利润率或 capex 变化 |
| Oracle | RPO US$638bn；FCF 负 | 融资、租赁开始、RPO 收入确认 | 每季 | 2026-09-30 | 债务/股权融资落地 |
| NVIDIA | Data Center US$75.2bn | 新框架、Rubin、毛利、出口 | 每季 | 2026-08-31 | 指引/毛利/中国变化 |
| AMD | MI450 sampling；Meta 最高 6GW | 正式订单、交付、采购承诺 | 每季 | 2026-08-31 | 1GW 出货/收入 |
| TSMC | 先进节点 77%；2nm 3% | 2nm ramp、封装、海外厂毛利 | 每季 | 2026-10-31 | 2nm/GM/capex 变化 |
| Micron | 毛利率 84.6%；HBM4 HVM | ASP、HBM4E、长协、库存 | 每季 | 2026-09-30 | ASP/毛利率拐点 |
| ASML | Q2 €9.3bn；2027 订单覆盖 | EUV 出货/验收、订单、中国 | 每季 | 2026-10-31 | 订单取消或许可变化 |
| AMAT | Semi Systems US$5.965bn | 重述分部、订单、OCF/FCF | 每季 | 2026-08-31 | 设备展望或现金流变化 |

## 领先指标与滞后指标

| 层级 | 指标 | 证据阶段 |
|---|---|---|
| 领先 | capex 指引、GW 计划、订单/RPO/backlog、采购承诺 | company_statement / verified_fact |
| 中间 | 设备出货/验收、wafer starts、HBM shipment、数据中心投运 | verified_fact 或 company_statement |
| 滞后 | 云付费用量、分部收入/利润、折旧、OCF、FCF | verified_fact |

## 即将出现的催化剂

| 催化剂 | 预计日期 | 概率 | 证据 | 投资影响 |
|---|---|---|---|---|
| NVIDIA/AMD/AMAT 后续季度结果 | 2026-08-31 前后 | high | 常规财报周期 | accelerator、设备和毛利验证 |
| Oracle/Micron 后续季度结果 | 2026-09-30 前后 | high | 常规财报周期 | RPO/长协与现金回报 |
| 云厂商、TSMC、ASML 后续季度结果 | 2026-10-31 前后 | high | 常规财报周期 | capex、Cloud、foundry、EUV |
| AMD MI450 首批 1GW 出货目标 | 2026-H2 | medium | company_statement | AMD/TSMC/HBM 收入桥 |
| ASML 2027 Low-NA 扩产/订单确认 | 2026-H2 | medium | company_statement | WFE 需求持续性 |

## 风险与预警信号

- capex 指引继续上升但 Cloud/AWS/OCI 增速和 FCF 同时下降。
- RPO/backlog 增长而未来 12 个月确认比例下降。
- 上游库存、应收、采购承诺和 capex 快于收入。
- memory ASP、设备订单或 accelerator 毛利率拐头。
- 订单/规划只停留在 sampling、announcement 或 capacity reservation。
- 出口控制、地缘或电力限制推迟交付和投运。

## 论点失效触发条件

- 云厂商连续两个季度下调 capex，且供应商订单/收入同步转弱。
- 新增容量无法带来可观察的付费使用、云利润和 FCF。
- 供应链高利润率被证明主要来自一次性价格/基数且快速回落。
- 长期 RPO、GW 合作或订单覆盖大幅取消、延后或重谈。

## 当前可交易性边界

每次形成证券交易判断前，必须同日核验：

- 收盘价、市值、EV、完全稀释股数、净现金/净债务；
- 当前一致预期、期权隐含波动和拥挤度；
- 最新业绩、指引、订单/交付、出口与监管状态；
- 风险预算、催化剂窗口与止损/失效条件。

本监测页目前不输出证券权重或买卖结论。

## 上次复核后的新增证据

- 2026-07-28：首次纳入 11 家公司最新官方财报、申报和电话会资料包。

## 下次复核

最迟 2026-10-31；若任一公司提前发布业绩、指引、重大订单、融资或监管变化，立即复核。
