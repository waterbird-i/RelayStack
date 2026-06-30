# 修复限流 token bucket

来源/场景：API gateway / webhook consumer 中常见的 token bucket 限流 bug。

目标：`src/ratelimit/token_bucket.py` 当前把 elapsed 转成 int，小数秒不会补 token；
时钟回拨时还可能扣出负数。

要求：

1. 只修改 `src/ratelimit/token_bucket.py`。
2. 按浮点秒补充 token。
3. token 不超过 capacity。
4. now 小于上次时间时，不补负 token。
5. `allow(cost, now)` 返回布尔值，并在允许时扣减 cost。

完成后运行：

```bash
bash test.sh
```

## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。