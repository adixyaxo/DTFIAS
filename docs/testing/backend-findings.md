# Backend Findings & Consistency Audit: DTFIAS (SIH26060)

> **Document Status:** Official Verified Findings Ledger  
> **Target Path:** `docs/testing/backend-findings.md`  
> **Author:** Backend Testing Agent & Backend Inconsistency Manager Agent  
> **Date:** September 2026  
> **Ground Truth Standards:** `GEMINI.md` / `CLAUDE.md`, `docs/architecture.md` (Rev 5), `docs/database.md` (v1 Lock), `docs/databaseTables.md`, `.agents/database/SKILL.md`, `.agents/fastapi/SKILL.md`

---

## 1. Executive Summary & Ledger Table

This audit documents every architectural, structural, security, data-layer, and operational inconsistency identified in the backend of the **Digital Twin for Indian Antarctic Stations (DTFIAS)**.

Each finding is verified against the canonical specifications, assigned a standard severity (`CRITICAL / P0`, `HIGH / P1`, `MEDIUM / P2`, `LOW / P3`), and documented with root causes, impacted files, and precise remediation procedures.

| Finding ID | Severity | Category / Domain | Short Title | Status |
|:---|:---:|:---|:---|:---:|
| **BE-LAYER-001** | **CRITICAL (P0)** | Architecture / Layering | Inverted Layer Dependency: Infrastructure illegally imports from `app.config.database` | **OPEN** |
| **BE-LAYER-002** | **CRITICAL (P0)** | Architecture / DDD | Complete Domain Engine Bypass: `app/routers` query ORM directly, ignoring Engine layer | **OPEN** |
| **BE-LAYER-003** | **LOW (P3)** | Architecture / Hygiene | Legacy Dead Code: Obsolete MySQL adapters and integration tests lingering in repo | **OPEN** |
| **BE-ENGINE-001** | **CRITICAL (P0)** | Domain Engine | "Ghost Engine": 90% of `engine/` comprises empty 0-byte files (Services, Protocols, Pipelines) | **OPEN** |
| **BE-ENGINE-002** | **HIGH (P1)** | Domain Engine / Typing | Class Overwrite & Pydantic V1 syntax in `engine/domain/users/user.py` | **OPEN** |
| **BE-DB-001** | **CRITICAL (P0)** | Database / Schema | Architectural schema fracture resolved: `architecture.md` aligned to `database.md` v1 Lock | **RESOLVED (DOCS ALIGNED)** |
| **BE-DB-002** | **CRITICAL (P0)** | Database / ORM | 95% Missing SQLAlchemy ORM Models (Only stub `users` and `testing` exist) | **OPEN** |
| **BE-DB-003** | **HIGH (P1)** | Database / Schemas | Missing Pydantic V2 Domain Schemas for Telemetry, Commands, and Stations | **OPEN** |
| **BE-DB-004** | **MEDIUM (P2)** | Database / Architecture | Misplacement of Database Engine & Session Factory in `app/config/` instead of `infrastructure/` | **OPEN** |
| **BE-AUTH-001** | **CRITICAL (P0)** | Security / RBAC | Missing Router-Level Role Guards on Station & HQ APIRouters (C5 Violation) | **OPEN** |
| **BE-AUTH-002** | **CRITICAL (P0)** | Security / RBAC | Unauthenticated Mock RBAC returning hardcoded dummy dict in `infrastructure/security` | **OPEN** |
| **BE-AUTH-003** | **HIGH (P1)** | Security / Auth | Dummy Authentication Router: Login returns message, Logout does not clear cookies | **OPEN** |
| **BE-AUTH-004** | **CRITICAL (P0)** | Security / Passwords | Missing Argon2 Password Hashing implementation (C6 Violation) | **OPEN** |
| **BE-SEC-001** | **CRITICAL (P0)** | Security / Compliance | Zero Audit Logging across entire application (C7 Violation, `audit_log.py` is 0 bytes) | **OPEN** |
| **BE-SEC-002** | **HIGH (P1)** | Security / Middleware | Missing CSRF Protection, Secure Cookie settings, and Security Middleware (C10, C11) | **OPEN** |
| **BE-SHARED-001** | **HIGH (P1)** | Shared Vocabulary | Empty Shared Layer: `enums.py`, `priorities.py`, and `thresholds.py` are all 0 bytes (C9) | **OPEN** |
| **BE-REALTIME-001** | **HIGH (P1)** | Realtime / Telemetry | Missing Server-Side Realtime Fan-Out & SSE `/stream` endpoints (C14 Violation) | **OPEN** |
| **BE-RESIL-001** | **HIGH (P1)** | Resilience / Polar Sync | Missing Store-and-Forward Write Buffer (`in_process_write_buffer.py` is 0 bytes) | **OPEN** |
| **BE-ROUTER-001** | **MEDIUM (P2)** | API Structure | Hollow Sub-Router Files & Monolithic Route Bundling in Station and HQ routers | **OPEN** |
| **BE-TEST-001** | **HIGH (P1)** | QA / Testing | Empty Test Suite & Broken Test Runner (`pytest` fails with closed file exception) | **OPEN** |
| **BE-ENV-001** | **HIGH (P1)** | Deployment / Config | Deficient `requirements.txt` & Broken `Dockerfile` (violates C17, Python 3.11 mismatch) | **OPEN** |

---

## 2. Detailed Findings by Domain

### Domain 1: Architectural Layering & DDD Boundaries

#### Finding BE-LAYER-001: Inverted Layer Dependency (Infrastructure importing from App)
- **ID:** `BE-LAYER-001`
- **Severity:** `CRITICAL (P0)`
- **Status:** `OPEN`
- **Affected Files:**
  - `infrastructure/database/postgres/connection.py` (Line 4)
  - `infrastructure/database/postgres/session.py` (Line 5)
- **Specification Authority:**
  - `docs/architecture.md` Section 3 (Allowed Imports Per Layer):
    > `infrastructure/database`, `infrastructure/resilience`, `infrastructure/security` May import: `engine.interfaces.*`, `engine.domain.*`, `shared.*`, DB/HTTP libs.  
    > **MUST NOT import from:** `app.*`
- **Actual Implementation:**
  In `infrastructure/database/postgres/connection.py`:
  ```python
  from app.config.database import engine
  ```
  In `infrastructure/database/postgres/session.py`:
  ```python
  from app.config.database import AsyncSessionLocal, get_db
  ```
- **Root Cause:** The database session and engine were hastily set up inside `app/config/database.py`, forcing the lower-level `infrastructure` layer to reach upward into the `app` (Interface) layer, inverting the architectural hierarchy.
- **Risk & Impact:** Violates Domain-Driven Design (DDD) layer isolation. Creates circular dependency risks, prevents isolating infrastructure adapters into standalone deployables or test harnesses, and violates mechanical architectural compliance checks.
- **Remediation Plan:**
  1. Relocate engine creation, session factory (`async_sessionmaker`), and base declarative model to `infrastructure/database/postgres/session.py` and `connection.py`.
  2. Have `app/config/database.py` re-export `get_db` and `engine` from `infrastructure/database/postgres/`, restoring top-to-bottom dependency flow.

---

#### Finding BE-LAYER-002: Complete Domain Engine Bypass
- **ID:** `BE-LAYER-002`
- **Severity:** `CRITICAL (P0)`
- **Status:** `OPEN`
- **Affected Files:**
  - `app/routers/auth/user.py` (Lines 1-27)
  - `app/routers/maitri/router.py`
  - `app/routers/bharati/router.py`
  - `app/routers/hq/router.py`
- **Specification Authority:**
  - `docs/architecture.md` Section 2 & 3:
    > `app/**` May import from: `engine.services.portals.*`, `infrastructure.*`, `shared.*`.  
    > **MUST NOT import from:** "nothing bypasses `engine.services.portals`"
  - `GEMINI.md` Section 2 (Four-Layer Architecture).
- **Actual Implementation:**
  `app/routers/auth/user.py` executes SQLAlchemy queries directly in the API handler:
  ```python
  result = await db.execute(select(UserModel).where(UserModel.id == user_id))
  user = result.scalar_one_or_none()
  ```
  Meanwhile, `app/routers/{maitri,bharati,hq}/router.py` bypass all engine services entirely and return static Jinja2 templates without calling `MaitriPortalService`, `BharatiPortalService`, or `HQPortalService`.
- **Root Cause:** Rapid prototyping resulted in routes directly binding to database models or returning unparameterized HTML views, skipping the domain engine entirely.
- **Risk & Impact:** Business rules (station isolation, alert threshold checks, command validation, telemetry deduplication) are bypassed. Testing the domain requires launching a full FastAPI HTTP stack.
- **Remediation Plan:**
  1. Implement concrete portal services (`MaitriPortalService`, `BharatiPortalService`, `HQPortalService`).
  2. Ensure all router handlers invoke their respective portal service methods rather than directly calling ORM or returning unbacked templates.

---

#### Finding BE-LAYER-003: Legacy Dead MySQL Code Artifacts Lingering in Repo
- **ID:** `BE-LAYER-003`
- **Severity:** `LOW (P3)`
- **Status:** `OPEN`
- **Affected Files:**
  - `infrastructure/database/mysql/connection.py`
  - `infrastructure/database/mysql/session.py`
  - `tests/integration/mysql/test_row_level_station_scoping.py`
- **Specification Authority:**
  - `docs/architecture.md` Section 0 ("What changed from Revision 4: database moved from MySQL to Supabase-hosted Postgres").
- **Actual Implementation:**
  Empty directories and 0-byte files for MySQL database connections and integration tests still reside in `infrastructure/database/mysql/` and `tests/integration/mysql/`.
- **Root Cause:** Incomplete cleanup during the Revision 4 to Revision 5 migration from MySQL to Supabase PostgreSQL.
- **Risk & Impact:** Developer confusion, clutter, and accidental reintroduction of MySQL-specific assumptions.
- **Remediation Plan:**
  1. Delete `infrastructure/database/mysql/` and `tests/integration/mysql/`.
  2. Ensure all references in documentation and scripts point solely to Supabase PostgreSQL.

---

### Domain 2: Engine Layer Completeness & Typing Integrity

#### Finding BE-ENGINE-001: "Ghost Engine" (Hollow Engine Implementation)
- **ID:** `BE-ENGINE-001`
- **Severity:** `CRITICAL (P0)`
- **Status:** `OPEN`
- **Affected Files:**
  - `engine/interfaces/clock.py` (0 bytes)
  - `engine/interfaces/repositories.py` (0 bytes)
  - `engine/interfaces/write_buffer.py` (0 bytes)
  - `engine/processing/pipeline.py` (0 bytes)
  - `engine/processing/ingestion/deduplicator.py` (0 bytes)
  - `engine/processing/ingestion/sanitizer.py` (0 bytes)
  - `engine/processing/ingestion/validator.py` (0 bytes)
  - `engine/services/core/alert_service.py` (0 bytes)
  - `engine/services/core/command_service.py` (0 bytes)
  - `engine/services/core/energy_service.py` (0 bytes)
  - `engine/services/core/environment_service.py` (0 bytes)
  - `engine/services/core/infrastructure_service.py` (0 bytes)
  - `engine/services/core/logistics_service.py` (0 bytes)
  - `engine/services/core/user_service.py` (0 bytes)
  - `engine/services/portals/maitri_portal_service.py` (0 bytes)
  - `engine/services/portals/bharati_portal_service.py` (0 bytes)
  - `engine/services/portals/hq_portal_service.py` (0 bytes)
  - `engine/simulation/scenario_runner.py` (0 bytes)
  - `engine/simulation/station_simulator.py` (0 bytes)
  - `engine/simulation/weather_simulator.py` (0 bytes)
- **Specification Authority:**
  - `docs/architecture.md` Section 5 & `GEMINI.md` Section 3.
  - Constraints C3, C4:
    > C3: `station_id` MUST be set server-side only, hard-coded as a class constant in portal services.  
    > C4: `maitri_portal_service.py` / `bharati_portal_service.py` MUST NOT define `issue_command`, `manage_users`, or `view_audit`.
- **Actual Implementation:**
  Every single protocol, service, ingestion pipeline, and simulation runner in the `engine/` layer is an empty 0-byte file, leaving the domain engine completely non-functional.
- **Root Cause:** File scaffolding was created during initial repository setup but never implemented with domain logic.
- **Risk & Impact:** The application has no backend domain logic whatsoever. Telemetry cannot be validated or ingested, alerts cannot trigger, commands cannot be validated or state-tracked, and station scoping cannot be enforced.
- **Remediation Plan:**
  1. Define typing Protocols in `engine/interfaces/` (`ClockPort`, `EnergyRepository`, `AlertRepository`, `CommandRepository`, `WriteBufferPort`).
  2. Implement core services in `engine/services/core/` (`EnergyService`, `AlertService`, `CommandService`).
  3. Implement portal service facades enforcing station scoping (`STATION_ID = "maitri"` / `"bharati"`) and privilege constraints (C3, C4).

---

#### Finding BE-ENGINE-002: Class Overwrite & Pydantic V1 Syntax in User Entity
- **ID:** `BE-ENGINE-002`
- **Severity:** `HIGH (P1)`
- **Status:** `OPEN`
- **Affected Files:**
  - `engine/domain/users/user.py` (Lines 14-23)
- **Specification Authority:**
  - `.agents/fastapi/SKILL.md` (Constraints: MUST NOT DO: Use Pydantic V1 syntax).
  - `GEMINI.md` Section 6 ("Pydantic V2 syntax only (`field_validator` not `@validator`, `model_config` not `class Config`)").
- **Actual Implementation:**
  In `engine/domain/users/user.py`:
  ```python
  class User(UserBase):
      password: str

  class User(UserBase):
      id: int
      roles: List[Role] = Field(default_factory=list)
      created_at: datetime
      
      class Config:
          from_attributes = True
  ```
- **Root Cause:** The class `User` is defined twice consecutively; the second definition completely shadows the first, discarding the `password` field. Furthermore, it uses Pydantic V1's deprecated `class Config` and legacy `typing.List`.
- **Risk & Impact:** Inconsistent runtime behavior, deprecation warnings or crashes under Pydantic V2, and loss of model fields.
- **Remediation Plan:**
  1. Refactor into modern Pydantic V2 schemas: `UserBase`, `UserCreate(UserBase)`, `UserResponse(UserBase)`.
  2. Replace `class Config: from_attributes = True` with `model_config = ConfigDict(from_attributes=True)`.
  3. Replace `id: int` with `UUID` or aligned identifier type.
  4. Replace `List[Role]` with `list[Role]`.

---

### Domain 3: Database Schema Divergence & ORM Absence

#### Finding BE-DB-001: Three-Way Architectural Schema Contradiction
- **ID:** `BE-DB-001`
- **Severity:** `CRITICAL (P0)`
- **Status:** `RESOLVED (DOCS ALIGNED)`
- **Affected Files:**
  - `docs/architecture.md` Section 8
  - `docs/database.md` (v1 Lock)
  - `GEMINI.md` Section 5
  - `CLAUDE.md` Section 5
  - `scripts/migrations/001_initial_schema.sql`
- **Specification Authority:**
  - `docs/architecture.md` (Revision 5 structural contract)
  - `docs/database.md` (v1 Lock schema authority)
- **Actual Implementation:**
  Previously, there were three conflicting schema definitions between `architecture.md` §8 (5 monolithic tables with integer IDs), `database.md` (25 normalized tables with UUIDs and Supabase Auth profiles), and `app/models/user.py`.
- **Resolution Performed:**
  1. `docs/database.md` and `scripts/migrations/001_initial_schema.sql` were formally established across all agent guidelines (`GEMINI.md`, `CLAUDE.md`) as the canonical single source of truth for the database schema.
  2. `docs/architecture.md` Section 8 was completely synchronized to reference the authoritative 25-table v1 Lock architecture and native operational enums.
  3. Building corresponding SQLAlchemy ORM models matching `docs/database.md` is tracked under `BE-DB-002`.

---

#### Finding BE-DB-002: 95% Missing SQLAlchemy ORM Models
- **ID:** `BE-DB-002`
- **Severity:** `CRITICAL (P0)`
- **Status:** `OPEN`
- **Affected Files:**
  - `app/models/`
- **Specification Authority:**
  - `GEMINI.md` Section 5 (Domain Tables: Auth, RBAC, Stations, Personnel, Assets, Sensors, Telemetry, Energy, Logistics, Maintenance, Commands, Alerts, Audit).
  - `docs/database.md` (25 distinct database tables).
- **Actual Implementation:**
  The `app/models/` folder contains only two files:
  - `app/models/user.py` (3 columns: `id`, `name`, `email`)
  - `app/models/test.py` (1 column: `test: bool`)
  There are zero ORM models for:
  - `profiles`, `roles`, `permissions`, `user_roles`, `role_permissions`, `station_access`
  - `stations`, `station_areas`, `assets`, `asset_status_history`, `sensors`, `sensor_configurations`
  - `energy_readings`, `environment_readings`, `asset_readings`, `energy_systems`, `energy_sources`, `energy_assets`
  - `inventory_items`, `inventory`, `inventory_transactions`, `shipments`, `shipment_items`
  - `maintenance_records`, `maintenance_events`, `commands`, `command_executions`, `alert_rules`, `active_alerts`, `audit_logs`
- **Root Cause:** ORM model scaffolding was never created after the database schema was designed.
- **Risk & Impact:** The backend cannot perform type-safe, parameterized ORM queries. Any database read/write requires raw SQL, risking constraint violations or syntax errors.
- **Remediation Plan:**
  Create structured SQLAlchemy models under `app/models/` (or `infrastructure/database/postgres/models/`) mirroring the 25 tables in `001_initial_schema.sql`.

---

#### Finding BE-DB-003: Missing Pydantic V2 Domain & Validation Schemas
- **ID:** `BE-DB-003`
- **Severity:** `HIGH (P1)`
- **Status:** `OPEN`
- **Affected Files:**
  - `app/schemas/user.py`
  - `app/schemas/test.py`
- **Specification Authority:**
  - `.agents/fastapi/SKILL.md` (Pydantic V2 schemas: `UserCreate`, `UserResponse`, `CommandCreate`, `EnergyReadingResponse`, etc.).
- **Actual Implementation:**
  `app/schemas/user.py` contains only:
  ```python
  class User(BaseModel):
      name: str
      email: str
  ```
  No validation, no password strength checks, no email validation with `EmailStr`, no `model_config = ConfigDict(from_attributes=True)`, and zero schemas for telemetry, commands, alerts, or stations.
- **Root Cause:** Incomplete schema implementation during initial setup.
- **Risk & Impact:** Inbound payloads are unvalidated; responses cannot be serialized safely, exposing internal database structures or sensitive fields.
- **Remediation Plan:**
  Implement comprehensive Pydantic V2 schemas for every domain entity with `model_config = ConfigDict(str_strip_whitespace=True, from_attributes=True)`.

---

#### Finding BE-DB-004: Misplacement of Database Engine in `app/config/`
- **ID:** `BE-DB-004`
- **Severity:** `MEDIUM (P2)`
- **Status:** `OPEN`
- **Affected Files:**
  - `app/config/database.py`
- **Specification Authority:**
  - `docs/architecture.md` Section 2 & Section 3.
- **Actual Implementation:**
  `create_async_engine`, `async_sessionmaker`, `Base = DeclarativeBase`, and `get_db()` are created directly in `app/config/database.py`.
- **Root Cause:** Following generic FastAPI tutorial structures rather than the project's mandated Four-Layer DDD architecture.
- **Risk & Impact:** Violates the architectural boundary where database engine management belongs to `infrastructure/database/postgres/`.
- **Remediation Plan:**
  Move concrete SQLAlchemy engine and session factory to `infrastructure/database/postgres/`, and have `app/config/database.py` re-export them.

---

### Domain 4: Authentication, RBAC & Security Integrity

#### Finding BE-AUTH-001: Missing Router-Level Role Guards on All Portals (C5 Violation)
- **ID:** `BE-AUTH-001`
- **Severity:** `CRITICAL (P0)`
- **Status:** `OPEN`
- **Affected Files:**
  - `app/routers/maitri/router.py` (Lines 5-6)
  - `app/routers/bharati/router.py` (Lines 5-6)
  - `app/routers/hq/router.py` (Lines 5-6)
- **Specification Authority:**
  - `GEMINI.md` Constraint C5 & `docs/architecture.md` Section 6:
    > C5: Every `APIRouter` under `app/routers/<portal>/` MUST declare its role guard via `dependencies=`, not per-endpoint decorators.
- **Actual Implementation:**
  All three portal routers leave the security guard as an inert comment:
  ```python
  # In a real app, this would have dependencies=[Depends(require_role("maitri_operator"))]
  router = APIRouter(prefix="/maitri", tags=["maitri"])
  ```
  ```python
  # In a real app, this would have dependencies=[Depends(require_role("bharati_operator"))]
  router = APIRouter(prefix="/bharati", tags=["bharati"])
  ```
  ```python
  # In a real app, this would have dependencies=[Depends(require_role_in("hq_operator", "hq_admin"))]
  router = APIRouter(prefix="/hq", tags=["hq"])
  ```
- **Root Cause:** Scaffolding comments were left unactivated to facilitate early UI testing, leaving all operational portals completely unauthenticated.
- **Risk & Impact:** Critical security vulnerability. Any anonymous web visitor can access Maitri, Bharati, and HQ Mission Control portals, inspect sensitive polar assets, and access telemetry without logging in.
- **Remediation Plan:**
  1. Implement `require_role(...)` in `app/dependencies/permissions.py` (or `infrastructure/security/authorization/rbac.py`).
  2. Wire `dependencies=[Depends(require_role("maitri_operator"))]`, `require_role("bharati_operator")`, and `require_role_in("hq_operator", "hq_admin")` directly onto the respective `APIRouter` declarations.

---

#### Finding BE-AUTH-002: Hardcoded Dummy RBAC in Security Layer
- **ID:** `BE-AUTH-002`
- **Severity:** `CRITICAL (P0)`
- **Status:** `OPEN`
- **Affected Files:**
  - `infrastructure/security/authorization/rbac.py` (Lines 6-23)
- **Specification Authority:**
  - `docs/architecture.md` Section 6
  - `GEMINI.md` Constraint C7
- **Actual Implementation:**
  In `infrastructure/security/authorization/rbac.py`:
  ```python
  async def get_current_user_mock():
      # In a real app, this retrieves the user from session/token
      return {"username": "test_user", "roles": [{"name": "maitri_operator"}]}

  def require_role(required_role: str) -> Callable:
      async def role_checker(user: dict = Depends(get_current_user_mock)):
          ...
  ```
  The RBAC checker relies on a hardcoded mock function returning a dummy user dictionary.
- **Root Cause:** Placeholder implementation for initial development that was never replaced with real token/cookie verification.
- **Risk & Impact:** Ineffective authorization. The system cannot distinguish between users, verify JWT signatures, or enforce permissions.
- **Remediation Plan:**
  1. Implement `get_current_user` extracting and decoding JWT tokens from secure cookies or `Authorization: Bearer` headers.
  2. Query user roles from database/JWT payload.
  3. Emit an audit log entry on permission denial (C7).

---

#### Finding BE-AUTH-003: Dummy Authentication Flow in Auth Router
- **ID:** `BE-AUTH-003`
- **Severity:** `HIGH (P1)`
- **Status:** `OPEN`
- **Affected Files:**
  - `app/routers/auth/auth.py` (Lines 13-26)
- **Specification Authority:**
  - `docs/architecture.md` Section 6, C10, C11
- **Actual Implementation:**
  ```python
  @router.post("/login")
  async def process_login():
      return {"message": "Login processing goes here"}

  @router.get("/logout")
  @router.post("/logout")
  async def logout():
      return RedirectResponse(url="/auth/login", status_code=302)
  ```
- **Root Cause:** Login and logout handlers were stubbed out and never hooked up to password validation or session creation.
- **Risk & Impact:** Users cannot log into the system; login returns a raw JSON placeholder. Logout does not clear cookies or invalidate tokens.
- **Remediation Plan:**
  1. Implement form handling for username/password login.
  2. Verify credentials using Argon2 password verification.
  3. Issue signed JWT session cookie with `httponly=True, secure=True, samesite="strict"`.
  4. Have logout delete the session cookie and redirect to login.

---

#### Finding BE-AUTH-004: Missing Argon2 Password Hashing Implementation (C6 Violation)
- **ID:** `BE-AUTH-004`
- **Severity:** `CRITICAL (P0)`
- **Status:** `OPEN`
- **Affected Files:**
  - `infrastructure/security/authentication/passwords.py` (0 bytes)
- **Specification Authority:**
  - `GEMINI.md` Constraint C6 & `docs/architecture.md` C6:
    > C6: Passwords MUST be hashed with argon2 (`infrastructure/security/authentication/passwords.py`). MUST NOT log or store plaintext, ever, including debug logs.
- **Actual Implementation:**
  `infrastructure/security/authentication/passwords.py` is an empty 0-byte file.
- **Root Cause:** The password hashing utility was never implemented.
- **Risk & Impact:** Password security is non-existent. Without this module, user passwords cannot be safely stored or validated.
- **Remediation Plan:**
  Implement `hash_password(plain: str) -> str` and `verify_password(plain: str, hashed: str) -> bool` using `argon2-cffi` or `passlib[argon2]`.

---

#### Finding BE-SEC-001: Zero Audit Logging Implementation (C7 Violation)
- **ID:** `BE-SEC-001`
- **Severity:** `CRITICAL (P0)`
- **Status:** `OPEN`
- **Affected Files:**
  - `infrastructure/security/audit/audit_log.py` (0 bytes)
  - `app/routers/`
  - `engine/services/`
- **Specification Authority:**
  - `GEMINI.md` Constraint C7 & `docs/architecture.md` C7:
    > C7: Every login, state write, command issuance, and permission denial MUST produce one `audit_log` row.
- **Actual Implementation:**
  `infrastructure/security/audit/audit_log.py` is 0 bytes, and no route or service in the application contains any audit logging calls.
- **Root Cause:** Audit subsystem was not implemented.
- **Risk & Impact:** Direct violation of Antarctic operational compliance and mission-critical accountability. Unauthorized actions, command dispatch, and security breaches leave zero forensic trail.
- **Remediation Plan:**
  1. Implement `record_audit_event(...)` in `infrastructure/security/audit/audit_log.py`.
  2. Integrate audit logging into login handlers, command issuance, and permission denial hooks.

---

#### Finding BE-SEC-002: Missing CSRF Protection & Security Middleware (C10, C11)
- **ID:** `BE-SEC-002`
- **Severity:** `HIGH (P1)`
- **Status:** `OPEN`
- **Affected Files:**
  - `app/middleware/security.py` (0 bytes)
  - `app/middleware/logging.py` (0 bytes)
  - `app/middleware/request_id.py` (0 bytes)
  - `main.py`
- **Specification Authority:**
  - `GEMINI.md` Constraints C10, C11 & `docs/architecture.md` C10, C11:
    > C10: Session cookies MUST be `httponly=True, secure=True, samesite="strict"`.  
    > C11: CSRF tokens MUST be verified on every `POST`/`PUT`/`DELETE` route.
- **Actual Implementation:**
  All three middleware files in `app/middleware/` are 0 bytes. `main.py` registers zero middleware on the `FastAPI` instance.
- **Root Cause:** Middleware files were scaffolded as empty stubs and never implemented.
- **Risk & Impact:** The application is vulnerable to Cross-Site Request Forgery (CSRF) on state-changing endpoints, lacks request tracing, and lacks standard security headers (`Content-Security-Policy`, `X-Content-Type-Options`).
- **Remediation Plan:**
  1. Implement CSRF verification middleware or dependencies.
  2. Add request ID generation and structured logging middleware.
  3. Wire middleware into `main.py`.

---

### Domain 5: Shared Vocabulary & System Constants

#### Finding BE-SHARED-001: Completely Hollow Shared Layer (C9 Violation)
- **ID:** `BE-SHARED-001`
- **Severity:** `HIGH (P1)`
- **Status:** `OPEN`
- **Affected Files:**
  - `shared/models/enums.py` (0 bytes)
  - `shared/constants/priorities.py` (0 bytes)
  - `shared/constants/thresholds.py` (0 bytes)
- **Specification Authority:**
  - `GEMINI.md` Constraint C9 & `docs/architecture.md` Section 2:
    > `shared/` LAYER: shared vocabulary (used by 2+ layers).
- **Actual Implementation:**
  All three files in `shared/` are 0 bytes. Neither enums nor system constants exist in Python code.
- **Root Cause:** Central domain constants and enums were never defined in Python code, forcing parts of the codebase to use arbitrary strings.
- **Risk & Impact:** Magic strings scattered throughout codebase; lack of type safety and enum validation.
- **Remediation Plan:**
  1. Define Python `StrEnum` classes in `shared/models/enums.py` matching `001_initial_schema.sql` (`StationId`, `RoleEnum`, `AlertSeverity`, `CommandStatus`, `ReadingQuality`, etc.).
  2. Define write-buffer priority levels in `shared/constants/priorities.py` (`P0_CRITICAL_ALERT`, `P1_COMMAND`, `P2_TELEMETRY`).
  3. Define real Antarctic engineering thresholds in `shared/constants/thresholds.py` (Bharati max power 340 kW, battery min 25%, fuel min 20%).

---

### Domain 6: Realtime SSE & Store-and-Forward Sync

#### Finding BE-REALTIME-001: Missing Server-Side Realtime & SSE Stream Pipeline (C14 Violation)
- **ID:** `BE-REALTIME-001`
- **Severity:** `HIGH (P1)`
- **Status:** `OPEN`
- **Affected Files:**
  - `infrastructure/realtime/` (Directory does not exist)
  - `app/routers/maitri/energy.py` (0 bytes)
  - `app/routers/bharati/energy.py` (0 bytes)
- **Specification Authority:**
  - `docs/architecture.md` Section 7 & Constraint C14:
    > Two options for driving `/maitri/energy/stream`: Option A (default, recommended): `app/routers/maitri/energy.py`'s `/stream` endpoint polls `EnergyRepository.latest()` on a short interval inside a `StreamingResponse` generator and yields an SSE event whenever the value changes.  
    > C14: Client-side `supabase-js` Realtime subscriptions from the browser are FORBIDDEN.
- **Actual Implementation:**
  Neither the `/stream` endpoint nor the `infrastructure/realtime/` folder exists.
- **Root Cause:** Realtime streaming was omitted during router implementation.
- **Risk & Impact:** ApexCharts and live dashboard telemetry badges cannot update reactively via HTMX SSE extensions.
- **Remediation Plan:**
  Implement Option A: a `StreamingResponse` SSE generator endpoint in `energy.py` scoped strictly by `station_id`.

---

#### Finding BE-RESIL-001: Missing Store-and-Forward Write Buffer
- **ID:** `BE-RESIL-001`
- **Severity:** `HIGH (P1)`
- **Status:** `OPEN`
- **Affected Files:**
  - `infrastructure/resilience/in_process_write_buffer.py` (0 bytes)
- **Specification Authority:**
  - `docs/architecture.md` Section 5 & `BackendTestingAgent/agent.md` Section 2:
    > "Simulate a dropped connection mid-write; confirm queued writes replay in the documented priority order (P0/P1/P2) once the link returns, with no duplication and no silent drops."
- **Actual Implementation:**
  `infrastructure/resilience/in_process_write_buffer.py` is an empty 0-byte file.
- **Root Cause:** Store-and-forward queue was never implemented.
- **Risk & Impact:** In the event of SATCOM dropouts, telemetry and commands are dropped rather than queued in priority order for store-and-forward reconciliation.
- **Remediation Plan:**
  Implement an in-memory or SQLite-backed write buffer queue respecting priority levels (P0, P1, P2) with replay idempotency.

---

### Domain 7: API Routing & Structural Modularity

#### Finding BE-ROUTER-001: Hollow Sub-Router Files & Monolithic Route Bundling
- **ID:** `BE-ROUTER-001`
- **Severity:** `MEDIUM (P2)`
- **Status:** `OPEN`
- **Affected Files:**
  - `app/routers/maitri/` (`alerts.py`, `dashboard.py`, `energy.py`, `environment.py`, `infrastructure.py`, `logistics.py` all 0 bytes)
  - `app/routers/bharati/` (mirrors maitri, all 0 bytes)
  - `app/routers/hq/` (`alerts.py`, `audit.py`, `commands.py`, `dashboard.py`, `stations.py`, `users.py` all 0 bytes)
- **Specification Authority:**
  - `docs/architecture.md` Section 2 (Repository Map) & `GEMINI.md` Section 3:
    > `maitri/` # router.py + dashboard, energy, environment, logistics, infrastructure, alerts  
    > `bharati/` # mirrors maitri/  
    > `hq/` # router.py + dashboard, stations, alerts, commands, users, audit
- **Actual Implementation:**
  All endpoints are defined monolithically inside `router.py`, while the dedicated sub-module files are empty 0-byte stubs.
- **Root Cause:** Developer convenience during template rendering, leaving modular route files unutilized.
- **Risk & Impact:** Bloated `router.py` files, inability to cleanly attach domain-specific dependencies, and difficulty in testing endpoints in isolation.
- **Remediation Plan:**
  Distribute endpoints into their designated sub-router files (`energy.py`, `alerts.py`, etc.) and aggregate them into the main station router via `router.include_router(...)`.

---

### Domain 8: Test Suite & QA Automation

#### Finding BE-TEST-001: Completely Empty Test Suite & Broken Pytest Session
- **ID:** `BE-TEST-001`
- **Severity:** `HIGH (P1)`
- **Status:** `OPEN`
- **Affected Files:**
  - `tests/e2e/test_full_energy_reading_flow.py` (0 bytes)
  - `tests/e2e/test_rbac_route_isolation.py` (0 bytes)
  - `tests/unit/engine/test_portal_services.py` (0 bytes)
  - `pyproject.toml` (0 bytes)
- **Specification Authority:**
  - `docs/architecture.md` Section 10 & 11 (Testing Contracts & Definition of Done)
  - `GEMINI.md` Section 12 (Testing Contracts)
- **Actual Implementation:**
  All test files in `tests/e2e/`, `tests/unit/`, and `tests/integration/` are 0 bytes. Running `pytest` fails with `ValueError: I/O operation on closed file` and collects 0 test items.
- **Root Cause:** Automated testing was deferred during initial interface development.
- **Risk & Impact:** Zero test coverage. Regressions in RBAC, station isolation, or telemetry ingestion cannot be mechanically prevented or detected.
- **Remediation Plan:**
  1. Populate `pyproject.toml` with valid `[tool.pytest.ini_options]` configuration.
  2. Implement unit tests for portal services and RBAC isolation in `tests/unit/` and `tests/e2e/`.

---

### Domain 9: Deployment, Environment & Packaging

#### Finding BE-ENV-001: Incomplete `requirements.txt` & Broken `Dockerfile`
- **ID:** `BE-ENV-001`
- **Severity:** `HIGH (P1)`
- **Status:** `OPEN`
- **Affected Files:**
  - `requirements.txt`
  - `Dockerfile`
  - `.env.example`
- **Specification Authority:**
  - `GEMINI.md` Section 1, 14 & Constraint C17:
    > Backend: Python 3.12+ · FastAPI · async SQLAlchemy (asyncpg driver)  
    > C17: Tailwind MUST be loaded via CDN. No npm build pipeline.
- **Actual Implementation:**
  1. `requirements.txt` is missing critical runtime dependencies: `sqlalchemy`, `asyncpg`, `argon2-cffi`, `python-jose`, `httpx`, `jinja2`, `pytest`.
  2. `Dockerfile` contains a Stage 1 Node.js build attempting `npm install` and `COPY package*.json ./`, but `package.json` does not exist in the repository. The Docker build fails immediately at Step 5.
  3. `Dockerfile` uses `FROM python:3.11-slim`, contradicting the Python 3.12+ requirement.
- **Root Cause:** Legacy frontend build pipeline from an earlier template was left in `Dockerfile` despite transitioning to CDN Tailwind (C17).
- **Risk & Impact:** Docker container cannot be built. Fresh developer checkouts cannot run the application without discovering missing Python dependencies by trial-and-error.
- **Remediation Plan:**
  1. Update `requirements.txt` with all required dependencies.
  2. Refactor `Dockerfile` into a clean single-stage Python 3.12 container, removing the Node.js build stage.
  3. Expand `.env.example` to document all required environment variables (`SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `ALGORITHM`, etc.).
