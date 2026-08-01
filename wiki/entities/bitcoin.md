---
page_type: entity
entity_type: project
subject: "Bitcoin（比特币）"
aliases:
  - "Bitcoin"
  - "比特币"
tags:
  - bitcoin
  - peer-to-peer
  - electronic-cash
  - proof-of-work
tickers: []
markets: []
asset_classes: []
industries:
  - distributed-systems
  - cryptography
themes:
  - peer-to-peer-electronic-cash
  - proof-of-work-consensus
research_tracks:
  - technology
  - commercialization
as_of: 2008-10-31
sources:
  - "[[2008-10-31-bitcoin-peer-to-peer-electronic-cash-system|Bitcoin: A Peer-to-Peer Electronic Cash System]]"
created: 2026-08-01
updated: 2026-08-01
---

# Bitcoin（比特币）

## 身份与范围

Bitcoin 是[[2008-10-31-bitcoin-peer-to-peer-electronic-cash-system|同名白皮书]]提出的点对点电子现金项目。本页只建立 2008-10-31 白皮书所支持的技术对象，不把之后的协议版本、软件实现、网络状态、市场资产、监管属性或采用情况倒填到历史来源中。

- 实体类型：`project`
- 文档中的名称：Bitcoin
- 作者署名：[[satoshi-nakamoto|Satoshi Nakamoto（中本聪）]]
- 文档中的网站：`www.bitcoin.org`
- 技术基线：无可信第三方的点对点电子现金；数字签名链、时间戳、Proof-of-Work、累计工作量链选择、节点激励、Merkle Tree 与 SPV。
- 证券或市场标识：本来源没有提供，故不填 ticker、listing regime 或交易市场。

## 白皮书所定义的问题

互联网支付通常依赖金融机构充当可信第三方。论文希望使任意两方能够直接交易，同时避免可复制数字信息被重复支付，并减少因可逆交易和中介争议处理产生的成本。

## 白皮书所定义的机制

1. 以数字签名链表达所有权转移；
2. 向点对点网络广播交易和区块；
3. 用 hash-linked Proof-of-Work 建立公开、难以改写的交易顺序；
4. 节点接受累计 Proof-of-Work 最大的有效链；
5. 以新币与交易费激励节点贡献资源；
6. 使用 Merkle Tree、区块头和 SPV 降低部分参与者的存储与验证负担。

## 技术与商业状态边界

| 里程碑 | 本来源能否证明 | 说明 |
|---|---|---|
| research publication | 是 | 2008-10-31 的原始邮件列表发布记录与 9 页论文。 |
| independent reproduction | 否 | 本地只复算概率表，不是完整系统独立复现。 |
| prototype / implementation | 否 | 论文未附实现代码或运行证据。 |
| pilot / production deployment | 否 | 论文没有部署证据。 |
| scaled adoption | 否 | 论文没有用户、交易量或网络规模证据。 |
| paid use / revenue / profit / FCF | 否 | 论文的手续费激励设计不等于商业收入、利润或现金流证据。 |

因此，若只按该来源分类，技术成熟度上限为 `research`，商业化阶段为 `none`。该分类只描述白皮书证据边界，不代表 Bitcoin 的当前状态。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| Bitcoin 在白皮书中被定义为无需可信第三方的点对点电子现金系统。 | verified_fact | 2008-10-31 | [[2008-10-31-bitcoin-peer-to-peer-electronic-cash-system|白皮书]] Abstract 与第 1 节 | high | 原文被证明误读。 |
| 系统安全论证依赖诚实节点控制多数 CPU power，并使最长链增长快于竞争链。 | model_assumption | 2008-10-31 | 白皮书第 4、5、11 节 | medium | 安全讨论离开该算力与网络假设。 |
| 新币发行与交易费可以激励节点保持诚实。 | source_opinion | 2008-10-31 | 白皮书第 6 节 | medium | 机制分析或实证不支持相关激励行为。 |

## 关联页面

- [[satoshi-nakamoto|Satoshi Nakamoto（中本聪）]]
- [[bitcoin-proof-of-work-consensus|Bitcoin 的 Proof-of-Work 共识与激励]]
- [[bitcoin-transaction-spv-and-privacy|Bitcoin 交易、SPV 与隐私边界]]
- [[2008-10-31-bitcoin-whitepaper-released|Bitcoin 白皮书公开发布（2008-10-31）]]
- [[bitcoin-attacker-catch-up-probability-model|Bitcoin 攻击者追赶概率模型]]

## 证据缺口与冲突

- 当前协议规范、客户端实现、治理、网络算力、能源消耗、交易市场、监管和采用均不在本次来源范围内。
- 本页不把“one-CPU-one-vote”解释为现代节点治理结构。
- 本页不建立 Bitcoin 作为当前资产的估值或交易判断。
