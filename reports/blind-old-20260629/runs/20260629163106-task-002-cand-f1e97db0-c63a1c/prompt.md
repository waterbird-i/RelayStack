# malformed URI 不应打断中间件

公开来源：[vitejs/vite#22714](https://github.com/vitejs/vite/pull/22714)。

目标：内存文件中间件对 `req.url` 调用 `decodeURIComponent`。当 URL 是 malformed
URI 时会抛 `URIError`，导致请求链路崩溃。请让这类请求安全跳过该中间件。

要求：

1. 修改 `packages/vite/src/node/server/middlewares/servePublicMiddleware.js`。
2. malformed URL 不应抛异常。
3. malformed URL 应调用 `next()`。
4. 正常 URL 仍然能命中内存文件并调用 `res.end(content)`。

完成后运行：

```bash
bash test.sh
```


## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。