# 收敛 comatemobile 路径判断

真实来源：`comate-stack-fe` commit `b9a5078e76`。

目标：避免普通评审文件路径中出现 `comatemobile` 字符串时，被误判成移动端入口。

要求：

1. 在 `src/utils/comatemobile/url.ts` 提供共享函数 `isComateMobilePath`。
2. 路径只允许精确匹配 `/devops/icode/comatemobile` 或它的子路径。
3. `src/index.tsx` 使用共享函数，不再直接 `includes('comatemobile')`。
4. `ensureHiddenFrameworkHeaderInCurrentUrl` 也复用共享函数。

完成后运行：

```bash
bash test.sh
```

