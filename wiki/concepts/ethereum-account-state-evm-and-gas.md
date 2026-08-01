---
page_type: concept
concept_type: architecture
subject: "Ethereum 账户状态、EVM 与 Gas"
aliases:
  - "Ethereum account model, EVM and gas"
  - "以太坊账户模型与虚拟机"
tags:
  - ethereum
  - account-model
  - evm
  - gas
  - state-transition
tickers: []
markets: []
asset_classes: []
industries:
  - distributed-systems
  - cryptography
themes:
  - programmable-state-transition
  - smart-contract-execution
research_tracks:
  - technology
  - commercialization
as_of: 2014-12-31
sources:
  - "[[2014-ethereum-next-generation-smart-contract-platform|Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform]]"
created: 2026-08-01
updated: 2026-08-01
---

# Ethereum 账户状态、EVM 与 Gas

## 问题与范围

本页提炼 2014 白皮书如何把通用区块链应用表示为账户状态与确定性执行。它不是当前 Ethereum Yellow Paper、客户端实现或费用市场的替代规范；白皮书中的 `STARTGAS`、`GASPRICE`、PoW block validation 等属于历史版本语境。

## 定义

白皮书把系统状态表示为所有账户的集合，每个账户由 20-byte address 标识，并包含四类字段：

1. nonce：计数该账户发出的 transaction，或对 contract account 则计数其创建的 contract；
2. ether balance；
3. contract code（若存在）；
4. storage：默认空的持久 key/value store。

账户分为两类：EOA（externally owned account，外部拥有账户）由 private key 控制；contract account（合约账户）由 code 控制。Transaction 是由 EOA 签名的外部输入，message 则可在合约执行中由合约发出。

## 核心机制

### 状态转换

白皮书用 `APPLY(S, TX) -> S'` 表示交易把旧状态 `S` 转为新状态 `S'`。过程依次检查格式、签名、nonce 与起始 Gas，预扣执行费用，向接收账户转移 value，执行代码，并在成功后退还未使用 Gas；若执行耗尽 Gas，则回滚该执行产生的状态变化，但不退还已经计入资源消耗的费用。

### EVM

- EVM 为 stack-based virtual machine（基于栈的虚拟机）。
- 每个 stack item 为 32 bytes，stack 最大深度为 1024。
- memory 是可扩展的 byte array，生命周期限于一次计算。
- storage 是 contract account 的持久状态，由 32-byte key 映射到 32-byte value。
- 执行状态还包括 program counter、remaining gas、当前 transaction/message、code 与全局 block state。
- EVM 被设计为 Turing-complete，但每次执行受 Gas 上限约束，因此不是无限计算承诺。

### Gas

每条计算、storage、memory 扩展和 transaction data 操作消耗 Gas。白皮书把 Gas 解释为：限制恶意或失控计算、对节点资源进行计价，并让发送者为自己请求的计算付费。Gas 是计算单位，ether 是支付媒介；`GASPRICE` 把二者关联。

## 竞争或替代路线

| 路线 | 机制 | 优势 | 约束 | 当前证据 | 成熟度 |
|---|---|---|---|---|---|
| UTXO 与受限脚本 | 以未花费输出表达状态，脚本语言限制循环与复杂状态 | 验证边界较窄、状态模型明确 | 通用状态与跨合约逻辑较难表达 | 白皮书对 Bitcoin scripting 的历史比较 | 不在本来源重新评估 |
| Meta-protocol | 在既有链交易中编码上层状态，由额外客户端解释 | 复用底层共识 | light client、可扩展性与功能边界受底层支持限制 | 白皮书对 Mastercoin 等路线的来源论述 | research |
| Account + EVM + Gas | 账户保存余额、代码与 storage，EVM 执行通用 bytecode，Gas 约束资源 | 统一可编程状态与合约间 message | 执行成本、状态增长、攻击面和费用设计复杂 | 白皮书机制说明；未在本来源独立复现 | research |

## 指标、Benchmark 与可比边界

- 白皮书给出栈宽度、栈深度、memory/storage 语义和指令计费原则，但没有提供同硬件、同负载的吞吐、延迟、状态增长或费用 benchmark。
- “Turing-complete”描述表达能力，不代表任何程序都能在给定 block gas 或经济成本内执行。
- 白皮书的历史 block operation cap 与费用调节规则不能映射为当前 base fee、priority fee 或 block gas limit。
- 算术/执行语义需要版本化规范和客户端测试才能独立复现；本文没有完成这种复现。

## 技术成熟度与商业化边界

按本来源，账户/EVM/Gas 架构最高证据为 `research`。机制完整度高于概念口号，但没有同版本客户端、测试向量、独立复现或生产运行证据。Gas 费用是协议资源分配机制，不自动等于某个实体的收入、利润或 FCF。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| 白皮书账户包含 nonce、balance、code 与 storage，并区分 EOA 与 contract account。 | verified_fact | 2014-12-31 | 白皮书 Ethereum Accounts | high | 原文定义被证明误读。 |
| EVM 使用 32-byte stack item、短期 memory 与持久 storage 执行合约 bytecode。 | verified_fact | 2014-12-31 | 白皮书 Ethereum Virtual Machine | high | 原文执行结构被证明误读。 |
| Gas 可使任意计算在资源上可计价，并避免无限循环永久占用协议。 | source_opinion | 2014-12-31 | 白皮书 Fees 与 Computation And Turing-Completeness | medium | 实现或经济分析显示所述计费无法实现该边界。 |
| Out-of-gas 会回滚执行状态变化但保留费用扣除。 | verified_fact | 2014-12-31 | 白皮书 Ethereum State Transition Function | high | 原文执行语义被证明误读。 |

## 关键未知项与待验证问题

- 哪个具体客户端或协议 revision 首次实现了这套语义？
- 合约间调用、异常、re-entrancy、state growth 与并发访问的实际安全边界是什么？
- 当前 Ethereum 对账户、执行、费用和共识分别有哪些后续变化？
- 在同一 workload、硬件与安全假设下，EVM 路线与替代执行环境的性能和开发成本如何比较？

## 产业与投资桥接

可编程执行可以支持应用开发，但表达能力不等于可靠部署、用户采用或价值捕获。开展商业化研究时，需要分别核验开发工具、审计、安全事故、用户需求、费用承担者和实际支付；开展资产研究还需另行核验当前协议、供给、监管、市场结构与估值。

## 关联实体、事件与模型

- [[ethereum|Ethereum（以太坊）]]
- [[vitalik-buterin|Vitalik Buterin]]
- [[blockchain-application-platform-design-tradeoffs|区块链应用平台的设计路线权衡]]
- [[smart-contracts-dapps-and-oracle-boundaries|Smart Contract、DApp 与 Oracle 证据边界]]
- [[2014-01-23-ethereum-goes-public|Ethereum 项目公开发布（2014-01-23）]]
- [[ethereum-whitepaper-issuance-model|Ethereum 白皮书历史发行与供给均衡模型]]
