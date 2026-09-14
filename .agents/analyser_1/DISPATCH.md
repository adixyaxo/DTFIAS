# Dispatch Instructions — Analyser Agent (Phase 2: Performance Weakness Detection)

## Working Directory
`c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\analyser_1`

## Project Root
`c:\Users\adity\Documents\Coding\Projects\DTFIAS`

## Original Request
Refer to `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\ORIGINAL_REQUEST.md` (section `## 2026-09-13T15:39:15Z`).

## Mission & Requirements
1. Ingest and analyze `c:\Users\adity\Documents\Coding\Projects\DTFIAS\perf_baseline.json` alongside the codebase (`app/routers/`, `app/models/`, `app/schemas/`, `app/templates/`, `app/static/`, `engine/services/`, `infrastructure/`).
2. Discover, locate, and document every concrete performance weakness across all six required categories:
   - **Slow ORM queries**: N+1 patterns, missing `.options(selectinload/joinedload)`, over-fetching all columns (e.g. `select(Model)` vs explicit columns or lightweight summaries), and un-eager loaded relations causing errors like `MissingGreenlet` in `POST /hq/commands`.
   - **Missing DB indexes**: Inspect SQLAlchemy model `__table_args__` and foreign keys/filter columns (e.g. `station_id`, `timestamp`, `severity`, `status`) in telemetry, alerts, and audit logs.
   - **Full-page Jinja2 renders vs HTMX partials**: Identify every portal route in `app/routers/maitri/`, `app/routers/bharati/`, `app/routers/hq/` that returns a full layout page when `HX-Request: "true"` is sent instead of a targeted partial/fragment.
   - **Alpine.js payload bloat**: Audit `x-data` in templates (and `app/static/js/`) for unused reactive properties, over-fetching JSON APIs, or massive inline JSON payloads.
   - **FastAPI response model trimming**: Audit `response_model=` on endpoints and identify schemas serializing unneeded fields or deeply nested models.
   - **Synchronous / blocking calls in async handlers & Redundant DB queries**: Audit `async def` routes and services for blocking calls (e.g. sync I/O, `time.sleep`, or synchronous password checks), as well as repetitive DB queries per request (e.g., redundant user profile lookups in auth/RBAC middleware/dependencies).
3. Produce a prioritized, actionable report at `c:\Users\adity\Documents\Coding\Projects\DTFIAS\perf_analysis.md` (and a copy or summary in your working directory).
   - EVERY finding MUST include:
     * Category
     * File path
     * Line number(s)
     * Root cause
     * Estimated latency and payload impact
     * Concrete recommended fix for the Fixer Agent
4. Adhere to all GEMINI.md hard constraints:
   - C1: `engine/**` purity (zero fastapi/sqlalchemy/asyncpg/jinja2)
   - C8: SQLAlchemy ORM or parameterized queries only (zero f-strings)
   - C3: `station_id` server-side only
   - C5: Router-level role dependencies
   - C7: Audit logs on state changes
   - C10/C11: Cookie security and CSRF intact
   - Four-layer architecture boundaries.
5. Maintain `progress.md` with liveness timestamps.
6. When complete, write `handoff.md` in `.agents/analyser_1/` and notify orchestrator_4 via `send_message`.

## 2026-09-13T15:55:44Z
You are the Analyser Agent (analyser_1) for Phase 2: Performance Weakness Detection.
Your working directory is: c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\analyser_1
Cover all 6 optimization areas with exact file paths, line numbers, root cause, estimated impact, and concrete fix recommendations:
1. Slow ORM queries (N+1, missing selectinload/joinedload, over-fetching columns, MissingGreenlet in POST /hq/commands)
2. Missing DB indexes on filtered/joined columns
3. Full-page Jinja2 renders on HTMX requests (missing request.headers.get("HX-Request") branching)
4. Alpine.js x-data payload and state bloat
5. FastAPI response model trimming
6. Sync/blocking calls in async def handlers and redundant per-request DB queries (e.g. in RBAC/auth)
Respect GEMINI.md hard constraints (C1, C8, C3, C5, C7, C10, C11).
Maintain progress.md with liveness timestamps.
When complete, write handoff.md in your working directory and notify the orchestrator with send_message.

## 2026-09-13T16:06:03Z
**Context**: Performance analysis for DTFIAS endpoints.
**Content**: Checking in on your progress regarding the 6 bottleneck categories and compilation of perf_analysis.md.
**Action**: Please update progress.md and report current status or if you need any assistance.
