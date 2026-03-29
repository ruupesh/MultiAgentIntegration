# Job Search Assistant Agent

A specialized A2A agent that finds job opportunities on the web and can persist results to disk.

## Features

- Web search via DuckDuckGo MCP.
- `write_to_disk` helper tool for writing output to local files.
- JSON list payloads written through `write_to_disk` are converted to CSV.

## Prerequisites

Set these in `backend_service/.env` (or override in `app/agentic/job_search/.env`):

- `AGENT_MODEL` (optional)
- `DDG_MCP_PATH` (required for DuckDuckGo MCP startup)

Example:

```env
DDG_MCP_PATH=D:/projects/TheOrc/backend_service/venv/Lib/site-packages/duckduckgo_mcp_server/server.py
```

## Run

From `backend_service`:

```powershell
uvicorn app.agentic.job_search.agent:a2a_app --host localhost --port 8001
```

Endpoints:

- Base URL: `http://localhost:8001`
- Agent card: `http://localhost:8001/.well-known/agent.json`
