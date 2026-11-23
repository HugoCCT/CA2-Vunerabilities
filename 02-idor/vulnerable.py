"""Intentionally vulnerable booking lookup for the CA2 IDOR demonstration."""

import sqlite3


_db = sqlite3.connect(":memory:")
_db.row_factory = sqlite3.Row
_db.execute(
    "CREATE TABLE bookings (id INTEGER PRIMARY KEY, owner_id INTEGER, destination TEXT, note TEXT)"
)
_db.executemany(
    "INSERT INTO bookings (owner_id, destination, note) VALUES (?, ?, ?)",
    [
        (1, "Galway", "Window seat requested"),
        (2, "Cork", "Private itinerary: client meeting at 09:00"),
    ],
)
_db.commit()


def get_booking(current_user_id: int, booking_id: int) -> dict | None:
    # Authentication is assumed to have happened before this function is called;
    # this lookup omits authorization and can return another owner's booking.
    row = _db.execute(
        "SELECT id, owner_id, destination, note FROM bookings WHERE id = ?",
        (booking_id,),
    ).fetchone()
    return dict(row) if row else None
