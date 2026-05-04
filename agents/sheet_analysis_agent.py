from model import create_model
from dotenv import load_dotenv
import pandas as pd
import os
from langchain_experimental.agents.agent_toolkits import create_csv_agent

load_dotenv()
model = create_model(os.getenv("GOOGLE_API_KEY"))


def ensure_csv(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".xlsx":
        print("checking excel file and converting to csv if needed...")
        df = pd.read_excel(file_path,engine="openpyxl")
        csv_path = file_path.rsplit(".", 1)[0] + ".csv"
        df.to_csv(csv_path, index=False)
        return csv_path

    return file_path
        
     
def build_sheet_analysis_agent(file_path:str):
    agent = create_csv_agent(
        model, ensure_csv(file_path), allow_dangerous_code=True, handle_parsing_errors=True
    )
    return agent