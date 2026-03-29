# Backend Setup

This guide covers local setup for the FastAPI backend and optional remote agent services used by TheOrc.

## 1. Prerequisites

Install the following first:

- Python 3.11+
- PostgreSQL (local or Docker)
- PowerShell (Windows)
- Windows Terminal (`wt.exe`) if you want one-command multi-tab startup
- Node.js + npm (required by MCP servers that run through `npx`)

Database setup is documented in [POSTGRES_SETUP.md](./POSTGRES_SETUP.md).

## 2. Create and Activate a Virtual Environment

From `backend_service`:

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure Environment Variables

Create `backend_service/.env`.

Minimum variables:

```env
GOOGLE_API_KEY=your_google_api_key
DATABASE_URL=postgresql+asyncpg://admin:admin@localhost:5432/my_db
SECRET_KEY=replace-with-a-strong-secret
```

Common optional variables:

```env
AGENT_MODEL=gemini/gemini-2.5-flash
AGENT_REASONING_EFFORT=medium
AGENT_THINKING_LEVEL=MEDIUM
AGENT_INCLUDE_THOUGHTS=false
ORCHESTRATOR_ENABLE_DIRECT_MCP_TOOLS=false
A2A_AUTH_REQUIRED=false
DDG_MCP_PATH=<path to duckduckgo_mcp_server/server.py>
FILESYSTEM_ALLOWED_PATHS=D:/projects/TheOrc
SQLITE_DB_PATH=D:/projects/TheOrc/backend_service/local.db
GIT_REPO_PATH=D:/projects/TheOrc
GITHUB_PERSONAL_ACCESS_TOKEN=<github_pat_if_using_github_agent>
```

Notes:

- Agent processes load `backend_service/.env`, then agent-local `.env` (if present) with override.
- Keep `A2A_AUTH_REQUIRED=false` for local development unless you specifically want JWT-protected A2A endpoints.
- `NEXT_PUBLIC_API_URL` belongs in `frontend/.env.local`, not here.

## 4. Apply Database Migrations

From `backend_service`:

```powershell
alembic upgrade head
```

This applies schema migrations. The API startup also calls `Base.metadata.create_all`, but migrations are still the recommended baseline.

## 5. Optional Demo Seed Data

If you want demo users, demo-owned agents/MCP tools, and marketplace entries, run:

```powershell
python -m scripts.seed_users
python -m scripts.seed_agents_and_market
python -m scripts.seed_mcp_and_market
```

Important:

- `scripts.seed_users` is destructive for data rows (local demo usage only).

## 6. Start Only the Main API

From `backend_service`:

```powershell
.\venv\Scripts\Activate.ps1
python run.py
```

Endpoints:

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`

## 7. Start the Full Multi-Agent Stack

The built-in launcher starts 12 services (API + 11 remote agents).

Command:

```powershell
.\start_all_agents.ps1
```

Before first run, verify `start_all_agents.ps1` has the correct `ProjectRoot` path for your machine.

Ports:

- `8000` API (`app.main:app`)
- `8001` Job Search
- `8002` GitHub Assistant
- `8003` Filesystem Assistant
- `8004` Web Research Assistant
- `8005` Knowledge Manager
- `8006` Database Analyst
- `8007` Reasoning Assistant
- `8008` Browser Automation
- `8009` Git Assistant
- `8010` Time Assistant
- `8011` Report Writer

Manual startup example:

```powershell
uvicorn app.main:app --host localhost --port 8000 --reload
uvicorn app.agentic.web_research_assistant.agent:a2a_app --host localhost --port 8004
```

## 8. Verify Backend Health

1. Open `http://127.0.0.1:8000/docs`.
2. Test register/login endpoints.
3. If using Postman, import `TheOrc.postman_collection.json`.
4. Open the frontend and verify agents, MCP tools, marketplace, and chat load.

## 9. Troubleshooting

### Database connection errors

- Confirm PostgreSQL is running.
- Confirm `DATABASE_URL` credentials and DB name are correct.
- Confirm the target database exists.

### Import or module errors

- Activate the virtual environment.
- Re-run `pip install -r requirements.txt`.
- Run commands from the `backend_service` directory.

### Remote agent returns `401 Unauthorized`

- For local dev, keep `A2A_AUTH_REQUIRED=false`.
- Restart agents after changing auth-related environment variables.

### Orchestrator cannot use sub-agents

- Ensure ports `8001` to `8011` are up.
- Check service terminals for startup failures (missing env vars, missing `npx`/`uvx`, etc.).

### MCP tool missing in orchestrator discovery

- Set `ORCHESTRATOR_ENABLE_DIRECT_MCP_TOOLS=true` if you want direct MCP exposure in discovery.