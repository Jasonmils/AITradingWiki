---
page_type: event
subject: "华为发布韬（τ）定律"
aliases:
  - "韬定律"
  - "τ 定律"
  - "Tau Scaling Law"
  - "华为 Tau Scaling"
tags:
  - semiconductor
  - huawei
  - logic-folding
  - system-co-design
  - technology-announcement
tickers: []
markets:
  - CN
  - GLOBAL
asset_classes:
  - equity
industries:
  - semiconductor
  - artificial-intelligence
  - computing-infrastructure
themes:
  - tau-scaling
  - logic-folding
  - transistor-density
  - system-level-compute
as_of: 2026-06-09
sources:
  - "https://www.huawei.com/cn/news/2026/5/ieee-iscas-tau-scaling"
  - "[[2026-06-09-china-semiconductor-frontier-innovation-and-inference|从变化中看到确定性：中国半导体前沿创新与推理需求（2026-06-09）]]"
created: 2026-07-29
updated: 2026-07-29
status: active
confidence: high
horizon: 3-5y
review_after: 2026-12-31
event_type: other
event_status: completed
announcement_date: 2026-05-25
expected_date:
effective_date: 2026-05-25
---

# 华为发布韬（τ）定律（2026-05-25）

## 事件摘要

2026-05-25，华为何庭波在 IEEE ISCAS 2026 发表“半导体新路径探索与实践”主旨演讲，并发布华为称为“韬（τ）定律”的半导体与电子系统演进原则。发布事件本身为 `verified_fact`。

华为将其描述为以“时间（τ）缩微”补充或替代单纯的几何缩微，通过 LogicFolding（逻辑折叠）、软件/架构/芯片协同、统一内存语义和系统互联等持续降低信号传播与系统通信时延。技术效果、产品数量和 2031 路线图均来自华为，分类为 `company_statement`，不能因发布发生就升级为独立验证成果。

## 时间线

| 日期 | 里程碑 | 事件状态 | 证据 |
|---|---|---|---|
| 2020–2026 | 华为称在过去六年基于该路径设计并量产 381 款芯片。 | company_statement | 华为新闻稿；缺少逐产品清单和统一量产定义 |
| 2026-05-25 | 何庭波在 IEEE ISCAS 2026 主旨演讲中发布韬（τ）定律。 | completed | [华为新闻稿](https://www.huawei.com/cn/news/2026/5/ieee-iscas-tau-scaling) |
| 2026 年秋季 | 华为计划推出采用 LogicFolding 的麒麟芯片。 | pending | 华为公司计划，未公布精确日期和独立测试 |
| 2031 | 华为预计基于该路径的高端芯片晶体管密度达到“1.4nm 制程同等水平”。 | pending | 华为路线图，不是已实现工艺节点 |

`event_status: completed`只指 2026-05-25 发布事件已经发生，不表示 2026 年秋季产品计划或 2031 路线图已经完成。

## 已确认事实

- IEEE ISCAS 2026 举办期间，华为于 2026-05-25 公布了这一命名和技术框架；
- 何庭波发表了“半导体新路径探索与实践”主旨演讲；
- 华为新闻稿把韬（τ）定律定义为以缩短信号传播时延为目标的多层级协同原则；
- 华为把框架分为器件、电路、芯片和系统层；
- 发布材料提及 LogicFolding、软件/架构/芯片协同、灵衢总线和统一内存语义。

这些内容确认“公司发布了什么”，不确认：

- “定律”已经获得独立学术界普遍接受；
- 381 款芯片都采用同一可核验实现；
- LogicFolding 已按公开规格量产；
- 等效 1.4nm 密度代表相同功耗、性能、良率或成本；
- 路线图会按期兑现。

## 公司陈述

华为新闻稿作出以下陈述：

1. 在过去六年中，华为基于韬（τ）定律成功设计并量产了 381 款芯片；
2. 将于 2026 年秋季面世的麒麟芯片将率先采用 LogicFolding；
3. 预计到 2031 年，基于该路径的高端芯片晶体管密度将达到 1.4nm 制程同等水平；
4. 多层级协同可持续提高性能、能效和晶体管密度。

这些陈述应分别验证：

- 产品清单、设计归属和“量产”的定义；
- 产品发布日期、芯片型号和技术实现；
- 晶体管密度、面积、功耗、性能、良率和成本；
- 实际工作负载、软件栈和系统性能；
- 独立测试、客户采用和财务贡献。

## 与制程节点的区分

[[2026-06-09-china-semiconductor-frontier-innovation-and-inference|来源课程]]把华为路线图与 TSMC、Intel 和 Samsung 的节点名称进行直接比较，并口播 TSMC 在 2026 年“已经在做 1.4nm”。

TSMC 2025 年报的正式口径是：

- A14 技术开发进展顺利；
- A14 计划于 2028 年量产；
- 2nm 已于 2025 年第四季度进入高量产；
- N2P 和 A16 计划于 2026 年下半年量产。

因此：

- “TSMC 正在开发 A14”：`verified_fact`；
- “TSMC 2026 年已经量产 1.4nm”：`disputed`；
- “华为 2031 年达到 1.4nm 制程同等水平”：`company_statement`；
- “两者节点数字相同就代表所有物理与经济指标相同”：`disputed`。

现代节点名称不是可直接相减或按数字排序的单一物理尺寸。比较至少需要晶体管密度、性能、功耗、面积、良率、设计规则、互连、封装和成本。

## 与系统级性能的关系

华为框架明确把优化范围扩展到：

- 器件电阻、寄生电容与互连；
- 电路关键路径和布局；
- 软件、架构与芯片协同；
- 系统互联、统一编址和通信时延。

这一结构支持 [[ai-compute-system-performance-and-token-economics|AI 算力的系统级性能与 Token 经济性]] 的研究框架：芯片能力需要通过内存、互联、软件、模型和服务负载转化为有效吞吐。

但“系统级优化”不能成为跳过验证的理由。仍需分别测量：

- 单芯片和集群性能；
- 端到端延迟与吞吐；
- 功耗、面积、利用率和可用率；
- 软件适配与开发成本；
- 同模型、同精度、同工作负载结果；
- 客户部署、订单、收入、利润和现金流。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| 华为于 2026-05-25 在 IEEE ISCAS 2026 发布韬（τ）定律。 | verified_fact | 2026-05-25 | 华为新闻稿 | high | IEEE 或华为正式更正事件记录。 |
| 韬定律提出以时间缩微、LogicFolding 和多层级协同推进系统演进。 | company_statement | 2026-05-25 | 华为对自身框架的定义 | high | 华为撤回或实质修改框架定义。 |
| 华为过去六年设计并量产 381 款相关芯片。 | company_statement | 2026-05-25 | 华为新闻稿 | medium | 公司更正，或逐产品证据不支持范围与量产定义。 |
| 2026 年秋季麒麟芯片将采用 LogicFolding。 | company_statement | 2026-05-25 | 华为产品计划 | medium | 产品未发布、未采用或公司修改计划。 |
| 2031 年高端芯片密度将达到 1.4nm 制程同等水平。 | company_statement | 2026-05-25 | 华为路线图 | low | 路线图取消、延期或独立测量不支持。 |
| “1.4nm 同等密度”等于已拥有完整 1.4nm 制造工艺和同等性能/功耗/成本。 | disputed | 2026-05-25 | 等效密度与完整工艺及经济性不是同一指标 | high | 公司公开完整工艺、良率、性能、功耗和成本并获独立验证。 |
| TSMC A14 在 2026 年已经量产。 | disputed | 2026-06-09 | TSMC 年报计划 2028 年量产 | high | TSMC 正式提前量产并更正路线图。 |
| 韬定律发布足以证明相关芯片已经形成订单、收入和利润。 | disputed | 2026-06-09 | 发布、产品、订单、交付和财务是不同证据阶段 | high | 公司财报逐项确认商业化传导。 |

## 投资相关性

该事件提高以下方向的研究优先级：

- 逻辑折叠、3D 集成和先进封装；
- 片上和系统互联；
- EDA、物理设计、验证与测试；
- 软件/架构/芯片协同；
- 超节点、统一内存语义和系统级 AI 计算；
- 相关制造、设备、材料和封装能力。

证据链仍应保持：

> 技术发布 → 论文/设计规则 → prototype → tape-out → 流片 → 良率 → 量产 → 客户部署 → 订单 → 交付 → 收入 → 利润与现金流

华为是非上市公司；本 Event 也不自动映射到任何供应商上市证券。没有订单、份额、财务和当前估值时，不能从发布事件直接形成交易结论。

## 下一步核验

- IEEE ISCAS 2026 论文、演讲材料或同行评审记录；
- 381 款芯片的清单、期间、设计归属和量产定义；
- 2026 年秋季麒麟产品的正式型号、发布时间和 LogicFolding 证据；
- 晶体管密度、性能、功耗、面积、良率与成本测试；
- LogicFolding 所需 EDA、制造、封装和测试流程；
- 系统级吞吐、延迟、能效与独立 benchmark；
- 供应链认证、订单、交付和财务披露；
- 2031 路线图的年度里程碑和变更。

## 证据缺口与失效条件

1. 当前主要公开证据来自华为自身发布，缺少独立复现和产品级拆解。
2. “381 款”缺少可公开审计的完整清单。
3. “1.4nm 同等水平”只指公司所称晶体管密度，不等于完整制程或经济性。
4. 2026 年秋季和 2031 年均为未来里程碑，应按期复核而非提前标记完成。
5. 节点名称跨厂商不可直接作为物理尺寸或全面性能排序。
6. 若公司更正产品计划、技术定义或路线图，应更新状态和证据分类。

## 关联页面

- [[2026-06-09-china-semiconductor-frontier-innovation-and-inference|从变化中看到确定性：中国半导体前沿创新与推理需求（2026-06-09）]]
- [[ai-compute-system-performance-and-token-economics|AI 算力的系统级性能与 Token 经济性]]
- [[taiwan-semiconductor-manufacturing|Taiwan Semiconductor Manufacturing Co., Ltd.（TSMC）]]
