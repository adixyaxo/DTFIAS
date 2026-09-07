# DTFIAS Master Documentation Index & Agentic Navigation Guide

> **Project:** Digital Twin for Indian Antarctic Stations (SIH26060)  
> **Target Audience:** Google Antigravity, Gemini Code, Claude Code, Autonomous Agents, and Human Engineers  
> **Status:** Authoritative Master Index & Single Source of Truth (SSOT) Map  
> **Last Verified:** September 2026  

---

## 1. Single Source of Truth (SSOT) Domain Matrix

When working on any task, agents MUST resolve conflicting information by following this strict hierarchy of authority. Higher-tier documents override lower-tier references.

| Domain | Single Source of Truth (Tier 1) | Secondary / Implementation References | Prohibited / Deprecated Patterns |
| :--- | :--- | :--- | :--- |
| **System Architecture & Layering** | [`docs/architecture.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/architecture.md) | [`GEMINI.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/GEMINI.md), [`CLAUDE.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/CLAUDE.md) | 2-layer MVC, importing DB/HTTP in `engine/` (C1), importing `app.config` in `infrastructure/` |
| **Database Schema & Migrations** | [`docs/database.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/database.md) (v1 Lock 25 tables), [`scripts/migrations/001_initial_schema.sql`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/scripts/migrations/001_initial_schema.sql) | [`docs/databaseTables.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/databaseTables.md), [`scripts/migrations/README.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/scripts/migrations/README.md) | Obsolete 5-table BIGSERIAL draft, MySQL dialects, f-string SQL queries (C8), `postgresql+asyncpg://` in `psql` CLI |
| **Brand Identity & Tokens** | [`.agents/brand_design/SKILL.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/.agents/brand_design/SKILL.md) | [`GEMINI.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/GEMINI.md) §7, [`.agents/frontend/SKILL.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/.agents/frontend/SKILL.md) (DTFIAS Override) | Space Grotesk, Arial, Roboto, rejecting Inter or `--brand-cream` as "AI slop", single-variant status colors |
| **Frontend Endpoints & Templates** | [`docs/frontend-endpoints.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/frontend-endpoints.md) | `app/templates/`, `app/routers/` | Bundler/npm pipelines (C17), React/Vue rewrites, hardcoded dummy URLs |
| **2.5D Digital Twin (Station Twin)** | [`docs/2dFrontend.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/2dFrontend.md) | `app/static/js/`, `app/templates/maitri/twin.html`, `app/templates/bharati/twin.html` | React `.tsx` components, phantom documentation files, unrealistic generator wattages (>340 kW) |
| **FastAPI Backend & Async Python** | [`.agents/fastapi/SKILL.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/.agents/fastapi/SKILL.md) | `app/routers/`, `app/schemas/`, `engine/services/` | Pydantic V1 syntax (`@validator`, `class Config`), sync DB calls, per-endpoint role guards (C5) |
| **PostgreSQL & Supabase Best Practices** | [`.agents/database/SKILL.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/.agents/database/SKILL.md) | `infrastructure/database/postgres/` | Direct browser connections to Supabase, missing foreign key indexes, using anon key as DB password |
| **Testing & Inconsistency Tracking** | [`docs/testing/backend-findings.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/testing/backend-findings.md), [`docs/testing/backend-inconsistencies.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/testing/backend-inconsistencies.md) | [`docs/documentation-tasks.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/documentation-tasks.md), `tests/` | Untracked schema or layer drift, phantom unit tests |

---

## 2. Hard Constraints Quick Reference (C1 – C17)

All agents MUST enforce these rules without exception. Violating any constraint is a blocking regression:

- **C1 (Engine Layer Purity):** `engine/**` imports ZERO HTTP or DB dependencies (`fastapi`, `starlette`, `jinja2`, `sqlalchemy`, `asyncpg`). Grep verified.
- **C2 (Station Scoping):** Station-scoped tables MUST use `station_id UUID REFERENCES stations(id) NOT NULL` (indexed FK).
- **C3 (Server-Side Station Scope):** `station_id` is set strictly server-side (class constant in portal services or user session). NEVER accepted from client request body/query parameters.
- **C4 (Role Boundaries):** `maitri_portal_service` and `bharati_portal_service` MUST NOT define `issue_command`, `manage_users`, or `view_audit`. Only `hq_portal_service` may.
- **C5 (Router Guards):** Role guards MUST be declared on `APIRouter(dependencies=[...])`, not decorated per endpoint.
- **C6 (Password Security):** Argon2 (`argon2-cffi`) ONLY. Plaintext passwords must NEVER appear in logs or exceptions.
- **C7 (Audit Trail):** Every login, state write, command issuance, and permission denial inserts a row into `audit_logs`.
- **C8 (SQL Injection Immunity):** All database operations use SQLAlchemy ORM or parameterized queries. ZERO f-string SQL.
- **C9 (Shared Layer Scope):** `shared/**` contains only types/constants used across 2+ top-level layers.
- **C10 (Session Security):** Cookies MUST be configured with `httponly=True`, `secure=True`, `samesite="strict"`.
- **C11 (CSRF Defense):** CSRF tokens verified on every state-mutating request (`POST`, `PUT`, `DELETE`).
- **C12 (Station Isolation):** Telemetry streams and cache entries must be tenant-isolated by station ID.
- **C13 (Secret Hygiene):** Supabase `SERVICE_ROLE_KEY` resides strictly in backend environment variables. Never in static JS or HTML.
- **C14 (Realtime Architecture):** Realtime listener runs exclusively on the server (`infrastructure/realtime/supabase_listener.py`). NO `supabase-js` or browser Realtime clients.
- **C15 (DB Access Control):** Backend connects as trusted service; RLS is disabled/default-deny for direct client connections.
- **C16 (3D Performance):** Three.js / `station_3d_view.js` is lazy-loaded on demand via Alpine `x-init`. NEVER in `base.html` unconditional scripts.
- **C17 (Runtime Architecture):** Runtime is bundler-free using Tailwind CDN (`<script src="https://cdn.tailwindcss.com">`). No npm build step required to run the server.

---

## 3. Agent Task Decision Trees

### "I need to create or modify an API endpoint"
1. Read [`docs/architecture.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/architecture.md) §3 and §5 to locate the correct layer.
2. Read [`.agents/fastapi/SKILL.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/.agents/fastapi/SKILL.md) for Pydantic V2 schema and async dependency injection patterns.
3. Check [`docs/frontend-endpoints.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/frontend-endpoints.md) to confirm URL route, method, response schema, and template binding.
4. Ensure router-level RBAC is applied via `APIRouter(dependencies=[Depends(...)])` (C5).
5. If the endpoint mutates state, ensure an audit record is dispatched to `audit_logs` (C7).

### "I need to create or alter a database table or column"
1. Read [`docs/database.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/database.md) (v1 Lock) in full.
2. Inspect [`scripts/migrations/001_initial_schema.sql`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/scripts/migrations/001_initial_schema.sql).
3. Verify table naming (singular vs plural convention in v1 Lock) and key types (`UUID` with `gen_random_uuid()`).
4. Add indexed foreign keys for all `REFERENCES` columns.
5. Create corresponding SQLAlchemy ORM model in `app/models/`. Never import SQLAlchemy in `engine/` (C1).

### "I need to design or modify a UI view or component"
1. Read [`.agents/brand_design/SKILL.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/.agents/brand_design/SKILL.md) for the official color palette and typography.
2. Review [`.agents/frontend/SKILL.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/.agents/frontend/SKILL.md) (DTFIAS Brand Override section).
3. Use the mandatory 4-tier typography:
   - Headings: `Playfair Display` (`--font-heading`)
   - Editorial / Callouts: `Playfair` (`--font-body`)
   - UI Chrome / Buttons / Tables: `Inter` (`--font-ui`)
   - Sensor Values / Readouts: `JetBrains Mono` (`--font-mono`)
4. Main page background MUST use `--brand-cream: #F5F2EB`.
5. Status colors MUST choose between light-bg variants (`--status-ok`, `--status-warning`, etc.) and dark-bg variants (`--status-ok-dark`, `--status-warning-dark`, etc.).
6. Use Tailwind utility classes via CDN; do not add npm dependencies (C17).

### "I need to implement or update the 2.5D Digital Twin view"
1. Read [`docs/2dFrontend.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/2dFrontend.md) in full.
2. Build interactive SVG components embedded directly into Jinja2 templates (`twin.html`, `asset_drawer.html`).
3. SVG hotspot elements must follow the kebab-case naming convention: `hotspot-{asset-slug}`.
4. Telemetry values must reflect real polar SCADA specs (e.g. Bharati ~282 kW load, 340 kW capacity, -15°C to -35°C ambient).

---

## 4. Documentation Directory Sitemap

```
DTFIAS/
├── README.md                      # Project introduction, quick start, architecture overview
├── GEMINI.md                      # Canonical behavioral contract for Google Antigravity & Gemini agents
├── CLAUDE.md                      # Canonical behavioral contract for Claude Code agents
├── docs/
│   ├── DOCUMENTATION-INDEX.md     # THIS FILE — Master SSOT & navigation index
│   ├── documentation-tasks.md     # Audit tracking ledger for documentation consistency
│   ├── architecture.md            # Structural contract (4-layer DDD, constraints C1–C17)
│   ├── database.md                # Canonical schema authority (v1 Lock 25 tables)
│   ├── databaseTables.md          # Generated column-level schema reference
│   ├── frontend-endpoints.md      # UI route catalog, templates, API contracts
│   ├── 2dFrontend.md              # 2.5D SVG digital twin implementation specification
│   └── testing/
│       ├── backend-findings.md    # Master verified backend findings ledger
│       ├── backend-inconsistencies.md # Master backend inconsistencies matrix
│       ├── aim-vs-desired-vs-actual-backend-deep-analysis.md # Triangulated backend audit
│       ├── aim-vs-desired-vs-actual-frontend-deep-analysis.md # Triangulated frontend audit
│       ├── design_inconsistencies.md # Frontend design & brand audit
│       ├── frontend-findings.md   # Master verified frontend findings ledger
│       └── frontend-fix-log.md    # Frontend repair and patch log
├── .agents/
│   ├── brand_design/SKILL.md      # Official DTFIAS color tokens and typography rules
│   ├── frontend/SKILL.md          # Complete frontend design guidelines with DTFIAS override
│   ├── database/SKILL.md          # Supabase & PostgreSQL indexing and connection rules
│   ├── fastapi/SKILL.md           # FastAPI async endpoints, Pydantic V2, and RBAC rules
│   └── agents/                    # Specialized agent personas (Backend, Frontend, Docs)
└── scripts/
    ├── migrations/
    │   ├── 001_initial_schema.sql # Canonical SQL migration script (25 tables)
    │   └── README.md              # Database setup and psql execution instructions
    └── test_db_connection.py      # Connectivity verification script
```

---

## 5. Verification Checklist Before Marking Tasks Complete

```bash
# 1. Verify Engine Layer Purity (Constraint C1)
grep -rE "^(import|from) (fastapi|sqlalchemy|asyncpg|jinja2)" engine/
# MUST return ZERO matches.

# 2. Verify No Leaked Secrets in Frontend (Constraint C13)
grep -r "SUPABASE_SERVICE_ROLE_KEY" app/static/ app/templates/
# MUST return ZERO matches.

# 3. Verify No Browser-Side Supabase Realtime (Constraint C14)
grep -rE "supabase-js|createClient\(" app/static/ app/templates/
# MUST return ZERO matches.

# 4. Verify No Raw f-string SQL (Constraint C8)
grep -rE 'execute\(f["\']' app/ engine/ infrastructure/
# MUST return ZERO matches.
```
