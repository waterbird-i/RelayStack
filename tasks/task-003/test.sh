#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from pathlib import Path

actions = Path("src/mcp/Skills/SkillDetail/SquareDetail/SkillHeaderActions.tsx").read_text(encoding="utf-8")
styles = Path("src/mcp/Skills/SkillDetail/SquareDetail/QuickInstallDropdown.styles.ts").read_text(encoding="utf-8")

assert "disabled={skill.isHiddenWorkspace}" in actions
assert "disabledReason" in actions
assert "隐藏空间" in actions
assert "迁移" in actions
assert "handleShare" in actions
assert "&:disabled" in styles
PY

