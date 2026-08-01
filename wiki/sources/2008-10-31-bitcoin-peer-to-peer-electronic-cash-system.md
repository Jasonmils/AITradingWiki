---
page_type: source
source_type: paper
subject: "Bitcoin: A Peer-to-Peer Electronic Cash System"
aliases:
  - "Bitcoin whitepaper"
  - "比特币白皮书"
tags:
  - bitcoin
  - peer-to-peer
  - proof-of-work
  - electronic-cash
  - cryptography
tickers: []
markets: []
asset_classes: []
industries:
  - distributed-systems
  - cryptography
themes:
  - peer-to-peer-electronic-cash
  - proof-of-work-consensus
  - double-spending
research_tracks:
  - technology
  - commercialization
as_of: 2008-10-31
sources:
  - "raw/bitcoin.pdf"
  - "https://www.metzdowd.com/pipermail/cryptography/2008-October/014810.html"
  - "https://bitcoin.org/en/bitcoin-paper"
  - "https://bitcoin.org/bitcoin.pdf"
created: 2026-08-01
updated: 2026-08-01
publication_date: 2008-10-31
verified_at: 2026-08-01
author: "Satoshi Nakamoto"
source_sha256: "b1674191a88ec5cdd733e4240a81803105dc412d6c6708d53ab94fc248f4f553"
source_size_bytes: 184292
pdf_pages: 9
local_pdf_creation_date: "2009-03-24 18:33:15 CET"
source_file_status: "retained_immutable"
---

# Bitcoin: A Peer-to-Peer Electronic Cash System

## 来源元数据

- 原始文件：`raw/bitcoin.pdf`
- 标题：*Bitcoin: A Peer-to-Peer Electronic Cash System*
- 作者署名：Satoshi Nakamoto；文内列出 `satoshin@gmx.com` 与 `www.bitcoin.org`。
- 来源类型：9 页技术论文，含 Abstract、正文第 1–12 节和参考文献。
- 首次公开日期：2008-10-31。该日期由 Cryptography Mailing List 的原始发布邮件核验；邮件链接指向 `http://www.bitcoin.org/bitcoin.pdf`。
- 知识截止日：2008-10-31。文档正文没有印刷发布日期或 revision 标识。
- 本地 PDF 元数据：Creator 为 Writer，Producer 为 OpenOffice.org 2.4，CreationDate 为 2009-03-24 18:33:15 CET。该文件生成日期不等于论文首次公开日期。
- 原始文件 SHA-256：`b1674191a88ec5cdd733e4240a81803105dc412d6c6708d53ab94fc248f4f553`
- 文件大小：184,292 bytes；未加密，无表单或 JavaScript。
- 身份核验：本地文件的标题、署名、9 页结构、章节与正文内容同 Bitcoin.org 标注为“Original”的英文版本一致；未验证两份 PDF 的逐字节哈希相同。
- 本地源文件状态：永久保留且未改动。

## 技术与模型口径

- 任务：在不依赖可信第三方的前提下，设计点对点电子现金并处理 double-spending（双重支付）。
- 系统边界：点对点网络、数字签名链、时间戳、hash-linked Proof-of-Work（哈希链接的工作量证明）、激励、Merkle Tree、简化支付验证与攻击者追赶概率。
- 软件、代码与版本：论文未附实现代码、网络版本、测试集、硬件配置或可执行复现实验。
- 对比基线：依赖金融机构作为可信第三方的电子支付，以及可信第三方负责识别双重支付的数字货币方案。
- 独立复现：本次仅复算论文的概率公式与表格；没有核验完整协议实现、网络安全性、生产部署或商业采用。
- 已知局限：概率模型假定固定算力份额及独立的 Poisson 区块到达过程；论文不等于当前 Bitcoin 协议、实现、网络经济或监管状态的完整说明。

## 摘要

1. 论文提出一种无需金融机构中介的点对点电子现金系统，使用点对点网络对交易进行时间排序，使攻击者若要改写历史必须重新完成相应 Proof-of-Work。
2. 所有权通过数字签名链转移；公开交易历史、区块、最长（累计工作量最大）链规则与诚实算力多数假设共同约束双重支付。
3. 新币发行与交易费为节点提供激励；论文认为，在预定发行量进入流通后，激励可逐步转由交易费承担。这是设计主张，不是已经验证的长期经济均衡。
4. Merkle Tree 支持删除已花费交易的旧数据；Simplified Payment Verification（SPV，简化支付验证）允许只保存区块头并通过 Merkle branch 验证交易被纳入区块。
5. 论文用攻击者算力占比 `q`、诚实节点占比 `p=1-q` 和确认差距 `z` 建立攻击者追赶概率模型；本地数值复算与论文表格一致，但这只确认算术实现，不验证现实网络中的全部攻击面。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| 论文提出使用点对点网络、时间戳与 Proof-of-Work 形成公开交易历史，以避免依赖可信第三方处理双重支付。 | verified_fact | 2008-10-31 | 论文 Abstract、第 1、3–5 节 | high | 本地文件内容或官方版本核验不再支持这一表述。 |
| 交易被定义为数字签名链：每位所有者签署上一笔交易的 hash 与下一位所有者的 public key。 | verified_fact | 2008-10-31 | 论文第 2 节 | high | 原文定义被证明误读。 |
| 论文以累计 Proof-of-Work 最大的链表示网络接受的事件顺序，并在诚实节点控制多数 CPU power 时给出安全论证。 | verified_fact | 2008-10-31 | 论文第 4、5、11 节 | high | 原文条件或链选择规则被证明误读。 |
| 节点激励可来自区块中的首笔新币交易与交易费，并可帮助节点保持诚实。 | source_opinion | 2008-10-31 | 论文第 6 节的机制设计与理性行为论证 | medium | 实证或机制分析显示该激励在所述边界下不足以支持预期行为。 |
| 只要诚实节点控制网络，SPV 用户可通过区块头与 Merkle branch 验证交易被网络接受。 | model_assumption | 2008-10-31 | 论文第 8 节 | medium | 网络、同步或攻击条件不满足诚实控制假设。 |
| 本地复算得到论文列示的 `q=0.1`、`q=0.3` 和 `P<0.001` 表格数值。 | codex_inference | 2026-08-01 | 按论文第 11 节公式与附录 C 代码进行数值复算 | high | 使用论文公式的独立复算产生不同结果。 |

## 实体

- [[bitcoin|Bitcoin（比特币）]]：论文定义的点对点电子现金系统/项目。
- [[satoshi-nakamoto|Satoshi Nakamoto（中本聪）]]：论文使用的作者署名；本次不推断其现实身份。

## 概念

- [[bitcoin-proof-of-work-consensus|Bitcoin 的 Proof-of-Work 共识与激励]]
- [[bitcoin-transaction-spv-and-privacy|Bitcoin 交易、SPV 与隐私边界]]

## 事件

- [[2008-10-31-bitcoin-whitepaper-released|Bitcoin 白皮书公开发布（2008-10-31）]]

## 提及的模型或假设

- [[bitcoin-attacker-catch-up-probability-model|Bitcoin 攻击者追赶概率模型]]
- 核心假设包括：攻击者与诚实节点分别以固定概率 `q`、`p` 找到下一区块；诚实链平均生成 `z` 个区块时，攻击者区块数服从参数 `λ=z(q/p)` 的 Poisson 分布；网络消息最终传播；攻击者目标被简化为从 `z` 个区块差距追上诚实链。

## 技术成熟度与商业化边界

本来源能直接证明的是“研究论文已公开”与“论文提出了机制和模型”。按本次来源边界，最高技术证据为 `research`，商业化证据为 `none`。这不是对 Bitcoin 在 2008-10-31 之后的实现、独立复现、prototype、production deployment、scaled adoption、付费使用、收入、利润或 FCF 的否定；只是这些后续里程碑不由这份论文单独证明。

## 证据缺口与冲突

1. 论文没有打印 publication date 或 revision；2008-10-31 来自原始邮件列表发布记录，本地 PDF 的 2009-03-24 元数据仅表示该文件的生成时间。
2. 本地文件与 Bitcoin.org 官方英文原版在内容和页结构上匹配，但没有验证远端 PDF 与本地文件逐字节相同。
3. 论文发布不等于同行评审、独立复现、开源实现、prototype、生产部署或规模采用。
4. “one-CPU-one-vote”描述的是论文中的 Proof-of-Work 投票权重，不应解释成现代节点治理的一人一票或一台机器一票。
5. public key pseudonymity（公钥假名性）不等于匿名；交易图关联可能暴露同一所有者的多笔交易。
6. 固定确认数不是普遍安全保证。攻击概率取决于攻击者资源、网络条件、交易价值与论文未建模的攻击面。
7. 本页不包含当前 Bitcoin 价格、监管、市场结构、协议实现或投资建议。
