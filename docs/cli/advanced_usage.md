# Advanced Usage

This guide covers advanced features, automation, scripting, and power-user techniques for the Cybersentry Command Line Interface.

---

## Table of Contents

1. [Parallel Execution](#parallel-execution)
2. [Queue System](#queue-system)
3. [Automation & Scripting](#automation--scripting)
4. [Memory Management](#memory-management)
5. [Workspace & Virtualization](#workspace--virtualization)
6. [CTF Workflows](#ctf-workflows)
7. [Cost Management](#cost-management)
8. [Configuration Management](#configuration-management)
9. [Integration Patterns](#integration-patterns)
10. [Troubleshooting](#troubleshooting)

---

## Parallel Execution

Run multiple agents simultaneously to get different perspectives or distribute workload.

### Basic Parallel Setup

#### Method 1: Using Commands

```bash
# Launch Cybersentry
cai

# Add agents to parallel configuration
Cybersentry> /parallel add redteam_agent alias1
Cybersentry> /parallel add blueteam_agent alias1
Cybersentry> /parallel add bug_bounter_agent gpt-4o

# List configured agents
Cybersentry> /parallel list

# Execute on all agents
Cybersentry> /parallel run "analyze the security of target.com"

# Merge results
Cybersentry> /parallel merge
```

#### Method 2: Using YAML Configuration

Create `agents.yaml`:

```yaml
metadata:
  description: "Multi-perspective security analysis"
  auto_run: true

agents:
  - name: offensive
    agent_type: redteam_agent
    model: alias1
    
  - name: defensive
    agent_type: blueteam_agent
    model: alias1
    
  - name: bug_hunter
    agent_type: bug_bounter_agent
    model: gpt-4o
    
  - name: forensics
    agent_type: dfir_agent
    model: alias1
```

Launch with YAML:

```bash
cai --yaml agents.yaml --prompt "perform comprehensive security assessment of target.com"
```

#### Method 3: Using Environment Variable

```bash
# Set parallel count
export Cybersentry_PARALLEL=3
export Cybersentry_AGENT_TYPE=redteam_agent
export Cybersentry_MODEL=alias1

cai --prompt "scan network 192.168.1.0/24"
```

### Advanced Parallel Patterns

#### Pattern 1: Distributed Reconnaissance

Split reconnaissance across multiple agents:

```yaml
# recon_team.yaml
agents:
  - name: subdomain_enum
    agent_type: redteam_agent
    model: alias1
    initial_prompt: "Enumerate subdomains for A-M range"
    
  - name: subdomain_enum2
    agent_type: redteam_agent
    model: alias1
    initial_prompt: "Enumerate subdomains for N-Z range"
    
  - name: port_scanner
    agent_type: network_security_analyzer_agent
    model: alias1
    initial_prompt: "Scan all discovered hosts"
    
  - name: web_analyzer
    agent_type: bug_bounter_agent
    model: alias1
    initial_prompt: "Analyze all web services found"
```

```bash
cai --yaml recon_team.yaml
```

#### Pattern 2: Red vs Blue Analysis

Compare offensive and defensive perspectives:

```bash
# Configure teams
Cybersentry> /parallel add redteam_agent alias1
Cybersentry> /parallel add blueteam_agent alias1

# Execute same analysis from different perspectives
Cybersentry> /parallel run "analyze the security posture of this web application"

# Compare results
Cybersentry> /parallel merge
```

#### Pattern 3: Multi-Model Comparison

Test different models on the same task:

```yaml
# model_comparison.yaml
agents:
  - name: alias_test
    agent_type: bug_bounter_agent
    model: alias1
    
  - name: gpt4o_test
    agent_type: bug_bounter_agent
    model: gpt-4o
    
  - name: claude_test
    agent_type: bug_bounter_agent
    model: claude-3-5-sonnet-20241022
```

### Managing Parallel Results

```bash
# View individual agent outputs
Cybersentry> /history 10 offensive
Cybersentry> /history 10 defensive

# Merge all conversations
Cybersentry> /parallel merge

# Save merged results
Cybersentry> /save parallel_assessment_results.json

# Clear parallel configuration
Cybersentry> /parallel clear
```

---

## Queue System

Batch process multiple prompts for automated workflows.

### Creating Queue Files

Create `security_checklist.txt`:

```text
# Security Assessment Checklist
# Comments start with # and are ignored

# Phase 1: Reconnaissance
/agent redteam_agent
Perform passive reconnaissance on target.com
Enumerate subdomains and services

# Phase 2: Vulnerability Scanning
/agent bug_bounter_agent
Test for OWASP Top 10 vulnerabilities
Check for known CVEs in discovered services

# Phase 3: Network Analysis
/agent network_security_analyzer_agent
$ nmap -sV -p- target.com
Analyze the network topology

# Phase 4: Report Generation
/agent reporting_agent
Generate comprehensive security report
/save security_assessment_report.md

# Phase 5: Cleanup
/cost
/history 50
```

### Loading and Executing Queues

#### Method 1: Auto-load on Startup

```bash
# Set environment variable
export Cybersentry_QUEUE_FILE="security_checklist.txt"
cai

# Queue executes automatically
```

#### Method 2: Command Line Queue

```bash
# Use semicolons to chain commands
cai --prompt "/agent redteam_agent ; scan target.com ; /save results.json"
```

### Advanced Queue Patterns

#### Pattern 1: CTF Challenge Queue

```text
# ctf_workflow.txt
/config CTF_NAME=hackableii
/config CTF_CHALLENGE=web_app
/agent redteam_agent
Analyze the CTF challenge environment
Find and exploit vulnerabilities
Extract the flag
/save ctf_solution.md
```

#### Pattern 2: Bug Bounty Workflow

```text
# bugbounty_recon.txt
/agent bug_bounter_agent
/config Cybersentry_PRICE_LIMIT=20.0

# Reconnaissance
Perform subdomain enumeration on target.com
Identify web technologies and frameworks
Map the attack surface

# Testing
Test authentication mechanisms for bypasses
Check for injection vulnerabilities
Analyze API endpoints for security issues

# Reporting
Compile findings into bug bounty report
/save bugbounty_findings.md
/cost
```

#### Pattern 3: Continuous Security Monitoring

```text
# daily_security_check.txt
/agent network_security_analyzer_agent

# Daily checks
$ nmap -sV 192.168.1.0/24
Analyze changes from previous scan
Identify new services or hosts
Report anomalies

/save daily_scan_$(date +%Y%m%d).json
```

---

## Automation & Scripting

Integrate Cybersentry into scripts and CI/CD pipelines.

### Bash Script Integration

#### Script 1: Automated Security Scan

```bash
#!/bin/bash
# security_scan.sh

TARGET="$1"
OUTPUT_DIR="./scan_results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Configuration
export Cybersentry_MODEL=alias1
export Cybersentry_AGENT_TYPE=redteam_agent
export Cybersentry_PRICE_LIMIT=10.0
export Cybersentry_MAX_TURNS=50
export Cybersentry_TRACING=false
export Cybersentry_DEBUG=0

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Run Cybersentry with automated prompt
cai --prompt "
/agent redteam_agent
Perform comprehensive security scan on $TARGET
Test for common vulnerabilities
/save $OUTPUT_DIR/scan_${TIMESTAMP}.json
/cost
/exit
"

echo "Scan completed. Results saved to $OUTPUT_DIR/scan_${TIMESTAMP}.json"
```

Usage:

```bash
chmod +x security_scan.sh
./security_scan.sh target.com
```

#### Script 2: Multi-Target Batch Scan

```bash
#!/bin/bash
# batch_scan.sh

TARGETS_FILE="$1"
OUTPUT_DIR="./batch_results"

mkdir -p "$OUTPUT_DIR"

while IFS= read -r target; do
    echo "Scanning $target..."
    
    Cybersentry_PRICE_LIMIT=5.0 cai --prompt "
    /agent bug_bounter_agent
    Scan $target for web vulnerabilities
    /save $OUTPUT_DIR/${target//\//_}_scan.json
    /exit
    "
    
    echo "Completed: $target"
    sleep 2
done < "$TARGETS_FILE"

echo "All scans completed!"
```

Usage:

```bash
# targets.txt contains one domain per line
./batch_scan.sh targets.txt
```

#### Script 3: CTF Automation

```bash
#!/bin/bash
# ctf_solver.sh

CTF_NAME="$1"
CHALLENGE="$2"

export CTF_NAME="$CTF_NAME"
export CTF_CHALLENGE="$CHALLENGE"
export CTF_INSIDE=true
export Cybersentry_AGENT_TYPE=redteam_agent
export Cybersentry_MODEL=alias1
export Cybersentry_MAX_TURNS=100

# Create queue file
cat > /tmp/ctf_queue.txt << 'EOF'
Analyze the CTF challenge
Identify vulnerabilities
Exploit and find the flag
/save ctf_solution.json
/exit
EOF

# Run with queue
Cybersentry_QUEUE_FILE=/tmp/ctf_queue.txt cai

# Cleanup
rm /tmp/ctf_queue.txt
```

Usage:

```bash
./ctf_solver.sh hackableii web_challenge
```

### CI/CD Integration

#### GitHub Actions Example

```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  security-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install Cybersentry
      run: |
        pip install cai
        
    - name: Run Security Scan
      env:
        ALIAS_API_KEY: ${{ secrets.ALIAS_API_KEY }}
        Cybersentry_MODEL: alias1
        Cybersentry_PRICE_LIMIT: 10.0
        Cybersentry_TRACING: false
      run: |
        cai --prompt "
        /agent bug_bounter_agent
        Analyze this repository for security issues
        Focus on OWASP Top 10 vulnerabilities
        /save security_report.json
        /exit
        "
        
    - name: Upload Results
      uses: actions/upload-artifact@v3
      with:
        name: security-report
        path: security_report.json
```

#### GitLab CI Example

```yaml
# .gitlab-ci.yml
security_scan:
  stage: test
  image: python:3.11
  
  before_script:
    - pip install cai
    
  script:
    - |
      cai --prompt "
      /agent redteam_agent
      Scan $CI_PROJECT_URL for vulnerabilities
      /save scan_results.json
      /exit
      "
      
  artifacts:
    paths:
      - scan_results.json
    expire_in: 1 week
    
  only:
    - main
    - merge_requests
```

### Non-Interactive Mode

```bash
# Single command execution
cai --prompt "scan 192.168.1.1" > output.txt

# Suppress interactive elements
Cybersentry_DEBUG=0 Cybersentry_BRIEF=true cai --prompt "quick scan"

# Pipe output
cai --prompt "analyze" | grep -i "vulnerability"

# JSON output for parsing
cai --prompt "scan target ; /save results.json ; /exit"
```

---

## Memory Management

Advanced persistent memory for long-term context.

### Episodic Memory

Store and recall specific episodes or sessions.

```bash
# Enable episodic memory
export Cybersentry_MEMORY=episodic
cai

# During session
Cybersentry> /memory save "SQLi vulnerability found in login"
Cybersentry> /memory save "XSS in comment section"

# List memories
Cybersentry> /memory list

# Apply memory to new session
Cybersentry> /memory apply mem_12345
```

### Semantic Memory

Store knowledge and facts.

```bash
# Enable semantic memory
export Cybersentry_MEMORY=semantic
cai

# Save semantic knowledge
Cybersentry> /memory save "Target uses Apache 2.4.41 with ModSecurity"
```

### Combined Memory

Use both episodic and semantic memory:

```bash
# Enable all memory types
export Cybersentry_MEMORY=all
export Cybersentry_MEMORY_ONLINE=true
export Cybersentry_MEMORY_ONLINE_INTERVAL=5

cai
```

### Online Memory Mode

Automatically save memory at intervals:

```bash
# Configure online memory
export Cybersentry_MEMORY=episodic
export Cybersentry_MEMORY_ONLINE=true
export Cybersentry_MEMORY_ONLINE_INTERVAL=3  # Save every 3 turns

cai --prompt "long reconnaissance session"
```

### Memory Workflows

#### Workflow 1: Multi-Day Assessment

**Day 1:**
```bash
Cybersentry> /agent bug_bounter_agent
Cybersentry> Perform reconnaissance on target.com
Cybersentry> /memory save "day1_reconnaissance"
Cybersentry> /save day1_session.json
```

**Day 2:**
```bash
Cybersentry> /agent bug_bounter_agent
Cybersentry> /memory apply day1_reconnaissance
Cybersentry> Continue testing based on yesterday's findings
Cybersentry> /memory save "day2_exploitation"
```

#### Workflow 2: Knowledge Base

```bash
# Build security knowledge base
Cybersentry> /memory save "CVE-2024-1234 affects Apache < 2.4.59"
Cybersentry> /memory save "SQL injection bypasses for ModSecurity"
Cybersentry> /memory save "XSS payload variants for WAF bypass"

# Later, in new session
Cybersentry> /memory list
Cybersentry> /memory apply mem_useful_techniques
```

### Memory Compaction

Reduce memory size while preserving important information:

```bash
# Compact current conversation
Cybersentry> /memory compact

# Status and statistics
Cybersentry> /memory status
```

### Memory Management

```bash
# Show specific memory
Cybersentry> /memory show mem_12345

# Merge memories
Cybersentry> /memory merge mem_12345 mem_67890 "combined_findings"

# Delete memory
Cybersentry> /memory delete mem_12345
```

---

## Workspace & Virtualization

Manage execution environments and Docker containers.

### Workspace Management

```bash
# Show current workspace
Cybersentry> /workspace show

# Change workspace
Cybersentry> /workspace set /home/user/pentests/target_corp

# List workspace contents
Cybersentry> /workspace list

# Execute commands in workspace
Cybersentry> $ ls -la
Cybersentry> $ cat target_info.txt
```

### Docker Container Execution

#### Automatic Container Setup (CTF)

```bash
# CTF automatically sets up container
export CTF_NAME=hackableii
export CTF_INSIDE=true
cai

# Commands execute inside container automatically
Cybersentry> $ whoami
Cybersentry> $ ip addr
```

#### Manual Container Management

```bash
# List available containers
Cybersentry> /virtualization list

# Set active container
Cybersentry> /virtualization set ubuntu_pentest

# All commands now execute in container
Cybersentry> $ nmap -sV localhost

# Return to host
Cybersentry> /virtualization clear
```

### Environment Variables for Virtualization

```bash
# CTF Configuration
export CTF_NAME=hackableii
export CTF_CHALLENGE=web_app
export CTF_SUBNET=192.168.3.0/24
export CTF_IP=192.168.3.100
export CTF_INSIDE=true  # Execute inside container

# Active Container
export Cybersentry_ACTIVE_CONTAINER=abc123def456

cai
```

### Advanced Virtualization Patterns

#### Pattern 1: Isolated Testing

```bash
#!/bin/bash
# isolated_test.sh

# Create isolated container
CONTAINER_ID=$(docker run -d ubuntu:latest sleep infinity)

# Set container for Cybersentry
export Cybersentry_ACTIVE_CONTAINER=$CONTAINER_ID

# Run tests
cai --prompt "
/virtualization set $CONTAINER_ID
Install and test malware sample
Analyze behavior
/save malware_analysis.json
/exit
"

# Cleanup
docker stop $CONTAINER_ID
docker rm $CONTAINER_ID
```

#### Pattern 2: Multi-Container Testing

```bash
# Test across multiple containers
Cybersentry> /virtualization set web_server_container
Cybersentry> $ curl http://localhost

Cybersentry> /virtualization set db_container
Cybersentry> $ psql -l

Cybersentry> /virtualization set app_container
Cybersentry> $ python test_exploit.py
```

---

## CTF Workflows

Specialized workflows for Capture The Flag challenges.

### Basic CTF Setup

```bash
# Configure CTF environment
export CTF_NAME=hackableii
export CTF_CHALLENGE=binary_exploit
export Cybersentry_AGENT_TYPE=redteam_agent
export Cybersentry_MODEL=alias1
export Cybersentry_MAX_TURNS=inf

cai
```

### CTF Challenge Types

#### Type 1: Web Challenges

```bash
export CTF_NAME=webchallenge
export CTF_INSIDE=true

cai --prompt "
/agent bug_bounter_agent
Analyze this web application
Find and exploit vulnerabilities
Extract the flag
/save web_ctf_solution.md
"
```

#### Type 2: Binary Exploitation

```bash
export CTF_NAME=pwn_challenge

cai --prompt "
/agent reverse_engineering_agent
Analyze the binary
Find buffer overflow vulnerability
Develop exploit
/save exploit.py
"
```

#### Type 3: Forensics

```bash
export CTF_NAME=forensics_challenge

cai --prompt "
/agent dfir_agent
Analyze the memory dump
Extract hidden data
Find the flag
/save forensics_analysis.md
"
```

### Automated CTF Solver

```bash
#!/bin/bash
# auto_ctf.sh

CHALLENGES=(
    "web_app:bug_bounter_agent"
    "binary_exploit:reverse_engineering_agent"
    "network_forensics:dfir_agent"
    "crypto:redteam_agent"
)

for challenge in "${CHALLENGES[@]}"; do
    IFS=':' read -r name agent <<< "$challenge"
    
    echo "Solving $name..."
    
    CTF_NAME="ctf_event" \
    CTF_CHALLENGE="$name" \
    Cybersentry_AGENT_TYPE="$agent" \
    cai --prompt "
    Analyze and solve the challenge
    Find the flag
    /save ${name}_solution.json
    /exit
    "
done
```

### CTF with Time Limits

```bash
# Set strict limits for CTF
export Cybersentry_MAX_TURNS=50
export Cybersentry_MAX_INTERACTIONS=200
export Cybersentry_PRICE_LIMIT=5.0

# Force exit if flag not found
# (requires force_until_flag mode)
cai --prompt "solve the CTF challenge"
```

---

## Cost Management

Control and optimize API usage costs.

### Setting Cost Limits

```bash
# Set price limit
export Cybersentry_PRICE_LIMIT=10.0

# Set interaction limit
export Cybersentry_MAX_INTERACTIONS=100

# Set turn limit
export Cybersentry_MAX_TURNS=50

cai
```

### Runtime Cost Adjustment

```bash
# Check current costs
Cybersentry> /cost

# Increase limit if needed
Cybersentry> /config Cybersentry_PRICE_LIMIT=20.0

# Check updated limit
Cybersentry> /config | grep PRICE_LIMIT
```

### Cost Optimization Strategies

#### Strategy 1: Model Selection

```bash
# Use cheaper models for reconnaissance
Cybersentry> /agent redteam_agent
Cybersentry> /model alias1  # Balanced cost/performance

# Use powerful models for complex analysis
Cybersentry> /model gpt-4o
Cybersentry> Analyze complex vulnerability chain
```

#### Strategy 2: Conversation Compaction

```bash
# When approaching token limits
Cybersentry> /compact

# Or set automatic compaction
export Cybersentry_AUTO_COMPACT=true
```

#### Strategy 3: Targeted Prompts

```bash
# Be specific to reduce back-and-forth
Cybersentry> Scan 192.168.1.1 ports 80,443,8080 with nmap -sV

# Instead of:
Cybersentry> Scan 192.168.1.1
# (agent asks which ports)
# (multiple turns = higher cost)
```

### Cost Monitoring

```bash
# View detailed cost breakdown
Cybersentry> /cost

# Per-agent costs
Cybersentry> /cost redteam_agent
Cybersentry> /cost bug_bounter_agent

# Session statistics
Cybersentry> /history
Cybersentry> /cost all
```

### Budget-Constrained Workflows

```bash
#!/bin/bash
# budget_scan.sh

# Set strict budget
export Cybersentry_PRICE_LIMIT=2.0
export Cybersentry_MODEL=alias1  # Cost-effective model

cai --prompt "
/agent redteam_agent
Quick vulnerability scan on $TARGET
Focus on critical issues only
/cost
/save budget_scan.json
/exit
"

# Check if limit was hit
if grep -q "price limit" budget_scan.json; then
    echo "Warning: Price limit reached"
fi
```

---

## Configuration Management

Advanced configuration patterns.

### Configuration Profiles

#### Profile 1: Development

```bash
# dev_profile.env
export Cybersentry_MODEL=alias1
export Cybersentry_DEBUG=2
export Cybersentry_PRICE_LIMIT=5.0
export Cybersentry_TRACING=true
export Cybersentry_MAX_TURNS=20
```

Usage:
```bash
source dev_profile.env
cai
```

#### Profile 2: Production

```bash
# prod_profile.env
export Cybersentry_MODEL=alias1
export Cybersentry_DEBUG=0
export Cybersentry_BRIEF=true
export Cybersentry_PRICE_LIMIT=50.0
export Cybersentry_TRACING=false
export Cybersentry_GUARDRAILS=true
```

#### Profile 3: CTF

```bash
# ctf_profile.env
export Cybersentry_MODEL=alias1
export Cybersentry_AGENT_TYPE=redteam_agent
export Cybersentry_MAX_TURNS=inf
export Cybersentry_PRICE_LIMIT=20.0
export Cybersentry_DEBUG=1
```

### Per-Agent Model Override

```bash
# Set different models for different agents
export Cybersentry_REDTEAM_AGENT_MODEL=gpt-4o
export Cybersentry_BUG_BOUNTER_AGENT_MODEL=alias1
export Cybersentry_DFIR_AGENT_MODEL=claude-3-5-sonnet-20241022

# Default model for others
export Cybersentry_MODEL=alias1

cai
```

### Dynamic Configuration

```bash
# Start with base config
Cybersentry> /config

# Adjust during session
Cybersentry> /config Cybersentry_DEBUG=2
Cybersentry> /config Cybersentry_PRICE_LIMIT=15.0

# Verify changes
Cybersentry> /env | grep Cybersentry
```

---

## Integration Patterns

Integrate Cybersentry with other tools and services.

### MCP Integration

#### Pattern 1: Burp Suite Integration

```bash
# Start Burp Suite MCP server
# (in separate terminal)
burp-mcp-server --port 9876

# In Cybersentry
Cybersentry> /mcp load http://localhost:9876/sse burp
Cybersentry> /mcp tools burp
Cybersentry> /mcp add redteam_agent burp

# Use Burp tools
Cybersentry> Use Burp to scan https://target.com
```

#### Pattern 2: Custom Tool Integration

```bash
# Load custom MCP server
Cybersentry> /mcp load stdio "python my_custom_tools.py" custom

# Add to agent
Cybersentry> /mcp add bug_bounter_agent custom

# Use custom tools
Cybersentry> Use custom scanner on target
```

### API Integration

```bash
#!/bin/bash
# api_integration.sh

# Get Cybersentry results
RESULT=$(cai --prompt "scan $TARGET ; /save -" 2>/dev/null)

# Send to external API
curl -X POST https://api.security-platform.com/scans \
  -H "Content-Type: application/json" \
  -d "$RESULT"
```

### Webhook Integration

```bash
#!/bin/bash
# webhook_notify.sh

# Run scan
cai --prompt "security scan on $TARGET ; /save results.json"

# Send webhook notification
curl -X POST $WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{
    "target": "'$TARGET'",
    "status": "complete",
    "results": "'$(cat results.json)'"
  }'
```

---

## Troubleshooting

Common issues and solutions.

### Issue: Price Limit Reached

```bash
# Check current cost
Cybersentry> /cost

# Increase limit
Cybersentry> /config Cybersentry_PRICE_LIMIT=20.0

# Or restart with higher limit
exit
Cybersentry_PRICE_LIMIT=20.0 cai
```

### Issue: Max Interactions Exceeded

```bash
# Check current count
Cybersentry> /env | grep MAX_INTERACTIONS

# Increase limit
Cybersentry> /config Cybersentry_MAX_INTERACTIONS=500

# Or use /flush to start fresh
Cybersentry> /flush
```

### Issue: Agent Not Responding

```bash
# Interrupt current operation
Ctrl+C

# Check agent status
Cybersentry> /agent

# Switch to different agent
Cybersentry> /agent redteam_agent

# Check configuration
Cybersentry> /config
```

### Issue: Context Window Full

```bash
# Check context usage (Cybersentry PRO)
Cybersentry> /context

# Compact conversation
Cybersentry> /compact

# Or flush and start fresh
Cybersentry> /flush
```

### Issue: Container Execution Problems

```bash
# Check virtualization status
Cybersentry> /virtualization info

# List containers
Cybersentry> /virtualization list

# Clear container setting
Cybersentry> /virtualization clear

# Verify workspace
Cybersentry> /workspace show
```

### Issue: Memory Loading Fails

```bash
# Check memory status
Cybersentry> /memory status

# List available memories
Cybersentry> /memory list

# Clear corrupted memory
Cybersentry> /memory delete mem_problematic

# Check storage directory
$ ls -la ~/.cai/memory/
```

### Debug Mode

```bash
# Enable maximum debugging
export Cybersentry_DEBUG=2
cai

# Or enable during session
Cybersentry> /config Cybersentry_DEBUG=2
```

---

## Best Practices

### 1. Session Management

```bash
# Always save important sessions
Cybersentry> /save project_name_$(date +%Y%m%d).json

# Use descriptive filenames
Cybersentry> /save pentest_target_corp_phase1.json
```

### 2. Cost Control

```bash
# Set reasonable limits
export Cybersentry_PRICE_LIMIT=10.0
export Cybersentry_MAX_TURNS=50

# Monitor regularly
Cybersentry> /cost
```

### 3. Agent Selection

```bash
# Use specialized agents
# ✅ Good: /agent bug_bounter_agent for web apps
# ❌ Bad: /agent one_tool_agent for complex tasks

# Let selection_agent help
Cybersentry> /agent selection_agent
Cybersentry> I need to test a mobile application
```

### 4. Parallel Execution

```bash
# Use YAML for complex setups
# ✅ Good: cai --yaml team_config.yaml
# ❌ Bad: Manual /parallel add for many agents
```

### 5. Memory Usage

```bash
# Save important findings
Cybersentry> /memory save "critical vulnerability in auth system"

# Use descriptive names
# ✅ Good: "SQLi in admin panel - bypasses WAF"
# ❌ Bad: "bug1"
```

---

## Quick Reference

### Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `Cybersentry_MODEL` | Default model | `alias1` |
| `Cybersentry_AGENT_TYPE` | Default agent | `redteam_agent` |
| `Cybersentry_PARALLEL` | Parallel count | `3` |
| `Cybersentry_QUEUE_FILE` | Auto-load queue | `prompts.txt` |
| `Cybersentry_MEMORY` | Memory mode | `episodic` |
| `Cybersentry_MEMORY_ONLINE` | Auto-save memory | `true` |
| `Cybersentry_PRICE_LIMIT` | Cost limit | `10.0` |
| `Cybersentry_MAX_TURNS` | Turn limit | `50` |
| `Cybersentry_ACTIVE_CONTAINER` | Docker container | `abc123` |

### Command Patterns

```bash
# Automation
cai --prompt "command ; command ; command"
Cybersentry_QUEUE_FILE=file.txt cai

# Parallel
cai --yaml agents.yaml --prompt "task"
Cybersentry_PARALLEL=3 cai

# CTF
CTF_NAME=challenge cai
```

---

## Next Steps

- 📖 [Getting Started](getting_started.md) - Basic usage
- 📚 [Commands Reference](commands_reference.md) - All commands
- 🏠 [CLI Overview](cli_index.md) - Main documentation

---

*Last updated: November 2025 | Cybersentry CLI v0.6+*

