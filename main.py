from agents.agent_orchestrator_graph import AgentGraph


import streamlit as st
import pandas as pd

#Initialzing agnet once and storing in session state to persist across interactions
if "agent" not in st.session_state:
    st.session_state.agent = AgentGraph()

st.title("TalkData: Your Data Companion")

st.write("Welcome to TalkData! Ask a question about your data.I will help you to answer it")

uploaded_file = st.file_uploader(
    "Upload an Excel or CSV file",
    type=["xlsx", "csv"],
)

user_query = st.text_input("Enter your data question here...", key="user_query")

@st.cache_data
def query_to_send_uploaded_file(uploaded_file):
    try:
        return pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file, engine="openpyxl")
    except Exception as e:
        st.error(f"Error loading file: {e}")   
        return None  


def query_to_send_to_agent():
    if uploaded_file and user_query:
        df = query_to_send_uploaded_file(uploaded_file)
        return user_query, df
    elif uploaded_file and not user_query:
        df = query_to_send_uploaded_file(uploaded_file)
        return "Summarize this dataset and tell me the main trends.", df
    elif user_query:
        return user_query, None
    else:
        return None, None

if st.button("Ask TalkData"):
    query_to_send, df = query_to_send_to_agent()
    result = st.session_state.agent.call_agents({
            "user_query": query_to_send,
            "df": df
    })
    output = result.get("messages", [])[-1]
    output_text = output.content if hasattr(output, 'content') else str(output)

    st.markdown("---")
    st.markdown("### Result")
    st.write(output_text)
        

