#!/usr/bin/env bash
set -euo pipefail

node - <<'JS'
const assert = require('assert');
const { retryAfterMs } = require('./src/http/retryAfter');

const now = Date.parse('2026-06-24T12:00:00Z');

assert.strictEqual(retryAfterMs('3', now), 3000);
assert.strictEqual(
  retryAfterMs('Wed, 24 Jun 2026 12:00:05 GMT', now),
  5000
);
assert.strictEqual(
  retryAfterMs('Wed, 24 Jun 2026 11:59:59 GMT', now),
  0
);
assert.strictEqual(retryAfterMs('10ms', now), 0);
assert.strictEqual(retryAfterMs('not-a-date', now), 0);
JS
