import sqlite3
from config import PCFORM_DB_PATH


class PcFormDatabase:

    @staticmethod
    def connect():
        # Connect to SQLite database
        return sqlite3.connect(PCFORM_DB_PATH)

    @staticmethod
    def create_table_data(conn):
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
                    Description TEXT,
                    created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
                )
            """)
            conn.commit()
            print("Table created or already exists.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    @staticmethod
    def create_table_auth(conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS pcform_auth (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT,
                    created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
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
                PcFormDatabase.create_table_data(conn)
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

    @ staticmethod
    def insert_pcform_auth(auth_data_list):
        conn = PcFormDatabase.connect()
        if conn:
            try:
                PcFormDatabase.create_table_auth(conn)
                cursor = conn.cursor()
                for data in auth_data_list:
                    keys = ', '.join(data.keys())
                    placeholders = ', '.join('?' * len(data))
                    sql = f"INSERT INTO pcform_auth ({keys}) VALUES ({placeholders})"
                    cursor.execute(sql, list(data.values()))
                conn.commit()
                print("Data inserted successfully.")
            except sqlite3.Error as e:
                print(f"Error inserting data into database: {e}")
                conn.rollback()
            finally:
                conn.close()
    
    @staticmethod
    def auth_data_retrieve(username, password):
        conn = PcFormDatabase.connect()
        c = conn.cursor()

        # Retrieve user data
        c.execute("SELECT username,password FROM pcform_auth WHERE username=? AND password=? ", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            stored_username, stored_password= user
            if password == stored_password and username == stored_username:
                print("Login successful.")
                return True
        print("Invalid username or password.")
        return False

    @staticmethod
    def check_user_exists(username):
        conn = PcFormDatabase.connect()
        PcFormDatabase.create_table_auth(conn)
        cursor = conn.cursor()
        if conn:
            # Check if username or email already exists
            cursor.execute(
                "SELECT * FROM pcform_auth WHERE username=?", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                print("Username or email already exists.")
                cursor.close()
                return False

    @ staticmethod
    def treeview():
        # Update with your database path
        conn = PcFormDatabase.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pcform")
        rows = cursor.fetchall()
        conn.close()
        return rows

    @ staticmethod
    # get columns name to show in search results
    def get_column_titles(table_name="pcform"):
        try:
            # Update with your database path
            conn = PcFormDatabase.connect()
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            conn.close()

            column_titles = [column[1] for column in columns]
            return column_titles
        except sqlite3.Error as e:
            print("Error fetching column titles:", e)
            return []

    @ staticmethod
    def _search(columns, query):
        try:
            conn = PcFormDatabase.connect()
            c = conn.cursor()

           # Construct the SQL query dynamically
            sql_query = "SELECT * FROM pcform WHERE "
            sql_query += " OR ".join([f"{column} LIKE ?" for column in columns])

            # Execute the query with the search query as parameter
        # Supply the same number of bindings as the number of search_columns
            bindings = ['%' + query + '%'] * len(columns)
            c.execute(sql_query, bindings)
            rows = c.fetchall()
        except sqlite3.Error as e:
            print("SQLite error:", e)
            return None
        finally:
            if conn:
                conn.close()
        return rows
    
    @staticmethod
    def load_last_username():
        conn = PcFormDatabase.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT username FROM pcform_auth ORDER BY id DESC LIMIT 1")
        last_username = cursor.fetchone()
        conn.close()
        return last_username[0] if last_username else ""
    
