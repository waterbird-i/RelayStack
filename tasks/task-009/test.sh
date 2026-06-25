#!/usr/bin/env bash
set -euo pipefail

node - <<'JS'
const assert = require('assert');
const { PromiseCache } = require('./src/cache/promiseCache');

(async () => {
  const cache = new PromiseCache();
  let calls = 0;

  const a = cache.get('user:1', async () => {
    calls += 1;
    return 'ok';
  });
  const b = cache.get('user:1', async () => {
    calls += 1;
    return 'wrong';
  });

  assert.strictEqual(await a, 'ok');
  assert.strictEqual(await b, 'ok');
  assert.strictEqual(calls, 1);

  let failCalls = 0;
  await assert.rejects(
    () => cache.get('user:2', async () => {
      failCalls += 1;
      throw new Error('temporary');
    }),
    /temporary/
  );

  const recovered = await cache.get('user:2', async () => {
    failCalls += 1;
    return 'recovered';
  });

  assert.strictEqual(recovered, 'recovered');
  assert.strictEqual(failCalls, 2);
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
JS
