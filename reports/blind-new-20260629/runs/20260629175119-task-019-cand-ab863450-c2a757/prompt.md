# 修复迁移计划排序

来源/场景：数据库迁移工具常见问题：字符串排序让 `10_` 排在 `2_` 前面，
重复版本也未检测。

目标：`src/migrations/planner.js` 当前直接 `files.sort()`。

要求：

1. 只修改 `src/migrations/planner.js`。
2. 文件名格式是 `<number>_<name>.sql`。
3. 按 number 数值升序排序。
4. 同一个 number 出现多次必须抛出 `duplicate migration version`。
5. 非法文件名抛出 `invalid migration name`。

完成后运行：

```bash
bash test.sh
```

## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。