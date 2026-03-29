# Frontend Setup

This guide covers local setup for the Next.js frontend.

## 1. Prerequisites

Install first:

- Node.js 20+
- npm
- Backend API running on `http://localhost:8000`

Backend setup is documented in [BACKEND_SETUP.md](./BACKEND_SETUP.md).

## 2. Install Dependencies

From `frontend`:

```powershell
npm install
```

## 3. Configure Environment Variables

Create or update `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

This is the base URL used by the UI for all backend API calls.

## 4. Start Development Server

From `frontend`:

```powershell
npm run dev
```

UI URL: `http://localhost:3000`

## 5. Build Validation

```powershell
npm run build
npm run start
```

## 6. Functional Verification

After frontend and backend are up:

1. Open `http://localhost:3000`.
2. Register or log in.
3. Verify `/agents` and `/mcp-tools` list data.
4. Verify `/marketplace` lists published items.
5. Verify `/chat` can send messages.

## 7. Troubleshooting

### Frontend cannot reach backend

- Confirm backend is on `localhost:8000`.
- Confirm `NEXT_PUBLIC_API_URL` in `.env.local`.
- Restart dev server after env changes.

### UI loads but data pages are empty

- Confirm backend migrations were applied.
- Confirm you have seeded data if your test flow expects demo marketplace content.
- Confirm remote agent services are running if chat should use sub-agents.

### Port `3000` is occupied

```powershell
npx next dev --port 3001
```

Then open `http://localhost:3001`.