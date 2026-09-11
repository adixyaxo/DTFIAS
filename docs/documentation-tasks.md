# DTFIAS: Master Documentation Tasks Ledger

> **Document Status:** Authoritative Documentation Inconsistency Ledger & Gap Tracking System  
> **Target Path:** `docs/documentation-tasks.md`  
> **Owner Agent:** Documentation Agent (`.agents/agents/DocumentationAgent/agent.md`)  
> **Associated Master Index:** [`docs/DOCUMENTATION-INDEX.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/DOCUMENTATION-INDEX.md)  
> **Last Verified:** September 2026  

---

## 1. Documentation Tasks Inventory

### DOC-001
- **ID:** DOC-001
- **Document:** `docs/architecture.md`, `GEMINI.md`, `CLAUDE.md`, `docs/database.md`
- **Status:** RESOLVED
- **Priority:** CRITICAL (P0)
- **Source:** Three-way architectural schema contradiction between early 5-table draft and 25-table v1 Lock.
- **Gap:** `architecture.md` §8 defined a toy 5-table schema with `BIGSERIAL` keys, while `database.md` defined 25 normalized tables with UUIDs.
- **Required Action:** Re-write `architecture.md` §8 and update Constraint C2 across agent contracts to reference the canonical 25-table v1 Lock schema.
- **Affected Code:** `docs/architecture.md`, `GEMINI.md`, `CLAUDE.md`
- **Owner Agent:** Documentation Agent
- **Verification:** Grep checks on C2 show uniform UUID foreign keys (`station_id UUID REFERENCES stations(id) NOT NULL`).

---

### DOC-002
- **ID:** DOC-002
- **Document:** `.agents/frontend/SKILL.md`, `.agents/brand_design/SKILL.md`
- **Status:** RESOLVED
- **Priority:** CRITICAL (P0)
- **Source:** Design system conflict between generic frontend skill and DTFIAS institutional brand palette.
- **Gap:** `.agents/frontend/SKILL.md` instructed agents to avoid cream backgrounds (`#F5F2EB`) and Inter as generic "AI slop", causing agents to reject official tokens.
- **Required Action:** Inject an explicit DTFIAS Project Brand Override at the top of `.agents/frontend/SKILL.md` establishing `--brand-cream` and the 4-tier typography stack.
- **Affected Code:** `.agents/frontend/SKILL.md`, `app/static/css/app.css`
- **Owner Agent:** Documentation Agent
- **Verification:** DTFIAS override block present and respected in `.agents/frontend/SKILL.md`.

---

### DOC-003
- **ID:** DOC-003
- **Document:** `scripts/migrations/README.md`
- **Status:** RESOLVED
- **Priority:** HIGH (P1)
- **Source:** CLI command error in database setup instructions.
- **Gap:** README instructed running `psql "postgresql+asyncpg://..."`, which causes `psql` to crash due to an unrecognized driver scheme.
- **Required Action:** Update instructions to use `postgresql://...` for `psql` and document the driver scheme distinction.
- **Affected Code:** `scripts/migrations/README.md`
- **Owner Agent:** Documentation Agent
- **Verification:** `psql` command runs validly with standard URI.

---

### DOC-004
- **ID:** DOC-004
- **Document:** `docs/frontend-endpoints.md`
- **Status:** RESOLVED
- **Priority:** HIGH (P1)
- **Source:** Frontend endpoint catalog audit.
- **Gap:** Contained 35 instances of the typo "ANARCTIC", unrendered AI citation tags (`filecite...`), and claimed Inter was the only system font.
- **Required Action:** Correct typos to DTFIAS, strip citation tags, and document the 4-tier typography system.
- **Affected Code:** `docs/frontend-endpoints.md`
- **Owner Agent:** Documentation Agent
- **Verification:** Zero matches for "ANARCTIC" or filecite tags.

---

### DOC-005
- **ID:** DOC-005
- **Document:** `docs/2dFrontend.md`
- **Status:** RESOLVED
- **Priority:** HIGH (P1)
- **Source:** 2.5D Digital Twin implementation specification.
- **Gap:** Specification referenced non-existent files (`1-project-overview.md`, `4-stations-and-headquarters.md`), proposed React `.tsx` components, and quoted unrealistic Bharati generator figures.
- **Required Action:** Reconcile stack to FastAPI + Jinja2 + Alpine.js, align power parameters (340 kW capacity, ~282.4 kW load), and link to in-repo canonical documents.
- **Affected Code:** `docs/2dFrontend.md`
- **Owner Agent:** Documentation Agent
- **Verification:** All markdown links in `docs/2dFrontend.md` resolve to valid repository paths.

---

### DOC-006
- **ID:** DOC-006
- **Document:** `docs/station-facts-and-research.md`
- **Status:** RESOLVED
- **Priority:** HIGH (P1)
- **Source:** Missing authoritative polar research reference (`4-stations-and-headquarters.md`).
- **Gap:** Prompts and specifications required grounding in station facts from `4-stations-and-headquarters.md`, which was missing from the repository.
- **Required Action:** Author `docs/station-facts-and-research.md` detailing NCPOR governance, Bharati, Maitri, SATCOM links, and separating real facts from simulated telemetry.
- **Affected Code:** `docs/station-facts-and-research.md`
- **Owner Agent:** Documentation Agent
- **Verification:** File exists, validated against MoES/NCPOR institutional records and `shared/constants/stations.py`.

---

### DOC-007
- **ID:** DOC-007
- **Document:** `docs/operations.md`
- **Status:** RESOLVED
- **Priority:** MEDIUM (P2)
- **Source:** Operations & Deployment domain requirements in `DocumentationAgent/agent.md`.
- **Gap:** No consolidated manual existed for environment variables, Docker deployment, local setup, observability, and SATCOM failure modes.
- **Required Action:** Author `docs/operations.md` covering all operational domains without exposing secrets.
- **Affected Code:** `docs/operations.md`
- **Owner Agent:** Documentation Agent
- **Verification:** File exists and covers Docker, environment variables, health checks, and failure modes.

---

### DOC-008
- **ID:** DOC-008
- **Document:** `docs/testing/test-strategy.md`
- **Status:** RESOLVED
- **Priority:** MEDIUM (P2)
- **Source:** Testing domain requirements in `DocumentationAgent/agent.md`.
- **Gap:** `docs/testing/` contained defect analyses but lacked a canonical quality strategy defining the testing pyramid, coverage thresholds, and DoD checks.
- **Required Action:** Author `docs/testing/test-strategy.md` linking unit, integration, and E2E suites with mechanical constraint verification.
- **Affected Code:** `docs/testing/test-strategy.md`
- **Owner Agent:** Documentation Agent
- **Verification:** File exists and establishes coverage goals (90% domain, 80% global).

---

### DOC-009
- **ID:** DOC-009
- **Document:** `docs/api-contracts.md`
- **Status:** RESOLVED
- **Priority:** HIGH (P1)
- **Source:** Backend domain requirements in `DocumentationAgent/agent.md`.
- **Gap:** No centralized inventory existed for backend REST endpoints, SSE streams, unified error envelopes, and RBAC permission mappings.
- **Required Action:** Author `docs/api-contracts.md` documenting all portal routes, payload schemas, and server-side station scoping.
- **Affected Code:** `docs/api-contracts.md`
- **Owner Agent:** Documentation Agent
- **Verification:** File exists, aligned with Constraints C3, C4, C5, and C14.

---

### DOC-010
- **ID:** DOC-010
- **Document:** `docs/project-overview.md`
- **Status:** RESOLVED
- **Priority:** MEDIUM (P2)
- **Source:** Project domain requirements in `DocumentationAgent/agent.md`.
- **Gap:** Problem statement, project boundaries, and explicit exclusions (e.g. AGEOS Earth Observation) were dispersed across informal notes.
- **Required Action:** Author `docs/project-overview.md` defining the SIH26060 charter, scope boundaries, and core terminology.
- **Affected Code:** `docs/project-overview.md`
- **Owner Agent:** Documentation Agent
- **Verification:** File exists with clear in-scope and non-goal definitions.

---

### DOC-011
- **ID:** DOC-011
- **Document:** `docs/testing/backend-inconsistencies.md`, `app/models/`
- **Status:** RESOLVED
- **Priority:** CRITICAL (P0)
- **Source:** Implementation audit vs `docs/database.md` v1 Lock.
- **Gap:** 23 out of 25 database entities defined in `001_initial_schema.sql` lack corresponding SQLAlchemy ORM models in `app/models/`.
- **Required Action:** Backend implementation team to generate SQLAlchemy 2.0 models for all 25 tables.
- **Affected Code:** `app/models/`
- **Owner Agent:** Backend Inconsistency Manager / Backend Testing Agent
- **Verification:** Models importable and mapped to all tables in `001_initial_schema.sql` (36 tables mapped).

---

### DOC-012
- **ID:** DOC-012
- **Document:** `docs/testing/backend-inconsistencies.md`, `engine/`
- **Status:** OPEN (TRACKED)
- **Priority:** HIGH (P1)
- **Source:** Implementation audit vs `docs/architecture.md`.
- **Gap:** "Ghost Engine": Core services (Energy, Alert, Command) are implemented, but remaining domain services (Environment, Infrastructure, Logistics, User), processing pipelines, and simulators are 0-byte stub files.
- **Required Action:** Implement remaining domain services and simulation components in `engine/`.
- **Affected Code:** `engine/services/core/`, `engine/simulation/`, `engine/processing/`
- **Owner Agent:** Backend Team
- **Verification:** Grep shows zero 0-byte files in `engine/`.

---

### DOC-013
- **ID:** DOC-013
- **Document:** `docs/testing/backend-inconsistencies.md`, `app/routers/`
- **Status:** RESOLVED
- **Priority:** CRITICAL (P0)
- **Source:** Security audit vs Constraint C5.
- **Gap:** Router-level role guards (`require_role`) are commented out on `/maitri`, `/bharati`, and `/hq`. `infrastructure/security/authorization/rbac.py` returns a hardcoded mock dict.
- **Required Action:** Implement live JWT/session role extraction and attach `dependencies=[Depends(require_role(...))]` on APIRouters.
- **Affected Code:** `app/routers/maitri/router.py`, `app/routers/bharati/router.py`, `app/routers/hq/router.py`, `infrastructure/security/authorization/rbac.py`
- **Owner Agent:** Backend / Security Team
- **Verification:** Unauthenticated requests to portal routes return `401/403`.

---

### DOC-014
- **ID:** DOC-014
- **Document:** `docs/testing/backend-inconsistencies.md`, `infrastructure/security/audit/`
- **Status:** RESOLVED
- **Priority:** CRITICAL (P0)
- **Source:** Compliance audit vs Constraint C7.
- **Gap:** `infrastructure/security/audit/audit_log.py` is 0 bytes; zero audit log rows are written on login, command issuance, or state mutation.
- **Required Action:** Implement `dispatch_audit_log` service writing rows to `audit_logs` table asynchronously.
- **Affected Code:** `infrastructure/security/audit/audit_log.py`, `app/routers/auth/auth.py`, `app/routers/hq/router.py`
- **Owner Agent:** Backend / Security Team
- **Verification:** Mutation endpoints insert a verified row in `audit_logs`.

---

### DOC-015
- **ID:** DOC-015
- **Document:** `docs/testing/backend-inconsistencies.md`, `infrastructure/resilience/`
- **Status:** OPEN (TRACKED)
- **Priority:** HIGH (P1)
- **Source:** Polar resilience architecture vs `docs/architecture.md` §7.
- **Gap:** `infrastructure/resilience/in_process_write_buffer.py` is 0 bytes; no store-and-forward queue exists to handle SATCOM dropouts.
- **Required Action:** Implement in-memory / disk-backed bounded write buffer with retry backoff and flush mechanism.
- **Affected Code:** `infrastructure/resilience/in_process_write_buffer.py`
- **Owner Agent:** Backend Team
- **Verification:** Unit tests confirm buffer queues readings on simulated network failure and flushes upon recovery.
