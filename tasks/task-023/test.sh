#!/usr/bin/env bash
set -euo pipefail

node - <<'JS'
const assert = require('assert');
const { satisfiesCaret } = require('./src/semver/caret');

assert.strictEqual(satisfiesCaret('1.2.3', '^1.2.3'), true);
assert.strictEqual(satisfiesCaret('1.9.0', '^1.2.3'), true);
assert.strictEqual(satisfiesCaret('1.2.2', '^1.2.3'), false);
assert.strictEqual(satisfiesCaret('2.0.0', '^1.2.3'), false);

assert.strictEqual(satisfiesCaret('0.2.9', '^0.2.3'), true);
assert.strictEqual(satisfiesCaret('0.3.0', '^0.2.3'), false);
assert.strictEqual(satisfiesCaret('0.0.3', '^0.0.3'), true);
assert.strictEqual(satisfiesCaret('0.0.4', '^0.0.3'), false);
JS
