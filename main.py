import streamlit as st
import pandas as pd
from agents.agent_orchestrator_graph import AgentGraph

# 1. Initialization
if "agent" not in st.session_state:
    st.session_state.agent = AgentGraph()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_df" not in st.session_state:
    st.session_state.current_df = None

st.title("TalkData: Your Data Companion")

# 2. Helper for File Loading
@st.cache_data
def load_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        return pd.read_excel(uploaded_file, engine="openpyxl")
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# 3. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle Input
prompt = st.chat_input("Ask about your data...", accept_file=True)

if prompt:
    user_text = prompt.text or ""
    display_content = user_text
    
    # Process File if present
    if prompt.files:
        st.session_state.current_df = load_data(prompt.files[0])
        file_name = prompt.files[0].name
        display_content += f"\n\n*(Uploaded: {file_name})*"
        
        # Default query if only file is uploaded
        if not user_text:
            user_text = "Summarize this dataset and tell me the main trends."

    # Display User Message
    with st.chat_message("user"):
        st.markdown(display_content)
    st.session_state.messages.append({"role": "user", "content": display_content})

    # 5. Agent Interaction
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = st.session_state.agent.call_agents({
                "user_query": user_text,
                "df": st.session_state.current_df
            })
            
            # Extract content safely
            output = result.get("messages", [])[-1]
            output_text = output.content if hasattr(output, 'content') else str(output)
            
            st.markdown(output_text)
            st.session_state.messages.append({"role": "assistant", "content": output_text})