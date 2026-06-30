# 修复 NDJSON streaming parser

来源/场景：日志采集、消息队列 consumer 和 LLM streaming 输出中常见的 chunk 边界问题。

目标：`src/streaming/ndjson.py` 当前按每个 chunk 独立 split line，跨 chunk 的 JSON 行会解析失败。

要求：

1. 只修改 `src/streaming/ndjson.py`。
2. 支持 JSON 行跨 chunk。
3. 忽略空行。
4. 输入结束时如果还有完整的最后一行但没有换行，也要解析。
5. 如果剩余 buffer 不是合法 JSON，应抛出原始 `json.JSONDecodeError`。

完成后运行：

```bash
bash test.sh
```

## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。