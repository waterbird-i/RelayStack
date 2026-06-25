const OPTIONAL_DEPS = ['@mdx-js/mdx', 'vite-tsconfig-paths'];

function getOptimizeDeps(resolveDependency) {
  return {
    include: ['react', ...OPTIONAL_DEPS],
  };
}

module.exports = { getOptimizeDeps };

