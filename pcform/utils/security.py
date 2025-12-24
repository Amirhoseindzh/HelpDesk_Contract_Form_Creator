import hashlib
import secrets


class PasswordHasher:
    """
    Secure password hashing utility.

    HOW IT WORKS:
    1. Generate random "salt" (random bytes)
    2. Combine salt + password
    3. Hash the combination
    4. Store salt + hash together
    """

    @staticmethod
    def hash(password: str) -> str:
        """Create secure hash of password."""
        # Generate 32 random hex characters
        salt = secrets.token_hex(16)

        # Hash salt+password using SHA-256
        combined = (salt + password).encode("utf-8")
        password_hash = hashlib.sha256(combined).hexdigest()

        return f"{salt}${password_hash}"

    @staticmethod
    def verify(password: str, stored_hash: str) -> bool:
        """
        Verify password against stored hash.

        Args:
            password: Plain text password to check
            stored_hash: Hash from database

        Returns:
            True if password matches
        """
        try:
            # Extract salt from stored hash
            salt, original_hash = stored_hash.split("$")

            # Hash input password with same salt
            combined = (salt + password).encode("utf-8")
            new_hash = hashlib.sha256(combined).hexdigest()

            # Use constant-time comparison (prevents timing attacks)
            return secrets.compare_digest(new_hash, original_hash)

        except (ValueError, AttributeError):
            # Invalid hash format
            return False


# Convenience instance
password_hasher = PasswordHasher()
