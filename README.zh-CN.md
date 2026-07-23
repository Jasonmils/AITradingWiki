# AI Trading Wiki 中文使用指南

AI Trading Wiki 是一个面向二级市场投资研究的 Codex Second Brain。

Codex 负责读取原始资料、维护结构化 Wiki、建立公司与产业之间的关联、更新财务模型、跟踪投资论点并回答问题；Obsidian 负责浏览、搜索、反向链接和图谱展示。

系统将投资研究拆成六层：

> 证据 → 对象 → 机制 → 事件 → 模型 → 投资判断

目标不是简单保存研报，而是持续回答：

- 公司经营什么业务，增长来自哪里？
- 哪些是已验证事实，哪些是公司表述、作者观点或市场传闻？
- 市场共识和非共识分别是什么？
- 财务预测依赖哪些假设？
- 哪些事件可以验证或推翻投资论点？
- 行业值得研究，是否等于当前价格值得交易？

## 目录结构

```text
AITradingWiki/
├── AGENTS.md
├── README.zh-CN.md
├── .agents/skills/              # Codex 自动发现的项目技能
├── skills/                      # 唯一的技能源码
│   ├── second-brain/
│   ├── second-brain-ingest/
│   ├── second-brain-query/
│   ├── second-brain-lint/
│   └── equity-research/
├── templates/
│   ├── source.md
│   ├── entity.md
│   ├── event.md
│   ├── model.md
│   ├── investment-thesis.md
│   └── monitoring.md
├── raw/                         # 只增不改的原始资料
│   └── assets/                  # 图片、图表和附件
├── wiki/
│   ├── sources/                 # 单份资料的事实摘要
│   ├── entities/                # 公司、证券、子公司、客户、产品等
│   ├── concepts/                # 产业机制、技术路线、指标和风险框架
│   ├── events/                  # 财报、订单、认证、并购和交易进度
│   ├── models/                  # 财务预测、估值、情景和敏感性
│   ├── synthesis/               # 投资论点、比较、判断和复盘
│   ├── index.md
│   └── log.md
└── output/                      # 非 canonical 报告和其他输出
```

`.agents/skills/` 使用相对符号链接指向 `skills/`，因此只需要维护一份技能源码。macOS Finder 中按 `Command + Shift + .` 可以显示 `.agents/`。

## 六类 Wiki 页面

| 页面类型 | 主要作用 | 典型内容 |
|---|---|---|
| Source | 保存单份资料明确表达的内容 | 财报摘要、电话会、研报、新闻 |
| Entity | 建立规范化研究对象 | 公司、证券、子公司、客户、供应商、产品 |
| Concept | 保存可以跨标的复用的机制 | 库存周期、技术路线、经营杠杆 |
| Event | 保存有时间和完成状态的变化 | 财报、订单、认证、并购、资产注入 |
| Model | 保存假设和计算过程 | 收入预测、利润、估值、情景和敏感性 |
| Synthesis | 形成投资判断 | 投资论点、行业比较、风险判断、复盘 |

不要按照“A股、港股、美股”“看多、看空”建立顶层目录。市场、观点和期限会变化，应使用元数据表达。

## 第一次打开

1. 在 Codex 中将工作目录设为：

```text
/Users/jasonmils/Library/Mobile Documents/iCloud~md~obsidian/Documents/jason_icloud_note/AITradingWiki
```

2. 升级后新建一个 Codex 任务或重启 Codex，使其重新发现五个项目技能。
3. 打开 Obsidian，选择 **Open folder as vault**，打开同一个目录。
4. 在 **Settings → Files and links → Attachment folder path** 中填写 `raw/assets/`。

## 五个 Codex 技能

| 技能 | 用途 |
|---|---|
| `$second-brain` | 初始化或修复另一个投资研究 Vault |
| `$second-brain-ingest` | 将不可变原始资料摄入 Wiki |
| `$second-brain-query` | 基于已有 Wiki 问答或比较多个标的 |
| `$second-brain-lint` | 审计结构、时效性和研究完整性 |
| `$equity-research` | 为一个上市证券建立或更新完整研究档案 |

显式使用 `$技能名` 最可靠。自然语言也可以触发，但完整单标的研究、模型更新或“现在是否值得建仓”应明确调用 `$equity-research`。

## 统一元数据

所有 Wiki 页面至少包含：

```yaml
---
page_type: source | entity | concept | event | model | synthesis
subject: ""
tags: []
tickers: []
markets: []
asset_classes: []
industries: []
themes: []
as_of: YYYY-MM-DD
sources: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

模型、投资论点、监控页面和其他当前性判断还应包含：

```yaml
status: draft | provisional | active | superseded | invalidated
confidence: low | medium | high
horizon: 1-3m | 6-12m | 12-24m | 3-5y
review_after: YYYY-MM-DD
```

- `updated`：文件最后编辑日期。
- `as_of`：数据和判断有效到哪一天。
- `review_after`：最晚什么时候需要重新核验。
- `status`：观点或模型目前是否仍然有效。

证券代码使用交易所前缀，例如：

```text
SZSE:300767
SSE:600519
HKEX:0700
NASDAQ:NVDA
```

常见别名可以保存到 `ticker_aliases`。

## 证据等级

重要论断必须分类：

| 类型 | 含义 |
|---|---|
| `verified_fact` | 已由一手或权威资料确认的事实 |
| `company_statement` | 公司或管理层表述、目标或指引 |
| `source_opinion` | 资料作者观点 |
| `market_consensus` | 可识别的市场或分析师共识 |
| `non_consensus` | 有证据支持的非共识判断 |
| `market_rumor` | 未确认的市场传闻 |
| `model_assumption` | 财务预测或估值假设 |
| `codex_inference` | Codex 基于证据形成的推断 |
| `disputed` | 存在实质冲突或争议 |

推荐使用论断级证据表：

```markdown
| 论断 | 类型 | 截止日 | 证据 | 置信度 | 失效条件 |
|---|---|---|---|---|---|
|  | verified_fact | YYYY-MM-DD | [[来源页面]] | high |  |
```

不得把以下概念混为一谈：

> 进入供应链 → 获得认证 → 正式订单 → 产品交付 → 确认收入 → 利润和现金流

## 日常工作流

### 1. 收集资料

把 Markdown、纯文本、财报、研报、电话会转录稿和会议记录放进 `raw/`。网页可通过 Obsidian Web Clipper 保存到 `raw/`，图片和附件放到 `raw/assets/`。

不要编辑、移动、改名或删除已经放入 `raw/` 的文件。

### 2. 摄入普通资料

```text
$second-brain-ingest 处理 raw/震安科技综合分析.md。

先识别涉及的公司、证券、业务分部、技术路线、客户、供应商、
交易事件、财务假设和风险。

把关键论断标记为已验证事实、公司表述、作者观点、市场传闻、
模型假设或 Codex 推断。

先给我 3–5 个关键结论和证据风险，等我确认后再写入 Wiki。
```

Codex 应创建 Source，选择性更新 Entity 和 Concept，把交易变化写入 Event，把预测和估值假设写入 Model，并更新 index、追加 log。

### 3. 摄入财报

```text
$second-brain-ingest 处理 raw/公司名称-2026Q2财报.pdf。

重点提取收入、毛利率、费用率、经营现金流、应收账款、存货、
资本开支、业务分部、管理层指引和同比环比变化。

历史事实写入 Source 和 Entity；管理层指引标记为
company_statement，不要当作已经实现的结果。
```

### 4. 建立单个股票研究档案

```text
$equity-research 为 SZSE:300767 建立完整研究档案。

先检查 Wiki 已有内容和研究覆盖度，再列出缺失、陈旧、冲突
和只有市场传闻支持的信息。

覆盖公司与证券、治理、业务分部、行业、技术、客户供应商、
历史财务、现金流、三情景模型、并表和少数股东权益、估值、
催化剂、风险、失效条件、跟踪指标和当前价格可交易性。

当前价格、最新财报、订单和交易进度必须重新核验。
先报告研究缺口，不要用推测填补。
```

该技能默认先交付研究报告和拟写页面清单，得到同意后才更新 Entity Hub、Event、Model、Synthesis、index 和 log。

### 5. 查询单个标的的已有观点

```text
$second-brain-query 我的知识库对 NASDAQ:NVDA 的当前判断是什么？

注明知识截止日，并区分：
- 已验证事实；
- 公司或资料作者观点；
- 市场共识；
- 非共识判断；
- Codex 推断；
- 催化剂；
- 风险和失效条件；
- 跟踪指标；
- 当前仍缺失的数据。

所有事实使用 [[wikilink]] 标注依据。
```

如果问题要求完整建档、更新模型或判断当前是否建仓，应改用 `$equity-research`。

### 6. 比较多个股票

```text
$second-brain-query 比较 NVDA、AVGO 和 AMD 的 AI 基础设施暴露。

比较收入来源、客户集中度、产品路线、毛利率、现金流、资本开支、
行业位置、估值、催化剂、风险和当前价格可交易性。

区分已验证事实、共识、非共识和 Codex 推断。
```

### 7. 更新投资论点

```text
$equity-research 更新 [[公司名称-投资论点-2026H2]]。

检查上次论点以来的新财报、交易进度、订单、客户验证、收入、
毛利率、现金流和股价变化。

逐项说明：
- 哪些事实得到确认；
- 哪些假设被削弱；
- 哪些风险已经发生；
- 哪些论点应标记 superseded 或 invalidated；
- 下一次验证时间。
```

旧论点不能删除，应保留用于复盘。

### 8. 运行健康检查

```text
$second-brain-lint 检查以下问题，先报告，不要直接修复：

1. 失效 wikilink、孤立页面和索引漂移；
2. 缺少 as_of、review_after 或必要元数据；
3. 已过期但仍标记 active 的页面；
4. 传闻、作者观点或模型假设被写成事实；
5. 模型假设没有来源；
6. ticker 格式不一致；
7. 数字缺少日期、币种、单位或来源；
8. Event 状态没有随里程碑更新；
9. 财务模型与最新财报不一致；
10. 投资论点缺少催化剂、风险、指标或失效条件；
11. 失效观点没有标记 invalidated；
12. Entity Hub 缺少关键研究模块。
```

建议每摄入 10 份资料、每月至少一次、财报后、重大投资决策前和论点更新前运行。

## 股票 Entity Hub

每个证券应有一个 Entity Hub，链接业务、治理、技术、Event、Model、投资论点和监控页面，并展示研究覆盖度：

```markdown
| 研究模块 | 状态 | 截止日 | 主要缺口 |
|---|---|---|---|
| 公司与证券 | complete | YYYY-MM-DD |  |
| 股权与治理 | partial | YYYY-MM-DD |  |
| 客户与供应链 | unverified | YYYY-MM-DD |  |
| 财务模型 | provisional | YYYY-MM-DD |  |
| 估值 | stale | YYYY-MM-DD |  |
```

`complete`、`partial`、`unverified`、`provisional` 和 `stale` 代表研究覆盖状态，不允许用猜测填补空白。

## 财务模型要求

Model 至少在适用时覆盖：

- 历史收入、利润和业务分部；
- 数量、价格和毛利率假设；
- 研发、销售和管理费用；
- 经营现金流、应收账款、存货和资本开支；
- 并表日期、持股比例和少数股东损益；
- 归母净利润、股本、EPS、净现金或净负债；
- 保守、基准和乐观情景；
- 可比公司、估值倍数和敏感性分析。

必须明确哪些数字来自财报、哪些来自公司指引、哪些是资料作者预测、哪些是 Codex 模型假设。

## 投资论点标准结构

投资论点应包括：

1. 结论与知识截止日；
2. 公司当前状态；
3. 已验证事实；
4. 市场共识；
5. 非共识判断；
6. Codex 推断；
7. 核心争议；
8. 多头、基准和空头情景；
9. 催化剂及预计时间；
10. 主要风险；
11. 论点失效条件；
12. 跟踪指标；
13. 估值与当前价格可交易性；
14. 证据缺口和冲突资料；
15. 观点变更记录。

必须分别回答行业吸引力、研究优先级和当前价格可交易性。

## 核心知识规则

1. `raw/` 和 `raw/assets/` 只读。
2. Source 只保存资料明确表达的内容。
3. Event 保存财报、订单、认证、并购、控制权和资产注入等变化。
4. Model 保存预测、估值、情景和敏感性。
5. Synthesis 保存投资论点、比较、判断和复盘。
6. 每个数字保留日期、期间、币种、单位和来源。
7. 冲突资料并列记录，不静默覆盖。
8. 所有当前性结论标明 `as_of`。
9. 过期观点标记 `superseded` 或 `invalidated`，不得删除。
10. 当前价格、最新财报、订单、认证和交易进度必须重新核验。
11. 不把行业空间直接等同于公司收入或当前价格的交易机会。
12. 不因业务优质而忽略上市公司持股比例和少数股东权益。

## 验证和维护

修复或重新生成 Codex 项目入口：

```bash
bash scripts/setup_codex.sh
```

运行验证：

```bash
bash tests/test_onboarding.sh
bash tests/test_codex_compat.sh
```

修改技能时只编辑 `skills/<skill-name>/`。`.agents/skills/` 会自动指向最新内容。技能未刷新时，新建 Codex 任务或重启 Codex。

基础工作流不需要 API Key。不要把 API Key、券商凭证或个人隐私写入仓库。`qmd`、`summarize` 和 `agent-browser` 是可选工具，不影响基本使用。
