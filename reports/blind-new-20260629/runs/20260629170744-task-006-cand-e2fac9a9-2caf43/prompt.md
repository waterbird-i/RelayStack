# 修复 dotenv 解析器

来源/场景：[python-dotenv](https://github.com/theskumar/python-dotenv) 类配置解析问题，
企业部署中也常见带 `=` 的 token 和带 `#` 的密码。

目标：`src/config/dotenv.js` 现在用简单 split 和全局 `#` 截断解析 `.env`，
会把 URL token、quoted value 解析错。

要求：

1. 只修改 `src/config/dotenv.js`。
2. key 需要 trim。
3. value 只按第一个 `=` 切分，保留后续 `=`。
4. 未加引号的 value 支持 ` # comment` 行尾注释。
5. 单引号或双引号内的 `#` 必须保留。
6. 空值必须保留为空字符串。

完成后运行：

```bash
bash test.sh
```

## Benchmark metrics
完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：
{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}
steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。
repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。