# 修复部署 reconciler

来源/场景：Kubernetes/operator、发布平台和配置中心常见的 desired/current 差异计算问题。

目标：`src/deploy/reconciler.js` 当前按数组下标比较 desired/current，
服务顺序变化会被误判成更新，删除也不稳定。

要求：

1. 只修改 `src/deploy/reconciler.js`。
2. 以 `name` 作为服务身份。
3. desired 有、current 没有：输出 `{ type: 'create', name }`。
4. 两边都有但 `image` 或 `replicas` 不同：输出 `{ type: 'update', name, before, after }`。
5. current 有、desired 没有：输出 `{ type: 'delete', name }`。
6. 输出顺序：先按 desired 顺序输出 create/update，再按 current 顺序输出 delete。

完成后运行：

```bash
bash test.sh
```
