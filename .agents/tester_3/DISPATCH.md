## 2026-09-13T17:14:13Z

# Dispatch Instructions — Tester Agent (tester_3)
## Phase 4: Post-Fix Benchmark & Comparison

## Working Directory
`c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\tester_3`

## Project Root
`c:\Users\adity\Documents\Coding\Projects\DTFIAS`

## Reference Artifacts
- Baseline Benchmark: `c:\Users\adity\Documents\Coding\Projects\DTFIAS\perf_baseline.json`
- Baseline Benchmark Script: `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\tester_1\run_baseline_benchmark.py`
- Phase 3 Handoff: `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\worker_fixer_1\handoff.md`
- Phase 3.5 Handoff: `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\worker_fixer_2\handoff.md`
- GEMINI.md: `c:\Users\adity\Documents\Coding\Projects\DTFIAS\GEMINI.md`

## Objectives & Requirements
1. Verify the Uvicorn server is running on `http://127.0.0.1:8000`. (If not listening, launch it via `.venv\Scripts\uvicorn.exe main:app --reload --port 8000`).
2. Run the identical benchmark suite across all 108 endpoint configurations against the live server (testing both standard requests and `HX-Request: "true"` headers). You can adapt or execute `.agents/tester_1/run_baseline_benchmark.py`.
3. Save structured results to:
   `c:\Users\adity\Documents\Coding\Projects\DTFIAS\perf_after.json`
4. Generate the before/after comparison table and summary to:
   `c:\Users\adity\Documents\Coding\Projects\DTFIAS\perf_comparison.md`
   - Executive Summary Table:
     * Average Response Time (ms): Before vs After & % reduction
     * Total Payload Volume (bytes / MB): Before vs After & % reduction (Target: >= 20%)
     * Endpoints >1000ms: Before vs After (Target: 0)
     * HTMX Partial Delivery (%): Before vs After (Target: 100%)
     * HTTP 500 Errors: Before vs After (Target: 0)
   - Comprehensive markdown comparison table for every single endpoint.
5. Run the full pytest suite:
   `pytest tests/` (confirm all 113 tests pass cleanly).
6. Verify GEMINI.md constraints:
   - C1: `grep -rE "^(import|from) (fastapi|sqlalchemy|asyncpg|jinja2)" engine/` → must be 0 matches.
   - C8: `grep -r "f\"" engine/ app/` for raw SQL → must be 0 matches.
   - C16: Three.js lazy-loading in templates.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations and measurements must be genuine live requests to the application. DO NOT hardcode test results. A forensic auditor will independently verify your results.

Maintain `progress.md` with liveness timestamps.
When complete, write `handoff.md` in your working directory and notify orchestrator_4 via `send_message`.
