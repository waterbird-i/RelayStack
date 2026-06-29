# 已知信息

- 已知入口文件：`src/semver/caret.js`。
- 根因：semver caret 不是字符串前缀匹配，尤其 0.x 有特殊上界。
- 最小实现：parse 三段整数，比较 `version >= lower && version < upper`。
- 测试覆盖 1.x、0.2.x、0.0.x。
