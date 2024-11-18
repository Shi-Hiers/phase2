import pymysql
from app.db_connect import get_db

def fetch_all(query, params=()):
    """Fetch all results for a given query and parameters."""
    connection = get_db()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def fetch_one(query, params=()):
    """Fetch a single result for a given query and parameters."""
    connection = get_db()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query, params)
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

def execute_query(query, params=()):
    """Execute a query and commit changes."""
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    cursor.close()
    connection.close()
