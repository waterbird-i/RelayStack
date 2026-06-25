def page(items, cursor=None, limit=2):
    start = int(cursor or 0)
    ordered = sorted(items, key=lambda item: (-item["created_at"], item["id"]))
    batch = ordered[start:start + limit]
    next_cursor = str(start + limit) if start + limit < len(ordered) else None
    return batch, next_cursor
