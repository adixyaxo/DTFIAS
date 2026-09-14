# DTFIAS Performance Profile and Endpoint Optimization Plan

## Objective
Benchmark all DTFIAS FastAPI application endpoints, analyze performance bottlenecks (ORM queries, DB indexes, full vs HTMX fragments, Alpine.js reactive bloat, response models, async blocking), implement optimizations ensuring all endpoints respond under 1s, payload size decreases by >= 20%, and verify zero regressions with full test suite and GEMINI.md compliance.

## Phase Breakdown

### Phase 1: R1 — Endpoint Benchmarking (Tester Agent)
- Subagent: `teamwork_preview_worker` (or `teamwork_preview_explorer`) acting as Tester Agent
- Working directory: `.agents/tester_1`
- Tasks:
  1. Inspect `app/routers/` (auth, maitri, bharati, hq, and all sub-routers) to build a complete inventory of HTTP GET/POST/PUT/DELETE endpoints.
  2. Verify if Uvicorn server is running on port 8000 (`http://127.0.0.1:8000`). If not, launch uvicorn in background or via standard test client / live requests.
  3. Prepare authentication credentials / session cookies for protected endpoints (HQ Admin, Station Operator, Viewer roles as needed).
  4. Benchmark every discovered endpoint:
     - Standard HTTP request (GET/POST/etc.)
     - HTMX request (with `HX-Request: "true"` header) for applicable endpoints
     - Measure TTFB and total duration in ms
     - Measure response size in bytes
     - Record HTTP status code
     - Classify response type (Full HTML, HTMX partial, JSON, Stream, etc.)
  5. Save structured data to `perf_baseline.json` at project root.

### Phase 2: R2 — Analysis & Weakness Detection (Analyser Agent)
- Subagent: `teamwork_preview_explorer` acting as Analyser Agent
- Working directory: `.agents/analyser_1`
- Tasks:
  1. Parse `perf_baseline.json` and rank slowest endpoints and largest payloads.
  2. Analyze codebase for:
     - ORM queries with N+1 or missing `selectinload`/`joinedload` or over-fetching columns (`select(Model)` vs explicit columns)
     - Missing database indexes on filter/join columns
     - Full-page Jinja2 renders on HTMX requests
     - Alpine.js `x-data` object bloat (unused reactive state)
     - Pydantic response models serializing excess fields
     - Synchronous / blocking calls in `async def` handlers
     - Redundant DB roundtrips
  3. Produce `perf_analysis.md` with:
     - Exact file path and line numbers
     - Root cause explanation
     - Estimated latency & payload impact
     - Prioritized actionable remediation plan

### Phase 3: R3 — Fix Implementation (Fixer Agent)
- Subagent: `teamwork_preview_worker` acting as Fixer Agent
- Working directory: `.agents/worker_fixer_1`
- Tasks:
  1. Ingest `perf_analysis.md`.
  2. Implement optimizations across all 6 categories:
     a) ORM/DB query optimization (`select(col1, col2)`, `selectinload()`, `__table_args__` indexes)
     b) HTMX partial refactoring (branch on `request.headers.get("HX-Request")` or render fragment template)
     c) Alpine.js payload trimming (clean x-data and trimmed JSON endpoints)
     d) Jinja2 template optimization (remove redundant blocks, include stable fragments)
     e) FastAPI response model trimming (slimmer Pydantic schemas)
     f) Concurrency / async fixes (replace blocking calls with async)
  3. Strictly adhere to GEMINI.md constraints.

### Phase 3.5: SPA-Style HTMX Navigation (Fixer Agent worker_fixer_2)
- Subagent: `teamwork_preview_worker` acting as SPA Fixer Agent
- Working directory: `.agents/worker_fixer_2`
- Tasks:
  1. Inspect `app/templates/layouts/base.html`, `layouts/dashboard.html`, `layouts/partial.html`, and portal templates.
  2. Implement SPA-style navigation without full page reloads:
     - Wrap main content area with `<main id="main-content">` consistently.
     - Add `hx-boost="true"` or explicit `hx-get` + `hx-target="#main-content"` + `hx-swap="innerHTML"` + `hx-push-url="true"` to nav links.
     - Verify partial fragment templates (`partial.html`, `partial_twin.html`) return just the inner content when `HX-Request: "true"` is present.
     - Add `htmx:afterSwap` event listener to re-initialize Alpine.js components if needed.
     - Ensure cross-portal navigation (e.g. Maitri -> HQ) swaps smoothly while preserving topnav/sidebar shell.
  3. Verify uvicorn server is running on port 8000; restart if needed.
  4. Run `pytest tests/` to confirm zero regressions.

### Phase 4: R4 — Verification & Comparison Run (Tester + Reviewer + Auditor)
- Subagents:
  - Tester Agent (`teamwork_preview_worker`) in `.agents/tester_2`: Re-run benchmarking suite identically, write `perf_after.json`, and generate `perf_comparison.md`.
  - Reviewer Agent (`teamwork_preview_reviewer`) in `.agents/reviewer_perf_1`: Review code diffs for correctness, maintainability, and layer adherence.
  - Challenger Agent (`teamwork_preview_challenger`) in `.agents/challenger_perf_1`: Stress test endpoints and edge cases.
  - Forensic Auditor (`teamwork_preview_auditor`) in `.agents/auditor_perf_1`: Verify genuine optimizations, no hardcoding, no cheating, check C1 and C8 compliance.
- Tasks:
  1. Verify all endpoints < 1000ms.
  2. Verify payload size reduced by >= 20% on average.
  3. Verify zero regressions.
  4. Run pytest (`pytest tests/`) and confirm all tests pass.
  5. Run C1 and C8 checks.
  6. Finalize `perf_comparison.md` and complete orchestrator handoff to Sentinel.
