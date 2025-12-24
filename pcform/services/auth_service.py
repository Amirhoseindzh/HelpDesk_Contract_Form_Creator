import re
from dataclasses import dataclass
from typing import Optional

from repositories.user_repo import UserRepository
from settings.config import MIN_PASSWORD_LENGTH, USERNAME_PATTERN
from utils.security import password_hasher


@dataclass
class AuthResult:
    """
    Result of an authentication operation.
    """

    success: bool
    message: str
    user_id: Optional[int] = None
    username: Optional[str] = None


class AuthService:
    """
    Authentication service.

    Usage:
        service = AuthService()

        # Register
        result = service.register("john", "pass123", "pass123")
        if result.success:
            print(f"Welcome, {result.username}!")
        else:
            print(f"Error: {result.message}")

        # Login
        result = service.login("john", "pass123")
        if result.success:
            print("Logged in!")
    """

    def __init__(self, user_repository: UserRepository = None):
        """
        Initialize with optional repository (Dependency Injection).
        """
        self.user_repo = user_repository or UserRepository()

    def register(
        self, username: str, password: str, confirm_password: str
    ) -> AuthResult:
        """
        Register a new user.

        Validates all inputs, hashes password, stores in database.
        """
        # === VALIDATION ===

        # Check all fields provided
        if not all([username, password, confirm_password]):
            return AuthResult(False, "All fields are required.")

        # Clean username
        username = username.strip().lower()

        # Check passwords match
        if password != confirm_password:
            return AuthResult(False, "Passwords do not match.")

        # Check password length
        if len(password) < MIN_PASSWORD_LENGTH:
            return AuthResult(
                False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters."
            )

        # Check username format
        if not re.match(USERNAME_PATTERN, username):
            return AuthResult(
                False, "Username can only contain letters, numbers, and underscores."
            )

        # Check if username taken
        if self.user_repo.exists(username):
            return AuthResult(False, f"Username '{username}' is already taken.")

        # === CREATE USER ===
        try:
            # Hash password BEFORE storing
            hashed = password_hasher.hash(password)

            # Store in database
            user_id = self.user_repo.create(username, hashed)

            return AuthResult(
                success=True,
                message="Registration successful!",
                user_id=user_id,
                username=username,
            )

        except Exception as e:
            return AuthResult(False, f"Registration failed: {str(e)}")

    def login(self, username: str, password: str) -> AuthResult:
        """
        Authenticate a user.

        Finds user, verifies password hash.
        """
        # Check fields provided
        if not username or not password:
            return AuthResult(False, "Username and password are required.")

        # Clean username
        username = username.strip().lower()

        # Find user
        user = self.user_repo.find_by_username(username)

        if not user:
            # Don't reveal if username exists (security)
            return AuthResult(False, "Invalid username or password.")

        # Verify password against hash
        if not password_hasher.verify(password, user["password_hash"]):
            return AuthResult(False, "Invalid username or password.")

        # Success!
        return AuthResult(
            success=True,
            message=f"Welcome back, {user['username']}!",
            user_id=user["id"],
            username=user["username"],
        )

    def get_last_username(self) -> str:
        """Get last registered username for login form."""
        return self.user_repo.get_last_username()
