#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from pathlib import Path

path = Path("src/components/icode/Markdown/DevOpsMarkdown.tsx")
text = path.read_text(encoding="utf-8")

assert "fixCodeBlockMarkers" in text
assert "replace(/^[ \\t]+(```)/gm" in text
assert "^```([^\\n`]+)\\n```" in text or "^```([^\\n`]+)\\n```[ \\t]*$" in text
assert "'```\\n$1\\n```'" in text or '"```\\n$1\\n```"' in text
PY

