"""Test MCP tool persistence in agents."""

import pytest
from unittest.mock import Mock, AsyncMock, patch

from cybersentry.agents import get_agent_by_name
from cybersentry.repl.commands.mcp import (
    MCPCommand,
    _GLOBAL_MCP_SERVERS,
    _AGENT_MCP_ASSOCIATIONS,
    add_mcp_server_to_agent,
    get_mcp_servers_for_agent,
    get_mcp_tools_for_agent,
)
from cybersentry.sdk.agents import Agent
from cybersentry.sdk.agents.tool import FunctionTool


class TestMCPPersistence:
    """Test MCP tool persistence functionality."""

    def setup_method(self):
        """Set up test environment."""
        # Clear global state
        _GLOBAL_MCP_SERVERS.clear()
        _AGENT_MCP_ASSOCIATIONS.clear()

    def teardown_method(self):
        """Clean up after tests."""
        # Clear global state
        _GLOBAL_MCP_SERVERS.clear()
        _AGENT_MCP_ASSOCIATIONS.clear()

    def test_mcp_assoc.y.b.e.r.s.e.n.t.r.y.n_persistence(self):
        """Test that MCP assoc.y.b.e.r.s.e.n.t.r.y.ns are persisted."""
        agent_name = "test_agent"
        server_name = "test_server"
        
        # Initially no assoc.y.b.e.r.s.e.n.t.r.y.ns
        assert get_mcp_servers_for_agent(agent_name) == []
        
        # Add assoc.y.b.e.r.s.e.n.t.r.y.n
        add_mcp_server_to_agent(agent_name, server_name)
        
        # Check assoc.y.b.e.r.s.e.n.t.r.y.n exists
        assert get_mcp_servers_for_agent(agent_name) == [server_name]
        
        # Add another server
        add_mcp_server_to_agent(agent_name, "another_server")
        assert set(get_mcp_servers_for_agent(agent_name)) == {server_name, "another_server"}
        
        # Duplicate adds should not create duplicates
        add_mcp_server_to_agent(agent_name, server_name)
        servers = get_mcp_servers_for_agent(agent_name)
        assert servers.count(server_name) == 1

    @patch("cybersentry.agents.get_available_agents")
    def test_agent_retrieval_includes_mcp_tools(self, mock_get_available):
        """Test that retrieving an agent includes associated MCP tools."""
        # Create a mock agent
        mock_agent = Mock(spec=Agent)
        mock_agent.name = "test_agent"
        mock_agent.tools = [Mock(name="existing_tool")]
        mock_agent.model = Mock()
        mock_agent.model.__class__.__name__ = "OpenAIChatCompletionsModel"
        mock_agent.model.model = "gpt-4"
        mock_agent.model._client = Mock()
        mock_agent.clone = Mock(return_value=mock_agent)
        
        mock_get_available.return_value = {"test_agent": mock_agent}
        
        # Create a mock MCP server
        mock_tool1 = Mock()
        mock_tool1.name = "mcp_tool1"
        mock_tool1.description = "Tool 1"
        mock_tool1.inputSchema = {}
        
        mock_tool2 = Mock()
        mock_tool2.name = "mcp_tool2"
        mock_tool2.description = "Tool 2"
        mock_tool2.inputSchema = {}
        
        mock_server = Mock()
        mock_server.list_tools = AsyncMock(return_value=[mock_tool1, mock_tool2])
        
        # Add server to global registry
        _GLOBAL_MCP_SERVERS["test_server"] = mock_server
        
        # Add assoc.y.b.e.r.s.e.n.t.r.y.n
        add_mcp_server_to_agent("test_agent", "test_server")
        
        # Get MCP tools for agent
        mcp_tools = get_mcp_tools_for_agent("test_agent")
        
        # Should have 2 MCP tools
        assert len(mcp_tools) == 2
        assert all(isinstance(tool, FunctionTool) for tool in mcp_tools)
        assert {tool.name for tool in mcp_tools} == {"mcp_tool1", "mcp_tool2"}

    def test_mcp_assoc.y.b.e.r.s.e.n.t.r.y.ns_command(self):
        """Test the /mcp assoc.y.b.e.r.s.e.n.t.r.y.ns command."""
        cmd = MCPCommand()
        
        # Initially no assoc.y.b.e.r.s.e.n.t.r.y.ns
        result = cmd.handle_assoc.y.b.e.r.s.e.n.t.r.y.ns()
        assert result is True
        
        # Add some assoc.y.b.e.r.s.e.n.t.r.y.ns
        add_mcp_server_to_agent("agent1", "server1")
        add_mcp_server_to_agent("agent1", "server2")
        add_mcp_server_to_agent("agent2", "server1")
        
        # Mock servers
        mock_server1 = Mock()
        mock_server1.list_tools = AsyncMock(return_value=[Mock(), Mock()])
        mock_server2 = Mock()
        mock_server2.list_tools = AsyncMock(return_value=[Mock()])
        
        _GLOBAL_MCP_SERVERS["server1"] = mock_server1
        _GLOBAL_MCP_SERVERS["server2"] = mock_server2
        
        # Test assoc.y.b.e.r.s.e.n.t.r.y.ns display
        with patch("cybersentry.repl.commands.mcp.console") as mock_console:
            result = cmd.handle_assoc.y.b.e.r.s.e.n.t.r.y.ns()
            assert result is True
            # Should print a table
            mock_console.print.assert_called()

    def test_multiple_agent_instances_share_mcp_tools(self):
        """Test that multiple instances of the same agent share MCP tool assoc.y.b.e.r.s.e.n.t.r.y.ns."""
        agent_name = "test_agent"
        server_name = "test_server"
        
        # Add assoc.y.b.e.r.s.e.n.t.r.y.n
        add_mcp_server_to_agent(agent_name, server_name)
        
        # Create mock server
        mock_tool = Mock()
        mock_tool.name = "shared_tool"
        mock_tool.description = "Shared tool"
        mock_tool.inputSchema = {}
        
        mock_server = Mock()
        mock_server.list_tools = AsyncMock(return_value=[mock_tool])
        _GLOBAL_MCP_SERVERS[server_name] = mock_server
        
        # Get tools for multiple "instances"
        tools1 = get_mcp_tools_for_agent(agent_name)
        tools2 = get_mcp_tools_for_agent(agent_name)
        
        # Both should have the same tools
        assert len(tools1) == 1
        assert len(tools2) == 1
        assert tools1[0].name == tools2[0].name == "shared_tool"