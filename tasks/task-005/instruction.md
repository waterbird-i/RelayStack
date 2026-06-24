# 移除 Markdown front matter 灰度开关

真实来源：`comate-stack-fe` commit `aecb886378`。

目标：Markdown front matter 预览对所有用户生效，不再按用户名灰度。

要求：

1. `src/components/icode/Markdown/index.tsx` 不再引用 `useCurrentUserName`。
2. 移除 `enableFrontMatterPreview` 白名单判断。
3. 直接对 `content` 调用 `parseMarkdownFrontMatter(content)`。
4. 保留正文渲染和 front matter 预览组件。

完成后运行：

```bash
bash test.sh
```

