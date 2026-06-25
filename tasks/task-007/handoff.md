# 已知信息

- 入口文件：`src/archive/safeExtract.js`。
- 根因：字符串前缀判断不是路径边界判断，`/tmp/outside` 会通过
  `/tmp/out` 的 startsWith 检查。
- 建议用 `path.resolve` 后检查 `target === base || target.startsWith(base + path.sep)`。
- 发现非法 entry 应 fail fast，不能静默过滤。
