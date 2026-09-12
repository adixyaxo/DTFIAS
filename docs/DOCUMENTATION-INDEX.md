# DTFIAS Master Documentation Index & Agentic Navigation Guide

> **Project:** Digital Twin for Indian Antarctic Stations (SIH26060)  
> **Target Audience:** Google Antigravity, Gemini Code, Claude Code, Autonomous Agents, and Human Engineers  
> **Status:** Authoritative Master Index & Single Source of Truth (SSOT) Map  
> **Maintained By:** Documentation Agent (`.agents/agents/DocumentationAgent/agent.md`)  
> **Last Verified:** September 2026  

---

## 1. Single Source of Truth (SSOT) Domain Matrix

When navigating or implementing features in DTFIAS, all agents MUST resolve conflicting information by following this strict hierarchy of authority. Higher-tier documents override lower-tier references.

| Domain | Single Source of Truth (Tier 1) | Secondary / Implementation References | Prohibited / Deprecated Patterns |
| :--- | :--- | :--- | :--- |
| **Project Charter & Scope** | [`docs/project-overview.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/project-overview.md) | [`README.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/README.md) | Ingesting raw AGEOS Earth Observation satellite data, public unauthenticated access |
| **System Architecture & Layering** | [`docs/architecture.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/architecture.md) | [`GEMINI.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/GEMINI.md), [`CLAUDE.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/CLAUDE.md) | 2-layer MVC, importing DB/HTTP in `engine/` (C1), importing `app.config` in `infrastructure/` |
| **Database Schema & Migrations** | [`docs/database.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/database.md) (v1 Lock 25 tables), [`scripts/migrations/001_initial_schema.sql`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/scripts/migrations/001_initial_schema.sql) | [`docs/databaseTables.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/databaseTables.md), [`scripts/migrations/README.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/scripts/migrations/README.md) | Obsolete 5-table BIGSERIAL draft, MySQL dialects, f-string SQL queries (C8), `postgresql+asyncpg://` in `psql` CLI |
| **Backend API Contracts** | [`docs/api-contracts.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/api-contracts.md) | [`docs/frontend-endpoints.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/frontend-endpoints.md), [`.agents/fastapi/SKILL.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/.agents/fastapi/SKILL.md) | Client-supplied `station_id` (C3), command issuance in station portals (C4), per-endpoint role guards (C5) |
| **Brand Identity & Tokens** | [`.agents/brand_design/SKILL.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/.agents/brand_design/SKILL.md) | [`GEMINI.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/GEMINI.md) §7, [`.agents/frontend/SKILL.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/.agents/frontend/SKILL.md) (DTFIAS Override) | Space Grotesk, Arial, Roboto, rejecting Inter or `--brand-cream` as "AI slop", single-variant status colors |
| **2.5D Digital Twin (Station Twin)** | [`docs/2dFrontend.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/2dFrontend.md) | `app/static/js/`, `app/templates/maitri/twin.html`, `app/templates/bharati/twin.html` | React `.tsx` components, external missing files (`4-stations-and-headquarters.md`), unrealistic generator wattages (>340 kW) |
| **3D Digital Twin Specification** | [`docs/bharati3d/00_bharati_3d_master_specification.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/00_bharati_3d_master_specification.md) | [`docs/bharati3d/`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/) (22 Deep Image Analyses), [`docs/bharati_3d_twin_implementation_plan.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati_3d_twin_implementation_plan.md) | Unconditional Three.js in `base.html` (C16), unoptimized raw CAD meshes (>2.5MB), invented non-CAD datums |
| **Operations & Deployment** | [`docs/operations.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/operations.md) | `Dockerfile`, `docker-compose.yml`, `scripts/test_db_connection.py` | Bundler/npm build steps (C17), committing credentials into `.env`, missing health checks |
| **Testing & Quality Strategy** | [`docs/testing/test-strategy.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/testing/test-strategy.md) | [`docs/testing/backend-findings.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/testing/backend-findings.md), [`docs/testing/backend-inconsistencies.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/testing/backend-inconsistencies.md), `tests/` | Untracked schema or layer drift, phantom unit tests, bypass of mechanical constraint assertions |
| **Antarctic Research & Station Facts**| [`docs/station-facts-and-research.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/station-facts-and-research.md) | [`shared/constants/stations.py`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/shared/constants/stations.py) | Confusing simulated sensor values with real polar facts, inventing unverified station equipment |

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

## 3. Eight Documentation Domains Directory Map

```
DTFIAS/
├── docs/
│   ├── DOCUMENTATION-INDEX.md         # THIS FILE — Master SSOT & navigation index
│   ├── documentation-tasks.md         # Structured task tracking ledger (DOC-001 to DOC-015)
│   ├── project-overview.md            # Domain 1 (Project): SIH26060 charter, scope, boundaries, terminology
│   ├── architecture.md                # Domain 2 (Architecture): Structural contract, 4-layer DDD, constraints C1–C17
│   ├── api-contracts.md               # Domain 3 (Backend): REST endpoints, SSE streams, error envelopes, RBAC
│   ├── frontend-endpoints.md          # Domain 3 & 5 (Backend/Frontend): UI route catalog, Jinja2 templates
│   ├── database.md                    # Domain 4 (Database): Canonical schema authority (v1 Lock 25 tables)
│   ├── databaseTables.md              # Domain 4 (Database): Generated column-level schema reference
│   ├── 2dFrontend.md                  # Domain 5 (Frontend): 2.5D SVG digital twin implementation specification
│   ├── bharati3d/                     # Domain 5 (3D Modeling): CAD blueprints & multi-batch visual specs (23 files)
│   │   ├── 00_bharati_3d_master_specification.md # Master 3D coordinate system, datums & Three.js hierarchy
│   │   └── [01-22]_*.md               # Detailed single-image CAD & architectural breakdowns
│   ├── testing/
│   │   ├── test-strategy.md           # Domain 6 (Testing): Testing pyramid, coverage thresholds, DoD checklist
│   │   ├── backend-findings.md        # Master verified backend findings ledger
│   │   ├── backend-inconsistencies.md # Master backend inconsistencies matrix
│   │   ├── aim-vs-desired-vs-actual-backend-deep-analysis.md # Triangulated backend audit
│   │   ├── aim-vs-desired-vs-actual-frontend-deep-analysis.md # Triangulated frontend audit
│   │   ├── design_inconsistencies.md  # Frontend design & brand audit
│   │   ├── frontend-findings.md       # Master verified frontend findings ledger
│   │   ├── frontend-fix-log.md        # Frontend repair and patch log
│   │   └── frontendInconsistency/     # Authoritative defect ledgers & deep frontend audit suite
│   │       ├── active-remaining-bugs.md # Master active defect ledger (16 empirically verified issues)
│   │       ├── navbar-inconsistencies.md # Deep navbar layout, hierarchy & responsive audit
│   │       └── routes-and-frontend-inconsistencies.md # Complete route & Jinja2 template audit
│   ├── operations.md                  # Domain 7 (Operations): Deployment, env vars, observability, failure modes
│   └── station-facts-and-research.md  # Domain 8 (Research): Authoritative polar station facts, NCPOR, SATCOM
├── .agents/
│   ├── brand_design/SKILL.md          # Official DTFIAS color tokens and typography rules
│   ├── frontend/SKILL.md              # Complete frontend design guidelines with DTFIAS override
│   ├── database/SKILL.md              # Supabase & PostgreSQL indexing and connection rules
│   ├── fastapi/SKILL.md               # FastAPI async endpoints, Pydantic V2, and RBAC rules
│   └── agents/
│       └── DocumentationAgent/agent.md# Documentation intelligence & evidence-collection agent persona
├── scripts/
│   ├── migrations/
│   │   ├── 001_initial_schema.sql     # Canonical SQL migration script (25 tables)
│   │   └── README.md                  # Database setup and psql execution instructions
│   └── test_db_connection.py          # Connectivity verification script
├── CLAUDE.md                          # Claude-flavored agent reference
├── GEMINI.md                          # Gemini-flavored agent reference
└── README.md                          # Repository quick-start
```

---

## 4. Verification Commands Before Marking Documentation Complete

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
