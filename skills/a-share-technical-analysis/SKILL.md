---
name: a-share-technical-analysis
description: Generate an auditable daily, weekly, and monthly technical snapshot for one SSE, SZSE, or BJSE security using BaoStock as the primary market-data source, AkShare as a fallback and cross-check, and parallel CZSC plus pinned chan.py structure extraction over the same normalized bars. Use when an A-share query, comparison, dossier, current-position review, or week/month allocation decision needs technical context. Do not use for intraday trading, a purely factual wiki lookup, non-A-share securities, or as a substitute for fundamentals and current-rule verification.
---

# A-Share Technical Analysis

为一个已解析的 A 股证券生成只读、可追溯的技术面快照。默认服务于周度或月度调仓：月线判断主结构，周线辅助仓位节奏，日线只用于执行时点。

## 适用边界

- 仅接受 `SSE:*`、`SZSE:*`、`BJSE:*` 的交易所前缀证券代码。
- 默认使用已完成的日 K 线，不使用盘中未完成 K 线，也不提供日内交易信号。
- 技术面是 `codex_inference`，不能覆盖基本面、估值、公司事件、流动性或市场规则结论。
- 不把任何形态写成确定性买卖建议。chan.py 的 BSP 1/1p/2/2s/3a/3b 只保留为中性结构候选，不翻译为交易动作。
- `data_quality_status` 与 `engine_consistency_status` 分开记录。行情、关键引擎锚点、chan.py 结构或参数稳定性任一为 `disputed`/`unavailable` 时，停止方向性结论。
- 不引入实时行情、自动交易、机器学习、动画图或交互图；只生成可审计的静态图。
- 输出先进入 `output/technical-analysis/`；未经策展人批准，不写入 Canonical Wiki、`wiki/index.md` 或 `wiki/log.md`。

## 执行流程

1. 读取 `references/data-contract.md`，解析代码、复权口径、字段单位和数据质量门。
2. 读取 `references/interpretation-rules.md`，确定月/周/日三个周期的职责和回答格式。
3. 若隔离环境不存在，运行 `bash scripts/setup_env.sh`。脚本使用 Python >=3.11，并将 chan.py 固定到 commit `429d6ed3043e27c93a003ba2b10e70a05575e1f5`。
4. 运行：

   ```bash
   .work/venvs/a-share-ta/bin/python \
     skills/a-share-technical-analysis/scripts/technical_snapshot.py \
     --ticker SSE:600519
   ```

5. 检查命令输出的 JSON 与 Markdown 路径，读取 Markdown 报告并将其与 Wiki 证据、当前价格和投资期限合并。
6. 同时检查 `.manifest.json`、静态 `.audit.png`、`artifacts.native_chan_charts` 中的月/周/日原生图、`.state-commit.json` 与结构 state 路径，并核对每个图的 SHA-256。只有 `data_quality_status=complete` 才允许提交生命周期 state，且提交发生在分析产物之后；若只想复现，使用 `--no-state-write`；若只禁用 chan.py 原生图，使用 `--no-native-chan-charts`；若无需任何图片，使用 `--no-audit-chart` 同时禁用审计图和原生图。
7. 在回答中保留 `technical_as_of`、行情源、复权口径、两个引擎身份、strict/broad `config_hash`、`data_quality_status`、`engine_consistency_status`、交叉核对结果和所有限制。

## C1–C5 实现契约

- **C1 — 同源双引擎：** CZSC 与固定 commit 的 chan.py 并行读取同一个 normalized qfq bars digest；chan.py 不得自行取数。
- **C2 — 完整结构：** 输出当前截止日 `confirmed`/`provisional` 的完整笔、线段、线段的线段、中枢与线段中枢。
- **C3 — BSP 历史：** BSP 1/1p/2/2s/3a/3b 始终为中性候选，并通过 `first_seen`/`last_changed`/`withdrawn` 保留候选的变化、撤回与重现历史。
- **C4 — 静态审计与参数稳定性：** 生成非动画、非交互的综合审计图，以及 chan.py 原生月/周/日静态图。原生图只绘制 `strict` profile，并与双引擎分析引用同一个 normalized input digest；默认图层为 K 线、合并 K 线、笔、线段、线段的线段、中枢、线段中枢、中性 BSP、线段 BSP 和 MACD。保留 strict/broad 各自 `config_hash` 与语义稳定交集，且不按结构数量简单判 `disputed`。
- **C5 — 多周期父子上下文：** 生成月→周、周→日父子映射，以及跨参数稳定、当前已确认中枢的区间嵌套关系。

质量门横跨 C1–C5：分开记录行情与引擎状态，按 `unavailable > disputed > degraded > complete` 汇总 `overall_technical_status`；任何关键层为 `disputed`/`unavailable` 时显式阻断方向结论。

## 数据与降级

- BaoStock 是主行情源；AkShare 用于字段补充、交叉核对和主源失败时降级。
- 主源失败而 AkShare 成功时，明确标为 `degraded`，不得暗示仍为 BaoStock 结果。
- 双源价格不一致超过质量阈值时标为 `disputed`，同时保留两方差异，不静默选择较有利的一方。
- 两源均失败时标为 `unavailable`，报告阻断原因，不用旧缓存伪装为当前数据。
- CZSC 与 chan.py 必须接收同一个归一化 K 线 frame；适配器禁止调用 chan.py 自带 DataAPI。
- chan.py 默认 checkout 位于 `.work/vendor/chan.py`，也可显式设置 `CHAN_PY_PATH`；commit 不匹配时结构化降级为 `unavailable`，报告仍应生成。
- strict/broad 两组固定参数均生成 `config_hash`；稳定结果取语义交集，结构数量差异本身不构成 `disputed`。
- 结构 state 的 identity 包含 adapter schema、固定 commit 和两组 `config_hash`；记录 `first_seen`、`last_changed`、`withdrawn`，不跨方法版本串联。
- state 写入使用跨进程锁、写前 cutoff/CAS 复核，并在分析产物生成后提交；同 stem 的 `.state-commit.json` 保留最终提交结果和 state hash。`degraded`、`disputed`、`unavailable` 行情均不得改写生命周期。
- 将综合审计图与 `native_chan_charts` 分别记录进 analysis manifest。为三张原生图记录 timeframe、路径、字节数和 SHA-256，并保留 pinned commit、strict `config_hash` 与 normalized input digest；不得把 BSP 图标解释为交易动作。
- 原生图渲染失败时保留 JSON、Markdown、analysis manifest 和可用图，将可视化产物结构化降级并写明原因；不得借渲染失败改变行情或引擎质量状态，也不得伪造缺失图片路径。
- `confirmed` 不是跨未来 K 线不可修订的承诺。真实 prefix/full 探针显示当前已确认笔与 BSP 仍可能延长、改变或消失；报告必须解释为“当前 `technical_as_of` 已确认、后续仍需生命周期审计”。BSP 无论所属笔是否确认都只称中性候选。
- `--offline-csv` 必须按 `--start/--end` 严格裁剪，并核对 CSV `symbol` 与 canonical ticker；历史回放不得读取 cutoff 之后的 K 线。
- CLI 拒绝把 output、cache 或 state 目录指向仓库 `raw/`、`wiki/` 或其子目录。
- 缓存、行情 manifest、结构 state、CZSC 与 Matplotlib 缓存均放在 `.work/`；报告、分析 manifest 和静态审计图放在 `output/`。

## 回答合同

至少说明：

1. 证券、`listing_regime: a_share`、投资期限和 `technical_as_of`；
2. 数据源、复权口径、数据质量和未完成数据是否被排除；
3. 月线主结构、周线仓位含义、日线执行含义；
4. CZSC 与 chan.py 的完整笔/线段/中枢（confirmed/provisional）、中性 BSP、参数稳定交集、双方语义锚点差异，以及 strict 原生月/周/日静态图的可用性；
5. 月→周、周→日父子映射及已确认稳定中枢的区间嵌套上下文；
6. 事实层数据与 `codex_inference` 的明确分界，以及图表 manifest/SHA-256、禁用状态或渲染降级原因；
7. 技术结论失效条件、基本面/事件冲突和不能完成的判断。

若要保存长期可复用的技术快照，先展示拟写页面和元数据，再等待用户批准。
