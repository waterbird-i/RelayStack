function parseMarkdown(markdown) {
  const lines = markdown.split(/\n/);
  const blocks = [];
  let list = null;

  for (const line of lines) {
    if (line === '') {
      continue;
    }

    const match = line.match(/^(\s*)([-*]|\d+\.)\s+(.+)$/);
    if (match) {
      const ordered = /\d+\./.test(match[2]);
      const tag = ordered ? 'ol' : 'ul';
      if (!list || list.tag !== tag) {
        list = { tag, items: [] };
        blocks.push(list);
      }
      list.items.push(match[3]);
      continue;
    }

    list = null;
    blocks.push({ tag: 'p', text: line });
  }

  return blocks.map(block => {
    if (block.tag === 'p') {
      return `<p>${block.text}</p>`;
    }
    return `<${block.tag}>${block.items.map(item => `<li>${item}</li>`).join('')}</${block.tag}>`;
  }).join('');
}

module.exports = { parseMarkdown };

