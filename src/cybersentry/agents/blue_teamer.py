"""Blue Team Base Agent
SSH_PASS
SSH_HOST
SSH_USER
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

# Prompts
blueteam_agent_system_prompt = load_prompt_template("prompts/system_blue_team_agent.md")
# Define tools list based on available API keys
tools = [
    generic_linux_command,
    run_ssh_command_with_credentials,
    execute_code,
]

load_dotenv()
# Add search_web tools if PERPLEXITY_API_KEY environment variable is set
if os.getenv('PERPLEXITY_API_KEY'):
    tools.append(make_web_search_with_explanation)

blueteam_agent = Agent(
    name="Blue Team Agent",
    instructions=create_system_prompt_renderer(blueteam_agent_system_prompt),
    description="""Agent that spec.y.b.e.r.s.e.n.t.r.y.es in system defense and security monitoring.
                   Expert in cybersecurity protection and incident response.""",
    model=OpenAIChatCompletionsModel(
        model=os.getenv('CYBERSENTRY_MODEL', "cybe4sent1nel0"),
        openai_client=AsyncOpenAI(),
    ),
    tools=tools,
)
