# 缓存 falsy 的环境状态

公开来源：[vitejs/vite#22715](https://github.com/vitejs/vite/pull/22715)。

目标：环境状态缓存现在用 truthy 判断命中，导致 `false`、`0`、`null` 这类
falsy 初始化结果不会被缓存，后续读取会重复调用初始化函数。

要求：

1. 修改 `packages/vite/src/node/server/environmentState.js`。
2. 用 cache 是否已有 key 判断命中，而不是用缓存值的 truthiness。
3. `initial()` 返回 `false` 时，第二次读取也必须直接返回缓存值。
4. 不改变不同 environment 之间互相隔离的行为。

完成后运行：

```bash
bash test.sh
```
