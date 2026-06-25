#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from src.ratelimit.token_bucket import TokenBucket

bucket = TokenBucket(rate_per_second=2, capacity=3, now=0.0)
assert bucket.allow(now=0.0) is True
assert bucket.allow(now=0.0) is True
assert bucket.allow(now=0.0) is True
assert bucket.allow(now=0.25) is False
assert bucket.allow(now=0.5) is True
assert bucket.allow(now=0.4) is False

capped = TokenBucket(rate_per_second=10, capacity=3, now=0.0)
assert capped.allow(cost=2, now=1.0) is True
assert capped.tokens == 1
PY
