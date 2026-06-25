# 已知信息

- 入口文件：`src/db/sql_filters.py`。
- 根因：`if not value` 丢掉 falsy 条件，f-string 直接拼值。
- 不需要接数据库，只构造 where 和 params。
- 测试会检查参数顺序和未知字段。
