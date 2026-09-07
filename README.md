# DTFIAS
Digital Twin for Indian Antarctic Stations

## Prerequisites

Before running the project, ensure you have:
- **Docker Desktop** (make sure the Docker engine/daemon is running)
- **A Supabase project** — [create one free at supabase.com](https://supabase.com)

> **No local database required.** DTFIAS now uses [Supabase](https://supabase.com) (hosted PostgreSQL) — Docker Compose only runs the FastAPI backend. The database lives in the cloud.

---

## Setup

### 1. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Then open `.env` and fill in your Supabase connection string:

```env
DATABASE_URL=postgresql+asyncpg://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
```

**Where to find your connection string:**
1. Go to your [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project → **Project Settings** → **Database**
3. Scroll to **Connection string** → select **URI**
4. Copy the string and **replace** `postgresql://` with `postgresql+asyncpg://`

### 2. Apply Database Schema

Before starting the backend, apply the initial schema to your Supabase project:
- Open your Supabase Dashboard → **SQL Editor** → **New Query**
- Paste and run the contents of `scripts/migrations/001_initial_schema.sql`
- Or run via `psql "postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres" -f scripts/migrations/001_initial_schema.sql`

To verify database connectivity:
```bash
python scripts/test_db_connection.py
```

---

## Running with Docker

### 3. Build and Start

```bash
docker compose up --build
```

*(Add `-d` to run detached in the background)*

The container will:
1. Pre-build Tailwind CSS
2. Install Python 3.12+ dependencies
3. Start the FastAPI server on port 8000

### 4. Access the Application

| URL | Description |
|-----|-------------|
| [http://localhost:8000](http://localhost:8000) | Web Application |
| [http://localhost:8000/docs](http://localhost:8000/docs) | Swagger API Docs |
| [http://localhost:8000/redoc](http://localhost:8000/redoc) | ReDoc API Docs |

### 5. Stop the Application

```bash
docker compose down
```

---

## Running Locally (without Docker)

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start the dev server
uvicorn main:app --reload
```

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `failed to connect to the docker API` | Open Docker Desktop and wait for the engine to start |
| `✗ Database Connection Test FAILED` | Check that `DATABASE_URL` in `.env` is correct and your Supabase project is active |
| `invalid connection string` | Ensure you replaced `postgresql://` with `postgresql+asyncpg://` in the DATABASE_URL |
| `docker: invalid reference format` | Use `docker compose up --build`, not `docker run .` |
