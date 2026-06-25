function serveMemoryFiles(files) {
  return function serveMemoryFile(req, res, next) {
    const url = decodeURIComponent(req.url || '/');

    if (files.has(url)) {
      res.end(files.get(url));
      return;
    }

    next();
  };
}

module.exports = { serveMemoryFiles };

