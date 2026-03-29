# Git Assistant Agent

A specialized Git operations agent that analyzes commit history, shows diffs, manages branches, and investigates code changes.

## MCP Server

Uses `mcp-server-git` (uvx/pip) — the official Git MCP server.

### Tools Provided
- `git_log` — Show commit history with filtering options
- `git_diff` — Show diffs between commits, branches, or working tree
- `git_status` — Show working tree status
- `git_show` — Show details of a specific commit
- `git_diff_staged` — Show staged changes
- `git_diff_unstaged` — Show unstaged changes
- `git_list_branches` — List all branches

## Setup

Set env in `backend_service/.env` (or override in `app/agentic/git_assistant/.env`):

```env
GIT_REPO_PATH=D:/projects/TheOrc
```

`GIT_REPO_PATH` must point to a valid Git repository.

## Running

```bash
uvicorn app.agentic.git_assistant.agent:a2a_app --host localhost --port 8009
```

## Port: 8009
