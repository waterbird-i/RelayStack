function parseMetadata(block) {
  const metadata = {};
  for (const line of block.split(/\r?\n/)) {
    const index = line.indexOf(':');
    if (index !== -1) {
      metadata[line.slice(0, index).trim()] = line.slice(index + 1).trim();
    }
  }
  return metadata;
}

function parseFrontMatter(text) {
  const start = text.indexOf('---');
  const end = text.indexOf('---', start + 3);
  if (start === -1 || end === -1) {
    return { metadata: {}, body: text };
  }
  return {
    metadata: parseMetadata(text.slice(start + 3, end).trim()),
    body: text.slice(end + 3).replace(/^\r?\n/, ''),
  };
}

module.exports = { parseFrontMatter };
