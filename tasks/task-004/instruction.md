# 可选依赖不存在时不要加入预构建列表

公开来源：[remix-run/react-router#11861](https://github.com/remix-run/react-router/pull/11861)。

目标：工具链配置无条件把可选依赖加入 `optimizeDeps.include`。当当前项目没有安装
这些可选包时，预构建配置会引用不存在的依赖。

要求：

1. 修改 `packages/router-dev/vite/optimizeDeps.js`。
2. 只有 resolver 能解析可选依赖时，才加入 `include`。
3. resolver 抛错时安全跳过，不影响必需依赖。
4. 已安装的可选依赖仍然会被加入。

完成后运行：

```bash
bash test.sh
```

