#!/usr/bin/env bash
set -euo pipefail

node - <<'JS'
const assert = require('assert');
const { matches } = require('./src/router/matcher');

assert.strictEqual(matches('/users', '/users/'), true);
assert.strictEqual(matches('/users', '/users?tab=all#top'), true);
assert.strictEqual(matches('/', '/'), true);
assert.strictEqual(matches('/', '/users'), false);
assert.strictEqual(matches('/users', '/users/42'), false);
JS
