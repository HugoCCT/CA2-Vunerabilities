"""Intentionally weak password storage for the CA2 comparison."""

import hashlib


_password_digests: dict[str, str] = {}


def register(user: str, password: str) -> None:
    # SHA-256 is a fast general-purpose hash, not a password KDF.
    # With no per-user salt, equal passwords produce equal database values.
    _password_digests[user] = hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify(user: str, password: str) -> bool:
    candidate = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return _password_digests.get(user) == candidate


def get_hash(user: str) -> str | None:
    """Return the simulated leaked database value for the demonstration."""
    return _password_digests.get(user)


def get_record(user: str) -> tuple[bytes, bytes] | None:
    """Expose (empty salt, digest bytes) as the leaked database record."""
    digest = get_hash(user)
    return (b"", bytes.fromhex(digest)) if digest else None
