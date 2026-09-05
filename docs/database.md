# DTFIAS — Database Design Specification

> **Version:** 1.0 (v1 Lock)  
> **Database:** Supabase PostgreSQL  
> **Auth:** Supabase Auth (`auth.users`)  
> **Schema default:** `public`

---

## Table of Contents

1. [Design Principles](#design-principles)
2. [Domain Map](#domain-map)
3. [Enumerations](#enumerations)
4. [AUTH Domain](#auth-domain)
5. [RBAC Domain](#rbac-domain)
6. [STATIONS Domain](#stations-domain)
7. [PERSONNEL Domain](#personnel-domain)
8. [ASSETS Domain](#assets-domain)
9. [SENSORS Domain](#sensors-domain)
10. [TELEMETRY Domain](#telemetry-domain)
11. [ENERGY Domain](#energy-domain)
12. [ENVIRONMENT Domain](#environment-domain)
13. [LOGISTICS Domain](#logistics-domain)
14. [MAINTENANCE Domain](#maintenance-domain)
15. [COMMANDS Domain](#commands-domain)
16. [ALERTS Domain](#alerts-domain)
17. [AUDIT Domain](#audit-domain)
18. [Relationships & Cardinality](#relationships--cardinality)
19. [Index Strategy](#index-strategy)
20. [Row-Level Security Strategy](#row-level-security-strategy)
21. [Telemetry Retention Policy](#telemetry-retention-policy)
22. [What is Deliberately Excluded](#what-is-deliberately-excluded)

---

## Design Principles

| Principle | Decision |
|-----------|----------|
| Authentication | Supabase Auth — no custom password table |
| Authorization | Application-level RBAC stored in `public` schema |
| Station extensibility | New stations are data rows, not schema changes |
| Telemetry | Separate domain tables — not one `sensor_readings` monolith |
| Personnel health | Status + condition only — no vitals, no complex medical records |
| Commands | HQ initiates; station validates and executes |
| Alerts | Temporary only — no permanent alert history |
| Telemetry retention | 30-day rolling window |
| File storage | Not in scope for v1 |
| Scientific data | Separate from operational telemetry |

---

## Domain Map

```text
auth.users  (Supabase managed)
     │
     │ 1:1
     ▼
profiles ──────────────────────────────────────────────────┐
     │                                                      │
     │ M:N (via user_roles)                                 │
     ▼                                                      │
roles ──── role_permissions ──── permissions               │
                                                            │
profiles ──── station_access ──── stations ────────────────┘
                                       │
                     ┌─────────────────┼──────────────────────┐
                     ▼                 ▼                       ▼
               station_areas       personnel             energy_systems
                     │                 │                       │
                     ▼                 ▼                       ▼
                  assets        station_assignments      energy_sources
                  assets ──── asset_status_history       energy_assets
                     │                 │                       │
                     ▼                 ▼                       ▼
               sensors ──── sensor_configurations  personnel_health_status
                     │
          ┌──────────┼───────────────┐
          ▼          ▼               ▼
   energy_readings  environment_readings  asset_readings

Independently:
  inventory_items ── inventory ── inventory_transactions
  shipments ── shipment_items
  maintenance_records ── maintenance_events
  commands ── command_executions
  alert_rules ── active_alerts
  scientific_observations
  audit_logs
```

---

## Enumerations

All enums are defined as PostgreSQL `ENUM` types.

### `station_status`
`ACTIVE` | `INACTIVE` | `UNDER_MAINTENANCE` | `DECOMMISSIONED`

### `station_type`
`RESEARCH_STATION` | `SUMMER_CAMP` | `FIELD_BASE` | `RELAY_STATION`

### `profile_status`
`ACTIVE` | `INACTIVE` | `SUSPENDED`

### `assignment_status`
`ACTIVE` | `COMPLETED` | `CANCELLED`

### `health_status`
`HEALTHY` | `ILL` | `INJURED` | `UNDER_OBSERVATION` | `MEDICAL_LEAVE` | `UNFIT`

### `asset_status`
`OPERATIONAL` | `DEGRADED` | `UNDER_MAINTENANCE` | `DECOMMISSIONED` | `STANDBY`

### `asset_criticality`
`CRITICAL` | `HIGH` | `MEDIUM` | `LOW`

### `sensor_status`
`ACTIVE` | `INACTIVE` | `FAULTY` | `CALIBRATING`

### `reading_quality`
`GOOD` | `UNCERTAIN` | `BAD` | `MISSING`

### `energy_source_type`
`DIESEL` | `SOLAR` | `WIND` | `BATTERY` | `HYBRID`

### `inventory_unit`
`LITRE` | `KILOGRAM` | `UNIT` | `METRE` | `KILOWATT_HOUR` | `BOX` | `PALLET`

### `transaction_type`
`RECEIVED` | `CONSUMED` | `TRANSFERRED` | `ADJUSTED` | `DISPOSED`

### `shipment_status`
`PLANNED` | `DISPATCHED` | `IN_TRANSIT` | `DELIVERED` | `CANCELLED`

### `maintenance_type`
`INSPECTION` | `PREVENTIVE` | `CORRECTIVE` | `EMERGENCY` | `CALIBRATION` | `UPGRADE`

### `maintenance_status`
`SCHEDULED` | `IN_PROGRESS` | `COMPLETED` | `CANCELLED` | `DEFERRED`

### `maintenance_priority`
`CRITICAL` | `HIGH` | `MEDIUM` | `LOW`

### `command_type`
`SYSTEM_CONTROL` | `SENSOR_CONTROL` | `ENERGY_CONTROL` | `LOGISTICS_CONTROL` | `PERSONNEL_CONTROL` | `ALERT_CONTROL`

### `command_status`
`PENDING` | `RECEIVED` | `VALIDATED` | `REJECTED` | `EXECUTING` | `EXECUTED` | `FAILED` | `EXPIRED`

### `alert_severity`
`CRITICAL` | `HIGH` | `MEDIUM` | `LOW` | `INFO`

### `alert_status`
`ACTIVE` | `ACKNOWLEDGED` | `RESOLVED` | `EXPIRED`

### `observation_type`
`AIR_TEMPERATURE` | `SNOW_OBSERVATION` | `ICE_OBSERVATION` | `ATMOSPHERIC_PRESSURE` | `WIND_OBSERVATION` | `PRECIPITATION` | `VISIBILITY` | `UV_INDEX` | `SEA_ICE_EXTENT`

### `access_level`
`READ` | `WRITE` | `ADMIN`

---

## AUTH Domain

### `auth.users`
> **Managed entirely by Supabase.** Do not create or modify directly.

| Column | Type | Notes |
|--------|------|-------|
| `id` | `UUID` | PK, used as FK in `profiles.id` |
| `email` | `TEXT` | Unique |
| `created_at` | `TIMESTAMPTZ` | |

Supabase handles: password hashing, sessions, JWTs, email auth, password reset.

---

### `profiles`

Maps 1:1 to `auth.users`. Stores application-level user data.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK, FK → `auth.users.id` ON DELETE CASCADE |
| `full_name` | `TEXT` | NOT NULL | |
| `employee_code` | `TEXT` | UNIQUE NOT NULL | e.g. `NCPOR-2024-001` |
| `designation` | `TEXT` | NULL | e.g. `Station Leader`, `Meteorologist` |
| `organization` | `TEXT` | NULL | e.g. `NCPOR`, `ISRO` |
| `phone` | `TEXT` | NULL | |
| `status` | `profile_status` | NOT NULL | DEFAULT `ACTIVE` |
| `avatar_url` | `TEXT` | NULL | External URL only |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

**Constraints:** UNIQUE(`employee_code`)  
**Trigger:** `updated_at` auto-set on row update  
**RLS:** Users can read their own profile; HQ_ADMIN can read all.

---

## RBAC Domain

### `roles`

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK, DEFAULT `gen_random_uuid()` |
| `name` | `TEXT` | UNIQUE NOT NULL | e.g. `HQ_ADMIN`, `STATION_OPERATOR` |
| `description` | `TEXT` | NULL | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

**Seed data:**

| name | description |
|------|-------------|
| `SUPER_ADMIN` | Full system access |
| `HQ_ADMIN` | HQ-level administration |
| `HQ_OPERATOR` | HQ monitoring and command |
| `STATION_ADMIN` | Station-level administration |
| `STATION_OPERATOR` | Station daily operations |
| `ENGINEER` | Engineering and maintenance |
| `SCIENTIST` | Scientific data access |
| `VIEWER` | Read-only access |

---

### `permissions`

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `code` | `TEXT` | UNIQUE NOT NULL | e.g. `station.read`, `command.create` |
| `description` | `TEXT` | NULL | |

**Seed data (permission codes):**

```
station.read          station.manage
asset.read            asset.manage
personnel.read        personnel.manage
health.read           health.manage
energy.read           energy.manage
logistics.read        logistics.manage
maintenance.read      maintenance.manage
telemetry.read
command.create        command.execute
alert.read            alert.manage
audit.read
```

---

### `user_roles`

Junction table: many users ↔ many roles.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `user_id` | `UUID` | NOT NULL | FK → `profiles.id` ON DELETE CASCADE |
| `role_id` | `UUID` | NOT NULL | FK → `roles.id` ON DELETE CASCADE |
| `assigned_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |
| `assigned_by` | `UUID` | NULL | FK → `profiles.id` |

**Constraints:** PK(`user_id`, `role_id`)

---

### `role_permissions`

Junction table: many roles ↔ many permissions.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `role_id` | `UUID` | NOT NULL | FK → `roles.id` ON DELETE CASCADE |
| `permission_id` | `UUID` | NOT NULL | FK → `permissions.id` ON DELETE CASCADE |

**Constraints:** PK(`role_id`, `permission_id`)

---

### `station_access`

Grants a user access to a specific station at a given level. Independent of role.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `user_id` | `UUID` | NOT NULL | FK → `profiles.id` ON DELETE CASCADE |
| `station_id` | `UUID` | NOT NULL | FK → `stations.id` ON DELETE CASCADE |
| `access_level` | `access_level` | NOT NULL | DEFAULT `READ` |
| `granted_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |
| `granted_by` | `UUID` | NULL | FK → `profiles.id` |

**Constraints:** UNIQUE(`user_id`, `station_id`)

---

## STATIONS Domain

### `stations`

One row per station. New stations are data rows — never schema changes.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `code` | `TEXT` | UNIQUE NOT NULL | e.g. `MAT`, `BHA`, `MAT2` |
| `name` | `TEXT` | NOT NULL | e.g. `Maitri`, `Bharati` |
| `description` | `TEXT` | NULL | |
| `station_type` | `station_type` | NOT NULL | |
| `status` | `station_status` | NOT NULL | DEFAULT `ACTIVE` |
| `latitude` | `DOUBLE PRECISION` | NULL | Decimal degrees |
| `longitude` | `DOUBLE PRECISION` | NULL | Decimal degrees |
| `elevation_m` | `DOUBLE PRECISION` | NULL | Metres above sea level |
| `capacity` | `INTEGER` | NULL | Max personnel count |
| `commissioned_at` | `DATE` | NULL | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

**Seed data:**

| code | name | type |
|------|------|------|
| `MAT` | Maitri | `RESEARCH_STATION` |
| `BHA` | Bharati | `RESEARCH_STATION` |

---

### `station_areas`

Lightweight spatial hierarchy within a station. Self-referential for nesting.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `station_id` | `UUID` | NOT NULL | FK → `stations.id` ON DELETE CASCADE |
| `parent_area_id` | `UUID` | NULL | FK → `station_areas.id` ON DELETE SET NULL |
| `name` | `TEXT` | NOT NULL | e.g. `Power System`, `Laboratory` |
| `area_type` | `TEXT` | NULL | e.g. `FUNCTIONAL`, `SPATIAL`, `SYSTEM` |
| `description` | `TEXT` | NULL | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

**Example hierarchy:**
```
Maitri (station)
  ├── Main Facility (area)
  │    ├── Living Area
  │    ├── Medical Area
  │    └── Laboratory
  ├── Power System
  ├── Water System
  ├── Storage
  └── Communications
```

---

## PERSONNEL Domain

### `personnel`

Application-level personnel records. Separate from `profiles` (which is auth-linked).
A person may or may not have a login (`profile_id` can be NULL for non-users).

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `profile_id` | `UUID` | NULL | FK → `profiles.id` ON DELETE SET NULL |
| `employee_code` | `TEXT` | UNIQUE NOT NULL | |
| `full_name` | `TEXT` | NOT NULL | |
| `designation` | `TEXT` | NULL | |
| `organization` | `TEXT` | NULL | |
| `phone` | `TEXT` | NULL | |
| `email` | `TEXT` | NULL | |
| `status` | `profile_status` | NOT NULL | DEFAULT `ACTIVE` |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

---

### `station_assignments`

Tracks each deployment of a person to a station over time.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `personnel_id` | `UUID` | NOT NULL | FK → `personnel.id` ON DELETE CASCADE |
| `station_id` | `UUID` | NOT NULL | FK → `stations.id` ON DELETE CASCADE |
| `station_role` | `TEXT` | NULL | e.g. `Station Leader`, `Meteorologist` |
| `arrival_date` | `DATE` | NOT NULL | |
| `departure_date` | `DATE` | NULL | NULL means currently deployed |
| `status` | `assignment_status` | NOT NULL | DEFAULT `ACTIVE` |
| `notes` | `TEXT` | NULL | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

**Cardinality:** One person can have many assignments over their career.  
**Constraint:** Only one `ACTIVE` assignment per person at a time (enforced by application layer).

---

### `personnel_health_status`

Basic health status only — no vitals, no complex diagnostics.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `personnel_id` | `UUID` | NOT NULL | FK → `personnel.id` ON DELETE CASCADE |
| `station_id` | `UUID` | NOT NULL | FK → `stations.id` |
| `status` | `health_status` | NOT NULL | |
| `condition` | `TEXT` | NULL | Free text e.g. `Respiratory infection` |
| `notes` | `TEXT` | NULL | |
| `recorded_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |
| `recorded_by` | `UUID` | NULL | FK → `profiles.id` |

**Access:** Restricted via RBAC — only `health.read` permission grants access.  
**Index:** `(personnel_id, recorded_at DESC)` for current status queries.

---

## ASSETS Domain

### `asset_types`

Lookup table for asset categories.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `name` | `TEXT` | UNIQUE NOT NULL | e.g. `Generator`, `Solar Panel` |
| `category` | `TEXT` | NULL | e.g. `ENERGY`, `HVAC`, `VEHICLE` |
| `description` | `TEXT` | NULL | |

**Seed data:**
`Generator`, `Solar Panel`, `Wind Turbine`, `Battery Bank`, `HVAC System`, `Water Treatment Plant`, `Fuel Tank`, `Communication Equipment`, `Scientific Equipment`, `Vehicle`, `Boiler`

---

### `assets`

Every physical piece of equipment at every station. Self-referential for hierarchy.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `station_id` | `UUID` | NOT NULL | FK → `stations.id` |
| `area_id` | `UUID` | NULL | FK → `station_areas.id` |
| `asset_type_id` | `UUID` | NOT NULL | FK → `asset_types.id` |
| `parent_asset_id` | `UUID` | NULL | FK → `assets.id` ON DELETE SET NULL — hierarchy |
| `asset_code` | `TEXT` | UNIQUE NOT NULL | e.g. `MAT-GEN-01` |
| `name` | `TEXT` | NOT NULL | |
| `manufacturer` | `TEXT` | NULL | |
| `model` | `TEXT` | NULL | |
| `serial_number` | `TEXT` | NULL | |
| `status` | `asset_status` | NOT NULL | DEFAULT `OPERATIONAL` |
| `criticality` | `asset_criticality` | NOT NULL | DEFAULT `MEDIUM` |
| `installation_date` | `DATE` | NULL | |
| `commissioned_at` | `DATE` | NULL | |
| `metadata` | `JSONB` | NULL | Flexible technical specs |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

**Example hierarchy:**
```
MAT-ENERGY-SYS (Energy System)
  ├── MAT-GEN-01 (Generator 01)
  ├── MAT-GEN-02 (Generator 02)
  ├── MAT-BATT-BANK (Battery Bank)
  │    ├── MAT-BATT-01
  │    └── MAT-BATT-02
  └── MAT-SOLAR-ARR (Solar Array)
```

---

### `asset_status_history`

Immutable audit of asset status changes.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `asset_id` | `UUID` | NOT NULL | FK → `assets.id` ON DELETE CASCADE |
| `old_status` | `asset_status` | NULL | NULL on first record |
| `new_status` | `asset_status` | NOT NULL | |
| `reason` | `TEXT` | NULL | |
| `changed_by` | `UUID` | NULL | FK → `profiles.id` |
| `changed_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

---

## SENSORS Domain

### `sensor_types`

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `name` | `TEXT` | UNIQUE NOT NULL | e.g. `TEMPERATURE`, `FUEL_LEVEL` |
| `description` | `TEXT` | NULL | |
| `default_unit` | `TEXT` | NULL | e.g. `°C`, `%`, `kPa` |

**Seed data:**
`TEMPERATURE`, `HUMIDITY`, `PRESSURE`, `WIND_SPEED`, `WIND_DIRECTION`, `SOLAR_RADIATION`, `FUEL_LEVEL`, `WATER_LEVEL`, `POWER_OUTPUT`, `BATTERY_SOC`, `VOLTAGE`, `CURRENT`

---

### `sensors`

A sensor instance attached to an asset at a station.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `station_id` | `UUID` | NOT NULL | FK → `stations.id` |
| `asset_id` | `UUID` | NULL | FK → `assets.id` ON DELETE SET NULL |
| `sensor_type_id` | `UUID` | NOT NULL | FK → `sensor_types.id` |
| `sensor_code` | `TEXT` | UNIQUE NOT NULL | e.g. `MAT-TMP-001` |
| `name` | `TEXT` | NOT NULL | |
| `unit` | `TEXT` | NOT NULL | Actual unit for this instance |
| `status` | `sensor_status` | NOT NULL | DEFAULT `ACTIVE` |
| `last_reading_at` | `TIMESTAMPTZ` | NULL | Updated on each reading |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

---

### `sensor_configurations`

Operational configuration for a sensor. Versioned by `effective_from`.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `sensor_id` | `UUID` | NOT NULL | FK → `sensors.id` ON DELETE CASCADE |
| `sampling_interval_seconds` | `INTEGER` | NOT NULL | e.g. 60, 900, 3600 |
| `min_threshold` | `DOUBLE PRECISION` | NULL | Alert if reading goes below |
| `max_threshold` | `DOUBLE PRECISION` | NULL | Alert if reading goes above |
| `calibration_offset` | `DOUBLE PRECISION` | NULL | DEFAULT 0.0 |
| `effective_from` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |
| `notes` | `TEXT` | NULL | |

---

## TELEMETRY Domain

> **Retention policy:** 30-day rolling window. Rows older than 30 days are deleted by a scheduled job or `pg_cron`.

### `energy_readings`

Time-series energy data per station.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `time` | `TIMESTAMPTZ` | NOT NULL | Partition key |
| `station_id` | `UUID` | NOT NULL | FK → `stations.id` |
| `energy_asset_id` | `UUID` | NULL | FK → `assets.id` |
| `generation_kw` | `DOUBLE PRECISION` | NULL | kW generated |
| `consumption_kw` | `DOUBLE PRECISION` | NULL | kW consumed |
| `battery_soc_pct` | `DOUBLE PRECISION` | NULL | Battery state of charge % |
| `voltage_v` | `DOUBLE PRECISION` | NULL | Volts |
| `current_a` | `DOUBLE PRECISION` | NULL | Amperes |
| `fuel_consumption_lph` | `DOUBLE PRECISION` | NULL | Litres per hour |
| `quality` | `reading_quality` | NOT NULL | DEFAULT `GOOD` |

**PK:** (`time`, `station_id`)  
**Index:** `(station_id, time DESC)`

---

### `environment_readings`

Time-series environmental/weather data per station.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `time` | `TIMESTAMPTZ` | NOT NULL | |
| `station_id` | `UUID` | NOT NULL | FK → `stations.id` |
| `temperature_c` | `DOUBLE PRECISION` | NULL | Celsius |
| `humidity_pct` | `DOUBLE PRECISION` | NULL | % |
| `pressure_hpa` | `DOUBLE PRECISION` | NULL | hPa |
| `wind_speed_mps` | `DOUBLE PRECISION` | NULL | m/s |
| `wind_direction_deg` | `DOUBLE PRECISION` | NULL | Degrees (0–360) |
| `solar_radiation_wm2` | `DOUBLE PRECISION` | NULL | W/m² |
| `quality` | `reading_quality` | NOT NULL | DEFAULT `GOOD` |

**PK:** (`time`, `station_id`)  
**Index:** `(station_id, time DESC)`

---

### `asset_readings`

Generic time-series for any sensor/asset combination not covered by specialised tables.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `time` | `TIMESTAMPTZ` | NOT NULL | |
| `asset_id` | `UUID` | NOT NULL | FK → `assets.id` |
| `sensor_id` | `UUID` | NULL | FK → `sensors.id` |
| `metric` | `TEXT` | NOT NULL | e.g. `fuel_level`, `temperature` |
| `value` | `DOUBLE PRECISION` | NOT NULL | |
| `unit` | `TEXT` | NULL | |
| `quality` | `reading_quality` | NOT NULL | DEFAULT `GOOD` |

**PK:** (`time`, `asset_id`, `metric`)  
**Index:** `(asset_id, time DESC)`

---

## ENERGY Domain

### `energy_systems`

One energy system per station (or logical system).

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `station_id` | `UUID` | NOT NULL | FK → `stations.id` |
| `name` | `TEXT` | NOT NULL | |
| `description` | `TEXT` | NULL | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

---

### `energy_sources`

Each source type within an energy system.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `energy_system_id` | `UUID` | NOT NULL | FK → `energy_systems.id` |
| `source_type` | `energy_source_type` | NOT NULL | |
| `name` | `TEXT` | NOT NULL | |
| `capacity_kw` | `DOUBLE PRECISION` | NULL | Rated capacity |
| `status` | `asset_status` | NOT NULL | DEFAULT `OPERATIONAL` |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

---

### `energy_assets`

Links physical assets to an energy source.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `energy_source_id` | `UUID` | NOT NULL | FK → `energy_sources.id` |
| `asset_id` | `UUID` | NOT NULL | FK → `assets.id` |

**Constraints:** UNIQUE(`energy_source_id`, `asset_id`)

---

## ENVIRONMENT Domain

### `scientific_observations`

Scientific environmental data — separate from operational telemetry.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `station_id` | `UUID` | NOT NULL | FK → `stations.id` |
| `observation_type` | `observation_type` | NOT NULL | |
| `observed_at` | `TIMESTAMPTZ` | NOT NULL | |
| `value` | `DOUBLE PRECISION` | NULL | Numeric value |
| `text_value` | `TEXT` | NULL | Free-form qualitative value |
| `unit` | `TEXT` | NULL | |
| `quality` | `reading_quality` | NOT NULL | DEFAULT `GOOD` |
| `source` | `TEXT` | NULL | Instrument/observer name |
| `metadata` | `JSONB` | NULL | Supplemental data |
| `recorded_by` | `UUID` | NULL | FK → `profiles.id` |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

**Note:** This table is not subject to 30-day retention. Scientific observations are permanent.

---

## LOGISTICS Domain

### `inventory_items`

Master catalogue of tracked items.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `name` | `TEXT` | NOT NULL | |
| `category` | `TEXT` | NULL | e.g. `FUEL`, `FOOD`, `MEDICAL`, `EQUIPMENT` |
| `unit` | `inventory_unit` | NOT NULL | |
| `description` | `TEXT` | NULL | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

---

### `inventory`

Current stock level per item per station.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `station_id` | `UUID` | NOT NULL | FK → `stations.id` |
| `item_id` | `UUID` | NOT NULL | FK → `inventory_items.id` |
| `quantity` | `DOUBLE PRECISION` | NOT NULL | Current quantity |
| `minimum_threshold` | `DOUBLE PRECISION` | NULL | Alert if below this |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

**Constraints:** UNIQUE(`station_id`, `item_id`)

---

### `inventory_transactions`

Full provenance for every stock movement.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `station_id` | `UUID` | NOT NULL | FK → `stations.id` |
| `item_id` | `UUID` | NOT NULL | FK → `inventory_items.id` |
| `transaction_type` | `transaction_type` | NOT NULL | |
| `quantity_delta` | `DOUBLE PRECISION` | NOT NULL | Positive = increase, Negative = decrease |
| `notes` | `TEXT` | NULL | |
| `transacted_by` | `UUID` | NULL | FK → `profiles.id` |
| `transacted_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |
| `shipment_id` | `UUID` | NULL | FK → `shipments.id` — if linked to a shipment |

---

### `shipments`

Logistics movements between locations.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `origin` | `TEXT` | NOT NULL | e.g. `GOA`, station code |
| `destination_station_id` | `UUID` | NOT NULL | FK → `stations.id` |
| `status` | `shipment_status` | NOT NULL | DEFAULT `PLANNED` |
| `dispatched_at` | `TIMESTAMPTZ` | NULL | |
| `expected_at` | `TIMESTAMPTZ` | NULL | |
| `delivered_at` | `TIMESTAMPTZ` | NULL | |
| `notes` | `TEXT` | NULL | |
| `created_by` | `UUID` | NULL | FK → `profiles.id` |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

---

### `shipment_items`

Line items within a shipment.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `shipment_id` | `UUID` | NOT NULL | FK → `shipments.id` ON DELETE CASCADE |
| `item_id` | `UUID` | NOT NULL | FK → `inventory_items.id` |
| `quantity` | `DOUBLE PRECISION` | NOT NULL | |

---

## MAINTENANCE Domain

### `maintenance_records`

A maintenance activity on an asset.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `asset_id` | `UUID` | NOT NULL | FK → `assets.id` |
| `station_id` | `UUID` | NOT NULL | FK → `stations.id` |
| `maintenance_type` | `maintenance_type` | NOT NULL | |
| `priority` | `maintenance_priority` | NOT NULL | DEFAULT `MEDIUM` |
| `status` | `maintenance_status` | NOT NULL | DEFAULT `SCHEDULED` |
| `description` | `TEXT` | NOT NULL | |
| `scheduled_at` | `TIMESTAMPTZ` | NULL | |
| `started_at` | `TIMESTAMPTZ` | NULL | |
| `completed_at` | `TIMESTAMPTZ` | NULL | |
| `performed_by` | `UUID` | NULL | FK → `profiles.id` |
| `created_by` | `UUID` | NULL | FK → `profiles.id` |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

---

### `maintenance_events`

Log of discrete events within a maintenance record.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `maintenance_id` | `UUID` | NOT NULL | FK → `maintenance_records.id` ON DELETE CASCADE |
| `event_type` | `TEXT` | NOT NULL | e.g. `STARTED`, `PARTS_ORDERED`, `COMPLETED`, `NOTE` |
| `description` | `TEXT` | NOT NULL | |
| `recorded_by` | `UUID` | NULL | FK → `profiles.id` |
| `recorded_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

---

## COMMANDS Domain

Implements the principle: **HQ requests; station validates and executes.**

### `commands`

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `station_id` | `UUID` | NOT NULL | FK → `stations.id` |
| `created_by` | `UUID` | NOT NULL | FK → `profiles.id` — HQ user |
| `command_type` | `command_type` | NOT NULL | |
| `parameters` | `JSONB` | NULL | Command-specific parameters |
| `status` | `command_status` | NOT NULL | DEFAULT `PENDING` |
| `rejection_reason` | `TEXT` | NULL | Populated if status = `REJECTED` |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |
| `expires_at` | `TIMESTAMPTZ` | NULL | NULL = no expiry |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

**Index:** `(station_id, status)` — for station polling pending commands.

---

### `command_executions`

Records the outcome when a station executes or rejects a command.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `command_id` | `UUID` | NOT NULL | FK → `commands.id` ON DELETE CASCADE |
| `executed_by` | `UUID` | NULL | FK → `profiles.id` — station operator |
| `result` | `TEXT` | NULL | Description of outcome |
| `result_metadata` | `JSONB` | NULL | Machine-readable execution result |
| `executed_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

---

## ALERTS Domain

Alerts are **temporary**. No permanent alert history table.

### `alert_rules`

Configurable rules that trigger alerts.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `station_id` | `UUID` | NOT NULL | FK → `stations.id` |
| `name` | `TEXT` | NOT NULL | |
| `description` | `TEXT` | NULL | |
| `severity` | `alert_severity` | NOT NULL | |
| `condition_expression` | `TEXT` | NOT NULL | Human-readable condition e.g. `fuel_level < 20%` |
| `is_active` | `BOOLEAN` | NOT NULL | DEFAULT `TRUE` |
| `created_by` | `UUID` | NULL | FK → `profiles.id` |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

---

### `active_alerts`

Currently live alerts. Removed when resolved or expired.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `station_id` | `UUID` | NOT NULL | FK → `stations.id` |
| `asset_id` | `UUID` | NULL | FK → `assets.id` |
| `sensor_id` | `UUID` | NULL | FK → `sensors.id` |
| `alert_rule_id` | `UUID` | NULL | FK → `alert_rules.id` ON DELETE SET NULL |
| `severity` | `alert_severity` | NOT NULL | |
| `alert_type` | `TEXT` | NOT NULL | e.g. `LOW_FUEL`, `HIGH_TEMPERATURE` |
| `message` | `TEXT` | NOT NULL | |
| `status` | `alert_status` | NOT NULL | DEFAULT `ACTIVE` |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |
| `acknowledged_at` | `TIMESTAMPTZ` | NULL | |
| `acknowledged_by` | `UUID` | NULL | FK → `profiles.id` |
| `expires_at` | `TIMESTAMPTZ` | NULL | |

---

## AUDIT Domain

### `audit_logs`

Immutable record of user actions on key entities.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | `UUID` | NOT NULL | PK |
| `user_id` | `UUID` | NULL | FK → `profiles.id` — NULL for system actions |
| `station_id` | `UUID` | NULL | FK → `stations.id` — if action is station-scoped |
| `action` | `TEXT` | NOT NULL | e.g. `CREATE`, `UPDATE`, `DELETE`, `LOGIN`, `COMMAND_ISSUED` |
| `entity_type` | `TEXT` | NOT NULL | e.g. `asset`, `command`, `personnel` |
| `entity_id` | `UUID` | NULL | The affected row's PK |
| `old_value` | `JSONB` | NULL | Previous state (for UPDATE/DELETE) |
| `new_value` | `JSONB` | NULL | New state (for CREATE/UPDATE) |
| `ip_address` | `INET` | NULL | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | DEFAULT `now()` |

**Note:** `audit_logs` is append-only. No UPDATE or DELETE is permitted via RLS.

---

## Relationships & Cardinality

```text
auth.users      1──1  profiles
profiles        M──N  roles           (via user_roles)
roles           M──N  permissions     (via role_permissions)
profiles        M──N  stations        (via station_access)

stations        1──M  station_areas
stations        1──M  assets
stations        1──M  personnel (via station_assignments)
stations        1──M  energy_systems
stations        1──M  inventory
stations        1──M  shipments

station_areas   1──M  assets
assets          1──M  assets          (self-referential: parent_asset_id)
assets          1──M  sensors
assets          1──M  asset_readings
assets          1──M  maintenance_records
assets          1──M  asset_status_history
assets          M──N  energy_sources  (via energy_assets)

personnel       1──M  station_assignments
personnel       1──M  personnel_health_status
personnel       0──1  profiles

sensors         1──M  sensor_configurations
sensors         1──M  asset_readings

energy_systems  1──M  energy_sources
energy_sources  M──N  assets          (via energy_assets)

inventory_items M──N  stations        (via inventory)
shipments       1──M  shipment_items
shipment_items  M──1  inventory_items

commands        1──M  command_executions
alert_rules     1──M  active_alerts
maintenance_records  1──M  maintenance_events
```

---

## Index Strategy

| Table | Index Columns | Reason |
|-------|--------------|--------|
| `profiles` | `employee_code` | Unique lookup |
| `station_access` | `(user_id, station_id)` | Permission checks |
| `stations` | `code` | Station lookup by code |
| `assets` | `(station_id, status)` | Station asset dashboard |
| `assets` | `asset_code` | Unique asset lookup |
| `sensors` | `(station_id, status)` | Active sensor list |
| `energy_readings` | `(station_id, time DESC)` | Time-series queries |
| `environment_readings` | `(station_id, time DESC)` | Time-series queries |
| `asset_readings` | `(asset_id, time DESC)` | Asset-level queries |
| `personnel_health_status` | `(personnel_id, recorded_at DESC)` | Latest health status |
| `commands` | `(station_id, status)` | Pending command polling |
| `maintenance_records` | `(station_id, status)` | Dashboard |
| `active_alerts` | `(station_id, severity, status)` | Alert dashboard |
| `audit_logs` | `(entity_type, entity_id)` | Entity audit trail |
| `audit_logs` | `(user_id, created_at DESC)` | User activity |
| `inventory` | `(station_id, item_id)` | Unique stock |
| `station_assignments` | `(personnel_id, status)` | Current assignment |

---

## Row-Level Security Strategy

Supabase Auth provides the JWT. The application extracts `auth.uid()` (= `profiles.id`) to enforce RLS.

### Principles

1. **`SUPER_ADMIN`** bypasses all RLS via a bypass policy (role-based).
2. **Station-scoped data** (assets, telemetry, personnel, commands) is filtered by `station_access`.
3. **Health data** (`personnel_health_status`) requires explicit `health.read` permission check.
4. **Audit logs** are readable by `audit.read` permission; never writable by end users.
5. **Telemetry tables** are insert-only for station service accounts; read for users with `telemetry.read`.

### Pattern

```sql
-- Example: assets
CREATE POLICY "station_member_can_read_assets"
ON assets FOR SELECT
USING (
    station_id IN (
        SELECT station_id FROM station_access
        WHERE user_id = auth.uid()
    )
);
```

Full RLS policies are in the migration script.

---

## Telemetry Retention Policy

| Table | Retention |
|-------|-----------|
| `energy_readings` | 30 days |
| `environment_readings` | 30 days |
| `asset_readings` | 30 days |
| `scientific_observations` | **Permanent** |
| `audit_logs` | **Permanent** |
| `active_alerts` | Until resolved/expired (no fixed retention) |

**Implementation:** `pg_cron` scheduled job or Supabase Edge Function running nightly:

```sql
DELETE FROM energy_readings      WHERE time      < now() - INTERVAL '30 days';
DELETE FROM environment_readings WHERE time      < now() - INTERVAL '30 days';
DELETE FROM asset_readings       WHERE time      < now() - INTERVAL '30 days';
DELETE FROM active_alerts        WHERE expires_at < now() AND status != 'ACTIVE';
```

---

## What is Deliberately Excluded

The following are **out of scope for v1** and should not be added without a formal schema change:

| Excluded | Reason |
|----------|--------|
| Document / file metadata | No file storage in v1 |
| Complex medical records | Health status only |
| Permanent alert history | Alerts are temporary |
| Message-transfer-session modeling | Not in scope |
| AI/ML prediction tables | Future iteration |
| Digital-twin duplicate tables | Operational DB only |
| Room-level BIM spatial model | Not in scope |
| Research paper storage | No document storage |
| OAuth provider tables | Supabase Auth handles this |
| Websocket session state | Stateless architecture |
