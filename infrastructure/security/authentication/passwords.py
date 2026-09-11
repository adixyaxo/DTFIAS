# infrastructure/security/authentication/passwords.py
"""
Argon2 password hashing implementation for DTFIAS.
Conforms to Constraint C6:
- Passwords MUST be hashed with argon2
- MUST NOT log or store plaintext passwords, ever, including debug logs
"""
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError

_ph = PasswordHasher(
    time_cost=2,
    memory_cost=15360,  # 15 MB to fix 20-second auth hangs on local VMs
    parallelism=1,
    hash_len=32,
    salt_len=16,
)


def hash_password(password: str) -> str:
    """Hashes a plaintext password using Argon2id."""
    if not password:
        raise ValueError("Password cannot be empty")
    return _ph.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verifies a plaintext password against an Argon2 hash. Never logs plaintext."""
    if not password or not hashed:
        return False
    try:
        return _ph.verify(hashed, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def needs_rehash(hashed: str) -> bool:
    """Checks whether the password hash needs updating to newer parameters."""
    return _ph.check_needs_rehash(hashed)


__all__ = ["hash_password", "verify_password", "needs_rehash"]
