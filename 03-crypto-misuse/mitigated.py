"""Salted scrypt password storage with a constant-time digest comparison."""

import hashlib
import hmac
import secrets


_password_records: dict[str, tuple[bytes, bytes]] = {}
_SCRYPT_N = 1 << 17  # OWASP's listed scrypt baseline: N=2^17, r=8, p=1.
_SCRYPT_R = 8
_SCRYPT_P = 1
_SCRYPT_MAXMEM = 256 * 1024 * 1024


def _derive(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=_SCRYPT_N,
        r=_SCRYPT_R,
        p=_SCRYPT_P,
        dklen=32,
        maxmem=_SCRYPT_MAXMEM,
    )


def register(user: str, password: str) -> None:
    salt = secrets.token_bytes(16)
    _password_records[user] = (salt, _derive(password, salt))


def verify(user: str, password: str) -> bool:
    record = _password_records.get(user)
    if record is None:
        return False
    salt, expected = record
    return hmac.compare_digest(expected, _derive(password, salt))


def get_hash(user: str) -> str | None:
    """Return the simulated leaked digest, excluding its separately stored salt."""
    record = _password_records.get(user)
    return record[1].hex() if record else None


def get_record(user: str) -> tuple[bytes, bytes] | None:
    """Expose the salt and digest an attacker would obtain in a database leak."""
    return _password_records.get(user)
