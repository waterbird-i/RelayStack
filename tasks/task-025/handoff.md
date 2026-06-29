# 已知信息

- 已知入口文件：`src/deploy/reconciler.js`。
- 根因：数组 index 不是资源身份，重排会制造假 diff。
- 用 `Map(name -> service)` 对齐即可。
- 测试覆盖重排不变、更新、新增、删除。
