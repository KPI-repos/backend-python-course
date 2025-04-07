import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

DB_CONFIG = {
    "dbname": "restaurant",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": "5432"
}

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
    finally:
        if conn is not None:
            conn.close()

@contextmanager
def get_db_cursor(commit=False):
    """Context manager for database cursors"""
    with get_db_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            if commit:
                conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()

def execute_query(query, params=None, commit=True):
    """Execute a query and return results"""
    with get_db_cursor(commit=commit) as cursor:
        cursor.execute(query, params or ())
        if cursor.description is not None:
            return cursor.fetchall()
        return None