# Dispatch Instructions — Reviewer Agent (reviewer_perf_1)
## Phase 5: Code & Architecture Review

## Working Directory
`c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\reviewer_perf_1`

## Project Root
`c:\Users\adity\Documents\Coding\Projects\DTFIAS`

## Mission & Scope
Perform an objective and rigorous review of the changes implemented in Phase 3 and Phase 3.5 across:
- `app/routers/` (`auth/`, `hq/`, `maitri/`, `bharati/`)
- `app/models/` (`command.py`, `telemetry.py`, `alert.py`, `audit.py`)
- `app/schemas/` (`command.py`, `user.py`)
- `app/templates/` (`layouts/base.html`, `layouts/dashboard.html`, `layouts/partial.html`, `layouts/partial_twin.html`)
- `infrastructure/security/authorization/rbac.py`
- `infrastructure/database/postgres/`
- `tests/` (`tests/unit/test_perf_fixes.py`, `tests/unit/test_spa_navigation.py`)

## Evaluation Criteria
1. Correctness and Robustness of fixes.
2. 4-Layer Architecture compliance (app -> engine -> infrastructure -> shared).
3. GEMINI.md hard constraints:
   - C1: zero fastapi/sqlalchemy/asyncpg/jinja2 in `engine/**`
   - C8: parameterized SQL / ORM only (zero f-strings)
   - C3: station_id set server-side only
   - C5: Role guards on APIRouter via dependencies=
   - C7: State-changing fixes write audit_logs
   - C10/C11: Cookie (httponly, secure, samesite=strict) and CSRF intact
   - C16: Lazy Three.js loading preserved
4. Run tests: `pytest tests/unit/` or full suite to verify.
5. Provide your verdict: `APPROVE` or `REQUEST_CHANGES`.

Write `handoff.md` in your working directory and send a message back with your verdict.

## 2026-09-13T17:24:43Z
<USER_REQUEST>
You are the Reviewer Agent (reviewer_perf_1) for Phase 5 verification of DTFIAS performance optimizations.

Working directory:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\reviewer_perf_1

Please read your dispatch instructions at:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\reviewer_perf_1\DISPATCH.md
and read GEMINI.md at:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\GEMINI.md
and read the original request at:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\ORIGINAL_REQUEST.md

Review all changes across routers, models, schemas, templates, RBAC, and tests.
Check correctness, robustness, layer boundaries, and GEMINI.md constraints (C1, C8, C3, C5, C7, C10, C11, C16).
Run tests to verify.
Deliver your verdict (APPROVE / REQUEST_CHANGES) in handoff.md and send_message.
</USER_REQUEST>
