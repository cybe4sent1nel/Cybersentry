import streamlit as st
import os
import sys
import asyncio
import time
import logging
import warnings
import random
from pathlib import Path
from dotenv import load_dotenv

# ============================================================================
# 1. SETUP & ENVIRONMENT
# ============================================================================

# Ensure 'src' is in the python path so cybersentry imports work
current_dir = Path(__file__).parent
src_path = current_dir / "src"
if src_path.exists():
    sys.path.append(str(src_path))

load_dotenv()

# Force Disable Tracing to prevent 401 Errors (from cli.py)
os.environ["CYBERSENTRY_TRACING"] = "false"
os.environ["TRACING_ENABLED"] = "false"

# Suppress Warnings (from cli.py)
warnings.filterwarnings("ignore", category=RuntimeWarning, module="asyncio")
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
warnings.filterwarnings("ignore", message=".*Pydantic serializer warnings.*")

# Configure logging
logging.basicConfig(level=logging.ERROR)

# ============================================================================
# 2. CYBERSENTRY IMPORTS
# ============================================================================
try:
    from cybersentry.util import (
        fix_litellm_transcription_annotations,
        setup_ctf,
        is_pentestperf_available,
        COST_TRACKER
    )
    from cybersentry.sdk.agents import Runner, Agent
    from cybersentry.agents import get_agent_by_name
    from cybersentry.sdk.agents.simple_agent_manager import AGENT_MANAGER
    from cybersentry.sdk.agents.global_usage_tracker import GLOBAL_USAGE_TRACKER
    from cybersentry.sdk.agents.run_to_jsonl import get_session_recorder
    
    # Import Patterns dynamically
    from cybersentry.agents.patterns.bb_triage import bb_triage_swarm_pattern
    from cybersentry.agents.patterns.offsec import offsec_pattern
    from cybersentry.agents.patterns.red_blue_team import blue_team_red_team_shared_context_pattern
    
except ImportError as e:
    st.error(f"Critical Import Error: {e}. Please ensure 'src' directory is present and dependencies are installed.")
    st.stop()

# ============================================================================
# 3. UTILITY FUNCTIONS (Ported from CLI)
# ============================================================================

def update_agent_models_recursively(agent, new_model, visited=None):
    """Recursively update model for agent and handoffs."""
    if visited is None:
        visited = set()
    
    if hasattr(agent, "name") and agent.name in visited:
        return
    if hasattr(agent, "name"):
        visited.add(agent.name)
    
    if hasattr(agent, "model") and hasattr(agent.model, "model"):
        agent.model.model = new_model
        # Reset client to force recreation
        if hasattr(agent.model, "_client"):
            agent.model._client = None
            
    if hasattr(agent, "handoffs"):
        for handoff_item in agent.handoffs:
            if hasattr(handoff_item, "model"):
                update_agent_models_recursively(handoff_item, new_model, visited)

CYBER_PHRASES = [
    "Decrypting your intentions...", "Scanning for vulnerabilities...",
    "Bypassing confusion firewalls...", "Brute-forcing solution space...",
    "Injecting intelligence...", "Performing pentesting analysis...",
    "Escalating privileges...", "Cracking cryptographic puzzles...",
    "Exploiting knowledge bases...", "Reverse engineering query...",
    "Executing zero-day strategy...", "Fuzzing for optimal solutions...",
    "Deploying persistent answers...", "Hacking through your questions...",
]

def get_random_status():
    return random.choice(CYBER_PHRASES)

# ============================================================================
# 4. STREAMLIT UI SETUP
# ============================================================================

st.set_page_config(
    page_title="CyberSentry Interface",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Terminal Look
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #00ff41;
    }
    div.stButton > button {
        background-color: #003300;
        color: #00ff41;
        border: 1px solid #00ff41;
    }
    div.stButton > button:hover {
        background-color: #00ff41;
        color: #000000;
    }
    .stTextInput > div > div > input {
        color: #00ff41;
        background-color: #000000;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 5. SESSION STATE MANAGEMENT
# ============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_initialized" not in st.session_state:
    # One-time setup
    fix_litellm_transcription_annotations()
    session_logger = get_session_recorder()
    GLOBAL_USAGE_TRACKER.start_session(session_id=session_logger.session_id, agent_name=None)
    st.session_state.session_initialized = True

if "current_agent_object" not in st.session_state:
    st.session_state.current_agent_object = None

# ============================================================================
# 6. SIDEBAR CONFIGURATION
# ============================================================================

with st.sidebar:
    st.title("🛡️ CyberSentry")
    st.caption("Advanced Security Agent Interface")

    # --- Mode Selection ---
    mode = st.radio("Operation Mode", ["Single Agent", "Pattern / Swarm"])

    selected_agent_obj = None
    selected_agent_name = ""

    if mode == "Single Agent":
        # List based on files provided
        available_agents = [
            "one_tool",
            "red_teamer",
            "blue_teamer",
            "bug_bounter",
            "codeagent",
            "dfir",
            "android_sast_agent",
            "memory_analysis_agent",
            "network_traffic_analyzer",
            "replay_attack_agent",
            "reporter",
            "retester",
            "reverse_engineering_agent",
            "subghz_sdr_agent",
            "wifi_security_tester"
        ]
        selected_agent_key = st.selectbox("Select Agent", available_agents, index=0)
        
        # Load the agent logic
        try:
            selected_agent_obj = get_agent_by_name(selected_agent_key, agent_id="StreamlitUser")
            selected_agent_name = getattr(selected_agent_obj, "name", selected_agent_key)
        except Exception as e:
            st.error(f"Failed to load agent: {e}")

    else:
        # Patterns from uploaded files
        patterns = {
            "Bug Bounty Swarm (Triage)": bb_triage_swarm_pattern,
            "Offensive Security Ops": offsec_pattern,
            "Red/Blue Team (Shared Context)": blue_team_red_team_shared_context_pattern
        }
        selected_pattern_key = st.selectbox("Select Pattern", list(patterns.keys()))
        selected_agent_obj = patterns[selected_pattern_key]
        selected_agent_name = selected_pattern_key

    # --- Model Configuration ---
    st.markdown("---")
    current_model = st.text_input(
        "Model ID", 
        value=os.getenv("CYBERSENTRY_MODEL", "cybe4sent1nel0"),
        help="E.g., openrouter/mistralai/mistral-7b-instruct:free"
    )

    # --- Session Stats ---
    st.markdown("---")
    st.subheader("Session Stats")
    cost = COST_TRACKER.session_total_cost
    st.metric("Total Cost", f"${cost:.6f}")
    
    # --- CTF Status ---
    if is_pentestperf_available():
        st.success("🚩 CTF Environment Detected")
        if st.button("Reset CTF"):
            setup_ctf()
            st.toast("CTF Environment Reset!")

    if st.button("Clear Chat History", type="primary"):
        st.session_state.messages = []
        st.rerun()

# ============================================================================
# 7. MAIN CHAT LOGIC
# ============================================================================

st.subheader(f"Active: {selected_agent_name}")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Enter command or prompt..."):
    # 1. Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Prepare Agent
    if selected_agent_obj:
        # Update model if changed
        update_agent_models_recursively(selected_agent_obj, current_model)
        
        # Switch Agent Manager Context
        # (Ideally we reset registry or handle switching, simplified here for Streamlit)
        AGENT_MANAGER.switch_to_single_agent(selected_agent_obj, selected_agent_name)

        # 3. Execute Agent (Async wrapper)
        async def run_async_step():
            try:
                # Run the agent
                result = await Runner.run(selected_agent_obj, prompt)
                return result
            except Exception as e:
                return f"Error executing agent: {str(e)}"

        # 4. Display "Thinking" UI
        with st.chat_message("assistant"):
            status_text = get_random_status()
            with st.status(status_text, expanded=True) as status:
                st.write("Initializing agent runtime...")
                st.write(f"Target Model: {current_model}")
                
                # Run the async loop
                start_time = time.time()
                response_obj = asyncio.run(run_async_step())
                duration = time.time() - start_time
                
                status.update(label=f"Completed in {duration:.2f}s", state="complete", expanded=False)

            # 5. Parse and Display Output
            final_text = ""
            if hasattr(response_obj, "final_output"):
                final_text = response_obj.final_output
            elif isinstance(response_obj, str):
                final_text = response_obj
            else:
                final_text = str(response_obj)
            
            st.markdown(final_text)
            
            # Add to history
            st.session_state.messages.append({"role": "assistant", "content": final_text})
            
            # Force a rerun to update cost in sidebar
            st.rerun()
    else:
        st.error("No agent selected or failed to load agent.")

# Footer / Credits
st.markdown("---")
st.caption(f"CyberSentry Web Interface | Developer: cybe4sent1nel | CWD: {os.getcwd()}")
