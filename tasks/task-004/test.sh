#!/usr/bin/env bash
set -euo pipefail

node - <<'JS'
const assert = require('assert');
const { getOptimizeDeps } = require('./packages/router-dev/vite/optimizeDeps');

const missing = getOptimizeDeps(() => {
  throw new Error('not found');
});
assert.deepStrictEqual(missing.include, ['react']);

const present = getOptimizeDeps(name => `/node_modules/${name}/index.js`);
assert.deepStrictEqual(present.include, ['react', '@mdx-js/mdx', 'vite-tsconfig-paths']);
JS

