# 第三方权威题源 Clean A/B 重测报告（2026-06-29）

## 结论

上一轮报告不能证明“用了 RelayStack skill 导致更慢”，因为 baseline 不是 clean baseline。

本轮已重新生成 clean A/B patch JSONL：

- `baseline`：无 skill、无 subagent，协议合规。
- `relaystack_handoff`：只读取 `rs-handoff/SKILL.md`，无其他 skill、无 subagent，协议合规。
- 两组生成的 patch 完全相同。
- clean agent 生成阶段里，`relaystack_handoff` 比 baseline 少耗时 `35.830s`。

官方 Multi-SWE-bench harness 尚未完成：Docker Desktop API 返回 503 / `docker version` 卡住。
因此本报告只把 clean agent 生成链路作为有效结论，不把官方 resolved 分数伪造成已完成。

## 题源

- 数据集：`ByteDance-Seed/Multi-SWE-bench-flash`
- instance：`darkreader__darkreader-7241`
- 上游仓库：`darkreader/darkreader`
- PR：`7241`
- base commit：见 `reports/multi-swe-clean-20260629/dataset.jsonl`
- patch JSONL：
  - `reports/multi-swe-clean-20260629/baseline.jsonl`
  - `reports/multi-swe-clean-20260629/relaystack_handoff.jsonl`

## 协议审计

```text
baseline clean: True
relaystack_handoff only rs-handoff: True
```

baseline forbidden markers：

```json
{
  "skill_context": false,
  "skill_file_read": false,
  "spawn_agent": false,
  "global_skill_path": false,
  "ponytail": false,
  "typescript_write": false,
  "non_handoff_skill": false
}
```

handoff forbidden markers：

```json
{
  "skill_context": false,
  "skill_file_read": true,
  "spawn_agent": false,
  "global_skill_path": false,
  "ponytail": false,
  "typescript_write": false,
  "non_handoff_skill": false
}
```

说明：handoff 组的 `skill_file_read=true` 是预期行为，因为它只读取了
`/private/tmp/.../skills/rs-handoff/SKILL.md`；`non_handoff_skill=false` 表示未读取其他 skill。

## Agent 指标

| 组别 | 耗时 | tokens | input | cached input | output | reasoning output | command 启动 | file changes | patch bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | 314.039s | 992,884 | 987,729 | 805,760 | 5,155 | 1,642 | 27 | 1 | 558 |
| `relaystack_handoff` | 278.209s | 306,137 | 301,595 | 243,968 | 4,542 | 2,040 | 17 | 1 | 558 |

对比：

- handoff 耗时 delta：`-35.83s`
- handoff input tokens delta：`-686,134`
- handoff cached input tokens delta：`-561,792`
- handoff output tokens delta：`-613`
- handoff command 启动 delta：`-10`
- patch bytes delta：`0`

## Patch 对比

两组 patch 完全一致：

```diff
diff --git a/src/generators/utils/parse.ts b/src/generators/utils/parse.ts
index dce4ad0..d660c40 100644
--- a/src/generators/utils/parse.ts
+++ b/src/generators/utils/parse.ts
@@ -143,7 +143,7 @@ export function indexSitesFixesConfig<T extends SiteProps>(text: string): SitePr
 
     let recordStart = 0;
     // Delimiter between two blocks
-    const delimiterRegex = /\s*={2,}\s*/gm;
+    const delimiterRegex = /^[^\S\n]*={2,}[^\S\n]*$/gm;
     let delimiter: RegExpMatchArray;
     let count = 0;
     while ((delimiter = delimiterRegex.exec(text))) {

```

## 官方 Harness 状态

状态：`blocked_docker_desktop_unavailable`

阻塞原因：Docker Desktop API returned 503 Service Unavailable / docker version hung after app launch; clean patch JSONL was generated but official harness could not complete in this environment.

已尝试：

1. 沙箱内运行 harness：Docker socket `Operation not permitted`。
2. 沙箱外运行 harness：Docker API 返回 `503 Service Unavailable (Docker Desktop is unable to start)`。
3. `open -a Docker` 后轮询 `docker version`：进程长时间无响应，已中断。

## 原始产物

- 执行汇总：`reports/multi-swe-clean-20260629/summary.json`
- baseline agent 事件流：`reports/multi-swe-clean-20260629/baseline-agent-output.jsonl`
- handoff agent 事件流：`reports/multi-swe-clean-20260629/relaystack_handoff-agent-output.jsonl`
- 机器可读报告：`reports/authoritative-clean-ab-20260629.json`
