from langchain_core.tools import tool
from utils.snowflake_client import SnowflakeClient

client = SnowflakeClient()

@tool
def query_snowflake_safely(query: str) -> dict:
    """Execute a read-only SQL query against a Snowflake data warehouse. 
    Only SELECT statements are allowed; write operations are blocked. 
    Use the exact table name and column name from the schema provided. 
    Do not guess column names or table names.

    Args:
        query: A valid SQL SELECT query to execute against Snowflake.
    """
    print(f"Executing query in tool: {query}")
    return client.execute_query_safely(query)

@tool
def describe_snowflake(table: str) -> dict:
    """Execute a read-only describe query against a Snowflake data warehouse. 
    Gives an overview of the table structure and its columns. Use the exact table name.

    Args:
        table (str): A valid table name to describe.

    Returns:
        dict: A dictionary containing column details, schema, data type, and nullability.
    """
    print(f"Executing describe query in tool for table: {table}")
    return client.describe_table(table)

from langchain_core.tools import tool

@tool
def list_tables_in_the_schema(user_input_schema: str = None) -> dict:
    """List all tables in the current schema.
    Fetches a list of table names from the Snowflake schema. 
    If no schema is provided, it defaults to the one set in the environment variables.

    Args:
        schema (str, optional): A valid schema name to list tables from. 

    Returns:
        dict: A dictionary containing the query execution status and the list of table names.
    """
    print(f"Listing tables in schema: {user_input_schema}")
    return client.list_tables_in_the_schema(user_input_schema)