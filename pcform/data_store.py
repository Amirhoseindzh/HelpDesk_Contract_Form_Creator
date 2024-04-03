import sqlite3
from config import PCFORM_DB_PATH


class PcFormDatabase:

    @staticmethod
    def connect():
        # Connect to SQLite database
        return sqlite3.connect(PCFORM_DB_PATH)

    @staticmethod
    def create_table(conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pcform (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fullname TEXT,
                    Device_Model TEXT,
                    Device_Serial Number TEXT,
                    ServiceMan TEXT,
                    Device_Problem TEXT,
                    Description TEXT
                )
            """)
            conn.commit()
            print("Table created or already exists.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    @staticmethod
    def insert_pcform(data_list):
        conn = PcFormDatabase.connect()
        if conn:
            try:
                PcFormDatabase.create_table(conn)
                cursor = conn.cursor()
                for data in data_list:
                    keys = ', '.join(data.keys())
                    placeholders = ', '.join('?' * len(data))
                    sql = f"INSERT INTO pcform ({keys}) VALUES ({placeholders})"
                    cursor.execute(sql, list(data.values()))
                conn.commit()
                print("Data inserted successfully.")
            except sqlite3.Error as e:
                print(f"Error inserting data into database: {e}")
                conn.rollback()
            finally:
                conn.close()