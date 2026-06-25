function planMigrations(files) {
  return files.slice().sort();
}

module.exports = { planMigrations };
