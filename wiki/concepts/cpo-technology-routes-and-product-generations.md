---
page_type: concept
subject: "CPO 技术路线与产品代际"
aliases: ["CPO product roadmap", "Optical I/O roadmap"]
tags: [technology, cpo, optical-io, product-roadmap]
tickers: ["NASDAQ:AVGO", "NASDAQ:CSCO", "NASDAQ:INTC", "NASDAQ:MRVL"]
markets: [US]
asset_classes: [equity]
industries: [semiconductors, optical-components, data-center-networking]
themes: [AI infrastructure, co-packaged optics, optical-io]
as_of: 2026-07-28
sources:
  - "[[broadcom-200g-lane-cpo-2025-05-15|Broadcom 第三代 200G/lane CPO（2025-05-15）]]"
  - "[[cisco-cpo-system-ofc-2023-03-07|Cisco OFC 2023 CPO 系统演示（2023-03-07）]]"
  - "[[marvell-1-6t-silicon-photonics-light-engine-2025-03-31|Marvell 1.6T 硅光光引擎（2025-03-31）]]"
  - "[[intel-fully-integrated-optical-io-chiplet-2024-06-26|Intel 全集成 Optical I/O Chiplet（2024-06-26）]]"
  - "[[ayar-labs-teraphy-validation-three-generations-2025-08-28|Ayar Labs TeraPHY 三代工程验证（2025-08-28）]]"
  - "[[ayar-labs-teraphy-optical-io-chiplet-2026-07-28|Ayar Labs TeraPHY Optical I/O Chiplet 产品页快照（2026-07-28）]]"
created: 2026-07-28
updated: 2026-07-28
---

# CPO 技术路线与产品代际

## 核心结论

CPO 不是单一产品，也不是按带宽数字顺序替代的统一市场。至少要同时区分：

1. **系统位置**：pluggable、LPO/LRO、on-board optics、switch CPO、XPU optical I/O；
2. **通道速率**：100G、200G、未来 400G per lane；
3. **聚合带宽**：1.6T、3.2T、4T、6.4T、8T 等；
4. **光源架构**：external/disaggregated laser 与 integrated/on-chip laser；
5. **调制与传输**：NRZ/PAM4、MRM/MZM、WDM 波长数、单模/多模；
6. **商业阶段**：设计、prototype、demo、sampling、EVT、DVT、production、customer deployment、revenue。

因此，任何公司估值都必须先把“产品是什么、处于哪一阶段、服务哪个网络层级”归一化。

## 分层产品路径

| 路线 | 光学位置 | 主要用途 | 可维护性与价值池 | 当前一手证据示例 |
|---|---|---|---|---|
| Retimed pluggable | 面板可插拔模块 | 通用前面板网络 | 模块独立更换；DSP/retimer 与模块装配保留价值 | 既有主流架构，本轮不作份额判断 |
| LPO/LRO | 面板模块或邻近板级位置，减少重定时 | 800G/1.6T 前面板或短距连接 | 部分 DSP 价值被压缩；线性 driver/TIA、SiPh engine 和系统调优增加 | Marvell 1.6T engine sampling |
| On-board optics/NPO | 光引擎位于 PCB、靠近 ASIC | 中间集成形态 | 电气距离缩短，但板级故障域与维修成本扩大 | Marvell 称其 engine 可直接系统集成 |
| Switch CPO | 光引擎与交换 ASIC 同封装或同基板 | 高端 scale-out 网络 | 光引擎、FAU、ELS、先进封装与系统集成成为核心 | Cisco 2023 demo；Broadcom Gen 2–3 |
| XPU optical I/O | optical I/O chiplet 与 CPU/GPU/XPU 共封装 | scale-up、memory/computing fabric | 价值靠近高价值计算封装，良率和故障影响更敏感 | Intel OCI prototype；Ayar EVT/DVT |

这些路线可能长期并存；从 LPO 送样不能直接推导 switch CPO 收入，从 switch CPO 生产也不能直接推导 XPU optical I/O 商业化。

## 带宽层级不能混用

| 指标 | 含义 | 常见误读 |
|---|---|---|
| `G/lane` | 单条电/光通道速率，如 100G/200G | 误当成完整 engine 或 system 带宽 |
| `1.6T/3.2T/6.4T engine/tile` | 单光引擎或 optical tile 聚合能力 | 误当成交换机总容量 |
| `4T/8T bidirectional chiplet` | optical I/O chiplet 双向带宽口径 | 与单向模块带宽直接比较 |
| `51.2T/102.4T switch` | 交换 ASIC 或整机交换容量 | 误当成单一光模块产品版本 |
| wavelengths/fiber | 每纤 WDM 波长数 | 只看数量而忽略符号率、编码、FEC 与链路预算 |

估值模型必须为每个数字保留方向、端口、lane、wavelength、fiber、距离和 FEC 口径。

## 厂商公开代际映射

| 公司 | 公开代际或产品 | 截止日状态 | 证据类型 | 估值边界 |
|---|---|---|---|---|
| Broadcom | Gen 1 TH4–Humboldt | 2021 供应链学习周期 | company_statement | 研发/制造学习，不等于成熟利润 |
| Broadcom | Gen 2 TH5–Bailly 100G/lane | 公司称 volume production | company_statement | 需客户部署、出货和收入交叉验证 |
| Broadcom | Gen 3 200G/lane | 2025 product-line announcement | verified_fact / company_statement | 产品发布不等于订单 |
| Broadcom | Gen 4 400G/lane | roadmap commitment | company_statement | 不纳入确定性收入 |
| Cisco | G100 + 3.2T optical tile | OFC 2023 system demo | verified_fact / company_statement | demo 不等于量产 |
| Marvell | 1.6T 8×200G DR8 engine | 2025 select-customer sampling | company_statement | 属 LPO/on-board 路线；不并入 6.4T CPO 收入 |
| Marvell | 6.4T CPO engine | OFC 2024 demo 的前代参照 | company_statement | 需正式产品和客户状态 |
| Intel | 4Tbps bidirectional OCI | OFC 2024 working prototype | verified_fact / company_statement | 不证明商业化 |
| Ayar Labs | TeraPHY 2T→4T→8T | demo→EVT/DVT；公开规格 preliminary | company_statement | 私营公司，缺量产与财务数据 |

## 商业阶段证据阶梯

```text
architecture/design
→ prototype
→ public demo
→ sampling
→ wafer sort / EVT
→ DVT / system integration
→ technical certification
→ formal order
→ delivery
→ recognized revenue
→ gross profit and cash flow
```

每个箭头都需要独立证据。`volume production` 或 `in production` 也不能替代客户数量、产量、ASP、收入和现金回款。

## 为什么影响估值

| 技术变量 | 对收入的影响 | 对利润/现金流的影响 | 对倍数的影响 |
|---|---|---|---|
| system route | 决定 serviceable TAM 与导入时间 | 决定替代既有 pluggable/DSP 的程度 | 路线确定性越低，概率折价越高 |
| lane rate/engine bandwidth | 改变端口密度、engine 数量与 ASP 路径 | 影响 die、封装、测试和散热复杂度 | 只升级带宽、未改善良率时不应扩张倍数 |
| external vs integrated laser | 改变 ELS/PIC 的价值池归属 | 影响冗余、维修、耦合与复合良率 | 可维护性和多源采购影响风险溢价 |
| WDM 与调制器路线 | 改变 wavelength/channel 数和链路能力 | 增加热调谐、控制、测试或封装成本 | 专有 IP 与量产 know-how 可能形成壁垒 |
| product stage | 决定收入概率与折现期 | 试产常伴随低利用率和高报废 | demo/roadmap 应使用高概率折价 |
| standards/multisourcing | 可能加速生态采用 | 也可能压低 ASP 与议价权 | TAM 扩大与份额/毛利稀释需同时建模 |

## 关键监控指标

- 每条路线分别统计 customer qualification、formal order、delivery、recognized revenue。
- 100G/200G/400G per lane 对 engine 数、功耗和端口密度的实际变化。
- LPO/on-board、switch CPO、XPU optical I/O 的独立 TAM 与 route mix。
- wafer sort、known-good-die、EVT/DVT、package yield 和 system yield。
- ELS 与 integrated laser 的采用比例、冗余方式、现场可替换性和 RMA。
- 产品带宽、距离、FEC、pJ/bit 的统一测试边界。

## 失效条件

- 可插拔、铜互连或板级光学在目标速率仍有更优 TCO。
- 200G/400G lane 的良率、热或信号完整性无法规模达标。
- XPU optical I/O 长期停留在 prototype/validation。
- 标准化导致价值池增长但单一供应商份额和毛利显著下降。
- 公开路线图持续延迟，且没有客户订单、交付或收入证据。

## 关联

- [[co-packaged-optics|共封装光学（CPO）]]
- [[cpo-optical-engine-components-cost-and-margin|CPO 光引擎组成、成本与利润]]
- [[cpo-commercialization-evidence-stages|CPO 商业化证据分层]]
- [[cpo-product-architecture-cost-and-margin-model-2026-2031|CPO 产品架构、成本与利润模型（2026–2031）]]
