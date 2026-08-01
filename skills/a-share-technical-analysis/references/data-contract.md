# A 股行情数据合同

## 代码规范

输入必须是交易所前缀代码：

| Canonical ticker | BaoStock | AkShare | CZSC symbol |
|---|---|---|---|
| `SSE:600519` | `sh.600519` | `600519` | `600519.SH` |
| `SZSE:000001` | `sz.000001` | `000001` | `000001.SZ` |
| `BJSE:920001` | `bj.920001` | `920001` | `920001.BJ` |

BJSE 接受六位代码且首位为 `4`、`8` 或 `9`；例如 `BJSE:430047`、
`BJSE:830799`、`BJSE:920001`。不要把北交所代码范围缩写为仅 `8xxxxx`。

不根据公司名猜证券代码。若交易所前缀与证券代码冲突，停止并要求解析。

## 标准 K 线字段

所有数据源必须归一化为：

| 字段 | 类型/单位 | 说明 |
|---|---|---|
| `dt` | Asia/Shanghai 交易日 | 日 K 的实际交易日期 |
| `symbol` | CZSC symbol | 带市场后缀 |
| `open` | CNY/股 | 开盘价 |
| `close` | CNY/股 | 收盘价 |
| `high` | CNY/股 | 最高价 |
| `low` | CNY/股 | 最低价 |
| `vol` | 股 | 成交股数 |
| `amount` | CNY | 成交额 |

BaoStock 日线 `volume` 已按股返回。AkShare `stock_zh_a_hist` 的 `成交量` 按手返回，归一化时乘以 100。两者 `成交额` 均按 CNY 保留。

## 复权口径

- `none`：BaoStock `adjustflag=3`；AkShare `adjust=""`。用于核对实际历史成交价。
- `qfq`：BaoStock `adjustflag=2`；AkShare `adjust="qfq"`。用于跨除权除息日期的技术结构分析。
- 不混合不同复权口径。报告必须写出 `adjustment`。
- 复权因子可能因数据源和更新时间不同而漂移；跨源复权序列发生差异时先标为 `disputed`，不要自动平均。
- 前复权序列无法完整核对时，再核对双源未复权行情。未复权核对通过只能把整体状态降为 `degraded`，不能把单源前复权结构升级为双源已验证。

## 数据质量门

先检查：

- 必需字段存在且可转为数值；
- 日期严格升序且无重复；
- `high >= max(open, close)`、`low <= min(open, close)`、`high >= low`；
- 成交量和成交额非负；
- 日线样本数足以支持所声明的周期；
- 最后 K 线是已完成交易日；
- 双源重叠日期、价格误差、成交量误差和成交额误差。

使用以下状态：

| 状态 | 含义 | 允许结论 |
|---|---|---|
| `complete` | 主源完整且双源核对通过 | 可给出有条件技术判断 |
| `degraded` | 使用备用源、双源核对不可用或样本偏少 | 仅给弱结论并说明缺口 |
| `disputed` | 双源差异超阈值或内部字段矛盾 | 不给方向性仓位结论 |
| `unavailable` | 无可用行情 | 仅报告阻断原因 |

行情数据通过双源核对时可作为 `verified_fact` 使用；技术结构、趋势含义和仓位解释始终是 `codex_inference`。只有单一数据源时，不把行情观测升级为双源已验证事实。

## Provenance

每次输出保留：

- `ticker`、请求起止日、实际首末交易日；
- 主源、备用源、取数时间；
- 原始字段映射、单位换算和复权口径；
- 包版本、质量检查和跨源差异；
- 缓存文件和 manifest 路径。
- 归一化输入 frame 的 SHA-256；CZSC 与 chan.py 必须引用同一个 digest。
- chan.py 上游 commit、checkout 路径、adapter schema、strict/broad 完整参数和各自 `config_hash`。
- 分开的 `data_quality_status`、`engine_consistency_status`、`chan_structure_status` 与 `profile_stability_status`。
- 结构 state identity/path、`first_seen`、`last_changed`、`withdrawn`，以及 JSON、Markdown、静态审计图的 SHA-256。
- `native_chan_charts` 的 pinned commit、strict `config_hash`、normalized input digest，以及月/周/日各图的路径、字节数、状态和 SHA-256。

当前运行环境固定 `czsc==0.10.12`。已验证的 `1.0.0rc8` 属于预发布版，
并将公共对象从 `czsc.core` 移到包顶层；桥接代码兼容两种导入位置，但在
1.0 发布稳定版并通过离线与在线回归前，不自动升级生产依赖。

chan.py 固定上游 commit `429d6ed3043e27c93a003ba2b10e70a05575e1f5`。
适配器只使用 `CChan.trigger_load` 注入上述标准 K 线，不得调用上游 DataAPI、
不得二次联网取数。checkout 缺失、无法验证 commit 或 commit 不匹配时，返回
结构化 `unavailable`；不能让整个技术报告崩溃。

结构 state 文件名及内容必须包含由 adapter schema、chan.py commit、strict/broad
`config_hash` 生成的 bundle identity。方法或参数变化应开始新的 state 序列，不能把
方法升级造成的差异记成旧结构 `withdrawn`。

State 同时保存 `technical_as_of`。新运行 cutoff 早于已保存 cutoff 时必须返回
`out_of_order_cutoff` 并拒绝写入，避免历史 fixture 把现行结构误标为撤回；同一 cutoff
但 input digest 改变时记录 `data_revision`，保留这次数据修订造成的生命周期变化。
状态提交必须持有跨进程锁，并在锁内重新读取 cutoff、bundle identity 与输入摘要；若
预览后 state 已被另一进程推进，必须重新计算或以 CAS 冲突停止，不能用旧快照覆盖新状态。
只有 `data_quality_status=complete` 的运行可提交 state。分析 JSON、Markdown、静态图和
analysis manifest 先生成，state 随后提交，最后用 `.state-commit.json` 记录提交结果、
关联 run identity 与 state SHA-256。

离线 CSV 必须先核对 `symbol` 与 canonical ticker，再按 `--start/--end` 闭区间严格裁剪；
裁剪后为空、日期不可解析或 symbol 混杂均 fail closed。离线 fixture 固定为 `degraded`，
不得写入生命周期 state。output、cache 与 state 目录不得落入仓库 `raw/` 或 `wiki/`。

分析文件 stem 至少包含复权口径、normalized input digest 前 8 位、method bundle hash
前 8 位和 UTC 微秒级 run timestamp，避免同日不同输入、参数或 provenance 更新互相覆盖。
JSON、Markdown、analysis manifest 与静态图必须先写
同目录临时文件再原子替换。analysis manifest 对仓库内路径优先保存 repo-relative path；
当 CLI 明确把 output/cache/state 指向仓库外目录时，可保留绝对路径并视为外部产物定位。

## 静态可视化产物

- 默认同时生成综合 `.audit.png` 与 chan.py 原生月线、周线、日线三张静态图。只调用 pinned chan.py 的 `CPlotDriver`，禁用 `CAnimateDriver`、GUI、Web/Plotly 交互和上游 DataAPI。
- 只用 `strict` profile 绘制原生图；用 `broad` profile 计算参数稳定性，不把两组结构叠在同一张图上。
- 让三张原生图复用 C1 的同一份 normalized bars 及其 input digest；禁止为绘图重新取数、重新复权或生成另一份未登记输入。
- 默认绘制 `kline`、`kline_combine`、`bi`、`seg`、`segseg`、`zs`、`segzs`、`bsp`、`segbsp` 和 `macd`。把所有 BSP 标记解释为 `neutral_candidate_not_trade_signal`，不得生成方向性交易标签。
- 在 analysis manifest 的 `artifacts.native_chan_charts` 中记录集合状态、`profile: strict`、upstream commit、strict `config_hash`、input digest、静态/非动画/非交互声明，以及三张图各自的 timeframe、path、status、bytes 和 SHA-256。继续单独记录 `artifacts.audit_chart`，不要混淆两类图。
- 使用 `--no-native-chan-charts` 时只把原生三图记为 `not_generated`，继续生成综合审计图。使用 `--no-audit-chart` 时保持“无需图片”的兼容语义，将综合审计图和原生三图都记为 `not_generated`，仍生成 JSON、Markdown 与 analysis manifest。
- 单张原生图失败时保留其他成功图并记录该 timeframe 的错误；集合性渲染失败时结构化标记 `degraded` 或 `unavailable`。无论哪种情况，都继续生成主报告和 manifest，不改写 `data_quality_status`、`engine_consistency_status` 或结构 state。
- 对成功图片先原子发布，再计算最终文件的 SHA-256 和字节数。manifest 不得引用临时文件、缺失文件或哈希不匹配的图片。

缓存不等于当前事实。若重新使用缓存，必须显示缓存的 `fetched_at` 并重新判断时效性。
行情缓存 stem 必须包含 normalized input digest 与 provider identity；数据文件和 manifest
以临时文件完整生成后再发布，不得按 ticker/cutoff 静默覆盖历史复权修订。同 identity
提交必须持有跨进程锁；已存在 bundle 只有在 manifest identity、大小和 SHA-256 全部
通过时才复用，部分或损坏 bundle 必须 fail closed，禁止覆盖修复。
