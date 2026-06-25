# 已知信息

- 入口文件：`src/config/deep_merge.py`。
- 根因：`dict.update` 是浅合并。
- 不需要支持 merge strategy 配置。
- 测试会检查输入对象未被原地修改。
