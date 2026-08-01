---
page_type: event
subject: "Bitcoin 白皮书公开发布（2008-10-31）"
aliases:
  - "Bitcoin whitepaper release"
  - "比特币白皮书发布"
tags:
  - bitcoin
  - research-release
  - whitepaper
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
as_of: 2026-08-01
sources:
  - "[[2008-10-31-bitcoin-peer-to-peer-electronic-cash-system|Bitcoin: A Peer-to-Peer Electronic Cash System]]"
  - "https://www.metzdowd.com/pipermail/cryptography/2008-October/014810.html"
  - "https://bitcoin.org/en/bitcoin-paper"
created: 2026-08-01
updated: 2026-08-01
status: active
confidence: high
horizon: 3-5y
review_after: 2027-08-01
event_type: research_release
event_status: completed
technology_maturity: research
commercialization_stage: none
announcement_date: 2008-10-31
expected_date:
effective_date: 2008-10-31
---

# Bitcoin 白皮书公开发布（2008-10-31）

## 事件摘要

2008-10-31，使用 Satoshi Nakamoto 署名的发件人在 Cryptography Mailing List 发布题为“Bitcoin P2P e-cash paper”的邮件，宣布正在开发一种完全点对点、无需可信第三方的电子现金系统，并链接 *Bitcoin: A Peer-to-Peer Electronic Cash System*。本地 `raw/bitcoin.pdf` 的标题、署名、9 页结构与 Bitcoin.org 标注的英文原版内容一致。

本 Event 只确认研究发布。`technology_maturity: research` 与 `commercialization_stage: none` 描述的是该发布事件当时由论文直接支持的最高证据，不是 Bitcoin 的当前技术或商业化状态。

## 时间线

| 日期 | 里程碑 | 事件状态 | 证据 |
|---|---|---|---|
| 2008-10-31 | Satoshi Nakamoto 向 Cryptography Mailing List 发布 Bitcoin P2P e-cash paper 邮件并链接论文。 | completed | 邮件列表原始归档 |
| 2009-03-24 | 本地 PDF 元数据显示该文件由 OpenOffice.org 2.4 生成。 | completed | `raw/bitcoin.pdf` 元数据；不是论文首次公开日期 |
| 2026-08-01 | 本地 PDF 与 Bitcoin.org 英文原版完成标题、署名、章节、页数和内容核验。 | completed | 本地逐页审阅与 Bitcoin.org 官方页面；未做远端逐字节哈希比对 |

## 已确认事实

- 发布邮件的归档时间为 Fri Oct 31 14:10:00 EDT 2008。
- 邮件说明系统为 fully peer-to-peer，并把论文链接指向 `http://www.bitcoin.org/bitcoin.pdf`。
- 本地论文标题为 *Bitcoin: A Peer-to-Peer Electronic Cash System*，作者署名为 Satoshi Nakamoto。

## 公司陈述

不适用；该来源不是公司披露。

## 传闻或争议性论断

- Satoshi Nakamoto 的现实身份不由发布邮件或白皮书确认；本次不记录身份候选。
- 2009-03-24 是本地 PDF 生成元数据，不与 2008-10-31 的公开发布日合并。

## 技术相关性

该事件建立 Bitcoin 技术研究的可追溯起点：点对点电子现金、数字签名链、时间戳、Proof-of-Work、累计工作量链选择、激励、Merkle Tree、SPV 和攻击者追赶概率模型在一份公开论文中被统一提出。

## 商业化相关性

论文定义了支付问题和节点激励，但发布事件本身不证明 prototype、网络上线、商户使用、付费采用、正式订单、收入、利润或 FCF。

## 投资相关性

本事件不提供当前资产价格、交易场所、监管、流动性、估值或可交易性判断。研究发布不能直接推出投资价值。

## 阶段晋级所需的下一项证据

若沿历史链条继续研究，下一步应分别核验：公开代码或可运行实现、创世区块与网络运行证据、独立节点复现、实际交易与用户采用。每一步应单独建立 Source/Event，不能由白皮书发布自动晋级。

## 下一步核验

- 取得并版本化最早公开软件、源代码与网络运行的一手记录；
- 区分论文设计、最早实现和现代协议规则；
- 仅在需要当前研究时，再核验网络、采用、市场与监管数据。

## 证据缺口与失效条件

- 远端官方 PDF 未与本地文件进行逐字节 SHA-256 比较。
- 如果原始邮件归档的真实性、日期或论文链接归属被权威证据推翻，应更新事件状态。
- `horizon: 3-5y` 是页面复核周期分类，不是交易持有期，也不是论文确认数或技术成熟时间。

## 关联页面

- [[bitcoin|Bitcoin（比特币）]]
- [[satoshi-nakamoto|Satoshi Nakamoto（中本聪）]]
- [[bitcoin-proof-of-work-consensus|Bitcoin 的 Proof-of-Work 共识与激励]]
- [[bitcoin-transaction-spv-and-privacy|Bitcoin 交易、SPV 与隐私边界]]
- [[bitcoin-attacker-catch-up-probability-model|Bitcoin 攻击者追赶概率模型]]
