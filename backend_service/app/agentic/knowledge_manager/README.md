# Knowledge Manager Agent

A specialized knowledge management agent that maintains a persistent knowledge graph with entities, observations, and relations.

## MCP Server

Uses `@modelcontextprotocol/server-memory` (npx) — the official Memory MCP server.

### Tools Provided
- `create_entities` — Create new entities with observations
- `create_relations` — Define relations between entities
- `add_observations` — Add observations to existing entities
- `delete_entities` — Remove entities from the knowledge graph
- `delete_observations` — Remove specific observations
- `delete_relations` — Remove relations between entities
- `read_graph` — Read the entire knowledge graph
- `search_nodes` — Search for entities by name or content
- `open_nodes` — Open specific entities by name

## Setup

The agent loads env from `backend_service/.env` and then optional agent-local `.env` override.

No additional authentication is required for the memory MCP server.

Persistence note:

- Memory data is written to the configured memory storage path used by the memory MCP server.

## Running

```bash
uvicorn app.agentic.knowledge_manager.agent:a2a_app --host localhost --port 8005
```

## Port: 8005
