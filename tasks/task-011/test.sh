#!/usr/bin/env bash
set -euo pipefail

node - <<'JS'
const assert = require('assert');
const { parseFrontMatter } = require('./src/markdown/frontmatter');

assert.deepStrictEqual(parseFrontMatter('---\ntitle: Hello\ndraft: false\n---\nBody'), {
  metadata: { title: 'Hello', draft: 'false' },
  body: 'Body',
});

const bodyOnly = 'Intro\n---\nthis is a horizontal rule\n---\nEnd';
assert.deepStrictEqual(parseFrontMatter(bodyOnly), {
  metadata: {},
  body: bodyOnly,
});

const unfinished = '---\ntitle: Missing end\nBody';
assert.deepStrictEqual(parseFrontMatter(unfinished), {
  metadata: {},
  body: unfinished,
});
JS
