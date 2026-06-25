# 修复 semver caret range

来源/场景：npm / package manager 依赖解析中常见的 `^` range 边界问题。

目标：`src/semver/caret.js` 当前用字符串前缀判断，错误处理 `^1.2.3` 和 `^0.2.3`。

要求：

1. 只修改 `src/semver/caret.js`。
2. 支持普通版本 `MAJOR.MINOR.PATCH`。
3. `^1.2.3` 表示 `>=1.2.3 <2.0.0`。
4. `^0.2.3` 表示 `>=0.2.3 <0.3.0`。
5. `^0.0.3` 表示 `>=0.0.3 <0.0.4`。
6. 不需要支持 prerelease 或复杂 range。

完成后运行：

```bash
bash test.sh
```

## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。