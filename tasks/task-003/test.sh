#!/usr/bin/env bash
set -euo pipefail

node - <<'JS'
const assert = require('assert');
const { parseMarkdown } = require('./src/listParser');

assert.strictEqual(parseMarkdown('- \n'), '<ul><li></li></ul>');
assert.strictEqual(parseMarkdown('* \n'), '<ul><li></li></ul>');
assert.strictEqual(parseMarkdown('1. \n'), '<ol><li></li></ol>');
assert.strictEqual(parseMarkdown('- \n\nnext'), '<ul><li></li></ul><p>next</p>');
JS

