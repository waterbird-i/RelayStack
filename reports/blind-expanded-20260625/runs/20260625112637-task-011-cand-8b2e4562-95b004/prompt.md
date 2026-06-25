# 修复 Markdown front matter 解析边界

来源/场景：文档站、博客和企业知识库常见 front matter 解析问题。

目标：`src/markdown/frontmatter.js` 当前会在正文中寻找任意 `---`，导致普通正文被误判成
front matter。

要求：

1. 只修改 `src/markdown/frontmatter.js`。
2. 只有文件第一行就是 `---` 时才解析 front matter。
3. 第二个单独一行的 `---` 作为结束。
4. 没有 front matter 时，metadata 为 `{}`，body 保持原文。
5. YAML 不需要完整解析，只需要支持 `key: value`。

完成后运行：

```bash
bash test.sh
```

## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。