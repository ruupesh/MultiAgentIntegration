# TheOrc Frontend

Next.js 16 + React 19 frontend for authentication, agent management, MCP tool management, marketplace, and orchestrated chat.

## Stack

- Next.js App Router
- TypeScript
- Material UI
- Redux Toolkit + RTK Query
- React Hook Form + Zod

## Prerequisites

- Node.js 20+
- npm
- Backend API running on `http://localhost:8000`

## Setup

From `frontend`:

```bash
npm install
```

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Run

```bash
npm run dev
```

Open `http://localhost:3000`.

## Scripts

```bash
npm run dev
npm run build
npm run start
npm run lint
```

## App Routes

- `/login`
- `/register`
- `/agents`
- `/mcp-tools`
- `/marketplace`
- `/chat`

## Key Frontend Modules

- `src/store/api/*` for backend API slices (auth, agents, MCP tools, marketplace, chat)
- `src/store/slices/chatSlice.ts` for chat UI state
- `src/components/*` for page and feature components
- `src/lib/auth.ts` for token and auth helpers

## Notes

- If you change `NEXT_PUBLIC_API_URL`, restart the dev server.
- Marketplace and chat behavior depends on backend data and agent services being up.
