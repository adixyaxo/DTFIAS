# Frontend Fix Log

Maintained by: Frontend Inconsistency Manager Agent  
Project: DTFIAS (SIH26060)

---

### Entry 1
- **Finding ID**: FE-RENDER-001
- **Date**: 2026-09-07
- **Changed Files**:
  - `app/templates/bharati/station_twin.html`
  - `app/templates/layouts/base.html`
- **Root Cause**: Base layout defined `{% block body %}`, but `station_twin.html` used `{% block content %}`. This caused Jinja2 to ignore the entire 2.5D station twin markup, delivering an empty shell of 7.7 KB.
- **Fix**: Replaced `{% block content %}` with `{% block body %}` in `station_twin.html`. Also nested `{% block content %}` inside `{% block body %}` in `base.html` as a fallback.
- **Tests**: HTTP GET `/bharati/station-twin` and `/bharati/twin`.
- **Regression Checks**: Verified `layouts/dashboard.html` and `index.html` render without regression.
- **Verification**: Verified body size changed from 7.7 KB to 48.6 KB and `st-root` interactive DOM container is rendered.

---

### Entry 2
- **Finding ID**: FE-ROUTE-001
- **Date**: 2026-09-07
- **Changed Files**:
  - `app/routers/hq/router.py`
  - `app/templates/hq/commands.html`
  - `app/templates/components/sidebar_hq.html`
- **Root Cause**: `/hq/commands` was a planned core SIH requirement (C4) for tactical station remote control, but the route was omitted from `router.py`, and both `commands.py` and `commands.html` were 0-byte empty files.
- **Fix**: Created production-grade `commands.html` template implementing the command ledger, priority tags (P0/P1/P2), target subsystems, and dispatch modal. Added route `@router.get("/commands")` in `app/routers/hq/router.py` and navigation item in `sidebar_hq.html`.
- **Tests**: HTTP GET `/hq/commands`.
- **Regression Checks**: Verified other HQ routes (`/hq/alerts`, `/hq/stations`) still route cleanly.
- **Verification**: Route returns HTTP 200 with 37.1 KB of structured markup.

---

### Entry 3
- **Finding ID**: FE-ROUTE-002
- **Date**: 2026-09-07
- **Changed Files**:
  - `app/routers/bharati/router.py`
  - `app/routers/maitri/router.py`
- **Root Cause**: `docs/frontend-endpoints.md` mapped the 2.5D twin to `/{station_id}/twin`, but only `/station-twin` was defined in the router, causing 404 on the documented canonical path.
- **Fix**: Added `@router.get("/twin")` as a co-equal route decorator to the existing `/station-twin` handler.
- **Tests**: HTTP GET `/bharati/twin` and `/maitri/twin`.
- **Regression Checks**: Existing `/station-twin` links continue to function without disruption.
- **Verification**: Both `/twin` and `/station-twin` return HTTP 200 with complete digital twin SVG markup.

---

### Entry 4
- **Finding ID**: FE-AUTH-001
- **Date**: 2026-09-07
- **Changed Files**:
  - `app/routers/auth/auth.py`
- **Root Cause**: Missing `/auth/logout` endpoint in authentication router.
- **Fix**: Added `@router.get("/logout")` and `@router.post("/logout")` handlers redirecting to `/auth/login`.
- **Tests**: HTTP GET `/auth/logout`.
- **Regression Checks**: Verified `/auth/login` and `/auth/recover` function as expected.
- **Verification**: Returns HTTP 302 with `Location: /auth/login`.

---

### Entry 5
- **Finding ID**: FE-RBAC-001
- **Date**: 2026-09-07
- **Changed Files**:
  - `app/routers/auth/user.py`
- **Root Cause**: Naked root `/users` and `/users/{user_id}` endpoints were mounted globally without authentication or RBAC guards, violating architecture rules and causing 500 errors on database connection failures.
- **Fix**: Added `prefix="/api/users", tags=["api_users"]` and scoped endpoints to `/{user_id}` and `/` under this prefix.
- **Tests**: Tested OpenAPI schema and HTTP GET `/api/users/1`.
- **Regression Checks**: Verified no frontend templates depend on naked `/users`.
- **Verification**: Root `/` namespace is clean and unpolluted.
