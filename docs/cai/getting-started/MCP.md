# MCP

Cybersentry supports the Model Context Protocol (MCP) for integrating external tools and services with AI agents. MCP is supported via two transport mechanisms:

1. **SSE (Server-Sent Events)** - For web-based servers that push updates over HTTP connections:
```bash
Cybersentry>/mcp load http://localhost:9876/sse burp
```

2. **STDIO (Standard Input/Output)** - For local inter-process communication:
```bash
Cybersentry>/mcp load stdio myserver python mcp_server.py
```

Once connected, you can add the MCP tools to any agent:
```bash
Cybersentry>/mcp add burp redteam_agent
Adding tools from MCP server 'burp' to agent 'Red Team Agent'...
                                 Adding tools to Red Team Agent
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Tool                              ┃ Status ┃ Details                                         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ send_http_request                 │ Added  │ Available as: send_http_request                 │
│ create_repeater_tab               │ Added  │ Available as: create_repeater_tab               │
│ send_to_intruder                  │ Added  │ Available as: send_to_intruder                  │
│ url_encode                        │ Added  │ Available as: url_encode                        │
│ url_decode                        │ Added  │ Available as: url_decode                        │
│ base64encode                      │ Added  │ Available as: base64encode                      │
│ base64decode                      │ Added  │ Available as: base64decode                      │
│ generate_random_string            │ Added  │ Available as: generate_random_string            │
│ output_project_options            │ Added  │ Available as: output_project_options            │
│ output_user_options               │ Added  │ Available as: output_user_options               │
│ set_project_options               │ Added  │ Available as: set_project_options               │
│ set_user_options                  │ Added  │ Available as: set_user_options                  │
│ get_proxy_http_history            │ Added  │ Available as: get_proxy_http_history            │
│ get_proxy_http_history_regex      │ Added  │ Available as: get_proxy_http_history_regex      │
│ get_proxy_websocket_history       │ Added  │ Available as: get_proxy_websocket_history       │
│ get_proxy_websocket_history_regex │ Added  │ Available as: get_proxy_websocket_history_regex │
│ set_task_execution_engine_state   │ Added  │ Available as: set_task_execution_engine_state   │
│ set_proxy_intercept_state         │ Added  │ Available as: set_proxy_intercept_state         │
│ get_active_editor_contents        │ Added  │ Available as: get_active_editor_contents        │
│ set_active_editor_contents        │ Added  │ Available as: set_active_editor_contents        │
└───────────────────────────────────┴────────┴─────────────────────────────────────────────────┘
Added 20 tools from server 'burp' to agent 'Red Team Agent'.
Cybersentry>/agent 13
Cybersentry>Create a repeater tab
```

You can list all active MCP connections and their transport types:
```bash
Cybersentry>/mcp list
```

https://github.com/user-attachments/assets/386a1fd3-3469-4f84-9396-2a5236febe1f

## Example: Controlling Chrome with Cybersentry

1) Install node, following the instructions on the [official site](https://nodejs.org/en/download/current)

2) Instal Chrome (Chromium is not compatible with this functionality)

3) Run the following commands:
	```
	/mcp load stdio devtools npx chrome-devtools-mcp@latest
	/mcp add devtools redteam_agent
	/agent redteam_agent
	```

Once this is done, you will have full control of Chrome using the red team agent.


