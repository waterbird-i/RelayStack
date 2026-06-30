你是接手 agent。先读下面的 RelayStack handoff，再执行任务。

不要重复探索 handoff 中已经明确给出的文件和事实。

## RelayStack handoff

# Handoff Snapshot: task-005

生成时间：2026-06-29 16:59:17

## 1. 当前目标
- 本轮目标：CLI 有文件参数时优先读文件
- 当前阶段：接手执行
- 负责人：benchmark-rs-handoff
- 是否可继续：是

## 2. 工作区状态
- 工作区：`/private/var/folders/bv/zq75bmmj17z8r1jg1y2hnf080000gn/T/rsbench-task-005-idzh5etv`
- 分支：master
- 最近提交：
未发现
- 未提交变更：
```text
?? bin/
```
- diff 统计：
未发现
- 主要改动文件：
```text
bin/
```

## 3. 已完成
- # 已知信息

- 已知入口文件：`bin/marked.js`。
- 只需要改 `bin/marked.js`。
- 最小 Markdown 转换只需要保留现有 `# title` 到 `<h1>` 的行为。
- `process.argv` 前两项是 node 和脚本路径，不能当用户输入。
- 不需要实现完整 CLI 参数解析器。

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

- 已知入口文件：`bin/marked.js`。
- 只需要改 `bin/marked.js`。
- 最小 Markdown 转换只需要保留现有 `# title` 到 `<h1>` 的行为。
- `process.argv` 前两项是 node 和脚本路径，不能当用户输入。
- 不需要实现完整 CLI 参数解析器。

## instruction.md

# CLI 有文件参数时优先读文件

公开来源：[markedjs/marked#3967](https://github.com/markedjs/marked/pull/3967)。

目标：Markdown CLI 同时支持 stdin 和文件路径。当前实现把第一个用户参数当成 Markdown
字符串本身，导致 `node bin/marked.js README.md` 不会读取文件内容。

要求：

1. 修改 `bin/marked.js`。
2. 有文件参数时读取该文件内容。
3. 没有文件参数时读取 stdin。
4. 参数处理必须跳过 `node` 和脚本路径，只看用户传入的 argv。

完成后运行：

```bash
bash test.sh
```




## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。