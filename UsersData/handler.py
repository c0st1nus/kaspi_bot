import sqlite3
from sqlite3 import Error
from functools import wraps

class DatabaseHandler:
    def __init__(self):
        self.db_file = "sqlite.db"
        self.conn = None
    
    def __enter__(self):
        """Context manager entry point"""
        self.conn = self.create_connection()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point"""
        if self.conn:
            if exc_type:  # Rollback if there was an exception
                self.conn.rollback()
            else:         # Commit if everything was successful
                self.conn.commit()
            self.conn.close()
        return False  # Propagate exceptions

    def create_connection(self) -> sqlite3.Connection:
        """Create a new database connection"""
        try:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row  # Enable dictionary-like access
            return conn
        except Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def create_table(self, create_table_sql):
        """Create a table from the create_table_sql statement"""
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            self.conn.commit()
        except Error as e:
            print(f"Error creating table: {e}")
            raise

    def insert_data(self, table, data):
        """Insert data into the specified table"""
        keys = ', '.join(data.keys())
        question_marks = ', '.join(['?'] * len(data))
        sql = f"INSERT INTO {table} ({keys}) VALUES ({question_marks})"
        try:
            c = self.conn.cursor()
            c.execute(sql, tuple(data.values()))
            return c.lastrowid
        except Error as e:
            print(f"Error inserting data: {e}")
            raise

    def update_data(self, table, data, condition, params=()):
        """Update data in the specified table"""
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        try:
            c = self.conn.cursor()
            c.execute(sql, tuple(data.values()) + tuple(params))
        except Error as e:
            print(f"Error updating data: {e}")
            raise

    def delete_data(self, table, condition, params=()):
        """Delete data from the specified table"""
        sql = f"DELETE FROM {table} WHERE {condition}"
        try:
            c = self.conn.cursor()
            c.execute(sql, params)
            return c.rowcount
        except Error as e:
            print(f"Error deleting data: {e}")
            raise

    def query_data(self, query, params=()):
        """Query data from the database"""
        try:
            c = self.conn.cursor()
            c.execute(query, params)
            return [dict(row) for row in c.fetchall()]
        except Error as e:
            print(f"Error querying data: {e}")
            raise

def db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with DatabaseHandler() as conn:
            return func(*args, conn, **kwargs)
    return wrapper
