---
page_type: concept
subject: "AI 算力的系统级性能与 Token 经济性"
aliases:
  - "AI 系统级算力"
  - "Token 经济性"
  - "AI Compute System Performance and Token Economics"
  - "Prefill/Decode 分离"
tags:
  - artificial-intelligence
  - ai-inference
  - system-performance
  - token-economics
  - prefill-decode
  - benchmarking
tickers: []
markets:
  - GLOBAL
  - CN
  - US
asset_classes:
  - equity
industries:
  - artificial-intelligence
  - semiconductor
  - cloud-computing
  - data-center
themes:
  - ai-compute
  - inference-economics
  - system-co-design
  - cluster-interconnect
  - workload-normalization
as_of: 2026-07-29
sources:
  - "[[2026-06-09-china-semiconductor-frontier-innovation-and-inference|从变化中看到确定性：中国半导体前沿创新与推理需求（2026-06-09）]]"
  - "https://docs.nvidia.com/dynamo/dev/user-guides/disaggregated-serving"
  - "https://docs.nvidia.com/aiperf/dev/reference/effective-vs-active-metrics"
  - "https://www.nda.gov.cn/sjj/ywpd/sjzy/0429/20260429164803571173880_pc.html"
  - "https://e.huawei.com/cn/products/computing/ascend/atlas-900-a3-superpod"
  - "https://www.huawei.com/cn/news/2026/5/ieee-iscas-tau-scaling"
created: 2026-07-29
updated: 2026-07-29
---

# AI 算力的系统级性能与 Token 经济性

## 定义

AI 算力的可用价值不能只由单颗芯片的峰值 FLOPS、TOPS 或制程节点决定。真实服务能力来自以下层级的联合结果：

> 芯片 → 内存与互联 → 节点/超节点 → 集群 → 编译器与推理框架 → 模型与工作负载 → 服务等级 → 有效 Token → 收入、利润与现金流

“Token 经济性”是指在明确模型质量和服务等级约束下，生产单位有效输入或输出 Token 所需的全生命周期成本及其可变现价值。它不是把 Token 数量机械等同于芯片需求或营业收入。

## 为什么单芯片指标不够

单芯片峰值规格通常不能回答：

- 多卡扩展时有多少算力消耗在通信、同步和重算；
- 内存容量、带宽与 KV cache 是否成为瓶颈；
- 编译器、算子和框架是否能达到理论利用率；
- 模型精度、稀疏性、量化和批处理是否一致；
- 长上下文、长输出、高并发和低延迟如何改变吞吐；
- 功耗、冷却、机房、故障与运维成本是多少；
- 用户实际需要的准确率、TTFT 和 TPOT 是否达标。

因此，单卡落后不必然意味着系统服务落后；超节点峰值领先也不必然意味着单位有效 Token 成本领先。

## 系统性能分层

| 层级 | 典型指标 | 常见误读 | 必要补充 |
|---|---|---|---|
| 芯片 | 峰值 FLOPS/TOPS、精度、HBM 带宽、功耗 | 节点名称或峰值越高，所有负载越快 | 实测利用率、模型、精度、稀疏性、内存与算子 |
| 节点 | 卡数、节点吞吐、局部带宽、内存容量 | 卡数增加可线性扩展 | 拓扑、通信开销、同步、故障和功率 |
| 超节点/集群 | 总 PFLOPS、bisection bandwidth、并行效率 | 不同卡数和精度的峰值可直接比较 | 同负载 scale-up/scale-out 效率、尾延迟和可用率 |
| 软件栈 | 编译器、kernel、runtime、调度和框架 | 硬件规格足以决定性能 | 算子覆盖、模型适配、版本、维护和开发成本 |
| 模型/负载 | 参数量、MoE、上下文、输入/输出长度、batch | 一个 benchmark 可代表所有业务 | 模型质量、请求分布、缓存命中、并发和 SLA |
| 服务 | TTFT、TPOT、吞吐、p95/p99、可用率 | 平均 Tokens/s 等于用户体验 | 负载下延迟、排队、故障恢复和服务降级 |
| 经济性 | 单位 Token 成本、价格、毛利、利用率 | Token 数增长等比例变成利润 | 降价、效率、资本开支、折旧、电力、竞争和客户付费 |

## Prefill 与 Decode

大语言模型推理通常分为两个主要阶段：

1. **Prefill**：处理输入提示词并生成初始 KV cache。通常对输入长度和计算吞吐更敏感。
2. **Decode**：基于 KV cache 逐步生成输出 Token。通常更受内存带宽、并发序列、输出长度和 KV cache 容量约束。

NVIDIA Dynamo 文档将两阶段描述为不同的计算与内存压力，并允许分别部署资源池。分离可能带来：

- 按不同瓶颈配置硬件和并行方式；
- 避免长提示词 Prefill 阻塞持续 Decode；
- 分别扩容，以满足 TTFT 和 TPOT 目标；
- 在动态负载中提高资源利用率。

分离也会引入：

- KV cache 在节点间传输的网络和时延成本；
- 路由、排队、调度和负载预测复杂度；
- 额外故障域与运维成本；
- 缓存命中、短提示词或低并发场景下的反效果。

因此，“Prefill/Decode 分离”是一种系统设计选择，不是任何负载下都成立的固定优势。

## Token 成本框架

可用如下结构组织研究，而不是把它当作现成估值公式：

```text
单位有效输出 Token 成本
=（计算设备年化成本
  + 网络、存储和机房年化成本
  + 电力、冷却和运维
  + 软件、适配和调度成本
  + 故障、重算和闲置成本）
 ÷ 满足质量与服务等级的有效输出 Token
```

“有效”要求同时满足：

- 指定模型、版本和质量/准确率；
- 指定输入与输出长度分布；
- 指定 TTFT、TPOT、吞吐和 p95/p99 延迟；
- 指定可用率、故障恢复和数据安全要求；
- 排除缓存重复计量、失败请求、无效生成和测试流量。

若研究商业回报，还需单独记录：

```text
Token 毛利
= 客户实际支付的 Token/订阅/任务收入
 - 对应推理服务成本
```

固定订阅、广告、Agent 任务收费和内部效率收益不能直接按公开 API Token 单价折算。

## 跨平台比较清单

比较两个 AI 平台前，至少统一：

| 维度 | 最低要求 |
|---|---|
| 模型 | 相同模型、权重、版本和精度目标 |
| 硬件 | 芯片型号、数量、时钟、内存、互联和拓扑 |
| 数值格式 | FP32/FP16/BF16/FP8/INT8/INT4、稀疏性和累计精度 |
| 软件 | 驱动、编译器、框架、kernel、推理引擎和版本 |
| 工作负载 | 输入/输出长度、batch、并发、上下文和请求分布 |
| 服务指标 | TTFT、TPOT、throughput、p95/p99 和可用率 |
| 能耗 | 芯片、节点、网络、冷却及全系统功率 |
| 经济成本 | 采购/租赁、折旧、机房、电力、软件、人员与维护 |
| 质量 | 任务准确率、拒答率、幻觉率或业务成功率 |
| 时间 | 测试日期、软件版本和产品状态 |

缺少其中关键项时，跨平台倍数应分类为 `company_statement` 或 `source_opinion`，而不是 `verified_fact`。

## CloudMatrix 384 与 NVL72 的案例

[[2026-06-09-china-semiconductor-frontier-innovation-and-inference|来源课程]]称：

- Ascend 910C 单卡性能约为 GB200 的三分之一；
- CloudMatrix 384 的集群性能约为 NVL72 的 1.7 倍；
- 因而系统级创新可以弥补单芯片差距。

华为产品资料确认 Atlas 900 A3 SuperPoD 最大支持 384 张 NPU，并给出约 307.2/288.7 PFLOPS@FP16、互联和内存规格。该资料可以确认厂商规格，不足以确认“所有训练/推理负载比 NVL72 快 1.7 倍”。

比较仍需统一：

- 384 张 NPU 与 72 张 GPU 的设备数量；
- FP16、FP8、稀疏性和累计精度；
- 模型、batch、上下文和输出长度；
- 训练收敛、推理准确率与端到端延迟；
- 全系统功耗、占地、可用率和利用率；
- 软件适配和迁移成本。

因此：

- “华为公布了 384 NPU 超节点及其规格”：`company_statement`；
- “峰值规格显示系统级扩展可以提高总算力”：`codex_inference`；
- “CloudMatrix 384 对所有任务都比 NVL72 快 1.7 倍”：`disputed`。

## Token 增长如何传导

国家数据局记录，2025 年用于 AI 训练和推理的数据总量为 199.48 EB，推理数据量 101.34 EB，首次超过训练数据量；全年 Token 调用量约 21,100tn。该数据提高了推理基础设施的研究优先级，但从 Token 到投资回报至少经过：

> 调用量 → 付费比例 → 单价/套餐 → 模型效率 → 计算需求 → 平台利用率 → 云/设备收入 → 毛利 → CAPEX 与折旧 → 自由现金流 → 估值

可能造成脱钩的因素包括：

- 模型压缩、蒸馏、量化和 speculative decoding；
- prefix/KV cache、批处理和流量调度；
- API 降价、免费额度、内部调用和无收入测试流量；
- 芯片代际提升与单位 Token 能耗下降；
- 云厂商自研芯片和供应商议价；
- 过度建设导致的低利用率；
- 应用无法形成用户付费或企业 ROI。

Token 调用量是需求和采用指标，不是独立的收入、利润或估值指标。

## 关键论断

| 论断 | 证据类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
| AI 服务性能由芯片、内存、互联、软件、模型和负载共同决定。 | verified_fact | 2026-07-29 | NVIDIA 系统部署文档与华为系统架构资料 | high | 独立测试长期显示单一芯片峰值足以解释所有端到端服务性能。 |
| Prefill 与 Decode 具有不同的资源和调度特征。 | verified_fact | 2026-07-29 | NVIDIA Dynamo/AIPerf 文档 | high | 主流模型架构和服务实现不再存在这两个阶段或资源差异。 |
| Prefill/Decode 分离在所有负载下都降低成本和延迟。 | disputed | 2026-07-29 | 分离还受输入长度、并发、缓存命中、KV 传输和调度影响 | high | 全负载范围的同口径测试支持无条件优势。 |
| 峰值 PFLOPS 可以直接代表单位有效 Token 成本。 | disputed | 2026-07-29 | 峰值不包含利用率、服务等级、能耗、软件和资本成本 | high | 真实服务数据证明这些因素可忽略且峰值与成本稳定一一对应。 |
| 2025 年中国 AI 推理数据量首次超过训练数据量。 | verified_fact | 2025-12-31 | 国家数据局 | high | 调查口径或结果被正式修订。 |
| Token 调用量增长必然等比例增加芯片收入和股票回报。 | disputed | 2026-07-29 | 中间受效率、价格、利用率、竞争、利润和估值影响 | high | 公司级长期数据证明稳定等比例传导。 |
| 在统一质量和 SLA 后，用单位有效 Token 全生命周期成本比较平台更接近经济价值。 | codex_inference | 2026-07-29 | 本页分层框架 | medium | 目标业务主要由 Token 之外的稀缺资源或收入模式决定。 |

## 投资研究应用

该框架可用于：

- 评价单卡、超节点、集群和推理服务的可比性；
- 拆解 GPU/NPU、HBM、网络、光互连、服务器、云与应用的价值分配；
- 评估 Token 增长是否真正转化为设备、云收入和现金回报；
- 区分性能发布、客户测试、订单、部署、利用率和财务兑现；
- 检查公司是否用不统一精度、功耗或工作负载制造性能倍数。

它不能单独回答：

- 哪个芯片或平台在所有负载下最好；
- 哪家公司会获得订单或利润；
- 当前股价是否便宜；
- 某个技术发布是否会按期量产；
- Token 增长是否足以覆盖 CAPEX。

## 监测指标

- Prefill 与 Decode 的吞吐、TTFT、TPOT 和 p95/p99。
- 集群 scale-up/scale-out 效率和通信占比。
- HBM/内存容量、带宽、KV cache 命中率和传输开销。
- 真实模型、上下文、输出长度与并发分布。
- 有效 Token 数、付费 Token 比例和净实现价格。
- 设备采购/租赁、折旧、电力、冷却、软件和运维成本。
- 可用率、故障率、重算、闲置和利用率。
- 云收入、毛利、CAPEX、折旧、营业现金流和 FCF。
- 客户测试、部署、订单、交付和收入确认。

## 证据缺口与失效条件

- 不同厂商很少公开同模型、同精度、同功耗、同服务等级的完整基准。
- 峰值规格、实验室 benchmark 与生产环境利用率之间缺少稳定换算。
- 公开 Token 统计可能包含内部调用、免费调用、缓存和重复计量。
- Token 单价持续变化，订阅、广告、Agent 任务和内部生产率没有统一计价。
- 厂商较少披露推理服务的单位成本、折旧、能耗和真实毛利。
- 若用于公司或证券判断，必须结合最新订单、财报、资本结构、估值、上市规则和当前价格。

## 关联页面

- [[2026-06-09-china-semiconductor-frontier-innovation-and-inference|从变化中看到确定性：中国半导体前沿创新与推理需求（2026-06-09）]]
- [[2026-05-25-huawei-presents-tau-scaling-law|华为发布韬（τ）定律（2026-05-25）]]
- [[ai-data-center-interconnect-architecture|AI 数据中心互连架构]]
- [[hyperscaler-ai-capex-roi-monitoring-model-2026|Hyperscaler AI CAPEX—ROI 监测模型（2026）]]
- [[ai-compute-supply-capacity-revenue-bridge-2026-2028|AI 算力供给容量—收入桥（2026–2028）]]
