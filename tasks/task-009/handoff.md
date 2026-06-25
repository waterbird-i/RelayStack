# 已知信息

- 入口文件：`src/cache/promiseCache.js`。
- 根因：`this.cache.set(key, promise)` 后没有在 rejected 时删除。
- 最小修复是在 promise 上挂 `catch`，删除当前 key 后继续抛出原错误。
- 注意不要破坏并发请求合并。
