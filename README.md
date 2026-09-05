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

---

## Running with Docker

### 2. Build and Start

```bash
docker compose up --build
```

*(Add `-d` to run detached in the background)*

The app will:
1. Build the Tailwind CSS
2. Install Python dependencies
3. Test the Supabase connection
4. Auto-create any missing database tables (via SQLAlchemy)
5. Start the FastAPI server on port 8000

### 3. Access the Application

| URL | Description |
|-----|-------------|
| [http://localhost:8000](http://localhost:8000) | Web Application |
| [http://localhost:8000/docs](http://localhost:8000/docs) | Swagger API Docs |
| [http://localhost:8000/redoc](http://localhost:8000/redoc) | ReDoc API Docs |

### 4. Stop the Application

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
