# Report Writer Agent

A specialized report writing agent that researches topics from the web and produces well-structured, professional reports saved to disk.

## MCP Servers

Uses `@modelcontextprotocol/server-fetch` (npx) — the official Fetch MCP server for web research.
Also uses the custom `write_to_disk` tool for saving reports.

### Tools Provided
- `fetch` — Fetch a URL and return the content as markdown
- `write_to_disk` — Save the generated report to a file on disk

## Setup

The agent loads env from `backend_service/.env` and optional agent-local `.env` override.

Requirements:

- Node.js and `npx` available on PATH (for `fetch-mcp`)
- No additional authentication required for public web research

## Output Format

Reports are saved using the filename passed to `write_to_disk`.

## Running

```bash
uvicorn app.agentic.report_writer.agent:a2a_app --host localhost --port 8011
```

## Port: 8011
