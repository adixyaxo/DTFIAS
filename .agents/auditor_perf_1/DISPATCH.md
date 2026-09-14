# Dispatch Instructions — Forensic Auditor (auditor_perf_1)
## Phase 5: Integrity & Forensic Audit

## Working Directory
`c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\auditor_perf_1`

## Project Root
`c:\Users\adity\Documents\Coding\Projects\DTFIAS`

## Mission & Scope
Perform forensic verification of all Phase 3, 3.5, and Phase 4 artifacts:
1. Verify Authenticity:
   - Check that optimizations are genuine (real database indexes in models, real async Argon2 offload, real template branching, real SPA navigation in base.html, real RBAC JWT optimization).
   - Verify that `perf_baseline.json` and `perf_after.json` contain genuine measurements and are not hardcoded or fabricated.
2. Verify GEMINI.md Hard Constraints:
   - C1: `grep -rE "^(import|from) (fastapi|sqlalchemy|asyncpg|jinja2)" engine/` MUST return 0.
   - C8: `grep -rn "execute(f\"" app/ engine/ infrastructure/` MUST return 0.
   - C3: `station_id` set server-side only.
   - C5: Role guards on APIRouter level.
   - C7: Audit logging on state writes intact.
   - C10/C11: Cookies (httponly, secure, samesite=strict) and CSRF intact.
   - C13/C14: No service role keys or client libraries in frontend.
   - C16: Lazy Three.js loading preserved.
3. Provide your verdict: `CLEAN` or `INTEGRITY VIOLATION`.

Write `handoff.md` in your working directory and report your verdict via `send_message`.

## 2026-09-13T17:24:44Z
<USER_REQUEST>
You are the Forensic Auditor (auditor_perf_1) for Phase 5 integrity verification of DTFIAS performance optimizations.

Working directory:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\auditor_perf_1

Please read your dispatch instructions at:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\auditor_perf_1\DISPATCH.md
and read GEMINI.md at:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\GEMINI.md
and read the original request at:
c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\ORIGINAL_REQUEST.md

Verify authentic implementation vs cheating / hardcoded values.
Verify that perf_baseline.json and perf_after.json are genuine live measurements.
Verify GEMINI.md constraints (C1, C8, C3, C5, C7, C10, C11, C13, C14, C16).
Deliver your verdict (CLEAN / INTEGRITY VIOLATION) in handoff.md and send_message.
</USER_REQUEST>
