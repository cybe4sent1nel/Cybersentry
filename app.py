import streamlit as st
import os
import sys
import asyncio
import time
from typing import Optional

# --- 0. CRITICAL FIX: PATH INJECTION FOR CLOUD DEPLOYMENT ---
# This ensures Streamlit's environment can find the 'cybersentry' source code 
# located in the adjacent 'src' folder, bypassing the installation failure.
try:
    current_dir = os.path.dirname(__file__)
    # Insert the 'src' directory at the beginning of the Python path
    sys.path.insert(0, os.path.join(current_dir, 'src')) 
except Exception as e:
    print(f"Path insertion failed: {e}") 
# -----------------------------------------------------------

# --- 1. CONFIGURE EXTERNAL LIBRARIES AND AGENT PATHS ---
try:
    # These imports will now succeed because 'src' is in the path
    from cybersentry.sdk.agents import Agent, OpenAIChatCompletionsModel, Runner  
    from cybersentry.agents.one_tool import one_tool_agent # Example Agent Instance
    import litellm
    
    # Define your agent dictionary
    AVAILABLE_AGENTS = {
        "CTF Agent (One-Tool)": one_tool_agent,
        # "Blue Team Agent": blue_team_agent, # Placeholder for other agents
    }
    
    # Get initial model name from ENV (used as default in UI)
    DEFAULT_MODEL = os.getenv('CYBERSENTRY_MODEL', "openrouter/mistralai/mistral-7b-instruct:free")
    
except ImportError as e:
    # Fallback structure for failed imports
    st.error(f"FATAL ERROR: Could not import necessary Cybersentry modules ({e}).")
    st.info("Ensure your source code is available and dependencies are correct.")
    AVAILABLE_AGENTS = {"Error": None}
    DEFAULT_MODEL = "Error Loading Model"


# --- 2. ASYNCHRONOUS WRAPPER (The Crucial Fix) ---

def run_agent_task(agent: Agent, user_input: str, model_name: str, api_key: str) -> str:
    """Safely wraps the agent's asynchronous execution."""
    
    # 1. Update the agent's model dynamically
    agent.model.model = model_name
    agent.model.openai_client = litellm.client(api_key=api_key) 
    
    # 2. Define the main asynchronous operation
    async def async_run():
        try:
            # --- REPLACE THIS BLOCK WITH YOUR REAL AGENT CALL ---
            # You must replace this with the actual Runner.run() call from your SDK
            
            st.code(f"Running agent '{agent.name}' with model '{model_name}'...")
            await asyncio.sleep(3) 
            response = {"final_output": f"SUCCESS: [MOCK] Agent received input: '{user_input}'. Execution simulated."}
            # --- END MOCK ---
            
            return response.get("final_output", "Agent finished, but no output found.")
            
        except Exception as e:
            return f"Agent Execution Error: {str(e)}"
    
    # 3. Execute the asynchronous code synchronously
    return asyncio.run(async_run())


# --- 3. STREAMLIT UI LAYOUT ---

def main():
    st.set_page_config(layout="wide", page_title="Cybersentry Agent Framework")
    st.title("🛡️ Cybersentry Agent Web Interface")
    st.markdown("---")

    # --- SIDEBAR: Configuration Inputs ---
    with st.sidebar:
        st.header("1. Authentication")
        api_key = st.text_input(
            "OpenRouter/OpenAI API Key (PAT)", 
            type="password", 
            help="Required for LiteLLM to connect to the model provider."
        )
        st.info("Your key will be used as the OPENAI_API_KEY.")

        st.header("2. Agent & Model Selection")
        
        selected_agent_name = st.selectbox(
            "Select Agent Persona:",
            list(AVAILABLE_AGENTS.keys()),
            key='agent_select',
            index=0
        )
        selected_agent = AVAILABLE_AGENTS.get(selected_agent_name)

        model_name = st.text_input(
            "LiteLLM Model ID:",
            DEFAULT_MODEL,
            help="Must support Chat Completions API. e.g., openrouter/openai/gpt-3.5-turbo",
            key='model_input'
        )
        
        st.markdown("---")
        st.caption("Rate Limits (Currently set via ENV variables):")
        st.caption(f"RPM: {os.getenv('LITELLM_MAX_RPM', '40')} | TPM: {os.getenv('LITELLM_MAX_TPM', '80000')}")

    # --- MAIN CONTENT: Execution Area ---
    st.header(f"Agent: {selected_agent_name}")
    st.markdown("---")

    user_prompt = st.text_area(
        "Enter your cybersecurity command or challenge:",
        key='prompt_input',
        height=150
    )

    if st.button("Run Agent Execution", use_container_width=True, disabled=not api_key):
        if not api_key:
            st.warning("Please enter your API Key/PAT to run the agent.")
            return

        st.info("Initiating autonomous agent execution... Please wait.")
        
        with st.spinner("Analyzing environment and executing strategy..."):
            
            start_time = time.time()
            result = run_agent_task(selected_agent, user_prompt, model_name, api_key)
            duration = time.time() - start_time
            
        st.success(f"Execution Complete in {duration:.2f} seconds")
        st.subheader("Agent Response:")
        
        if result.startswith("Agent Execution Error"):
            st.error(result)
        else:
            st.code(result, language='text')

if __name__ == "__main__":
    main()
