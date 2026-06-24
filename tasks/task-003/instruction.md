# 隐藏空间 Skill 禁止分享

真实来源：`comate-stack-fe` commit `c18efce167`。

目标：Skill 位于隐藏空间时，分享按钮不可点击，并提示用户先迁移空间。

要求：

1. 在 `SkillHeaderActions.tsx` 里给“分享”按钮绑定 `disabled={skill.isHiddenWorkspace}`。
2. 隐藏空间时给 `disabledReason`，文案必须同时包含“隐藏空间”和“迁移”。
3. 在按钮样式里补齐 `&:disabled` 禁用态。
4. 不要改分享函数 `handleShare` 的正常路径。

完成后运行：

```bash
bash test.sh
```

