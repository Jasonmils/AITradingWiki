---
page_type: model
model_type: technology_trend
subject: "Bitcoin 攻击者追赶概率模型"
aliases:
  - "Bitcoin attacker catch-up probability"
  - "比特币攻击者追赶概率"
tags:
  - bitcoin
  - proof-of-work
  - probability-model
  - security-model
tickers: []
markets: []
asset_classes: []
industries:
  - distributed-systems
  - cryptography
themes:
  - proof-of-work-security
  - confirmation-risk
research_tracks:
  - technology
as_of: 2008-10-31
sources:
  - "[[2008-10-31-bitcoin-peer-to-peer-electronic-cash-system|Bitcoin: A Peer-to-Peer Electronic Cash System]]"
created: 2026-08-01
updated: 2026-08-01
status: provisional
confidence: medium
horizon: 3-5y
technology_maturity: research
review_after: 2027-08-01
base_units: "probability"
---

# Bitcoin 攻击者追赶概率模型

## 问题、范围与系统边界

该模型复现白皮书第 11 节的问题：当诚实链已领先 `z` 个区块、攻击者拥有总区块生成能力占比 `q` 时，攻击者最终追上诚实链的概率是多少？

模型只描述这一随机追赶问题。它不覆盖网络延迟、节点隔离、实现漏洞、密钥盗窃、池化、策略性挖矿、审查、费用市场、交易对手行为或现实攻击收益，因此不能把结果解释为交易的普遍最终性保证。

## 机制与公式

设：

- `p`：诚实节点找到下一区块的概率；
- `q`：攻击者找到下一区块的概率，且 `p + q = 1`；
- `z`：诚实链领先的区块数；
- `λ = z(q/p)`：诚实链产生 `z` 个区块期间，攻击者产生区块数的 Poisson 参数。

若攻击者已落后 `z` 个区块，其最终追上的概率为：

```text
q_z = 1                  if p <= q
q_z = (q / p)^z          if p > q
```

把收款方等待期间攻击者已经挖出的区块数 `k` 纳入后，论文给出：

```text
P = 1 - Σ[k=0..z] Poisson(k; λ) × (1 - (q/p)^(z-k))
λ = z(q/p)
Poisson(k; λ) = exp(-λ) × λ^k / k!
```

## 已观察输入

| 输入 | 数值或状态 | 日期/期间 | 单位 | 证据类型 | 来源 | 置信度 |
|---|---:|---|---|---|---|---|
| 攻击者占比示例 | `q=0.1`、`q=0.3` | 2008-10-31 | share | verified_fact | 白皮书第 11 节表格 | high |
| 风险阈值示例 | `P<0.001` | 2008-10-31 | probability | verified_fact | 白皮书第 11 节表格 | high |
| 本地复算状态 | 表内全部列示值一致 | 2026-08-01 | arithmetic check | codex_inference | 按论文公式与 C 代码复算 | high |

## Benchmark 归一化与复现状态

这是公式算术复现，不是协议、节点软件或网络攻击的独立复现。输入与论文保持一致，没有用当前网络算力、区块间隔、传播延迟或经济参数替换。复算确认公式与论文表格内部一致，但不能验证假设是否覆盖现实。

## 模型假设

| 假设 | 基准表述 | 时间范围 | 单位 | 证据类型 | 来源 | 置信度 |
|---|---|---|---|---|---|---|
| 区块生成份额固定 | `p` 与 `q` 在追赶过程中保持不变 | 攻击期间 | share | model_assumption | 白皮书第 11 节 | medium |
| 区块到达独立 | 诚实与攻击者区块到达可用独立随机过程近似 | 攻击期间 | process | model_assumption | 白皮书第 11 节 | medium |
| Poisson 近似 | 诚实链生成 `z` 个区块时攻击者区块数服从 `λ=z(q/p)` 的 Poisson 分布 | 等待 `z` 个区块 | blocks | model_assumption | 白皮书第 11 节 | medium |
| 攻击目标简化 | 攻击者目标为从 `z` 区块差距追上诚实链 | 攻击期间 | blocks | model_assumption | 白皮书第 11 节 | medium |

## 复算结果：`q=0.1`

| `z` | 追赶概率 `P` |
|---:|---:|
| 0 | 1.0000000 |
| 1 | 0.2045873 |
| 2 | 0.0509779 |
| 3 | 0.0131722 |
| 4 | 0.0034552 |
| 5 | 0.0009137 |
| 6 | 0.0002428 |
| 7 | 0.0000647 |
| 8 | 0.0000173 |
| 9 | 0.0000046 |
| 10 | 0.0000012 |

## 复算结果：`q=0.3`

| `z` | 追赶概率 `P` |
|---:|---:|
| 0 | 1.0000000 |
| 5 | 0.1773523 |
| 10 | 0.0416605 |
| 15 | 0.0101008 |
| 20 | 0.0024804 |
| 25 | 0.0006132 |
| 30 | 0.0001522 |
| 35 | 0.0000379 |
| 40 | 0.0000095 |
| 45 | 0.0000024 |
| 50 | 0.0000006 |

## 敏感性：使 `P<0.001` 的最小 `z`

| 攻击者占比 `q` | 最小 `z` |
|---:|---:|
| 0.10 | 5 |
| 0.15 | 8 |
| 0.20 | 11 |
| 0.25 | 15 |
| 0.30 | 24 |
| 0.35 | 41 |
| 0.40 | 89 |
| 0.45 | 340 |

复算结果显示，在模型内部，`q` 越接近 0.5，达到同一概率阈值所需的 `z` 非线性增加；若 `q>=p`，模型给出的最终追赶概率为 1。该结果是模型条件下的数学性质，不是固定确认数的现实保证。

## 关键里程碑与失效条件

- 已完成：论文公式、两个概率表与阈值表的本地数值复算。
- 尚未完成：使用真实网络数据估计动态 `q`、区块到达相关性和传播条件。
- 尚未完成：对网络级攻击、软件实现、经济激励和交易价值进行联合建模。
- 失效条件：若研究问题包含论文未建模的攻击面，或 `p/q` 非固定、到达过程显著偏离独立 Poisson 假设，则本模型不能单独支持安全结论。

## 局限与变更记录

1. `confidence: medium` 表示公式复算可靠，但现实外部有效性有限；两者不能合并成高置信安全判断。
2. `technology_maturity: research` 只描述本模型在该来源中的证据状态，不代表 Bitcoin 当前网络成熟度。
3. `horizon: 3-5y` 是 Schema 要求的模型复核分类，不是交易持有期，也不是确认等待时间。
4. 模型未纳入网络延迟、eclipse attack、selfish mining、算力池行为、费用市场、外部攻击收益或经济最终性。
5. 2026-08-01：首次建立；按论文公式与附录 C 代码完成表格复算。

## 关联页面

- [[2008-10-31-bitcoin-peer-to-peer-electronic-cash-system|Bitcoin: A Peer-to-Peer Electronic Cash System]]
- [[bitcoin|Bitcoin（比特币）]]
- [[bitcoin-proof-of-work-consensus|Bitcoin 的 Proof-of-Work 共识与激励]]
- [[bitcoin-transaction-spv-and-privacy|Bitcoin 交易、SPV 与隐私边界]]
- [[2008-10-31-bitcoin-whitepaper-released|Bitcoin 白皮书公开发布（2008-10-31）]]
