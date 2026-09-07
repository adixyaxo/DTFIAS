# DTFIAS: Master Backend Inconsistencies Report

> **Document Status:** Authoritative Master Inconsistency Audit & Architecture Gap Analysis  
> **Target Path:** `docs/testing/backend-inconsistencies.md`  
> **Author:** Backend Testing Agent & Backend Inconsistency Manager Agent  
> **Date:** September 2026  
> **Primary References:**
> - [Backend Findings Ledger](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/testing/backend-findings.md)
> - [Triangulated Backend Deep Analysis](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/testing/aim-vs-desired-vs-actual-backend-deep-analysis.md)
> - [Architecture Contract](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/architecture.md)
> - [Database Design Specification](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/database.md)
> - [Gemini Agent Guidelines](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/GEMINI.md)

---

## 1. Executive Summary

A comprehensive architectural and code-level audit of the backend for the **Digital Twin for Indian Antarctic Stations (DTFIAS — SIH26060)** was conducted, evaluating the codebase against the architectural specifications (`docs/architecture.md`), database design (`docs/database.md`), agent skills (`.agents/fastapi/SKILL.md`, `.agents/database/SKILL.md`), and core behavioral rules (`GEMINI.md`).

The audit revealed that while the project possesses a mature database migration script (`scripts/migrations/001_initial_schema.sql`) and well-styled frontend views, **the backend implementation itself is largely a hollow scaffolding shell exhibiting critical architectural, security, and data contract discrepancies**.

### Key Findings at a Glance:
1. **Architectural Layer Inversion:** Lower-level database connection code (`infrastructure/database/postgres/`) imports from the high-level interface layer (`app/config/database.py`), violating the clean 4-layer DDD contract.
2. **The "Ghost Engine":** 90% of files in `engine/` (services, repositories, protocols, ingestion pipelines, simulators) are empty 0-byte files. The interface layer (`app/routers/`) completely bypasses the engine.
3. **Three-Way Database Schema Fracture:** An irreconcilable contradiction exists between `docs/architecture.md` (5 monolithic tables with integer IDs and enum station scoping), `docs/database.md` (25 normalized tables with UUIDs and Supabase Auth profiles), and `app/models/` (a toy integer user model).
4. **95% Missing ORM Models & Schemas:** 23 out of 25 database entities have zero SQLAlchemy models and zero Pydantic validation schemas.
5. **Disabled Security & Mock RBAC:** Router-level role guards (`require_role`) are commented out on all station and HQ routers. The security module uses a hardcoded mock dictionary returning `"maitri_operator"`, leaving all portals publicly accessible.
6. **Zero Audit & Compliance Logging:** `audit_log.py` is 0 bytes; zero audit rows are recorded anywhere, violating polar life-safety compliance (Constraint C7).
7. **Missing Realtime & Store-and-Forward Sync:** Neither the `/stream` SSE endpoints nor the SATCOM store-and-forward write buffer (`in_process_write_buffer.py`) is implemented.
8. **Broken Container Build & Test Runner:** `Dockerfile` attempts an `npm install` on a non-existent `package.json`, and `pytest` fails with an I/O error on a closed file.

---

## 2. Master Inconsistencies Matrix

| ID | Severity | Area / Domain | Short Description | Affected Files | Status |
|:---|:---:|:---|:---|:---|:---:|
| **BE-LAYER-001** | **CRITICAL (P0)** | Architecture / Layering | Inverted dependency: `infrastructure/` imports from `app.config.database` | `infrastructure/database/postgres/connection.py`, `session.py` | **OPEN** |
| **BE-LAYER-002** | **CRITICAL (P0)** | Architecture / DDD | Complete engine bypass: Routes query ORM directly or return static views | `app/routers/auth/user.py`, `maitri/router.py`, `bharati/router.py`, `hq/router.py` | **OPEN** |
| **BE-LAYER-003** | **LOW (P3)** | Architecture / Hygiene | Legacy MySQL artifacts lingering in repo | `infrastructure/database/mysql/`, `tests/integration/mysql/` | **OPEN** |
| **BE-ENGINE-001** | **CRITICAL (P0)** | Domain Engine | "Ghost Engine": 90% of engine files are 0-byte stubs | `engine/services/*`, `engine/interfaces/*`, `engine/processing/*`, `engine/simulation/*` | **OPEN** |
| **BE-ENGINE-002** | **HIGH (P1)** | Domain Engine / Typing | Class overwrite & Pydantic V1 syntax in User entity | `engine/domain/users/user.py` | **OPEN** |
| **BE-DB-001** | **CRITICAL (P0)** | Database / Schema | Architectural schema fracture resolved: `architecture.md` aligned to `database.md` v1 Lock | `docs/architecture.md`, `docs/database.md` | **RESOLVED (DOCS ALIGNED)** |
| **BE-DB-002** | **CRITICAL (P0)** | Database / ORM | 95% missing SQLAlchemy ORM models (only 2 stub models exist) | `app/models/` | **OPEN** |
| **BE-DB-003** | **HIGH (P1)** | Database / Schemas | Missing Pydantic V2 validation schemas for Telemetry, Commands, and Stations | `app/schemas/user.py`, `test.py` | **OPEN** |
| **BE-DB-004** | **MEDIUM (P2)** | Database / Config | Misplacement of DB engine in `app/config/` instead of `infrastructure/` | `app/config/database.py` | **OPEN** |
| **BE-AUTH-001** | **CRITICAL (P0)** | Security / RBAC | Missing router-level role guards on Maitri, Bharati, and HQ routers (C5) | `app/routers/maitri/router.py`, `bharati/router.py`, `hq/router.py` | **OPEN** |
| **BE-AUTH-002** | **CRITICAL (P0)** | Security / RBAC | Mock RBAC returning hardcoded dummy dict `test_user` | `infrastructure/security/authorization/rbac.py` | **OPEN** |
| **BE-AUTH-003** | **HIGH (P1)** | Security / Auth | Dummy auth router: login returns message, logout does not clear cookies | `app/routers/auth/auth.py` | **OPEN** |
| **BE-AUTH-004** | **CRITICAL (P0)** | Security / Passwords | Missing Argon2 password hashing implementation (C6) | `infrastructure/security/authentication/passwords.py` | **OPEN** |
| **BE-SEC-001** | **CRITICAL (P0)** | Security / Audit | Zero audit logging across entire application (C7) | `infrastructure/security/audit/audit_log.py` | **OPEN** |
| **BE-SEC-002** | **HIGH (P1)** | Security / Middleware | Missing CSRF protection, secure cookie configuration, and security middleware (C10, C11) | `app/middleware/security.py`, `logging.py`, `request_id.py`, `main.py` | **OPEN** |
| **BE-SHARED-001** | **HIGH (P1)** | Shared Vocabulary | Hollow shared layer: `enums.py`, `priorities.py`, `thresholds.py` are 0 bytes | `shared/models/enums.py`, `shared/constants/priorities.py`, `thresholds.py` | **OPEN** |
| **BE-REALTIME-001** | **HIGH (P1)** | Realtime / Telemetry | Missing server-side SSE fan-out & `/stream` endpoints (C14) | `infrastructure/realtime/`, `app/routers/maitri/energy.py`, `bharati/energy.py` | **OPEN** |
| **BE-RESIL-001** | **HIGH (P1)** | Resilience / Polar Sync | Missing store-and-forward write buffer queue for SATCOM outages | `infrastructure/resilience/in_process_write_buffer.py` | **OPEN** |
| **BE-ROUTER-001** | **MEDIUM (P2)** | API Structure | Empty sub-router files & monolithic route bundling in station routers | `app/routers/maitri/*.py`, `bharati/*.py`, `hq/*.py` | **OPEN** |
| **BE-TEST-001** | **HIGH (P1)** | QA / Testing | Empty test suite & broken pytest session (0 tests executed) | `tests/e2e/`, `tests/unit/`, `tests/integration/`, `pyproject.toml` | **OPEN** |
| **BE-ENV-001** | **HIGH (P1)** | Deployment / Config | Deficient `requirements.txt` & broken `Dockerfile` (violates C17, Python 3.11) | `requirements.txt`, `Dockerfile`, `.env.example` | **OPEN** |

---

## 3. The Core Dilemmas Explained

### 1. The Three-Way Database Schema Conflict
The most dangerous inconsistency is that three parts of the repository define three different database designs:
- **`docs/architecture.md` §8**: Defines 5 tables (`users`, `energy_readings`, `alerts`, `commands`, `audit_log`). Stations are an `ENUM ('maitri', 'bharati')`, users have integer PKs, and energy readings have generator columns.
- **`docs/database.md` & `scripts/migrations/001_initial_schema.sql`**: Defines 25 tables. Auth uses Supabase Auth with UUID profiles. Stations are dynamic rows in `stations`. Telemetry is a partitioned composite table (`time`, `station_id`).
- **`app/models/user.py`**: A toy SQLite model with `id`, `name`, `email`.

**Resolution**: `docs/database.md` and `scripts/migrations/001_initial_schema.sql` are the modern, production-grade schema (v1 Lock). `architecture.md` must be updated to align with it, and SQLAlchemy ORM models must be generated to mirror `001_initial_schema.sql`.

### 2. The Architectural Layer Inversion
In `infrastructure/database/postgres/connection.py` and `session.py`, code imports from `app.config.database`.
- According to `docs/architecture.md` Section 3, `infrastructure/` **MUST NOT** import from `app.*`.
- **Resolution**: Move the database engine, session factory, and Base model into `infrastructure/database/postgres/session.py`. Let `app/config/database.py` re-export them.

### 3. The Security & RBAC Vacuum
All station routers (`/maitri`, `/bharati`, `/hq`) have their role guards commented out. In `infrastructure/security/authorization/rbac.py`, the user is hardcoded to a mock dictionary returning `"maitri_operator"`.
- Anyone can access the system without logging in.
- If guards are activated with the current code, every user is treated as a Maitri operator, locking out Bharati operators and HQ administrators.
- **Resolution**: Implement real JWT verification, Argon2 password hashing, and uncomment router-level `dependencies=[Depends(require_role(...))]` on all portal routers.

---

## 4. Remediation Priority & Action Plan

To systematically resolve these inconsistencies, execute the 5-phase remediation plan detailed in [aim-vs-desired-vs-actual-backend-deep-analysis.md](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/testing/aim-vs-desired-vs-actual-backend-deep-analysis.md):

1. **Phase 1 (Foundations & Layer Inversion)**:
   - Fix `Dockerfile` (single-stage Python 3.12, eliminate Node build).
   - Update `requirements.txt` with `sqlalchemy`, `asyncpg`, `argon2-cffi`, `python-jose`, `httpx`, `pytest`.
   - Move database engine to `infrastructure/database/postgres/`.
   - Delete obsolete `infrastructure/database/mysql/`.
2. **Phase 2 (Schema & ORM Realization)**:
   - Populate `shared/models/enums.py` and `shared/constants/`.
   - Implement complete SQLAlchemy 2.0 async ORM models in `app/models/` (or `infrastructure/`) for all 25 tables.
   - Implement Pydantic V2 schemas in `app/schemas/`.
3. **Phase 3 (Core Domain Engine & Portal Services)**:
   - Implement Protocols in `engine/interfaces/`.
   - Implement `EnergyService`, `AlertService`, `CommandService` in `engine/services/core/`.
   - Implement `MaitriPortalService`, `BharatiPortalService`, `HQPortalService` enforcing server-side `station_id` (C3) and command privileges (C4).
4. **Phase 4 (Authentication, RBAC & Audit)**:
   - Implement Argon2 hashing in `passwords.py`.
   - Implement real JWT verification in `rbac.py` and enforce router-level guards (C5).
   - Implement `audit_log.py` and wire audit logging on all logins, state writes, and command dispatches (C7).
   - Add CSRF protection and security headers middleware (C10, C11).
5. **Phase 5 (Realtime, Resilience & Test Automation)**:
   - Implement `/stream` SSE endpoints for Maitri and Bharati energy charts.
   - Implement `in_process_write_buffer.py` for store-and-forward SATCOM resiliency.
   - Configure `pyproject.toml` and write async tests for RBAC route isolation and telemetry flow.
