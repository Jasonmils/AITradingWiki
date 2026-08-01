# A 股研究数据合同

## 标识和来源顺序

- 输入只能是 `SSE:######`、`SZSE:######` 或 `BJSE:######`。
- 保留 canonical ticker；只在 adapter 内转换为腾讯、东财、巨潮所需代码。
- 重要事项按“交易所/公司正式披露 → 公司 IR → 第三方聚合 → 新闻线索”核验。
- BJSE 当前 `920xxx` 与历史 `43/83/87xxxx` 不自动互相转换；历史号码的冻结报价必须标记 stale，并要求按公司名称核对当前代码。

## 每个 adapter 的统一字段

```text
canonical_ticker
provider
endpoint
source_url
queried_at
response_fetched_at
as_of
timezone
raw_response_sha256
field_units
evidence_class_hint
data_quality_status
error_type
error_message
result_status
record_count
records
from_cache
```

- `result_status=empty` 且 `error_type=null`：请求和 schema 均成功，确实没有记录。
- `result_status=error`：传输、HTTP、provider、schema、标识解析、无效分页参数或分页失败。`page_size`、`max_pages` 必须是正整数；不得把未发起请求的结果标为 `empty`。
- `data_quality_status=complete|degraded|unavailable`。第三方单源和未完成官方回查的数据不得仅因接口成功而升级为已验证事实。
- 非空响应列表中的行必须是符合 adapter 关键字段合同的对象；schema 漂移、证券代码不匹配或关键字段缺失必须返回 `schema_error`，不得静默跳过后返回 `empty`。
- 分页中断或 schema 错误若已取得部分记录，保留记录可推导出的 `as_of`，同时保持 `result_status=error` 和 `data_quality_status=degraded`。
- 多页结果的 `raw_response_sha256` 是按页顺序直接连接原始响应后计算的 SHA-256。
- `queried_at` 是本次调用时间，`response_fetched_at` 是底层响应抓取时间；缓存命中时两者可以不同。二者均使用 UTC ISO 8601；市场日期按 `Asia/Shanghai` 解释。

## 模块

- D1 `quote`：当前价、昨收、最高和最低价必须是有限正数；关键字段缺失返回 `schema_error`。当前价、PE/PB、市值等仍是 provider 观测。报价早于时效门、冻结，或时间戳比本机 UTC 快超过 300 秒时标记 stale 并要求官方回查。`suspension_status` 只是候选状态，必须回查交易所或公司公告。
- D2 `announcements`、`lockups`、`dividends`、`holder_counts`、`block_trades`、`margin`：CNINFO 公告优先；东财事件数据均带 `official_recheck_required=true`。
- D3 `financial_filings`、`financial_crosscheck`、`consensus`：正式报告优先；`financial_filings` 默认按 CNINFO 定期报告 category 和近六年日期窗口查询，避免先遍历全部公告。新浪三表和 THS 一致预期只作交叉检查。预测必须保留年度、表内更新时间和机构覆盖数；envelope `as_of` 优先表内更新时间，机构数缺失也必须设置 `coverage_warning=true`。
- D4 `ir`、`news`：公司回复为 `company_statement`；提问和新闻是检索线索。

## CLI 写入边界

- `--output-dir` 与 `--cache-dir` 不得指向本仓库 `raw/`、`wiki/` 或其子目录，解析符号链接后仍执行该检查。
- 报告与缓存先用同目录唯一 `NamedTemporaryFile` 写入并刷新，再原子替换目标文件；异常时清理临时文件。

## 禁止推断

- 不设置固定 30 倍或任何统一估值锚。
- 不用 PEG 阈值直接判断贵/便宜。
- 不把股东户数下降、订单大小分类、热榜或新闻热度解释为可验证的资金主体行为。
- 不因公告“宣布”而推断事项已完成、形成收入、利润或现金流。
