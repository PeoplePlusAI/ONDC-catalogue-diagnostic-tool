import pandas as pd
import sqlite3
import json


def connect_to_database(database_path):
    """
    Connects to the SQLite database and returns the connection object.
    
    Args:
    - database_path: The path to the SQLite database file.
    
    Returns:
    - conn: The connection object.
    """
    conn = sqlite3.connect(database_path)
    return conn

def import_csv_to_database(csv_file_path, table_name, conn):
    """
    Imports a CSV file into the SQLite database.
    
    Args:
    - csv_file_path: The path to the CSV file.
    - table_name: The name of the table to be created in the database.
    - conn: The connection object to the SQLite database.
    """
    df = pd.read_csv(csv_file_path)
    df.to_sql(table_name, conn, if_exists='replace')
    return df

def execute_sql_query(query, conn):
    """
    Executes an SQL query on the SQLite database and returns the result as a pandas DataFrame.
    
    Args:
    - query: The SQL query to be executed.
    - conn: The connection object to the SQLite database.
    
    Returns:
    - df_query_result: The result of the query as a pandas DataFrame.
    """
    df_query_result = pd.read_sql_query(query, conn)
    return json.loads(df_query_result.to_json())

def extract_column_query_result(df_query_result):
    """
    Displays the result of an SQL query as JSON.
    
    Args:
    - df_query_result: The result of the query as a pandas DataFrame.
    """
    return eval(list(df_query_result.values())[0].get('0'))
    

def extract_row_query_result(df_query_result):
    """
    Displays the result of an SQL query as JSON.
    
    Args:
    - df_query_result: The result of the query as a pandas DataFrame.
    """
    return list(df_query_result.get("index").values())


def run_sql_queries(csv_file_path, column_query, row_query):
    """
    Generates SQL queries based on the requirements and the column names.
    
    Args:
    - csv_file_path: The path to the CSV file.
    - queries: The requirements for the SQL queries.
    
    Returns:
    - sql_queries: The generated SQL queries.
    """
    conn = connect_to_database('db/my_database.db')
    df = import_csv_to_database(csv_file_path, 'products', conn)
    query1 = column_query
    query2 = row_query
    df_query_result = execute_sql_query(query1, conn)
    column_query_result = extract_column_query_result(df_query_result)
    passed = False
    if column_query_result == True:
        df_query_result = execute_sql_query(query2, conn)
        failed_rows = extract_row_query_result(df_query_result)
        passed = False if failed_rows else True
    return {"passed": passed, "failed_rows": failed_rows}
