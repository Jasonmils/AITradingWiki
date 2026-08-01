# Log

Chronological record of all operations.

## 2026-07-23 setup | Vault initialized
Created vault "AI Trading Wiki" for investment and trading research. Configured Codex with `AGENTS.md` and four repository-scoped Second Brain skills.

## 2026-07-24 setup | Equity research schema upgraded
Added Event and Model layers, six canonical templates, evidence classification, and the repository-scoped `equity-research` skill. Existing sources, pages, index entries, and prior log entries were preserved.

## 2026-07-24 ingest | Goldman Sachs Global Tech Optical Networking
Processed `raw/CPO-report-GoldmanSachs.pdf`. Created: [Goldman Sachs Global Tech Optical Networking (2026-04-17), NVIDIA Corporation, Broadcom Inc., Marvell Technology Inc., Co-Packaged Optics, AI Data Center Interconnect Architecture, Silicon Photonics and Optical Light Sources, Optical Circuit Switch, CPO Switch Commercialization Roadmap 2025–2027, Goldman Sachs AI Optical Networking TAM and CPO Adoption Model 2026–2028E]. Updated: [`wiki/index.md`]. Evidence risks: third-party sell-side opinions and model assumptions; product roadmaps and company data not checked against primary sources; visible page/exhibit gaps; internal unit, penetration and BoM inconsistencies preserved as disputed.

## 2026-07-24 maintenance | Wiki 中文优先规则与 CPO 摄入页面本地化
新增中文优先规则并更新六个 canonical 模板；将本次 CPO 报告摄入形成的 10 个 Wiki 页面及索引展示文本改为中文。保留英文公司法定名称、证券代码、证据类型枚举、单位及 CPO、OCS、ASIC、XPU、DSP、BoM、TAM 等专有名词；数字、页码、来源、置信度和证据边界未改变。

## 2026-07-26 ingest | 中国商业航天：雄心与软肋
处理 `raw/26.07.14-第十二课.mp4`。创建：[[2026-07-14-china-commercial-space-ambition-and-weakness|中国商业航天：雄心与软肋（2026-07-14）]]、[[commercial-space-business-loop|商业航天商业闭环与付费客户]]、[[reusable-rocket-economics-and-recovery-paths|可复用火箭经济性与回收路径]]、[[china-commercial-space-scale-up-and-bottlenecks|中国商业航天规模化能力与产业软肋]]、[[space-computing-economics|太空算力的适用边界与工程经济性]]。更新：[`wiki/index.md`]。证据风险：ASR、OCR、说话人分离和 DeepSeek 精炼均属派生证据；课程包含非公开交流线索、时效敏感的 IPO/估值/发射论断和未经一手核验的统计口径；未创建 Event、Entity、Model、Synthesis 或当前交易判断。

## 2026-07-26 maintenance | 长征十号乙型号与回收表述校正
根据策展人校正，将 Canonical Wiki 中派生转录的“7·10 长征十号Z”统一改为“7·10 长征十号乙完成回收”。更新：[[2026-07-14-china-commercial-space-ambition-and-weakness|中国商业航天：雄心与软肋（2026-07-14）]]、[[reusable-rocket-economics-and-recovery-paths|可复用火箭经济性与回收路径]]。原始 MP4、`timeline.json`、原始 HTML 和 DeepSeek HTML 保持不变；由于尚未摄入对应官方公告，未创建已核验 Event，也未将完成回收外推为再次使用、稳定复用或航班化。

## 2026-07-26 maintenance | 视频源文件终态清理
在策展人确认完成转录与 Canonical Wiki 摄入后，删除 `raw/26.07.14-第十二课.mp4`，保留原始与 DeepSeek 精炼转录 HTML，并在 `output/video-ingest/manifests/26.07.14-第十二课-1cc28ba4571a.json` 记录源文件 SHA-256 与清理状态。同时删除该视频的本地音频、帧、OCR、时间轴及其他处理中间文件。关联来源：[[2026-07-14-china-commercial-space-ambition-and-weakness|中国商业航天：雄心与软肋（2026-07-14）]]；预计释放 2403.4 MiB。

## 2026-07-27 ingest | 矛盾和理性
处理 `raw/【买方知识圈】2026年07月20日 矛盾和理性.mp4`。创建：[[2026-07-20-contradiction-and-rationality|矛盾和理性（2026-07-20）]]。更新：[`wiki/index.md`]。证据风险：ASR、OCR、说话人分离和 DeepSeek 精炼均属派生证据；课程包含时效敏感的市场点位、监管归因、IPO、估值、盈利预测和未核验统计口径；未创建 Entity、Concept、Event、Model、Synthesis 或当前交易判断；源 MP4 继续保留。

## 2026-07-27 maintenance | 视频源文件终态清理
在策展人确认完成转录与 Canonical Wiki 摄入后，删除 `raw/【买方知识圈】2026年07月20日 矛盾和理性.mp4`，保留原始与 DeepSeek 精炼转录 HTML，并在 `output/video-ingest/manifests/买方知识圈-2026年07月20日-矛盾和理性-e56dff670fc0.json` 记录源文件 SHA-256 与清理状态。同时删除该视频的本地音频、帧、OCR、时间轴及其他处理中间文件。关联来源：[[2026-07-20-contradiction-and-rationality|矛盾和理性（2026-07-20）]]；预计释放 1767.6 MiB。

## 2026-07-27 ingest | 从涨价到扩产：半导体设备、零部件与国产算力
处理 `raw/微信视频2026-07-27_102842_648.mp4`。创建：[[2026-07-15-from-price-hikes-to-expansion|从涨价到扩产：半导体设备、零部件与国产算力]]。更新：[`wiki/index.md`]。证据风险：发布日期未知，知识截止日 2026-07-15 为根据口播事件推定；ASR、OCR、说话人分离和 DeepSeek 精炼均属派生证据；大量产能、涨价、订单、客户、市场规模、估值和国产算力路线图缺少一手底稿。美光美国投资按官方约 US$200bn 口径记录，视频 US$250bn 保留为 `disputed`。未创建 Entity、Concept、Event、Model、Synthesis 或当前交易判断；源 MP4 及全部处理中间文件继续保留。

## 2026-07-27 ingest | 说好的利空去哪儿了？
处理 `raw/26.04.28-第一节.mp4`。创建：[[2026-04-28-where-did-the-bearish-case-go|说好的利空去哪儿了？（2026-04-28）]]。更新：[`wiki/index.md`]。证据风险：课程属于宏观与资本市场观点，ASR、OCR、说话人分离和 DeepSeek 精炼均属派生证据；课程关于长期货币制度、全球秩序、外资回流和中证 500 的结论缺少可复算模型。按策展人要求，2026 年 3 月 CPI 采用国家统计局同比 1.0%、规模以上工业增加值采用国家统计局单月同比 5.7%；课程 1.2%和“6.7%或六点几”原话保留为 `disputed`。未创建 Entity、Concept、Event、Model、Synthesis 或当前交易判断；源 MP4 及全部处理中间文件继续保留。

## 2026-07-27 ingest | AI 进化论
处理 `raw/26.05.07- 第二节.mp4`。创建：[[2026-05-07-ai-evolution|AI 进化论（2026-05-07）]]。更新：[`wiki/index.md`]。证据风险：ASR、OCR、说话人分离和 DeepSeek 精炼均属派生证据；课程关于中美 AI 投资与数据中心、公司估值融资、IPO、职业替代和长期产业机会的数字或结论缺少统一口径。MegaScale 55.2% MFU 按论文限定为 175B 模型、12,288 张 GPU 的特定实验；课程所称 DeepSeek R1“US$6mn 全成本”、xAI 11% MFU 和昇腾 950 适配分别保留为 `disputed` 或 `market_rumor`。未创建 Entity、Concept、Event、Model、Synthesis 或当前交易判断；源 MP4 及全部处理中间文件继续保留。

## 2026-07-27 ingest | 官方机构 AI 报告批次（6 份）
处理并永久保留以下原始 PDF：`raw/2025-01-citi-agentic-ai-finance-do-it-for-me-economy.pdf`、`raw/2025-09-15-citi-productivity-ai-revolution.pdf`、`raw/2026-02-11-morgan-stanley-mapping-ai-rate-of-change.pdf`、`raw/2026-06-16-bofa-ai-ten-secret-ingredients.pdf`、`raw/2026-06-26-hsbc-china-bifurcated-economy-full-arc-ai.pdf`、`raw/2026-06-jpmorgan-mid-year-investment-outlook.pdf`。

创建 Source：[[citi-agentic-ai-finance-2025-01|Citi：Agentic AI 与金融业的“Do It For Me”经济]]、[[citi-productivity-ai-revolution-2025-09-10|Citi：生产率的 AI 革命]]、[[morgan-stanley-mapping-ai-rate-of-change-2026-02-11|Morgan Stanley：映射 AI 变化率]]、[[bofa-ai-ten-secret-ingredients-2026-06-16|BofA：AI 的十种秘密原料]]、[[hsbc-china-full-arc-ai-opportunity-2026-06-26|HSBC：中国分化经济中的全链条 AI 机会]]、[[jpmorgan-mid-year-investment-outlook-2026-06|J.P. Morgan Asset Management：2026 年中投资展望]]。

创建 Concept：[[agentic-ai-in-financial-services|金融服务中的 Agentic AI]]、[[ai-productivity-diffusion-and-roi|AI 生产率扩散与 ROI]]、[[ai-exposure-materiality-and-rate-of-change|AI 暴露、重要性与变化率]]、[[ai-infrastructure-critical-material-bottlenecks|AI 基础设施关键材料瓶颈]]、[[china-full-arc-ai-investment-chain|中国全链条 AI 投资链]]。创建 Model：[[citi-us-ai-productivity-scenario-2025|Citi 美国 AI 生产率情景模型（2025）]]、[[hyperscaler-ai-capex-roi-monitoring-model-2026|Hyperscaler AI CAPEX—ROI 监测模型（2026）]]。创建 Synthesis：[[ai-capex-roi-and-tradability-evidence-map-2024-2026|AI CAPEX、ROI 与可交易性证据图谱（2024–2026）]]。更新：[`wiki/index.md`]。

证据风险：多份文件为主题研究、资产管理或私人银行观点，并非统一口径的独立股票研究；Citi 生产率报告与 BofA 报告为公开删节版，HSBC 仅 3 页；Morgan Stanley 约 3,600 只股票映射依赖分析师调查；J.P. Morgan 的 CAPEX、EPS 和盈利增长为时效敏感的一致预期。未将模型假设、市场共识或来源观点升级为事实；未因公司名单批量创建 Entity，也未把报告发布日期创建为 Event。由于尚未复核当前价格、最新财报、公司级估值与催化剂，本批次未形成即时交易结论。

## 2026-07-27 ingest | CPO 公司增长与估值官方来源包（31 份）
处理并永久保留 `output/cpo-valuation-source-pack-2026-07-27.md` 所列 31 份官方原件（28 份 PDF、3 份 HTML，共 1,983 个 PDF 页面）。创建 31 个 Source 页面；新增 Entity：[[coherent|Coherent Corp.]]、[[lumentum|Lumentum Holdings Inc.]]、[[fabrinet|Fabrinet]]、[[tfc-communication|天孚通信]]、[[innolight|中际旭创]]、[[robotechnik-ficontec|罗博特科与 ficonTEC]]；更新 [[nvidia|NVIDIA Corporation（英伟达）]]、[[broadcom|Broadcom Inc.（博通）]]、[[marvell-technology|Marvell Technology, Inc.（迈威尔科技）]]。

创建 Concept：[[cpo-commercialization-evidence-stages|CPO 商业化证据分层]]、[[cpo-value-chain-and-company-exposure|CPO 价值链与公司暴露度]]、[[cpo-reliability-and-external-laser-source|CPO 可靠性与外置激光源（ELS）]]、[[cpo-customer-concentration-and-revenue-double-counting|CPO 客户集中度与产业链重复计量]]；更新 [[co-packaged-optics|共封装光学（CPO）]]。创建/更新 Event：[[cpo-switch-commercialization-roadmap-2025-2027|CPO 交换机商业化路线图（2025–2027）]]、[[marvell-celestial-ai-acquisition-2025-2026|Marvell 收购 Celestial AI（2025–2026）]]、[[coherent-nvidia-strategic-partnership-2026|NVIDIA 与 Coherent 战略合作（2026）]]、[[robotechnik-ficontec-consolidation-2025|罗博特科并表 ficonTEC（2025）]]。

创建 Model：[[cpo-industry-volume-value-model-2026-2031|CPO 行业量价与价值池模型（2026–2031）]]、[[cpo-company-financial-baseline-2025-2026|CPO 公司财务基线与资本结构（2025–2026）]]、[[cpo-company-growth-and-valuation-scenarios-2027-2031|CPO 公司增长与估值情景（2027–2031）]]；创建 Synthesis/Monitoring：[[cpo-company-comparison-consensus-and-non-consensus-2026|CPO 公司比较：共识、非共识与估值边界（2026）]]、[[cpo-commercialization-and-valuation-monitoring-2026|CPO 商业化与估值监测清单（2026）]]；更新 `wiki/index.md`。

证据风险：所有覆盖公司均未在监管财报中单列 CPO 收入；`volume production`、`in production`、生态合作、采购承诺、在手订单、交付、客户部署、收入、利润和现金流保持分层。Goldman、Coherent 与 Lumentum 的 TAM/SAM 定义不一致，模型仅作为 `model_assumption` 压力测试。Lumentum 本地 PDF 文件名含 Q3 但正文为 FY2026 Q2，已保留不可变原件并另摄入真实 Q3 10-Q。2026-07-27 无法从统一可靠行情源取得全部公司同一时点的现价与 EV，因此未形成目标价或当前交易结论。

## 2026-07-27 ingest | A股市场回顾：涅槃之路，新生之机
处理 `raw/26.05.12-第三节.mp4`。创建：[[2026-05-12-a-share-market-rebirth-and-slow-bull|A股市场回顾：涅槃之路，新生之机（2026-05-12）]]、[[market-capitalization-to-gdp-ratio|证券化率与市值/GDP指标]]、[[2024-04-12-capital-market-new-nine-guidelines|2024年资本市场“新国九条”发布]]。更新：[`wiki/index.md`]。证据风险：ASR、OCR、说话人分离和 DeepSeek 精炼均属派生证据；课程内 A 股总市值同时出现约 117、120、123、140/141.2 万亿元等冲突口径，沪深近日期官方数据只支持约 116.49 万亿元（尚未包含北交所）；证券化率固定阈值和“慢牛”属于课程观点；“五大顶部信号”仅有六个事后选择样本，缺少可复算规则和样本外检验。采用国务院 2024-04-12 公开发布“新国九条”的官方口径；未创建 Entity、Model、Synthesis 或当前交易判断；源 MP4 及全部处理中间文件继续保留。

## 2026-07-28 ingest | CPO 技术路线、产品代际与单位经济性官方来源包（7 份）
处理并永久保留 `raw/2021-06-04-cw-wdm-msa-technical-specifications-rev-1-0.pdf`、`raw/2024-06-26-intel-fully-integrated-optical-io-chiplet.pdf`、`raw/2023-03-07-cisco-cpo-system-ofc-2023.html`、`raw/2025-03-31-marvell-1-6t-silicon-photonics-light-engine.html`、`raw/2025-08-28-ayar-labs-teraphy-three-generations-validation.html`、`raw/2026-07-28-ayar-labs-teraphy-optical-io-chiplet.html`、`raw/2026-07-28-ayar-labs-supernova-light-source.html`。

创建 7 个 Source：[[cw-wdm-msa-technical-specifications-rev-1-0|CW-WDM MSA 技术规范 Rev 1.0（2021-06-04）]]、[[intel-fully-integrated-optical-io-chiplet-2024-06-26|Intel 全集成 Optical I/O Chiplet（2024-06-26）]]、[[cisco-cpo-system-ofc-2023-03-07|Cisco OFC 2023 CPO 系统演示（2023-03-07）]]、[[marvell-1-6t-silicon-photonics-light-engine-2025-03-31|Marvell 1.6T 硅光光引擎（2025-03-31）]]、[[ayar-labs-teraphy-validation-three-generations-2025-08-28|Ayar Labs TeraPHY 三代工程验证（2025-08-28）]]、[[ayar-labs-teraphy-optical-io-chiplet-2026-07-28|Ayar Labs TeraPHY Optical I/O Chiplet 产品页快照（2026-07-28）]]、[[ayar-labs-supernova-light-source-2026-07-28|Ayar Labs SuperNova 多波长光源产品页快照（2026-07-28）]]；更新 [[broadcom-200g-lane-cpo-2025-05-15|Broadcom 第三代 200G/lane CPO（2025-05-15）]]。

创建 Entity：[[cisco-systems|Cisco Systems, Inc.（思科）]]、[[intel-corporation|Intel Corporation（英特尔）]]、[[ayar-labs|Ayar Labs]]；更新 [[broadcom|Broadcom Inc.（博通）]]、[[marvell-technology|Marvell Technology, Inc.（迈威尔科技）]]。创建 Concept：[[cpo-technology-routes-and-product-generations|CPO 技术路线与产品代际]]、[[cpo-optical-engine-components-cost-and-margin|CPO 光引擎组成、成本与利润]]；更新 [[co-packaged-optics|共封装光学（CPO）]]、[[silicon-photonics-and-optical-light-sources|硅光与光学光源]]、[[cpo-reliability-and-external-laser-source|CPO 可靠性与外置激光源（ELS）]]。创建 Model：[[cpo-product-architecture-cost-and-margin-model-2026-2031|CPO 产品架构、成本与利润模型（2026–2031）]]；更新行业价值池、公司增长估值、商业化路线图、公司比较与监测页面及 `wiki/index.md`。

证据风险：除 CW-WDM/OIF 的标准定义外，性能、功耗、可靠性、成本优势和产品阶段主要是 `company_statement`；demo、prototype、sampling、EVT/DVT、production、customer deployment、recognized revenue、profit/FCF 保持分层。公开来源没有可审计的 CPO 单品 ASP、BoM、composite yield、RMA 或毛利，模型输入均保留为 `model_assumption`。LPO/on-board、switch CPO 与 XPU optical I/O 使用独立 TAM/概率；integrated/external laser 与 pluggable/DSP 替代影响不得重复计量；未形成当前价格交易结论。

## 2026-07-28 ingest | 从一五计划到十五五规划：读懂中国政策的逻辑
处理 `raw/26.05.19-第四节.mp4`。创建：[[2026-05-19-from-first-five-year-plan-to-fifteenth-five-year-plan|从一五计划到十五五规划：读懂中国政策的逻辑（2026-05-19）]]、[[china-policy-document-reading-framework|中国政策文件的层级、传导与阅读框架]]、[[2026-03-12-fifteenth-five-year-plan-approved|十五五规划纲要获全国人大批准（2026-03-12）]]。更新：[`wiki/index.md`]。证据风险：ASR、OCR、说话人分离和 DeepSeek 精炼均属派生证据；课程把十五五第五项原则说成“系统观念加守正创新”并遗漏官方第六项“统筹发展和安全”，把官方八项战略性新兴产业口播为七项并混入低空经济；新加坡人均 GDP 为美国 1.6 倍、全球减贫算术、外国代表团和巴厘岛购物中心等说法缺少同口径或一手支持。按全国人大规划纲要、2026-04-28 政治局会议通稿和世界银行同口径资料记录；未创建 Entity、Model、Synthesis 或当前交易判断；源 MP4 及全部处理中间文件继续保留。

## 2026-07-28 ingest | P0 云厂商与算力供应链官方披露资料包（43 份）
处理并永久保留 `output/p0-cloud-compute-official-materials-phase1-2026-07-28.md` 所列 43 份官方原件，覆盖 Microsoft、Alphabet、Amazon、Meta、Oracle、NVIDIA、AMD、TSMC、Micron、ASML 与 Applied Materials。所有原件保留在 `raw/`，已完成 SHA-256 复核；未使用第三方电话会文字稿。

创建 11 个 Source pack：[[microsoft-fy2026-q3-official-source-pack|Microsoft FY2026 Q3 官方披露资料包]]、[[alphabet-q2-2026-official-source-pack|Alphabet Q2 2026 官方披露资料包]]、[[amazon-q1-2026-official-source-pack|Amazon Q1 2026 官方披露资料包]]、[[meta-q1-2026-official-source-pack|Meta Q1 2026 官方披露资料包]]、[[oracle-q4-fy2026-official-source-pack|Oracle Q4/FY2026 官方披露资料包]]、[[nvidia-q1-fy2027-official-source-pack|NVIDIA Q1 FY2027 官方披露资料包]]、[[amd-q1-2026-official-source-pack|AMD Q1 2026 官方披露资料包]]、[[tsmc-q2-2026-official-source-pack|TSMC Q2 2026 官方披露资料包]]、[[micron-q3-fy2026-official-source-pack|Micron Q3 FY2026 官方披露资料包]]、[[asml-q2-2026-official-source-pack|ASML Q2 2026 官方披露资料包]]、[[applied-materials-q2-fy2026-official-source-pack|Applied Materials Q2 FY2026 官方披露资料包]]。

创建 Entity：[[microsoft-corporation|Microsoft Corporation]]、[[alphabet-inc|Alphabet Inc.]]、[[amazon-com-inc|Amazon.com, Inc.]]、[[meta-platforms-inc|Meta Platforms, Inc.]]、[[oracle-corporation|Oracle Corporation]]、[[advanced-micro-devices|Advanced Micro Devices, Inc.]]、[[taiwan-semiconductor-manufacturing|Taiwan Semiconductor Manufacturing Co., Ltd.（TSMC）]]、[[micron-technology|Micron Technology, Inc.]]、[[asml-holding|ASML Holding N.V.]]、[[applied-materials|Applied Materials, Inc.]]；更新 [[nvidia|NVIDIA Corporation（英伟达）]]。

创建 11 个 earnings Event：[[microsoft-fy2026-q3-results-2026-04-29|Microsoft FY2026 Q3 业绩与资本开支更新]]、[[alphabet-q2-2026-results-2026-07-22|Alphabet Q2 2026 业绩、TPU 系统收入与 capex 上调]]、[[amazon-q1-2026-results-2026-04-29|Amazon Q1 2026 业绩、AWS 芯片与现金回报]]、[[meta-q1-2026-results-2026-04-29|Meta Q1 2026 业绩与 capex 上调]]、[[oracle-q4-fy2026-results-2026-06-10|Oracle Q4/FY2026 业绩、RPO 与融资结构]]、[[nvidia-q1-fy2027-results-2026-05-20|NVIDIA Q1 FY2027 业绩与披露口径变更]]、[[amd-q1-2026-results-2026-05-05|AMD Q1 2026 业绩与 MI450/Meta 合作进展]]、[[tsmc-q2-2026-results-2026-07-16|TSMC Q2 2026 业绩与先进制程结构]]、[[micron-q3-fy2026-results-2026-06-24|Micron Q3 FY2026 业绩、HBM 与客户长协]]、[[asml-q2-2026-results-2026-07-15|ASML Q2 2026 业绩、EUV 订单与产能计划]]、[[applied-materials-q2-fy2026-results-2026-05-14|Applied Materials Q2 FY2026 业绩与设备展望]]。

更新 [[hyperscaler-ai-capex-roi-monitoring-model-2026|Hyperscaler AI CAPEX—ROI 监测模型（2026）]]；创建 Model：[[hyperscaler-capex-cash-return-comparison-2026|Hyperscaler 资本开支与现金回报比较（2026）]]、[[ai-compute-supply-capacity-revenue-bridge-2026-2028|AI 算力供给容量—收入桥（2026–2028）]]、[[ai-supply-chain-normalized-margin-scenarios-2026-2028|AI 算力供应链正常化利润率情景（2026–2028）]]。更新 [[ai-capex-roi-and-tradability-evidence-map-2024-2026|AI CAPEX、ROI 与可交易性证据图谱（2024–2026）]]；创建 [[cloud-and-compute-supply-chain-comparison-2026|云厂商与算力供应链比较（2026）]] 与 [[ai-capex-capacity-and-cash-return-monitoring-2026|AI CAPEX、容量与现金回报监测（2026）]]；更新 `wiki/index.md`。

证据风险：Microsoft、Alphabet、Amazon、Meta 最新 2026 capex 公司指引机械合计 US$710–740bn 为 `codex_inference`，不是纯 AI capex，也不覆盖 J.P. Morgan 的 US$697bn `market_consensus` 历史基线。现金 capex、融资租赁、未入表租赁与客户供货 GPU 口径不统一；RPO/backlog、GW 规划、sampling、订单、出货、收入、利润和 FCF 保持分层。NVIDIA 毛利率含 H20 基数、Micron 利润率含存储周期、ASML 收入受验收、Applied Materials 利润受投资收益和分部重述影响。缺少统一时点现价、EV、一致预期和拥挤度，未形成当前交易结论。

## 2026-07-28 ingest | 伊朗专题：战争、霍尔木兹海峡与国际关系框架
处理 `raw/26.05.26-第五节.mp4`。创建：[[2026-05-26-iran-special-topic|伊朗专题：战争、霍尔木兹海峡与国际关系框架（2026-05-26）]]、[[geopolitical-shock-to-asset-price-evidence-chain|地缘政治冲击到资产价格的证据链]]、[[2026-02-28-us-israel-iran-conflict-and-hormuz-crisis|美以—伊朗冲突升级与霍尔木兹海峡危机（2026）]]、[[2026-04-28-uae-announces-opec-exit|阿联酋宣布退出 OPEC 与 OPEC+（2026-04-28）]]。更新：[`wiki/index.md`]。证据风险：ASR、OCR、说话人分离和 DeepSeek 精炼均属派生证据；1,063 条发言未绑定 PPT，41 处可疑修订均保留原文。课程关于恺加王朝年份、革命前伊朗 60% 城市化率、埃及近两亿人口、伊朗“最现代化/最工业化”、俄罗斯策划 2023-10-07、秘密代理人网络、五年内国界变化和长期油价方向等存在数字冲突、来源观点或传闻。美以—伊朗战争、霍尔木兹航运受阻、阿里·哈梅内伊死亡与继任、阿联酋自 2026-05-01 退出 OPEC/OPEC+按联合国、伊朗官方、阿联酋官方、OPEC、EIA 和美国财政部资料分层记录；贝森特推动阿联酋退出的归因未获官方支持。未创建 Entity、Model、Synthesis 或当前交易判断；源 MP4 及全部处理中间文件继续保留。
## [2026-07-28] maintenance | A 股与美股分市场分析路由

升级统一 Schema、Query、Equity Research、Ingest、Lint 与四类模板；新增 `a_share`、`us_equity`、`cross_market` 分析 Profile，并为现有上市 Entity、Model 与 Synthesis 补充 listing regime、发行人注册地、会计/币种、政策辖区和跨上市关系 metadata。未创建按市场划分的顶层目录，未改动 `raw/`。

## 2026-07-28 ingest | 知兴替，明得失——以日本为鉴
处理 `raw/26.06.02-第六节.mp4`。创建：[[2026-06-02-rise-and-fall-lessons-from-japan|知兴替，明得失——以日本为鉴（2026-06-02）]]、[[balance-sheet-recession|资产负债表衰退]]、[[1986-us-japan-semiconductor-agreement-and-1987-tariffs|1986 年日美半导体安排与 1987 年关税制裁]]。更新：[`wiki/index.md`]。证据风险：ASR、OCR、说话人分离和 DeepSeek 精炼均属派生证据；808 条发言未绑定 PPT，9 处可疑修订均保留原文。东京奥运会按日本官方 1964 年口径记录；Sony 技术许可按 Western Electric 晶体管专利、US$25,000 且不含制造诀窍记录；日美半导体安排与 1987 年 100%关税按 USTR、美国总统公告和日本经济产业省资料记录，并与 Toshiba Machine/Kongsberg 机床出口管制案分离；泡沫末期消费通胀 6%–8%、20%硬性份额目标和“美国单一摧毁日本半导体”保留为 `disputed`。日本 2026-04-28 至 2026-05-27 外汇干预按财务省 ¥11.7349tn 记录，未将“日本央行死守 160”升级为事实。未创建 Entity、Model、Synthesis 或当前交易判断；源 MP4 及全部处理中间文件继续保留。

## 2026-07-29 ingest | 从变化中看到确定性：中国半导体前沿创新与推理需求
处理 `raw/26.06.09-第七节.mp4`。创建：[[2026-06-09-china-semiconductor-frontier-innovation-and-inference|从变化中看到确定性：中国半导体前沿创新与推理需求（2026-06-09）]]、[[ai-compute-system-performance-and-token-economics|AI 算力的系统级性能与 Token 经济性]]、[[2024-05-24-national-integrated-circuit-industry-investment-fund-iii-established|国家集成电路产业投资基金三期成立（2024-05-24）]]、[[2026-05-25-huawei-presents-tau-scaling-law|华为发布韬（τ）定律（2026-05-25）]]。更新：[`wiki/index.md`]。证据风险：ASR、OCR、说话人分离和 DeepSeek 精炼均属派生证据；332 条发言未绑定 PPT，2 处可疑修订均回退或保留原文。大基金三期按 2024-05-24 成立、注册资本 RMB 344bn 记录，注册资本不等于实缴、募集或已投资；课程一期 RMB 104.7bn 与公开注册资本 RMB 98.72bn、最终募集 RMB 138.7bn 口径冲突。大基金参与 DeepSeek 融资保留为 `market_rumor`。韬定律发布为 `verified_fact`，381 款芯片、2026 年秋季麒麟和 2031 年 1.4nm 同等密度均为 `company_statement`。TSMC A14 按官方计划 2028 年量产记录；CloudMatrix 384/NVL72 的 1.7 倍因精度、卡数、功耗与负载未统一保留为争议性跨平台比较。推理数据按国家数据局 2025 年 101.34 EB、训练约 98.14 EB，2026 年 3 月底日均 Token 超 140tn 记录。未创建 Entity、Model、Synthesis 或当前交易判断；源 MP4 及全部处理中间文件继续保留。

## 2026-08-01 ingest | A股市场回顾：潮起潮落，研鉴时代
处理 `raw/26.06.16-第八节.mp4`。创建：[[2026-06-16-a-share-market-history-and-regime-evolution|A股市场回顾：潮起潮落，研鉴时代（2026-06-16）]]、[[a-share-investment-regime-evolution|A股投资范式与市场主线轮动]]、[[2005-04-29-share-trading-reform-pilot-launched|股权分置改革试点启动（2005-04-29）]]、[[a-share-policy-liquidity-and-industrial-regime-thesis|A股政策、流动性与产业主线框架]]。更新：[[2024-04-12-capital-market-new-nine-guidelines|2024年资本市场“新国九条”发布]]、[`wiki/index.md`]。证据风险：ASR、OCR、说话人分离和 DeepSeek 精炼均属派生证据，精炼文本仍有明显年份、主体和专名错误；本片与 2026-05-12 视频属于同一课程系列，不是独立确认。股权分置改革按证监会 2005-04-29 试点启动、五部委 2005-08-23 全面推进的官方节点分层记录；2015 年工业利润同比下降 2.3%、GDP 增长 6.9%、PPI 下降 5.2%采用国家统计局口径；“维稳资金至少 RMB 1.5tn”缺少同定义官方披露，保留为 `disputed`。创建的 Synthesis 为低置信 `provisional` 框架，不建立“5/6 命中率”或“五六年周期”Model，不形成当前价格交易判断；未创建 Entity。源 MP4、两份转录 HTML、权威时间轴及全部处理中间文件继续保留，未执行清理。

## [2026-08-01] ingest | 《一周政策解读》市场与产业研究汇编（2026-06-13）

处理并永久保留 `raw/20260613【一周政策解读】.pdf`。创建：[[2026-06-13-weekly-policy-interpretation|《一周政策解读》市场与产业研究汇编（2026-06-13）]]；更新：[`wiki/index.md`]。证据风险：来源为 73 页会员教学汇编，混合新闻、卖方观点、产业调研和个股推荐；SpaceX 上市及估值叙事保留为 `market_rumor`/`disputed`，政策、订单、扩产、收入和利润未取得一手连续证据。本次未创建 Entity、Event、Model 或当前交易判断；原始 PDF SHA-256 保持 `2b3a036d65da824853cda00e5fb4d1a5b7c815c02a4128a55a3715e25eef508e`。

## [2026-08-01] ingest | 《一周政策解读》市场与产业研究汇编（2026-06-19）

处理并永久保留 `raw/20260619【一周政策解读】.pdf`。创建：[[2026-06-19-weekly-policy-interpretation|《一周政策解读》市场与产业研究汇编（2026-06-19）]]；更新：[`wiki/index.md`]。证据风险：来源为 79 页会员教学汇编；ETF、AI 商业化、先进封装、规模化和交易拥挤判断均为二手来源观点，缺少统一行情、客户、订单、交付和财务勾稽。未批量创建 Entity，未创建 Event、Model 或当前交易判断；原始 PDF SHA-256 保持 `3d603990d16b8b9c9192fbca656b75048e512657e77e0af0c329b42b4579ccd4`。

## [2026-08-01] ingest | 《一周政策解读》市场与产业研究汇编（2026-06-27）

处理并永久保留 `raw/20260627【一周政策解读】.pdf`。创建：[[2026-06-27-weekly-policy-interpretation|《一周政策解读》市场与产业研究汇编（2026-06-27）]]；更新：[`wiki/index.md`]。证据风险：来源为 65 页会员教学汇编；电子板块成交约 RMB 1.22tn、融资余额约 RMB 626.187bn、存储/先进封装景气及公司验证与订单均未附可复算或一手底稿，分别保留为 `source_opinion`、`codex_inference` 或 `disputed`。未创建 Entity、Event、Model 或当前交易判断；原始 PDF SHA-256 保持 `4e0fcfb6c23fcca3630d9ef9149f5064c74111750d3c3b8424d2d150c15ef6b6`。

## [2026-08-01] ingest | 《一周政策解读》市场与产业研究汇编（2026-07-04）

处理并永久保留 `raw/20260704【一周政策解读】.pdf`。创建：[[2026-07-04-weekly-policy-interpretation|《一周政策解读》市场与产业研究汇编（2026-07-04）]]；更新：[`wiki/index.md`]。证据风险：来源为 64 页会员教学汇编；科创 50 涨幅、开户数、政策影响、AI 云服务价值捕获、存储/先进封装景气均缺少完整原始口径，“长鑫上市进度推迟”保留为 `market_rumor`。未创建 Entity、Event、Model 或当前交易判断；原始 PDF SHA-256 保持 `6a32e32a1862273b26b78af50103ac46bd125d9679cf923d238443c28452e3b4`。

## [2026-08-01] ingest | 《一周政策解读》市场与产业研究汇编（2026-07-11）

处理并永久保留 `raw/20260711【一周政策解读】.pdf`。创建：[[2026-07-11-weekly-policy-interpretation|《一周政策解读》市场与产业研究汇编（2026-07-11）]]；更新：[`wiki/index.md`]。证据风险：来源为 66 页会员教学汇编；ETF 调仓、AI4S、商业航天、Meta 自研芯片和先进封装均未形成技术到财务的证据链，兆易创新与工业富联等 2026H1 业绩预告仅按二手转述记录，待交易所公告和正式财报核验。未创建 Entity、Event、Model 或当前交易判断；原始 PDF SHA-256 保持 `28020552c48d82638b55973354fe679a8de663bd5f69089955cb1675ed9b2c28`。

## [2026-08-01] ingest | 《一周政策解读》市场与产业研究汇编（2026-07-18）

处理并永久保留 `raw/20260718【一周政策解读】.pdf`。创建：[[2026-07-18-weekly-policy-interpretation|《一周政策解读》市场与产业研究汇编（2026-07-18）]]；更新：[`wiki/index.md`]。证据风险：来源为 67 页会员教学汇编；AI 拥挤、半导体指数回撤、ASML、UMC silicon photonics、Kimi K3 与创新药 BD/临床节点均需回到行情、公司、技术或监管原件，并保持审批、endpoint、商业化、收入、利润和 FCF 分层。未创建 Entity、Event、Model 或当前交易判断；原始 PDF SHA-256 保持 `57f5dfe37e669692b7df560f87c0b300e1dc6d639132fa90c58488720f6707cb`。

## [2026-08-01] ingest | 《一周政策解读》市场与产业研究汇编（2026-07-25）

处理并永久保留 `raw/20260725【一周政策解读】.pdf`。创建：[[2026-07-25-weekly-policy-interpretation|《一周政策解读》市场与产业研究汇编（2026-07-25）]]；更新：[`wiki/index.md`]。证据风险：来源为 51 页会员教学汇编；Tesla/Intel 市场与业绩数据、约 US$3.5tn AI 融资需求均缺少完整原始口径，TSMC 2027 涨价保留为 `market_rumor`，“一次性通过、量产订单即将获批、小批量、规模量产前夕”未被合并或升级为规模收入。未创建 Entity、Event、Model 或当前交易判断；原始 PDF SHA-256 保持 `fe35a4e1e3cf1d80f3bbaa1700ace7a5bf24351641f6d749159a7f1b7bbb54cf`。

## [2026-08-01] ingest | 李录：我们时代的全球价值投资

处理并永久保留 `raw/李录：我们时代的全球价值投资_ 在北大光华管理学院的演讲2024-12-07 _ 全文图解-虎嗅网.html`。创建：[[2026-05-12-li-lu-global-value-investing-speech|李录：我们时代的全球价值投资]]、[[li-lu|李录]]、[[global-value-investing-and-purchasing-power|全球价值投资与购买力框架]]；更新：[`wiki/index.md`]。证据风险：知识截止日按演讲日期 2024-12-07，虎嗅转载日期为 2026-05-12；来源是 Web3天空之城署名的第三方整理/转载稿，不是北京大学、李录或 Himalaya Capital 官方逐字稿。就业、制造业、消费和储蓄等宏观数字缺少年份、定义和原始链接，保留为低置信 `source_opinion`。未创建 Event、Model 或任何具体证券的当前交易判断；原始 HTML SHA-256 保持 `7e8f4cef3f97657e4cd94c2c19b2bd285c2bcf2354c6e0d32d2234d47f8d1695`。

## [2026-08-01] ingest | Bitcoin: A Peer-to-Peer Electronic Cash System

处理并永久保留 `raw/bitcoin.pdf`。创建：[[2008-10-31-bitcoin-peer-to-peer-electronic-cash-system|Bitcoin: A Peer-to-Peer Electronic Cash System]]、[[bitcoin|Bitcoin（比特币）]]、[[satoshi-nakamoto|Satoshi Nakamoto（中本聪）]]、[[bitcoin-proof-of-work-consensus|Bitcoin 的 Proof-of-Work 共识与激励]]、[[bitcoin-transaction-spv-and-privacy|Bitcoin 交易、SPV 与隐私边界]]、[[2008-10-31-bitcoin-whitepaper-released|Bitcoin 白皮书公开发布（2008-10-31）]]、[[bitcoin-attacker-catch-up-probability-model|Bitcoin 攻击者追赶概率模型]]；更新：[`wiki/index.md`]。证据风险：首次公开日按 Cryptography Mailing List 的 2008-10-31 原始邮件记录，本地 PDF 的 2009-03-24 元数据只表示文件生成时间；本地文件与 Bitcoin.org 英文原版内容和 9 页结构一致，但未验证远端逐字节哈希相同。论文发布、完整实现、独立复现、生产部署、规模采用和商业收入保持分层；攻击者追赶概率表已本地复算一致，但固定 `p/q`、Poisson 到达与攻击范围均为模型假设。未建立当前 Bitcoin 协议、监管、价格、估值或交易判断；原始 PDF SHA-256 保持 `b1674191a88ec5cdd733e4240a81803105dc412d6c6708d53ab94fc248f4f553`。

## [2026-08-01] ingest | Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform

处理并永久保留 `raw/Ethereum_Whitepaper_-_Buterin_2014.pdf`。创建：[[2014-ethereum-next-generation-smart-contract-platform|Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform]]、[[ethereum|Ethereum（以太坊）]]、[[vitalik-buterin|Vitalik Buterin]]、[[ethereum-account-state-evm-and-gas|Ethereum 账户状态、EVM 与 Gas]]、[[blockchain-application-platform-design-tradeoffs|区块链应用平台的设计路线权衡]]、[[smart-contracts-dapps-and-oracle-boundaries|Smart Contract、DApp 与 Oracle 证据边界]]、[[2014-01-23-ethereum-goes-public|Ethereum 项目公开发布（2014-01-23）]]、[[ethereum-whitepaper-issuance-model|Ethereum 白皮书历史发行与供给均衡模型]]；更新：[`wiki/index.md`]。证据风险：白皮书仅能确定发布于 2014 年，`as_of: 2014-12-31` 是年份上界而非精确日期，本地 PDF 的 2022-02-02 ModDate 仅表示文件生成/修改元数据；本地文件与 Ethereum.org 官方下载 PDF 的内容及 36 页结构一致，但未验证远端逐字节哈希。官方 PDF 与当前官方 HTML 在销售兑换范围、矿池数量和后加内容上存在版本冲突，本次以本地 PDF 为唯一摄入正文；研究发布、代码、独立复现、部署、采用与商业收入保持分层。历史 PoW、矿工线性发行和费用方案已被 The Merge、PoS 与后续费用机制取代，发行算术虽复算一致，当前适用性标记为 `superseded`。未建立当前 ETH 供给、价格、估值或交易判断；原始 PDF SHA-256 保持 `4cc15f99f5df56c8a7156188a9b9290c71e7dfd9a92093b028213c9a185c0a15`。
