#!/usr/bin/env bash
set -euo pipefail

node - <<'JS'
const assert = require('assert');
const { serveMemoryFiles } = require('./packages/vite/src/node/server/middlewares/servePublicMiddleware');

let nextCalls = 0;
const middleware = serveMemoryFiles(new Map([['/asset.txt', 'hello']]));

assert.doesNotThrow(() => middleware({ url: '/%E0%A4%A' }, { end() {} }, () => { nextCalls += 1; }));
assert.strictEqual(nextCalls, 1);

let body = '';
middleware({ url: '/asset.txt' }, { end(value) { body = value; } }, () => { nextCalls += 1; });
assert.strictEqual(body, 'hello');
assert.strictEqual(nextCalls, 1);
JS

