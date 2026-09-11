# DTFIAS: Operations, Deployment & Observability Manual

> **Document Status:** Authoritative Operations & Deployment Guide  
> **Target Path:** `docs/operations.md`  
> **Owner Agent:** Documentation Agent / DTFIAS Engineering  
> **Last Verified:** September 2026  

---

## 1. Environment Configuration

The application reads configuration from environment variables defined in `.env` (managed via `pydantic-settings` in `app/config/settings.py`). 

> [!CAUTION]
> Never commit `.env` or real credential strings to version control. Always distribute `.env.example` with non-sensitive template values.

### 1.1 Complete Environment Variable Reference

| Variable Name | Required | Default / Format | Description & Security Guidelines |
| :--- | :---: | :--- | :--- |
| `APP_NAME` | No | `"DTFIAS"` | Human-readable application title displayed in header and Swagger docs. |
| `ENVIRONMENT` | Yes | `development` / `production` | Runtime mode. In `production`, secure cookies (`secure=True`) and strict CORS are enforced. |
| `DATABASE_URL` | Yes | `postgresql+asyncpg://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres` | Asynchronous connection string for SQLAlchemy using `asyncpg`. **Must use the Postgres database password, NOT the anon key.** |
| `SUPABASE_URL` | Yes | `https://[REF].supabase.co` | Supabase project API gateway endpoint. |
| `SUPABASE_KEY` | Yes | `eyJ...` (anon key) | Public Supabase publishable key for client identification. |
| `SUPABASE_SERVICE_ROLE_KEY` | Yes | `eyJ...` (service role) | Superuser administrative key. **Backend only (Constraint C13). Never pass to static files or templates.** |
| `SECRET_KEY` | Yes | 64-char hex string | Master cryptographic secret used for JWT signing and session state encryption. |
| `ALGORITHM` | No | `HS256` | JWT signature algorithm. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `480` (8 hours) | Token lifespan before requiring re-authentication. |
| `COOKIE_SECURE` | No | `True` (prod) / `False` (dev) | Configures the `secure` flag on session cookies (Constraint C10). |
| `SIMULATION_INTERVAL_SECONDS` | No | `5` | Cadence at which the background telemetry simulator injects new polar sensor data. |

---

## 2. Local Development Setup

### 2.1 Prerequisites
- **Python 3.12+** (64-bit)
- **Git**
- Active access to a Supabase project (hosted PostgreSQL)

### 2.2 Step-by-Step Initialization

```bash
# 1. Clone repository
git clone https://github.com/adixyaxo/DTFIAS.git
cd DTFIAS

# 2. Set up Python virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure local environment file
cp .env.example .env
# Open .env in your editor and configure DATABASE_URL and SECRET_KEY

# 5. Execute initial database schema migrations (if not already applied)
# Run scripts/migrations/001_initial_schema.sql in the Supabase SQL Editor
# OR run via psql using the standard postgresql:// URI:
# psql "postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres" -f scripts/migrations/001_initial_schema.sql

# 6. Verify database connectivity
python scripts/test_db_connection.py

# 7. Start the development server with live reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Once started, access:
- Application UI: `http://localhost:8000`
- Interactive OpenAPI Docs: `http://localhost:8000/docs`
- Alternative API Spec: `http://localhost:8000/redoc`

---

## 3. Production Deployment Architecture

### 3.1 Containerized Deployment (Docker)
The system is packaged as a clean, single-stage Python 3.12 container adhering to Constraint C17 (bundler-free runtime with zero npm dependencies required).

```dockerfile
# Build image
docker build -t dtfias-core:latest .

# Run container
docker run -d \
  --name dtfias \
  -p 8000:8000 \
  --env-file .env \
  dtfias-core:latest
```

### 3.2 Docker Compose Stack
```bash
docker compose up -d --build
```
The compose stack binds port 8000 and restarts automatically on system reboot.

---

## 4. Observability, Logging & Health Checks

### 4.1 Health Check Endpoints
- `GET /health` or `GET /api/v1/health`
  - Returns `{"status": "ok", "database": "connected", "timestamp": "2026-09-08T..."}`.
  - Used by container orchestrators (Docker, Kubernetes, AWS ECS) and load balancers.

### 4.2 Logging Standards
- Structured JSON logging is enforced across all application layers (`app/middleware/logging.py`).
- Every HTTP request receives a unique `X-Request-ID` (UUIDv4) passed through response headers and included in all log lines.
- **Log Levels:**
  - `DEBUG`: In-depth telemetry parsing and simulation steps (disabled in production).
  - `INFO`: User logins, station view navigation, background job ticks.
  - `WARNING`: High sensor values exceeding normal bands, telemetry jitter, retry attempts.
  - `ERROR`: SATCOM link drops, failed database transactions, unhandled route exceptions.
  - `CRITICAL`: Life-safety P0 alert triggers, generator failure events, audit log write failures.

### 4.3 Immutable Audit Logging (Constraint C7)
All security-critical actions are recorded in the PostgreSQL `audit_logs` table:
- User authentication events (successful login, failed login, session termination).
- Station command issuances (`commands` and `command_executions`).
- Manual threshold modifications or alarm acknowledgments.
- Access denials / permission violations.

---

## 5. Failure Modes & Polar Contingency Protocols

### 5.1 Scenario 1: SATCOM Link Outage (Antarctic Blackout)
- **Symptom:** The station loses all communication with NCPOR HQ in Goa due to auroral ionospheric disturbance or antenna radome icing.
- **System Behavior:**
  1. The station-side digital twin continues operating in autonomous local mode.
  2. Telemetry ingestion writes to the local store-and-forward write buffer (`infrastructure/resilience/in_process_write_buffer.py`).
  3. HQ portal displays a visual "Stale Data / Link Severed" banner with the exact timestamp of the last verified reading.
  4. Upon SATCOM restoration, the write buffer flushes backlogged readings to HQ in chronological sequence with `reading_quality = 'GOOD'`.

### 5.2 Scenario 2: Cloud Database Latency Spikes
- **Symptom:** Supabase query response time exceeds 1500 ms due to cloud network routing.
- **System Behavior:**
  1. SQLAlchemy connection pool (`pool_size=10`, `max_overflow=20`) prevents connection starvation.
  2. SSE stream endpoints yield cached latest state without blocking on slow table queries.
  3. Connection timeouts are capped at 5000 ms, after which graceful error degradation triggers.

### 5.3 Scenario 3: Life-Safety Power Microgrid Trip (P0 Event)
- **Symptom:** Main diesel genset drops offline; emergency battery bank activates.
- **System Behavior:**
  1. Telemetry ingestion immediately flags `battery_soc_pct < 20%` or `power_kw == 0`.
  2. Alert engine triggers a `P0 (CRITICAL)` record in `active_alerts`.
  3. Server-Sent Events push the alert instantly to all connected operator portals.
  4. Station SVG twin displays a persistent pulsing red glow on `hotspot-power_plant`.
