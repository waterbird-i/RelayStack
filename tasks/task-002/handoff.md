# 已知信息

- 已知入口文件：`packages/vite/src/node/server/middlewares/servePublicMiddleware.js`。
- 只需要改 `servePublicMiddleware.js`。
- 根因是 `decodeURIComponent(req.url)` 对 malformed URI 直接抛错。
- 最小修法是捕获 `URIError`，无法解码时 `next()`。
- 不需要处理静态文件读取、MIME 类型或 HTTP 缓存。

