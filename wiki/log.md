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
