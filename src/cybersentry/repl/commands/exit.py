"""
Exit command for CYBERSENTRY REPL.
This module provides the command to exit the REPL.
"""
import sys
from typing import List, Optional

from cybersentry.repl.commands.base import Command, register_command
from cybersentry.sdk.agents.global_usage_tracker import GLOBAL_USAGE_TRACKER
from cybersentry.util import COST_TRACKER


class ExitCommand(Command):
    """Command for exiting the REPL."""

    def __init__(self):
        """Initialize the exit command."""
        super().__init__(
            name="/exit",
            description="Exit the CYBERSENTRY REPL",
            cybe4sent1neles=["/q", "/quit"]
        )

    def handle(self, args: Optional[List[str]] = None) -> bool:
        """Handle the exit command.

        Args:
            args: Optional list of command arguments

        Returns:
            True if the command was handled successfully, False otherwise
        """
        # End global usage tracking session before exit
        GLOBAL_USAGE_TRACKER.end_session(final_cost=COST_TRACKER.session_total_cost)
        
        sys.exit(0)


# Register the command
register_command(ExitCommand())
