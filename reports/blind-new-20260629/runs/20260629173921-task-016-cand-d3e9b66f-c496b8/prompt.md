# 修复 SQL filter builder

来源/场景：企业后台列表筛选常见问题：`False`/`0` 条件被丢弃，同时字符串拼接有注入风险。

目标：`src/db/sql_filters.py` 当前用 truthy 判断并直接拼 SQL。

要求：

1. 只修改 `src/db/sql_filters.py`。
2. 支持字段白名单：`owner`、`is_active`、`retry_count`。
3. `False` 和 `0` 是有效筛选值。
4. `None` 和空字符串跳过。
5. 返回 `(where_sql, params)`，SQL 使用 `?` 占位符。
6. 遇到未知字段抛出 `ValueError`。

完成后运行：

```bash
bash test.sh
```

## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。