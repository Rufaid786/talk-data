from langchain_core.tools import tool
from snowflake_client import SnowflakeClient

client = SnowflakeClient()

@tool
def query_snowflake(query: str) -> dict:
    """Execute a read-only SQL query against a Snowflake data warehouse. 
    Only SELECT statements are allowed; write operations are blocked. 
    Use the exact table name and column name from the schema provided. 
    Do not guess column names or table names.

    Args:
        query: A valid SQL SELECT query to execute against Snowflake.
    """
    print(f"Executing query in tool: {query}")
    return client.execute_query_safely(query)