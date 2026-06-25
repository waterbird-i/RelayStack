# CLI 有文件参数时优先读文件

公开来源：[markedjs/marked#3967](https://github.com/markedjs/marked/pull/3967)。

目标：Markdown CLI 同时支持 stdin 和文件路径。当前实现把第一个用户参数当成 Markdown
字符串本身，导致 `node bin/marked.js README.md` 不会读取文件内容。

要求：

1. 修改 `bin/marked.js`。
2. 有文件参数时读取该文件内容。
3. 没有文件参数时读取 stdin。
4. 参数处理必须跳过 `node` 和脚本路径，只看用户传入的 argv。

完成后运行：

```bash
bash test.sh
```

