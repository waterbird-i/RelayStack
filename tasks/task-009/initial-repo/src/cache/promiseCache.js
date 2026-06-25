class PromiseCache {
  constructor() {
    this.cache = new Map();
  }

  get(key, loader) {
    if (this.cache.has(key)) {
      return this.cache.get(key);
    }
    const promise = Promise.resolve().then(loader);
    this.cache.set(key, promise);
    return promise;
  }
}

module.exports = { PromiseCache };
