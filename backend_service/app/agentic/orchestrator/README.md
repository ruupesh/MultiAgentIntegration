# Supervisor (Orchestrator Agent)

The Supervisor is the root orchestration agent used by backend chat processing. It is not run as a standalone A2A service.

## Runtime Flow

1. `tool_agent_discovery` classifies the user request and outputs routing JSON.
2. `Orchestrator` reads that routing result and dynamically configures:
   - `sub_agents` for single-agent handoff flows
   - `AgentTool` wrappers for multi-agent call-and-return flows
   - direct MCP toolsets when requested and available

The root is a `SequentialAgent`: discovery -> orchestrator.

## Built-in Tools

- `check_prime` (HITL confirmation enabled)
- `check_weather`
- `find_file_path` (HITL confirmation enabled)

## Remote Agents and MCP Sources

- Remote agent catalog comes from `app/agentic/adapters/remote_agents_conf.yml` or DB overrides.
- MCP tool catalog comes from `app/agentic/adapters/mcp_conf.yml` or DB overrides.
- Direct MCP use in discovery is gated by `ORCHESTRATOR_ENABLE_DIRECT_MCP_TOOLS`.

## Environment Variables

- `AGENT_MODEL` (optional, defaults to `gemini/gemini-2.5-flash`)
- `ORCHESTRATOR_ENABLE_DIRECT_MCP_TOOLS` (`true`/`false`, default `false`)
- `AGENT_REASONING_EFFORT`, `AGENT_THINKING_LEVEL`, `AGENT_INCLUDE_THOUGHTS` (optional)

## How to Run

Start the backend API from `backend_service`:

```powershell
python run.py
```

The orchestrator is invoked through chat API requests handled by `app/services/chat_service.py`.

