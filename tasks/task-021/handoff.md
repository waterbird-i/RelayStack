# 已知信息

- 入口文件：`src/schedule/business_days.py`。
- 根因：当前直接 `timedelta(days=days)`。
- 最小实现是按天循环，遇到工作日才递减 remaining。
- 测试覆盖周五 +1、节假日跳过、days=0。
