任务：修复 Multi-SWE-bench 实例 darkreader__darkreader-7241。
上游标题：Fix: parser should ignore Base64 padding within CSS
已知入口文件：`src/generators/utils/parse.ts`。
问题线索：CSS fixes 配置块分隔符应只匹配独立成行的 `==...==`，不要匹配 Base64 padding 中的 `=`。
建议验证：围绕 `indexSitesFixesConfig` 增加或运行 parser 相关测试；最终以 Multi-SWE-bench 官方 harness 为准。