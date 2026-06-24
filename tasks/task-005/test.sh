#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from pathlib import Path

text = Path("src/components/icode/Markdown/index.tsx").read_text(encoding="utf-8")

assert "useCurrentUserName" not in text
assert "enableFrontMatterPreview" not in text
assert "parseMarkdownFrontMatter(content)" in text
assert "MarkdownFrontMatter" in text
assert "bodyContent" in text
PY

