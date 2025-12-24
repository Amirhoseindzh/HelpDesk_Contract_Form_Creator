from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from services.database import get_db_connection


class BaseRepository(ABC):
    """
    Abstract base class for repositories.

    All repositories must implement:
    - table_name property
    - _create_table method
    """

    @property
    @abstractmethod
    def table_name(self) -> str:
        """Return the table name for this repository."""
        pass

    @abstractmethod
    def _create_table(self) -> None:
        """Create the table if it doesn't exist."""
        pass

    def __init__(self):
        """Initialize repository and ensure table exists."""
        self._create_table()

    def _execute(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results as list of dicts.

        Args:
            query: SQL query string
            params: Query parameters (use ? placeholders)

        Returns:
            List of dictionaries, one per row
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            # Convert Row objects to dictionaries
            return [dict(row) for row in rows]

    def _execute_one(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        """Execute query and return single result or None."""
        results = self._execute(query, params)
        return results[0] if results else None

    def _execute_write(self, query: str, params: tuple = ()) -> int:
        """
        Execute INSERT/UPDATE/DELETE and return affected row id.

        Returns:
            lastrowid for INSERT, rowcount for UPDATE/DELETE
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.lastrowid
