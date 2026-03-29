# Database Analyst Agent

A specialized database analyst agent that executes SQL queries, designs schemas, analyzes data, and manages SQLite databases.

## MCP Server

Uses `mcp-server-sqlite` (uvx/pip) — the official SQLite MCP server.

### Tools Provided
- `read_query` — Execute a SELECT query and return results
- `write_query` — Execute INSERT, UPDATE, or DELETE queries
- `create_table` — Create a new table with specified schema
- `list_tables` — List all tables in the database
- `describe_table` — Get column info for a specific table
- `append_insight` — Store an analytical insight

## Setup

Set env in `backend_service/.env` (or override in `app/agentic/database_analyst/.env`):

```env
SQLITE_DB_PATH=D:/projects/TheOrc/backend_service/local.db
```

If not set, the SQLite MCP server defaults to `database.db` in the current working directory.

## Running

```bash
uvicorn app.agentic.database_analyst.agent:a2a_app --host localhost --port 8006
```

## Port: 8006
