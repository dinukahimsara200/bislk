"""
db.py — Database connection helper for BisLK
Uses mysql-connector-python (pip install mysql-connector-python)
XAMPP default: host=localhost, user=root, password=''
"""

import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
from flask import current_app


def get_connection():
    """
    Opens and returns a raw MySQL connection.
    Use get_db() context manager in route handlers instead.
    """
    try:
        conn = mysql.connector.connect(
            host     = current_app.config['DB_HOST'],
            user     = current_app.config['DB_USER'],
            password = current_app.config['DB_PASSWORD'],
            database = current_app.config['DB_NAME'],
            charset  = 'utf8mb4'
        )
        return conn
    except Error as e:
        current_app.logger.error(f"Database connection failed: {e}")
        raise


@contextmanager
def get_db():
    """
    Context manager — automatically commits and closes.

    Usage in a route:
        with get_db() as (conn, cur):
            cur.execute("SELECT ...")
            rows = cur.fetchall()
    """
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)   # rows come back as dicts
    try:
        yield conn, cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()