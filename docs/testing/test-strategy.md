# DTFIAS: Master Testing Strategy & Quality Assurance Framework

> **Document Status:** Authoritative Testing Strategy & QA Standard  
> **Target Path:** `docs/testing/test-strategy.md`  
> **Owner Agent:** Documentation Agent & Backend/Frontend Testing Agents  
> **Last Verified:** September 2026  
> **Related Reports:** [`docs/testing/backend-findings.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/testing/backend-findings.md), [`docs/testing/frontend-findings.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/testing/frontend-findings.md)

---

## 1. Quality Philosophy & Testing Pyramid

The Antarctic Digital Twin platform operates under life-safety conditions where software bugs can compromise station heating, energy balancing, or remote command execution. 

Testing follows a strict 3-tier pyramid:

```
          / \
         /   \     E2E Tests (10%)
        / E2E \    - Playwright browser workflows
       /───────\   - SATCOM dropout simulation
      /         \
     / Integrat. \ Integration Tests (30%)
    /─────────────\ - Database repository queries against test Postgres
   /               \ - FastAPI TestClient endpoint & RBAC verification
  /      Unit       \ Unit Tests (60%)
 /───────────────────\ - Pure domain services (`engine/services/`)
                       - Pydantic V2 schema validation
                       - Ingestion math & threshold calculators
```

---

## 2. Test Suite Organization

| Directory | Scope & Purpose | Dependencies Allowed | Typical Execution Time |
| :--- | :--- | :--- | :--- |
| `tests/unit/` | Pure logic: domain algorithms, ingestion parsers, telemetry validators, energy calculators. | Zero network, zero database, zero HTTP server. Fast, in-memory only. | < 5 seconds |
| `tests/integration/` | Database repositories, SQLAlchemy queries, FastAPI endpoint contracts, RBAC guards, session cookies. | Live or Dockerized test PostgreSQL database, `httpx.AsyncClient`. | 10 – 30 seconds |
| `tests/e2e/` | Complete user flows: login, twin hotspot navigation, remote command dispatch, SSE stream push. | Running FastAPI server, test database, browser emulator. | 30 – 90 seconds |

---

## 3. Mandatory Behavioral Verification (Constraints C1 – C17)

Every test run must include automated mechanical assertions against architectural rules:

### 3.1 Constraint C1: Engine Layer Purity
The pure Python domain layer (`engine/`) must have zero imports of web or database frameworks.
```python
# tests/unit/architecture/test_layer_purity.py
import subprocess
import pytest

def test_engine_layer_purity():
    cmd = 'grep -rE "^(import|from) (fastapi|sqlalchemy|asyncpg|jinja2|starlette)" engine/'
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    assert res.stdout.strip() == "", f"Engine layer violates C1 purity:\n{res.stdout}"
```

### 3.2 Constraint C13 & C14: Client-Side Security Isolation
The frontend static files and Jinja2 templates must never contain service keys or direct Supabase clients:
```python
# tests/unit/architecture/test_frontend_security.py
import subprocess

def test_no_service_role_in_templates():
    cmd = 'grep -r "SUPABASE_SERVICE_ROLE_KEY" app/static/ app/templates/'
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    assert res.stdout.strip() == "", "Found leaked SUPABASE_SERVICE_ROLE_KEY in frontend"

def test_no_supabase_js_in_browser():
    cmd = 'grep -rE "supabase-js|createClient\\(" app/static/ app/templates/'
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    assert res.stdout.strip() == "", "Found unauthorized supabase-js client in browser"
```

---

## 4. Test Execution Guidelines

### 4.1 Running Tests Locally
```bash
# Run entire test suite
pytest

# Run unit tests only (instant feedback)
pytest tests/unit/

# Run integration tests (requires live test DB)
pytest tests/integration/

# Run tests with test coverage reporting
pytest --cov=app --cov=engine --cov=infrastructure --cov-report=term-missing
```

### 4.2 Coverage Thresholds
- **Pure Domain Engine (`engine/`)**: Minimum **90%** branch coverage.
- **Data Repositories & Security (`infrastructure/`)**: Minimum **80%** coverage.
- **FastAPI Endpoints (`app/routers/`)**: Minimum **85%** endpoint coverage.
- **Global Project Coverage Target**: Minimum **80%** overall.

---

## 5. Defect Management & Regression Ledger

All discovered defects, regressions, or inconsistencies must be logged into:
- [`docs/testing/backend-inconsistencies.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/testing/backend-inconsistencies.md)
- [`docs/testing/backend-findings.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/testing/backend-findings.md)
- [`docs/testing/frontend-findings.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/testing/frontend-findings.md)
- [`docs/documentation-tasks.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/documentation-tasks.md)

---

## 6. Definition of Done (DoD) Sign-off Checklist

Before any PR or feature is marked complete, verify:
- [ ] Unit tests pass cleanly with `pytest tests/unit/`.
- [ ] No `engine/**` purity violations (C1).
- [ ] Station scoping enforced on all station entities via `station_id` (C2).
- [ ] Station ID is strictly server-bound, never accepted from user request bodies (C3).
- [ ] Role guards are attached at the `APIRouter` level (C5).
- [ ] Passwords hashed with Argon2; zero plaintext credentials in logs (C6).
- [ ] State-mutating operations record an audit log in `audit_logs` (C7).
- [ ] Database queries are parameterized; zero f-strings (C8).
- [ ] No frontend runtime bundler introduced; CDN Tailwind maintained (C17).
