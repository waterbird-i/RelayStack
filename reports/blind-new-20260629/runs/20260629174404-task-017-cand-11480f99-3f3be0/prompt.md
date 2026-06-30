# 修复日志脱敏

来源/场景：企业日志平台常见安全问题：token/password 出现在 header 或 URL query 中。

目标：`src/logging/redactor.py` 当前只按小写精确匹配 header，且完全不处理 URL query。

要求：

1. 只修改 `src/logging/redactor.py`。
2. header key 大小写不敏感。
3. 敏感 header：`authorization`、`cookie`、`x-api-key`。
4. URL query 中 `token`、`password`、`secret` 大小写不敏感脱敏。
5. 非敏感 query 参数和值必须保留。

完成后运行：

```bash
bash test.sh
```

## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。