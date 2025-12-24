import sqlite3
from contextlib import contextmanager
from typing import Generator

from settings.config import PCFORM_DB_PATH


class DatabaseConnection:
    """
    Database connection manager.

    Usage:
        # Option 1: Context manager (recommended)
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
        # Connection auto-closed!

        # Option 2: Manual (not recommended)
        db = DatabaseConnection()
        conn = db.connect()
        # ... do stuff ...
        conn.close()  # Don't forget this!
    """

    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(PCFORM_DB_PATH)
        self._connection = None

    def connect(self) -> sqlite3.Connection:
        """Create new database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn

    def __enter__(self) -> sqlite3.Connection:
        """Called when entering 'with' block."""
        self._connection = self.connect()
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called when exiting 'with' block (even if error!)."""
        if self._connection:
            if exc_type is None:
                # No error, commit changes
                self._connection.commit()
            else:
                # Error occurred, rollback changes
                self._connection.rollback()
            self._connection.close()
            self._connection = None


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """
    Function-based context manager for database connections.

    Usage:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(...)
    """
    conn = sqlite3.connect(str(PCFORM_DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
