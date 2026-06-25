# 已知信息

- 入口文件：`src/ci/junit_summary.py`。
- 根因：只看单个 suite attribute，没有递归所有 testsuite。
- stdlib `xml.etree.ElementTree` 足够。
- 小心不要重复统计父 testsuites 聚合属性和子 testsuite 属性。
