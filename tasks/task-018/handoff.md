# 已知信息

- 已知入口文件：`src/router/matcher.js`。
- 根因：没有路径 normalize。
- 可以用 WHATWG `URL`，但要兼容相对路径；给一个 dummy origin 即可。
- 不需要写完整 router。
