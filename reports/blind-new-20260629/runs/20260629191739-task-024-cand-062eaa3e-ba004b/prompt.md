你是接手 agent。先读下面的 RelayStack handoff，再执行任务。

不要重复探索 handoff 中已经明确给出的文件和事实。

## RelayStack handoff

# Handoff Snapshot: task-024

生成时间：2026-06-29 19:15:10

## 1. 当前目标
- 本轮目标：修复 NDJSON streaming parser
- 当前阶段：接手执行
- 负责人：benchmark-rs-handoff
- 是否可继续：是

## 2. 工作区状态
- 工作区：`/private/var/folders/bv/zq75bmmj17z8r1jg1y2hnf080000gn/T/rsbench-task-024-ehyvd9yf`
- 分支：master
- 最近提交：
未发现
- 未提交变更：
```text
?? src/
```
- diff 统计：
未发现
- 主要改动文件：
```text
src/
```

## 3. 已完成
- # 已知信息

- 已知入口文件：`src/streaming/ndjson.py`。
- 根因：stream chunk 边界不等于行边界。
- 最小实现维护 buffer，每次只解析 `\n` 前的完整行。
- 测试覆盖跨 chunk、空行、末尾无换行。

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

- 已知入口文件：`src/streaming/ndjson.py`。
- 根因：stream chunk 边界不等于行边界。
- 最小实现维护 buffer，每次只解析 `\n` 前的完整行。
- 测试覆盖跨 chunk、空行、末尾无换行。

## instruction.md

# 修复 NDJSON streaming parser

来源/场景：日志采集、消息队列 consumer 和 LLM streaming 输出中常见的 chunk 边界问题。

目标：`src/streaming/ndjson.py` 当前按每个 chunk 独立 split line，跨 chunk 的 JSON 行会解析失败。

要求：

1. 只修改 `src/streaming/ndjson.py`。
2. 支持 JSON 行跨 chunk。
3. 忽略空行。
4. 输入结束时如果还有完整的最后一行但没有换行，也要解析。
5. 如果剩余 buffer 不是合法 JSON，应抛出原始 `json.JSONDecodeError`。

完成后运行：

```bash
bash test.sh
```



## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。