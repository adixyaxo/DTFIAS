# DTFIAS — Route Integrity & Broken Frontend Surface Deep Audit

> **Document Status:** Authoritative QA & Frontend Defect Audit  
> **Target Path:** `docs/testing/frontendInconsistency/route-analysis-and-broken-frontends-audit.md`  
> **Auditor Persona:** Frontend Testing Agent (`.agents/agents/FrontendTestingAgent/agent.md`)  
> **Scope:** Full Route Surface (`app/routers/`), Jinja2 Template Library (`app/templates/`), Sidebar Navigation Maps (`app/templates/components/sidebar_*.html`), and DOM Render States.  
> **Date:** September 2026  
> **Target Audience:** Frontend Inconsistency Manager, Backend Engineers, and System Architects  

---

## 1. Executive Summary

A comprehensive automated and empirical route audit was conducted across the entire DTFIAS platform. Using an ASGI client test harness (`httpx.AsyncClient` with real template rendering and authenticated role evaluation), every URL declared in the backend routers, referenced in documentation, or linked inside the sidebar navigation components was tested.

### Critical Discoveries Summary

1. **Active Sidebar Links Throwing HTTP 404 Not Found (P0):**
   * Six primary operational domain links present in the station sidebars—**Infrastructure**, **Local Environment**, and **Logistics** for both Bharati and Maitri—return **HTTP 404 Not Found**.
   * When operators click these links, the browser displays raw JSON: `{"detail":"Not Found"}`.
   * **The Tragedy:** The frontend templates (`station/infrastructure.html`, `station/environment.html`, `station/logistics.html`) are fully written, styled, and present in `app/templates/station/` (aggregating ~112 KB of rich UI), but **backend endpoints were never wired** in `app/routers/bharati/router.py` or `app/routers/maitri/router.py`.
2. **Dashboard Alias 404s (P1):**
   * Navigating to `/{station}/dashboard` (e.g. `/bharati/dashboard`, `/maitri/dashboard`, `/hq/dashboard`) returns **HTTP 404 Not Found**. The routes were mounted exclusively at the root slash `/{station}/`.
3. **Orphaned Templates via Permanent 301 Redirects (P1):**
   * `/hq/roles` immediately redirects with HTTP 301 to `/hq/users`. The dedicated RBAC permissions matrix template `app/templates/hq/roles.html` (5 KB) is completely orphaned.
   * `/hq/reports` immediately redirects with HTTP 301 to `/hq/compliance`. The template `app/templates/hq/reports.html` (6.2 KB) is completely orphaned.
   * `/hq/simulations` is fully implemented and operational, but the sidebar link in `sidebar_hq.html` is commented out with `<!-- HIDE OUT-OF-SCOPE ROUTE -->`.
4. **Severe Cross-Station Domain Contamination in Working Routes (P0):**
   * When a Maitri operator visits `/maitri/` (Dashboard), `/maitri/twin`, `/maitri/energy`, `/maitri/telemetry`, `/maitri/personnel`, or `/maitri/health`, the rendered DOM displays **Bharati Station's physical facility data**.
   * The page renders Volvo Penta D13 Tier-4 generators (installed only at Bharati; Maitri uses legacy Deutz sets), Larsemann Hills coordinates (`69°24'S, 76°11'E`), and station codes (`IND-ANT-03`).
5. **Universal Tab Title Failure across Continental HQ (P2):**
   * 12 distinct views in `/hq/*` (`stations`, `energy`, `environment`, `logistics`, `compliance`, `telemetry`, `alerts`, `health`, `research`, `settings`, `simulations`, `assets`) fail to provide a `title` variable in their template contexts. Every browser tab displays the identical fallback: `"Antarctic Digital Twin"`.
6. **Full-Page Mockup DOM Pollution in Modals (P1):**
   * `app/templates/components/modals/asset_detail.html` and `alert_dialog.html` contain full Stitch page mockups with duplicate `<header>`, `<aside>`, and `<h1>` elements. Because `layouts/dashboard.html` unconditionally includes these modal files on every page, every screen in the app has invisible Bharati Volvo Penta headers injected into its DOM.

---

## 2. Comprehensive Route Verification Matrix

The following table records the empirical test results for every route, contrasting what the UI promises against what the server actually delivers.

| Portal | Route URL | HTTP Method | Auth Role Required | Server Status | Rendered Template / Target | What the User Actually Sees | Defect ID |
| :--- | :--- | :---: | :--- | :---: | :--- | :--- | :--- |
| **Public** | `/` | GET | None | **200 OK** | `index.html` (23.7 KB) | Institutional landing page, gateway cards to HQ, Bharati, Maitri | Nominal |
| **Auth** | `/auth/login` | GET | None | **200 OK** | `auth/login.html` (39.5 KB) | Dual-pane secure login gateway with polar isometric illustration | Nominal |
| **Auth** | `/auth/recover` | GET | None | **200 OK** | `auth/recover.html` (33.1 KB) | Password reset / recovery request card | Nominal |
| **Auth** | `/auth/logout` | GET | None | **302 Found** | Redirect -> `/auth/login` | Clears cookie and redirects to login | Nominal |
| **Bharati** | `/bharati/` | GET | `bharati_operator` | **200 OK** | `station/dashboard.html` (170 KB) | Bharati Station Dashboard; generator telemetry; maintenance logs | Nominal |
| **Bharati** | `/bharati/dashboard` | GET | `bharati_operator` | **404 NOT FOUND** | None (FastAPI default) | Raw JSON: `{"detail":"Not Found"}` | **FE-ROUTE-002** |
| **Bharati** | `/bharati/station-twin` | GET | `bharati_operator` | **200 OK** | `bharati/station_twin.html` (64.7 KB) | Bharati 2.5D interactive SVG digital twin with layer filters | Nominal |
| **Bharati** | `/bharati/twin` | GET | `bharati_operator` | **200 OK** | `bharati/station_twin.html` (64.7 KB) | Alias for `/bharati/station-twin` | Nominal |
| **Bharati** | `/bharati/energy` | GET | `bharati_operator` | **200 OK** | `station/energy.html` (167 KB) | Microgrid & combined heat/power SCADA | Nominal |
| **Bharati** | `/bharati/infrastructure`| GET | `bharati_operator` | **404 NOT FOUND** | None (FastAPI default) | Raw JSON: `{"detail":"Not Found"}` (**Sidebar Link Broken**) | **FE-ROUTE-001** |
| **Bharati** | `/bharati/environment` | GET | `bharati_operator` | **404 NOT FOUND** | None (FastAPI default) | Raw JSON: `{"detail":"Not Found"}` (**Sidebar Link Broken**) | **FE-ROUTE-001** |
| **Bharati** | `/bharati/logistics` | GET | `bharati_operator` | **404 NOT FOUND** | None (FastAPI default) | Raw JSON: `{"detail":"Not Found"}` (**Sidebar Link Broken**) | **FE-ROUTE-001** |
| **Bharati** | `/bharati/telemetry` | GET | `bharati_operator` | **200 OK** | `station/telemetry.html` (127 KB) | Real-time sensor channels, frequency bands, RSSI charts | Nominal |
| **Bharati** | `/bharati/alerts` | GET | `bharati_operator` | **200 OK** | `station/alerts.html` (159 KB) | Station incident triage matrix, active alarm list | Nominal |
| **Bharati** | `/bharati/personnel` | GET | `bharati_operator` | **200 OK** | `station/personnel.html` (128 KB) | Winter/Summer personnel roster, team allocations | Nominal |
| **Bharati** | `/bharati/health` | GET | `bharati_operator` | **200 OK** | `station/health.html` (129 KB) | Medical readiness, telemedicine vitals, infirmary stock | Nominal |
| **Bharati** | `/bharati/research` | GET | `bharati_operator` | **200 OK** | `station/research.html` (126 KB) | Atmospheric physics, glaciology research observations | Nominal |
| **Bharati** | `/bharati/assets/{id}` | GET | `bharati_operator` | **200 OK** | `station/asset_detail.html` (126 KB) | Physical equipment datasheet, maintenance schedule | Nominal |
| **Maitri** | `/maitri/` | GET | `maitri_operator` | **200 OK** | `station/dashboard.html` (170 KB) | **Contaminated:** Shows Bharati Volvo D13 generators & 69°24'S | **FE-ROUTE-004** |
| **Maitri** | `/maitri/dashboard` | GET | `maitri_operator` | **404 NOT FOUND** | None (FastAPI default) | Raw JSON: `{"detail":"Not Found"}` | **FE-ROUTE-002** |
| **Maitri** | `/maitri/station-twin` | GET | `maitri_operator` | **200 OK** | `station/twin.html` (188 KB) | **Contaminated:** Shows Bharati cutaway illustration & Larsemann coords | **FE-ROUTE-004** |
| **Maitri** | `/maitri/twin` | GET | `maitri_operator` | **200 OK** | `station/twin.html` (188 KB) | Alias for `/maitri/station-twin` | **FE-ROUTE-004** |
| **Maitri** | `/maitri/energy` | GET | `maitri_operator` | **200 OK** | `station/energy.html` (167 KB) | **Contaminated:** Displays Bharati microgrid telemetry | **FE-ROUTE-004** |
| **Maitri** | `/maitri/infrastructure` | GET | `maitri_operator` | **404 NOT FOUND** | None (FastAPI default) | Raw JSON: `{"detail":"Not Found"}` (**Sidebar Link Broken**) | **FE-ROUTE-001** |
| **Maitri** | `/maitri/environment` | GET | `maitri_operator` | **404 NOT FOUND** | None (FastAPI default) | Raw JSON: `{"detail":"Not Found"}` (**Sidebar Link Broken**) | **FE-ROUTE-001** |
| **Maitri** | `/maitri/logistics` | GET | `maitri_operator` | **404 NOT FOUND** | None (FastAPI default) | Raw JSON: `{"detail":"Not Found"}` (**Sidebar Link Broken**) | **FE-ROUTE-001** |
| **Maitri** | `/maitri/telemetry` | GET | `maitri_operator` | **200 OK** | `station/telemetry.html` (127 KB) | **Contaminated:** Shows Bharati sensor channels | **FE-ROUTE-004** |
| **Maitri** | `/maitri/alerts` | GET | `maitri_operator` | **200 OK** | `station/alerts.html` (159 KB) | Station alarm triage matrix | Nominal |
| **Maitri** | `/maitri/personnel` | GET | `maitri_operator` | **200 OK** | `station/personnel.html` (128 KB) | Personnel roster (contains Maitri conditional names) | Nominal |
| **Maitri** | `/maitri/health` | GET | `maitri_operator` | **200 OK** | `station/health.html` (129 KB) | Medical readiness (contains Maitri conditional names) | Nominal |
| **Maitri** | `/maitri/research` | GET | `maitri_operator` | **200 OK** | `station/research.html` (126 KB) | Geomagnetic & meteorological observations | Nominal |
| **Maitri** | `/maitri/assets/{id}` | GET | `maitri_operator` | **200 OK** | `station/asset_detail.html` (126 KB) | Asset datasheet | Nominal |
| **HQ** | `/hq/` | GET | `hq_admin` | **200 OK** | `hq/dashboard.html` (178 KB) | NCPOR Continental Command; satellite uplink status; station cards | Nominal |
| **HQ** | `/hq/dashboard` | GET | `hq_admin` | **404 NOT FOUND** | None (FastAPI default) | Raw JSON: `{"detail":"Not Found"}` | **FE-ROUTE-002** |
| **HQ** | `/hq/stations` | GET | `hq_admin` | **200 OK** | `hq/stations.html` (135 KB) | Polar Station Registry; tab title: "Antarctic Digital Twin" | **FE-ROUTE-005** |
| **HQ** | `/hq/energy` | GET | `hq_admin` | **200 OK** | `hq/energy.html` (182 KB) | Cross-Station Microgrid Overview; tab title: "Antarctic Digital Twin" | **FE-ROUTE-005** |
| **HQ** | `/hq/environment` | GET | `hq_admin` | **200 OK** | `hq/environment.html` (165 KB) | Continental Geospatial & Meteorological Array | **FE-ROUTE-005** |
| **HQ** | `/hq/logistics` | GET | `hq_admin` | **200 OK** | `hq/logistics.html` (169 KB) | Polar Vessel Manifest, Convoy Tracking, Jet A-1 Fuel Reserves | **FE-ROUTE-005** |
| **HQ** | `/hq/compliance` | GET | `hq_admin` | **200 OK** | `hq/compliance.html` (161 KB) | Madrid Protocol Annex III Environmental Compliance Ledger | **FE-ROUTE-005** |
| **HQ** | `/hq/audit` | GET | `hq_admin` | **200 OK** | `hq/audit.html` (168 KB) | Cryptographic FIPS 140-3 Immutable Audit Ledger (Constraint C7) | Nominal |
| **HQ** | `/hq/users` | GET | `hq_admin` | **200 OK** | `hq/users.html` (176 KB) | Multi-Station Personnel Governance & Role Roster | Nominal |
| **HQ** | `/hq/roles` | GET | `hq_admin` | **301 MOVED** | Redirect -> `/hq/users` | **Bypassed:** Bypasses `hq/roles.html`, lands on Users page | **FE-ROUTE-003** |
| **HQ** | `/hq/reports` | GET | `hq_admin` | **301 MOVED** | Redirect -> `/hq/compliance` | **Bypassed:** Bypasses `hq/reports.html`, lands on Compliance | **FE-ROUTE-003** |
| **HQ** | `/hq/telemetry` | GET | `hq_admin` | **200 OK** | `hq/telemetry.html` (160 KB) | Central Telemetry Streams; tab title: "Antarctic Digital Twin" | **FE-ROUTE-005** |
| **HQ** | `/hq/alerts` | GET | `hq_admin` | **200 OK** | `hq/alerts.html` (166 KB) | Continental Incident Protocol Control & Crisis Triage | **FE-ROUTE-005** |
| **HQ** | `/hq/commands` | GET | `hq_admin` | **200 OK** | `hq/commands.html` (144 KB) | Tactical Remote Command Dispatch (C4 compliant) | Nominal |
| **HQ** | `/hq/health` | GET | `hq_admin` | **200 OK** | `hq/health.html` (141 KB) | Continental Health & Readiness; tab title: "Antarctic Digital Twin" | **FE-ROUTE-005** |
| **HQ** | `/hq/research` | GET | `hq_admin` | **200 OK** | `hq/research.html` (135 KB) | Joint Polar Science Projects; tab title: "Antarctic Digital Twin" | **FE-ROUTE-005** |
| **HQ** | `/hq/settings` | GET | `hq_admin` | **200 OK** | `hq/settings.html` (133 KB) | Global System Settings; tab title: "Antarctic Digital Twin" | **FE-ROUTE-005** |
| **HQ** | `/hq/simulations` | GET | `hq_admin` | **200 OK** | `hq/simulations.html` (135 KB) | Simulations Workspace; **Sidebar link commented out** | **FE-ROUTE-003** |
| **HQ** | `/hq/assets` | GET | `hq_admin` | **200 OK** | `hq/assets.html` (165 KB) | Physical Asset Inventory; tab title: "Antarctic Digital Twin" | **FE-ROUTE-005** |

---

## 3. Deep Analysis of Broken & Non-Working Frontends

### 3.1 The "Operational Domain Black Hole" (404 Endpoints)
In both `sidebar_bharati.html` and `sidebar_maitri.html`, the "OPERATIONAL DOMAINS" section contains:
```html
<a href="/bharati/infrastructure">... Infrastructure & LSS ...</a>
<a href="/bharati/environment">... Local Environment ...</a>
<a href="/bharati/logistics">... Logistics & Supply ...</a>
```
When an operator clicks any of these three navigation items:
1. **What happens under the hood:** The browser sends `GET /bharati/infrastructure`. FastAPI evaluates its routing table, fails to find a handler, and returns a bare `application/json` payload with status `404 Not Found`.
2. **What the operator sees:** The page abruptly turns black/white with a single raw string:
   ```json
   {"detail":"Not Found"}
   ```
   There is no styling, no navigation bar, no error explanation, and no way back except the browser's Back button.
3. **The Irony:** The files `app/templates/station/infrastructure.html` (42 KB), `app/templates/station/environment.html` (32 KB), and `app/templates/station/logistics.html` (37 KB) already exist, with complete SCADA metric dials, HVAC schematics, atmospheric sensor gauges, and convoy inventory manifests. They are completely stranded because three lines of Python are missing from `router.py`.

---

### 3.2 The Redirect Shell Game (`/hq/roles` and `/hq/reports`)
In `sidebar_hq.html` (Line 68), the navigation promises a **"Roles & Matrix"** screen:
```html
<a class="..." href="/hq/roles">
  <span class="material-symbols-outlined">admin_panel_settings</span><span>Roles & Matrix</span>
</a>
```
1. **What happens:** The server issues an HTTP 301 Permanent Redirect to `/hq/users`.
2. **What the operator sees:** The user clicks "Roles & Matrix", expecting a multi-station permissions matrix (Madrid Protocol officer, Station Lead, Scientist permissions). Instead, the page jumps to "Personnel & Users" (`/hq/users`), where the active sidebar highlight stays on "Personnel & Users", disorienting the operator.
3. **The Orphan:** `app/templates/hq/roles.html` contains an actual RBAC matrix table with permission toggles (`station.read`, `energy.manage`, `command.execute`). It is completely unreachable.
4. **The Same Problem with `/hq/reports`:** In `hq/router.py`, `/hq/reports` redirects to `/hq/compliance`. `app/templates/hq/reports.html` sits completely unused.

---

### 3.3 The Maitri Station Identity Crisis (Domain Cross-Contamination)
Maitri Station is an inland research base situated in the ice-free Schirmacher Oasis ($70^\circ 46'\text{S}, 11^\circ 44'\text{E}$). It was constructed in 1989 on solid rock foundation and operates legacy Deutz generators and containerized living modules.

Yet when an operator logs into the **Maitri Inland Portal** (`/maitri/`):
* **The Cutaway Twin (`/maitri/twin`):** The 2D/2.5D station twin displays an aerodynamic, two-story modular building raised on hydraulic stilts—which is the distinctive architecture of **Bharati Station** in Larsemann Hills!
* **The Coordinates:** The header ribbon displays $69^\circ 24'\text{S}, 76^\circ 11'\text{E}$ (Bharati's coordinates, 3,000 km away from Maitri).
* **The Microgrid (`/maitri/energy`):** The generation readout claims the station is powered by `CHP Unit #03 - Volvo Penta D13 Tier-4 Polar Diesel`. Maitri has no such units.
* **The Station Code:** Telemetry badges display `IND-ANT-03` and `IN-ANT-BHT-02` (Bharati identifiers).
* **Visual Experience:** A Maitri station lead sees the physical layout, weather, generators, and coordinates of Bharati Station, destroying the operational credibility of the digital twin.

---

### 3.4 The Tab Title Vacuum across Continental HQ
When opening multiple tabs across the Continental HQ portal:
* Tab 1 (`/hq/stations`): Shows tab label **"Antarctic Digital Twin"**
* Tab 2 (`/hq/energy`): Shows tab label **"Antarctic Digital Twin"**
* Tab 3 (`/hq/environment`): Shows tab label **"Antarctic Digital Twin"**
* Tab 4 (`/hq/logistics`): Shows tab label **"Antarctic Digital Twin"**
* Tab 5 (`/hq/compliance`): Shows tab label **"Antarctic Digital Twin"**
* Tab 6 (`/hq/telemetry`): Shows tab label **"Antarctic Digital Twin"**
* Tab 7 (`/hq/alerts`): Shows tab label **"Antarctic Digital Twin"**

**Root Cause:** In `app/routers/hq/router.py`, `render_hq` is written as:
```python
def render_hq(request: Request, name: str):
    return templates.TemplateResponse(request=request, name=f"hq/{name}.html", context={"station_id": "hq"})
```
It fails to supply `"title": f"NCPOR HQ - {name.title()}"`. Consequently, Jinja falls back to the default `base.html` string on 12 out of 16 HQ pages.

---

### 3.5 Global DOM Pollution via Full-Page Modal Injections
In `app/templates/layouts/dashboard.html` (Lines 16–22):
```html
<dialog id="dtfias_alert_modal" ...>
    {% include "components/modals/alert_dialog.html" ignore missing %}
</dialog>
<dialog id="dtfias_asset_modal" ...>
    {% include "components/modals/asset_detail.html" ignore missing %}
</dialog>
```
1. **The Defect:** Both `alert_dialog.html` and `asset_detail.html` do not contain standalone modal dialog cards; they contain **entire exported Stitch web pages** (including duplicate `<header class="fixed top-0 ...">`, full `<aside>` sidebars, and `<h1>CHP Unit #03</h1>` tags).
2. **The Damage:** Because `layouts/dashboard.html` is the parent layout for every station and HQ page, **every view in DTFIAS has an entire hidden second website injected into its DOM inside `<dialog>` tags**.
3. **Consequences:**
   * Duplicate IDs (`#telemetry-console`, `#station-overview`) throughout the DOM.
   * Screen readers announce the hidden modal's header and sidebar links before reaching page content.
   * Keyword search engines and scrapers index Bharati Volvo Penta headers on every single Maitri and HQ URL.

---

## 4. Master Finding Records

```text
ID: FE-ROUTE-001
Title: Primary operational domain links (Infrastructure, Environment, Logistics) throw HTTP 404 in Bharati and Maitri
Severity: P0 (Critical)
Status: Open

Route:
- /bharati/infrastructure
- /bharati/environment
- /bharati/logistics
- /maitri/infrastructure
- /maitri/environment
- /maitri/logistics
Component: Station Sidebar Navigation & Subsystem Views
File:
- app/routers/bharati/router.py
- app/routers/maitri/router.py
- app/templates/components/sidebar_bharati.html (L28, 31, 34)
- app/templates/components/sidebar_maitri.html (L28, 31, 34)
Viewport: All
Browser: All

Category: Functional / API Integration

Expected:
Clicking "Infrastructure & LSS", "Local Environment", or "Logistics & Supply" in the station sidebar must load the corresponding station subsystem view (rendering `station/infrastructure.html`, `station/environment.html`, or `station/logistics.html`).

Actual:
The router files (`bharati/router.py` and `maitri/router.py`) omit endpoints for `/infrastructure`, `/environment`, and `/logistics`. Clicking any of these links yields HTTP 404 with raw JSON: `{"detail":"Not Found"}`.

Reproduction:
1. Log in as a Bharati or Maitri operator.
2. In the left sidebar, click "Infrastructure & LSS" (/bharati/infrastructure).
3. Observe raw unstyled JSON 404 error page.
4. Repeat for "Local Environment" and "Logistics & Supply".

Evidence:
- Terminal test output:
  [404] GET /bharati/infrastructure len=22
  [404] GET /bharati/environment    len=22
  [404] GET /bharati/logistics      len=22
  [404] GET /maitri/infrastructure  len=22
  [404] GET /maitri/environment     len=22
  [404] GET /maitri/logistics       len=22
- Template presence:
  `app/templates/station/infrastructure.html` (42,789 bytes) exists!
  `app/templates/station/environment.html` (32,165 bytes) exists!
  `app/templates/station/logistics.html` (37,842 bytes) exists!

Consistency Rule Violated:
docs/api-contracts.md; docs/frontend-endpoints.md §3 ("Station Modules"); .agents/agents/FrontendTestingAgent/agent.md §Primary Objectives ("1. Test every frontend route/page. 5. Detect API integration problems").

Root Cause Hypothesis:
The routes were implemented in `hq/router.py` but accidentally left out of `bharati/router.py` and `maitri/router.py` when modularizing sub-routers.

Recommended Fix:
In both `app/routers/bharati/router.py` and `app/routers/maitri/router.py`, add the missing route definitions:
```python
@router.get("/infrastructure", response_class=HTMLResponse)
async def station_infrastructure(request: Request):
    return render_station(request, "infrastructure")

@router.get("/environment", response_class=HTMLResponse)
async def station_environment(request: Request):
    return render_station(request, "environment")

@router.get("/logistics", response_class=HTMLResponse)
async def station_logistics(request: Request):
    return render_station(request, "logistics")
```

Regression Check:
Verify all three links return 200 OK and render the rich operational templates for both Maitri and Bharati.
Dependencies: None.
```

---

```text
ID: FE-ROUTE-002
Title: Common /{station}/dashboard aliases return HTTP 404 Not Found
Severity: P1 (High)
Status: Open

Route:
- /bharati/dashboard
- /maitri/dashboard
- /hq/dashboard
Component: Sub-Router Mount Points
File:
- app/routers/bharati/dashboard.py
- app/routers/maitri/dashboard.py
- app/routers/hq/dashboard.py
Viewport: All
Browser: All

Category: Functional / Navigation

Expected:
Navigating to `/{station}/dashboard` should render the main station/HQ dashboard (matching documentation and common URL patterns), or redirect with HTTP 301 to `/{station}/`.

Actual:
The dashboard sub-routers only declare `@router.get("/")`. As a result, visiting `/bharati/dashboard`, `/maitri/dashboard`, or `/hq/dashboard` throws HTTP 404 Not Found.

Reproduction:
1. Enter `http://localhost:8000/bharati/dashboard` into browser address bar.
2. Observe HTTP 404 Not Found.

Evidence:
- Test output:
  [404] GET /bharati/dashboard len=22
  [404] GET /maitri/dashboard  len=22
  [404] GET /hq/dashboard      len=22

Consistency Rule Violated:
docs/frontend-endpoints.md; URL ergonomics and defensive routing.

Root Cause Hypothesis:
Sub-routers were mounted with only the root slash `@router.get("/")`.

Recommended Fix:
Add dual decorators in `dashboard.py` files:
```python
@router.get("/", response_class=HTMLResponse)
@router.get("/dashboard", response_class=HTMLResponse)
async def station_dashboard(...):
```

Regression Check:
Both `/bharati/` and `/bharati/dashboard` return 200 OK with identical content.
Dependencies: None.
```

---

```text
ID: FE-ROUTE-003
Title: Orphaned templates caused by permanent 301 redirects (/hq/roles and /hq/reports)
Severity: P1 (High)
Status: Open

Route:
- /hq/roles
- /hq/reports
Component: Continental HQ Subsystem Routing
File: app/routers/hq/router.py (Lines 75-81)
Viewport: All
Browser: All

Category: Functional / Architectural Integrity

Expected:
1. Clicking "Roles & Matrix" in `sidebar_hq.html` should display the RBAC Permission Matrix (`hq/roles.html`).
2. Visiting `/hq/reports` should render operational reports (`hq/reports.html`).

Actual:
`hq/router.py` redirects `/hq/roles` to `/hq/users` and `/hq/reports` to `/hq/compliance`. Both `hq/roles.html` (5,025 bytes) and `hq/reports.html` (6,212 bytes) are orphaned templates that are never displayed to users.

Reproduction:
1. Log in to NCPOR HQ.
2. Click "Roles & Matrix" in the sidebar.
3. Observe URL redirects to `/hq/users` and renders the user management list instead of the permission matrix.

Evidence:
```python
@router.get("/reports", response_class=RedirectResponse)
async def hq_reports(request: Request):
    return RedirectResponse(url="/hq/compliance", status_code=301)

@router.get("/roles", response_class=RedirectResponse)
async def hq_roles(request: Request):
    return RedirectResponse(url="/hq/users", status_code=301)
```

Consistency Rule Violated:
docs/architecture.md §RBAC; docs/frontend-endpoints.md §2; .agents/agents/FrontendTestingAgent/agent.md §Role-Based UI.

Root Cause Hypothesis:
Temporary redirects were added during early development before templates were completed, and were never updated to render the real templates.

Recommended Fix:
Update `hq/router.py` to render the actual templates:
```python
@router.get("/roles", response_class=HTMLResponse)
async def hq_roles(request: Request):
    return render_hq(request, "roles")

@router.get("/reports", response_class=HTMLResponse)
async def hq_reports(request: Request):
    return render_hq(request, "reports")
```

Regression Check:
`/hq/roles` renders the RBAC permissions matrix; `/hq/reports` renders operational mission reports.
Dependencies: None.
```

---

```text
ID: FE-ROUTE-004
Title: Maitri Station routes display Bharati facility data, coordinates, and Volvo Penta generators
Severity: P0 (Critical)
Status: Open

Route: All /maitri/* routes
Component: Station Portal Templates
File:
- app/templates/station/*
- app/templates/station/twin.html
- app/routers/maitri/router.py
Viewport: All
Browser: All

Category: Visual Consistency / Domain Integrity

Expected:
Maitri Station views must represent Maitri's actual domain facts: Schirmacher Oasis ($70^\circ 46'\text{S}, 11^\circ 44'\text{E}$), legacy Deutz generator arrays, and containerized modular habitat.

Actual:
Maitri renders from `app/templates/station/*`, which is hardcoded for Bharati Station. Maitri operators see:
- Bharati coordinates: $69^\circ 24'\text{S}, 76^\circ 11'\text{E}$
- Bharati generators: `Volvo Penta D13 Tier-4 Polar Diesel`
- Bharati station codes: `IND-ANT-03`, `IN-ANT-BHT-02`
- Bharati 2D/2.5D twin isometric cutaway on stilts (Bharati is on stilts; Maitri is on rock foundation).

Reproduction:
1. Navigate to `http://localhost:8000/maitri/`.
2. Inspect the station coordinates in the header ribbon: reads $69^\circ 24'\text{S}$.
3. Navigate to `http://localhost:8000/maitri/twin`.
4. Observe the architectural schematic depicts Bharati's Larsemann Hills facility on stilts.

Evidence:
- Automated test scan:
  URL: /maitri/
  [CONTAMINATION]: Mentions 'Bharati' 10x; Mentions Bharati coords 69°24'S; Mentions Volvo Penta D13 (Bharati-only); Mentions Bharati station codes
  URL: /maitri/twin
  [CONTAMINATION]: Mentions 'Bharati' 9x; Mentions Bharati coords 69°24'S; Mentions Volvo Penta D13; Mentions Bharati station codes

Consistency Rule Violated:
docs/station-facts-and-research.md (Authoritative polar station facts); .agents/agents/FrontendTestingAgent/agent.md §Project Context.

Root Cause Hypothesis:
Templates in `app/templates/station/` were copied from Bharati Stitch screen exports without parameterized Jinja conditional blocks for Maitri-specific equipment and schematics.

Recommended Fix:
1. In `app/templates/station/dashboard.html` and `energy.html`, wrap generator and facility blocks in Jinja conditionals:
   ```jinja2
   {% if station_id == 'maitri' %}
     <!-- Maitri Legacy Deutz Gensets & Schirmacher Oasis facts -->
   {% else %}
     <!-- Bharati Volvo Penta D13 Gensets & Larsemann Hills facts -->
   {% endif %}
   ```
2. Replace hardcoded coordinates with dynamic `{{ station.coordinates }}` and `{{ station.location }}`.

Regression Check:
Verify `/maitri/` displays zero occurrences of "Bharati", "Volvo Penta", or "69°24'S".
Dependencies: None.
```

---

```text
ID: FE-ROUTE-005
Title: 12 out of 16 Continental HQ routes lack page titles, displaying generic fallback in browser tabs
Severity: P2 (Medium)
Status: Open

Route:
- /hq/stations
- /hq/energy
- /hq/environment
- /hq/logistics
- /hq/compliance
- /hq/telemetry
- /hq/alerts
- /hq/health
- /hq/research
- /hq/settings
- /hq/simulations
- /hq/assets
Component: Continental HQ Router Context
File: app/routers/hq/router.py (Line 25-26)
Viewport: All
Browser: All

Category: Visual Consistency / Usability

Expected:
Every route must provide a descriptive title in its template context (e.g. `"title": "NCPOR HQ - Microgrid & Energy"`), enabling operators to distinguish multiple open dashboard tabs.

Actual:
`render_hq` only passes `{"station_id": "hq"}` without a `"title"` key. All 12 routes fall back to `"Antarctic Digital Twin"` in `base.html`. Operators cannot distinguish tabs.

Reproduction:
1. Open `/hq/energy`, `/hq/logistics`, and `/hq/alerts` in three adjacent browser tabs.
2. Look at the tab titles.
3. All three tabs read identically: "Antarctic Digital Twin".

Evidence:
- Scan output:
  URL: /hq/energy       Title: Antarctic Digital Twin
  URL: /hq/environment  Title: Antarctic Digital Twin
  URL: /hq/logistics    Title: Antarctic Digital Twin
  URL: /hq/compliance   Title: Antarctic Digital Twin
  URL: /hq/telemetry    Title: Antarctic Digital Twin

Consistency Rule Violated:
.agents/frontend/SKILL.md §Craft Checklist; Accessibility WCAG 2.4.2 (Page Titled).

Root Cause Hypothesis:
`render_hq` helper in `hq/router.py` omitted the `title` parameter.

Recommended Fix:
Update `render_hq` in `app/routers/hq/router.py`:
```python
def render_hq(request: Request, name: str):
    return templates.TemplateResponse(
        request=request,
        name=f"hq/{name}.html",
        context={
            "station_id": "hq",
            "title": f"NCPOR HQ - {name.replace('_', ' ').title()}",
        },
    )
```

Regression Check:
Every HQ tab displays a unique, informative title in the browser tab bar.
Dependencies: None.
```

---

```text
ID: FE-ROUTE-006
Title: Full-page Stitch mockups inside modal dialogs pollute global DOM on all views
Severity: P1 (High)
Status: Open

Route: All dashboard views
Component: Master Dashboard Layout Modal Includes
File:
- app/templates/layouts/dashboard.html (Lines 16-22)
- app/templates/components/modals/alert_dialog.html
- app/templates/components/modals/asset_detail.html
Viewport: All
Browser: All

Category: Accessibility / HTML Semantics

Expected:
Modal dialog templates should contain strictly dialog content (card wrapper, close button, body content, action buttons).

Actual:
Both modal files contain complete exported Stitch web pages with redundant `<header>`, `<aside>`, and `<h1>` tags. Because `layouts/dashboard.html` includes them unconditionally via `<dialog>`, every single page in the application contains three distinct `<header>` tags and two distinct `<aside>` sidebars in its DOM tree.

Reproduction:
1. Open DevTools on any page (e.g. `/maitri/energy`).
2. Search DOM for `<header>`.
3. Observe 3 separate header tags in the DOM.
4. Observe the second header is inside `<dialog id="dtfias_asset_modal">` containing the full Bharati layout.

Evidence:
- DOM Inspection of `/maitri/energy`:
  Header 1: Line 1 of `topnav.html`
  Header 2: Line 1 of `alert_dialog.html` (inside `<dialog id="dtfias_alert_modal">`)
  Header 3: Line 1 of `asset_detail.html` (inside `<dialog id="dtfias_asset_modal">`)

Consistency Rule Violated:
HTML5 Semantic Specification (one primary `<header>` per landmark context); .agents/frontend/SKILL.md §Accessibility.

Root Cause Hypothesis:
Stitch exported entire screens for modals instead of isolated dialog components. The developer included them directly without stripping out the outer page chrome.

Recommended Fix:
Strip the outer `<header>`, `<aside>`, and `<main class="pt-14 pl-72">` wrappers from `alert_dialog.html` and `asset_detail.html`, retaining only the inner modal card content.

Regression Check:
DOM search for `<header>` on dashboard pages returns exactly one visible topnav header.
Dependencies: None.
```

---

## 5. Strategic Remediation Plan

To resolve all non-working routes and restore full frontend integrity:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ROUTE REPAIR IMPLEMENTATION PLAN                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 1: Add Missing Routes to Station Routers (Fixes FE-ROUTE-001 & 002)     │
│   - In `app/routers/bharati/router.py` & `app/routers/maitri/router.py`:     │
│       * Wire `/infrastructure` -> `render_station(request, "infrastructure")`│
│       * Wire `/environment`    -> `render_station(request, "environment")`   │
│       * Wire `/logistics`      -> `render_station(request, "logistics")`     │
│   - In `dashboard.py` files:                                                │
│       * Add `@router.get("/dashboard")` alias decorator                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 2: Un-orphan Templates & Restore HQ Routing (Fixes FE-ROUTE-003)        │
│   - In `app/routers/hq/router.py`:                                          │
│       * Change `/hq/roles` redirect to render `hq/roles.html`               │
│       * Change `/hq/reports` redirect to render `hq/reports.html`           │
│   - In `app/templates/components/sidebar_hq.html`:                          │
│       * Un-comment the `/hq/simulations` link                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 3: Parameterize Station Identity (Fixes FE-ROUTE-004)                   │
│   - In `app/templates/station/*`:                                           │
│       * Add Jinja conditionals to distinguish Maitri & Bharati equipment    │
│       * Replace hardcoded coordinates with `{{ station.coordinates }}`       │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 4: Fix Page Titles & Clean Modal DOM (Fixes FE-ROUTE-005 & 006)         │
│   - In `app/routers/hq/router.py`:                                          │
│       * Update `render_hq` to pass dynamic `title` in context               │
│   - In `app/templates/components/modals/*`:                                 │
│       * Strip full-page chrome (`<header>`, `<aside>`) from modal files     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Sign-off & Handoff
* **Report Compiled By:** Frontend Testing Agent
* **Consumer:** Frontend Inconsistency Manager / Engineering Team
* **Status:** Verified with automated test evidence and empirical HTTP captures.
