# Dispatch Instructions — Fixer Agent (Phase 3: Targeted Fix Implementation)

## Working Directory
`c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\worker_fixer_1`

## Project Root
`c:\Users\adity\Documents\Coding\Projects\DTFIAS`

## Original Request & Reference Materials
- Original Request: `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\ORIGINAL_REQUEST.md` (section `## 2026-09-13T15:39:15Z`)
- Weakness & Implementation Blueprint: `c:\Users\adity\Documents\Coding\Projects\DTFIAS\perf_analysis.md`
- GEMINI.md behavioral contract: `c:\Users\adity\Documents\Coding\Projects\DTFIAS\GEMINI.md`
- FastAPI & DB Skills: `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\fastapi\SKILL.md` and `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\database\SKILL.md`

## Objectives
Implement the concrete, prioritized fixes across all 6 performance categories following Section 4 (Concrete Implementation Blueprint) in `perf_analysis.md`:

### 1. Reliability & Concurrency Fixes (P0)
- **Fix `MissingGreenlet` in `POST /hq/commands`**:
  * In `app/models/command.py:41`, add `lazy="selectin"` to `Command.executions`.
  * In `app/schemas/command.py`, create/use `CommandCreateResponse` without `executions` for newly issued commands.
  * In `app/routers/hq/commands.py:39`, use `response_model=CommandCreateResponse`.
- **Fix SSE `/stream` Hang on benchmark clients / non-event-stream requests**:
  * In `app/routers/maitri/energy.py` and `app/routers/bharati/energy.py`:
    Immediately yield an initial telemetry event upon connection.
    If the request does not specify `Accept: text/event-stream`, yield the snapshot and exit cleanly to avoid blocking clients and connection pool starvation.
- **Eliminate Redundant 3-Query DB RBAC Lookups**:
  * In `infrastructure/security/authorization/rbac.py` (`get_current_user_optional`):
    For valid signed JWT tokens, construct the `Profile` with its roles and station access directly from token claims, avoiding 3 sequential remote Supabase round-trips on every HTTP request. If DB fallback is needed, cache profiles with a short TTL.
- **Async Argon2 Verification**:
  * In `app/routers/auth/auth.py:83`, wrap `verify_password` with `await asyncio.to_thread(verify_password, password, user.hashed_password)` to prevent event loop blocking.

### 2. Database Indexes & Query Optimizations (P1)
- **Add Missing SQLAlchemy Model Indexes via `__table_args__`**:
  * In `app/models/telemetry.py`: Add composite index `Index("ix_energy_readings_station_time", "station_id", "time")` and for `EnvironmentReading`.
  * In `app/models/alert.py`: Add composite indexes `Index("ix_active_alerts_station_status", "station_id", "status")` and on status + created_at.
  * In `app/models/command.py`: Add composite index on `station_id, status, created_at` and index on `command_id` in `CommandExecution`.
  * In `app/models/audit.py`: Add indexes on `created_at`, `(station_id, created_at)`, `(user_id, created_at)`.
- **Optimize `HQPortalService.get_overview()`**:
  * In `engine/services/portals/hq_portal_service.py`, collapse redundant multi-station alert queries into a single batch query grouped in-memory.
- **Optimize `_resolve_station_id()`**:
  * In `infrastructure/database/postgres/repositories/station_repository.py`, add or use a query that fetches only the station ID without `selectinload(Station.areas)` when only the ID is required.

### 3. HTMX Partial Rendering (P0/P1)
- **Create Partial Layout**:
  * Create `app/templates/layouts/partial.html` rendering `<div id="dashboard_content">{% block dashboard_content %}{% endblock %}</div>` (and required partial blocks).
- **Conditional Rendering in Routers**:
  * In `app/routers/hq/router.py` (`render_hq`), `app/routers/maitri/router.py` (`render_station`), and `app/routers/bharati/router.py` (`render_station`):
    Check if `request.headers.get("HX-Request") == "true"`.
    If HTMX: render with the partial template/layout; if standard browser: render with the full base layout.
  * Ensure the payload size for HTMX requests drops by 80-90% (from ~150KB to < 20KB).

### 4. Alpine.js & Template Trimming (P2)
- In `app/static/js/three/station_twin.js` (or `app/static/js/station_twin.js`):
  Trim legacy/redundant coordinates and throttle background loops when `document.hidden`.
- In `app/templates/components/topnav.html`:
  Only run 1s interval when clock element is visible.

## Strict GEMINI.md Constraints (MANDATORY):
- C1: `engine/**` must import ZERO fastapi/sqlalchemy/asyncpg/jinja2 (grep enforced).
- C8: No f-string SQL — SQLAlchemy ORM or parameterized queries only.
- C3: `station_id` set server-side only, never from request body.
- C5: Role guards on APIRouter via `dependencies=`, not per-endpoint.
- C7: Every state-changing fix touching auth/commands/alerts must still write an `audit_logs` row.
- C10/C11: Cookie (httponly, secure, samesite=strict) and CSRF intact.
- 4-layer architecture boundaries strictly preserved.

## Verification:
- Run `pytest tests/` and verify all tests pass (0 failures).
- Run `grep -rE "^(import|from) (fastapi|sqlalchemy|asyncpg|jinja2)" engine/` and confirm 0 matches.
- Run `grep -r "f\"" engine/ app/` for raw SQL and confirm 0 matches.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Maintain `progress.md` with liveness timestamps.
When complete, write `handoff.md` in `.agents/worker_fixer_1/` and notify orchestrator_4 via `send_message`.

## 2026-09-13T16:08:34Z
You are the Fixer Agent (worker_fixer_1) for Phase 3: Targeted Fix Implementation.

Your working directory is:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\worker_fixer_1

Please read your dispatch instructions at:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\worker_fixer_1\DISPATCH.md
and read the implementation blueprint at:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\perf_analysis.md
and read GEMINI.md at:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\GEMINI.md

Your mission:
Implement the high-impact performance optimizations across all 6 categories following the 4-stage blueprint in perf_analysis.md:
1. Fix MissingGreenlet in POST /hq/commands (lazy="selectin" on Command.executions, CommandCreateResponse)
2. Fix SSE /stream timeout/hang on non-event-stream clients and yield initial event immediately
3. Eliminate redundant 3-query DB RBAC lookups in rbac.py (use verified JWT claims or short TTL cache)
4. Wrap Argon2 password verify with asyncio.to_thread
5. Add missing indexes via __table_args__ on telemetry, alert, command, and audit models
6. Optimize HQPortalService.get_overview() and _resolve_station_id()
7. Implement HTMX partial fragment rendering (layouts/partial.html and request.headers.get("HX-Request") branching in router helpers) to reduce HTMX payload by 80-90%
8. Trim Alpine.js static payload and clock interval

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Strictly adhere to GEMINI.md constraints:
- C1: engine/** imports zero fastapi/sqlalchemy/asyncpg/jinja2 (grep enforced)
- C8: No f-string SQL — SQLAlchemy ORM or parameterized queries only
- C3: station_id set server-side only
- C5: Role guards on APIRouter via dependencies=
- C7: State-changing fixes write audit_logs
- C10/C11: Cookie and CSRF intact
- Run pytest tests/ and ensure all tests pass cleanly.

Maintain progress.md with liveness timestamps.
When complete, write handoff.md in your working directory and notify the orchestrator with send_message.

## 2026-09-13T16:29:00Z
**Context**: Phase 3 Fix Implementation.
**Content**: Checking in on your progress regarding the implementation of Stages 1-4 and test verification.
**Action**: Please update progress.md with your current progress and status.
