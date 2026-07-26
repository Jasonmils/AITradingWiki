---
page_type: concept
subject: "光路交换机（OCS）"
aliases:
  - "Optical Circuit Switch"
  - OCS
  - "光路交换机"
tags:
  - technology
  - optical-networking
  - data-center-networking
tickers: []
markets: []
asset_classes:
  - equity
industries:
  - optical-components
  - data-center-networking
themes:
  - AI infrastructure
  - optical circuit switching
as_of: 2026-04-17
sources:
  - "[[goldman-sachs-global-tech-optical-networking-2026-04-17|高盛全球科技：光网络（2026-04-17）]]"
created: 2026-07-24
updated: 2026-07-24
---

# 光路交换机（OCS）

## 定义与机制

报告将 Optical Circuit Switch（OCS，光路交换机）定义为一种全光交换路线：在输入和输出光纤之间建立模拟光路，不采用传统数据中心交换机的光—电—光转换。

报告认为，同一台 OCS 可以传输 800G、1.6T 和 3.2T 光信号，因此在数据速率升级时可能无需更换交换机。这属于 `source_opinion`，不是已经独立验证的普遍属性。

## 技术路线

| 路线 | 报告所述进展 | 切换时间 | 可靠性 | 插入损耗 | 主要权衡 | 证据类型 |
|---|---|---|---|---|---|---|
| MEMS | 已量产；主流方案 | 中等，<100ms | 低 | 低，约 3dB | 技术成熟，但依赖机械驱动 | source_opinion |
| LC/LCoS | 已量产 | 慢，>100ms | 高 | 低，约 4dB | 可靠性较高，但切换较慢且端口数受限 | source_opinion |
| Piezo/DLBS | 认证中 | 中等，<100ms | 高 | 低，约 2.5dB | 损耗较低，但串扰较高 | source_opinion |
| SiPh | 认证中 | 纳秒级 | 高 | 高，约 6dB | 速度快且量产后可能低成本，但插损和串扰较高 | source_opinion |

来源：PDF 第 23 页 Exhibit 43。

## 报告描述的采用与供应商信号

| 日期或期间 | 论断 | 数值 | 证据类型 | PDF 证据 |
|---|---|---:|---|---|
| 2015 | Google 启动 Apollo OCS 研发项目 | — | company_statement | 第 22 页 Exhibit 42 |
| 2023 | Google TPU v4 超级计算机使用 48 台自研 OCS 互连 4,096 颗芯片 | 4,096 颗芯片；48 台 OCS | company_statement | 第 22 页 Exhibit 42 |
| 2025 | Google TPU v7 SuperPod 使用 OCS 互连 9,216 颗芯片 | 9,216 颗芯片 | company_statement | 第 22 页 Exhibit 42 |
| 2025 | OCP 宣布 OCS 项目并列出参与方 | — | company_statement | 第 22 页 Exhibit 42 |
| 2026 年 2 月 | Lumentum OCS backlog 超过 US$400m | >400 | company_statement | 第 22 页 |
| 2026 年 2 月 | Coherent 报告拥有超过 10 个 OCS 客户接洽项目 | >10 个客户 | company_statement | 第 22 页 |
| 报告截止日 | Robotechnik 报告获得欧洲客户的 OCS 封装产线订单 | EUR7.7m | company_statement | 第 22 页 |
| 2027 年目标 | Innolight 计划推出 SiPh OCS | — | company_statement | 第 22 页 |

所有公司论断均由高盛报告二手转述，需要一手核验。

## ASP 估算

| 产品 | 区间 | 期间 | 发布日期 | 币种 | 单位 | 证据类型 | 来源 |
|---|---:|---|---|---|---|---|---|
| OCS 交换机 | 50–200 | 截至 2026 年 4 月 | 2026-04-17 | USD | US$k/switch | source_opinion | 来源报告第 23 页 Exhibit 44 |
| 传统交换机 | 10–100 | 截至 2026 年 4 月 | 2026-04-17 | USD | US$k/switch | source_opinion | 来源报告第 23 页 Exhibit 44 |

## 投资相关机制

- 潜在收益：带宽灵活性、更低的转换开销、功率效率以及更长的升级周期。
- 采用约束：各技术路线的可靠性、插入损耗、切换时间、串扰、端口规模和认证状态。
- 价值链影响：OCS 可能把部分交换价值量转向光学系统，但不会消除服务器主板对光模块的需求。

## 跟踪指标

- 客户部署数量和端口规模。
- OCS backlog 向出货和已确认收入的转化。
- 各路线的插入损耗、切换时间、可靠性和串扰。
- ASP、毛利率和安装成本。
- 供应商订单和客户认证的一手证据。

## 证据缺口与冲突

- 未摄入供应商一手公告、客户验收文件或收入确认依据。
- Backlog、订单、出货、已确认收入、利润和现金流仍需严格区分。
- 现有证据是一组二手论断，而非一个经一手核验的明确日期事件，因此未创建独立 Event。
