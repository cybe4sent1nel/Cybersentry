"""Reverse Engineering and Binary Analysis Agent"""
import os
from dotenv import load_dotenv
from cybersentry.sdk.agents import Agent, OpenAIChatCompletionsModel  # pylint: disable=import-error
from openai import AsyncOpenAI
from cybersentry.util import load_prompt_template  # Add this import
from cybersentry.tools.command_and_control.sshpass import (  # pylint: disable=import-error # noqa: E501
    run_ssh_command_with_credentials
)

from cybersentry.tools.reconnaissance.generic_linux_command import (  # pylint: disable=import-error # noqa: E501
    generic_linux_command
)
from cybersentry.tools.web.search_web import (  # pylint: disable=import-error # noqa: E501
    make_web_search_with_explanation,
)

from cybersentry.tools.reconnaissance.exec_code import (  # pylint: disable=import-error # noqa: E501
    execute_code
)

load_dotenv()
# Prompts
reverse_engineering_agent_system_prompt = load_prompt_template("prompts/reverse_engineering_agent.md")

# Define functions list
functions = [
    generic_linux_command,
    run_ssh_command_with_credentials,
    execute_code,
]

# Add make_web_search_with_explanation function if PERPLEXITY_API_KEY environment variable is set
if os.getenv('PERPLEXITY_API_KEY'):
    functions.append(make_web_search_with_explanation)
    
# Create the agent
reverse_engineering_agent = Agent(
    name="Reverse Engineering Spec.y.b.e.r.s.e.n.t.r.y.t",
    instructions=reverse_engineering_agent_system_prompt,
    description="""Agent for binary analysis and reverse engineering.
                   Spec.y.b.e.r.s.e.n.t.r.y.es in firmware analysis, binary disassembly,
                   decompilation, and vulnerability discovery using tools
                   like Ghidra, Binwalk, and various binary analysis utilities.""",
    tools=functions,
    model=OpenAIChatCompletionsModel(
        model=os.getenv('CYBERSENTRY_MODEL', "cybe4sent1nel0"),
        openai_client=AsyncOpenAI(),
    )
)
