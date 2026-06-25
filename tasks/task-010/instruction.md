# 修复依赖排序循环检测

来源/场景：包管理器、CI pipeline 和企业发布编排中常见的依赖图排序问题。

目标：`src/deps/dependency_order.py` 现在只用 visited set，遇到循环依赖时不会报出
有用错误，也可能返回不完整结果。

要求：

1. 只修改 `src/deps/dependency_order.py`。
2. 无环图返回依赖优先的拓扑顺序。
3. 循环图必须抛出 `ValueError`。
4. 错误信息包含循环路径，例如 `api -> db -> auth -> api`。
5. 输出顺序需要稳定，按输入字典顺序遍历即可。

完成后运行：

```bash
bash test.sh
```
