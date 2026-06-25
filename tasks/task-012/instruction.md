# 修复 CSV 用户导入

来源/场景：企业后台批量导入用户时常见的 CSV BOM、大小写邮箱重复和空行问题。

目标：`src/importer/csv_import.py` 当前会把 BOM 留在 header 中，并按原始 email
做大小写敏感去重。

要求：

1. 只修改 `src/importer/csv_import.py`。
2. 支持 UTF-8 BOM。
3. email 需要 trim 并转小写。
4. 空 email 行跳过。
5. 重复 email 只保留第一次出现。
6. name 需要 trim。

完成后运行：

```bash
bash test.sh
```
