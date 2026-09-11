# DTFIAS: Master API Inventory & Endpoint Contracts Specification

> **Document Status:** Authoritative Backend API Inventory & Contract Specification  
> **Target Path:** `docs/api-contracts.md`  
> **Owner Agent:** Documentation Agent / DTFIAS Backend Engineering  
> **Last Verified:** September 2026  
> **Complements:** [`docs/frontend-endpoints.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/frontend-endpoints.md), [`docs/architecture.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/architecture.md)

---

## 1. Global API Conventions

### 1.1 Base URL & Content Types
- **API Base Prefix:** `/api/v1` (for REST endpoints) and `/` (for server-rendered HTML views).
- **Request Payloads:** `application/json` with Pydantic V2 schema validation.
- **Response Payloads:** `application/json` (REST) or `text/event-stream` (SSE).

### 1.2 Unified Error Envelope
All error responses return a standardized JSON structure:
```json
{
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "User lacks 'command.create' permission for station 'bharati'.",
    "request_id": "8f3b610c-8067-466d-8bc3-366579b122e1",
    "details": [
      {
        "field": "station_id",
        "issue": "Cross-station command execution forbidden for station operators."
      }
    ]
  }
}
```

### 1.3 HTTP Status Code Standards
| Status Code | Usage in DTFIAS |
| :--- | :--- |
| `200 OK` | Successful query retrieval or non-mutating action. |
| `201 Created` | Successful creation of a resource (e.g., command registered, user profile created). |
| `202 Accepted` | Asynchronous command accepted for transmission over SATCOM. |
| `400 Bad Request` | Pydantic V2 schema validation failure or malformed payload. |
| `401 Unauthorized` | Missing, expired, or cryptographically invalid session token. |
| `403 Forbidden` | Authenticated user lacks the requisite RBAC permission. |
| `404 Not Found` | Requested station, asset, alert, or sensor ID does not exist. |
| `409 Conflict` | Unique constraint violation (e.g. duplicate email or asset code). |
| `422 Unprocessable` | Semantic validation failure (e.g. generator output exceeds physical capacity). |
| `500 Internal Error` | Unhandled server exception (triggers alert & structured JSON log). |

---

## 2. Authentication & Session Endpoints (`/auth`)

| Endpoint | Method | RBAC Requirement | Request Schema | Response Schema | Description |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `/auth/login` | `POST` | Public | `LoginRequest` | `UserSessionResponse` | Authenticates user via Argon2, issues secure session cookies (`httponly`, `samesite=strict`). Dispatches audit log. |
| `/auth/logout` | `POST` | Authenticated | Empty | `MessageResponse` | Invalidates session, clears authentication cookies. Dispatches audit log. |
| `/auth/me` | `GET` | Authenticated | None | `UserProfileResponse` | Returns profile, active roles, and scoped station permissions for currently logged-in user. |
| `/auth/refresh` | `POST` | Authenticated | Empty | `TokenRefreshResponse` | Refreshes JWT access token before expiration. |

---

## 3. Station Telemetry & Twin Endpoints (`/maitri`, `/bharati`)

> [!IMPORTANT]
> In accordance with **Constraint C3**, `station_id` is set strictly server-side by the router binding (e.g., `maitri_portal_service` binds `station_id="maitri"`). The client request never supplies `station_id` in query or body parameters.

| Route Pattern | Method | Auth / Role Guard | Query / Body Schema | Response Type | Description |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `/{station}/api/telemetry/latest` | `GET` | `telemetry.read` | None | `StationTelemetrySnapshot` | Retrieves latest aggregated readings (power load, battery SoC, ambient temp, wind speed, habitat pressure). |
| `/{station}/api/assets` | `GET` | `asset.read` | None | `list[AssetSummaryResponse]` | Lists all tracked physical assets with current status and alert state. |
| `/{station}/api/assets/{asset_id}` | `GET` | `asset.read` | Path: `asset_id (str)` | `AssetDetailResponse` | Detailed sensor telemetry, maintenance history, and specifications for a single asset. |
| `/{station}/api/energy/history` | `GET` | `energy.read` | `hours: int = 24` | `list[EnergyReadingResponse]` | Historical time-series energy data for trend analysis and ApexCharts visualization. |
| `/{station}/api/environment/history` | `GET` | `telemetry.read` | `hours: int = 24` | `list[EnvironmentReadingResponse]` | Historical weather telemetry (temperature, wind gust, atmospheric pressure, solar radiation). |
| `/{station}/api/alerts` | `GET` | `alert.read` | `status: str = 'ACTIVE'` | `list[AlertResponse]` | Active and acknowledged alarms scoped to the specific station. |
| `/{station}/api/alerts/{id}/ack` | `POST` | `alert.manage` | `AlertAckRequest` | `AlertResponse` | Acknowledges an active alert with user notes. Logs to `audit_logs`. |

---

## 4. Real-Time Streaming Endpoints (SSE)

In compliance with **Constraint C14**, real-time updates use server-side Server-Sent Events (`text/event-stream`). Browsers do not connect to Supabase Realtime directly.

| Endpoint | Method | Guard | Event Name | Data Payload Schema | Description |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `/maitri/energy/stream` | `GET` | `energy.read` | `energy_reading` | `EnergyStreamEvent` | Real-time generator kW, battery SoC, and grid load stream for Maitri. |
| `/bharati/energy/stream` | `GET` | `energy.read` | `energy_reading` | `EnergyStreamEvent` | Real-time generator kW, battery SoC, and grid load stream for Bharati. |
| `/hq/alerts/stream` | `GET` | `alert.read` | `alert_notification` | `AlertStreamEvent` | Multi-station critical alert stream pushing P0/P1 notifications to HQ operations bridge. |

---

## 5. Headquarters Management Endpoints (`/hq`)

> [!CAUTION]
> In accordance with **Constraint C4**, station services must never expose command dispatch, user management, or system-wide audit views. Only `/hq` may implement these endpoints.

| Endpoint | Method | Guard | Request Schema | Response Schema | Description |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `/hq/api/commands` | `POST` | `command.create` | `CommandCreateRequest` | `CommandResponse` | Dispatches a remote control command to station actuators (e.g. generator load switchover, HVAC setpoint change). Dispatches audit log. |
| `/hq/api/commands/{id}/execute`| `POST` | `command.execute` | `CommandExecuteRequest` | `CommandExecutionResponse` | Dual-authorization execution approval for safety-critical commands. |
| `/hq/api/stations` | `GET` | `station.read` | None | `list[StationOverviewResponse]` | High-level situation cards for all stations (Maitri, Bharati, future stations). |
| `/hq/api/users` | `GET` | `personnel.manage` | None | `list[UserAdminResponse]` | Lists all system users, active station assignments, and assigned RBAC roles. |
| `/hq/api/audit` | `GET` | `audit.read` | `AuditQueryFilter` | `list[AuditLogResponse]` | Immutable system audit log review for compliance and incident post-mortems. |

---

## 6. RBAC Role & Permission Mapping

| Role Name | Scope | Granted Permission Codes |
| :--- | :--- | :--- |
| `SUPER_ADMIN` | Global (All Stations & HQ) | `*` (All permissions) |
| `HQ_ADMIN` | Global | `station.*`, `asset.*`, `personnel.*`, `health.*`, `energy.*`, `logistics.*`, `maintenance.*`, `telemetry.read`, `command.*`, `alert.*`, `audit.read` |
| `HQ_OPERATOR` | Global | `station.read`, `asset.read`, `telemetry.read`, `energy.read`, `logistics.read`, `health.read`, `alert.manage`, `command.create` |
| `STATION_ADMIN` | Station-Scoped (Maitri or Bharati) | `station.read`, `asset.*`, `personnel.*`, `health.manage`, `energy.*`, `logistics.*`, `maintenance.*`, `telemetry.read`, `alert.manage` |
| `STATION_OPERATOR` | Station-Scoped | `station.read`, `asset.read`, `energy.read`, `telemetry.read`, `logistics.read`, `maintenance.read`, `alert.manage` |
| `ENGINEER` | Station-Scoped | `asset.*`, `energy.*`, `telemetry.read`, `maintenance.*`, `alert.manage` |
| `SCIENTIST` | Station-Scoped | `telemetry.read`, `asset.read`, `health.read` |
| `VIEWER` | Global / Read-Only | `station.read`, `asset.read`, `telemetry.read`, `alert.read` |
