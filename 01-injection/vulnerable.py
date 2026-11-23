"""Intentionally vulnerable catalogue search used for the CA2 demonstration."""

import sqlite3


_db = sqlite3.connect(":memory:")
_db.row_factory = sqlite3.Row
_db.execute(
    "CREATE TABLE catalogue (id INTEGER PRIMARY KEY, title TEXT, is_public INTEGER)"
)
_db.executemany(
    "INSERT INTO catalogue (title, is_public) VALUES (?, ?)",
    [
        ("Maple field guide", 1),
        ("Coastal birds", 1),
        ("Staff access codes", 0),
        ("Garden plants", 1),
    ],
)
_db.commit()


def search_records(title: str) -> list[dict]:
    # The title is inserted into SQL syntax instead of remaining data.
    # An apostrophe can close the string and let input change the WHERE clause.
    query = f"SELECT id, title, is_public FROM catalogue WHERE title = '{title}' AND is_public = 1"
    return [dict(row) for row in _db.execute(query).fetchall()]
