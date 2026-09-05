# architecture.md — Antarctic Digital Twin (SIH26060)

**Revision 5 — Final.** Structural contract for AI coding agents
(Google Antigravity, Claude Code, or equivalent) and human engineers.
RFC 2119-style language (MUST / MUST NOT / SHOULD) throughout —
written to be checked mechanically, not just read.

**What changed from Revision 4:** database moved from MySQL to
**Supabase-hosted Postgres**; frontend stack now explicitly **Tailwind
CSS + Alpine.js + HTMX + ApexCharts + optional lazy-loaded Three.js**.
Everything else (layering, RBAC, portal segregation, engine purity)
is unchanged and still load-bearing.

**Companion file:** pair this with `AGENTS.md` at the repo root for
behavioral rules (commit style, lint, test commands). This file is the
structural authority — file placement, ownership, interfaces.

---

## 0. How an Agent Should Use This Document

1. Before creating any file, locate its layer in Section 2 and confirm
   planned imports against Section 3. Wrong imports mean wrong layer —
   move the file, don't add the import.
2. Before implementing a service method, check Section 5 for an
   existing signature. Implement to it exactly. If none exists, add it
   to this document in the same change as the implementation.
3. Before adding a route, confirm it sits under an `APIRouter` with the
   correct `dependencies=[Depends(require_role(...))]` already applied
   (Section 6). Do not substitute a per-endpoint check for the
   router-level guard.
4. Before adding anything under `app/static/js/three/`, confirm it is
   wired to load lazily (Section 7) — never added to the base template's
   unconditional `<script>` tags.
5. Run the Section 11 checklist before considering any layer "done."

---

## 1. Non-Negotiable Constraints

| # | Constraint |
|---|---|
| C1 | `engine/**` MUST NOT import `fastapi`, `starlette`, `jinja2`, `sqlalchemy`, `asyncpg`, or any HTTP/DB library. `grep -rE "^(import\|from) (fastapi\|sqlalchemy\|asyncpg\|jinja2)" engine/` MUST return zero matches. |
| C2 | Every station-scoped table MUST have `station_id station_id_enum NOT NULL` (Postgres native enum type — see Section 8), never free text. |
| C3 | `station_id` MUST be set server-side only, hard-coded as a class constant in `engine/services/portals/{maitri,bharati}_portal_service.py`. MUST NOT be read from request body, query params, or any client-supplied field. |
| C4 | `maitri_portal_service.py` / `bharati_portal_service.py` MUST NOT define `issue_command`, `manage_users`, or `view_audit`. Only `hq_portal_service.py` may. |
| C5 | Every `APIRouter` under `app/routers/<portal>/` MUST declare its role guard via `dependencies=`, not per-endpoint decorators. |
| C6 | Passwords MUST be hashed with argon2 (`infrastructure/security/authentication/passwords.py`). MUST NOT log or store plaintext, ever, including debug logs. |
| C7 | Every login, state write, command issuance, and permission denial MUST produce one `audit_log` row. |
| C8 | All SQL access MUST go through SQLAlchemy ORM/parameterized queries. MUST NOT build raw SQL via string concatenation or f-strings anywhere. (Note: Models currently reside in `app/models/` instead of `infrastructure/`). |
| C9 | `shared/**` MUST contain only code imported by 2+ of {`engine`, `app`, `infrastructure`}. Single-importer code moves into that layer. |
| C10 | Session cookies MUST be `httponly=True`, `secure=True`, `samesite="strict"`. |
| C11 | CSRF tokens MUST be verified on every `POST`/`PUT`/`DELETE` route. |
| C12 | `app/main.py` MUST set `templates.env.auto_reload = False` only when `config.ENV == "production"`. |
| C13 | The Supabase **service-role key** MUST exist only in backend environment variables (read via `app/config/settings.py`). It MUST NOT appear in any file under `app/static/`, `app/templates/`, or any response body/template context, ever. |
| C14 | If Supabase Realtime is used at all (Section 7), the subscription MUST originate server-side (`infrastructure/realtime/supabase_listener.py`, service-role key) and be re-broadcast to browsers only through FastAPI's own RBAC-aware SSE endpoint. Client-side `supabase-js` Realtime subscriptions from the browser are FORBIDDEN — there is no Supabase Auth session to scope them by role. |
| C15 | Row-Level Security (RLS) on Supabase tables is NOT part of this project's access-control model — only the backend connects directly to Postgres, using a role with full table access. Leave RLS disabled or default-deny; do not rely on it, and do not assume enabling it adds protection here (it protects against a client connecting directly, which never happens in this architecture). |
| C16 | Any script under `app/static/js/three/` MUST be loaded lazily (dynamic `<script>` injection triggered by opening the 3D view, or `hx-trigger="revealed"`) — never included in `layouts/base.html`'s unconditional script tags. |
| C17 | Tailwind MUST be loaded via the CDN `<script src="https://cdn.tailwindcss.com">` for this build (no Node/npm build pipeline) — consistent with the no-bundler approach already used for htmx/Alpine. |

---

## 2. Full Repository Layout

```
antarctic-digital-twin/
│
├── app/                                        # LAYER: interface (FastAPI, HTTP-only concerns, ORM, Config)
│   ├── main_router.py                          # Aggregates portal routers
│   ├── config/                                 # Configuration and settings
│   │   ├── database.py                         # Async session and engine config
│   │   ├── settings.py
│   │   └── templates.py
│   ├── middleware/                             # Logging, request ID, security
│   ├── models/                                 # SQLAlchemy ORM Models (deviation from Rev 4)
│   │   └── user.py, test.py
│   ├── schemas/                                # Pydantic validation schemas
│   │   └── user.py, test.py
│   ├── routers/
│   │   ├── auth/
│   │   ├── maitri/
│   │   │   ├── router.py                       # APIRouter instance
│   │   │   └── dashboard.py, energy.py, environment.py, logistics.py, infrastructure.py, alerts.py
│   │   ├── bharati/
│   │   │   └── (mirrors maitri/)
│   │   └── hq/
│   │       ├── router.py
│   │       └── dashboard.py, stations.py, alerts.py, commands.py, users.py, audit.py
│   ├── static/                                 # CSS (Tailwind) and JS (HTMX)
│   └── templates/                              # Jinja2 HTML templates
│       ├── layouts/
│       ├── components/
│       ├── auth/
│       └── maitri/, bharati/, hq/
│
├── engine/                                     # LAYER: domain (pure Python)
│   ├── domain/
│   │   └── users/                              # Core entity state definitions
│   ├── processing/
│   │   ├── ingestion/                          # Sanitization and deduplication
│   │   └── pipeline.py
│   ├── services/
│   │   ├── core/                               # Core services (energy, environment, etc.)
│   │   └── portals/                            # Portal-specific service facades
│   ├── interfaces/
│   │   └── clock.py, repositories.py, write_buffer.py
│   └── simulation/                             # Simulators and scenario runners
│
├── infrastructure/                             # LAYER: implementations of engine/interfaces
│   ├── database/
│   │   ├── mysql/                              # Legacy MySQL connections
│   │   └── postgres/                           # Active Supabase-hosted Postgres connections
│   ├── resilience/
│   └── security/                               # Audit logs, passwords, RBAC
│
├── shared/                                     # LAYER: shared vocabulary
│   ├── constants/                              # System-wide priorities and thresholds
│   └── models/                                 # Global Enums
│
├── tests/
│   ├── e2e/
│   ├── integration/
│   └── unit/
│
├── docs/                                       # Project documentation
├── scripts/                                    # DB migrations and seeding scripts
├── deployment/
├── main.py                                     # FastAPI application entry point
├── pyproject.toml
└── README.md
```


---

## 3. Allowed Imports Per Layer

| Layer | May import from | MUST NOT import from |
|---|---|---|
| `app/**` | `engine.services.portals.*`, `infrastructure.*`, `shared.*` | nothing bypasses `engine.services.portals` |
| `engine/domain`, `engine/rules`, `engine/processing` | `shared.*`, stdlib, `pydantic` | `engine.services`, `infrastructure.*`, `app.*` |
| `engine/services/core` | `engine.domain.*`, `engine.rules.*`, `engine.processing.*`, `engine.interfaces.*`, `shared.*` | `infrastructure.*` implementations (interfaces only), `app.*` |
| `engine/services/portals` | `engine.services.core.*`, `engine.interfaces.*`, `shared.*` | `infrastructure.*`, `app.*` |
| `engine/interfaces` | stdlib, `typing.Protocol`, `engine.domain.*` | everything else |
| `infrastructure/database`, `infrastructure/resilience`, `infrastructure/security` | `engine.interfaces.*`, `engine.domain.*`, `shared.*`, DB/HTTP libs | `app.*` |
| `infrastructure/realtime` | `shared.*`, Supabase server client, stdlib | `engine.*` (it operates on already-persisted data, purely for display fan-out — does not need domain logic) |
| `shared/**` | stdlib, `pydantic` | `engine.*`, `infrastructure.*`, `app.*` |

---

## 4. Domain Models — Field Contracts (unchanged from Rev. 4)

See Revision 4 field contracts for `EnergyState`, `EnvironmentState`,
`LogisticsState`, `InfrastructureState`, `Alert`, `Command`, `User` —
no fields changed by the database/frontend migration. Timestamps are
now `TIMESTAMPTZ`-backed at the Postgres layer (Section 8); the
Pydantic `datetime` fields are unaffected as long as values are
timezone-aware (`datetime.now(timezone.utc)`, never naive `datetime.now()`).

---

## 5. Interface (Port) and Service Signatures — Implement Exactly

Unchanged from Revision 4 (`EnergyRepository`, `AlertRepository`,
`CommandRepository`, `UserRepository`, `AuditRepository`,
`WriteBufferPort`, `EnergyService`, `MaitriPortalService`,
`HQPortalService` — see Section 5 of the prior revision for full
signatures). The Protocols don't change when the concrete database
underneath them changes from MySQL to Postgres — that's the entire
point of defining them as Protocols in `engine/interfaces/`.

One addition:

```python
# engine/interfaces/write_buffer.py — unchanged, but now also the queue
# type infrastructure/realtime/broadcaster.py uses internally for SSE
# fan-out ordering (P0 alerts broadcast before P1 telemetry, same Priority enum)
```

---

## 6. Router + RBAC Pattern (unchanged)

```python
# app/dependencies/permissions.py
def require_role(*allowed_roles: str):
    def _check(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")  # MUST audit first (C7)
        return user
    return _check
```

```python
# app/routers/maitri/router.py
router = APIRouter(prefix="/maitri", dependencies=[Depends(require_role("maitri_operator"))])
# In a real app, endpoints like dashboard, energy, etc. are registered here or imported.
```

---

## 7. Frontend Stack — Wiring Detail

**Base template (`app/templates/layouts/base.html`) loads, unconditionally:**
```html
<script src="/static/vendor/htmx.min.js"></script>
<script src="/static/vendor/htmx-ext-sse.js"></script>
<script src="/static/vendor/alpine.min.js" defer></script>
<script src="/static/vendor/apexcharts.min.js"></script>
<script src="https://cdn.tailwindcss.com"></script>   <!-- C17 -->
```
**Never included here:** `three.module.js` or `station_3d_view.js` (C16).

**Live chart pattern (ApexCharts + SSE, no Supabase client in the browser):**
```html
<!-- app/templates/components/live_chart.html -->
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

**Two options for driving `/maitri/energy/stream` — pick one, document
which in your README:**

- **Option A (default, simplest — recommended):** `app/routers/maitri/energy.py`'s
  `/stream` endpoint polls `EnergyRepository.latest()` on a short
  interval inside a `StreamingResponse` generator and yields an SSE
  event whenever the value changes. No dependency on Supabase Realtime
  at all — fewer moving parts, easiest to demo reliably.
- **Option B (optional upgrade):** `infrastructure/realtime/supabase_listener.py`
  subscribes to Postgres changes using the **service-role key**
  (server-side only, per C14), and `broadcaster.py` pushes to the same
  `/stream` SSE endpoint's open connections — removes polling latency,
  adds one more moving part (the listener process) to keep alive
  during the demo. Only adopt this if Option A's polling interval
  genuinely isn't responsive enough.

**3D view, lazy-loaded (C16):**
```html
<!-- app/templates/maitri/view_3d.html -->
<div id="station-3d-container" x-data
     x-init="
       const s = document.createElement('script');
       s.src = '/static/js/three/station_3d_view.js';
       s.onload = () => initStation3D('station-3d-container');
       document.body.appendChild(s);
     "></div>
```
This ensures `three.module.js` and `station_3d_view.js` are fetched
only when a user actually opens this page — the main dashboard's load
time is unaffected regardless of how elaborate the 3D view becomes.

---

## 8. Postgres Schema (Supabase-hosted)

```sql
CREATE TYPE station_id_enum AS ENUM ('maitri', 'bharati');
CREATE TYPE role_enum AS ENUM ('maitri_operator', 'bharati_operator', 'hq_operator', 'hq_admin');
CREATE TYPE alert_severity_enum AS ENUM ('info', 'warning', 'critical');
CREATE TYPE command_state_enum AS ENUM ('SENT','RECEIVED','EXECUTING','EXECUTED','REJECTED','FAILED');

CREATE TABLE users (
    id            BIGSERIAL PRIMARY KEY,
    username      VARCHAR(64) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role          role_enum NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    is_active     BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE energy_readings (
    id                BIGSERIAL PRIMARY KEY,
    station_id        station_id_enum NOT NULL,
    solar_output_kw   DOUBLE PRECISION,
    wind_output_kw    DOUBLE PRECISION,
    diesel_output_kw  DOUBLE PRECISION,
    battery_soc_pct   DOUBLE PRECISION,
    load_kw           DOUBLE PRECISION,
    fuel_remaining_l  DOUBLE PRECISION,
    generator_temp_c  DOUBLE PRECISION,
    recorded_at       TIMESTAMPTZ NOT NULL,
    created_by        BIGINT NOT NULL REFERENCES users(id)
);
CREATE INDEX idx_energy_station_time ON energy_readings (station_id, recorded_at);
-- environment_readings / logistics_readings / infrastructure_readings mirror this shape

CREATE TABLE alerts (
    id                BIGSERIAL PRIMARY KEY,
    station_id        station_id_enum NOT NULL,
    subsystem         VARCHAR(32) NOT NULL,
    severity          alert_severity_enum NOT NULL,
    message           TEXT NOT NULL,
    triggered_by_rule VARCHAR(64),
    acknowledged      BOOLEAN NOT NULL DEFAULT FALSE,
    acknowledged_by   BIGINT REFERENCES users(id),
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_alerts_station_severity ON alerts (station_id, severity, acknowledged);

CREATE TABLE commands (
    id            BIGSERIAL PRIMARY KEY,
    station_id    station_id_enum NOT NULL,
    action        VARCHAR(64) NOT NULL,
    parameters    JSONB,
    issued_by     BIGINT NOT NULL REFERENCES users(id),
    state         command_state_enum NOT NULL DEFAULT 'SENT',
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE audit_log (
    id          BIGSERIAL PRIMARY KEY,
    user_id     BIGINT,
    role        VARCHAR(32),
    station_id  VARCHAR(16),
    action      VARCHAR(64) NOT NULL,
    detail      JSONB,
    ip_address  VARCHAR(45),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_audit_user_time ON audit_log (user_id, created_at);

-- RLS deliberately not configured as a security boundary here — see C15.
```

**Connection string:** use Supabase's **pooled ("Transaction mode")**
connection URI for `SUPABASE_DB_URL`, not the direct connection —
Supabase's smaller compute tiers cap total simultaneous direct Postgres
connections, and a pooled connection avoids exhausting that limit
under concurrent requests from one FastAPI process.

---

## 9. Naming Conventions (unchanged)

Files `snake_case.py`, classes `PascalCase`, service methods verb-first,
repository methods `save`/`latest`/`history`/`get_by_*`, test files
mirror source path under `tests/`.

---

## 10. Testing Contracts

All Revision 4 contracts apply unchanged, plus:

| Layer | Required test | Must assert |
|---|---|---|
| Realtime (if Option B used) | `tests/e2e/test_realtime_never_reaches_wrong_role.py` | a Bharati-tagged DB change never appears on a Maitri session's SSE stream |
| 3D loader | manual/lighthouse check, not a unit test | `station_3d_view.js` and `three.module.js` are absent from the initial page's network waterfall; only appear after opening `/maitri/view_3d` |

---

## 11. Definition of Done Checklist

All Revision 4 items apply, plus:

- [ ] `grep -r "SUPABASE_SERVICE_ROLE_KEY" app/static/ app/templates/` returns nothing (C13).
- [ ] `grep -r "supabase-js\|createClient(" app/static/ app/templates/` returns nothing unless a documented, reviewed exception exists (C14) — default is no Supabase client code in the browser at all.
- [ ] New `/stream` SSE route: confirmed it only emits events already scoped to the requesting session's `station_id`/role.
- [ ] Any new Three.js asset: confirmed absent from `base.html` and only referenced via a lazy `x-init` script injection (C16).