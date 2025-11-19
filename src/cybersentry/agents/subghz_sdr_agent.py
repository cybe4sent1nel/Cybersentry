"""Sub-GHz Radio Frequency Analysis Agent using HackRF One"""
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
subghz_agent_system_prompt = load_prompt_template("prompts/subghz_agent.md")

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
subghz_sdr_agent = Agent(
    name="Sub-GHz SDR Spec.y.b.e.r.s.e.n.t.r.y.t",
    instructions=subghz_agent_system_prompt,
    description="""Agent for sub-GHz radio frequency analysis using HackRF One.
                   Spec.y.b.e.r.s.e.n.t.r.y.es in signal capture, replay, and protocol analysis for IoT, 
                   automotive, industrial, and wireless security applications.""",
    tools=functions,
    model=OpenAIChatCompletionsModel(
        model=os.getenv('CYBERSENTRY_MODEL', "cybe4sent1nel0"),
        openai_client=AsyncOpenAI(),
    )
)
