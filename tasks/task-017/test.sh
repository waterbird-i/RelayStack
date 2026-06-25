#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from urllib.parse import parse_qsl, urlsplit
from src.logging.redactor import redact_headers, redact_url

assert redact_headers({
    "Authorization": "Bearer abc",
    "X-Api-Key": "key",
    "Trace-Id": "t1",
}) == {
    "Authorization": "<redacted>",
    "X-Api-Key": "<redacted>",
    "Trace-Id": "t1",
}

redacted = redact_url("https://api.test/users?token=abc&view=full&PASSWORD=pw&secret=s")
params = dict(parse_qsl(urlsplit(redacted).query))
assert params["token"] == "<redacted>"
assert params["PASSWORD"] == "<redacted>"
assert params["secret"] == "<redacted>"
assert params["view"] == "full"
assert "abc" not in redacted and "pw" not in redacted
PY
