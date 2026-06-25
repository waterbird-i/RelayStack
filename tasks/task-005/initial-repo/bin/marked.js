#!/usr/bin/env node
const fs = require('fs');

function render(markdown) {
  return markdown.trim().replace(/^#\s+(.+)$/, '<h1>$1</h1>');
}

function main(argv, stdin) {
  const input = argv[2] || stdin;
  return render(input);
}

if (require.main === module) {
  let stdin = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', chunk => {
    stdin += chunk;
  });
  process.stdin.on('end', () => {
    process.stdout.write(main(process.argv, stdin));
  });
}

module.exports = { main, render };
