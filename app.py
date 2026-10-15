import streamlit as st
import json
from agent.llm_agent import NemotronAgent
from env.gym_env import CodingGymEnv

st.set_page_config(page_title="AI Agent Coding Gym", layout="wide")

st.title("🤖 Nebius x NVIDIA: Agent Evaluation Gym")
st.markdown("Benchmarking **NVIDIA Nemotron** on autonomous code-fixing tasks.")

# Sidebar for API Key & Model Selection
st.sidebar.header("Configuration")
nebius_api_key = st.sidebar.text_input("Nebius API Key", type="password")
model_choice = st.sidebar.selectbox("Model", ["nvidia/nemotron-4-340b-instruct", "nvidia/nemotron-3-super"])

# Load Tasks
with open("data/tasks.json", "r") as f:
    tasks = json.load(f)

task_titles = [f"{t['task_id']}: {t['title']}" for t in tasks]
selected_task_title = st.selectbox("Select Task", task_titles)
selected_task = next(t for t in tasks if f"{t['task_id']}: {t['title']}" == selected_task_title)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Task Description")
    st.write(selected_task["description"])
    st.subheader("Buggy Code")
    st.code(selected_task["buggy_code"], language="python")

if st.button("🚀 Run Agent Evaluation"):
    if not nebius_api_key:
        st.error("Please enter a valid Nebius API key in the sidebar.")
    else:
        agent = NemotronAgent(api_key=nebius_api_key, model=model_choice)
        env = CodingGymEnv(selected_task)
        
        with st.spinner("Nemotron agent generating code fix..."):
            fixed_code = agent.generate_fix(selected_task["buggy_code"], selected_task["description"])
        
        with col2:
            st.subheader("Agent Proposed Fix")
            st.code(fixed_code, language="python")
            
            # Step in Gym Environment
            _, reward, passed, logs = env.step(fixed_code)
            
            st.subheader("Evaluation Results")
            if passed:
                st.success(f"✅ Tests Passed! Reward: {reward}")
            else:
                st.error(f"❌ Tests Failed. Reward: {reward}")
            
            with st.expander("Pytest Output Logs"):
                st.text(logs)
