# GitHub Assistant Agent

A specialized GitHub operations agent that manages repositories, issues, pull requests, and performs code search across GitHub.

## MCP Server

Uses `@modelcontextprotocol/server-github` (npx) — the official GitHub MCP server.

### Tools Provided
- `search_repositories` — Search for GitHub repositories
- `search_code` — Search code across GitHub
- `create_issue` — Create a new issue in a repository
- `list_issues` — List issues with filters
- `create_pull_request` — Create a pull request
- `get_file_contents` — Read file contents from a repository
- `create_or_update_file` — Create or update a file via a commit
- `list_branches` — List branches in a repository
- `fork_repository` — Fork a repository

## Setup

The agent loads env in this order:

1. `backend_service/.env`
2. `app/agentic/github_assistant/.env` (optional override)

Required when using GitHub tools:

- `GITHUB_PERSONAL_ACCESS_TOKEN`

Recommended token scopes: `repo`, `read:org`, `read:user`.

## Running

```bash
uvicorn app.agentic.github_assistant.agent:a2a_app --host localhost --port 8002
```

## Port: 8002
