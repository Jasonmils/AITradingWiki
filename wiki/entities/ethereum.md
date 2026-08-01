---
page_type: entity
entity_type: project
subject: "Ethereum（以太坊）"
aliases:
  - "Ethereum"
  - "以太坊"
tags:
  - ethereum
  - blockchain-platform
  - smart-contract
  - decentralized-application
tickers: []
markets: []
asset_classes: []
industries:
  - distributed-systems
  - cryptography
themes:
  - blockchain-application-platform
  - smart-contracts
research_tracks:
  - technology
  - commercialization
as_of: 2014-12-31
sources:
  - "[[2014-ethereum-next-generation-smart-contract-platform|Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform]]"
created: 2026-08-01
updated: 2026-08-01
---

# Ethereum（以太坊）

## 身份与范围

Ethereum 是[[2014-ethereum-next-generation-smart-contract-platform|2014 年白皮书]]提出的通用区块链应用平台。本页只建立该历史来源支持的项目与技术对象，不把之后的主网上线、协议升级、生态采用、治理、市场资产或监管状态倒填到白皮书时期。

- 实体类型：`project`
- 文档中的名称：Ethereum
- 白皮书署名作者：[[vitalik-buterin|Vitalik Buterin]]
- 问题定义：既有区块链往往只支持单一用途或受限脚本；Ethereum 希望提供可编程状态转换层，使用户在共享底层上构建合约和 DApp。
- 历史技术基线：账户状态、交易、内部 message、EVM bytecode、Gas、contract storage、历史 PoW 与 modified GHOST。
- 证券或市场标识：本来源没有定义上市证券或交易制度，故不填 ticker、market 或 asset class。

## 白皮书所定义的对象

Ethereum 被描述为一条带内建 Turing-complete 编程语言的区块链。参与者可以创建任意规则来管理所有权、交易格式和状态转换，并让合约在接收 transaction 或 message 后执行代码、读写 storage 和发送后续 message。

## 技术与商业状态边界

| 里程碑 | 本来源能否证明 | 说明 |
|---|---|---|
| research publication | 是 | 官方页面确认白皮书于 2014 年发布，且 2014-01-23 官方博文宣布项目公开。 |
| independent reproduction | 否 | 本次只做发行表算术复算，不是 EVM 或协议复现。 |
| prototype / implementation | 否 | 白皮书未附可核验的完整客户端与运行记录。 |
| pilot / production deployment | 否 | 文档没有生产网络部署证据。 |
| scaled adoption | 否 | 应用清单是设计示例，不是用户、交易量或生产采用证据。 |
| paid use / revenue / profit / FCF | 否 | Gas、手续费与发行属于协议机制，不等于企业商业收入或现金流。 |

因此，若只按该来源分类，技术成熟度上限为 `research`，商业化阶段为 `none`。这只是白皮书证据边界，不代表 Ethereum 的当前状态。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| Ethereum 在白皮书中被定义为通用的 smart contract 与 decentralized application 平台。 | verified_fact | 2014-12-31 | [[2014-ethereum-next-generation-smart-contract-platform|白皮书]]标题、Abstract 与 Ethereum 部分 | high | 原文定义被证明误读。 |
| 账户、EVM 和 Gas 共同构成白皮书描述的可编程状态转换机制。 | verified_fact | 2014-12-31 | 白皮书 Ethereum Accounts、Messages and Transactions、Ethereum Virtual Machine | high | 原文执行机制被证明误读。 |
| 通用平台路线会比为每个应用建立独立区块链更容易开发并获得组合性。 | source_opinion | 2014-12-31 | 白皮书 Motivation 与 Applications | medium | 实现、性能或采用数据不支持该比较。 |

## 关联页面

- [[vitalik-buterin|Vitalik Buterin]]
- [[ethereum-account-state-evm-and-gas|Ethereum 账户状态、EVM 与 Gas]]
- [[blockchain-application-platform-design-tradeoffs|区块链应用平台的设计路线权衡]]
- [[smart-contracts-dapps-and-oracle-boundaries|Smart Contract、DApp 与 Oracle 证据边界]]
- [[2014-01-23-ethereum-goes-public|Ethereum 项目公开发布（2014-01-23）]]
- [[ethereum-whitepaper-issuance-model|Ethereum 白皮书历史发行与供给均衡模型]]

## 证据缺口与冲突

- 官方白皮书页面明确提示原始白皮书已经不能准确反映当前 Ethereum；本页不可用于当前协议事实核验。
- 白皮书没有证明后续客户端实现、主网上线、协议升级、生产采用、经济安全或生态商业化。
- 当前 ETH 的资产属性、供给、价格、市场结构、监管与投资判断均不在本页范围内。
