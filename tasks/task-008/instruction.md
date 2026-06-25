# 修复 Retry-After 解析

来源/场景：[urllib3](https://github.com/urllib3/urllib3) / HTTP 客户端重试中常见的
`Retry-After` 兼容问题。

目标：`src/http/retryAfter.js` 当前只支持整数秒，还会把 `10ms` 当成 10 秒。

要求：

1. 只修改 `src/http/retryAfter.js`。
2. 纯数字 header 按秒转毫秒。
3. HTTP-date header 按 `date - now` 转毫秒。
4. 过去的日期返回 0。
5. 非法 header 返回 0，`10ms` 这类非纯数字不能按 10 秒处理。

完成后运行：

```bash
bash test.sh
```
