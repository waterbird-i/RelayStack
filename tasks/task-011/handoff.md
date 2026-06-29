# 已知信息

- 已知入口文件：`src/markdown/frontmatter.js`。
- 根因：`indexOf('---')` 没有限制必须在文件开头、单独一行。
- 不需要引入 YAML parser。
- 测试覆盖有 front matter、正文中 `---`、缺失结束线。
