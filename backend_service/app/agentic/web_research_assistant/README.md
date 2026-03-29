# Web Research Assistant Agent

A specialized web research agent that fetches, analyzes, and summarizes content from any public web page or API endpoint.

## MCP Server

Uses `fetch-mcp` (npx) for web fetch operations.

### Tools Provided
- `fetch` — Fetch a URL and return the content as markdown, text, or raw HTML

## Setup

The agent loads env from `backend_service/.env` and optional agent-local `.env` override.

Requirements:

- Node.js and `npx` available on PATH
- No auth needed for public URLs

## Running

```bash
uvicorn app.agentic.web_research_assistant.agent:a2a_app --host localhost --port 8004
```

## Port: 8004
