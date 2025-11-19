# Getting Started with Cybersentry CLI

This guide will walk you through launching the Cybersentry CLI for the first time and performing your first security assessment using the command-line interface.

## Prerequisites

Before starting, ensure you have:

- ✅ Cybersentry installed (see [Installation Guide](../cai_installation.md))
- ✅ Python 3.9+ installed
- ✅ A valid `ALIAS_API_KEY` from [Alias Robotics](https://cybe4sent1nel(FAHAD KHAN).com)

## Step 1: Launch the CLI

Open your terminal and run:

```bash
cai
```

You should see the Cybersentry banner and prompt:

```
          CCCCCCCCCCCCC      ++++++++   ++++++++      IIIIIIIIII
       CCC::::::::::::C  ++++++++++       ++++++++++  I::::::::I
     CC:::::::::::::::C ++++++++++         ++++++++++ I::::::::I
    C:::::CCCCCCCC::::C +++++++++    ++     +++++++++ II::::::II
   C:::::C       CCCCCC +++++++     +++++     +++++++   I::::I
  C:::::C                +++++     +++++++     +++++    I::::I
  C:::::C                ++++                   ++++    I::::I
  C:::::C                 ++                     ++     I::::I
  C:::::C                  +   +++++++++++++++   +      I::::I
  C:::::C                    +++++++++++++++++++        I::::I
  C:::::C                     +++++++++++++++++         I::::I
   C:::::C       CCCCCC        +++++++++++++++          I::::I
    C:::::CCCCCCCC::::C         +++++++++++++         II::::::II
     CC:::::::::::::::C           +++++++++           I::::::::I
       CCC::::::::::::C             +++++             I::::::::I
          CCCCCCCCCCCCC               ++              IIIIIIIIII

                      Cybersecurity AI (Cybersentry), v0.6.0
                          Bug bounty-ready AI

Cybersentry>
```

The navigation bar at the bottom displays important system information including your current model, agent, cost tracking, and session details.

## Step 2: Configure Your API Key

If your `ALIAS_API_KEY` is not configured, you'll see an authentication error. Configure it using one of these methods:

### Method 1: Using a `.env` file (Recommended)

Create a `.env` file in your working directory:

```env
ALIAS_API_KEY=ak_live_1234567890abcdef
Cybersentry_MODEL=alias1
Cybersentry_AGENT_TYPE=redteam_agent
Cybersentry_DEBUG=1
Cybersentry_PRICE_LIMIT=10.0
```

### Method 2: Environment Variables

Set it directly in your terminal:

```bash
export ALIAS_API_KEY="ak_live_1234567890abcdef"
cai
```

### Method 3: Runtime Configuration

After launching Cybersentry, use the `/config` command:

```bash
Cybersentry> /config Cybersentry_MODEL=alias1
```

To view all current configuration:

```bash
Cybersentry> /config
```

## Step 3: Select Your Model

Cybersentry supports multiple AI models. For optimal performance and cost balance, we recommend `alias1`:

```bash
Cybersentry> /model alias1
```

To see all available models:

```bash
Cybersentry> /model-show
```

### Recommended Models

| Model | Provider | Best For | Cost |
|-------|----------|----------|------|
| `alias1` | Alias Robotics | **Recommended** - Balanced performance | Medium |
| `gpt-4o` | OpenAI | Complex reasoning and multi-modal | High |
| `claude-3-5-sonnet-20241022` | Anthropic | Fast responses with good quality | High |
| `o1-mini` | OpenAI | Reasoning tasks | Medium |

> **💡 Tip**: You can change models at any time without losing your conversation history.

## Step 4: Choose Your Agent

Cybersentry provides specialized agents for different security tasks. Here's how to choose:

### Option 1: List All Available Agents

```bash
Cybersentry> /agent list
```

This displays all agents with their descriptions and primary use cases.

### Option 2: Use the Selection Agent

If you're unsure which agent to use, start with the `selection_agent`:

```bash
Cybersentry> /agent selection_agent
Cybersentry> I need to test a web application for SQL injection
```

The agent will recommend the best agent for your task.

### Option 3: Choose Directly

If you know which agent you need:

```bash
Cybersentry> /agent redteam_agent
```

### Common Agents and When to Use Them

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| `redteam_agent` | Offensive security testing | Default for penetration testing |
| `bug_bounter_agent` | Bug bounty hunting | Finding high-value vulnerabilities in web apps |
| `blueteam_agent` | Defensive security analysis | Security posture assessment and hardening |
| `one_tool_agent` | Single-tool execution | Quick scans with specific tools |
| `dfir_agent` | Digital forensics and incident response | Log analysis and forensic investigation |
| `reverse_engineering_agent` | Binary analysis | Malware analysis, firmware reversing |
| `network_security_analyzer_agent` | Network security assessment | Network scanning and traffic analysis |
| `wifi_security_agent` | WiFi security testing | Wireless penetration testing |
| `selection_agent` | Agent recommendation | **When unsure which agent to use** |

> **💡 Pro Tip**: Start with `selection_agent` if you're new to Cybersentry—it will guide you to the right agent for your task.

## Step 5: Start Your First Interaction

Now you're ready to interact with Cybersentry! Simply type your prompt and press **Enter**.

### Example 1: Basic Network Reconnaissance

```bash
Cybersentry> Scan 192.168.1.1 for open ports and services
```

The agent will:
- Process your request
- Select and execute appropriate tools (e.g., nmap)
- Display results in real-time
- Provide analysis and recommendations

### Example 2: Web Application Testing

```bash
Cybersentry> /agent bug_bounter_agent
Cybersentry> Test https://example.com for common web vulnerabilities
```

The agent will:
- Perform reconnaissance
- Test for OWASP Top 10 vulnerabilities
- Execute security tools
- Provide detailed findings

### Example 3: CTF Challenge

```bash
# Set up CTF environment
Cybersentry> /config CTF_NAME=hackableii
Cybersentry> /config CTF_CHALLENGE=web_challenge

# Start the challenge
Cybersentry> Analyze this CTF challenge and find the flag
```

### Understanding the Output

As the agent works, you'll see:

1. **Tool Execution**: Messages showing which tools are being launched
2. **Tool Output**: Real-time results from executed commands
3. **Agent Reasoning**: The agent's thought process (if `Cybersentry_DEBUG=1`)
4. **Final Analysis**: Summary, findings, and recommendations
5. **Cost Tracking**: Updated costs in the navigation bar

## Step 6: Essential Commands

Here are the most important commands to know:

### Getting Help

```bash
# General help
Cybersentry> /help

# Help for specific command
Cybersentry> /help agent

# Quick reference guide
Cybersentry> /quickstart
```

### Agent Management

```bash
# List all agents
Cybersentry> /agent list

# Switch to a specific agent
Cybersentry> /agent redteam_agent

# Get info about current agent
Cybersentry> /agent info
```

### Model Management

```bash
# View current model
Cybersentry> /model

# Change model
Cybersentry> /model gpt-4o

# List all available models
Cybersentry> /model-show
```

### Session Management

```bash
# Save current conversation
Cybersentry> /save pentest_session.json

# Save as Markdown report
Cybersentry> /save findings_report.md

# Load previous conversation
Cybersentry> /load pentest_session.json
```

### View History and Costs

```bash
# View conversation history
Cybersentry> /history

# View last 20 messages
Cybersentry> /history 20

# Check costs and token usage
Cybersentry> /cost
```

### Clear and Reset

```bash
# Clear terminal output (keeps history)
Cybersentry> Ctrl+L

# Flush conversation history
Cybersentry> /flush

# Exit Cybersentry
Cybersentry> /exit
# or press Ctrl+D
```

## Step 7: Shell Command Execution

Cybersentry allows you to execute shell commands directly:

### Using /shell Command

```bash
Cybersentry> /shell nmap -sV 192.168.1.1
```

### Using $ Shortcut

```bash
Cybersentry> $ whoami
Cybersentry> $ ls -la
Cybersentry> $ nmap -sV localhost
```

### Interactive Tools

For interactive tools, the agent will handle them appropriately:

```bash
Cybersentry> Run a comprehensive port scan on 192.168.1.0/24
# Agent will execute nmap with appropriate flags
```

## Step 8: Working with Configuration

### View Current Configuration

```bash
Cybersentry> /config
```

This displays a panel with all environment variables and their current values.

### Change Configuration at Runtime

```bash
# Set a specific variable (use the number from /config output)
Cybersentry> /config set 18 "5.0"

# Or set by name
Cybersentry> /config Cybersentry_PRICE_LIMIT=5.0
Cybersentry> /config Cybersentry_MAX_TURNS=50
```

### Important Configuration Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `Cybersentry_MODEL` | Default model to use | `alias1` |
| `Cybersentry_AGENT_TYPE` | Default agent | `redteam_agent` |
| `Cybersentry_DEBUG` | Debug level (0-2) | `1` |
| `Cybersentry_PRICE_LIMIT` | Maximum cost in USD | `10.0` |
| `Cybersentry_MAX_TURNS` | Maximum conversation turns | `50` |
| `Cybersentry_MAX_INTERACTIONS` | Maximum tool interactions | `100` |
| `Cybersentry_TRACING` | Enable OpenTelemetry tracing | `true` |
| `Cybersentry_GUARDRAILS` | Enable security guardrails | `true` |

See the complete [Configuration Guide](../cai/getting-started/configuration.md) for all options.

## Step 9: Common Workflows

### Workflow 1: Quick Security Scan

```bash
# Launch with specific agent
Cybersentry_AGENT_TYPE=redteam_agent cai

# Execute scan
Cybersentry> Perform a quick security assessment of 192.168.1.100

# Save results
Cybersentry> /save quick_scan_results.md
```

### Workflow 2: Bug Bounty Reconnaissance

```bash
# Start with bug bounty agent
Cybersentry> /agent bug_bounter_agent

# Reconnaissance
Cybersentry> Perform full reconnaissance on target.com

# Test specific vulnerability
Cybersentry> Test the login form for SQL injection

# Generate report
Cybersentry> Generate a detailed bug bounty report

# Save session
Cybersentry> /save bugbounty_target_session.json
```

### Workflow 3: CTF Challenge

```bash
# Configure CTF environment
export CTF_NAME="hackableii"
export CTF_CHALLENGE="web_app"
export Cybersentry_AGENT_TYPE="redteam_agent"

# Launch and solve
cai

Cybersentry> Analyze this CTF challenge and find the flag
```

### Workflow 4: Network Analysis

```bash
Cybersentry> /agent network_security_analyzer_agent

# Analyze network
Cybersentry> Scan the network 192.168.1.0/24 for security issues

# Analyze captured traffic
Cybersentry> Analyze this PCAP file for suspicious activity

# View findings
Cybersentry> /history
```

## Step 10: Keyboard Shortcuts

Master these shortcuts for faster navigation:

| Shortcut | Action |
|----------|--------|
| `Tab` | Autocomplete commands and arguments |
| `↑` / `↓` | Navigate through command history |
| `Ctrl+C` | Interrupt current execution |
| `Ctrl+L` | Clear terminal screen |
| `Ctrl+Z` | Suspend process (resume with `fg`) |
| `Ctrl+U` | Clear current input line |
| `Ctrl+A` | Move cursor to start of line |
| `Ctrl+E` | Move cursor to end of line |

## Common First-Time Issues

### Issue: API Key Not Valid

**Solution**: 
```bash
# Check your API key is set correctly
Cybersentry> /env | grep ALIAS_API_KEY

# If not set, add it to .env file
echo "ALIAS_API_KEY=your_key_here" >> .env
```

### Issue: Agent Not Responding

**Solution**:
```bash
# Cancel current operation
Ctrl+C

# Check agent is loaded
Cybersentry> /agent

# Switch to a different agent
Cybersentry> /agent redteam_agent
```

### Issue: Command Not Found

**Solution**:
```bash
# Get help for available commands
Cybersentry> /help

# Use Tab completion to see available commands
Cybersentry> /<Tab>

# Check command syntax
Cybersentry> /help <command_name>
```

### Issue: Price Limit Reached

**Solution**:
```bash
# Check current costs
Cybersentry> /cost

# Increase limit
Cybersentry> /config Cybersentry_PRICE_LIMIT=20.0

# Or set it before launching
Cybersentry_PRICE_LIMIT=20.0 cai
```

### Issue: Max Turns Exceeded

**Solution**:
```bash
# Increase turn limit
Cybersentry> /config Cybersentry_MAX_TURNS=100

# Or flush history and start fresh
Cybersentry> /flush
```

## Next Steps

Congratulations! You've completed the basics of Cybersentry CLI. Here's what to explore next:

### Learn More Commands
- 📚 [Commands Reference](commands_reference.md) - Complete command documentation
- 🚀 [Advanced Usage](advanced_usage.md) - Automation, scripting, and advanced features

### Explore Advanced Features
- **Queue System**: Batch process multiple prompts
- **Parallel Execution**: Run multiple agents simultaneously
- **Memory Management**: Persistent context across sessions
- **MCP Integration**: Connect external tools and services

### Specialized Workflows
- **CTF Challenges**: Learn CTF-specific workflows
- **Bug Bounty**: Master bug bounty hunting techniques
- **Automation**: Script security assessments
- **CI/CD Integration**: Integrate Cybersentry into your pipeline

### Get Help
- ❓ [FAQ](../cai_faq.md) - Common questions
- 💬 [Discord](https://discord.gg/cybe4sent1nel(FAHAD KHAN)) - Community support
- 🐛 [GitHub Issues](https://github.com/cybe4sent1nel(FAHAD KHAN)/cai/issues) - Report bugs

## Quick Reference Card

### Most Used Commands

```bash
/agent list              # List all agents
/agent <name>            # Switch agent
/model <name>            # Change model
/config                  # View configuration
/help                    # Get help
/save <file>             # Save session
/load <file>             # Load session
/cost                    # Show costs
/history                 # View history
/shell <cmd>             # Run shell command
$ <cmd>                  # Shell shortcut
/exit                    # Exit Cybersentry
```

### Essential Workflows

```bash
# Quick scan
cai --prompt "scan target.com for vulnerabilities"

# CTF mode
CTF_NAME="challenge" cai

# Bug bounty
Cybersentry_AGENT_TYPE=bug_bounter_agent cai

# With initial setup
Cybersentry_MODEL=alias1 Cybersentry_PRICE_LIMIT=10 cai
```

---

*Last updated: November 2025 | Cybersentry CLI v0.6+*

