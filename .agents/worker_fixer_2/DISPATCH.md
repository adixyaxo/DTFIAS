# Dispatch Instructions — SPA Fixer Agent (worker_fixer_2)
## Phase 3.5: SPA-Style HTMX Navigation (No Full Page Reloads)

## Working Directory
`c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\worker_fixer_2`

## Project Root
`c:\Users\adity\Documents\Coding\Projects\DTFIAS`

## Original Request & References
- System Resume & New Requirement: `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\orchestrator_4\DISPATCH.md` (section `## 2026-09-13T16:56:48Z`)
- GEMINI.md: `c:\Users\adity\Documents\Coding\Projects\DTFIAS\GEMINI.md`
- Frontend Skill: `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\frontend\SKILL.md`

## Mission & Requirements
Implement seamless SPA-style navigation across the DTFIAS web portal using HTMX so that clicking navigation links never triggers a full browser page reload.

### Implementation Checklist:
1. **Stable Content Container**:
   - In `app/templates/layouts/base.html` and `app/templates/layouts/dashboard.html` (and wherever the main layout lives), ensure the main swap area is enclosed in a stable, canonical container: `<main id="main-content">` (or `<div id="main-content">`).
2. **HTMX Interception**:
   - In `app/templates/layouts/base.html`, add `hx-boost="true"` to `<nav>`, `<aside id="sidebar">`, or `<body hx-boost="true">`.
   - Set `hx-target="#main-content"`, `hx-select="#main-content"`, and `hx-swap="innerHTML"`.
   - Ensure `hx-push-url="true"` so that the browser URL updates and back/forward browser history works seamlessly.
3. **Partial Fragment Alignment**:
   - Check `app/templates/layouts/partial.html` and `app/templates/layouts/partial_twin.html` created in Phase 3. Ensure they render `<main id="main-content">` or match the `hx-target` / `hx-select` selector.
   - Verify that when an endpoint receives `HX-Request: "true"`, it returns only the partial fragment, reducing payload from ~150KB to ~15KB without reloading topnav, sidebars, or CDN scripts.
4. **Alpine.js & Lazy Three.js Safety**:
   - Listen to `htmx:afterSwap` on `document.body` to initialize Alpine components if needed (`if (window.Alpine) { Alpine.initTree(e.detail.target); }`).
   - Preserve Lazy Three.js loading pattern (C16): Three.js must never be loaded unconditionally in base.html.
5. **Cross-Portal Navigation (Maitri ↔ Bharati ↔ HQ)**:
   - Ensure navigation between stations and HQ maintains the outer layout shell while updating active sidebar states and swapping `#main-content`.
6. **Server & Test Verification**:
   - Verify if Uvicorn is running on port 8000; restart it if needed (`.venv\Scripts\uvicorn.exe main:app --reload --port 8000`).
   - Run `pytest tests/` and confirm all 101 tests pass.
   - Run GEMINI.md C1 and C8 checks.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work.

Maintain `progress.md` with liveness timestamps.
When complete, write `handoff.md` in your working directory and notify orchestrator_4 via `send_message`.

## 2026-09-13T16:57:18Z
Implement SPA-style navigation across the DTFIAS web portal using HTMX so that clicking navigation links never triggers full browser page reloads:
1. Ensure the main content area is wrapped in a stable container: `<main id="main-content">` (or `<div id="main-content">`).
2. Implement HTMX navigation interception (via `hx-boost="true"`, `hx-target="#main-content"`, `hx-select="#main-content"`, `hx-swap="innerHTML"`, `hx-push-url="true"`).
3. Align with Phase 3 partial templates (`partial.html`, `partial_twin.html`) so that requests with `HX-Request: "true"` return only the fragment, cutting payload by 80-90%.
4. Ensure Alpine.js re-initializes on `htmx:afterSwap` (`if (window.Alpine) { Alpine.initTree(e.detail.target); }`).
5. Check if Uvicorn dev server is running on port 8000; restart it if needed (`.venv\Scripts\uvicorn.exe main:app --reload --port 8000`).
6. Run `pytest tests/` (verify all 101 tests pass).
7. Run GEMINI.md C1 and C8 checks.
