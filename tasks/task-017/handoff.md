# 已知信息

- 入口文件：`src/logging/redactor.py`。
- 根因：大小写敏感匹配和缺失 URL query 处理。
- stdlib `urllib.parse` 足够。
- 测试不会要求保留 query 参数原始顺序以外的复杂编码边界。
