你是接手 agent。先读下面的 RelayStack handoff，再执行任务。

不要重复探索 handoff 中已经明确给出的文件和事实。

## RelayStack handoff

# Handoff Snapshot: task-019

生成时间：2026-06-29 19:00:03

## 1. 当前目标
- 本轮目标：修复迁移计划排序
- 当前阶段：接手执行
- 负责人：benchmark-rs-handoff
- 是否可继续：是

## 2. 工作区状态
- 工作区：`/private/var/folders/bv/zq75bmmj17z8r1jg1y2hnf080000gn/T/rsbench-task-019-kkk6f0p3`
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

- 已知入口文件：`src/migrations/planner.js`。
- 根因：字符串排序不等于版本号排序。
- 正则提取数字版本即可，不需要读 SQL 文件。
- 测试覆盖排序、重复版本、非法名称。

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

- 已知入口文件：`src/migrations/planner.js`。
- 根因：字符串排序不等于版本号排序。
- 正则提取数字版本即可，不需要读 SQL 文件。
- 测试覆盖排序、重复版本、非法名称。

## instruction.md

# 修复迁移计划排序

来源/场景：数据库迁移工具常见问题：字符串排序让 `10_` 排在 `2_` 前面，
重复版本也未检测。

目标：`src/migrations/planner.js` 当前直接 `files.sort()`。

要求：

1. 只修改 `src/migrations/planner.js`。
2. 文件名格式是 `<number>_<name>.sql`。
3. 按 number 数值升序排序。
4. 同一个 number 出现多次必须抛出 `duplicate migration version`。
5. 非法文件名抛出 `invalid migration name`。

完成后运行：

```bash
bash test.sh
```



## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。