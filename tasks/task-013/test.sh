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
