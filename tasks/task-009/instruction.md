# 修复 Promise 缓存重试

来源/场景：企业 API client 常见的请求合并缓存问题：并发请求要 coalesce，
但失败不能永久污染缓存。

目标：`src/cache/promiseCache.js` 当前会缓存 rejected promise，导致第一次临时失败后
同 key 后续请求永远失败。

要求：

1. 只修改 `src/cache/promiseCache.js`。
2. 同一个 key 的并发 loader 必须只调用一次。
3. fulfilled promise 可以继续复用。
4. rejected promise 必须从缓存删除，允许下一次重新调用 loader。
5. 不新增依赖。

完成后运行：

```bash
bash test.sh
```
