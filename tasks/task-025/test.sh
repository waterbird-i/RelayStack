#!/usr/bin/env bash
set -euo pipefail

node - <<'JS'
const assert = require('assert');
const { diffServices } = require('./src/deploy/reconciler');

assert.deepStrictEqual(
  diffServices(
    [
      { name: 'api', image: 'api:v1', replicas: 2 },
      { name: 'web', image: 'web:v1', replicas: 1 },
    ],
    [
      { name: 'web', image: 'web:v1', replicas: 1 },
      { name: 'api', image: 'api:v1', replicas: 2 },
    ]
  ),
  []
);

assert.deepStrictEqual(
  diffServices(
    [
      { name: 'api', image: 'api:v2', replicas: 2 },
      { name: 'worker', image: 'worker:v1', replicas: 1 },
    ],
    [
      { name: 'api', image: 'api:v1', replicas: 2 },
      { name: 'web', image: 'web:v1', replicas: 1 },
    ]
  ),
  [
    {
      type: 'update',
      name: 'api',
      before: { name: 'api', image: 'api:v1', replicas: 2 },
      after: { name: 'api', image: 'api:v2', replicas: 2 },
    },
    { type: 'create', name: 'worker' },
    { type: 'delete', name: 'web' },
  ]
);
JS
