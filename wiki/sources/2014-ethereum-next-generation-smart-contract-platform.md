---
page_type: source
source_type: paper
subject: "Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform"
aliases:
  - "Ethereum whitepaper"
  - "以太坊白皮书"
tags:
  - ethereum
  - smart-contract
  - decentralized-application
  - evm
  - gas
tickers: []
markets: []
asset_classes: []
industries:
  - distributed-systems
  - cryptography
themes:
  - blockchain-application-platform
  - smart-contracts
  - decentralized-applications
research_tracks:
  - technology
  - commercialization
as_of: 2014-12-31
sources:
  - "raw/Ethereum_Whitepaper_-_Buterin_2014.pdf"
  - "https://ethereum.org/whitepaper/"
  - "https://ethereum.org/content/whitepaper/whitepaper-pdf/Ethereum_Whitepaper_-_Buterin_2014.pdf"
  - "https://blog.ethereum.org/2014/01/23/ethereum-now-going-public"
created: 2026-08-01
updated: 2026-08-01
publication_year: 2014
verified_at: 2026-08-01
author: "Vitalik Buterin"
source_sha256: "4cc15f99f5df56c8a7156188a9b9290c71e7dfd9a92093b028213c9a185c0a15"
source_size_bytes: 941366
pdf_pages: 36
pdf_modified_at: "2022-02-02 14:40:12 CET"
source_file_status: "retained_immutable"
---

# Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform

## 来源元数据

- 原始文件：`raw/Ethereum_Whitepaper_-_Buterin_2014.pdf`
- 标题：*Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform.*
- 作者署名：[[vitalik-buterin|Vitalik Buterin]]。
- 来源类型：36 页技术白皮书；第 3 页除页脚外为空白，经逐页视觉核验属于版式而非提取失败。
- 发布年份：2014。Ethereum 官方白皮书页面将其标为 2014 年发布，但本地 PDF 没有精确 publication date 或 revision；为便于排序，`as_of: 2014-12-31` 仅表示年份上界，不是精确发布日期。
- 相关公开事件：2014-01-23 的 Ethereum Foundation 官方博文宣布项目“going public”并提及此前已形成初稿；该日期不等于本地 PDF 的精确 revision 日期。
- 本地 PDF 元数据：Author 与 Creator 为 Vitalik Buterin，Producer 为 Paul Dylan-Ennis，ModDate 为 2022-02-02 14:40:12 CET。该修改元数据不等于白皮书首次发布日期。
- 原始文件 SHA-256：`4cc15f99f5df56c8a7156188a9b9290c71e7dfd9a92093b028213c9a185c0a15`
- 文件大小：941,366 bytes；36 页，未加密，无 JavaScript。PDF 声明 AcroForm，但本地结构检查发现 0 个表单字段、0 个 widget 与 42 个普通 annotation。
- 身份核验：本地文件的标题、作者、36 页结构和正文关键参数与 Ethereum.org 官方下载 PDF 一致；未验证远端 PDF 与本地文件逐字节哈希相同。
- 本地源文件状态：永久保留且未改动。

## 技术与模型口径

- 任务：把区块链从单一应用账本扩展为可执行任意状态转换规则的通用平台。
- 系统边界：账户状态、交易与内部 message、EVM（Ethereum Virtual Machine，以太坊虚拟机）、Gas、合约存储、区块状态根、历史 Proof-of-Work 共识、uncle/GHOST 设计、DApp 和 DAO 应用示例。
- 软件、代码与版本：论文给出伪代码和示例合约，但未附可运行客户端版本、测试集、部署配置或完整 benchmark。
- 独立复现：本次只完成白皮书历史发行表与供给均衡算术复算；没有复现 EVM、共识、安全性、应用部署或网络采用。
- 当前适用性：Ethereum 官方页面明确提示原始白皮书经过十余年升级后已不能准确反映当前 Ethereum。白皮书中的 PoW、矿工发行与历史费用描述不得作为当前协议事实。

## 摘要

1. 白皮书把区块链抽象为 `APPLY(S, TX) -> S'` 的状态转换系统，并提出内建 Turing-complete 编程语言，使用户可定义任意状态转换函数，而不必为每种应用建立独立区块链。
2. 系统使用 account-based state（账户状态）：外部拥有账户由私钥控制，合约账户由代码控制；交易由外部账户发起，合约可在执行中发送内部 message。
3. EVM 采用 32-byte stack、可扩展 memory 与持久化 key/value storage；Gas 为每项计算、存储和数据操作计价，并在执行耗尽 Gas 时回滚状态变化但保留费用扣除。
4. 白皮书列举 token、稳定价值货币、身份与信誉、去中心化文件存储、DAO、多签钱包、保险、数据馈送、赌博和预测市场等应用，但这些是设计示例或来源主张，不是实现、采用或商业收入证据。
5. 论文给出以 `X` 为销售量基准的历史发行模型，包括购买者、早期贡献者、长期研究基金与持续矿工发行；本地复算与表格一致，但 PoW 已在 2022 年 The Merge 后被弃用，因此该模型只保留为历史设计证据。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| 白皮书提出一条带内建 Turing-complete 语言的区块链，使参与者可创建合约和去中心化应用。 | verified_fact | 2014-12-31 | 本地 PDF Abstract、Introduction 与 Ethereum 部分 | high | 本地文档内容或来源身份核验不再支持该表述。 |
| Ethereum 状态由账户构成；账户包含 nonce、ether balance、contract code 与 storage，并分为外部拥有账户和合约账户。 | verified_fact | 2014-12-31 | 本地 PDF “Ethereum Accounts” | high | 原文定义被证明误读。 |
| Gas 对计算、存储和带宽进行资源计量，执行耗尽 Gas 时状态变化回滚，但交易发送者仍支付执行费用。 | verified_fact | 2014-12-31 | 本地 PDF “Messages and Transactions”与“Ethereum State Transition Function” | high | 原文执行语义被证明误读。 |
| 通用平台可降低新建区块链应用的实现门槛并形成更基础的协议层。 | source_opinion | 2014-12-31 | 白皮书 Motivation 与 Applications | medium | 实现、复现或采用证据显示通用平台没有所述开发或组合优势。 |
| 五层 GHOST 方案在 15 秒区块时间下可达到超过 95% 的效率，且矿池中心化收益保持低于 3%。 | model_assumption | 2014-12-31 | 白皮书 Mining Centralization 与 Scalable Decentralization | low | 同条件 benchmark、网络数据或独立复现不支持相关参数。 |
| 本地复算得到发行表的 `1.198X`、`1.458X`、`2.498X` 总量及各组比例，并得到 1% 年损失率下 `26X` 的均衡量。 | codex_inference | 2026-08-01 | 按白皮书 Fees and Allocation 的公式与表格复算 | high | 使用同一公式的独立复算得到不同结果。 |
| 官方下载 PDF 写明销售为 `1337-2000 ether per BTC`、最大矿池示例为前两家；当前官方 HTML 分别写作 `1000-2000` 与前三家。 | disputed | 2026-08-01 | 本地/官方 PDF 与 Ethereum.org 当前 HTML 对照 | high | 官方提供明确 revision 映射，证明两者可无冲突地归入同一版本。 |

## 实体

- [[ethereum|Ethereum（以太坊）]]：白皮书提出的通用区块链应用平台项目。
- [[vitalik-buterin|Vitalik Buterin]]：白皮书署名作者与 2014-01-23 官方公开博文作者。

## 概念

- [[ethereum-account-state-evm-and-gas|Ethereum 账户状态、EVM 与 Gas]]
- [[blockchain-application-platform-design-tradeoffs|区块链应用平台的设计路线权衡]]
- [[smart-contracts-dapps-and-oracle-boundaries|Smart Contract、DApp 与 Oracle 证据边界]]

## 事件

- [[2014-01-23-ethereum-goes-public|Ethereum 项目公开发布（2014-01-23）]]

## 提及的模型或假设

- [[ethereum-whitepaper-issuance-model|Ethereum 白皮书历史发行与供给均衡模型]]
- 历史共识假设包括 PoW、modified GHOST、uncle 纳入以及矿工持续发行；这些不能作为当前 Ethereum 的共识或发行规则。
- 应用层假设包括稳定价值货币、数据馈送、计算市场和 DAO 等可由合约实现；实现可行性、oracle 信任、用户采用、收入和价值捕获必须分别核验。

## 技术成熟度与商业化边界

本来源直接证明的是研究设计已成文并公开。按这份白皮书的单一来源边界，最高技术证据为 `research`，商业化证据为 `none`。合约伪代码和应用示例不等于独立复现、prototype、pilot、production deployment、scaled adoption、付费使用、收入、利润或 FCF。后续 Ethereum 实现与协议演进需要独立 Source/Event 支持。

## 证据缺口与冲突

1. 本地 PDF 没有精确发布日期或 revision；`2014-12-31` 只是年份上界。2014-01-23 是项目公开事件，不是该文件版本的精确日期。
2. 本地 PDF 的 2022 ModDate 是文件再生成/修改元数据，不能当作白皮书首次发布时间。
3. 本地文件与官方可下载 PDF 的内容和 36 页结构匹配，但没有验证远端逐字节 SHA-256。
4. Ethereum.org 当前 HTML 与官方 PDF 存在实质文本差异，包括销售兑换范围、矿池数量和后加的 PoS/社会契约内容。本页以本地 PDF 为唯一摄入正文，不静默采用网页修订。
5. “Namecoin in two lines”“协议少于二十行”与 GHOST 效率等论断缺少同版本代码、基准条件和独立复现，不能升级为已验证性能事实。
6. 数据馈送、稳定价值资产、保险和预测市场依赖外部数据或受信任主体。白皮书本身承认单一可信 data feed 会削弱完全去中心化属性。
7. 白皮书中的 PoW、矿工、发行和费用设计是历史方案；Ethereum 已在 2022-09-15 The Merge 后改用 PoS，费用机制也受到 EIP-1559 等后续升级影响。
8. 本页不包含当前 Ethereum 协议全貌、ETH 供给、价格、监管、估值或交易建议。
