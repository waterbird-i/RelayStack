# 修复配置合并

来源/场景：CI/CD、应用配置和 Helm values 类工具常见 deep merge 语义。

目标：`src/config/deep_merge.py` 当前是浅合并，override 一个嵌套字段会丢失同级配置。

要求：

1. 只修改 `src/config/deep_merge.py`。
2. 两边都是 dict 时递归合并。
3. list 按 override 整体替换，不做拼接。
4. 标量按 override 替换。
5. 不修改输入对象。

完成后运行：

```bash
bash test.sh
```

## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。