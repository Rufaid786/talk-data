
from langgraph.graph import StateGraph, END
from model import create_model
from dotenv import load_dotenv
import os
from systemprompts.supervisor_system_prompt import SUPERVISOR_PROMPT
from agents.snowflake_agent import build_snowflake_agent
from agents.sheet_analysis_agent import build_sheet_analysis_agent

load_dotenv()
model = create_model(os.getenv("GOOGLE_API_KEY"))

def supervisor_agent_node(state: dict) -> dict:
    
    response = model.invoke(SUPERVISOR_PROMPT.format(user_query=state["user_query"]))

    return {
        "user_query": state["user_query"],
        "messages": [response]
    }
    

def snowflake_agent_node(state: dict) -> dict:
    agent = build_snowflake_agent()
    # Invoke and update the state's message history
    agent_response = agent.invoke({"messages": [{"role": "user", "content": state["user_query"]}]})  
    final_response=agent_response["messages"][-1].content
    print(f"Snowflake agent response: {final_response}")
    
    return {
        "messages": [final_response]
    }

def sheet_node(state: dict) -> dict:
    file_path = "sampledatas.csv" 
    agent = build_sheet_analysis_agent(file_path)
    result = agent.invoke({"input": state["user_query"]})
    
    return {
        "messages": [result["output"]]
    }

def route_to_agent(state: dict) -> str:
    lastmessage = state['messages'][-1].content.strip().lower()
    
    # Return a string instead of a dictionary
    if 'snowflake_agent' in lastmessage:
        return 'snowflake'
    elif 'excel_agent' in lastmessage:
        return 'sheet'
    else:
        return END

# Initialize the graph
graph = StateGraph(dict)
graph.add_node("supervisor", supervisor_agent_node)
graph.add_node("snowflake", snowflake_agent_node)
graph.add_node("sheet", sheet_node)

graph.set_entry_point("supervisor")

graph.add_conditional_edges("supervisor", route_to_agent)
graph.add_edge("snowflake", "supervisor")
graph.add_edge("sheet", "supervisor")

agent = graph.compile()

if __name__ == "__main__":
    user_query = "how many rows are there in customer table?"
    result = agent.invoke({"user_query": user_query})
    print(result)