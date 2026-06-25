#!/usr/bin/env bash
set -euo pipefail

node - <<'JS'
const assert = require('assert');
const { planMigrations } = require('./src/migrations/planner');

assert.deepStrictEqual(
  planMigrations(['10_add_index.sql', '2_create_users.sql', '1_init.sql']),
  ['1_init.sql', '2_create_users.sql', '10_add_index.sql']
);
assert.throws(
  () => planMigrations(['1_init.sql', '01_duplicate.sql']),
  /duplicate migration version/
);
assert.throws(
  () => planMigrations(['latest.sql']),
  /invalid migration name/
);
JS
