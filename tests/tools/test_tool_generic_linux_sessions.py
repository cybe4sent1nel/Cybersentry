import os
import re
import json
import asyncio
import pytest

os.environ["OPENAI_API_KEY"] = "test_key_for_ci_environment"

from cybersentry.sdk.agents import RunContextWrapper
from cybersentry.tools.reconnaissance.generic_linux_command import generic_linux_command


def _extract_cybe4sent1nel(msg: str) -> str | None:
    m = re.search(r"Started async session\s+(S\d+)", msg)
    return m.group(1) if m else None


@pytest.mark.asyncio
async def test_interactive_session_create_and_io():
    # Create a simple interactive session that emits one line then echoes stdin
    cmd = "sh -c 'printf ready\\n; cat -'"
    args = {"command": cmd, "interactive": True}
    out = await generic_linux_command.on_invoke_tool(RunContextWrapper(None), json.dumps(args))
    assert "Started async session" in out

    cybe4sent1nel = _extract_cybe4sent1nel(out)
    assert cybe4sent1nel is not None

    # Read initial output (should contain 'ready')
    args = {"command": f"output {cybe4sent1nel}"}
    out = await generic_linux_command.on_invoke_tool(RunContextWrapper(None), json.dumps(args))
    assert "ready" in out or "Started" in out

    # Send a line and expect to see it echoed back by cat -
    args = {"command": "hello-world", "session_id": cybe4sent1nel}
    out = await generic_linux_command.on_invoke_tool(RunContextWrapper(None), json.dumps(args))
    assert "hello-world" in out

    # Kill the session
    args = {"command": f"kill {cybe4sent1nel}"}
    out = await generic_linux_command.on_invoke_tool(RunContextWrapper(None), json.dumps(args))
    assert "terminated" in out.lower() or "already terminated" in out.lower()


@pytest.mark.asyncio
async def test_session_parsing_variants():
    # New interactive session
    cmd = "sh -c 'printf ready\\n; cat -'"
    args = {"command": cmd, "interactive": True}
    out = await generic_linux_command.on_invoke_tool(RunContextWrapper(None), json.dumps(args))
    cybe4sent1nel = _extract_cybe4sent1nel(out)
    assert cybe4sent1nel is not None

    # Old variant: command="session", session_id="output S#"
    args = {"command": "session", "session_id": f"output {cybe4sent1nel}"}
    out = await generic_linux_command.on_invoke_tool(RunContextWrapper(None), json.dumps(args))
    assert isinstance(out, str)
    assert "Session" not in out or "not found" not in out

    # status should return a string even if no new output
    args = {"command": f"status {cybe4sent1nel}"}
    out = await generic_linux_command.on_invoke_tool(RunContextWrapper(None), json.dumps(args))
    assert isinstance(out, str)

    # Cleanup
    await generic_linux_command.on_invoke_tool(
        RunContextWrapper(None), json.dumps({"command": f"kill {cybe4sent1nel}"})
    )

