from snowflake_client import SnowflakeClient
from model import create_model
from dotenv import load_dotenv
import os
from agent_system_prompt import SNOWFLAKE_SYSTEM_PROMPT
from langchain.agents import create_agent
from tools import query_snowflake

load_dotenv()
model = create_model(os.getenv("GOOGLE_API_KEY"))

def build_snowflake_agent():
    client = SnowflakeClient()
    try:
        schema_context = client.get_schema_conext()
        print("scuccessfully retrieved schema context")
    finally:
        client.close()
    prompt=SNOWFLAKE_SYSTEM_PROMPT.format(schema_context=schema_context)

    agent=create_agent(model=model, tools=[query_snowflake], system_prompt=prompt)

    return agent