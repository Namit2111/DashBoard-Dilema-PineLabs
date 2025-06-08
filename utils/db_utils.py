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

def get_colums_schema(table_name):
    """Return the schema of a given columsn of a table."""
    schema = get_table_schema(table_name)
    return schema[['name', 'type']]


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


def execute_query(query: str, fetch: bool = True):
    """
    Execute a SQL query. Fetch results if it's a SELECT query.

    Args:
        query (str): The SQL query to run.
        fetch (bool): Whether to fetch and return data (for SELECT queries).

    Returns:
        pd.DataFrame if fetch is True and the query is SELECT; otherwise, None.
    """
    conn = connect()
    try:
        if fetch:
            df = pd.read_sql(query, conn)
            return df
        else:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
    except Exception as e:
        print(f"Error running query: {e}")
        raise
    finally:
        conn.close()


def summarize_dataframe(df: pd.DataFrame, max_rows: int = 50) -> str:
    """Return a summarized Markdown representation of a large DataFrame."""
    summary = {
        "columns": list(df.columns),
        "num_rows": len(df),
        "top_rows": df.head(5).to_markdown(index=False),
        "summary_stats": df.describe(include='all').to_markdown()
    }

    return f"""
# Summary of Large Dataset

**Columns**: {summary['columns']}
**Total Rows**: {summary['num_rows']}

## Sample (First 5 Rows)
{summary['top_rows']}

## Descriptive Statistics
{summary['summary_stats']}
"""


def get_distinct_column_values(table, column):
    """Returns distinct values for a column from the table."""
    conn = connect()
    query = f"SELECT DISTINCT {column} FROM {table};"
    result = pd.read_sql(query, conn)
    conn.close()
    return result[column].dropna().tolist()
