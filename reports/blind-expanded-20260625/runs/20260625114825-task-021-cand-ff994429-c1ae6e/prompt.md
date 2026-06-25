# 修复业务日调度

来源/场景：工单 SLA、财务结算、企业审批流常见的 business-day 计算。

目标：`src/schedule/business_days.py` 当前直接加自然日，未跳过周末和 holidays。

要求：

1. 只修改 `src/schedule/business_days.py`。
2. `add_business_days(start, days, holidays=())` 返回 `date`。
3. 周六、周日不计入 business day。
4. holidays 是 `date` 集合，也不计入。
5. `days=0` 返回 start 本身。

完成后运行：

```bash
bash test.sh
```

## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。