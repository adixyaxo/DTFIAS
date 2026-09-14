# Dispatch Instructions — Tester Agent (Phase 4: Post-Fix Benchmark & Comparison)

## Working Directory
`c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\tester_2`

## Project Root
`c:\Users\adity\Documents\Coding\Projects\DTFIAS`

## Original Request & Baseline Artifacts
- Original Request: `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\ORIGINAL_REQUEST.md` (section `## 2026-09-13T15:39:15Z`)
- Baseline Benchmark: `c:\Users\adity\Documents\Coding\Projects\DTFIAS\perf_baseline.json`
- Analysis Report: `c:\Users\adity\Documents\Coding\Projects\DTFIAS\perf_analysis.md`
- Phase 3 Handoff: `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\worker_fixer_1\handoff.md`

## Objectives & Requirements
1. Verify the Uvicorn server is running on `http://127.0.0.1:8000`. (If not running, start it using `.venv\Scripts\uvicorn.exe main:app --reload --port 8000`).
2. Run the identical benchmark suite across all 108 endpoint configurations (standard requests and `HX-Request: "true"` headers). You can adapt or run the benchmark runner script from `.agents/tester_1/run_baseline_benchmark.py`.
3. Save the post-optimization benchmark results to:
   `c:\Users\adity\Documents\Coding\Projects\DTFIAS\perf_after.json`
4. Generate `c:\Users\adity\Documents\Coding\Projects\DTFIAS\perf_comparison.md`:
   - Summary section comparing:
     * Average response time (ms): baseline vs after and % improvement
     * Total payload volume (bytes/MB): baseline vs after and % reduction (Target: >= 20%)
     * Number of endpoints exceeding 1,000ms: baseline vs after (Target: 0)
     * HTMX partial delivery: count of HTMX requests returning partial fragments (Target: 100%)
     * HTTP 500 error count: baseline vs after (Target: 0)
   - Comprehensive markdown comparison table for every tested endpoint.
5. Run full test suite:
   `pytest tests/`
   Verify that all tests pass cleanly.
6. Verify GEMINI.md constraints:
   - C1: `grep -rE "^(import|from) (fastapi|sqlalchemy|asyncpg|jinja2)" engine/` → must be 0 matches.
   - C8: `grep -r "f\"" engine/ app/` for raw SQL → must be 0 matches.
   - C13/C14: Verify no Supabase service role keys or client libraries in frontend.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations and measurements must be genuine live requests to the application. DO NOT hardcode test results. A forensic auditor will independently verify your results.

Maintain `progress.md` with liveness timestamps.
When complete, write `handoff.md` in `.agents/tester_2/` and notify orchestrator_4 via `send_message`.

## 2026-09-13T16:35:23Z
You are the Tester Agent (tester_2) for Phase 4: Post-Fix Benchmark & Comparison.

Your working directory is:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\tester_2

Please read your dispatch instructions at:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\tester_2\DISPATCH.md
and read the baseline benchmark at:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\perf_baseline.json
and read the original request at:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\ORIGINAL_REQUEST.md

Your mission:
1. Verify the Uvicorn server is running on port 8000 (start or reload if needed).
2. Execute the identical benchmark suite across all 108 endpoint configurations against the live server.
3. Save structured results to:
   c:\Users\adity\Documents\Coding\Projects\DTFIAS\perf_after.json
4. Generate the before/after comparison table and summary to:
   c:\Users\adity\Documents\Coding\Projects\DTFIAS\perf_comparison.md
5. Run the test suite: pytest tests/ (ensure 100% passing).
6. Run C1 and C8 grep checks to verify zero violations.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations and measurements must be genuine live requests to the application. DO NOT hardcode test results. A forensic auditor will independently verify your results. Integrity violations WILL be detected and your work WILL be rejected.

Maintain progress.md with liveness timestamps.
When complete, write handoff.md in your working directory and notify the orchestrator with send_message.

