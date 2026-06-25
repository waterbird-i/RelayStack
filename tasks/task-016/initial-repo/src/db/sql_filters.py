def build_where(filters):
    clauses = []
    params = []
    for key, value in filters.items():
        if not value:
            continue
        clauses.append(f"{key} = '{value}'")
    return (" AND ".join(clauses) or "1=1", params)
