# Dispatch Instructions — Tester Agent (Phase 1: Baseline Benchmarking)

## Working Directory
`c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\tester_1`

## Project Root
`c:\Users\adity\Documents\Coding\Projects\DTFIAS`

## Original Request
Refer to `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\ORIGINAL_REQUEST.md` (section `## 2026-09-13T15:39:15Z`).

## Objective & Requirements
1. Discover all endpoints across all routers in `app/routers/` (`auth/`, `maitri/`, `bharati/`, `hq/`, and sub-routers, plus root routes in `main.py`).
2. Check if the Uvicorn server is running on `http://127.0.0.1:8000`. If not running, start it using `uvicorn main:app --port 8000` (or `uvicorn main:app --reload --port 8000`) or verify connectivity.
3. Authenticate to obtain valid session credentials/cookies for protected routes across different roles (HQ Admin, Station Operator, Viewer).
4. Run a comprehensive benchmarking suite:
   - For each route, test standard request (GET/POST).
   - If the route supports HTMX or serves HTML, test with `HX-Request: "true"` header.
   - Measure:
     * Time to first byte (TTFB) in ms
     * Total response time in ms
     * Response payload size in bytes
     * HTTP status code
     * Response content type
     * `is_partial`: boolean (true if response is JSON, HTMX partial snippet without full `<!DOCTYPE html>` or `<html>` document tag; false if full page).
5. Write the output to `perf_baseline.json` at the project root (`c:\Users\adity\Documents\Coding\Projects\DTFIAS\perf_baseline.json`).
6. Format of `perf_baseline.json`:
   ```json
   {
     "timestamp": "ISO timestamp",
     "summary": {
       "total_endpoints_tested": 0,
       "avg_response_time_ms": 0.0,
       "total_payload_bytes": 0,
       "endpoints_over_1000ms": 0
     },
     "endpoints": [
       {
         "route": "/hq/dashboard",
         "method": "GET",
         "is_htmx": false,
         "status_code": 200,
         "ttfb_ms": 45.2,
         "total_time_ms": 78.4,
         "size_bytes": 145020,
         "is_partial": false,
         "content_type": "text/html; charset=utf-8"
       }
     ]
   }
   ```
7. Integrity:
   DO NOT CHEAT. All measurements must be genuine live requests to the application. DO NOT hardcode test results. A forensic auditor will independently verify your results.
8. Maintain `progress.md` with liveness timestamps.
9. When complete, write `handoff.md` in `.agents/tester_1/` and send a completion message back to orchestrator_4.

## 2026-09-13T15:41:25Z
You are the Tester Agent (tester_1) for Phase 1: Baseline Endpoint Benchmarking of the DTFIAS application.

Your working directory is:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\tester_1

Please read your dispatch instructions at:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\tester_1\DISPATCH.md
and read the original request at:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\ORIGINAL_REQUEST.md

Your mission:
1. Discover all HTTP endpoints across all routers in app/routers/ (auth/, maitri/, bharati/, hq/, and all sub-routers, plus main.py).
2. Check if the Uvicorn server is running on http://127.0.0.1:8000. If not running, start it (e.g. run `uvicorn main:app --reload --port 8000` or verify it with curl/httpx).
3. Authenticate with appropriate session cookies/tokens to access protected endpoints.
4. Benchmark each endpoint (standard and HX-Request: "true" where applicable), recording:
   - route, method, is_htmx
   - status_code, content_type
   - ttfb_ms, total_time_ms
   - size_bytes
   - is_partial (true if HTML snippet/JSON, false if full HTML document)
5. Save the complete structured benchmark results to:
   c:\Users\adity\Documents\Coding\Projects\DTFIAS\perf_baseline.json
6. Maintain progress.md in your working directory with heartbeat timestamps.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations and measurements must be genuine live requests to the application. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

When finished, write handoff.md in your working directory and notify the orchestrator with send_message.
