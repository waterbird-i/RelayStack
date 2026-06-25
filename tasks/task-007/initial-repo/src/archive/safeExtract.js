const path = require('path');

function planExtraction(entries, destination) {
  const base = path.resolve(destination);
  return entries
    .map((entry) => ({
      name: entry.name,
      target: path.resolve(base, entry.name),
    }))
    .filter((entry) => entry.target.startsWith(base));
}

module.exports = { planExtraction };
