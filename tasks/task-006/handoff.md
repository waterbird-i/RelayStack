# 已知信息

- 已知入口文件：`src/config/dotenv.js`。
- 根因：当前实现用 `line.split('=')` 和 `value.indexOf('#')`，没有区分
  第一个等号、quoted value 和 inline comment。
- 不需要引入 dotenv 依赖，只需要补足当前小 parser 的边界。
- 测试覆盖：URL 中的 `=`、quoted `#`、未 quoted inline comment、空值。
