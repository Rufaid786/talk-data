import os
from dotenv import load_dotenv
import snowflake.connector  
from snowflake.connector import DictCursor

load_dotenv()

#If a function name starts with an underscore, it is intended to be a private method and should not be called from outside the class.
class SnowflakeClient:
    #These operations are not allowed
    FORBIDDEN_KEYWORDS = ['DROP', 'DELETE', 'ALTER', 'TRUNCATE', 'GRANT', 'REVOKE','MERGE','UPDATE']

    def __init__(self):
        # Load environment variables from .env file connection is established using snowflake connector
        self.conn = snowflake.connector.connect(
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA')
        )

    def _validate_query(self, query:str)->None:
        """Basic validation to prevent execution of potentially harmful queries"""
        upper_query = query.upper()
        for keyword in self.FORBIDDEN_KEYWORDS:
            if keyword in upper_query:
                raise ValueError(f"Query contains forbidden keyword: {keyword}")

    def _limit_query(self, query:str, limit=100)->str:
        """Add a LIMIT clause to the query if not already present"""
        upper_query = query.upper()
        if 'LIMIT' not in upper_query:
            return query.rstrip(';') + f' LIMIT {limit};'
        return query
    
    #By default cursor returns a list of tuples, where each tuple represents a row of the result set.
    #Since we are passing these datas to LLM ,LLM won't be able to understand the data in tuple format, so we are converting it into dict for labelling the datas.
    def execute_query(self, query:str)->dict:
        """Execute a SQL query and return results as a list of dictionaries"""
        self._validate_query(query)
        limited_query = self._limit_query(query)
        cursor = self.conn.cursor(DictCursor)  # Use DictCursor to get results as dictionaries
        try:
            cursor.execute(limited_query)
            return cursor.fetchall()
        finally:
            cursor.close()

    #Tool can directly call execute_query and return its result.But since this data is something whichw e pass onto LLM its better to have some metadatas along with it
    #So that LLM can understand the data better and can also use the metadata for better reasoning and decision making and use it for troubleshooting if there is any error in the query execution.
    def execute_query_safely(self, query:str)->list[dict]:
        """It is a wapper around execute_query to add some metadata and validation before executing the query.This will be called by the tool"""
        try:    
            query_result=self.execute_query(query)
            columns =list(query_result[0].keys()) if query_result else []
            return {
                "success": True,
                "columns": columns,
                "row_count": len(query_result),
                "result": query_result,
                "executed_sql":self._limit_query(query)
            } 
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "executed_sql":self._limit_query(query),
                "hint":"Check your column name ,tablename and SQL syntax.Trye again with a corrected query"
            }  
        
    def list_tables_in_the_schema(self, schema:str=None)->dict:
        """List all tables in the current schema"""
        schema=schema or os.getenv('SNOWFLAKE_SCHEMA')
        query = f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{schema}';"
        return self.execute_query_safely(query)
    
    def describe_table(self, tablename:str)->dict:
        """Describe a table .Gives an overview of the table structure and its columns"""
        query = f"""
            SELECT COLUMN_NAME, DATA_TYPE, TABLE_SCHEMA, IS_NULLABLE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{tablename}'
            ORDER BY ORDINAL_POSITION;"""
        return self.execute_query_safely(query)
    
    def get_schema_conext(self,tables:list[str]=None)->dict:
        """Get current database, schema, warehouse and optionally list of tables in the schema"""
        if tables is None:
            tables_data=self.list_tables_in_the_schema()
            tables=[t['TABLE_NAME'] for t in tables_data['result']]

        output=["#Available Tables\n"]
        for table in tables:
            describe_data = self.describe_table(table)
            # Handle errors if describe_table returns an error status
            if not describe_data["success"]:
                output.append(f"\n## {table}\n Error: {describe_data['error']}")
                continue
            output.append(f"\n## {table}")
        
            # Access the result array
            results = describe_data.get('result', [])
            for col in results:
                output.append(
                    f"- `{col.get('COLUMN_NAME')}` ({col.get('DATA_TYPE')})"
                )
            
        return "\n".join(output)
    

    def close(self):
        """Close the Snowflake connection"""
        self.conn.close()

 