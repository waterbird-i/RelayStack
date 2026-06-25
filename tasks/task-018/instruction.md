# 修复路由匹配

来源/场景：Web router / API gateway 常见路径规范化问题。

目标：`src/router/matcher.js` 当前直接字符串比较，导致 `/users/` 和 `/users?tab=all`
不能匹配 `/users`。

要求：

1. 只修改 `src/router/matcher.js`。
2. 比较时忽略 query string 和 hash。
3. 非 root 路径忽略末尾 `/`。
4. root `/` 仍然只匹配 root。
5. 不需要实现动态参数。

完成后运行：

```bash
bash test.sh
```
