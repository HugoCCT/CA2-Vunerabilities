"""Catalogue search with values kept separate from SQL syntax."""

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
    return [
        dict(row)
        for row in _db.execute(
            "SELECT id, title, is_public FROM catalogue WHERE title = ? AND is_public = 1",
            (title,),
        ).fetchall()
    ]
