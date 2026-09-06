# GEMINI.md — DTFIAS Agent Reference
> **Digital Twin for Indian Antarctic Stations (SIH26060)**  
> **This file is the canonical behavioral contract for Google Antigravity, Gemini Code, and equivalent AI coding agents working on this repository.**  
> Companion to `docs/architecture.md` (structural authority) and `docs/database.md` (schema authority).  
> RFC 2119-style language throughout — MUST / MUST NOT / SHOULD.  
> See also: `CLAUDE.md` (same rules, Claude-flavored formatting).

---

## 0. Before You Touch Anything

1. Read `docs/architecture.md` **in full** before creating or moving any file — locate the correct layer first.
2. Read `docs/database.md` **in full** before writing any SQL, ORM model, or migration.
3. Read `.agents/<domain>/SKILL.md` for the relevant domain before implementing.
4. Never write raw SQL via f-strings — SQLAlchemy ORM/parameterized queries only (C8).
5. Never modify `.env` silently. If `DATABASE_URL` appears broken (e.g., `db.https://` prefix, wrong key type), **flag it** to the developer and stop.
6. Run the Definition-of-Done checklist (`docs/architecture.md §11`) before considering any layer complete.

---

## 1. Project Identity

| Key | Value |
|-----|-------|
| **Name** | DTFIAS — Digital Twin for Indian Antarctic Stations |
| **Event** | Smart India Hackathon 2026 (SIH26060) |
| **Backend** | Python 3.12+ · FastAPI · async SQLAlchemy (asyncpg driver) |
| **Database** | Supabase-hosted PostgreSQL (cloud, no local DB required) |
| **Auth system** | Supabase Auth (`auth.users`) — application RBAC in `public` schema |
| **Frontend** | Server-rendered Jinja2 + Tailwind CSS (CDN) + Alpine.js + HTMX + ApexCharts |
| **3D layer** | Three.js — lazy-loaded only, never in base template |
| **Entry point** | `main.py` → `uvicorn main:app --reload` |
| **Port** | 8000 (local) / 8000 (Docker) |

---

## 2. Four-Layer Architecture

This project is intentionally layered. Violating layer boundaries is treated as a blocking bug.

```
┌─────────────────────────────────────────────────────────────────┐
│  app/           INTERFACE LAYER                                  │
│  FastAPI routes, Pydantic schemas, Jinja2 templates, ORM models │
│  May import: engine.services.portals.*, infrastructure.*, shared.*│
├─────────────────────────────────────────────────────────────────┤
│  engine/        DOMAIN LAYER  (pure Python — zero HTTP/DB deps) │
│  domain/, processing/, services/core, services/portals,          │
│  interfaces/ (Protocols)                                          │
│  May import: shared.*, stdlib, pydantic only                     │
├─────────────────────────────────────────────────────────────────┤
│  infrastructure/ IMPLEMENTATION LAYER                            │
│  Concrete DB adapters, security, resilience, realtime            │
│  May import: engine.interfaces.*, engine.domain.*, shared.*      │
├─────────────────────────────────────────────────────────────────┤
│  shared/        VOCABULARY LAYER                                 │
│  Enums, constants — used by 2+ layers above                      │
│  May import: stdlib, pydantic only                               │
└─────────────────────────────────────────────────────────────────┘
```

### Import Law (C1): engine/** must import ZERO of:
`fastapi` | `starlette` | `jinja2` | `sqlalchemy` | `asyncpg`

Verify with: `grep -rE "^(import|from) (fastapi|sqlalchemy|asyncpg|jinja2)" engine/`  
This MUST return zero matches at all times.

---

## 3. Full Repository Map

```
DTFIAS/
├── app/
│   ├── config/
│   │   ├── database.py       # async engine + session factory
│   │   ├── settings.py       # pydantic-settings, reads .env
│   │   └── templates.py      # Jinja2 environment
│   ├── middleware/
│   ├── models/               # SQLAlchemy ORM models (deviation: live here not infrastructure/)
│   ├── schemas/              # Pydantic V2 validation schemas
│   ├── routers/
│   │   ├── auth/
│   │   ├── maitri/           # router.py + dashboard, energy, environment, logistics, infrastructure, alerts
│   │   ├── bharati/          # mirrors maitri/
│   │   └── hq/               # router.py + dashboard, stations, alerts, commands, users, audit
│   ├── static/               # vendor JS (htmx, alpine, apexcharts), CSS, app JS
│   └── templates/            # layouts/, components/, auth/, maitri/, bharati/, hq/
├── engine/
│   ├── domain/users/
│   ├── processing/ingestion/ + pipeline.py
│   ├── services/core/        # EnergyService, AlertService, etc.
│   ├── services/portals/     # maitri_portal_service.py, bharati_portal_service.py, hq_portal_service.py
│   ├── interfaces/           # clock.py, repositories.py, write_buffer.py (Protocols)
│   └── simulation/
├── infrastructure/
│   ├── database/postgres/    # Active Supabase connections
│   ├── realtime/             # supabase_listener.py (server-side SSE fan-out)
│   ├── resilience/
│   └── security/             # audit logs, argon2 passwords, RBAC
├── shared/
│   ├── constants/
│   └── models/               # global Enums
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
│   ├── architecture.md       # structural authority — READ FIRST
│   ├── database.md           # schema authority — READ BEFORE ANY DB WORK
│   ├── databaseTables.md     # generated column-level table reference
│   └── 2dFrontend.md         # 2.5D station view implementation brief
├── scripts/
│   └── test_db_connection.py # quick connectivity test
├── .agents/
│   ├── database/SKILL.md     # Supabase/Postgres best practices
│   ├── fastapi/SKILL.md      # FastAPI + Pydantic V2 + async SQLAlchemy
│   ├── frontend/SKILL.md     # Complete frontend design guidelines
│   └── brand_design/SKILL.md # Brand colors + typography
├── main.py                   # FastAPI app entry point
├── .env                      # Local secrets — never commit
├── .env.example              # Template — commit this, not .env
├── CLAUDE.md                 # Agent reference (Claude flavor)
├── GEMINI.md                 # Agent reference (Gemini flavor)
└── requirements.txt
```

---

## 4. Hard Constraints

> These are checked mechanically. Violating any is a **blocking bug**.

| Code | Constraint |
|------|-----------|
| **C1** | `engine/**` imports ZERO HTTP/DB libraries. Grep enforced. |
| **C2** | Station-scoped tables: `station_id station_id_enum NOT NULL` — Postgres enum, never text. |
| **C3** | `station_id` is set server-side only (class constant in portal services). Never from request body/params. |
| **C4** | `maitri_portal_service` and `bharati_portal_service` MUST NOT define `issue_command`, `manage_users`, or `view_audit`. Only `hq_portal_service` may. |
| **C5** | Role guards MUST be on the `APIRouter` via `dependencies=`, not per-endpoint. |
| **C6** | Argon2 only for password hashing. Never log plaintext — including debug. |
| **C7** | Every login, state write, command issuance, and permission denial → one `audit_log` row. |
| **C8** | All SQL via SQLAlchemy ORM/parameterized queries. Zero f-string SQL construction. |
| **C9** | `shared/**` only contains code used by 2+ of {`engine`, `app`, `infrastructure`}. |
| **C10** | Session cookies: `httponly=True`, `secure=True`, `samesite="strict"`. |
| **C11** | CSRF tokens verified on every POST/PUT/DELETE. |
| **C13** | Supabase service-role key: backend env vars only. Never in `app/static/` or `app/templates/`. |
| **C14** | Supabase Realtime: server-side only (`infrastructure/realtime/supabase_listener.py`). No `supabase-js` Realtime in browser. |
| **C15** | RLS is NOT the access control mechanism. Only backend connects to Postgres. RLS = disabled/default-deny. |
| **C16** | Three.js/`station_3d_view.js`: lazy-loaded only. Never in `layouts/base.html` unconditional scripts. |
| **C17** | Tailwind via CDN: `<script src="https://cdn.tailwindcss.com">`. No npm build pipeline. |

---

## 5. Database Schema

### Connection String Format
```
postgresql+asyncpg://postgres:<DB_PASSWORD>@db.<PROJECT_REF>.supabase.co:5432/postgres
```

> **Common mistake**: Using the `sb_publishable_*` anon API key as the DB password. This is **wrong** — it will fail authentication. The DB password is found at: Supabase Dashboard → Project Settings → Database → URI (the `[YOUR-PASSWORD]` part).

> **Common mistake**: Including `https://` in the host. The host is `db.<PROJECT_REF>.supabase.co`, not `db.https://<PROJECT_REF>.supabase.co`.

### Postgres ENUMs (define before tables)
```sql
CREATE TYPE station_id_enum AS ENUM ('maitri', 'bharati');
CREATE TYPE role_enum AS ENUM ('maitri_operator', 'bharati_operator', 'hq_operator', 'hq_admin');
CREATE TYPE alert_severity_enum AS ENUM ('info', 'warning', 'critical');
CREATE TYPE command_state_enum AS ENUM ('SENT','RECEIVED','EXECUTING','EXECUTED','REJECTED','FAILED');
```

### DTFIAS Full Domain Map

| Domain | Tables |
|--------|--------|
| AUTH | `auth.users` (Supabase-managed), `profiles` (1:1 FK) |
| RBAC | `roles`, `permissions`, `user_roles`, `role_permissions`, `station_access` |
| STATIONS | `stations`, `station_areas` |
| PERSONNEL | `personnel`, `station_assignments`, `personnel_health_status` |
| ASSETS | `assets`, `asset_status_history` |
| SENSORS | `sensors`, `sensor_configurations` |
| TELEMETRY | `energy_readings`, `environment_readings`, `asset_readings` (30-day rolling) |
| ENERGY | `energy_systems`, `energy_sources`, `energy_assets` |
| LOGISTICS | `inventory_items`, `inventory`, `inventory_transactions`, `shipments`, `shipment_items` |
| MAINTENANCE | `maintenance_records`, `maintenance_events` |
| COMMANDS | `commands`, `command_executions` |
| ALERTS | `alert_rules`, `active_alerts` |
| AUDIT | `audit_logs` |

### Key roles (RBAC seed data)
`SUPER_ADMIN` | `HQ_ADMIN` | `HQ_OPERATOR` | `STATION_ADMIN` | `STATION_OPERATOR` | `ENGINEER` | `SCIENTIST` | `VIEWER`

### Key permissions (permission codes)
```
station.read   station.manage   asset.read     asset.manage
personnel.read personnel.manage health.read    health.manage
energy.read    energy.manage    logistics.read logistics.manage
maintenance.read maintenance.manage telemetry.read
command.create command.execute  alert.read     alert.manage  audit.read
```

---

## 6. FastAPI Implementation Guide

### Skill reference: `.agents/fastapi/SKILL.md` (read before implementing any endpoint)

### Canonical Pattern (schema + endpoint + CRUD)

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, field_validator, model_config

class UserCreate(BaseModel):
    model_config = model_config(str_strip_whitespace=True)
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

class UserResponse(BaseModel):
    model_config = model_config(from_attributes=True)
    id: int
    email: EmailStr
```

```python
# app/routers/auth/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.config.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app import crud

router = APIRouter(prefix="/users", tags=["users"])
DbDep = Annotated[AsyncSession, Depends(get_db)]

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: DbDep) -> UserResponse:
    existing = await crud.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    return await crud.create_user(db, payload)
```

### What MUST be true
- All I/O: `async`/`await`
- All type hints present
- Pydantic V2 syntax only (`field_validator` not `@validator`, `model_config` not `class Config`)
- `X | None` not `Optional[X]`
- Dependency injection via `Annotated` pattern
- RBAC guard on `APIRouter`, not per-endpoint
- HTTP status codes are semantically correct

### What MUST NOT happen
- Synchronous DB calls
- Pydantic V1 syntax
- Hardcoded secrets or config values in code
- f-string SQL construction (C8)
- Per-endpoint role decorators instead of router-level (C5)

---

## 7. Frontend Implementation Guide

### Skill reference: `.agents/frontend/SKILL.md` (read before any frontend work)

### Mandatory base template scripts (C17, no exceptions)
```html
<script src="/static/vendor/htmx.min.js"></script>
<script src="/static/vendor/htmx-ext-sse.js"></script>
<script src="/static/vendor/alpine.min.js" defer></script>
<script src="/static/vendor/apexcharts.min.js"></script>
<script src="https://cdn.tailwindcss.com"></script>
```

### Lazy Three.js (C16 — required pattern)
```html
<div id="station-3d-container" x-data
     x-init="
       const s = document.createElement('script');
       s.src = '/static/js/three/station_3d_view.js';
       s.onload = () => initStation3D('station-3d-container');
       document.body.appendChild(s);
     "></div>
```

### Live chart (ApexCharts + HTMX SSE — no Supabase client in browser)
```html
<div id="energy-chart" hx-ext="sse" sse-connect="/maitri/energy/stream"></div>
<script>
  const chart = new ApexCharts(document.querySelector("#energy-chart"), {
    chart: { type: "line", animations: { enabled: true } },
    series: [{ name: "Battery SoC %", data: [] }],
  });
  chart.render();
  document.body.addEventListener("htmx:sseMessage", (e) => {
    const reading = JSON.parse(e.detail.data);
    chart.appendData([{ data: [reading.battery_soc_pct] }]);
  });
</script>
```

### Brand Design System (`.agents/brand_design/SKILL.md`)

```css
:root {
  /* Main palette */
  --color-dark:       #141413;
  --color-light:      #faf9f5;
  --color-mid-gray:   #b0aea5;
  --color-light-gray: #e8e6dc;

  /* Accents */
  --color-accent-orange: #d97757;
  --color-accent-blue:   #6a9bcc;
  --color-accent-green:  #788c5d;

  /* Typography */
  --font-heading: 'Poppins', Arial, sans-serif;
  --font-body:    'Lora', Georgia, serif;
}
```

### Frontend Design Rules (from `.agents/frontend/SKILL.md`)
- **BOLD aesthetic direction** — commit to one and execute precisely; no generic "modern SaaS" look
- Mobile-first responsive patterns throughout
- Animations: CSS transforms/opacity only (no layout thrash)
- P0 alerts: persistent CSS pulse; P1: color change only; P2: no animation
- Staleness: dimmed hotspot + "last updated Xm ago" label — this is the project's technical differentiator

---

## 8. SSE / Realtime Architecture

**Option A (default — use this):**  
`app/routers/maitri/energy.py` `/stream` endpoint polls `EnergyRepository.latest()` on a short interval inside a `StreamingResponse` generator. Yields SSE event when value changes.

**Option B (optional upgrade only if Option A is genuinely insufficient):**  
`infrastructure/realtime/supabase_listener.py` subscribes to Postgres changes using the service-role key (server-side only, C14). `broadcaster.py` pushes to open SSE connections.

> C14 is absolute: NO supabase-js Realtime subscription from the browser under any circumstances.

---

## 9. 2.5D Station View (SIH Demo Feature)

### Reference: `docs/2dFrontend.md` (full implementation brief)

| Item | Specification |
|------|--------------|
| MVP station | Bharati (first) — then Maitri as config change |
| Component | Station-agnostic: `<StationTwin stationId="bharati" />` |
| SVG hotspot naming | `hotspot-{asset-slug}` (kebab-case, stable IDs) |
| Interactivity | Inline SVG only (not `<img>`) — requires DOM access |
| P0 alert visual | Persistent CSS pulse animation |
| P1 alert visual | Color change, no animation |
| Staleness indicator | Dimmed hotspot + "last updated Xm ago" label |

**Required asset IDs:** `main_building`, `power_plant`, `fuel_storage`, `hvac`, `comms_satcom`, `medical_bay`, `personnel_roster`, `environment_sensors`, `heliport` (Bharati only), `vehicle_fleet`

**NOT in scope:** AGEOS / ISRO X-S band earth station (separate infrastructure, out of scope per project docs)

---

## 10. Skills Reference

| Domain | Skill file | When to load |
|--------|-----------|-------------|
| Database / Postgres | `.agents/database/SKILL.md` | ANY SQL, schema, migrations, RLS, indexes, query performance, connection issues |
| FastAPI backend | `.agents/fastapi/SKILL.md` | Endpoints, Pydantic schemas, async DB, JWT/OAuth2, WebSockets, OpenAPI |
| Frontend | `.agents/frontend/SKILL.md` | All HTML/CSS/JS — aesthetics, mobile, animations, data visualization |
| Brand / design | `.agents/brand_design/SKILL.md` | Visual design, color palette, typography |

---

## 11. Naming Conventions

| Artifact | Convention | Example |
|----------|-----------|---------|
| Python files | `snake_case.py` | `energy_service.py` |
| Classes | `PascalCase` | `EnergyReading` |
| Service methods | verb-first | `create_command`, `acknowledge_alert` |
| Repository methods | fixed vocabulary | `save`, `latest`, `history`, `get_by_station_id` |
| Test files | mirror source | `tests/unit/engine/services/test_energy_service.py` |
| Pydantic schemas | `{Model}Create`, `{Model}Response`, `{Model}Update` | `CommandCreate` |
| Router prefixes | domain nouns | `/auth`, `/maitri`, `/bharati`, `/hq` |
| SQLAlchemy models | singular | `User`, `EnergyReading`, `AuditLog` |

---

## 12. Testing Contracts

```bash
# Run all tests
pytest

# Unit tests only
pytest tests/unit/

# Integration (requires live DB)
pytest tests/integration/

# E2E
pytest tests/e2e/
```

### After every endpoint group:
1. `pytest` passes
2. `/docs` (Swagger UI) reflects correct API surface
3. Schemas validate expected inputs/outputs

### Special E2E checks:
- If Option B (Realtime) is used: `test_realtime_never_reaches_wrong_role.py` — Bharati-tagged DB change must NEVER appear on Maitri SSE stream
- 3D loader: Lighthouse/manual check — `station_3d_view.js` must be absent from initial page waterfall

---

## 13. Definition of Done Checklist

Before any layer is considered complete:

```bash
# C13 — no service-role key in frontend
grep -r "SUPABASE_SERVICE_ROLE_KEY" app/static/ app/templates/   # → zero results

# C14 — no supabase-js Realtime in browser
grep -r "supabase-js\|createClient(" app/static/ app/templates/  # → zero results

# C1 — engine layer purity
grep -rE "^(import|from) (fastapi|sqlalchemy|asyncpg|jinja2)" engine/  # → zero results
```

And manually verify:
- [ ] New SSE route: events scoped to requesting session's `station_id`/role only
- [ ] Any new Three.js asset: absent from `base.html`, lazy-loaded via `x-init`
- [ ] New station-scoped tables: `station_id` is enum type, set server-side, never from request
- [ ] Every state-changing endpoint: writes `audit_log` row (C7)
- [ ] All passwords: argon2-hashed, never logged (C6)
- [ ] All cookies: `httponly`, `secure`, `samesite=strict` (C10)
- [ ] CSRF verified on all POST/PUT/DELETE (C11)
- [ ] All `pytest` tests pass

---

## 14. Quick Start

```bash
# 1. Create virtual environment
python -m venv .venv
.venv\Scripts\activate     # Windows
# source .venv/bin/activate # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env: set DATABASE_URL with real Postgres password from Supabase dashboard

# 4. Test database connection
python scripts/test_db_connection.py

# 5. Start dev server
uvicorn main:app --reload

# 6. Access
#   App:    http://localhost:8000
#   Docs:   http://localhost:8000/docs
#   ReDoc:  http://localhost:8000/redoc
```

### Docker alternative
```bash
docker compose up --build
```

---

## 15. Common Gotchas

| Symptom | Root cause | Fix |
|---------|-----------|-----|
| `InvalidPasswordError: password authentication failed` | `DATABASE_URL` contains anon API key (`sb_publishable_*`) not DB password | Get DB password from Supabase Dashboard → Project Settings → Database → URI |
| `invalid connection string` | `db.https://` in host or missing `+asyncpg` driver | Fix to `postgresql+asyncpg://postgres:<PW>@db.<REF>.supabase.co:5432/postgres` |
| Engine layer import error | `engine/` importing SQLAlchemy/FastAPI | Move concrete implementation to `infrastructure/`, keep only Protocols in `engine/interfaces/` |
| RBAC guard not working | Per-endpoint `Depends(require_role(...))` instead of router-level `dependencies=` | Move guard to `APIRouter(..., dependencies=[Depends(require_role(...))])` |
| Tailwind not applying | Tried to use npm/PostCSS build | Use CDN only: `<script src="https://cdn.tailwindcss.com">` (C17) |
| Three.js blocks page load | Added to `base.html` script tags | Move to lazy `x-init` pattern (C16) |
| SSE leaks cross-station data | SSE endpoint not scoped by session role/station_id | Scope `StreamingResponse` generator to `current_user.station_id` |
