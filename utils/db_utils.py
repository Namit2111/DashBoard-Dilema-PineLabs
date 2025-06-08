import sqlite3
import pandas as pd
from config.config import DB_PATH



def connect(db_path=DB_PATH):
    """Establish and return a database connection."""
    return sqlite3.connect(db_path)


def get_table_names():
    """Return a list of all table names in the database."""
    conn = connect()
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql(query, conn)
    conn.close()
    return tables['name'].tolist()


def get_table_schema(table_name):
    """Return the schema (column name + type) of a given table."""
    conn = connect()
    query = f"PRAGMA table_info({table_name});"
    schema = pd.read_sql(query, conn)
    conn.close()
    return schema[['name', 'type']]


def get_column_names(table_name):
    """Return just the column names of a given table."""
    schema = get_table_schema(table_name)
    return schema['name'].tolist()


def preview_table(table_name, limit=5):
    """Return the first N rows of a table."""
    conn = connect()
    query = f"SELECT * FROM {table_name} LIMIT {limit};"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def run_query(query):
    """Run a raw SQL query and return the result as a DataFrame."""
    conn = connect()
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def get_table_row_count(table_name):
    """Return the number of rows in a table."""
    conn = connect()
    query = f"SELECT COUNT(*) AS row_count FROM {table_name};"
    result = pd.read_sql(query, conn)
    conn.close()
    return result.iloc[0]['row_count']


def get_all_schemas():
    """Return schemas for all tables in the database."""
    tables = get_table_names()
    all_schemas = {}
    for table in tables:
        all_schemas[table] = get_table_schema(table)
    return all_schemas
