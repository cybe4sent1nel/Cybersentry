"""
This module defines agents for Android Static Application Security Testing (SAST).

It includes:
- `app_logic_mapper_agent`: An agent for analyzing application logic.
- `android_sast_agent`: An agent for static analysis and vulnerability discovery in Android applications.
"""

from cybersentry.sdk.agents import Agent, OpenAIChatCompletionsModel
from cybersentry.tools.reconnaissance.generic_linux_command import generic_linux_command
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

from cybersentry.util import load_prompt_template, create_system_prompt_renderer
from cybersentry.tools.reconnaissance.exec_code import (
    execute_code
)


# Prompts
android_sast_system_prompt = load_prompt_template("prompts/system_android_sast.md")
app_logic_mapper_system_prompt = load_prompt_template("prompts/system_android_app_logic_mapper.md")



# Define tools list based on available API keys
tools = [
    generic_linux_command,
    execute_code,
]


load_dotenv()
model_name = os.getenv("CYBERSENTRY_MODEL", "cybe4sent1nel0")

app_logic_mapper = Agent(
    name="AppLogicMapper",
    description="Agent spec.y.b.e.r.s.e.n.t.r.y.ing in application analysis to understand the logic of operation and return a complete map of it.",
    instructions=create_system_prompt_renderer(app_logic_mapper_system_prompt),
    tools=tools,
    model=OpenAIChatCompletionsModel(
        model=model_name,
        openai_client=AsyncOpenAI(),
    ),
)



android_sast = Agent(
    name="AndroidSAST",
    description="Agent spec.y.b.e.r.s.e.n.t.r.y.ing in static application security testing and vulnerability discovery for Android applications",
    instructions=create_system_prompt_renderer(android_sast_system_prompt),
    tools=[
        app_logic_mapper.as_tool(
            tool_name="app_mapper",
            tool_description="application analysis to understand the logic of operation and return a complete map of it."
        ),
        generic_linux_command,
        execute_code,
        ],
    model=OpenAIChatCompletionsModel(
        model=model_name,
        openai_client=AsyncOpenAI(),
    ),
)

