# Project Setup Docs

This folder contains local setup guides for TheOrc.

Available guides:

- [POSTGRES_SETUP.md](./POSTGRES_SETUP.md): Run PostgreSQL locally with Docker (persistent data).
- [BACKEND_SETUP.md](./BACKEND_SETUP.md): Set up FastAPI, migrations, and optional multi-agent services.
- [FRONTEND_SETUP.md](./FRONTEND_SETUP.md): Set up and run the Next.js UI.

Recommended order:

1. Complete PostgreSQL setup.
2. Complete backend setup and verify the API on port `8000`.
3. Start agent services if you want orchestrated multi-agent chat.
4. Complete frontend setup and verify the UI on port `3000`.