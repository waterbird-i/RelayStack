# 阻断归档路径穿越

来源/场景：[snyk/zip-slip-vulnerability](https://github.com/snyk/zip-slip-vulnerability)
记录的 Zip Slip 类问题，企业构建系统解压制品时也常见。

目标：`src/archive/safeExtract.js` 负责把归档 entry 映射到目标目录。
当前实现只做 `startsWith(base)`，会漏掉 sibling-prefix 路径，也会静默丢弃非法 entry。

要求：

1. 只修改 `src/archive/safeExtract.js`。
2. 目标路径必须位于 destination 内部。
3. `../`、绝对路径、sibling prefix 都必须抛出 `unsafe path` 错误。
4. 正常路径返回 `{ name, target }` 列表。
5. 不需要真正解压文件。

完成后运行：

```bash
bash test.sh
```

## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。