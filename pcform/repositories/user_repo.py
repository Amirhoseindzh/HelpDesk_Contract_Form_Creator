from typing import Optional, Dict, Any
from repositories.base_repo import BaseRepository
from services.database import get_db_connection


class UserRepository(BaseRepository):
    """Repository for user database operations."""

    @property
    def table_name(self) -> str:
        return "pcform_auth"

    def _create_table(self) -> None:
        """Create users table if not exists."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS pcform_auth (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
                )
            """
            )

    def create(self, username: str, password_hash: str) -> int:
        """Create new user.
        Note:
            This method expects password to ALREADY be hashed!
            Hashing is done in the service layer.
        """
        
        return self._execute_write(
            """
            INSERT INTO pcform_auth (username, password_hash) 
            VALUES (?, ?)
            """,
            (username.lower().strip(), password_hash),
        )

    def find_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        return self._execute_one(
            "SELECT * FROM pcform_auth WHERE username = ?", (username.lower().strip(),)
        )

    def exists(self, username: str) -> bool:
        """Check if username exists."""
        return self.find_by_username(username) is not None

    def get_last_username(self) -> str:
        """Get most recently created username."""
        result = self._execute_one(
            "SELECT username FROM pcform_auth ORDER BY id DESC LIMIT 1"
        )
        return result["username"] if result else ""

    def get_all(self) -> list:
        """Get all users (for admin purposes)."""
        return self._execute("SELECT id, username, created_at FROM pcform_auth")
