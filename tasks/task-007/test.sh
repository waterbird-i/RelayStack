#!/usr/bin/env bash
set -euo pipefail

node - <<'JS'
const assert = require('assert');
const path = require('path');
const { planExtraction } = require('./src/archive/safeExtract');

const dest = path.join('/tmp', 'rsbench-extract', 'out');

assert.throws(
  () => planExtraction([{ name: '../outside.txt' }], dest),
  /unsafe path/
);
assert.throws(
  () => planExtraction([{ name: '/etc/passwd' }], dest),
  /unsafe path/
);
assert.throws(
  () => planExtraction([{ name: '../outside-prefix/file.txt' }], dest),
  /unsafe path/
);

const planned = planExtraction([
  { name: 'assets/app.js' },
  { name: 'nested/../ok.txt' },
], dest);

assert.deepStrictEqual(planned, [
  { name: 'assets/app.js', target: path.join(dest, 'assets/app.js') },
  { name: 'nested/../ok.txt', target: path.join(dest, 'ok.txt') },
]);
JS
