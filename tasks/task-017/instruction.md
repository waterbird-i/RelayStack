# 修复日志脱敏

来源/场景：企业日志平台常见安全问题：token/password 出现在 header 或 URL query 中。

目标：`src/logging/redactor.py` 当前只按小写精确匹配 header，且完全不处理 URL query。

要求：

1. 只修改 `src/logging/redactor.py`。
2. header key 大小写不敏感。
3. 敏感 header：`authorization`、`cookie`、`x-api-key`。
4. URL query 中 `token`、`password`、`secret` 大小写不敏感脱敏。
5. 非敏感 query 参数和值必须保留。

完成后运行：

```bash
bash test.sh
```
