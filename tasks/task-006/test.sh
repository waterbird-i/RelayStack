#!/usr/bin/env bash
set -euo pipefail

node - <<'JS'
const assert = require('assert');
const { parseEnv } = require('./src/config/dotenv');

const env = parseEnv(`
# comment
API_URL=https://example.test/callback?token=a=b=c
EMPTY=
QUOTED_HASH="abc#not-comment"
SINGLE_HASH='x#y'
PASSWORD=abc#def
INLINE=value # deploy comment
SPACED = keep me
`);

assert.deepStrictEqual(env, {
  API_URL: 'https://example.test/callback?token=a=b=c',
  EMPTY: '',
  QUOTED_HASH: 'abc#not-comment',
  SINGLE_HASH: 'x#y',
  PASSWORD: 'abc#def',
  INLINE: 'value',
  SPACED: 'keep me',
});
JS
