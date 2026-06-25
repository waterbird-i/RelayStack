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
