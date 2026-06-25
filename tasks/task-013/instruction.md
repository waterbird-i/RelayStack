# 修复 feature flag 显式 false

来源/场景：企业灰度发布中常见的 flag fallback bug：显式关闭被默认值覆盖。

目标：`src/flags/feature_flags.py` 当前用 truthy fallback，导致 `False` 和 `0`
被当成缺失。

要求：

1. 只修改 `src/flags/feature_flags.py`。
2. flags 中存在 key 时必须使用该值，即使是 `False`。
3. env 中 `FEATURE_<NAME>` 存在时优先级最高。
4. env 字符串支持 `true/false/1/0/yes/no/on/off`。
5. 缺失时返回 default。

完成后运行：

```bash
bash test.sh
```
