# Kaku: Kakuro Daily Puzzle Application
A daily kakuro puzzle generator intended to bring you some logical fun daily just in time for your morning coffee. Kaku generates a variety of difficulty and layouts of unique puzzles. This is done by utilising random generators and solution parsing algorithms.

## Features
- A new Kakuro puzzle generated daily
- Interactive grid with keyboard (arrow key) navigation between entry cells
- Timer with pause/resume
- Answer checking against the stored solution, without exposing it to the client

## Tech stack
- **Backend**: FastAPI, backed by Supabase (Postgres) for puzzle/solution storage
- **Frontend**: React + Vite
- **Deployment**: Vercel, serving the API as a Python serverless function and the frontend as a static build from a single project (see `vercel.json`)

## Local setup

### Environment variables
Copy `.env.example` to `.env` and fill in:
- `SUPABASE_URL`
- `SUPABASE_SECRET_KEY`
- `CORS_ORIGINS` (defaults to `http://localhost:5173`)

### Backend
```
pip install -r requirements.txt
uvicorn api.main:app --reload
```
Runs on `http://localhost:8000`.

### Frontend
```
cd frontend
npm install
npm run dev
```
Runs on `http://localhost:5173`, with API calls proxied to the backend (see `frontend/vite.config.js`).

## Generating and pruning puzzles
Puzzles are generated a month at a time and pruned once they're in the past. Both run on a schedule via GitHub Actions (`.github/workflows/`), but can also be run manually:

```
python -m api.scripts.generate_monthly_puzzles --year <YYYY> --month <M>
python -m api.scripts.prune_old_puzzles
```

Both require `SUPABASE_URL` and `SUPABASE_SECRET_KEY` to be set in the environment.

## API
| Method | Route | Description |
| --- | --- | --- |
| GET | `/puzzles/today` | Fetch today's puzzle |
| GET | `/puzzles/{date}` | Fetch the puzzle for a given date (`YYYY-MM-DD`) |
| POST | `/puzzles/{date}/check` | Check a submitted grid against the stored solution |
