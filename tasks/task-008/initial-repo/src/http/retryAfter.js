function retryAfterMs(header, now = Date.now()) {
  if (!header) return 0;
  const seconds = parseInt(header, 10);
  if (!Number.isNaN(seconds)) return seconds * 1000;
  return 0;
}

module.exports = { retryAfterMs };
