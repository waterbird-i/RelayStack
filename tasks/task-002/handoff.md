# 已知信息

- 相关文件只有 `src/utils/comatemobile/url.ts` 和 `src/index.tsx`。
- 旧代码问题是 `window.location.pathname.includes('/comatemobile')` 太宽松。
- 精确规则应是 `/devops/icode/comatemobile` 或其子路径。
- 不需要改路由表，也不需要处理其他 app 的 basename。

