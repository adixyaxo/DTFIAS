# Performance Weakness Detection & Optimization Analysis — Analyser Summary
**Working Directory Copy for `analyser_1`**
**Canonical File**: `c:\Users\adity\Documents\Coding\Projects\DTFIAS\perf_analysis.md`

Refer to `perf_analysis.md` for the exhaustive 5-stage blueprint covering all 6 categories:
1. **Slow ORM Queries & MissingGreenlet**:
   - `MissingGreenlet` in `POST /hq/commands` due to lazy loading `executions` in `CommandResponse` (HTTP 500, 16.8s).
   - N+1 query loop in `HQPortalService.get_overview()` generating 6 sequential remote queries for stations/telemetry/alerts (14s-17.9s).
   - `_resolve_station_id()` over-fetching all `StationArea` rows via `selectinload(Station.areas)`.
   - Unnecessary `session.refresh(model)` on write operations in `audit_repository.py`, etc.
2. **Missing Database Indexes**:
   - High-frequency telemetry: `(station_id, time DESC)` missing on `energy_readings` and `environment_readings`.
   - Active alerts: `(station_id, status, created_at DESC)` and `(status, created_at DESC)` missing on `active_alerts`.
   - Commands: `(station_id, status, created_at DESC)` and `command_id` foreign key missing on `commands` & `command_executions`.
   - Audit logs: `(created_at DESC)` and `(station_id, created_at DESC)` missing on `audit_logs`.
3. **Full-Page Jinja2 Renders on HTMX Requests**:
   - Zero `HX-Request` branching across `render_hq`, `render_station`, and dashboard routers.
   - `hx-boost="true"` downloads 100KB-163KB per navigation click (11.8 MB total baseline volume across 108 requests).
   - Implementing `layouts/partial.html` will cut payload by 85%-90%.
4. **Alpine.js Payload Bloat and State Overhead**:
   - 28KB `station_twin.js` with dead 2D SVG coordinates (`svgX`, `svgY`) and static telemetry data.
   - Unthrottled 2s `_tick()` simulation loop running in background tabs.
   - Hidden 1s UTC clock in `topnav.html` running on mobile/tablet/laptop viewports (<1536px).
5. **FastAPI Response Model Over-Serialization**:
   - `CommandResponse` over-serializing nested `executions` on command creation.
   - `UserResponse` serializing non-existent `email` and unused timestamps.
6. **Sync/Blocking Calls & Redundant DB Queries**:
   - Redundant 3-query Supabase lookup in `get_current_user_optional` on every request despite signed JWT claims (causes 4.3s-5.3s baseline).
   - Synchronous CPU-bound Argon2 `verify_password` on asyncio event loop.
   - Infinite SSE polling loop holding `AsyncSession` open indefinitely on `/stream`, causing 64s timeouts and pool exhaustion.
