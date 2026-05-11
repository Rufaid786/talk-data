from model import create_model
from dotenv import load_dotenv
import pandas as pd
import os
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_core.messages import SystemMessage

load_dotenv()
model = create_model(os.getenv("GROQ_API_KEY"))


def build_sheet_analysis_agent(df: pd.DataFrame):
    print("sheet prompt invoked")
    # This prompt tells the LLM exactly how to handle tool parameters
    system_prompt = (
        "You are a strict Data Analyst. You have access to a pandas DataFrame and SQL tools. "
        "CRITICAL INSTRUCTIONS:\n"
        "1. When calling tools, NEVER pass 'null' or None for required string parameters.\n"
        "2. If a tool requires a 'schema' or 'user_input_schema', use an empty string '' if unknown, "
        "but NEVER use null.\n"
        "3. First, use python_repl_ast to inspect the dataframe (df.info(), df.head()).\n"
        "4. Only use SQL tools if the user explicitly asks for database-wide metadata.\n"
        "5. If you are unsure of a parameter value, do not guess; use an empty string or 'public'."
    )

    agent = create_pandas_dataframe_agent(
        model, 
        df, 
        allow_dangerous_code=True,
        # Use Tool Calling for modern Groq/Llama models
        agent_type="tool-calling", 
        verbose=True,
        system_message=SystemMessage(content=system_prompt)
    )
    return agent