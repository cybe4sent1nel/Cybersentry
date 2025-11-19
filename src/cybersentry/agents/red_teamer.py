"""Red Team Base Agent"""
import os
from dotenv import load_dotenv
from cybersentry.sdk.agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
# from cybersentry.tools.command_and_control.sshpass import (  # pylint: disable=import-error # noqa: E501
#     run_ssh_command_with_credentials
# )

from cybersentry.tools.reconnaissance.generic_linux_command import (  # pylint: disable=import-error # noqa: E501
    generic_linux_command
)
from cybersentry.tools.web.search_web import (  # pylint: disable=import-error # noqa: E501
    make_web_search_with_explanation,
)

from cybersentry.tools.reconnaissance.exec_code import (  # pylint: disable=import-error # noqa: E501
    execute_code
)
from cybersentry.util import load_prompt_template, create_system_prompt_renderer
from cybersentry.agents.guardrails import get_security_guardrails

load_dotenv()
model_name = os.getenv("CYBERSENTRY_MODEL", "cybe4sent1nel0")
# Prompts
redteam_agent_system_prompt = load_prompt_template("prompts/system_red_team_agent.md")
# Define tools list based on available API keys
tools = [
    generic_linux_command,
    #run_ssh_command_with_credentials,
    execute_code,
]

# Add make_web_search_with_explanation function if PERPLEXITY_API_KEY environment variable is set
if os.getenv('PERPLEXITY_API_KEY'):
    tools.append(make_web_search_with_explanation)

# Get security guardrails
input_guardrails, output_guardrails = get_security_guardrails()

redteam_agent = Agent(
    name="Red Team Agent",
    description="""Agent that mimics a red teamer in a security assessment.
                   Expert in cybersecurity, recon, and exploitation.""",
    instructions=create_system_prompt_renderer(redteam_agent_system_prompt),
    tools=tools,
    input_guardrails=input_guardrails,
    output_guardrails=output_guardrails,
    model=OpenAIChatCompletionsModel(
        model=model_name,
        openai_client=AsyncOpenAI(),
    ),
)

# Transfer function
def transfer_to_redteam_agent(**kwargs):  # pylint: disable=W0613
    """Transfer to red team agent.
    Accepts any keyword arguments but ignores them."""
    return redteam_agent