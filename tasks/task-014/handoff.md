# 已知信息

- 入口文件：`src/pagination/cursor_page.py`。
- 根因：offset cursor 在数据集变化后不稳定。
- 可以用 JSON/base64 或简单字符串保存 `created_at` 和 `id`。
- 测试会在第一页后插入新记录，第二页不能重复第一页最后一条。
