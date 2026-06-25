#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from src.streaming.ndjson import parse_chunks

chunks = [
    '{"id": 1, "text": "hel',
    'lo"}\n\n{"id": 2}',
    '\n{"id": 3}',
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
