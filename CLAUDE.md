# CLAUDE.md — DTFIAS Agent Reference
> **Digital Twin for Indian Antarctic Stations (SIH26060)**  
> **This file is the canonical behavioral contract for Claude Code and all AI coding agents working on this repository.**  
> Pair with `docs/architecture.md` (structural authority) and `docs/database.md` (schema authority).  
> RFC 2119-style language throughout — MUST / MUST NOT / SHOULD.

---

## 0. Before You Touch Anything

1. Read `docs/architecture.md` **before** creating or moving any file.
2. Read `docs/database.md` **before** writing any SQL or ORM model.
3. Read the relevant `.agents/<domain>/SKILL.md` **before** implementing in that domain.
4. Run the Definition-of-Done checklist in `docs/architecture.md §11` before marking a layer "done".
5. Never modify `.env` — it may contain secrets. If the `DATABASE_URL` is broken, flag it; don't silently write a new one.

---

## 1. Project Identity

| Key | Value |
|-----|-------|
| **Project name** | DTFIAS — Digital Twin for Indian Antarctic Stations |
| **Competition** | Smart India Hackathon 2026 (SIH26060) |
| **Backend** | FastAPI + async SQLAlchemy (asyncpg) |
| **Database** | Supabase-hosted PostgreSQL |
| **Auth** | Supabase Auth (`auth.users`) — no custom password table |
| **Frontend** | Jinja2 templates + Tailwind CSS (CDN) + Alpine.js + HTMX + ApexCharts |
| **3D view** | Three.js (lazy-loaded only — never in base template) |
| **Python** | >=3.12, async-first throughout |
| **Entry point** | `main.py` -> `uvicorn main:app` |

---

## 2. Repository Layout (Non-Negotiable)

```
DTFIAS/
├── app/          # LAYER: interface — FastAPI, HTTP, ORM, Config, Templates
│   ├── config/   # settings.py, database.py, templates.py
│   ├── middleware/
│   ├── models/   # SQLAlchemy ORM models (currently here, not in infrastructure/)
│   ├── schemas/  # Pydantic v2 validation schemas
│   ├── routers/  # auth/, maitri/, bharati/, hq/
│   ├── static/
│   └── templates/
├── engine/       # LAYER: domain — pure Python, ZERO external imports (see C1)
│   ├── domain/
│   ├── processing/
│   ├── services/
│   │   ├── core/
│   │   └── portals/   # maitri_portal_service.py, bharati_portal_service.py, hq_portal_service.py
│   └── interfaces/    # Protocol definitions only
├── infrastructure/ # LAYER: implementations of engine/interfaces
│   ├── database/postgres/
│   ├── resilience/
│   ├── security/
│   └── realtime/
├── shared/       # LAYER: code used by 2+ of the above layers
├── tests/        # unit/, integration/, e2e/
├── docs/         # architecture.md, database.md, databaseTables.md, 2dFrontend.md
├── scripts/      # DB migrations, seeding, test scripts
├── .agents/      # AI agent skills (read these before working in each domain)
├── main.py
├── pyproject.toml
└── requirements.txt
```

---

## 3. Hard Constraints (Checked Mechanically)

| Code | Rule |
|------|------|
| **C1** | `engine/**` MUST NOT import `fastapi`, `starlette`, `jinja2`, `sqlalchemy`, `asyncpg`, or any HTTP/DB library. `grep -rE "^(import|from) (fastapi|sqlalchemy|asyncpg|jinja2)" engine/` MUST return zero matches. |
| **C2** | Every station-scoped table MUST have `station_id station_id_enum NOT NULL` — Postgres native enum, never free text. |
| **C3** | `station_id` MUST be set server-side only, hard-coded as a class constant in the portal service files. MUST NOT be read from request body, query params, or any client-supplied field. |
| **C4** | `maitri_portal_service.py` / `bharati_portal_service.py` MUST NOT define `issue_command`, `manage_users`, or `view_audit`. Only `hq_portal_service.py` may. |
| **C5** | Every `APIRouter` under `app/routers/<portal>/` MUST declare its role guard via `dependencies=`, NOT per-endpoint decorators. |
| **C6** | Passwords MUST be hashed with argon2 (`infrastructure/security/authentication/passwords.py`). MUST NOT log or store plaintext. |
| **C7** | Every login, state write, command issuance, and permission denial MUST produce one `audit_log` row. |
| **C8** | All SQL access MUST go through SQLAlchemy ORM/parameterized queries. MUST NOT build raw SQL via string concatenation or f-strings. |
| **C9** | `shared/**` MUST contain only code imported by 2+ of {`engine`, `app`, `infrastructure`}. |
| **C10** | Session cookies MUST be `httponly=True`, `secure=True`, `samesite="strict"`. |
| **C11** | CSRF tokens MUST be verified on every `POST`/`PUT`/`DELETE` route. |
| **C13** | The Supabase **service-role key** MUST exist only in backend env vars. MUST NOT appear in `app/static/`, `app/templates/`, or any response body. |
| **C14** | Supabase Realtime subscriptions MUST originate server-side only. Client-side `supabase-js` Realtime from the browser is **FORBIDDEN**. |
| **C15** | Row-Level Security (RLS) is NOT part of this project's access control model. Leave RLS disabled/default-deny. |
| **C16** | `app/static/js/three/` MUST be loaded lazily. NEVER include in `layouts/base.html` unconditional script tags. |
| **C17** | Tailwind MUST be loaded via CDN: `<script src="https://cdn.tailwindcss.com">`. No Node/npm build pipeline. |

---

## 4. Layer Import Rules

| Layer | May import | MUST NOT import |
|-------|------------|-----------------|
| `app/**` | `engine.services.portals.*`, `infrastructure.*`, `shared.*` | bypassing portal services |
| `engine/domain`, `engine/rules`, `engine/processing` | `shared.*`, stdlib, `pydantic` | `engine.services`, `infrastructure.*`, `app.*` |
| `engine/services/core` | `engine.domain.*`, `engine.rules.*`, `engine.processing.*`, `engine.interfaces.*`, `shared.*` | `infrastructure.*` (interfaces only), `app.*` |
| `engine/services/portals` | `engine.services.core.*`, `engine.interfaces.*`, `shared.*` | `infrastructure.*`, `app.*` |
| `engine/interfaces` | stdlib, `typing.Protocol`, `engine.domain.*` | everything else |
| `infrastructure/**` | `engine.interfaces.*`, `engine.domain.*`, `shared.*`, DB/HTTP libs | `app.*` |
| `shared/**` | stdlib, `pydantic` | `engine.*`, `infrastructure.*`, `app.*` |

---

## 5. Database — Supabase PostgreSQL

### Connection
- **Auth**: Supabase Auth manages `auth.users` — do NOT create custom password tables
- **Driver**: `postgresql+asyncpg://` for async SQLAlchemy
- **Pooling**: Use Transaction-mode pooled URI to avoid connection exhaustion
- **Config**: `DATABASE_URL` in `.env` -> read by `app/config/settings.py` -> used by `app/config/database.py`
- **Password**: Must be the actual Postgres database password (from Supabase Dashboard > Project Settings > Database > URI). NOT the `sb_publishable_*` anon API key.

### Key Postgres ENUMs
```sql
station_id_enum: 'maitri' | 'bharati'
role_enum: 'maitri_operator' | 'bharati_operator' | 'hq_operator' | 'hq_admin'
alert_severity_enum: 'info' | 'warning' | 'critical'
command_state_enum: 'SENT' | 'RECEIVED' | 'EXECUTING' | 'EXECUTED' | 'REJECTED' | 'FAILED'
```

### Domain Map (see `docs/database.md` for full detail)
- **AUTH**: `auth.users` (Supabase-managed) -> `profiles` (1:1)
- **RBAC**: `roles`, `permissions`, `user_roles`, `role_permissions`, `station_access`
- **STATIONS**: `stations`, `station_areas`
- **PERSONNEL**: `personnel`, `station_assignments`, `personnel_health_status`
- **ASSETS**: `assets`, `asset_status_history`
- **SENSORS**: `sensors`, `sensor_configurations`
- **TELEMETRY**: `energy_readings`, `environment_readings`, `asset_readings` (30-day rolling)
- **ENERGY**: `energy_systems`, `energy_sources`, `energy_assets`
- **LOGISTICS**: `inventory_items`, `inventory`, `inventory_transactions`, `shipments`, `shipment_items`
- **MAINTENANCE**: `maintenance_records`, `maintenance_events`
- **COMMANDS**: `commands`, `command_executions`
- **ALERTS**: `alert_rules`, `active_alerts`
- **AUDIT**: `audit_logs`

### ORM/Schema Rules
- All SQLAlchemy ORM models: `app/models/`
- All Pydantic schemas: `app/schemas/`
- All CRUD: service/CRUD files, never inline in routers
- Timestamps: always `TIMESTAMPTZ`, always timezone-aware (`datetime.now(timezone.utc)`, never naive)

---

## 6. FastAPI Patterns

### Skill: `.agents/fastapi/SKILL.md`

### MUST
- Type hints everywhere
- Pydantic V2: `field_validator`, `model_validator`, `model_config`
- `Annotated` DI pattern: `DbDep = Annotated[AsyncSession, Depends(get_db)]`
- `async`/`await` for ALL I/O
- `X | None` instead of `Optional[X]`
- Router-level role guards: `dependencies=[Depends(require_role("maitri_operator"))]`

### MUST NOT
- Synchronous database operations
- Pydantic V1 syntax (`@validator`, `class Config`)
- Hardcoded config values (use `app/config/settings.py`)
- Per-endpoint role checks (must be on router, not endpoint)

### RBAC Pattern
```python
# app/dependencies/permissions.py
def require_role(*allowed_roles: str):
    def _check(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")  # audit first (C7)
        return user
    return _check

# app/routers/maitri/router.py
router = APIRouter(prefix="/maitri", dependencies=[Depends(require_role("maitri_operator"))])
```

---

## 7. Frontend Stack

### Skill: `.agents/frontend/SKILL.md`

### Always in base template:
```html
<script src="/static/vendor/htmx.min.js"></script>
<script src="/static/vendor/htmx-ext-sse.js"></script>
<script src="/static/vendor/alpine.min.js" defer></script>
<script src="/static/vendor/apexcharts.min.js"></script>
<script src="https://cdn.tailwindcss.com"></script>
```

### Never in base template: `three.module.js`, `supabase-js`, any Supabase client

### Brand colors (`.agents/brand_design/SKILL.md`):
| Token | Hex | Use |
|-------|-----|-----|
| Dark | `#141413` | Primary text, dark backgrounds |
| Light | `#faf9f5` | Light backgrounds |
| Mid Gray | `#b0aea5` | Secondary elements |
| Light Gray | `#e8e6dc` | Subtle backgrounds |
| Orange | `#d97757` | Primary accent |
| Blue | `#6a9bcc` | Secondary accent |
| Green | `#788c5d` | Tertiary accent |

### Typography:
- Headings: **Poppins** (fallback: Arial)
- Body: **Lora** (fallback: Georgia)

---

## 8. Skills Catalog

| Skill | Path | Trigger |
|-------|------|---------|
| `supabase-postgres-best-practices` | `.agents/database/SKILL.md` | Any SQL, schema, migration, RLS, index, or query performance work |
| `fastapi-expert` | `.agents/fastapi/SKILL.md` | Any endpoint, schema, async DB, JWT, or WebSocket work |
| `frontend-design-complete` | `.agents/frontend/SKILL.md` | All frontend — CSS, animations, mobile, data viz |
| `brand-guidelines` | `.agents/brand_design/SKILL.md` | Visual design, brand colors, typography |

---

## 9. Naming Conventions

| Artifact | Convention |
|----------|------------|
| Files | `snake_case.py` |
| Classes | `PascalCase` |
| Service methods | verb-first: `create_user`, `issue_command` |
| Repository methods | `save` / `latest` / `history` / `get_by_*` |
| Test files | mirror source path under `tests/` |
| Pydantic schemas | `{Model}Create`, `{Model}Response`, `{Model}Update` |
| Router prefixes | `/auth`, `/maitri`, `/bharati`, `/hq` |

---

## 10. Definition of Done Checklist

- [ ] `grep -r "SUPABASE_SERVICE_ROLE_KEY" app/static/ app/templates/` → zero results (C13)
- [ ] `grep -r "supabase-js\|createClient(" app/static/ app/templates/` → zero results (C14)
- [ ] `grep -rE "^(import|from) (fastapi|sqlalchemy|asyncpg|jinja2)" engine/` → zero results (C1)
- [ ] New SSE route scoped to requesting session's `station_id`/role only
- [ ] Three.js assets: absent from `base.html`, lazy-loaded only
- [ ] All station-scoped tables: `station_id` is enum, set server-side only
- [ ] Every state-changing endpoint: writes `audit_log` row (C7)
- [ ] All passwords: argon2-hashed, never logged (C6)
- [ ] All cookies: `httponly`, `secure`, `samesite=strict` (C10)
- [ ] CSRF verified on all POST/PUT/DELETE (C11)
- [ ] `pytest` passes on all modified paths

---

## 11. Running the Project

```bash
# Local dev (Windows)
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Test DB connection
python scripts/test_db_connection.py

# Docker
docker compose up --build
```

URLs: `http://localhost:8000` | `http://localhost:8000/docs` | `http://localhost:8000/redoc`
