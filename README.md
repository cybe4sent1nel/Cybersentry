[![TryHackMe Badge](https://tryhackme-badges.s3.amazonaws.com/fahadkhanxyz8816.png)](https://tryhackme.com/p/fahadkhanxyz8816)
# Cybersentry
# 🛡️ Cybersentry

**Cybersentry** is an advanced, AI-powered cybersecurity agent framework designed to assist security professionals, CTF players, and bug bounty hunters. It leverages Large Language Models (LLMs) to autonomously plan, execute tools, and analyze results within a secure environment.

> **Update:** Now features a "Gemini-style" interactive CLI with live status updates and witty cyberpunk commentary! 🤖✨

---

## 🚀 Key Features

* **🤖 AI-Driven Agents:** Deploy specialized agents (e.g., CTF Agent, Blue Team, Bug Hunter) to solve complex security challenges.
* **🔧 Tool Integration:** Agents can autonomously execute system commands, network scans, and custom scripts.
* **🌐 Multi-Model Support:** Powered by **LiteLLM**, allowing seamless switching between OpenRouter, OpenAI, Anthropic, and local models.
* **⚡ Smart Rate Limiting:** Built-in client-side throttling to prevent provider rate-limit blocks.
* **✨ Interactive UI:** Beautiful, animated CLI experience powered by `rich`, featuring dynamic status updates while the AI "thinks."

---

## 🛠️ Installation

### Prerequisites
* **Python 3.12+**
* **Linux/WSL2** environment (Recommended)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/cybersentry.git](https://github.com/yourusername/cybersentry.git)
    cd cybersentry
    ```

2.  **Set up the Virtual Environment:**
    *Using `uv` (Recommended if available):*
    ```bash
    uv sync
    source .venv/bin/activate
    ```
    *Or using standard `pip`:*
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e .
    ```

---

## ⚙️ Configuration

Cybersentry relies on environment variables to manage API keys and model selection.

### 1. Set API Keys
Create a `.env` file or export these variables in your shell. (Example using **OpenRouter**):

```bash
# Your API Key (OpenRouter keys work with the OpenAI client in LiteLLM)
export OPENAI_API_KEY="sk-or-v1-..."

# Set the Base URL for OpenRouter
export OPENAI_API_BASE="[https://openrouter.ai/api/v1](https://openrouter.ai/api/v1)"
# Set Requests Per Minute (Recommended: 40 for free tiers)
export LITELLM_MAX_RPM=40

# Set Tokens Per Minute
export LITELLM_MAX_TPM=80000
# DEfine model of your choice
export CYBERSENTRY_MODEL="openrouter/mistralai/mistral-7b-instruct:free"
# COmmand to run
cybersentry
