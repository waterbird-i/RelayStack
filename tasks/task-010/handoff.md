# 已知信息

- 入口文件：`src/deps/dependency_order.py`。
- 根因：只有 `visited`，缺少当前递归栈 `visiting`。
- 最小修复是 DFS 时维护 path；遇到已在 path 中的节点就截取循环段报错。
- 测试同时校验无环排序和循环错误信息。
