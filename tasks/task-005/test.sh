#!/usr/bin/env bash
set -euo pipefail

printf '# From file\n' > fixture.md

file_output="$(node bin/marked.js fixture.md)"
stdin_output="$(printf '# From stdin\n' | node bin/marked.js)"

test "$file_output" = '<h1>From file</h1>'
test "$stdin_output" = '<h1>From stdin</h1>'

