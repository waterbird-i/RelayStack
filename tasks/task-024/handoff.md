# 已知信息

- 已知入口文件：`src/streaming/ndjson.py`。
- 根因：stream chunk 边界不等于行边界。
- 最小实现维护 buffer，每次只解析 `\n` 前的完整行。
- 测试覆盖跨 chunk、空行、末尾无换行。
