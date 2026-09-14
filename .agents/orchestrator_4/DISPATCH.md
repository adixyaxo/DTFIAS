# Dispatch Instructions — Performance Profile & Endpoint Optimization

## Working Directory
`c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\orchestrator_4`

## Project Root
`c:\Users\adity\Documents\Coding\Projects\DTFIAS`

## Original Request
Refer to `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\ORIGINAL_REQUEST.md` (section `## 2026-09-13T15:39:15Z`).

## Mission & Scope
Analyse the full performance profile of the DTFIAS FastAPI application (Digital Twin for Indian Antarctic Stations, SIH26060) and optimise every endpoint to respond under 1 second, reducing HTML/JSON payload sizes and minimising HTMX/Alpine.js round-trip data volume.

Coordinate the 4 required phases with dedicated specialist subagents:
1. **R1. Endpoint Benchmarking (Tester Agent)**: Discover and benchmark all endpoints across auth, maitri, bharati, hq, and sub-routers. Write `perf_baseline.json`. Check server status; start uvicorn if needed.
2. **R2. Analysis & Weakness Detection (Analyser Agent)**: Analyze `perf_baseline.json` alongside codebase. Produce prioritized weakness report `perf_analysis.md` (ORM queries, indexes, HTMX fragments, Alpine.js payloads, response models, sync calls in async def).
3. **R3. Fix Implementation (Fixer Agent)**: Implement highest-impact fixes across all 6 categories while strictly respecting GEMINI.md hard constraints (C1, C8, C3, C5, C7, C10, C11).
4. **R4. Verification Run (Tester Agent, second pass)**: Benchmark suite rerun producing `perf_after.json` and `perf_comparison.md`. Verify pytest and code integrity.

Maintain `plan.md` and update `progress.md` continuously. When completed, write `handoff.md` and notify Sentinel.

## 2026-09-13T15:39:15Z
Analyse the full performance profile of the DTFIAS FastAPI application (Digital Twin for Indian Antarctic Stations, SIH26060) and optimise every endpoint to respond under 1 second, reducing HTML/JSON payload sizes and minimising HTMX/Alpine.js round-trip data volume.

Integrity mode: development (strict)

Requirements:
- R1. Endpoint Benchmarking (Tester Agent) -> perf_baseline.json
- R2. Analysis & Weakness Detection (Analyser Agent) -> perf_analysis.md
- R3. Fix Implementation (Fixer Agent) across 6 categories (ORM/DB queries, HTMX partials, Alpine.js payloads, Jinja2 templates, FastAPI schemas, Async/concurrency) adhering strictly to GEMINI.md
- R4. Verification Run (Tester Agent, second pass) -> perf_after.json, perf_comparison.md, pytest, C1/C8 compliance

## 2026-09-13T16:56:48Z
System resumed after restart. All prior background tasks and subagents were stopped.

New Requirement added before Phase 4 completes:
- **SPA-Style HTMX Navigation (No Full Page Reloads on Route Change)**:
  1. In `app/templates/layouts/base.html` (or equivalent layout), ensure navigation links don't trigger full browser reload.
  2. Stable main content wrapper: `<main id="main-content">` (or equivalent).
  3. `hx-boost="true"` or explicit `hx-get` + `hx-target` + `hx-push-url="true"` on nav links.
  4. Ensure `HX-Request` header returns partial fragments (`partial.html`, `partial_twin.html`) and swaps `#main-content`.
  5. Cross-portal navigation preserves layout shell; re-init Alpine.js on `htmx:afterSwap` if needed.
  6. Verify uvicorn server on port 8000.
  7. Resume Phase 4 verification: `perf_after.json`, `perf_comparison.md`, `pytest tests/`, GEMINI.md C1/C8 checks.
