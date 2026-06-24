#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from pathlib import Path

header = Path("src/mcp/Skills/SkillDetail/SquareDetail/SkillHeader.tsx").read_text(encoding="utf-8")
actions = Path("src/mcp/Skills/SkillDetail/SquareDetail/SkillHeaderActions.tsx").read_text(encoding="utf-8")

assert "checkDraftScannerResult" in header
assert "SkillStatus.PUBLISHING" in actions
assert "key: 'publish'" in actions
PY

