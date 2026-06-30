# 第三方权威题源 A/B 重测报告（项目 skills 隔离，2026-06-29）

## 结论

本轮满足用户指定协议：

- `baseline`：不使用任何 skill，不启动 subagent。
- `relaystack_handoff`：仅可使用本项目 `skills/` 下的 RelayStack skill，不使用全局、插件或第三方 skill，不启动 subagent。

重测 agent 生成链路已完成，协议审计通过；修复 Docker Desktop daemon 后，官方 Multi-SWE-bench harness 也已补跑完成。两组均为 `1/1 resolved`。

## 题源

- 数据集：`ByteDance-Seed/Multi-SWE-bench-flash`
- instance：`darkreader__darkreader-7241`
- 上游仓库：`darkreader/darkreader`
- PR：`7241`
- run dir：`reports/multi-swe-project-skills-20260629`

## 协议审计

```text
baseline clean: True
relaystack_handoff project skills only: True
```

baseline 读取的 skill：

```json
[]
```

handoff 读取的 skill：

```json
[
  "/private/tmp/codex-relaystack_handoff-k4ydtkw4/skills/rs-handoff/SKILL.md",
  "/private/tmp/codex-relaystack_handoff-k4ydtkw4/skills/rs-issue-fix/SKILL.md"
]
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
  "non_project_skill": false
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
  "non_project_skill": false
}
```

说明：handoff 组 `skill_file_read=true` 是预期行为；它实际只读取了临时 `CODEX_HOME` 中复制自本项目的 `rs-handoff` 和 `rs-issue-fix`。

## Agent 指标

| 组别 | 耗时 | tokens | input | cached input | output | reasoning output | command 启动 | file changes | patch bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | 347.771s | 822,230 | 814,729 | 661,888 | 7,501 | 3,028 | 32 | 2 | 1016 |
| `relaystack_handoff` | 282.844s | 280,621 | 275,515 | 216,448 | 5,106 | 2,420 | 16 | 2 | 565 |

对比：

- handoff 耗时 delta：`-64.927s`
- handoff tokens delta：`-541,609`
- handoff input tokens delta：`-539,214`
- handoff output tokens delta：`-2,395`
- handoff command 启动 delta：`-16`
- patch bytes delta：`-451`

## Patch 摘要

baseline patch：

```diff
diff --git a/src/generators/utils/parse.ts b/src/generators/utils/parse.ts
index dce4ad0..97452b1 100644
--- a/src/generators/utils/parse.ts
+++ b/src/generators/utils/parse.ts
@@ -21,7 +21,7 @@ export interface SitesFixesParserOptions<T> {
 export function parseSitesFixesConfig<T extends SiteProps>(text: string, options: SitesFixesParserOptions<T>) {
     const sites: T[] = [];
 
-    const blocks = text.replace(/\r/g, '').split(/^\s*={2,}\s*$/gm);
+    const blocks = text.replace(/\r/g, '').split(/^\s*={3,}\s*$/gm);
     blocks.forEach((block) => {
         const lines = block.split('\n');
         const commandIndices: number[] = [];
@@ -143,7 +143,7 @@ export function indexSitesFixesConfig<T extends SiteProps>(text: string): SitePr
 
     let recordStart = 0;
     // Delimiter between two blocks
-    const delimiterRegex = /\s*={2,}\s*/gm;
+    const delimiterRegex = /^\s*={3,}\s*$/gm;
     let delimiter: RegExpMatchArray;
     let count = 0;
     while ((delimiter = delimiterRegex.exec(text))) {

```

handoff patch：

```diff
diff --git a/src/generators/utils/parse.ts b/src/generators/utils/parse.ts
index dce4ad0..48dcff0 100644
--- a/src/generators/utils/parse.ts
+++ b/src/generators/utils/parse.ts
@@ -143,7 +143,7 @@ export function indexSitesFixesConfig<T extends SiteProps>(text: string): SitePr
 
     let recordStart = 0;
     // Delimiter between two blocks
-    const delimiterRegex = /\s*={2,}\s*/gm;
+    const delimiterRegex = /^[^\S\r\n]*={2,}[^\S\r\n]*\r?$/gm;
     let delimiter: RegExpMatchArray;
     let count = 0;
     while ((delimiter = delimiterRegex.exec(text))) {

```

## 官方 Harness 状态

状态：`official_evaluated`

官方结果：

| 组别 | completed | resolved | unresolved | error |
| --- | ---: | ---: | ---: | ---: |
| `baseline` | 1 | 1 | 0 | 0 |
| `relaystack_handoff` | 1 | 1 | 0 | 0 |

Docker 修复记录：旧 `com.docker.backend` 进程卡死且对 TERM 无响应；强制结束该单进程并重新启动 Docker Desktop 后，Docker Server API 恢复，随后两组官方 harness 均完成。

## 原始产物

- 执行汇总：`reports/multi-swe-project-skills-20260629/summary.json`
- baseline patch JSONL：`reports/multi-swe-project-skills-20260629/baseline.jsonl`
- handoff patch JSONL：`reports/multi-swe-project-skills-20260629/relaystack_handoff.jsonl`
- baseline agent 事件流：`reports/multi-swe-project-skills-20260629/baseline-agent-output.jsonl`
- handoff agent 事件流：`reports/multi-swe-project-skills-20260629/relaystack_handoff-agent-output.jsonl`
- baseline 官方报告：`reports/multi-swe-project-skills-20260629/baseline-output/final_report.json`
- handoff 官方报告：`reports/multi-swe-project-skills-20260629/relaystack_handoff-output/final_report.json`
- 机器可读报告：`reports/authoritative-project-skills-ab-20260629.json`
