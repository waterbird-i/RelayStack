# 发布中 Skill 禁止再次发布

真实来源：`comate-stack-fe` commit `e4e4819872`。

目标：Skill 处于发布中状态时，展示草稿检测结果，并且更多菜单里不再出现“发布”入口。

要求：

1. `SkillHeader.tsx` 中的 `SkillStatusTag` 传入 `checkDraftScannerResult`。
2. `SkillHeaderActions.tsx` 中更多菜单的发布入口排除 `SkillStatus.PUBLISHING`。
3. 不要影响草稿、已发布和普通可发布状态的其他菜单项。

完成后运行：

```bash
bash test.sh
```

