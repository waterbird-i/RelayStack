function stripComment(value) {
  const index = value.indexOf('#');
  return index === -1 ? value.trim() : value.slice(0, index).trim();
}

function unquote(value) {
  if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
    return value.slice(1, -1);
  }
  return value;
}

function parseEnv(text) {
  const env = {};
  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;
    const parts = line.split('=');
    const key = parts[0].trim();
    const value = stripComment((parts[1] || '').trim());
    env[key] = unquote(value);
  }
  return env;
}

module.exports = { parseEnv };
