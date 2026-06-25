#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from src.ci.junit_summary import summarize

xml = '''
<testsuites>
  <testsuite name="unit" tests="2" failures="1" errors="0" skipped="0">
    <testcase name="a"><failure /></testcase>
    <testcase name="b" />
  </testsuite>
  <testsuite name="integration">
    <testcase name="c"><error /></testcase>
    <testcase name="d"><skipped /></testcase>
  </testsuite>
</testsuites>
'''
assert summarize(xml) == {"tests": 4, "failures": 1, "errors": 1, "skipped": 1}

single = '<testsuite><testcase name="a" /><testcase name="b"><skipped /></testcase></testsuite>'
assert summarize(single) == {"tests": 2, "failures": 0, "errors": 0, "skipped": 1}
PY
