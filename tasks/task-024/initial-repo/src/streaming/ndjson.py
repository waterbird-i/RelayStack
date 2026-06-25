import json


def parse_chunks(chunks):
    rows = []
    for chunk in chunks:
        for line in chunk.splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows
