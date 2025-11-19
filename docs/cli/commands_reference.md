# Cybersentry CLI Commands Reference

This comprehensive guide documents all commands available in the Cybersentry Command Line Interface, organized by category for easy navigation.

---

## Command Categories

1. [Agent Management](#agent-management)
2. [Model Management](#model-management)
3. [Memory & History](#memory--history)
4. [Environment & Configuration](#environment--configuration)
5. [Tools & Integration](#tools--integration)
6. [System Management](#system-management)
7. [Parallel Execution](#parallel-execution)
8. [Utilities](#utilities)

---

## Agent Management

### `/agent` or `/a`

Manage and switch between different AI agents.

**Syntax**:
```bash
/agent [subcommand] [arguments]
/a [subcommand] [arguments]
```

**Subcommands**:

#### `list`
List all available agents with their descriptions.

```bash
/agent list
```

**Output**: Table showing agent names, descriptions, and primary use cases.

#### `<agent_name>`
Switch to a specific agent.

```bash
/agent redteam_agent
/agent bug_bounter_agent
/a blueteam_agent
```

#### `info` or `info <agent_name>`
Display detailed information about the current or specified agent.

```bash
# Current agent info
/agent info

# Specific agent info
/agent info redteam_agent
```

**Examples**:

```bash
# List all agents
Cybersentry> /agent list

# Switch to red team agent
Cybersentry> /agent redteam_agent

# Switch to bug bounty agent (using alias)
Cybersentry> /a bug_bounter_agent

# Get info about DFIR agent
Cybersentry> /agent info dfir_agent
```

**Available Agents**:

| Agent | Use Case |
|-------|----------|
| `redteam_agent` | Offensive security testing |
| `blueteam_agent` | Defensive security analysis |
| `bug_bounter_agent` | Bug bounty hunting |
| `one_tool_agent` | Single-tool execution |
| `dfir_agent` | Digital forensics |
| `reverse_engineering_agent` | Binary analysis |
| `network_security_analyzer_agent` | Network security |
| `wifi_security_agent` | WiFi security testing |
| `android_sast_agent` | Android security analysis |
| `selection_agent` | Agent recommendation |

**Notes**:
- Agent changes are immediate
- Conversation history is preserved when switching
- Each agent has specialized tools and instructions

---

## Model Management

### `/model` or `/mod`

View or change the current LLM model.

**Syntax**:
```bash
/model [model_name]
/mod [model_name]
```

**Examples**:

```bash
# View current model
Cybersentry> /model

# Change to alias1
Cybersentry> /model alias1

# Change to GPT-4o
Cybersentry> /model gpt-4o

# Change to Claude
Cybersentry> /model claude-3-5-sonnet-20241022
```

### `/model-show`

Display all available models from the LiteLLM repository.

**Syntax**:
```bash
/model-show
```

**Output**: Comprehensive list of models by provider (OpenAI, Anthropic, Ollama, etc.)

**Examples**:

```bash
# Show all available models
Cybersentry> /model-show

# Then select one
Cybersentry> /model gpt-4o
```

**Commonly Used Models**:

| Model | Provider | Cost | Best For |
|-------|----------|------|----------|
| `alias1` | Alias Robotics | Medium | Balanced performance ⭐ |
| `gpt-4o` | OpenAI | High | Complex reasoning |
| `claude-3-5-sonnet-20241022` | Anthropic | High | Fast & accurate |
| `o1-mini` | OpenAI | Medium | Reasoning tasks |

---

## Memory & History

### `/history` or `/his`

Display conversation history.

**Syntax**:
```bash
/history [number] [agent_name]
/his [number]
```

**Parameters**:
- `number`: Number of recent messages to show (default: 10)
- `agent_name`: Filter by specific agent

**Examples**:

```bash
# Show last 10 messages
Cybersentry> /history

# Show last 20 messages
Cybersentry> /history 20

# Show last 5 messages
Cybersentry> /his 5

# Show history for specific agent
Cybersentry> /history 10 redteam_agent
```

**Output**: Formatted conversation with timestamps, roles (user/agent), and message content.

---

### `/memory` or `/mem`

Manage persistent memory storage across sessions.

**Syntax**:
```bash
/memory <subcommand> [arguments]
/mem <subcommand> [arguments]
```

**Subcommands**:

#### `list`
Show all saved memories.

```bash
/memory list
```

#### `save [name]`
Save current conversation as a memory.

```bash
/memory save "web app pentest findings"
/mem save ctf_techniques
```

#### `apply <memory_id>`
Apply a saved memory to the current session.

```bash
/memory apply mem_12345
```

#### `show <memory_id>`
Display the content of a specific memory.

```bash
/memory show mem_12345
```

#### `delete <memory_id>`
Remove a memory permanently.

```bash
/memory delete mem_12345
```

#### `merge <id1> <id2> [name]`
Combine two memories into one.

```bash
/memory merge mem_12345 mem_67890 "combined_findings"
```

#### `compact`
AI-powered memory summarization.

```bash
/memory compact
```

#### `status`
Show memory system status and statistics.

```bash
/memory status
```

**Examples**:

```bash
# Save current session insights
Cybersentry> /memory save "SQLi vulnerabilities found"

# List all memories
Cybersentry> /memory list

# Apply previous knowledge
Cybersentry> /memory apply mem_12345

# Check memory status
Cybersentry> /mem status
```

**Notes**:
- Memories persist across sessions
- Stored in `.cai/memory/` directory
- Useful for long-term research projects

---

### `/compact` or `/cmp`

Compact the current conversation to reduce context size.

**Syntax**:
```bash
/compact [model_name]
/cmp
```

**Parameters**:
- `model_name`: Optional model to use for compaction

**Examples**:

```bash
# Compact with current model
Cybersentry> /compact

# Compact with specific model
Cybersentry> /compact alias1
```

**Use Cases**:
- Approaching token limits
- Long conversations that need summarization
- Maintaining conversation flow with reduced tokens

---

### `/flush` or `/clear`

Clear conversation history.

**Syntax**:
```bash
/flush [agent_name|all]
/clear
```

**Parameters**:
- `agent_name`: Flush specific agent history
- `all`: Flush all agent histories

**Examples**:

```bash
# Flush current agent
Cybersentry> /flush

# Flush specific agent
Cybersentry> /flush redteam_agent

# Flush all agents
Cybersentry> /flush all
```

**Warning**: This action is irreversible. Consider using `/save` first.

---

### `/load` or `/l`

Load conversation history from a file.

**Syntax**:
```bash
/load <filename>
/l <filename>
```

**Supported Formats**:
- JSON (`.json`)
- JSONL (`.jsonl`)
- Markdown (`.md`)

**Examples**:

```bash
# Load JSON session
Cybersentry> /load pentest_session.json

# Load JSONL data
Cybersentry> /load conversation.jsonl

# Using alias
Cybersentry> /l ~/sessions/previous_work.json
```

**Notes**:
- Restores conversation context
- Compatible with `/save` output
- Can load partial histories

---

### `/merge` or `/mrg`

Merge agent message histories (shortcut for `/parallel merge`).

**Syntax**:
```bash
/merge [agent1] [agent2]
/mrg
```

**Examples**:

```bash
# Merge all parallel agents
Cybersentry> /merge

# Merge specific agents
Cybersentry> /merge redteam_agent blueteam_agent
```

**Use Cases**:
- Combining parallel execution results
- Integrating different agent perspectives

---

## Environment & Configuration

### `/config` or `/cfg`

Display and configure environment variables.

**Syntax**:
```bash
/config [VARIABLE=value]
/config set <number> <value>
/cfg
```

**Examples**:

```bash
# View all configuration
Cybersentry> /config

# Set by variable name
Cybersentry> /config Cybersentry_PRICE_LIMIT=10.0
Cybersentry> /config Cybersentry_MAX_TURNS=50

# Set by number (from /config output)
Cybersentry> /config set 18 "5.0"
```

**Common Configuration Variables**:

| Variable | Description | Default |
|----------|-------------|---------|
| `Cybersentry_MODEL` | Default model | `alias1` |
| `Cybersentry_AGENT_TYPE` | Default agent | `redteam_agent` |
| `Cybersentry_DEBUG` | Debug level (0-2) | `1` |
| `Cybersentry_PRICE_LIMIT` | Cost limit (USD) | `1.0` |
| `Cybersentry_MAX_TURNS` | Max conversation turns | `inf` |
| `Cybersentry_MAX_INTERACTIONS` | Max tool calls | `inf` |
| `Cybersentry_TRACING` | Enable tracing | `true` |
| `Cybersentry_GUARDRAILS` | Security guardrails | `false` |

**Notes**:
- Changes take effect immediately
- Use `/config` without arguments to see all options
- Numbers in first column can be used with `set` subcommand

---

### `/env` or `/e`

Display current environment variables.

**Syntax**:
```bash
/env [pattern]
/e
```

**Parameters**:
- `pattern`: Optional filter pattern (e.g., "Cybersentry", "CTF")

**Examples**:

```bash
# Show all environment variables
Cybersentry> /env

# Filter Cybersentry-specific variables
Cybersentry> /env Cybersentry

# Filter CTF variables
Cybersentry> /env CTF
```

---

### `/workspace` or `/ws`

Manage workspace directories.

**Syntax**:
```bash
/workspace <subcommand> [path]
/ws <subcommand>
```

**Subcommands**:

#### `show` or `pwd`
Display current workspace directory.

```bash
/workspace show
/ws pwd
```

#### `set <path>`
Change workspace directory.

```bash
/workspace set /path/to/project
/ws set ~/ctf_challenges
```

#### `list` or `ls`
List workspace contents.

```bash
/workspace list
/ws ls
```

**Examples**:

```bash
# Show current workspace
Cybersentry> /workspace show

# Change workspace
Cybersentry> /workspace set /home/user/pentests

# List files
Cybersentry> /ws ls
```

**Notes**:
- Affects where shell commands execute
- Useful for CTF challenges and projects
- Works with Docker containers

---

### `/virtualization` or `/virt`

Manage Docker-based virtualization environments.

**Syntax**:
```bash
/virtualization <subcommand> [arguments]
/virt <subcommand>
```

**Subcommands**:

#### `list`
List available containers.

```bash
/virtualization list
```

#### `set <container_id>`
Set active container for command execution.

```bash
/virtualization set abc123def456
/virt set mycontainer
```

#### `clear`
Return to host environment.

```bash
/virtualization clear
```

#### `info`
Show current virtualization status.

```bash
/virtualization info
```

**Examples**:

```bash
# List containers
Cybersentry> /virtualization list

# Execute commands in container
Cybersentry> /virt set ubuntu_ctf

# Return to host
Cybersentry> /virt clear
```

**Notes**:
- Automatically set when CTF challenges start
- Commands execute inside specified container
- Uses `Cybersentry_ACTIVE_CONTAINER` environment variable

---

## Tools & Integration

### `/mcp` or `/m`

Manage Model Context Protocol (MCP) servers and their tools.

**Syntax**:
```bash
/mcp <subcommand> [arguments]
/m <subcommand>
```

**Subcommands**:

#### `load <url> <name>`
Load an SSE MCP server.

```bash
/mcp load http://localhost:9876/sse burp
```

#### `load stdio <command> <name>`
Load a STDIO MCP server.

```bash
/mcp load stdio "npx -y @modelcontextprotocol/server-brave-search" brave
```

#### `list`
List active MCP connections.

```bash
/mcp list
```

#### `add <agent_name> <server_name>`
Add MCP tools to an agent.

```bash
/mcp add redteam_agent burp
```

#### `remove <server_name>`
Remove an MCP server connection.

```bash
/mcp remove burp
```

#### `tools <server_name>`
List tools from an MCP server.

```bash
/mcp tools burp
```

#### `status`
Check MCP server connection status.

```bash
/mcp status
```

#### `associations`
Show agent-MCP associations.

```bash
/mcp associations
```

**Examples**:

```bash
# Load Burp Suite MCP server
Cybersentry> /mcp load http://localhost:9876/sse burp

# List MCP tools
Cybersentry> /mcp tools burp

# Add to current agent
Cybersentry> /mcp add redteam_agent burp

# Check status
Cybersentry> /mcp status
```

**Common MCP Servers**:
- **Burp Suite**: Web application testing tools
- **Brave Search**: Web search capabilities
- **Filesystem**: File operations
- **Git**: Repository management
- **Postgres**: Database operations

**Notes**:
- Extends agent capabilities dynamically
- Supports both SSE and STDIO protocols
- See [MCP Documentation](../cai/getting-started/MCP.md) for details

---

### `/shell` or `/s` or `/$`

Execute shell commands directly from the CLI.

**Syntax**:
```bash
/shell <command>
/s <command>
$ <command>
```

**Examples**:

```bash
# Using /shell
Cybersentry> /shell nmap -sV 192.168.1.1

# Using /s alias
Cybersentry> /s whoami

# Using $ shortcut
Cybersentry> $ ls -la

# Complex commands
Cybersentry> $ nmap -sV -p- 192.168.1.0/24 -oN scan_results.txt
```

**Notes**:
- Commands execute in current workspace
- Respects `Cybersentry_ACTIVE_CONTAINER` if set
- Output displayed in real-time
- `Ctrl+C` to interrupt running commands

---

## System Management

### `/kill` or `/k`

Terminate active processes or stuck sessions.

**Syntax**:
```bash
/kill
/k
```

**Examples**:

```bash
# Kill current process
Cybersentry> /kill

# Alternative: Ctrl+C
```

**Use Cases**:
- Stopping stuck tool executions
- Canceling long-running operations
- Interrupting agent loops

---

### `/exit` or `/quit` or `/q`

Exit the Cybersentry CLI.

**Syntax**:
```bash
/exit
/quit
/q
```

**Examples**:

```bash
# Exit Cybersentry
Cybersentry> /exit

# Alternative: Ctrl+D
```

**Notes**:
- Performs clean shutdown
- Saves session logs
- Stops background processes

---

### `/quickstart`

Display setup information and quick start guide.

**Syntax**:
```bash
/quickstart
```

**Examples**:

```bash
# Show quickstart guide
Cybersentry> /quickstart
```

**Notes**:
- Auto-displays on first launch
- Useful for new users
- Shows essential commands and setup

---

## Parallel Execution

### `/parallel` or `/par` or `/p`

Manage parallel agent configurations and execution.

**Syntax**:
```bash
/parallel <subcommand> [arguments]
/par <subcommand>
/p <subcommand>
```

**Subcommands**:

#### `add <agent_name> [model]`
Add an agent to parallel configuration.

```bash
/parallel add redteam_agent alias1
/par add bug_bounter_agent gpt-4o
```

#### `remove <agent_id>`
Remove an agent from parallel configuration.

```bash
/parallel remove P1
```

#### `list`
List all parallel agents.

```bash
/parallel list
```

#### `clear`
Clear all parallel configurations.

```bash
/parallel clear
```

#### `run <prompt>`
Execute a prompt across all parallel agents.

```bash
/parallel run "scan 192.168.1.1 for vulnerabilities"
```

#### `merge`
Merge all parallel agent histories.

```bash
/parallel merge
```

**Examples**:

```bash
# Configure parallel agents
Cybersentry> /parallel add redteam_agent alias1
Cybersentry> /parallel add blueteam_agent alias1
Cybersentry> /parallel add bug_bounter_agent gpt-4o

# List configuration
Cybersentry> /parallel list

# Execute on all agents
Cybersentry> /parallel run "analyze target.com"

# Merge results
Cybersentry> /parallel merge

# Clear configuration
Cybersentry> /parallel clear
```

**YAML Configuration**:

Create `agents.yaml`:

```yaml
agents:
  - name: red1
    agent_type: redteam_agent
    model: alias1
  - name: bug1
    agent_type: bug_bounter_agent
    model: alias1
```

Launch with YAML:

```bash
cai --yaml agents.yaml --prompt "scan target.com"
```

**Notes**:
- Each agent runs independently
- Results can be merged
- Different models per agent supported
- See [Advanced Usage](advanced_usage.md) for more details

---

### `/run` or `/r`

Execute queued prompts (works with parallel mode).

**Syntax**:
```bash
/run <prompt>
/r <prompt>
```

**Examples**:

```bash
# Queue and run prompt
Cybersentry> /run "analyze this binary"

# Alternative
Cybersentry> /r "test for XSS"
```

**Notes**:
- Executes immediately if agents are ready
- Queues if agents are busy
- Works with both single and parallel modes

---

**Queue File Format** (`prompts.txt`):

```text
# Comments start with #
/agent redteam_agent
Scan 192.168.1.0/24 for open ports
Test https://target.com for vulnerabilities
$ nmap -sV 192.168.1.1
Generate security report
```

**Notes**:
- Prompts execute sequentially
- Supports commands and regular prompts
- Can load from files for automation

---

## Utilities

### `/help` or `/h` or `/?`

Display help information and command documentation.

**Syntax**:
```bash
/help [command]
/h [command]
/? [command]
```

**Examples**:

```bash
# General help
Cybersentry> /help

# Help for specific command
Cybersentry> /help agent
Cybersentry> /h parallel
Cybersentry> /? mcp
```

**Topics**:
- `agent`: Agent management
- `parallel`: Parallel execution
- `memory`: Memory management
- `config`: Configuration
- `mcp`: MCP integration
- `commands`: List all commands

---

### `/graph` or `/g`

Visualize agent interaction graphs.

**Syntax**:
```bash
/graph [agent_name]
/g
```

**Examples**:

```bash
# Show graph for current conversation
Cybersentry> /graph

# Show graph for specific agent
Cybersentry> /graph redteam_agent
```

**Output**:
- Directed graph of conversations
- User and agent interactions
- Tool calls highlighted
- Conversation flow visualization

---

### `/context` or `/ctx` 🚀 **Cybersentry PRO Exclusive**

> **⚡ Cybersentry PRO Exclusive Feature**  
> The `/context` command is available exclusively in **Cybersentry PRO**. To access this feature and unlock advanced monitoring capabilities, visit [Alias Robotics](https://cybe4sent1nel(FAHAD KHAN).com/cybersecurityai.php) for more information.

View context usage and token statistics for the current conversation.

**Syntax**:
```bash
/context [agent_name]
/ctx
```

**Examples**:

```bash
# Show context for current agent
Cybersentry> /context

# Show context for specific agent
Cybersentry> /ctx redteam_agent
```

**Output Includes**:
- Total context usage (used/max tokens) with percentage
- Visual grid representation with Cybersentry logo
- Breakdown by category:
  - System prompt tokens
  - Tool definitions tokens
  - Memory/RAG tokens
  - User prompts tokens
  - Assistant responses tokens
  - Tool calls tokens
  - Tool results tokens
- Free space available
- Color-coded visualization

**Notes**:
- Helps monitor token limits
- Useful for long conversations
- Different models have different context windows

---

### `/cost`

Display API usage costs and token statistics.

**Syntax**:
```bash
/cost [agent_name]
```

**Examples**:

```bash
# Show costs for current session
Cybersentry> /cost

# Show costs for specific agent
Cybersentry> /cost redteam_agent

# Show all agents' costs
Cybersentry> /cost all
```

**Output Includes**:
- Total cost (USD)
- Input tokens used
- Output tokens used
- Cost per interaction
- Model pricing rates
- Agent breakdown

---

### `/save`

Save current conversation to a file.

**Syntax**:
```bash
/save <filename>
```

**Supported Formats**:
- JSON (`.json`)
- Markdown (`.md`)

**Examples**:

```bash
# Save as JSON
Cybersentry> /save pentest_session.json

# Save as Markdown
Cybersentry> /save findings_report.md

# Full path
Cybersentry> /save ~/sessions/project_alpha.json
```

**Notes**:
- Saves all conversation history
- Includes agent names and timestamps
- Cost information preserved
- Can be loaded with `/load`

---

### `/temperature` or `/temp`

Adjust the model's temperature parameter.

**Syntax**:
```bash
/temperature <value>
/temp <value>
```

**Parameters**:
- `value`: Temperature (0.0 - 2.0)
  - Lower = more deterministic
  - Higher = more creative

**Examples**:

```bash
# Set to more deterministic
Cybersentry> /temperature 0.2

# Set to more creative
Cybersentry> /temp 1.5

# View current temperature
Cybersentry> /temperature
```

---

### `/api`

Manage API keys and authentication.

**Syntax**:
```bash
/api <subcommand> [arguments]
```

**Subcommands**:
- `show`: Display configured API keys (masked)

**Examples**:

```bash
# Show API keys
Cybersentry> /api show

---

## Special Features

### Command Chaining

Chain multiple commands using semicolons (`;`).

**Syntax**:
```bash
command1 ; command2 ; command3
```

**Examples**:

```bash
# Chain commands at launch
cai --prompt "/agent redteam_agent ; scan 192.168.1.1 ; /save results.json"

# Chain in CLI
Cybersentry> /agent bug_bounter_agent ; test https://target.com ; /cost
```

**Use Cases**:
- Automation workflows
- Batch operations
- Quick sequences

---

### Auto-loading Queue from File

Load and execute prompts automatically on startup.

**Environment Variable**:
```bash
export Cybersentry_QUEUE_FILE="/path/to/prompts.txt"
```

**Launch**:
```bash
Cybersentry_QUEUE_FILE=~/my_prompts.txt cai
```

**Notes**:
- Prompts execute automatically
- Returns to interactive mode when done
- Perfect for automation

---

## Quick Reference

### Most Used Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/agent <name>` | Switch agent | `/agent redteam_agent` |
| `/model <name>` | Change model | `/model alias1` |
| `/config` | View config | `/config` |
| `/help` | Get help | `/help agent` |
| `/save <file>` | Save session | `/save session.json` |
| `/load <file>` | Load session | `/load session.json` |
| `/cost` | Show costs | `/cost` |
| `/history` | View history | `/history 20` |
| `$ <cmd>` | Shell command | `$ nmap -sV target` |
| `/exit` | Exit Cybersentry | `/exit` |

### Command Aliases

| Full Command | Aliases |
|--------------|---------|
| `/agent` | `/a` |
| `/model` | `/mod` |
| `/config` | `/cfg` |
| `/help` | `/h`, `/?` |
| `/history` | `/his` |
| `/memory` | `/mem` |
| `/workspace` | `/ws` |
| `/virtualization` | `/virt` |
| `/parallel` | `/par`, `/p` |
| `/shell` | `/s`, `/$` |
| `/context` | `/ctx` |
| `/compact` | `/cmp` |
| `/temperature` | `/temp` |
| `/load` | `/l` |
| `/merge` | `/mrg` |
| `/run` | `/r` |
| `/kill` | `/k` |
| `/exit` | `/quit`, `/q` |

---

## Next Steps

- 📖 [Getting Started Guide](getting_started.md) - Learn the basics
- 🚀 [Advanced Usage](advanced_usage.md) - Automation and advanced features
- 🏠 [CLI Overview](cli_index.md) - Return to main CLI documentation

---

*Last updated: November 2025 | Cybersentry CLI v0.6+*

