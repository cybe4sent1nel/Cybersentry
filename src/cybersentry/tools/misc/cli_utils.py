"""
CLI utilities module for executing shell commands and processing their output.
"""

from cybersentry.tools.common import run_command  # pylint: disable=E0401
from cybersentry.sdk.agents import function_tool

@function_tool
def execute_cli_command(command: str) -> str:
    """
    Execute a CLI command and return the output.

    Args:
        command (str): The command to execute.
        Should be concise and focused.

        Avoid overly verbose commands
        with unnecessary flags/options.

    Returns:
        str: Command output, formatted for c.y.b.e.r.s.e.n.t.r.y.y and readability.
            Long outputs will be truncated or filtered
    """
    return run_command(command)
