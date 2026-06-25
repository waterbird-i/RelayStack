#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from src.importer.csv_import import import_users

data = "﻿email,name\n Alice@Example.COM , Alice \n,No Email\nalice@example.com,Duplicate\nBOB@example.com,Bob\n"
assert import_users(data) == [
    {"email": "alice@example.com", "name": "Alice"},
    {"email": "bob@example.com", "name": "Bob"},
]
PY
