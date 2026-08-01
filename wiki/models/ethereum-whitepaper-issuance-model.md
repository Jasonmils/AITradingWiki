---
page_type: model
model_type: technology_trend
subject: "Ethereum 白皮书历史发行与供给均衡模型"
aliases:
  - "Ethereum whitepaper issuance model"
  - "以太坊白皮书发行模型"
tags:
  - ethereum
  - issuance-model
  - proof-of-work
  - supply-equilibrium
tickers: []
markets: []
asset_classes: []
industries:
  - distributed-systems
  - cryptography
themes:
  - historical-token-issuance
  - protocol-incentives
research_tracks:
  - technology
  - commercialization
as_of: 2014-12-31
sources:
  - "[[2014-ethereum-next-generation-smart-contract-platform|Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform]]"
  - "https://ethereum.org/developers/docs/consensus-mechanisms/pos/"
  - "https://ethereum.org/roadmap/merge/"
  - "https://eips.ethereum.org/EIPS/eip-1559"
created: 2026-08-01
updated: 2026-08-01
status: superseded
confidence: medium
horizon: 3-5y
technology_maturity: research
review_after: 2027-08-01
base_units: "X, share, percent"
---

# Ethereum 白皮书历史发行与供给均衡模型

## 问题、范围与系统边界

本模型复现 2014 Ethereum 白皮书“Currency and Issuance”及“Fees”相关部分的历史发行设计。令 `X` 为 currency sale（货币销售）中售出的 ether 总量，模型描述购买者、早期贡献者、长期研究基金和 PoW 矿工发行在 launch、1 年后与 5 年后的相对供给。

该模型仅回答“白皮书设计在自身公式下如何计算”。Ethereum 已于 2022-09-15 通过 The Merge 弃用 PoW，因此持续向矿工发行 `0.26X/year` 的方案已被后续协议演进取代。`status: superseded` 指当前适用性，而不是否定历史文本或算术复现。

## 机制与公式

白皮书定义：

- Currency sale：以 `1337-2000 ether per BTC` 的范围销售，总销售量记为 `X`；
- 早期贡献者分配：`0.099X`；
- 长期研究基金：`0.099X`；
- PoW 矿工永久线性发行：每年 `0.26X`。

因此，若 `t` 为 launch 后年数：

```text
Initial supply = X + 0.099X + 0.099X = 1.198X
Miner issuance(t) = 0.26Xt
Total supply(t) = 1.198X + 0.26Xt
Group share(t) = group amount(t) / Total supply(t)
```

若每年丢失或销毁的 ether 占总量固定为 `l`，白皮书的长期均衡近似为：

```text
0.26X = l × equilibrium supply
equilibrium supply = 0.26X / l
```

当 `l=1%` 时，均衡量为 `26X`。

## 已观察输入

| 输入 | 数值或状态 | 日期/期间 | 单位 | 证据类型 | 来源 | 置信度 |
|---|---:|---|---|---|---|---|
| Currency sale 兑换范围 | `1337-2000` | 2014 白皮书 | ether per BTC | verified_fact | 本地/官方 PDF | high |
| 购买者分配 | `X` | launch | X | verified_fact | 白皮书 Currency and Issuance | high |
| 早期贡献者分配 | `0.099X` | launch | X | verified_fact | 白皮书 Currency and Issuance | high |
| 长期研究基金 | `0.099X` | launch | X | verified_fact | 白皮书 Currency and Issuance | high |
| PoW 矿工发行 | `0.26X` | 每年 | X/year | model_assumption | 白皮书 Currency and Issuance | medium |
| 供给损失率示例 | `1%` | 每年 | percent/year | model_assumption | 白皮书 Currency and Issuance | low |
| PoW 当前适用状态 | 已于 2022-09-15 The Merge 后弃用 | 2022-09-15 | protocol state | verified_fact | Ethereum.org The Merge 与 PoS 文档 | high |
| 本地复算状态 | 表格与均衡公式一致 | 2026-08-01 | arithmetic check | codex_inference | 按白皮书公式复算 | high |

## Benchmark 归一化与复现状态

本次是 dimensionless（无量纲）比例与百分比算术复现，不是链上供给审计、客户端复现或经济均衡的实证检验。所有结果以 `X` 归一化，没有代入实际 sale 总量、BTC 价格、当前 ETH 供给、质押发行、burn 或市场价格。

官方当前 HTML 与官方 PDF 存在版本差异：PDF/本地文件为 `1337-2000 ether per BTC`，当前 HTML 为 `1000-2000 ether per BTC`。本模型忠实采用所摄入 PDF，不静默替换输入。

## 模型假设

| 假设 | 保守 | 基准 | 乐观 | 时间范围 | 单位 | 证据类型 | 来源 | 置信度 |
|---|---:|---:|---:|---|---|---|---|---|
| 购买者分配固定 | `X` | `X` | `X` | launch | X | model_assumption | 白皮书 | high |
| 两项基金分配固定 | `0.198X` | `0.198X` | `0.198X` | launch | X | model_assumption | 白皮书 | high |
| 矿工发行线性且永久 | `0.26X` | `0.26X` | `0.26X` | 每年 | X/year | model_assumption | 白皮书 | low |
| 供给损失率固定 | `0.5%` | `1.0%` | `2.0%` | 长期 | percent/year | model_assumption | 白皮书基准与 Codex 敏感性 | low |
| 不计其他 mint/burn | 是 | 是 | 是 | 全期 | boolean | model_assumption | 模型简化 | low |

## 复算结果：总供给与分配比例

| 时点 | 总供给 | 购买者 | 早期贡献者 | 长期研究基金 | 矿工累计发行 |
|---|---:|---:|---:|---:|---:|
| launch | `1.198X` | 83.4725% | 8.2638% | 8.2638% | 0.0000% |
| 1 年后 | `1.458X` | 68.5871% | 6.7901% | 6.7901% | 17.8326% |
| 5 年后 | `2.498X` | 40.0320% | 3.9632% | 3.9632% | 52.0416% |

各时点比例合计为 100%。四舍五入后的表格与白皮书列示的 83.5%/8.26%/8.26%/0%、68.6%/6.79%/6.79%/17.8%、40.0%/3.96%/3.96%/52.0% 一致。

## 供给均衡敏感性

在“每年损失量 = 固定损失率 × 总供给”和持续发行 `0.26X/year` 的模型内：

| 固定年损失率 `l` | 计算 | 均衡供给 |
|---:|---:|---:|
| 0.5% | `0.26X / 0.005` | `52X` |
| 1.0% | `0.26X / 0.01` | `26X` |
| 2.0% | `0.26X / 0.02` | `13X` |

这只是模型内部敏感性。固定比例损失、永久线性 PoW 发行和不计其他 burn/mint 均不是当前 Ethereum 的有效联合假设。

## 性能、成本、可靠性与规模化结果

不适用。该模型描述相对发行与供给，不测量吞吐、费用、网络安全、用户采用或商业收入。矿工获得协议发行不等于上市公司收入，ether 供给也不能直接转换为平台价值、资产价格或 FCF。

## 关键里程碑与失效条件

- 已完成：白皮书总供给、组别比例和 1% 损失率均衡值的本地复算。
- 版本失效：Ethereum 于 2022-09-15 The Merge 后从 PoW 转为 PoS，永久矿工发行假设不再描述当前协议。
- 费用边界：EIP-1559 引入 base fee burn 与 priority fee 等机制，白皮书的历史费用口径不能映射为当前费用模型。
- 当前研究若涉及实际供给，必须重新取得同一截止日的官方协议、发行、质押、burn 与链上数据，不能沿用本模型。

## 局限与变更记录

1. `confidence: medium` 表示历史文本与算术复现可靠，但外部有效性和当前适用性低；二者不能合并成高置信当前供给判断。
2. `technology_maturity: research` 描述白皮书模型的证据状态，不代表当前 Ethereum 技术成熟度。
3. `horizon: 3-5y` 是 Schema 的页面复核分类，不是发行预测期或交易持有期。
4. 本模型没有代入实际 sale 结果、历史 fork、PoS issuance、fee burn、遗失率观测、当前供给或价格。
5. 2026-08-01：首次建立；复算历史发行表和均衡敏感性，并因 The Merge 标记为 `superseded`。

## 关联页面

- [[2014-ethereum-next-generation-smart-contract-platform|Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform]]
- [[ethereum|Ethereum（以太坊）]]
- [[vitalik-buterin|Vitalik Buterin]]
- [[ethereum-account-state-evm-and-gas|Ethereum 账户状态、EVM 与 Gas]]
- [[2014-01-23-ethereum-goes-public|Ethereum 项目公开发布（2014-01-23）]]
