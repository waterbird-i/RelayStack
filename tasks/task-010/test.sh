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
