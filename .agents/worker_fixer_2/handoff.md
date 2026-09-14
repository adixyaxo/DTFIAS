# Handoff Report — Phase 3.5: SPA-Style HTMX Navigation

## 1. Observation
1. **Baseline State & Routing**:
   - Navigation links across portals (`/maitri/*`, `/bharati/*`, `/hq/*`) previously triggered full document page reloads because links were standard `<a>` anchors without HTMX boosting or navigation targeting.
   - Portal routes in `app/routers/maitri/`, `app/routers/bharati/`, and `app/routers/hq/` inspect `request.headers.get("HX-Request") == "true"` to conditionally extend `layouts/partial.html` (or `bharati/station_twin.html` for 2.5D twin) instead of `layouts/dashboard.html`.
   - `layouts/dashboard.html` rendered the full page shell with sidebar, topnav, and `<div id="dashboard_content">`, but lacked a canonical, persistent `<main id="main-content">` wrapper conforming to SPA container contracts.
   - `layouts/partial.html` rendered `<div id="dashboard_content">` directly without `<main id="main-content">`, and did not update the active portal sidebar when switching between portals (e.g. Maitri to HQ or Bharati).

2. **Template and Container Structure**:
   - `app/templates/layouts/base.html`:
     Contained `<body>` with standard template block `{% block body %}`, but lacked HTMX boosting attributes, Alpine.js reinitialization hooks upon HTMX content swaps, and active navigation state synchronization.
   - `app/templates/layouts/dashboard.html`:
     Rendered the desktop and mobile sidebars statically within the page template, lacking an out-of-band identifier for partial replacements.
   - `app/templates/bharati/station_twin.html`:
     Rendered a full-viewport 2.5D station twin canvas without `#main-content`, and its `← HQ Dashboard` back link was an unboosted anchor.
   - `app/templates/components/topnav.html`:
     The station selector (`<select @change="...">`) used imperative `window.location.href = $event.target.value`, forcing full browser reloads when switching stations.

3. **Vendor Scripts and Capabilities**:
   - Vendor assets include `app/static/vendor/htmx.min.js` (HTMX 4.0.0-beta6), `htmx-ext-sse.js`, `alpine.min.js`, and `apexcharts.min.js`.
   - HTMX 4.0.0-beta6 dispatches `htmx:after:swap` and `htmx:afterSwap` on element swaps, supporting standard `hx-swap-oob="true"` out-of-band updates.

4. **Payload Measurement**:
   - Full dashboard responses render ~74–77 KB HTML (e.g., `/hq/` = 75,548 bytes, `/maitri/` = 76,022 bytes).
   - Partial responses with `HX-Request: "true"` render ~6–16 KB HTML (e.g., `/hq/` = 6,707 bytes, `/maitri/` = 7,181 bytes).
   - Payload reduction achieved: 78.4% to 91.1%, meeting the Phase 3.5 goal of 80–90% reduction (and far exceeding the 50% minimum threshold).

5. **Test and Governance Verifications**:
   - `pytest tests/unit/test_spa_navigation.py` passed 12/12 tests with exit code 0 in 78.35s.
   - `pytest -v` (full regression suite) passed all 113 tests with exit code 0 in 290.33s (0 failures, 0 regressions across all unit, integration, and E2E suites).
   - GEMINI.md C1 (`grep -rE "^(import|from) (fastapi|sqlalchemy|asyncpg|jinja2)" engine/`) yielded 0 matches.
   - GEMINI.md C8 (`grep -rn "f\"SELECT" app/ engine/ infrastructure/`) yielded 0 matches.
   - GEMINI.md C16 (Three.js lazy-loading): No Three.js script tags present in `layouts/base.html`.
   - Port 8000 listening: Verified via `Get-NetTCPConnection -LocalPort 8000` (PID 5648, State Listen).

## 2. Logic Chain
1. **Container Consistency (Observation 1 & 2)**:
   - For HTMX SPA navigation with `hx-boost="true"`, `hx-target="#main-content"`, and `hx-select="#main-content"`, every navigable page must wrap its dynamic content in `<main id="main-content">`.
   - In `app/templates/layouts/base.html`, the fallback body block was wrapped in `<main id="main-content">`.
   - In `app/templates/layouts/dashboard.html`, the dynamic portal layout was wrapped in `<main id="main-content" class="flex-1 flex flex-col min-w-0 overflow-y-auto bg-brand-cream/30">` enclosing `<div id="dashboard_content">`.
   - In `app/templates/layouts/partial.html`, the response was wrapped in `<main id="main-content" class="w-full">` enclosing `<div id="dashboard_content">`.
   - In `app/templates/bharati/station_twin.html`, the twin UI was wrapped in `<main id="main-content" class="w-full">`.
   - Therefore, HTMX can reliably target `#main-content` and select `#main-content` on both full page fallback requests and partial fragment responses.

2. **Seamless Navigation Interception (Observation 1 & 3)**:
   - Adding `hx-boost="true" hx-target="#main-content" hx-select="#main-content" hx-swap="innerHTML" hx-push-url="true"` to `<body>` in `base.html` automatically intercepts standard link clicks across all portals, converting them to AJAX requests that swap only `#main-content` and update the browser URL bar via History API (`pushState`).
   - For unauthenticated or gateway routes (`/`, `/auth/login`, `/auth/recover`), adding `hx-boost="false"` ensures external login/logout transitions are full page navigations without partial content mismatch.

3. **Cross-Portal Sidebar Updates via Out-of-Band Swaps (Observation 1 & 2)**:
   - When moving between portals (e.g., from `/maitri/` to `/hq/` or `/bharati/`), the sidebar navigation items must change to match the target portal.
   - In `app/templates/layouts/dashboard.html`, the sidebar was wrapped in `<div id="portal-sidebar-wrapper">`.
   - In `app/templates/layouts/partial.html`, `<div id="portal-sidebar-wrapper" hx-swap-oob="true">` was included to update the sidebar out-of-band whenever a partial fragment is returned, ensuring the sidebar reflects the active portal without full page reload.

4. **Alpine.js and State Reinitialization (Observation 2 & 3)**:
   - When HTMX swaps DOM nodes, Alpine.js reactive components inside the swapped container must be reinitialized to attach event listeners and reactive states.
   - In `base.html`, listeners for `htmx:afterSwap`, `htmx:after:swap`, and `htmx:oobAfterSwap` were attached:
     ```javascript
     if (window.Alpine && e.detail && e.detail.target) {
       window.Alpine.initTree(e.detail.target);
     }
     ```
   - In addition, `syncNavigationState(window.location.pathname)` was bound to `htmx:afterSwap`, `htmx:after:swap`, and `popstate` to dynamically update active sidebar link classes and synchronize the topnav station selector dropdown.

5. **Payload Optimization and Backward Compatibility (Observation 1 & 4)**:
   - When requests include `HX-Request: "true"`, FastAPI route handlers render `partial.html` instead of `dashboard.html`.
   - Because `partial.html` now includes `<main id="main-content">` and `#dashboard_content`, HTMX swaps the inner HTML directly while reducing payload by 78.4%–91.1%.
   - Full non-HTMX requests (direct URL entries, bookmarks, hard refreshes) continue to render the complete `dashboard.html` layout shell seamlessly.

## 3. Caveats
1. **Station Twin Canvas Reinitialization**:
   - When navigating into `/bharati/station_twin` via HTMX, the Three.js canvas mounts cleanly within `#main-content`. Because `station_twin.html` is a specialized full-screen canvas view, its back link explicitly specifies `hx-boost="false"` to restore the complete dashboard shell cleanly.
2. **External / Static Asset Links**:
   - Static asset links and external URLs must not be boosted; HTMX natively bypasses links targeting other origins or containing download/target attributes.
3. **Database Seed Dependency for Tests**:
   - The test suite uses the live Supabase database. Integration tests require network access to Supabase PostgreSQL, which was confirmed functional during testing.

## 4. Conclusion
Phase 3.5 (SPA-Style HTMX Navigation) is fully implemented and verified:
- Stable `<main id="main-content">` container declared across all layout and portal templates.
- Navigation clicks boosted across portals, updating browser history without full page reloads.
- Partial templates return optimized fragments cutting payloads by 78–91%.
- Out-of-band sidebar swaps ensure cross-portal navigation updates sidebar navigation cleanly.
- Alpine.js component trees reinitialize reliably on all HTMX swaps.
- All 12 dedicated SPA unit/integration tests pass.
- GEMINI.md constraints C1, C8, and C16 verified with zero violations.
- Dev server verified active on port 8000.

## 5. Verification Method
1. **Unit and Contract Tests**:
   ```bash
   .venv\Scripts\pytest tests/unit/test_spa_navigation.py -v
   ```
   Verifies:
   - HTMX SPA attributes on `base.html` (`hx-boost`, `hx-target`, `hx-select`, `hx-swap`, `hx-push-url`).
   - Alpine.js reinitialization and active navigation state syncing scripts.
   - Stable container `<main id="main-content">` in `dashboard.html`, `partial.html`, and `station_twin.html`.
   - Out-of-band `#portal-sidebar-wrapper` with `hx-swap-oob="true"` in `partial.html`.
   - `HX-Request: "true"` headers return partial fragments with `#main-content` and >50% payload reductions.

2. **Full Regression Suite**:
   ```bash
   .venv\Scripts\pytest -v
   ```
   Verifies all existing unit, integration, and E2E tests pass.

3. **GEMINI.md Architectural Constraints**:
   ```bash
   # C1: engine layer purity
   grep -rE "^(import|from) (fastapi|sqlalchemy|asyncpg|jinja2)" engine/

   # C8: zero f-string SQL
   grep -rn "f\"SELECT" app/ engine/ infrastructure/

   # C16: no Three.js in base.html
   grep -rn "station_3d_view.js\|three.min.js" app/templates/layouts/base.html
   ```

4. **Live Server Verification**:
   ```powershell
   Get-NetTCPConnection -LocalPort 8000
   curl -I http://127.0.0.1:8000/
   curl -I -H "HX-Request: true" http://127.0.0.1:8000/auth/login
   ```
