# 已知信息

- 入口文件：`src/ratelimit/token_bucket.py`。
- 根因：`int(now - updated_at)` 丢掉小数秒。
- 真实限流不能依赖每秒整数 tick。
- 测试覆盖 0.5 秒补 1 token、capacity 上限、时钟回拨。
