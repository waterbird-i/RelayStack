function diffServices(desired, current) {
  const changes = [];
  const max = Math.max(desired.length, current.length);
  for (let index = 0; index < max; index += 1) {
    const next = desired[index];
    const old = current[index];
    if (next && !old) {
      changes.push({ type: 'create', name: next.name });
    } else if (!next && old) {
      changes.push({ type: 'delete', name: old.name });
    } else if (JSON.stringify(next) !== JSON.stringify(old)) {
      changes.push({ type: 'update', name: next.name, before: old, after: next });
    }
  }
  return changes;
}

module.exports = { diffServices };
