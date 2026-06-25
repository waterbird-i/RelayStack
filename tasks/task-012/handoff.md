# 已知信息

- 入口文件：`src/importer/csv_import.py`。
- 根因：`csv.DictReader` 读到 BOM 后 header 变成 `\ufeffemail`；
  去重也没有做 normalize。
- 不需要 pandas，stdlib `csv` 足够。
- 测试覆盖 BOM、重复邮箱大小写、空邮箱、name trim。
