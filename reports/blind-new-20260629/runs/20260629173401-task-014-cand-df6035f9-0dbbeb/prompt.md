# 修复游标分页稳定性

来源/场景：Feed、工单列表、消息列表常见的 cursor pagination 问题。

目标：`src/pagination/cursor_page.py` 当前把 cursor 当 offset。
当第一页之后有新数据插入，第二页会重复上一页数据或跳过数据。

要求：

1. 只修改 `src/pagination/cursor_page.py`。
2. 输入 items 是 dict 列表，包含 `id` 和 `created_at`。
3. 排序规则：`created_at` 倒序，`id` 倒序。
4. cursor 必须基于最后一条记录的 `(created_at, id)`，不能基于 offset。
5. 返回 `(page_items, next_cursor)`。
6. 最后一页 `next_cursor` 为 `None`。

完成后运行：

```bash
bash test.sh
```

## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。