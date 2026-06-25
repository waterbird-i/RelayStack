# 修复 semver caret range

来源/场景：npm / package manager 依赖解析中常见的 `^` range 边界问题。

目标：`src/semver/caret.js` 当前用字符串前缀判断，错误处理 `^1.2.3` 和 `^0.2.3`。

要求：

1. 只修改 `src/semver/caret.js`。
2. 支持普通版本 `MAJOR.MINOR.PATCH`。
3. `^1.2.3` 表示 `>=1.2.3 <2.0.0`。
4. `^0.2.3` 表示 `>=0.2.3 <0.3.0`。
5. `^0.0.3` 表示 `>=0.0.3 <0.0.4`。
6. 不需要支持 prerelease 或复杂 range。

完成后运行：

```bash
bash test.sh
```
