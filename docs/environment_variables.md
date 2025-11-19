# Environment Variables Reference

This comprehensive guide documents all environment variables available in Cybersentry, including their purposes, default values, and usage examples.

---

## 📋 Complete Reference Table

| Variable | Description | Default |
|----------|-------------|---------|
| CTF_NAME | Name of the CTF challenge to run (e.g. "picoctf_static_flag") | - |
| CTF_CHALLENGE | Specific challenge name within the CTF to test | - |
| CTF_SUBNET | Network subnet for the CTF container | 192.168.3.0/24 |
| CTF_IP | IP address for the CTF container | 192.168.3.100 |
| CTF_INSIDE | Whether to conquer the CTF from within container | true |
| Cybersentry_MODEL | Model to use for agents | alias1 |
| Cybersentry_DEBUG | Set debug output level (0: Only tool outputs, 1: Verbose debug output, 2: CLI debug output) | 1 |
| Cybersentry_BRIEF | Enable/disable brief output mode | false |
| Cybersentry_MAX_TURNS | Maximum number of turns for agent interactions | inf |
| Cybersentry_MAX_INTERACTIONS | Maximum number of interactions (tool calls, agent actions, etc.) allowed in a session. If exceeded, only CLI commands are allowed until increased. If force_until_flag=true, the session will exit | inf |
| Cybersentry_PRICE_LIMIT | Price limit for the conversation in dollars. If exceeded, only CLI commands are allowed until increased. If force_until_flag=true, the session will exit | 1 |
| Cybersentry_TRACING | Enable/disable OpenTelemetry tracing. When enabled, traces execution flow and agent interactions for debugging and analysis | true |
| Cybersentry_AGENT_TYPE | Specify the agents to use (e.g., boot2root, one_tool, redteam_agent). Use "/agent" command in CLI to list all available agents | redteam_agent |
| Cybersentry_STATE | Enable/disable stateful mode. When enabled, the agent will use a state agent to keep track of the state of the network and the flags found | false |
| Cybersentry_MEMORY | Enable/disable memory mode (episodic: use episodic memory, semantic: use semantic memory, all: use both episodic and semantic memory) | false |
| Cybersentry_MEMORY_ONLINE | Enable/disable online memory mode | false |
| Cybersentry_MEMORY_OFFLINE | Enable/disable offline memory | false |
| Cybersentry_ENV_CONTEXT | Add environment context, dirs and current env available | true |
| Cybersentry_MEMORY_ONLINE_INTERVAL | Number of turns between online memory updates | 5 |
| Cybersentry_SUPPORT_MODEL | Model to use for the support agent | o3-mini |
| Cybersentry_SUPPORT_INTERVAL | Number of turns between support agent executions | 5 |
| Cybersentry_STREAM | Enable/disable streaming output in rich panel | false |
| Cybersentry_TELEMETRY | Enable/disable telemetry | true |
| Cybersentry_PARALLEL | Number of parallel agent instances to run. When set to values greater than 1, executes multiple instances of the same agent in parallel and displays all results | 1 |
| Cybersentry_GUARDRAILS | Enable/disable security guardrails for agents. When set to "true", applies security guardrails to prevent potentially dangerous outputs and inputs | false |
| Cybersentry_GCTR_NITERATIONS | Number of tool interactions before triggering GCTR (Generative Cut-The-Rope) analysis in bug_bounter_gctr agent. Only applies when using gctr-enabled agents | 5 |
| Cybersentry_ACTIVE_CONTAINER | Docker container ID where commands should be executed. When set, shell commands and tools execute inside the specified container instead of the host. Automatically set when CTF challenges start (if CTF_INSIDE=true) or when switching containers via /virtualization command | - |

---

## 🎯 Quick Reference by Use Case

### 🚀 Getting Started (Essential)

For first-time users, these are the essential variables to configure:

```bash
# Required: Model selection
Cybersentry_MODEL="alias1"                    # or gpt-4o, claude-sonnet-4.5, ollama/qwen2.5:72b

# Recommended: Agent type
Cybersentry_AGENT_TYPE="redteam_agent"        # See available agents with /agent command

# Optional but useful: Cost control
Cybersentry_PRICE_LIMIT="1"                   # Maximum spend in dollars
```

**Related Documentation:**
- [Installation Guide](cai/getting-started/installation.md)
- [Configuration Guide](cai/getting-started/configuration.md)

---

### 🏴 CTF Challenges

For running Capture The Flag challenges in containerized environments:

```bash
# Challenge selection
CTF_NAME="picoctf_static_flag"        # Name of the CTF challenge
CTF_CHALLENGE="web_exploitation_1"    # Specific sub-challenge

# Network configuration
CTF_SUBNET="192.168.3.0/24"          # Container subnet
CTF_IP="192.168.3.100"               # Container IP address

# Execution mode
CTF_INSIDE="true"                     # Run agent inside container
```

**Best Practices:**
- Set `CTF_INSIDE=true` to run the agent inside the challenge container
- Use `Cybersentry_ACTIVE_CONTAINER` to manually specify which container to execute commands in
- Combine with `Cybersentry_STATE=true` to track discovered flags

**Related Documentation:**
- [CTF Benchmarks](benchmarking/jeopardy_ctfs.md)

---

### 🧠 Memory & State Management

For maintaining context across sessions and learning from past interactions:

```bash
# State tracking
Cybersentry_STATE="true"                      # Enable network state tracking

# Memory modes
Cybersentry_MEMORY="all"                      # Options: episodic, semantic, all, false
Cybersentry_MEMORY_ONLINE="true"              # Enable online memory
Cybersentry_MEMORY_OFFLINE="true"             # Enable offline memory

# Memory tuning
Cybersentry_MEMORY_ONLINE_INTERVAL="5"       # Turns between memory updates
```

**Memory Modes Explained:**
- `episodic`: Remember specific past events and interactions
- `semantic`: Extract and store general knowledge
- `all`: Combine both episodic and semantic memory

**Related Documentation:**
- [Advanced Features](tui/advanced_features.md)

---

### 🛡️ Security & Safety

For enabling security guardrails and controlling agent behavior:

```bash
# Security guardrails
Cybersentry_GUARDRAILS="true"                 # Prevent dangerous commands
Cybersentry_PRICE_LIMIT="1"                   # Maximum cost in dollars
Cybersentry_MAX_INTERACTIONS="inf"            # Maximum allowed interactions

# Debugging & monitoring
Cybersentry_DEBUG="1"                         # 0: minimal, 1: verbose, 2: CLI debug
Cybersentry_TRACING="true"                    # Enable OpenTelemetry tracing
```

**Security Layers:**
- **Guardrails**: Prompt injection detection and command validation
- **Cost Limits**: Prevent runaway API usage
- **Interaction Limits**: Control agent autonomy

**Related Documentation:**
- [Guardrails Documentation](guardrails.md)
- [TUI Advanced Features](tui/advanced_features.md)

---

### ⚡ Performance Optimization

For optimizing output, execution speed, and resource usage:

```bash
# Output control
Cybersentry_BRIEF="true"                      # Concise output mode
Cybersentry_STREAM="false"                    # Disable streaming for faster processing

# Context optimization
Cybersentry_ENV_CONTEXT="true"                # Include environment in context
Cybersentry_MAX_TURNS="50"                    # Limit conversation turns

# Telemetry
Cybersentry_TELEMETRY="true"                  # Enable usage analytics
```

**Performance Tips:**
- Enable `Cybersentry_BRIEF` for concise outputs in automated workflows
- Set `Cybersentry_MAX_TURNS` to prevent infinite loops
- Use `Cybersentry_STREAM=false` when output display is not needed

---

### 🔧 Advanced Agent Configuration

For specialized agents and complex workflows:

```bash
# Support agent (meta-reasoning)
Cybersentry_SUPPORT_MODEL="o3-mini"          # Model for support agent
Cybersentry_SUPPORT_INTERVAL="5"             # Turns between support executions

# Parallel execution
Cybersentry_PARALLEL="3"                      # Run 3 agent instances simultaneously

# Specialized agents
Cybersentry_GCTR_NITERATIONS="5"             # For bug_bounty_gctr agent
```

**Specialized Agent Variables:**
- `Cybersentry_GCTR_NITERATIONS`: Controls Cut-The-Rope analysis frequency in GCTR agents
- `Cybersentry_SUPPORT_MODEL`: Meta-agent for strategic planning
- `Cybersentry_PARALLEL`: Swarm-style parallel agent execution

**Related Documentation:**
- [Agents Documentation](agents.md)
- [Teams & Parallel Execution](tui/teams_and_parallel_execution.md)

---

### 🐳 Container & Virtualization

For executing commands inside Docker containers:

```bash
# Container targeting
Cybersentry_ACTIVE_CONTAINER="a1b2c3d4e5f6"  # Docker container ID

# Automatic with CTF
CTF_INSIDE="true"                     # Auto-set Cybersentry_ACTIVE_CONTAINER on CTF start
```

**Container Execution:**
- When `Cybersentry_ACTIVE_CONTAINER` is set, all shell commands execute inside that container
- Automatically configured when starting CTF challenges with `CTF_INSIDE=true`
- Switch containers using `/virtualization` command in CLI

**Related Documentation:**
- [Commands Reference](cai/getting-started/commands.md)

---

### 🖥️ TUI-Specific Configuration

For Terminal User Interface features and workflows:

```bash
# TUI display
Cybersentry_STREAM="true"                     # Enable streaming in TUI panels
Cybersentry_BRIEF="false"                     # Full output for interactive sessions

# TUI workflows
Cybersentry_PARALLEL="1"                      # Usually 1 for TUI, use Teams feature instead
Cybersentry_GUARDRAILS="false"                # Consider enabling for team workflows
```

**TUI Recommendations:**
- Set `Cybersentry_STREAM=true` for better interactive experience
- Use built-in Teams feature instead of `Cybersentry_PARALLEL`
- Enable `Cybersentry_GUARDRAILS` when coordinating multiple agents

**Related Documentation:**
- [TUI Documentation](tui/tui_index.md)
- [TUI Getting Started](tui/getting_started.md)

---

## 💡 Common Configuration Examples

### Example 1: Local Development with Ollama

```bash
Cybersentry_MODEL="ollama/qwen2.5:72b"
Cybersentry_AGENT_TYPE="redteam_agent"
Cybersentry_PRICE_LIMIT="0"
Cybersentry_DEBUG="1"
Cybersentry_GUARDRAILS="false"
```

### Example 2: Production CTF Solving

```bash
CTF_NAME="hackthebox_challenge"
CTF_INSIDE="true"
Cybersentry_MODEL="alias1"
Cybersentry_STATE="true"
Cybersentry_MEMORY="all"
Cybersentry_GUARDRAILS="true"
Cybersentry_PRICE_LIMIT="5"
```

### Example 3: Pentesting with Cost Control

```bash
Cybersentry_MODEL="gpt-4o"
Cybersentry_AGENT_TYPE="redteam_agent"
Cybersentry_PRICE_LIMIT="2"
Cybersentry_MAX_INTERACTIONS="100"
Cybersentry_GUARDRAILS="true"
Cybersentry_BRIEF="false"
```

### Example 4: Parallel Testing (Non-TUI)

```bash
Cybersentry_MODEL="Neural x SEC-fast"
Cybersentry_PARALLEL="5"
Cybersentry_BRIEF="true"
Cybersentry_MAX_TURNS="20"
Cybersentry_STREAM="false"
```

---

## 📚 Related Documentation

- [Configuration Guide](cai/getting-started/configuration.md) - Basic setup and API keys
- [Commands Reference](cai/getting-started/commands.md) - Available CLI commands
- [TUI Documentation](tui/tui_index.md) - Terminal User Interface features
- [Agents Documentation](agents.md) - Available agent types
- [Guardrails](guardrails.md) - Security and safety features

---

## ⚠️ Important Notes

### API Keys

Cybersentry does NOT provide API keys for any model by default. Configure your own keys in the `.env` file:

```bash
OPENAI_API_KEY="sk-..."              # Required (can use "sk-123" as placeholder)
ANTHROPIC_API_KEY="sk-ant-..."       # For Claude models
ALIAS_API_KEY="sk-..."               # For alias1 (Cybersentry PRO)
OLLAMA_API_BASE="http://localhost:11434/v1"  # For local models
```

See the [Configuration Guide](cai/getting-started/configuration.md) for more details.

### Setting Variables

There are three ways to configure environment variables:

**1. `.env` file (Recommended)**
```bash
# Add to .env file
Cybersentry_MODEL="alias1"
Cybersentry_PRICE_LIMIT="1"
```

**2. Command-line**
```bash
Cybersentry_MODEL="gpt-4o" Cybersentry_PRICE_LIMIT="2" cai
```

**3. Runtime configuration**
Use CLI commands to modify settings during execution. See [Commands Reference](cai/getting-started/commands.md).

