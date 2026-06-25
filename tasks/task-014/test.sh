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
