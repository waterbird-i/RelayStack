# 修复迁移计划排序

来源/场景：数据库迁移工具常见问题：字符串排序让 `10_` 排在 `2_` 前面，
重复版本也未检测。

目标：`src/migrations/planner.js` 当前直接 `files.sort()`。

要求：

1. 只修改 `src/migrations/planner.js`。
2. 文件名格式是 `<number>_<name>.sql`。
3. 按 number 数值升序排序。
4. 同一个 number 出现多次必须抛出 `duplicate migration version`。
5. 非法文件名抛出 `invalid migration name`。

完成后运行：

```bash
bash test.sh
```
