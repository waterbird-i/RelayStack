const cache = new WeakMap();

function getEnvironmentState(environment, initial) {
  const cached = cache.get(environment);
  if (cached) {
    return cached;
  }

  const value = initial();
  cache.set(environment, value);
  return value;
}

module.exports = { getEnvironmentState };

