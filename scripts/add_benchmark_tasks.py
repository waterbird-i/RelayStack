#!/usr/bin/env python3
from __future__ import annotations

import os
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"


def clean(text: str) -> str:
    return textwrap.dedent(text).strip() + "\n"


TASK_DATA = {
    "task-006": {
        "difficulty": "easy",
        "summary": "dotenv 解析保留等号和引号内 #",
        "instruction": """
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
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/config/dotenv.js`。
        - 根因：当前实现用 `line.split('=')` 和 `value.indexOf('#')`，没有区分
          第一个等号、quoted value 和 inline comment。
        - 不需要引入 dotenv 依赖，只需要补足当前小 parser 的边界。
        - 测试覆盖：URL 中的 `=`、quoted `#`、未 quoted inline comment、空值。
        """,
        "files": {
            "src/config/dotenv.js": """
            function stripComment(value) {
              const index = value.indexOf('#');
              return index === -1 ? value.trim() : value.slice(0, index).trim();
            }

            function unquote(value) {
              if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
                return value.slice(1, -1);
              }
              return value;
            }

            function parseEnv(text) {
              const env = {};
              for (const rawLine of text.split(/\\r?\\n/)) {
                const line = rawLine.trim();
                if (!line || line.startsWith('#')) continue;
                const parts = line.split('=');
                const key = parts[0].trim();
                const value = stripComment((parts[1] || '').trim());
                env[key] = unquote(value);
              }
              return env;
            }

            module.exports = { parseEnv };
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        node - <<'JS'
        const assert = require('assert');
        const { parseEnv } = require('./src/config/dotenv');

        const env = parseEnv(`
        # comment
        API_URL=https://example.test/callback?token=a=b=c
        EMPTY=
        QUOTED_HASH="abc#not-comment"
        SINGLE_HASH='x#y'
        PASSWORD=abc#def
        INLINE=value # deploy comment
        SPACED = keep me
        `);

        assert.deepStrictEqual(env, {
          API_URL: 'https://example.test/callback?token=a=b=c',
          EMPTY: '',
          QUOTED_HASH: 'abc#not-comment',
          SINGLE_HASH: 'x#y',
          PASSWORD: 'abc#def',
          INLINE: 'value',
          SPACED: 'keep me',
        });
        JS
        """,
    },
    "task-007": {
        "difficulty": "medium",
        "summary": "归档解压计划阻断 Zip Slip 路径穿越",
        "instruction": """
        # 阻断归档路径穿越

        来源/场景：[snyk/zip-slip-vulnerability](https://github.com/snyk/zip-slip-vulnerability)
        记录的 Zip Slip 类问题，企业构建系统解压制品时也常见。

        目标：`src/archive/safeExtract.js` 负责把归档 entry 映射到目标目录。
        当前实现只做 `startsWith(base)`，会漏掉 sibling-prefix 路径，也会静默丢弃非法 entry。

        要求：

        1. 只修改 `src/archive/safeExtract.js`。
        2. 目标路径必须位于 destination 内部。
        3. `../`、绝对路径、sibling prefix 都必须抛出 `unsafe path` 错误。
        4. 正常路径返回 `{ name, target }` 列表。
        5. 不需要真正解压文件。

        完成后运行：

        ```bash
        bash test.sh
        ```
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/archive/safeExtract.js`。
        - 根因：字符串前缀判断不是路径边界判断，`/tmp/outside` 会通过
          `/tmp/out` 的 startsWith 检查。
        - 建议用 `path.resolve` 后检查 `target === base || target.startsWith(base + path.sep)`。
        - 发现非法 entry 应 fail fast，不能静默过滤。
        """,
        "files": {
            "src/archive/safeExtract.js": """
            const path = require('path');

            function planExtraction(entries, destination) {
              const base = path.resolve(destination);
              return entries
                .map((entry) => ({
                  name: entry.name,
                  target: path.resolve(base, entry.name),
                }))
                .filter((entry) => entry.target.startsWith(base));
            }

            module.exports = { planExtraction };
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        node - <<'JS'
        const assert = require('assert');
        const path = require('path');
        const { planExtraction } = require('./src/archive/safeExtract');

        const dest = path.join('/tmp', 'rsbench-extract', 'out');

        assert.throws(
          () => planExtraction([{ name: '../outside.txt' }], dest),
          /unsafe path/
        );
        assert.throws(
          () => planExtraction([{ name: '/etc/passwd' }], dest),
          /unsafe path/
        );
        assert.throws(
          () => planExtraction([{ name: '../outside-prefix/file.txt' }], dest),
          /unsafe path/
        );

        const planned = planExtraction([
          { name: 'assets/app.js' },
          { name: 'nested/../ok.txt' },
        ], dest);

        assert.deepStrictEqual(planned, [
          { name: 'assets/app.js', target: path.join(dest, 'assets/app.js') },
          { name: 'nested/../ok.txt', target: path.join(dest, 'ok.txt') },
        ]);
        JS
        """,
    },
    "task-008": {
        "difficulty": "easy",
        "summary": "Retry-After 同时支持秒数和 HTTP-date",
        "instruction": """
        # 修复 Retry-After 解析

        来源/场景：[urllib3](https://github.com/urllib3/urllib3) / HTTP 客户端重试中常见的
        `Retry-After` 兼容问题。

        目标：`src/http/retryAfter.js` 当前只支持整数秒，还会把 `10ms` 当成 10 秒。

        要求：

        1. 只修改 `src/http/retryAfter.js`。
        2. 纯数字 header 按秒转毫秒。
        3. HTTP-date header 按 `date - now` 转毫秒。
        4. 过去的日期返回 0。
        5. 非法 header 返回 0，`10ms` 这类非纯数字不能按 10 秒处理。

        完成后运行：

        ```bash
        bash test.sh
        ```
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/http/retryAfter.js`。
        - 根因：`parseInt` 会接受部分数字，也完全不处理 RFC1123 HTTP-date。
        - 用正则判断纯数字，再用 `Date.parse` 处理日期即可。
        - 不需要新增依赖。
        """,
        "files": {
            "src/http/retryAfter.js": """
            function retryAfterMs(header, now = Date.now()) {
              if (!header) return 0;
              const seconds = parseInt(header, 10);
              if (!Number.isNaN(seconds)) return seconds * 1000;
              return 0;
            }

            module.exports = { retryAfterMs };
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        node - <<'JS'
        const assert = require('assert');
        const { retryAfterMs } = require('./src/http/retryAfter');

        const now = Date.parse('2026-06-24T12:00:00Z');

        assert.strictEqual(retryAfterMs('3', now), 3000);
        assert.strictEqual(
          retryAfterMs('Wed, 24 Jun 2026 12:00:05 GMT', now),
          5000
        );
        assert.strictEqual(
          retryAfterMs('Wed, 24 Jun 2026 11:59:59 GMT', now),
          0
        );
        assert.strictEqual(retryAfterMs('10ms', now), 0);
        assert.strictEqual(retryAfterMs('not-a-date', now), 0);
        JS
        """,
    },
    "task-009": {
        "difficulty": "medium",
        "summary": "Promise 缓存失败后允许后续重试",
        "instruction": """
        # 修复 Promise 缓存重试

        来源/场景：企业 API client 常见的请求合并缓存问题：并发请求要 coalesce，
        但失败不能永久污染缓存。

        目标：`src/cache/promiseCache.js` 当前会缓存 rejected promise，导致第一次临时失败后
        同 key 后续请求永远失败。

        要求：

        1. 只修改 `src/cache/promiseCache.js`。
        2. 同一个 key 的并发 loader 必须只调用一次。
        3. fulfilled promise 可以继续复用。
        4. rejected promise 必须从缓存删除，允许下一次重新调用 loader。
        5. 不新增依赖。

        完成后运行：

        ```bash
        bash test.sh
        ```
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/cache/promiseCache.js`。
        - 根因：`this.cache.set(key, promise)` 后没有在 rejected 时删除。
        - 最小修复是在 promise 上挂 `catch`，删除当前 key 后继续抛出原错误。
        - 注意不要破坏并发请求合并。
        """,
        "files": {
            "src/cache/promiseCache.js": """
            class PromiseCache {
              constructor() {
                this.cache = new Map();
              }

              get(key, loader) {
                if (this.cache.has(key)) {
                  return this.cache.get(key);
                }
                const promise = Promise.resolve().then(loader);
                this.cache.set(key, promise);
                return promise;
              }
            }

            module.exports = { PromiseCache };
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        node - <<'JS'
        const assert = require('assert');
        const { PromiseCache } = require('./src/cache/promiseCache');

        (async () => {
          const cache = new PromiseCache();
          let calls = 0;

          const a = cache.get('user:1', async () => {
            calls += 1;
            return 'ok';
          });
          const b = cache.get('user:1', async () => {
            calls += 1;
            return 'wrong';
          });

          assert.strictEqual(await a, 'ok');
          assert.strictEqual(await b, 'ok');
          assert.strictEqual(calls, 1);

          let failCalls = 0;
          await assert.rejects(
            () => cache.get('user:2', async () => {
              failCalls += 1;
              throw new Error('temporary');
            }),
            /temporary/
          );

          const recovered = await cache.get('user:2', async () => {
            failCalls += 1;
            return 'recovered';
          });

          assert.strictEqual(recovered, 'recovered');
          assert.strictEqual(failCalls, 2);
        })().catch((error) => {
          console.error(error);
          process.exit(1);
        });
        JS
        """,
    },
    "task-010": {
        "difficulty": "hard",
        "summary": "依赖排序检测循环并输出依赖优先顺序",
        "instruction": """
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
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/deps/dependency_order.py`。
        - 根因：只有 `visited`，缺少当前递归栈 `visiting`。
        - 最小修复是 DFS 时维护 path；遇到已在 path 中的节点就截取循环段报错。
        - 测试同时校验无环排序和循环错误信息。
        """,
        "files": {
            "src/deps/dependency_order.py": """
            def resolve_order(graph):
                visited = set()
                order = []

                def visit(node):
                    if node in visited:
                        return
                    visited.add(node)
                    for dep in graph.get(node, []):
                        visit(dep)
                    order.append(node)

                for node in graph:
                    visit(node)
                return order
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        python3 - <<'PY'
        from src.deps.dependency_order import resolve_order

        graph = {
            "web": ["api", "assets"],
            "api": ["db", "auth"],
            "assets": [],
            "db": [],
            "auth": ["db"],
        }
        order = resolve_order(graph)
        assert order.index("db") < order.index("api")
        assert order.index("auth") < order.index("api")
        assert order.index("api") < order.index("web")
        assert order.index("assets") < order.index("web")

        cyclic = {
            "api": ["db"],
            "db": ["auth"],
            "auth": ["api"],
        }
        try:
            resolve_order(cyclic)
        except ValueError as exc:
            message = str(exc)
            assert "api -> db -> auth -> api" in message, message
        else:
            raise AssertionError("cycle was not reported")
        PY
        """,
    },
    "task-011": {
        "difficulty": "easy",
        "summary": "Front matter 只在文件开头解析",
        "instruction": """
        # 修复 Markdown front matter 解析边界

        来源/场景：文档站、博客和企业知识库常见 front matter 解析问题。

        目标：`src/markdown/frontmatter.js` 当前会在正文中寻找任意 `---`，导致普通正文被误判成
        front matter。

        要求：

        1. 只修改 `src/markdown/frontmatter.js`。
        2. 只有文件第一行就是 `---` 时才解析 front matter。
        3. 第二个单独一行的 `---` 作为结束。
        4. 没有 front matter 时，metadata 为 `{}`，body 保持原文。
        5. YAML 不需要完整解析，只需要支持 `key: value`。

        完成后运行：

        ```bash
        bash test.sh
        ```
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/markdown/frontmatter.js`。
        - 根因：`indexOf('---')` 没有限制必须在文件开头、单独一行。
        - 不需要引入 YAML parser。
        - 测试覆盖有 front matter、正文中 `---`、缺失结束线。
        """,
        "files": {
            "src/markdown/frontmatter.js": """
            function parseMetadata(block) {
              const metadata = {};
              for (const line of block.split(/\\r?\\n/)) {
                const index = line.indexOf(':');
                if (index !== -1) {
                  metadata[line.slice(0, index).trim()] = line.slice(index + 1).trim();
                }
              }
              return metadata;
            }

            function parseFrontMatter(text) {
              const start = text.indexOf('---');
              const end = text.indexOf('---', start + 3);
              if (start === -1 || end === -1) {
                return { metadata: {}, body: text };
              }
              return {
                metadata: parseMetadata(text.slice(start + 3, end).trim()),
                body: text.slice(end + 3).replace(/^\\r?\\n/, ''),
              };
            }

            module.exports = { parseFrontMatter };
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        node - <<'JS'
        const assert = require('assert');
        const { parseFrontMatter } = require('./src/markdown/frontmatter');

        assert.deepStrictEqual(parseFrontMatter('---\\ntitle: Hello\\ndraft: false\\n---\\nBody'), {
          metadata: { title: 'Hello', draft: 'false' },
          body: 'Body',
        });

        const bodyOnly = 'Intro\\n---\\nthis is a horizontal rule\\n---\\nEnd';
        assert.deepStrictEqual(parseFrontMatter(bodyOnly), {
          metadata: {},
          body: bodyOnly,
        });

        const unfinished = '---\\ntitle: Missing end\\nBody';
        assert.deepStrictEqual(parseFrontMatter(unfinished), {
          metadata: {},
          body: unfinished,
        });
        JS
        """,
    },
    "task-012": {
        "difficulty": "medium",
        "summary": "CSV 用户导入处理 BOM、大小写去重和空行",
        "instruction": """
        # 修复 CSV 用户导入

        来源/场景：企业后台批量导入用户时常见的 CSV BOM、大小写邮箱重复和空行问题。

        目标：`src/importer/csv_import.py` 当前会把 BOM 留在 header 中，并按原始 email
        做大小写敏感去重。

        要求：

        1. 只修改 `src/importer/csv_import.py`。
        2. 支持 UTF-8 BOM。
        3. email 需要 trim 并转小写。
        4. 空 email 行跳过。
        5. 重复 email 只保留第一次出现。
        6. name 需要 trim。

        完成后运行：

        ```bash
        bash test.sh
        ```
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/importer/csv_import.py`。
        - 根因：`csv.DictReader` 读到 BOM 后 header 变成 `\\ufeffemail`；
          去重也没有做 normalize。
        - 不需要 pandas，stdlib `csv` 足够。
        - 测试覆盖 BOM、重复邮箱大小写、空邮箱、name trim。
        """,
        "files": {
            "src/importer/csv_import.py": """
            import csv
            from io import StringIO


            def import_users(text):
                users = []
                seen = set()
                reader = csv.DictReader(StringIO(text))
                for row in reader:
                    email = row.get("email", "").strip()
                    if not email or email in seen:
                        continue
                    seen.add(email)
                    users.append({
                        "email": email,
                        "name": row.get("name", "").strip(),
                    })
                return users
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        python3 - <<'PY'
        from src.importer.csv_import import import_users

        data = "\ufeffemail,name\\n Alice@Example.COM , Alice \\n,No Email\\nalice@example.com,Duplicate\\nBOB@example.com,Bob\\n"
        assert import_users(data) == [
            {"email": "alice@example.com", "name": "Alice"},
            {"email": "bob@example.com", "name": "Bob"},
        ]
        PY
        """,
    },
    "task-013": {
        "difficulty": "easy",
        "summary": "Feature flag 保留显式 false 并解析环境变量",
        "instruction": """
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
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/flags/feature_flags.py`。
        - 根因：`or` fallback 把显式 falsy 值当缺失。
        - 用 `key in dict` 判断是否存在。
        - env 解析只需要覆盖测试里的常见布尔字符串。
        """,
        "files": {
            "src/flags/feature_flags.py": """
            def is_enabled(flags, name, default=False, env=None):
                env = env or {}
                env_key = "FEATURE_" + name.upper()
                value = env.get(env_key) or flags.get(name) or default
                return bool(value)
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        python3 - <<'PY'
        from src.flags.feature_flags import is_enabled

        assert is_enabled({"new_checkout": False}, "new_checkout", default=True) is False
        assert is_enabled({"ranker": 0}, "ranker", default=True) is False
        assert is_enabled({}, "missing", default=True) is True
        assert is_enabled({"search": False}, "search", env={"FEATURE_SEARCH": "true"}) is True
        assert is_enabled({"search": True}, "search", env={"FEATURE_SEARCH": "off"}) is False
        PY
        """,
    },
    "task-014": {
        "difficulty": "hard",
        "summary": "游标分页避免插入新数据后重复/跳过",
        "instruction": """
        # 修复游标分页稳定性

        来源/场景：Feed、工单列表、消息列表常见的 cursor pagination 问题。

        目标：`src/pagination/cursor_page.py` 当前把 cursor 当 offset。
        当第一页之后有新数据插入，第二页会重复上一页数据或跳过数据。

        要求：

        1. 只修改 `src/pagination/cursor_page.py`。
        2. 输入 items 是 dict 列表，包含 `id` 和 `created_at`。
        3. 排序规则：`created_at` 倒序，`id` 倒序。
        4. cursor 必须基于最后一条记录的 `(created_at, id)`，不能基于 offset。
        5. 返回 `(page_items, next_cursor)`。
        6. 最后一页 `next_cursor` 为 `None`。

        完成后运行：

        ```bash
        bash test.sh
        ```
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/pagination/cursor_page.py`。
        - 根因：offset cursor 在数据集变化后不稳定。
        - 可以用 JSON/base64 或简单字符串保存 `created_at` 和 `id`。
        - 测试会在第一页后插入新记录，第二页不能重复第一页最后一条。
        """,
        "files": {
            "src/pagination/cursor_page.py": """
            def page(items, cursor=None, limit=2):
                start = int(cursor or 0)
                ordered = sorted(items, key=lambda item: (-item["created_at"], item["id"]))
                batch = ordered[start:start + limit]
                next_cursor = str(start + limit) if start + limit < len(ordered) else None
                return batch, next_cursor
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        python3 - <<'PY'
        from src.pagination.cursor_page import page

        items = [
            {"id": "d", "created_at": 30},
            {"id": "c", "created_at": 20},
            {"id": "b", "created_at": 20},
            {"id": "a", "created_at": 10},
        ]

        first, cursor = page(items, limit=2)
        assert [item["id"] for item in first] == ["d", "c"]
        assert cursor is not None

        items.append({"id": "e", "created_at": 40})
        second, cursor = page(items, cursor=cursor, limit=2)
        assert [item["id"] for item in second] == ["b", "a"]
        assert cursor is None
        PY
        """,
    },
    "task-015": {
        "difficulty": "medium",
        "summary": "Token bucket 支持小数秒补充并防时钟回拨",
        "instruction": """
        # 修复限流 token bucket

        来源/场景：API gateway / webhook consumer 中常见的 token bucket 限流 bug。

        目标：`src/ratelimit/token_bucket.py` 当前把 elapsed 转成 int，小数秒不会补 token；
        时钟回拨时还可能扣出负数。

        要求：

        1. 只修改 `src/ratelimit/token_bucket.py`。
        2. 按浮点秒补充 token。
        3. token 不超过 capacity。
        4. now 小于上次时间时，不补负 token。
        5. `allow(cost, now)` 返回布尔值，并在允许时扣减 cost。

        完成后运行：

        ```bash
        bash test.sh
        ```
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/ratelimit/token_bucket.py`。
        - 根因：`int(now - updated_at)` 丢掉小数秒。
        - 真实限流不能依赖每秒整数 tick。
        - 测试覆盖 0.5 秒补 1 token、capacity 上限、时钟回拨。
        """,
        "files": {
            "src/ratelimit/token_bucket.py": """
            class TokenBucket:
                def __init__(self, rate_per_second, capacity, now=0.0):
                    self.rate_per_second = rate_per_second
                    self.capacity = capacity
                    self.tokens = capacity
                    self.updated_at = now

                def allow(self, cost=1, now=0.0):
                    elapsed = int(now - self.updated_at)
                    self.tokens = min(self.capacity, self.tokens + elapsed * self.rate_per_second)
                    self.updated_at = now
                    if self.tokens >= cost:
                        self.tokens -= cost
                        return True
                    return False
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        python3 - <<'PY'
        from src.ratelimit.token_bucket import TokenBucket

        bucket = TokenBucket(rate_per_second=2, capacity=3, now=0.0)
        assert bucket.allow(now=0.0) is True
        assert bucket.allow(now=0.0) is True
        assert bucket.allow(now=0.0) is True
        assert bucket.allow(now=0.25) is False
        assert bucket.allow(now=0.5) is True
        assert bucket.allow(now=0.4) is False

        capped = TokenBucket(rate_per_second=10, capacity=3, now=0.0)
        assert capped.allow(cost=2, now=1.0) is True
        assert capped.tokens == 1
        PY
        """,
    },
    "task-016": {
        "difficulty": "medium",
        "summary": "SQL filter builder 保留 falsy 并参数化",
        "instruction": """
        # 修复 SQL filter builder

        来源/场景：企业后台列表筛选常见问题：`False`/`0` 条件被丢弃，同时字符串拼接有注入风险。

        目标：`src/db/sql_filters.py` 当前用 truthy 判断并直接拼 SQL。

        要求：

        1. 只修改 `src/db/sql_filters.py`。
        2. 支持字段白名单：`owner`、`is_active`、`retry_count`。
        3. `False` 和 `0` 是有效筛选值。
        4. `None` 和空字符串跳过。
        5. 返回 `(where_sql, params)`，SQL 使用 `?` 占位符。
        6. 遇到未知字段抛出 `ValueError`。

        完成后运行：

        ```bash
        bash test.sh
        ```
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/db/sql_filters.py`。
        - 根因：`if not value` 丢掉 falsy 条件，f-string 直接拼值。
        - 不需要接数据库，只构造 where 和 params。
        - 测试会检查参数顺序和未知字段。
        """,
        "files": {
            "src/db/sql_filters.py": """
            def build_where(filters):
                clauses = []
                params = []
                for key, value in filters.items():
                    if not value:
                        continue
                    clauses.append(f"{key} = '{value}'")
                return (" AND ".join(clauses) or "1=1", params)
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        python3 - <<'PY'
        from src.db.sql_filters import build_where

        sql, params = build_where({
            "owner": "alice",
            "is_active": False,
            "retry_count": 0,
        })
        assert sql == "owner = ? AND is_active = ? AND retry_count = ?"
        assert params == ["alice", False, 0]

        assert build_where({"owner": ""}) == ("1=1", [])

        try:
            build_where({"owner; DROP TABLE jobs": "x"})
        except ValueError as exc:
            assert "unknown filter" in str(exc)
        else:
            raise AssertionError("unknown filter was not rejected")
        PY
        """,
    },
    "task-017": {
        "difficulty": "medium",
        "summary": "日志脱敏覆盖大小写 header 和 URL query",
        "instruction": """
        # 修复日志脱敏

        来源/场景：企业日志平台常见安全问题：token/password 出现在 header 或 URL query 中。

        目标：`src/logging/redactor.py` 当前只按小写精确匹配 header，且完全不处理 URL query。

        要求：

        1. 只修改 `src/logging/redactor.py`。
        2. header key 大小写不敏感。
        3. 敏感 header：`authorization`、`cookie`、`x-api-key`。
        4. URL query 中 `token`、`password`、`secret` 大小写不敏感脱敏。
        5. 非敏感 query 参数和值必须保留。

        完成后运行：

        ```bash
        bash test.sh
        ```
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/logging/redactor.py`。
        - 根因：大小写敏感匹配和缺失 URL query 处理。
        - stdlib `urllib.parse` 足够。
        - 测试不会要求保留 query 参数原始顺序以外的复杂编码边界。
        """,
        "files": {
            "src/logging/redactor.py": """
            SECRET_HEADERS = {"authorization", "cookie", "x-api-key"}


            def redact_headers(headers):
                return {
                    key: ("<redacted>" if key in SECRET_HEADERS else value)
                    for key, value in headers.items()
                }


            def redact_url(url):
                return url
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        python3 - <<'PY'
        from urllib.parse import parse_qsl, urlsplit
        from src.logging.redactor import redact_headers, redact_url

        assert redact_headers({
            "Authorization": "Bearer abc",
            "X-Api-Key": "key",
            "Trace-Id": "t1",
        }) == {
            "Authorization": "<redacted>",
            "X-Api-Key": "<redacted>",
            "Trace-Id": "t1",
        }

        redacted = redact_url("https://api.test/users?token=abc&view=full&PASSWORD=pw&secret=s")
        params = dict(parse_qsl(urlsplit(redacted).query))
        assert params["token"] == "<redacted>"
        assert params["PASSWORD"] == "<redacted>"
        assert params["secret"] == "<redacted>"
        assert params["view"] == "full"
        assert "abc" not in redacted and "pw" not in redacted
        PY
        """,
    },
    "task-018": {
        "difficulty": "easy",
        "summary": "路由匹配忽略 query 并规范 trailing slash",
        "instruction": """
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
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/router/matcher.js`。
        - 根因：没有路径 normalize。
        - 可以用 WHATWG `URL`，但要兼容相对路径；给一个 dummy origin 即可。
        - 不需要写完整 router。
        """,
        "files": {
            "src/router/matcher.js": """
            function matches(route, requestPath) {
              return route === requestPath;
            }

            module.exports = { matches };
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        node - <<'JS'
        const assert = require('assert');
        const { matches } = require('./src/router/matcher');

        assert.strictEqual(matches('/users', '/users/'), true);
        assert.strictEqual(matches('/users', '/users?tab=all#top'), true);
        assert.strictEqual(matches('/', '/'), true);
        assert.strictEqual(matches('/', '/users'), false);
        assert.strictEqual(matches('/users', '/users/42'), false);
        JS
        """,
    },
    "task-019": {
        "difficulty": "medium",
        "summary": "迁移文件按数字版本排序并检测重复版本",
        "instruction": """
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
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/migrations/planner.js`。
        - 根因：字符串排序不等于版本号排序。
        - 正则提取数字版本即可，不需要读 SQL 文件。
        - 测试覆盖排序、重复版本、非法名称。
        """,
        "files": {
            "src/migrations/planner.js": """
            function planMigrations(files) {
              return files.slice().sort();
            }

            module.exports = { planMigrations };
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        node - <<'JS'
        const assert = require('assert');
        const { planMigrations } = require('./src/migrations/planner');

        assert.deepStrictEqual(
          planMigrations(['10_add_index.sql', '2_create_users.sql', '1_init.sql']),
          ['1_init.sql', '2_create_users.sql', '10_add_index.sql']
        );
        assert.throws(
          () => planMigrations(['1_init.sql', '01_duplicate.sql']),
          /duplicate migration version/
        );
        assert.throws(
          () => planMigrations(['latest.sql']),
          /invalid migration name/
        );
        JS
        """,
    },
    "task-020": {
        "difficulty": "medium",
        "summary": "JUnit 汇总支持嵌套 testsuites 和 testcase 子节点",
        "instruction": """
        # 修复 JUnit XML 汇总

        来源/场景：CI 平台聚合测试报告时常见的 JUnit XML 方言兼容问题。

        目标：`src/ci/junit_summary.py` 当前只读取第一个 testsuite 的属性，遇到嵌套
        `testsuites` 或只有 testcase 子节点时统计错误。

        要求：

        1. 只修改 `src/ci/junit_summary.py`。
        2. 支持根节点是 `testsuite` 或 `testsuites`。
        3. 汇总 tests、failures、errors、skipped。
        4. 如果 suite 属性缺失，要能从 testcase 子节点推导。
        5. failure/error/skipped 子节点分别计数。

        完成后运行：

        ```bash
        bash test.sh
        ```
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/ci/junit_summary.py`。
        - 根因：只看单个 suite attribute，没有递归所有 testsuite。
        - stdlib `xml.etree.ElementTree` 足够。
        - 小心不要重复统计父 testsuites 聚合属性和子 testsuite 属性。
        """,
        "files": {
            "src/ci/junit_summary.py": """
            import xml.etree.ElementTree as ET


            def summarize(xml_text):
                root = ET.fromstring(xml_text)
                suite = root if root.tag == "testsuite" else root.find("testsuite")
                if suite is None:
                    return {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
                return {
                    "tests": int(suite.attrib.get("tests", 0)),
                    "failures": int(suite.attrib.get("failures", 0)),
                    "errors": int(suite.attrib.get("errors", 0)),
                    "skipped": int(suite.attrib.get("skipped", 0)),
                }
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        python3 - <<'PY'
        from src.ci.junit_summary import summarize

        xml = '''
        <testsuites>
          <testsuite name="unit" tests="2" failures="1" errors="0" skipped="0">
            <testcase name="a"><failure /></testcase>
            <testcase name="b" />
          </testsuite>
          <testsuite name="integration">
            <testcase name="c"><error /></testcase>
            <testcase name="d"><skipped /></testcase>
          </testsuite>
        </testsuites>
        '''
        assert summarize(xml) == {"tests": 4, "failures": 1, "errors": 1, "skipped": 1}

        single = '<testsuite><testcase name="a" /><testcase name="b"><skipped /></testcase></testsuite>'
        assert summarize(single) == {"tests": 2, "failures": 0, "errors": 0, "skipped": 1}
        PY
        """,
    },
    "task-021": {
        "difficulty": "medium",
        "summary": "业务日调度跳过周末和节假日",
        "instruction": """
        # 修复业务日调度

        来源/场景：工单 SLA、财务结算、企业审批流常见的 business-day 计算。

        目标：`src/schedule/business_days.py` 当前直接加自然日，未跳过周末和 holidays。

        要求：

        1. 只修改 `src/schedule/business_days.py`。
        2. `add_business_days(start, days, holidays=())` 返回 `date`。
        3. 周六、周日不计入 business day。
        4. holidays 是 `date` 集合，也不计入。
        5. `days=0` 返回 start 本身。

        完成后运行：

        ```bash
        bash test.sh
        ```
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/schedule/business_days.py`。
        - 根因：当前直接 `timedelta(days=days)`。
        - 最小实现是按天循环，遇到工作日才递减 remaining。
        - 测试覆盖周五 +1、节假日跳过、days=0。
        """,
        "files": {
            "src/schedule/business_days.py": """
            from datetime import timedelta


            def add_business_days(start, days, holidays=()):
                return start + timedelta(days=days)
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        python3 - <<'PY'
        from datetime import date
        from src.schedule.business_days import add_business_days

        assert add_business_days(date(2026, 6, 26), 1) == date(2026, 6, 29)
        assert add_business_days(date(2026, 6, 24), 2, {date(2026, 6, 25)}) == date(2026, 6, 29)
        assert add_business_days(date(2026, 6, 24), 0) == date(2026, 6, 24)
        PY
        """,
    },
    "task-022": {
        "difficulty": "medium",
        "summary": "配置 merge 深合并 dict 且列表替换",
        "instruction": """
        # 修复配置合并

        来源/场景：CI/CD、应用配置和 Helm values 类工具常见 deep merge 语义。

        目标：`src/config/deep_merge.py` 当前是浅合并，override 一个嵌套字段会丢失同级配置。

        要求：

        1. 只修改 `src/config/deep_merge.py`。
        2. 两边都是 dict 时递归合并。
        3. list 按 override 整体替换，不做拼接。
        4. 标量按 override 替换。
        5. 不修改输入对象。

        完成后运行：

        ```bash
        bash test.sh
        ```
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/config/deep_merge.py`。
        - 根因：`dict.update` 是浅合并。
        - 不需要支持 merge strategy 配置。
        - 测试会检查输入对象未被原地修改。
        """,
        "files": {
            "src/config/deep_merge.py": """
            def merge_config(base, override):
                result = dict(base)
                result.update(override)
                return result
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        python3 - <<'PY'
        from src.config.deep_merge import merge_config

        base = {
            "server": {"host": "0.0.0.0", "port": 8080, "tags": ["blue"]},
            "debug": False,
        }
        override = {
            "server": {"port": 9090, "tags": ["green"]},
            "workers": 4,
        }
        merged = merge_config(base, override)
        assert merged == {
            "server": {"host": "0.0.0.0", "port": 9090, "tags": ["green"]},
            "debug": False,
            "workers": 4,
        }
        assert base["server"]["port"] == 8080
        assert override["server"]["tags"] == ["green"]
        merged["server"]["host"] = "127.0.0.1"
        assert base["server"]["host"] == "0.0.0.0"
        PY
        """,
    },
    "task-023": {
        "difficulty": "hard",
        "summary": "Semver caret range 正确处理 0.x",
        "instruction": """
        # 修复 semver caret range

        来源/场景：npm / package manager 依赖解析中常见的 `^` range 边界问题。

        目标：`src/semver/caret.js` 当前用字符串前缀判断，错误处理 `^1.2.3` 和 `^0.2.3`。

        要求：

        1. 只修改 `src/semver/caret.js`。
        2. 支持普通版本 `MAJOR.MINOR.PATCH`。
        3. `^1.2.3` 表示 `>=1.2.3 <2.0.0`。
        4. `^0.2.3` 表示 `>=0.2.3 <0.3.0`。
        5. `^0.0.3` 表示 `>=0.0.3 <0.0.4`。
        6. 不需要支持 prerelease 或复杂 range。

        完成后运行：

        ```bash
        bash test.sh
        ```
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/semver/caret.js`。
        - 根因：semver caret 不是字符串前缀匹配，尤其 0.x 有特殊上界。
        - 最小实现：parse 三段整数，比较 `version >= lower && version < upper`。
        - 测试覆盖 1.x、0.2.x、0.0.x。
        """,
        "files": {
            "src/semver/caret.js": """
            function satisfiesCaret(version, range) {
              if (!range.startsWith('^')) return version === range;
              const prefix = range.slice(1).split('.').slice(0, 2).join('.');
              return version.startsWith(prefix + '.');
            }

            module.exports = { satisfiesCaret };
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        node - <<'JS'
        const assert = require('assert');
        const { satisfiesCaret } = require('./src/semver/caret');

        assert.strictEqual(satisfiesCaret('1.2.3', '^1.2.3'), true);
        assert.strictEqual(satisfiesCaret('1.9.0', '^1.2.3'), true);
        assert.strictEqual(satisfiesCaret('1.2.2', '^1.2.3'), false);
        assert.strictEqual(satisfiesCaret('2.0.0', '^1.2.3'), false);

        assert.strictEqual(satisfiesCaret('0.2.9', '^0.2.3'), true);
        assert.strictEqual(satisfiesCaret('0.3.0', '^0.2.3'), false);
        assert.strictEqual(satisfiesCaret('0.0.3', '^0.0.3'), true);
        assert.strictEqual(satisfiesCaret('0.0.4', '^0.0.3'), false);
        JS
        """,
    },
    "task-024": {
        "difficulty": "hard",
        "summary": "NDJSON streaming parser 保留跨 chunk 半行",
        "instruction": """
        # 修复 NDJSON streaming parser

        来源/场景：日志采集、消息队列 consumer 和 LLM streaming 输出中常见的 chunk 边界问题。

        目标：`src/streaming/ndjson.py` 当前按每个 chunk 独立 split line，跨 chunk 的 JSON 行会解析失败。

        要求：

        1. 只修改 `src/streaming/ndjson.py`。
        2. 支持 JSON 行跨 chunk。
        3. 忽略空行。
        4. 输入结束时如果还有完整的最后一行但没有换行，也要解析。
        5. 如果剩余 buffer 不是合法 JSON，应抛出原始 `json.JSONDecodeError`。

        完成后运行：

        ```bash
        bash test.sh
        ```
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/streaming/ndjson.py`。
        - 根因：stream chunk 边界不等于行边界。
        - 最小实现维护 buffer，每次只解析 `\\n` 前的完整行。
        - 测试覆盖跨 chunk、空行、末尾无换行。
        """,
        "files": {
            "src/streaming/ndjson.py": """
            import json


            def parse_chunks(chunks):
                rows = []
                for chunk in chunks:
                    for line in chunk.splitlines():
                        if line.strip():
                            rows.append(json.loads(line))
                return rows
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        python3 - <<'PY'
        from src.streaming.ndjson import parse_chunks

        chunks = [
            '{"id": 1, "text": "hel',
            'lo"}\\n\\n{"id": 2}',
            '\\n{"id": 3}',
        ]
        assert parse_chunks(chunks) == [
            {"id": 1, "text": "hello"},
            {"id": 2},
            {"id": 3},
        ]

        try:
            parse_chunks(['{"id":'])
        except Exception as exc:
            assert exc.__class__.__name__ == "JSONDecodeError"
        else:
            raise AssertionError("invalid trailing buffer did not raise")
        PY
        """,
    },
    "task-025": {
        "difficulty": "hard",
        "summary": "部署 reconciler 按服务名 diff 而不是数组下标",
        "instruction": """
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
        """,
        "handoff": """
        # 已知信息

        - 入口文件：`src/deploy/reconciler.js`。
        - 根因：数组 index 不是资源身份，重排会制造假 diff。
        - 用 `Map(name -> service)` 对齐即可。
        - 测试覆盖重排不变、更新、新增、删除。
        """,
        "files": {
            "src/deploy/reconciler.js": """
            function diffServices(desired, current) {
              const changes = [];
              const max = Math.max(desired.length, current.length);
              for (let index = 0; index < max; index += 1) {
                const next = desired[index];
                const old = current[index];
                if (next && !old) {
                  changes.push({ type: 'create', name: next.name });
                } else if (!next && old) {
                  changes.push({ type: 'delete', name: old.name });
                } else if (JSON.stringify(next) !== JSON.stringify(old)) {
                  changes.push({ type: 'update', name: next.name, before: old, after: next });
                }
              }
              return changes;
            }

            module.exports = { diffServices };
            """,
        },
        "test": """
        #!/usr/bin/env bash
        set -euo pipefail

        node - <<'JS'
        const assert = require('assert');
        const { diffServices } = require('./src/deploy/reconciler');

        assert.deepStrictEqual(
          diffServices(
            [
              { name: 'api', image: 'api:v1', replicas: 2 },
              { name: 'web', image: 'web:v1', replicas: 1 },
            ],
            [
              { name: 'web', image: 'web:v1', replicas: 1 },
              { name: 'api', image: 'api:v1', replicas: 2 },
            ]
          ),
          []
        );

        assert.deepStrictEqual(
          diffServices(
            [
              { name: 'api', image: 'api:v2', replicas: 2 },
              { name: 'worker', image: 'worker:v1', replicas: 1 },
            ],
            [
              { name: 'api', image: 'api:v1', replicas: 2 },
              { name: 'web', image: 'web:v1', replicas: 1 },
            ]
          ),
          [
            {
              type: 'update',
              name: 'api',
              before: { name: 'api', image: 'api:v1', replicas: 2 },
              after: { name: 'api', image: 'api:v2', replicas: 2 },
            },
            { type: 'create', name: 'worker' },
            { type: 'delete', name: 'web' },
          ]
        );
        JS
        """,
    },
}


def write_task(name: str, data: dict[str, object]) -> None:
    task_dir = TASKS / name
    initial = task_dir / "initial-repo"
    if task_dir.exists():
        raise SystemExit(f"{name} already exists")

    initial.mkdir(parents=True)
    (task_dir / "instruction.md").write_text(clean(data["instruction"]), encoding="utf-8")
    (task_dir / "handoff.md").write_text(clean(data["handoff"]), encoding="utf-8")

    for rel_path, content in data["files"].items():
      path = initial / rel_path
      path.parent.mkdir(parents=True, exist_ok=True)
      path.write_text(clean(content), encoding="utf-8")

    test_path = task_dir / "test.sh"
    test_path.write_text(clean(data["test"]), encoding="utf-8")
    os.chmod(test_path, 0o755)


def main() -> None:
    for name, data in TASK_DATA.items():
        write_task(name, data)
    print(f"created {len(TASK_DATA)} benchmark tasks")


if __name__ == "__main__":
    main()
