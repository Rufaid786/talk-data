from utils.snowflake_client import SnowflakeClient
from model import create_model
from dotenv import load_dotenv
import os
from systemprompts.snowflake_agent_system_prompt import SNOWFLAKE_SYSTEM_PROMPT
from langchain.agents import create_agent
from tools.snowflake_tools import query_snowflake_safely,describe_snowflake,list_tables_in_the_schema

load_dotenv()
model = create_model(os.getenv("GROQ_API_KEY"))

def build_snowflake_agent():
    client = SnowflakeClient()
    try:
        schema_context = client.get_schema_conext()
        print("scuccessfully retrieved schema context")
    finally:
        client.close()
    prompt=SNOWFLAKE_SYSTEM_PROMPT.format(schema_context=schema_context)

    agent=create_agent(model=model, tools=[query_snowflake_safely,describe_snowflake,list_tables_in_the_schema], system_prompt=prompt)

    return agent