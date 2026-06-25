# 已知信息

- 只需要改 `packages/router-dev/vite/optimizeDeps.js`。
- `react` 是必需依赖，应始终 include。
- `@mdx-js/mdx` 和 `vite-tsconfig-paths` 是可选依赖。
- resolver 抛错表示当前项目不能解析该可选包，跳过即可。

