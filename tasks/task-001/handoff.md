# 已知信息

- 只需要改 `packages/vite/src/node/server/environmentState.js`。
- bug 根因是把缓存值本身当作命中判断。
- `WeakMap.prototype.has` 可以区分“未缓存”和“缓存了 falsy 值”。
- 不需要新增依赖，也不需要重构缓存结构。

