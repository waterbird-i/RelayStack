# 已知信息

- 已知入口文件：`src/flags/feature_flags.py`。
- 根因：`or` fallback 把显式 falsy 值当缺失。
- 用 `key in dict` 判断是否存在。
- env 解析只需要覆盖测试里的常见布尔字符串。
