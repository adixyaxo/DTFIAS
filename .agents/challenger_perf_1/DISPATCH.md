# Dispatch Instructions — Challenger Agent (challenger_perf_1)
## Phase 5: Empirical Verification & Stress Testing

## Working Directory
`c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\challenger_perf_1`

## Project Root
`c:\Users\adity\Documents\Coding\Projects\DTFIAS`

## Mission & Scope
Empirically test and stress-test the performance optimizations and SPA navigation:
1. Live request testing against `http://127.0.0.1:8000`:
   - Test `POST /hq/commands` to verify HTTP 201 Created and zero `MissingGreenlet` errors.
   - Test `GET /maitri/energy/stream` and `GET /bharati/energy/stream` with both SSE and non-SSE client headers to verify immediate response and clean exit.
   - Test HTMX partial fragment requests (`HX-Request: "true"`) across HQ, Maitri, and Bharati to verify fragment content, `<main id="main-content">`, out-of-band sidebar updates, and 75-90% payload reduction.
   - Test unauthenticated requests to verify proper 302 redirects to `/auth/login`.
2. Check for race conditions, error handling, and regressions.
3. Provide your verdict: `APPROVE` or `REQUEST_CHANGES`.


## 2026-09-13T17:24:44Z

<USER_REQUEST>
You are the Challenger Agent (challenger_perf_1) for Phase 5 empirical verification and stress testing of DTFIAS endpoints.

Working directory:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\challenger_perf_1

Please read your dispatch instructions at:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\challenger_perf_1\DISPATCH.md
and read GEMINI.md at:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\GEMINI.md
and read the original request at:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\ORIGINAL_REQUEST.md

Empirically test live endpoints on http://127.0.0.1:8000 (POST /hq/commands, SSE /stream, HTMX partial requests, unauthenticated redirects).
Verify stability, error handling, and performance under edge conditions.
Deliver your verdict (APPROVE / REQUEST_CHANGES) in handoff.md and send_message.
</USER_REQUEST>
