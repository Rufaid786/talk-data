from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from model import create_model
from dotenv import load_dotenv
import os
from systemprompts.supervisor_system_prompt import SUPERVISOR_DECISION_PROMPT, SUPERVISOR_SYNTHESIS_RESPONSE_PROMPT
from agents.snowflake_agent import build_snowflake_agent
from agents.sheet_analysis_agent import build_sheet_analysis_agent

load_dotenv()
model = create_model(os.getenv("GOOGLE_API_KEY"))

# Define state structure using TypedDict and operator.add
class AgentState(TypedDict):
    user_query: str
    messages: Annotated[list, operator.add]

def supervisor_agent_node(state: dict) -> dict:
    messages = state.get("messages", [])
    
    # Check if we are returning from an agent
    if messages:
        last_message = messages[-1]
        last_content = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        # If it's the agent's output (does not contain the routing instructions)
        if 'snowflake_agent' not in last_content and 'excel_agent' not in last_content:
            prompt=SUPERVISOR_SYNTHESIS_RESPONSE_PROMPT.format(
                user_query=state["user_query"],
                agent_response=last_content
            )
            response = model.invoke(prompt)
            return {"messages": [response]}

    # Initial run: Determine which agent to route to
    response = model.invoke(SUPERVISOR_DECISION_PROMPT.format(user_query=state["user_query"]))
    
    return {
        "user_query": state["user_query"],
        "messages": [response]
    }
    
def snowflake_agent_node(state: dict) -> dict:
    agent = build_snowflake_agent()
    # Invoke and add to message history
    response = agent.invoke({"messages": [{"role": "user", "content": state["user_query"]}]})  
    final_response = response["messages"][-1].content
    
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
    messages = state.get("messages", [])
    if not messages:
        return END
        
    last_message = messages[-1]
    
    if hasattr(last_message, 'content'):
        text_content = last_message.content.strip().lower()
    else:
        text_content = str(last_message).strip().lower()
        
    if 'snowflake_agent' in text_content:
        return 'snowflake'
    elif 'excel_agent' in text_content:
        return 'sheet'
    else:
        return END

# Initialize the graph
graph = StateGraph(AgentState)
graph.add_node("supervisor", supervisor_agent_node)
graph.add_node("snowflake", snowflake_agent_node)
graph.add_node("sheet", sheet_node)

graph.set_entry_point("supervisor")

graph.add_conditional_edges("supervisor", route_to_agent)
graph.add_edge("snowflake", "supervisor")
graph.add_edge("sheet", "supervisor")

agent = graph.compile()

if __name__ == "__main__":
    user_query = "what are the columns available in customer table?"
    result = agent.invoke({"user_query": user_query})
    final_response = result["messages"][-1].content
    print(final_response)