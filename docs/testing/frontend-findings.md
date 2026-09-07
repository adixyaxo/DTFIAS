# Frontend Findings & Consistency Audit

Author: Frontend Inconsistency Manager Agent / Frontend Testing Agent  
Date: 2026-09-07  
Project: Digital Twin for Indian Antarctic Stations (SIH26060)

---

## Summary of Findings

| ID | Title | Severity | Category | Status |
|---|---|---|---|---|
| **FE-RENDER-001** | `bharati/station_twin.html` block name mismatch caused blank page | P0 | Functional / Rendering | Fixed & Verified |
| **FE-ROUTE-001** | Missing `/hq/commands` route and empty template stubs | P1 | Functional / Routing | Fixed & Verified |
| **FE-ROUTE-002** | Station twin URL mismatch (`/station-twin` vs canonical `/twin`) | P2 | Navigation / Contract | Fixed & Verified |
| **FE-AUTH-001** | Missing `/auth/logout` endpoint in authentication router | P2 | Functional / Auth | Fixed & Verified |
| **FE-RBAC-001** | Unauthenticated `/users` and `/users/{user_id}` routes exposed on root | P1 | Security / RBAC | Fixed & Verified |
| **FE-SCOPE-001** | Unnecessary / Extra routes in station routers (`/personnel`, `/health`, `/research`, `/telemetry`) | P3 | Architecture / Scope | Documented |
| **FE-SCOPE-002** | Unnecessary / Extra routes in HQ router (`/simulations`, `/research`, `/health`, `/reports`, `/roles`, `/settings`) | P3 | Architecture / Scope | Documented |

---

### Finding FE-RENDER-001: Bharati 2.5D Twin Rendered Blank (Block Mismatch)
- **ID**: `FE-RENDER-001`
- **Title**: Station Twin template overrides `{% block content %}` instead of `{% block body %}`
- **Severity**: P0
- **Status**: Fixed
- **Route**: `/bharati/station-twin`, `/bharati/twin`
- **Component**: Bharati 2.5D Interactive Station Twin
- **File**: `app/templates/bharati/station_twin.html`
- **Expected**: Complete 2.5D station twin schematic with telemetry bars, layer filters, and SVG hotspots.
- **Actual**: Returned only 7.7 KB containing the HTML head shell with 0 bytes inside body.
- **Root Cause**: `app/templates/layouts/base.html` defines `{% block body %}`, while `station_twin.html` defined `{% block content %}`.
- **Fix**: Changed block in `app/templates/bharati/station_twin.html` to `{% block body %}`, and nested `{% block content %}` inside `{% block body %}` in `base.html` as a defensive fallback.
- **Verification**: Retested via HTTP GET. Response body size increased from 7.7 KB to 48.6 KB; verified `station-twin` root container is present.

---

### Finding FE-ROUTE-001: Missing HQ Tactical Commands Route & 0-Byte Stubs
- **ID**: `FE-ROUTE-001`
- **Title**: `/hq/commands` route missing from `app/routers/hq/router.py` and template was 0 bytes
- **Severity**: P1
- **Status**: Fixed
- **Route**: `/hq/commands`
- **Component**: HQ Remote Command & Control Console
- **File**: `app/routers/hq/router.py`, `app/templates/hq/commands.html`, `app/templates/components/sidebar_hq.html`
- **Expected**: Operational command dispatch interface supporting command lifecycle states (`SENT`, `RECEIVED`, `EXECUTING`, `EXECUTED`, `REJECTED`, `FAILED`), station targeting, and cryptographic audit log link.
- **Actual**: `commands.html` was 0 bytes, `commands.py` was 0 bytes, and route `/hq/commands` was omitted from the router and sidebar.
- **Fix**: Implemented full `commands.html` matching design system, added `@router.get("/commands")` to `app/routers/hq/router.py`, and added navigation item in `sidebar_hq.html`.
- **Verification**: Verified via HTTP GET: status 200, length 37.1 KB, verified dispatch modal and command ledger rendering.

---

### Finding FE-ROUTE-002: Digital Twin Canonical URL Discrepancy
- **ID**: `FE-ROUTE-002`
- **Title**: Documented route `/{station_id}/twin` resulted in 404
- **Severity**: P2
- **Status**: Fixed
- **Route**: `/maitri/twin`, `/bharati/twin`
- **Component**: Station Navigation
- **File**: `app/routers/maitri/router.py`, `app/routers/bharati/router.py`
- **Expected**: Navigating to either `/{station_id}/twin` (per `docs/frontend-endpoints.md`) or `/{station_id}/station-twin` renders the digital twin.
- **Actual**: Only `/station-twin` was defined; `/twin` returned 404.
- **Fix**: Added `@router.get("/twin")` alongside `@router.get("/station-twin")` in both routers.
- **Verification**: Verified both `/bharati/twin` and `/maitri/twin` return 200 with complete markup.

---

### Finding FE-AUTH-001: Missing `/auth/logout` Route
- **ID**: `FE-AUTH-001`
- **Title**: No session termination or logout route defined
- **Severity**: P2
- **Status**: Fixed
- **Route**: `/auth/logout`
- **File**: `app/routers/auth/auth.py`
- **Expected**: GET or POST `/auth/logout` terminates the session and redirects to `/auth/login`.
- **Actual**: Route returned 404.
- **Fix**: Added `GET` and `POST` handlers for `/auth/logout` returning a 302 redirect to `/auth/login`.
- **Verification**: Verified HTTP GET `/auth/logout` returns 302 with `Location: /auth/login`.

---

### Finding FE-RBAC-001: Naked Root `/users` Endpoint Exposing Direct Database Operations
- **ID**: `FE-RBAC-001`
- **Title**: Unauthenticated root CRUD `/users` and `/users/{user_id}` mounted without RBAC
- **Severity**: P1
- **Status**: Fixed
- **Route**: `/users`, `/users/{user_id}`
- **File**: `app/routers/auth/user.py`, `app/main_router.py`
- **Expected**: All user administration belongs inside `/hq/users` behind `hq_admin` RBAC.
- **Actual**: Root `/users` was directly mounted to `main_router`, bypassing prefix and crashing when accessing DB without active Supabase credentials.
- **Fix**: Namespaced the CRUD router under `prefix="/api/users", tags=["api_users"]` away from the root application namespace.
- **Verification**: Verified openapi schema confirms root is unpolluted.

---

### Finding FE-SCOPE-001: Extra / Redundant Routes in Station Portals
- **ID**: `FE-SCOPE-001`
- **Title**: Station routers declare dummy placeholder sub-routes not planned in architecture
- **Severity**: P3
- **Status**: Documented for Pruning
- **Routes**:
  - `/{station_id}/personnel` (Extra: mapped in `docs/frontend-endpoints.md` into `/{station_id}/logistics`)
  - `/{station_id}/health` (Extra: dummy stub; health is a sub-widget in logistics/roster)
  - `/{station_id}/research` (Extra: dummy stub; station science downlinks directly)
  - `/{station_id}/telemetry` (Redundant: telemetry is already integrated per subsystem)
- **Recommendation**: In future cleanup, consolidate these back into the 6 canonical station routes: `dashboard`, `twin`, `energy`, `infrastructure`, `environment`, `logistics`, `alerts`.

---

### Finding FE-SCOPE-002: Extra / Redundant Routes in HQ Portal
- **ID**: `FE-SCOPE-002`
- **Title**: HQ router declares non-contractual simulation and placeholder endpoints
- **Severity**: P3
- **Status**: Documented for Pruning
- **Routes**:
  - `/hq/simulations` (Extra: out-of-scope Param Shivay HPC simulation job queue)
  - `/hq/research` (Extra: non-contractual science dashboard)
  - `/hq/health` (Extra: duplicate of personnel status)
  - `/hq/reports` (Redundant: duplicates `/hq/compliance`)
  - `/hq/roles` (Redundant: duplicates `/hq/users` which already contains RBAC matrix)
  - `/hq/settings` (Extra: configuration is managed via backend environment)
- **Recommendation**: Keep canonical HQ routes: `dashboard`, `stations`, `energy`, `environment`, `logistics`, `compliance`, `alerts`, `commands`, `assets`, `users`, `audit`, `telemetry`.
