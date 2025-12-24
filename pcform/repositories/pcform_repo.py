from typing import List, Dict, Any, Optional
from .base_repo import BaseRepository
from services.database import get_db_connection


class PCFormRepository(BaseRepository):
    """Repository for PCForm records."""

    # Define valid columns to prevent SQL injection
    VALID_COLUMNS = [
        "id",
        "fullname",
        "Device_Model",
        "Device_Serial",
        "ServiceMan",
        "Device_Problem",
        "Description",
        "created_at",
        "is_favorite",
    ]

    SEARCHABLE_COLUMNS = [
        "fullname",
        "Device_Model",
        "Device_Serial",
        "ServiceMan",
        "Device_Problem",
        "Description",
    ]

    @property
    def table_name(self) -> str:
        return "pcform"

    def _create_table(self) -> None:
        """Create pcform table if not exists."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS pcform (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fullname TEXT,
                    Device_Model TEXT,
                    Device_Serial TEXT,
                    ServiceMan TEXT,
                    Device_Problem TEXT,
                    Description TEXT,
                    created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
                    is_favorite INTEGER DEFAULT 0
                )
            """
            )

            # Add is_favorite column if missing (for existing databases)
            try:
                cursor.execute(
                    "ALTER TABLE pcform ADD COLUMN is_favorite INTEGER DEFAULT 0"
                )
            except Exception:
                pass  # Column already exists

    def create(self, data: Dict[str, Any]) -> int:
        """
        Create new PCForm record.

        Args:
            data: Dictionary with form data

        Returns:
            ID of created record
        """
        # SECURITY: Only allow valid columns (prevent SQL injection)
        safe_data = {
            k: v for k, v in data.items() if k in self.VALID_COLUMNS and k != "id"
        }

        if not safe_data:
            raise ValueError("No valid columns provided")

        columns = ", ".join(safe_data.keys())
        placeholders = ", ".join("?" * len(safe_data))

        return self._execute_write(
            f"INSERT INTO pcform ({columns}) VALUES ({placeholders})",
            tuple(safe_data.values()),
        )

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all records."""
        return self._execute("SELECT * FROM pcform ORDER BY id DESC")

    def get_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        """Get single record by ID."""
        return self._execute_one("SELECT * FROM pcform WHERE id = ?", (record_id,))

    def search(self, query: str, columns: List[str]) -> List[Dict[str, Any]]:
        """
        Search records.

        Args:
            query: Search text
            columns: Columns to search (default: all searchable)

        Returns:
            List of matching records
        """
        if not query or not query.strip():
            return self.get_all()

        # Use only valid, searchable columns
        search_cols = columns or self.SEARCHABLE_COLUMNS
        valid_cols = [c for c in search_cols if c in self.SEARCHABLE_COLUMNS]

        if not valid_cols:
            return []

        # Build WHERE clause
        conditions = " OR ".join(f"{col} LIKE ?" for col in valid_cols)
        params = tuple(f"%{query}%" for _ in valid_cols)

        return self._execute(f"SELECT * FROM pcform WHERE {conditions}", params)

    def toggle_favorite(self, record_id: int) -> Optional[int]:
        """Toggle favorite status, return new status."""
        record = self.get_by_id(record_id)
        if not record:
            return None

        new_status = 0 if record["is_favorite"] else 1

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE pcform SET is_favorite = ? WHERE id = ?",
                (new_status, record_id),
            )

        return new_status

    def delete(self, record_id: int) -> bool:
        """Delete record by ID."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pcform WHERE id = ?", (record_id,))
            return cursor.rowcount > 0
