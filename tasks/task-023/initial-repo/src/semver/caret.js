function satisfiesCaret(version, range) {
  if (!range.startsWith('^')) return version === range;
  const prefix = range.slice(1).split('.').slice(0, 2).join('.');
  return version.startsWith(prefix + '.');
}

module.exports = { satisfiesCaret };
