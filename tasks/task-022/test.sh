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
