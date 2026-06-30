# 空 Markdown 列表项应被解析

公开来源：[markedjs/marked#3984](https://github.com/markedjs/marked/pull/3984)。

目标：Markdown parser 当前要求列表 marker 后必须有内容，导致 `- `、`* `、
`1. ` 这种空列表项不生成 `<li></li>`。

要求：

1. 修改 `src/listParser.js`。
2. 无序列表的空项 `- ` / `* ` 应输出空 `<li></li>`。
3. 有序列表的空项 `1. ` 应输出空 `<li></li>`。
4. 列表后的普通段落不能被列表吞掉。

完成后运行：

```bash
bash test.sh
```


## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。