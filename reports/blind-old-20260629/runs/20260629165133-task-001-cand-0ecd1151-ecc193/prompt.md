你是接手 agent。先读下面的 RelayStack handoff，再执行任务。

不要重复探索 handoff 中已经明确给出的文件和事实。

## RelayStack handoff

# Handoff Snapshot: task-001

生成时间：2026-06-29 16:48:11

## 1. 当前目标
- 本轮目标：缓存 falsy 的环境状态
- 当前阶段：接手执行
- 负责人：benchmark-rs-handoff
- 是否可继续：是

## 2. 工作区状态
- 工作区：`/private/var/folders/bv/zq75bmmj17z8r1jg1y2hnf080000gn/T/rsbench-task-001-6vgx0jcf`
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

- 已知入口文件：`packages/vite/src/node/server/environmentState.js`。
- 只需要改 `packages/vite/src/node/server/environmentState.js`。
- bug 根因是把缓存值本身当作命中判断。
- `WeakMap.prototype.has` 可以区分“未缓存”和“缓存了 falsy 值”。
- 不需要新增依赖，也不需要重构缓存结构。

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

- 已知入口文件：`packages/vite/src/node/server/environmentState.js`。
- 只需要改 `packages/vite/src/node/server/environmentState.js`。
- bug 根因是把缓存值本身当作命中判断。
- `WeakMap.prototype.has` 可以区分“未缓存”和“缓存了 falsy 值”。
- 不需要新增依赖，也不需要重构缓存结构。

## instruction.md

# 缓存 falsy 的环境状态

公开来源：[vitejs/vite#22715](https://github.com/vitejs/vite/pull/22715)。

目标：环境状态缓存现在用 truthy 判断命中，导致 `false`、`0`、`null` 这类
falsy 初始化结果不会被缓存，后续读取会重复调用初始化函数。

要求：

1. 修改 `packages/vite/src/node/server/environmentState.js`。
2. 用 cache 是否已有 key 判断命中，而不是用缓存值的 truthiness。
3. `initial()` 返回 `false` 时，第二次读取也必须直接返回缓存值。
4. 不改变不同 environment 之间互相隔离的行为。

完成后运行：

```bash
bash test.sh
```



## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。