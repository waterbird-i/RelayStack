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

