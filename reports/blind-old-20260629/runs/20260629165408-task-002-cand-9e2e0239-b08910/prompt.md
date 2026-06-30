你是接手 agent。先读下面的 RelayStack handoff，再执行任务。

不要重复探索 handoff 中已经明确给出的文件和事实。

## RelayStack handoff

# Handoff Snapshot: task-002

生成时间：2026-06-29 16:51:33

## 1. 当前目标
- 本轮目标：malformed URI 不应打断中间件
- 当前阶段：接手执行
- 负责人：benchmark-rs-handoff
- 是否可继续：是

## 2. 工作区状态
- 工作区：`/private/var/folders/bv/zq75bmmj17z8r1jg1y2hnf080000gn/T/rsbench-task-002-by5kgwrk`
- 分支：master
- 最近提交：
未发现
- 未提交变更：
```text
?? packages/
```
- diff 统计：
未发现
- 主要改动文件：
```text
packages/
```

## 3. 已完成
- # 已知信息

- 已知入口文件：`packages/vite/src/node/server/middlewares/servePublicMiddleware.js`。
- 只需要改 `servePublicMiddleware.js`。
- 根因是 `decodeURIComponent(req.url)` 对 malformed URI 直接抛错。
- 最小修法是捕获 `URIError`，无法解码时 `next()`。
- 不需要处理静态文件读取、MIME 类型或 HTTP 缓存。

## 4. 未完成
- 未发现

## 5. 阻塞与风险
- 阻塞：未发现
- 风险：未发现
- 需要用户确认：未发现

## 6. 项目上下文
- README：
未发现
- docs：
未发现
- handoff：
未发现
- skills：
未发现

## 7. Agent 交接信息
- 参与代理与结论：
- 未发现
- Agent records：
未发现
- 可复用发现：
- 未发现
- 修改原因：未提供

## 8. 下一步
1. 下一步动作：按 instruction.md 完成最小实现
2. 验证方式：bash test.sh
3. 完成标志：未提供

## 9. 复现命令
```bash
git status --short
git diff --stat
git diff --name-only
git log --oneline -n 5
```

## 10. Agent 并行边界
未发现


## 任务补充

# 已知信息

- 已知入口文件：`packages/vite/src/node/server/middlewares/servePublicMiddleware.js`。
- 只需要改 `servePublicMiddleware.js`。
- 根因是 `decodeURIComponent(req.url)` 对 malformed URI 直接抛错。
- 最小修法是捕获 `URIError`，无法解码时 `next()`。
- 不需要处理静态文件读取、MIME 类型或 HTTP 缓存。

## instruction.md

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