import streamlit as st
import os
import asyncio
import time
import json
from rich.console import Console # Used for simulating the CLI context
from typing import Optional

# --- 1. CONFIGURE EXTERNAL LIBRARIES AND AGENT PATHS ---
# Note: You may need to adjust these imports based on your final Cybersentry structure.
try:
    # Assuming the Agent classes are accessible via the SDK path
    # If this fails, you need to ensure your local package is installed with 'pip install -e .'
    from cybersentry.sdk.agents import Agent, OpenAIChatCompletionsModel, Runner 
    from cybersentry.agents.one_tool import one_tool_agent # Example Agent Instance
    # You might also need to initialize LiteLLM settings here, but we rely on ENV vars.
    import litellm
    
    # Define your agent dictionary based on the names the user selects
    AVAILABLE_AGENTS = {
        "CTF Agent (One-Tool)": one_tool_agent,
        # "Blue Team Agent": blue_team_agent, # Placeholder for other agents
    }
    
    # Get initial model name from ENV (as set in your one_tool.py)
    DEFAULT_MODEL = os.getenv('CYBERSENTRY_MODEL', "openrouter/mistralai/mistral-7b-instruct:free")
    
except ImportError as e:
    # Fallback structure for development environment issues
    st.error(f"FATAL ERROR: Could not import necessary Cybersentry modules ({e}).")
    st.info("Please ensure you have run 'pip install -e .' in your terminal.")
    AVAILABLE_AGENTS = {"Error": None}
    DEFAULT_MODEL = "Error Loading Model"


# --- 2. ASYNCHRONOUS WRAPPER (The Crucial Fix) ---

# Since Streamlit runs synchronously, we must use asyncio.run() to execute our agent.
def run_agent_task(agent: Agent, user_input: str, model_name: str, api_key: str) -> str:
    """Safely wraps the agent's asynchronous execution."""
    
    # 1. Update the agent's model dynamically with user-provided settings
    # This is necessary because Streamlit clears sessions often.
    agent.model.model = model_name
    agent.model.openai_client = litellm.client(api_key=api_key) 
    
    # 2. Define the main asynchronous operation
    async def async_run():
        try:
            # We mock a small runner execution here for simplicity, 
            # but you would call your actual agent execution logic (Runner.run)
            st.code(f"Running agent '{agent.name}' with model '{model_name}'...")
            
            # Assuming Cybersentry's run signature:
            # response = await Runner.run(agent, user_input)
            
            # --- MOCK RESPONSE FOR DEMO (REPLACE WITH REAL Runner.run CALL) ---
            await asyncio.sleep(3) 
            response = {"final_output": f"SUCCESS: [MOCK] Agent received input: '{user_input}'. Simulation of {agent.name} is complete."}
            # --- END MOCK ---
            
            # Process and return the final output
            return response.get("final_output", "Agent finished, but no output found.")
            
        except Exception as e:
            return f"Agent Execution Error: {str(e)}"
    
    # 3. Execute the asynchronous code synchronously
    # NOTE: This creates a new event loop and runs the agent within it.
    return asyncio.run(async_run())


# --- 3. STREAMLIT UI LAYOUT ---

def main():
    st.set_page_config(layout="wide", page_title="Cybersentry Agent Framework")
    st.title("🛡️ Cybersentry Agent Web Interface")
    st.markdown("---")

    # --- SIDEBAR: Configuration Inputs ---
    with st.sidebar:
        st.header("1. Authentication")
        # PAT/API Key input
        api_key = st.text_input(
            "OpenRouter/OpenAI API Key (PAT)", 
            type="password", 
            help="Required for LiteLLM to connect to the model provider."
        )
        st.info("Your key will be used as the OPENAI_API_KEY for all LiteLLM calls.")

        st.header("2. Agent & Model Selection")
        
        # Agent selection
        selected_agent_name = st.selectbox(
            "Select Agent Persona:",
            list(AVAILABLE_AGENTS.keys()),
            key='agent_select',
            index=0
        )
        selected_agent = AVAILABLE_AGENTS.get(selected_agent_name)

        # Model selection (using the default from ENV or code)
        model_name = st.text_input(
            "LiteLLM Model ID:",
            DEFAULT_MODEL,
            help="e.g., openrouter/openai/gpt-3.5-turbo. Must support Chat Completions API.",
            key='model_input'
        )
        
        # Display rate limit warning/info
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
        
        # Display loading spinner while the synchronous call blocks
        with st.spinner("Analyzing environment and executing strategy..."):
            
            # --- Execute the agent logic ---
            start_time = time.time()
            result = run_agent_task(selected_agent, user_prompt, model_name, api_key)
            duration = time.time() - start_time
            
        # --- Display Results ---
        st.success(f"Execution Complete in {duration:.2f} seconds")
        st.subheader("Agent Response:")
        
        # Try to parse as code block for nice display, otherwise show raw text
        if result.startswith("Agent Error"):
            st.error(result)
        else:
            st.code(result, language='text')

if __name__ == "__main__":
    main()
