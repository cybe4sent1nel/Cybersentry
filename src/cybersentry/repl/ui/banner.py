"""
Module for displaying the CYBERSENTRY banner and welcome message.
"""
# Standard library imports
import os
import glob
import logging
import sys
from configparser import ConfigParser

# Third-party imports
import requests  # pylint: disable=import-error
from rich.console import Console, Group  # FIX: Added Group here
from rich.panel import Panel  # pylint: disable=import-error
from rich.table import Table  # pylint: disable=import-error
from rich.text import Text    # FIX: Added Text here
from rich.columns import Columns  # FIX: Added Columns here
from rich.padding import Padding # ADDED: For cleaner spacing

# For reading TOML files
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        # If tomli is not available, we'll handle it in the get_version function
        pass


def get_version():
    """Get the CYBERSENTRY version from pyproject.toml."""
    version = "unknown"
    try:
        # Determine which TOML parser to use
        if sys.version_info >= (3, 11):
            toml_parser = tomllib
        else:
            try:
                import tomli as toml_parser
            except ImportError:
                logging.warning("Could not import tomli. Falling back to manual parsing.")
                # Simple manual parsing for version only
                with open('pyproject.toml', 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip().startswith('version = '):
                            # Extract version from line like 'version = "0.4.0"'
                            version = line.split('=')[1].strip().strip('"\'')
                            return version
                return version

        # Use proper TOML parser if available
        with open('pyproject.toml', 'rb') as f:
            config = toml_parser.load(f)
        version = config.get('project', {}).get('version', 'unknown')
    except Exception as e:  # pylint: disable=broad-except
        logging.warning("Could not read version from pyproject.toml: %s", e)
    return version


def get_supported_models_count():
    """Get the count of supported models (with function calling)."""
    try:
        # Fetch model data from LiteLLM repository
        response = requests.get(
            "https://raw.githubusercontent.com/BerriAI/litellm/main/"
            "model_prices_and_context_window.json",
            timeout=2
        )

        if response.status_code == 200:
            model_data = response.json()

            # Count models with function calling support
            function_calling_models = sum(
                1 for model_info in model_data.values()
                if model_info.get("supports_function_calling", False)
            )

            # Try to get Ollama models count
            try:
                ollama_api_base = os.getenv(
                    "OLLAMA_API_BASE",
                    "http://host.docker.internal:8000/v1"
                )
                ollama_response = requests.get(
                    f"{ollama_api_base.replace('/v1', '')}/api/tags",
                    timeout=1
                )

                if ollama_response.status_code == 200:
                    ollama_data = ollama_response.json()
                    ollama_models = len(
                        ollama_data.get(
                            'models', ollama_data.get('items', [])
                        )
                    )
                    return function_calling_models + ollama_models
            except Exception:  # pylint: disable=broad-except
                logging.debug("Could not fetch Ollama models")
                # Continue without Ollama models

            return function_calling_models
    except Exception:  # pylint: disable=broad-except
        logging.warning("Could not fetch model data from LiteLLM")

    # Default count if we can't fetch the data
    return "many"


def count_tools():
    """Count the number of tools in the CYBERSENTRY framework."""
    try:
        # Count Python files in the tools directory
        tool_files = glob.glob("cybersentry/tools/**/*.py", recursive=True)
        # Exclude __init__.py and other non-tool files
        tool_files = [
            f for f in tool_files
            if not f.endswith("__init__.py") and not f.endswith("__pycache__")
        ]
        return len(tool_files)
    except Exception:  # pylint: disable=broad-except
        logging.warning("Could not count tools")
        return "50+"


def count_agents():
    """Count the number of agents in the CYBERSENTRY framework."""
    try:
        # Count Python files in the agents directory
        agent_files = glob.glob("cybersentry/agents/**/*.py", recursive=True)
        # Exclude __init__.py and other non-agent files
        agent_files = [
            f for f in agent_files
            if not f.endswith("__init__.py") and not f.endswith("__pycache__")
        ]
        return len(agent_files)
    except Exception:  # pylint: disable=broad-except
        logging.warning("Could not count agents")
        return "20+"


def count_ctf_memories():
    """Count the number of CTF memories in the CYBERSENTRY framework."""
    # This is a placeholder - adjust the actual counting logic based on your
    # framework structure
    return "100+"


def display_banner(console: Console):
    """
    Display a stylized CYBERSENTRY banner with Alias Robotics corporate colors.

    Args:
        console: Rich console for output
    """
    version = get_version()

    # CYBERSENTRY'S ASCII BANNER DO NOT MESS WITH IT
    # Use noqa to ignore line length for the ASCII art
    banner = f"""

[bold green]                      ███
                              ████  █████
                          █████   ██    ████
                       ████    █████████    ████
                   ████    █████       █████   ████
                ████   █████     █████     ████    ████
             ████   ████        ███████       █████   ████                    ███
            ██  █████           ██   ██           █████  ██                  █████
            ██ ██                ██ ██                ██ ██                  ██ ██
            ████                  █ █                  ████                  ██ ██
            ████         ██████████ ██████████          ██                   ██ ██
            ██ █      ███          █          ██             ███        ██   ██ ███████████        █████████     ███  ██████
            ████      █  █████████████████████  █           █████      ████  ██          ███     ███       ███  ███████    █
            ████     █ ██                     ██ █          ██ ██      ████  ██  ████████  ██   ██  ███████  ██ ██    ██████
            ████   █████   █████       █████   █ ███        ██ ██      ████  ██ ██      ███ ██ ██ ██       █ ██ ██  ███
            ████  ███ ██  ███████     ███████  ██████       ██ ██      ████  ██ ██        █  █ ██ ███████████ █ ██ ██
            ██ █  ██  █   █    ██     █    ██  ██  ██       ██ ██      ████  ██ ██        █  █ ██            ██ ██ ██
            ████  ███ ██  ███████     ███████  ██████       ██ ██      █ ██  ██ ██       ██ ██ ██ █████████████ ██ ██
            ████   █████   █████       █████   █ ███        ██ ██    ███ ██  ██ ██     ███  ██ ██ ██            ██ ██
            ██ █     █ █                       █ █     ███   ██ █████  █ ██  ██  ███████   ██   ██  ██████████  ██ ██
            ██ ██    █ ███                   ███ █    █ █     ███    ███ ██   ███       ███      ███        ██  █████
             ██ ██    █  ██   ███████████   █   █    █  █      ███████ █ ██    ██████████          ██████████    ███
              ██ ██    ███                   ███   ██  █     █        ██ ██
               ██  ██       ███████████████      ███ ██     ██████████  ██
                 ██ ███                        ███  ██      ██        ███
                  ███ ████                   ███  ██         ██████████                       ███
                    ███  ████             ████  ███                                          █████
                      ███   ████       ████  ███                                             ██ ██
                         ███   █████████  ████  █████████    █████████     ███ █████████   ████ █████   ███ ██████  ███        ███
                            ████       ████   ██            ██       ███   █████      ███            █ █████       █████      █████
                               █████████     ██ █████████  █  ███████  ██  █    ██████  ██ ████ █████  ██   ██████ ██ ██      ██ ██
                                  ██         ██ ███       ██ █       ██ ██ █ ███     ██ ██   ██ ██     ██ ███      ██ ██      ██ ██
                                              ██   ████  ██ ███████████ ██ █ ██      ██ ██   ██ ██     ██ ██       ██ ██      ██ ██
                                               ████   ██ ██            ███ █ ██       █ ██   ██ ██     ██ ██       ██ ██      ██ ██
                                                  ████ ██ █  ████████████  █ ██       █ ██   ██ ██     ██ ██       ██ ██      ██ ██
                                            ████     █  █ ██ ███     █     █ ██       █ ██   ██ ██     ██ ██       ██ ███   ████ ██
                                               ██████  ██  ██  ██████ █    █ ██       █ ██   ██  █████ ██ ██        ██  █████    ██
                                             ██      ███    ████     ██    ████       ████    ███    █ █████         ███     ███ ██
                                              ████████        ████████     ███        ███       █████   ███            ██████ ██ ██
                                                                                                                              ██ ██
                                                                                                                            ███ ██
                                                       ██████████████████████████████████████████████████████████████████████  ██
                                                      ██                                                                     ███
                                                      ████████████████████████████████████████████████████████████████████████
                                                       ███ [/bold green]

[bold blue]                                         Cybersecurity AGENTIC AI (CYBERSENTRY), v{version}[/bold blue]
[white]                                              Bug bounty-ready AI[/white]
    """

    console.print(banner, end="")

    # # Create a table showcasing CYBERSENTRY framework capabilities
    # #
    # # reconsider in the future if necessary
    # display_framework_capabilities(console)


def display_framework_capabilities(console: Console):
    """
    Display a table showcasing CYBERSENTRY framework capabilities in Metasploit style.

    Args:
        console: Rich console for output
    """
    # Create the main table
    table = Table(
        title="",
        box=None,
        show_header=False,
        show_edge=False,
        padding=(0, 2)
    )

    table.add_column("Category", style="bold cyan")
    table.add_column("Count", style="bold yellow")
    table.add_column("Description", style="white")

    # Add rows for different capabilities
    table.add_row(
        "AI Models",
        str(get_supported_models_count()),
        "Supported AI models including GPT-4, Claude, Llama"
    )

    # table.add_row(
    #    "Tools",
    #    str(count_tools()),
    #    "Cybersecurity tools for reconnaissance and scanning"
    # )

    table.add_row(
        "Agents",
        str(count_agents()),
        "Spec.y.b.e.r.s.e.n.t.r.y.ed AI agents for different cybersecurity tasks"
    )

    # Add the table to a panel for better visual separation
    capabilities_panel = Panel(
        table,
        title="[bold blue]CYBERSENTRY Features[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    )

    console.print(capabilities_panel)


def display_welcome_tips(console: Console):
    """
    Display welcome message with tips for using the REPL.

    Args:
        console: Rich console for output
    """
    console.print(Panel(
        "[white]• Use arrow keys ↑↓ to navigate command history[/white]\n"
        "[white]• Press Tab for command completion[/white]\n"
        "[white]• Type /help for available commands[/white]\n"
        "[white]• Type /help cybe4sent1neles for command shortcuts[/white]\n"
        "[white]• Press Ctrl+L to clear the screen[/white]\n"
        "[white]• Press Esc+Enter to add a new line (multiline input)[/white]\n"
        "[white]• Press Ctrl+C to exit[/white]",
        title="Quick Tips",
        border_style="blue"
    ))


def display_agent_overview(console: Console):
    """
    Display a quick overview of available agents.

    Args:
        console: Rich console for output
    """
    # Create agents table
    agents_table = Table(
        title="",
        box=None,
        show_header=True,
        header_style="bold yellow",
        show_edge=False,
        padding=(0, 1)
    )

    agents_table.add_column("Agent", style="cyan", width=25)
    agents_table.add_column("Spec.y.b.e.r.s.e.n.t.r.y.ation", style="white")
    agents_table.add_column("Best For", style="green")
# Add agent rows (content remains the same)
    agents = [
        ("one_tool_agent", "🤖 Sentinel Shell (Core Agent)", "Quick CTF Solving, Direct Linux/Shell Operations"),
        ("red_teamer", "😈 PhantomPwn (Offensive Specialist)", "Advanced Penetration Testing, Zero-Day Exploitation"),
        ("blue_teamer", "🛡️ Aegis Defender (Defensive Sentinel)", "Proactive System Defense, Threat Monitoring & Hardening"),
        ("bug_bounter", "💰 VulneraFinder (Web/API Hunter)", "Automated Bug Bounty, Web Security & API Fuzzing"),
        ("dfir", "⏳ Chronos Analyst (Forensics Engine)", "Digital Incident Response, Deep Artifact Analysis"),
        ("network_traffic_analyzer", "📡 TrafficWhisperer (Packet Analyst)", "Real-time Network Traffic Analysis, Protocol Monitoring"),
        ("flag_discriminator", "🔑 Keystone Extractor (Flag Validation)", "Targeted CTF Flag Finding and Verification"),
        ("codeagent", "💻 GhostWriter (Code Integrity)", "Exploit Development, Static/Dynamic Code Analysis"),
        ("thought", "💡 Strategic Nexus (Planning Engine)", "High-Level Tactical Planning, Scenario Analysis"),
    ]

    for agent, spec, best_for in agents:
        agents_table.add_row(agent, spec, best_for)

    # Create the panel with new colors
    agent_panel = Panel(
        agents_table,
        title="[bold #00FF00]🤖 Deployed CYBERSENTRY Agents (Nexus Roster)[/bold #00FF00]", # Title changed to Lime Green
        border_style="#FF1493", # Border changed to Deep Pink
        padding=(1, 2),
        title_align="center"
    )
    console.print(agent_panel)


def display_quick_guide(console: Console):
    """Display the quick guide with comprehensive command reference."""
    # --- Styles
    CMD_STYLE = "green"
    CATEGORY_STYLE = "bold yellow"
    INFO_STYLE = "white"
    HIGHLIGHT_STYLE = "bold magenta"
    DIM_STYLE = "dim"
    LINK_STYLE = "blue underline"

    # --- 1. Command Matrix (Left Panel Content) ---
    help_text_content = Text.assemble(
        ("🤖 AGENT ORCHESTRATION", CATEGORY_STYLE), " (/a)\n",
        ("  CYBERSENTRY>/agent list", CMD_STYLE), " - **Show all deployed Agent personalities**\n",
        ("  CYBERSENTRY>/agent select [NAME]", CMD_STYLE), " - **Assign a new active Agent** (e.g., PhantomPwn)\n",
        ("  CYBERSENTRY>/agent info [NAME]", CMD_STYLE), " - **Display detailed specifications for an Agent**\n",
        ("  CYBERSENTRY>/parallel add [NAME]", CMD_STYLE), " - **Deploy an Agent into the Swarm Reconnaissance pool**\n\n",

        ("📚 KNOWLEDGE BASE & AUDIT TRAIL", CATEGORY_STYLE), "\n",
        ("  CYBERSENTRY>/memory list", CMD_STYLE), " - **List all persistent memories and learned data**\n",
        ("  CYBERSENTRY>/history", CMD_STYLE), " - **Review the full Command & Response history**\n",
        ("  CYBERSENTRY>/compact", CMD_STYLE), " - **Summarize the current session for context trimming**\n",
        ("  CYBERSENTRY>/flush", CMD_STYLE), " - **Wipe the current conversation context/history**\n\n",

        ("🌐 OPERATIONAL ENVIRONMENT", CATEGORY_STYLE), "\n",
        ("  CYBERSENTRY>/workspace set [NAME]", CMD_STYLE), " - **Isolate operations within a specific directory**\n",
        ("  CYBERSENTRY>/config", CMD_STYLE), " - **View and modify all runtime variables**\n",
        ("  CYBERSENTRY>/virt run [IMAGE]", CMD_STYLE), " - **Execute isolated security tools via Docker/VM**\n\n",

        ("🛠️ EXTERNAL TOOLS & MODELS", CATEGORY_STYLE), "\n",
        ("  CYBERSENTRY>/mcp load [TYPE] [CONFIG]", CMD_STYLE), " - **Integrate external MCP (Master Control Program) servers**\n",
        ("  CYBERSENTRY>/shell [COMMAND]", CMD_STYLE), " or **!** - **Execute immediate OS shell commands** (e.g., !ls)\n",
        ("  CYBERSENTRY>/model [NAME]", CMD_STYLE), " - **Switch the active Large Language Model** (LLM)\n\n",
    )

    help_panel = Panel(
        Padding(help_text_content, (0, 1)),
        title="[bold magenta]🧠 CYBERSENTRY Nexus Command Matrix[/bold magenta]",
        border_style="magenta",
        padding=(1, 2)
    )

    # --- 2. Context / Author Info (Right Panel Content) ---
    context_text_content = Text.assemble(
        ("🚀 **The 'Nexus' AI Engine**", f"bold #00FF00"), "\n\n",
        "The **CYBERSENTRY** framework was developed by:\n",
        ("FAHAD KHAN (cybe4sent1nel)", f"bold #00FFFF"),
        " - a **CSE Student** with a passion for **AI, Cybersecurity, and Data Science**.\n\n",

        "This session is powered by the specialized security model:\n",
        ("SENTINEL-X.5", HIGHLIGHT_STYLE),
        " - exclusively tuned for adversarial and defensive tasks.\n\n",

        ("🔗 Connect with Fahad Khan for more updates and exciting stuff:", "bold white"), "\n",
        ("• GitHub: ", "bold white"), ("https://github.com/cybe4sent1nel", LINK_STYLE), " 🐙\n",
        ("• LinkedIn: ", "bold white"), ("https://www.linkedin.com/in/fahad-cybersecurity-ai/", LINK_STYLE), " 🌐\n\n",

        ("SENTINEL-X.5", HIGHLIGHT_STYLE),
        " excels in security-critical domains, including:\n",
        "• Zero-Trust Architecture Analysis\n",
        "• Exploit Development & Patch Gap Identification\n",
        "• Malware Reversing and Sandbox Evasion\n",
        "• Advanced Threat Hunting\n",
    )

    context_panel = Panel(
        Padding(context_text_content, (0, 1)),
        title="[bold #FF1493]✨ SENTINEL-X.5: The Cyber-Specialist AI[/bold #FF1493]",
        border_style="#FF1493",
        padding=(1, 2)
    )

    # --- 3. Footer Content (Playbooks, Config, Hotkeys) ---

    # Playbooks & Security Notice
    playbooks_and_notice = Text.assemble(
        ("🏆 Capture The Flag (CTF) Workflow", CATEGORY_STYLE), "\n",
        ("  1. CYBERSENTRY> /agent select **PhantomPwn**", CMD_STYLE), "\n",
        ("  2. CYBERSENTRY> /session start **TheVault**", CMD_STYLE), "\n",
        ("  3. CYBERSENTRY> **Analyze the challenge file...**", CMD_STYLE), "\n\n",

        ("💰 Zero-Day Hunter (Bug Bounty)", CATEGORY_STYLE), "\n",
        ("  1. CYBERSENTRY> /agent select **VulneraFinder**", CMD_STYLE), "\n",
        ("  2. CYBERSENTRY> /model **gpt-4o-mini**", CMD_STYLE), "\n",
        ("  3. CYBERSENTRY> **Test Target URL: https://acme-corp.net**", CMD_STYLE), "\n\n",

        ("🚨 Data Security Notice:", "bold red"), "\n",
        ("CYBERSENTRY anonymizes telemetry data solely for research and improvement.\n", INFO_STYLE),
        ("Your operational privacy is our priority (GDPR Compliant).\n", INFO_STYLE),
    )

    # Config Variables
    current_model = os.getenv('CYBERSENTRY_MODEL', "cybe4sent1nel0")
    current_agent_type = os.getenv('CYBERSENTRY_AGENT_TYPE', "one_tool_agent")

    config_vars = Text.assemble(
        ("💻 Core Environment Configuration:", "bold cyan"), "\n",
        ("  CYBERSENTRY_MODEL", CMD_STYLE), f" = {current_model}\n",
        ("  CYBERSENTRY_AGENT_TYPE", CMD_STYLE), f" = {current_agent_type}\n",
        ("  CYBERSENTRY_PARALLEL_LIMIT", CMD_STYLE), f" = {os.getenv('CYBERSENTRY_PARALLEL', '4')}\n",
        ("  CYBERSENTRY_LOG_STREAM", CMD_STYLE), f" = {os.getenv('CYBERSENTRY_STREAM', 'true')}\n",
        ("  CYBERSENTRY_SESSION_NAME", CMD_STYLE), f" = {os.getenv('CYBERSENTRY_WORKSPACE', 'default_session')}\n\n",

        ("🌀 Swarm Reconnaissance (Parallel Agents)", CATEGORY_STYLE), "\n",
        ("  1. CYBERSENTRY> /swarm add **NetMapper**", CMD_STYLE), "\n",
        ("  2. CYBERSENTRY> /swarm add **TrafficWhisperer**", CMD_STYLE), "\n",
        ("  3. CYBERSENTRY> **Start distributed scan of 10.0.0.0/8**", CMD_STYLE), "\n\n",
    )

    # Hotkeys / Secrets
    shell_secrets = Text.assemble(
        ("⚡ NEXUS CONSOLE HOTKEYS", CATEGORY_STYLE), "\n",
        ("  ESC + ENTER", CMD_STYLE), " - **Enter/submit multi-line input mode**\n",
        ("  TAB", CMD_STYLE), " - **Automate command and argument completion**\n",
        ("  ↑/↓", CMD_STYLE), " - **Scroll through previous commands**\n",
        ("  Ctrl+C", CMD_STYLE), " - **Send Interrupt Signal (stop current operation/exit)**\n\n",

        ("✨ Shell Secrets:", "bold green"), "\n",
        ("• Type /? for the comprehensive command dictionary\n", DIM_STYLE),
        ("• Type /? setup for this initial quick guide\n", DIM_STYLE),
        ("• Use /history to review and re-run past commands\n", DIM_STYLE),
        ("• Prefix with ! for direct OS command execution: !ping 1.1.1.1\n", DIM_STYLE),

        ("\n[bold yellow]Ready:[/bold yellow] Press Enter to proceed into the Sentinel Shell.", INFO_STYLE)
    )

    # Combine footer sections into columns
    footer_columns = Columns(
        [
            Padding(playbooks_and_notice, (0, 2)),
            Padding(config_vars, (0, 2)),
            Padding(shell_secrets, (0, 2)),
        ],
        expand=True,
        padding=(0, 0)
    )

    footer_panel = Panel(
        footer_columns,
        title="[bold cyan]⚡ Quick Starts & Nexus Environment Configuration[/bold cyan]",
        border_style="cyan",
        padding=(1, 1)
    )

    # --- 4. Final Layout ---

    # Top row combines the Command Matrix and Context/Author Info
    top_row_columns = Columns(
        [help_panel, context_panel],
        expand=True,
        padding=(0, 0) # Panels manage their own padding
    )

    # Final Panel wraps the vertical stack
    final_quick_guide_content = Group(
        top_row_columns,
        footer_panel
    )

    console.print(Panel(
        final_quick_guide_content,
        title="[bold underline #00FFFF]🚀 CYBERSENTRY The Definitive Framework for AI + Security Orchestration - Type /help for detailed documentation[/bold underline #00FFFF]",
        border_style="blue",
        padding=(0, 0),
        title_align="center"
    ), end="")

# --- The rest of the file remains the same ---
