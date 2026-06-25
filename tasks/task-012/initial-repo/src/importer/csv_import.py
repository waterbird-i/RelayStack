import csv
from io import StringIO


def import_users(text):
    users = []
    seen = set()
    reader = csv.DictReader(StringIO(text))
    for row in reader:
        email = row.get("email", "").strip()
        if not email or email in seen:
            continue
        seen.add(email)
        users.append({
            "email": email,
            "name": row.get("name", "").strip(),
        })
    return users
