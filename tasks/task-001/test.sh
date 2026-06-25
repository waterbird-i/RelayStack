#!/usr/bin/env bash
set -euo pipefail

node - <<'JS'
const assert = require('assert');
const { getEnvironmentState } = require('./packages/vite/src/node/server/environmentState');

const envA = {};
const envB = {};
let calls = 0;
const first = getEnvironmentState(envA, () => {
  calls += 1;
  return false;
});
const second = getEnvironmentState(envA, () => {
  calls += 1;
  return true;
});
const third = getEnvironmentState(envB, () => {
  calls += 1;
  return 0;
});
const fourth = getEnvironmentState(envB, () => {
  calls += 1;
  return 1;
});

assert.strictEqual(first, false);
assert.strictEqual(second, false);
assert.strictEqual(third, 0);
assert.strictEqual(fourth, 0);
assert.strictEqual(calls, 2);
JS

