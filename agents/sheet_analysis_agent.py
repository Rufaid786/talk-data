from model import create_model
from dotenv import load_dotenv
import pandas as pd
import os
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

load_dotenv()
model = create_model(os.getenv("GROQ_API_KEY"))


def build_sheet_analysis_agent(df: pd.DataFrame):
    agent = create_pandas_dataframe_agent(
        model, df, allow_dangerous_code=True
    )
    return agent