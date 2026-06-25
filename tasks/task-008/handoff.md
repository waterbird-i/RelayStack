# 已知信息

- 入口文件：`src/http/retryAfter.js`。
- 根因：`parseInt` 会接受部分数字，也完全不处理 RFC1123 HTTP-date。
- 用正则判断纯数字，再用 `Date.parse` 处理日期即可。
- 不需要新增依赖。
