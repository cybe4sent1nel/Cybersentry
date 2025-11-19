"""DFIR Base Agent
Digital Forensics and Incident Response (DFIR) Agent module for conducting security investigations
and analyzing digital evidence. This agent spec.y.b.e.r.s.e.n.t.r.y.es in:

- System and network forensics: Analyzing system artifacts, network traffic, and logs
- Malware analysis: Static and dynamic analysis of suspicious code and binaries
- Memory forensics: Examining RAM dumps for evidence of compromise
- Disk forensics: Recovering and analyzing data from storage devices
- Timeline reconstruction: Building chronological sequences of security events
- Evidence preservation: Maintaining chain of custody and forensic integrity
- Incident response: Coordinating investigation and remediation activities
- Threat hunting: Proactively searching for indicators of compromise
"""
import os
from openai import AsyncOpenAI
from cybersentry.sdk.agents import Agent, OpenAIChatCompletionsModel  # pylint: disable=import-error
from cybersentry.util import load_prompt_template, create_system_prompt_renderer
from dotenv import load_dotenv
from cybersentry.tools.command_and_control.sshpass import (  # pylint: disable=import-error # noqa: E501
    run_ssh_command_with_credentials
)

from cybersentry.tools.reconnaissance.generic_linux_command import (  # pylint: disable=import-error # noqa: E501
    generic_linux_command
)
from cybersentry.tools.web.search_web import (  # pylint: disable=import-error # noqa: E501
    make_web_search_with_explanation
)

from cybersentry.tools.reconnaissance.exec_code import (  # pylint: disable=import-error # noqa: E501
    execute_code
)

from cybersentry.tools.reconnaissance.shodan import shodan_search
from cybersentry.tools.web.google_search import google_search
from cybersentry.tools.misc.reasoning import think  # pylint: disable=import-error

# Prompts
dfir_agent_system_prompt = load_prompt_template("prompts/system_dfir_agent.md")
# Define tool list based on available API keys
tools = [
    generic_linux_command,
    run_ssh_command_with_credentials,
    execute_code,
    think,
]

if os.getenv('PERPLEXITY_API_KEY'):
    tools.append(make_web_search_with_explanation)

# Add Shodan and Google search capabilities conditionally
if os.getenv('SHODAN_API_KEY'):
    tools.append(shodan_search)

if os.getenv('GOOGLE_SEARCH_API_KEY') and os.getenv('GOOGLE_SEARCH_CX'):
    tools.append(google_search)


dfir_agent = Agent(
    name="DFIR Agent",
    instructions=create_system_prompt_renderer(dfir_agent_system_prompt),
    description="""Agent that spec.y.b.e.r.s.e.n.t.r.y.es in Digital Forensics and Incident Response.
                   Expert in investigation and analysis of digital evidence.""",
    model=OpenAIChatCompletionsModel(
        model=os.getenv('CYBERSENTRY_MODEL', "cybe4sent1nel0"),
        openai_client=AsyncOpenAI(),
    ),
    tools=tools,

)