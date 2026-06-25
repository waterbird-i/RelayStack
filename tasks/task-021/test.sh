#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from datetime import date
from src.schedule.business_days import add_business_days

assert add_business_days(date(2026, 6, 26), 1) == date(2026, 6, 29)
assert add_business_days(date(2026, 6, 24), 2, {date(2026, 6, 25)}) == date(2026, 6, 29)
assert add_business_days(date(2026, 6, 24), 0) == date(2026, 6, 24)
PY
