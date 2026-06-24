#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from pathlib import Path

url = Path("src/utils/comatemobile/url.ts").read_text(encoding="utf-8")
index = Path("src/index.tsx").read_text(encoding="utf-8")

assert "COMATE_MOBILE_PATH_PATTERN" in url
assert "isComateMobilePath" in url
assert "/devops/icode/comatemobile" in url
assert "(?:/|$)" in url
assert "isComateMobilePath()" in index
assert ".includes('/comatemobile')" not in url + index
assert ".includes('comatemobile')" not in url + index
PY

