# Time & Timezone Assistant Agent

A specialized time and timezone agent that provides current times, converts between timezones, helps schedule meetings, and performs date/time calculations.

## MCP Server

Uses `mcp-server-time` (uvx/pip) — the official Time MCP server.

### Tools Provided
- `get_current_time` — Get the current time in a specified timezone
- `convert_time` — Convert a time between timezones

## Setup

The agent loads env from `backend_service/.env` and optional agent-local `.env` override.

No additional authentication is required.

## Running

```bash
uvicorn app.agentic.time_assistant.agent:a2a_app --host localhost --port 8010
```

## Port: 8010
