-- =============================================================================
-- DTFIAS — Supabase PostgreSQL Migration
-- Version: 001 — Initial Schema
-- Description: Full schema creation for Digital Twin for Indian Antarctic Stations
-- Run in: Supabase SQL Editor or via supabase db push
-- =============================================================================
-- NOTE: Run this entire script in one transaction. On failure, nothing is committed.
-- =============================================================================

BEGIN;

-- =============================================================================
-- SECTION 0: Extensions
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";   -- gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS "pg_cron";    -- telemetry retention (if available on your Supabase plan)

-- =============================================================================
-- SECTION 1: Enumerations
-- =============================================================================

CREATE TYPE station_status    AS ENUM ('ACTIVE', 'INACTIVE', 'UNDER_MAINTENANCE', 'DECOMMISSIONED');
CREATE TYPE station_type      AS ENUM ('RESEARCH_STATION', 'SUMMER_CAMP', 'FIELD_BASE', 'RELAY_STATION');
CREATE TYPE profile_status    AS ENUM ('ACTIVE', 'INACTIVE', 'SUSPENDED');
CREATE TYPE assignment_status AS ENUM ('ACTIVE', 'COMPLETED', 'CANCELLED');
CREATE TYPE health_status     AS ENUM ('HEALTHY', 'ILL', 'INJURED', 'UNDER_OBSERVATION', 'MEDICAL_LEAVE', 'UNFIT');
CREATE TYPE asset_status      AS ENUM ('OPERATIONAL', 'DEGRADED', 'UNDER_MAINTENANCE', 'DECOMMISSIONED', 'STANDBY');
CREATE TYPE asset_criticality AS ENUM ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW');
CREATE TYPE sensor_status     AS ENUM ('ACTIVE', 'INACTIVE', 'FAULTY', 'CALIBRATING');
CREATE TYPE reading_quality   AS ENUM ('GOOD', 'UNCERTAIN', 'BAD', 'MISSING');
CREATE TYPE energy_source_type AS ENUM ('DIESEL', 'SOLAR', 'WIND', 'BATTERY', 'HYBRID');
CREATE TYPE inventory_unit    AS ENUM ('LITRE', 'KILOGRAM', 'UNIT', 'METRE', 'KILOWATT_HOUR', 'BOX', 'PALLET');
CREATE TYPE transaction_type  AS ENUM ('RECEIVED', 'CONSUMED', 'TRANSFERRED', 'ADJUSTED', 'DISPOSED');
CREATE TYPE shipment_status   AS ENUM ('PLANNED', 'DISPATCHED', 'IN_TRANSIT', 'DELIVERED', 'CANCELLED');
CREATE TYPE maintenance_type  AS ENUM ('INSPECTION', 'PREVENTIVE', 'CORRECTIVE', 'EMERGENCY', 'CALIBRATION', 'UPGRADE');
CREATE TYPE maintenance_status AS ENUM ('SCHEDULED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', 'DEFERRED');
CREATE TYPE maintenance_priority AS ENUM ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW');
CREATE TYPE command_type      AS ENUM ('SYSTEM_CONTROL', 'SENSOR_CONTROL', 'ENERGY_CONTROL', 'LOGISTICS_CONTROL', 'PERSONNEL_CONTROL', 'ALERT_CONTROL');
CREATE TYPE command_status    AS ENUM ('PENDING', 'RECEIVED', 'VALIDATED', 'REJECTED', 'EXECUTING', 'EXECUTED', 'FAILED', 'EXPIRED');
CREATE TYPE alert_severity    AS ENUM ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO');
CREATE TYPE alert_status      AS ENUM ('ACTIVE', 'ACKNOWLEDGED', 'RESOLVED', 'EXPIRED');
CREATE TYPE observation_type  AS ENUM (
    'AIR_TEMPERATURE', 'SNOW_OBSERVATION', 'ICE_OBSERVATION',
    'ATMOSPHERIC_PRESSURE', 'WIND_OBSERVATION', 'PRECIPITATION',
    'VISIBILITY', 'UV_INDEX', 'SEA_ICE_EXTENT'
);
CREATE TYPE access_level      AS ENUM ('READ', 'WRITE', 'ADMIN');

-- =============================================================================
-- SECTION 2: Helper — auto-update updated_at trigger function
-- =============================================================================

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

-- =============================================================================
-- SECTION 3: AUTH DOMAIN
-- =============================================================================

-- profiles — 1:1 with auth.users
CREATE TABLE profiles (
    id              UUID        PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    full_name       TEXT        NOT NULL,
    employee_code   TEXT        UNIQUE NOT NULL,
    designation     TEXT,
    organization    TEXT,
    phone           TEXT,
    status          profile_status NOT NULL DEFAULT 'ACTIVE',
    avatar_url      TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TRIGGER trg_profiles_updated_at
    BEFORE UPDATE ON profiles
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

COMMENT ON TABLE profiles IS 'Application user profiles — 1:1 with auth.users. Supabase manages authentication; this table manages application identity.';

-- =============================================================================
-- SECTION 4: RBAC DOMAIN
-- =============================================================================

-- roles
CREATE TABLE roles (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT        UNIQUE NOT NULL,
    description TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE roles IS 'Application roles. Users are assigned one or more roles via user_roles.';

-- permissions
CREATE TABLE permissions (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    code        TEXT        UNIQUE NOT NULL,
    description TEXT
);

COMMENT ON TABLE permissions IS 'Fine-grained permission codes. Assigned to roles via role_permissions.';

-- user_roles — M:N junction
CREATE TABLE user_roles (
    user_id     UUID        NOT NULL REFERENCES profiles(id)   ON DELETE CASCADE,
    role_id     UUID        NOT NULL REFERENCES roles(id)      ON DELETE CASCADE,
    assigned_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    assigned_by UUID        REFERENCES profiles(id)            ON DELETE SET NULL,
    PRIMARY KEY (user_id, role_id)
);

COMMENT ON TABLE user_roles IS 'Many-to-many: a user can hold multiple roles.';

-- role_permissions — M:N junction
CREATE TABLE role_permissions (
    role_id       UUID NOT NULL REFERENCES roles(id)       ON DELETE CASCADE,
    permission_id UUID NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

COMMENT ON TABLE role_permissions IS 'Many-to-many: a role grants multiple permissions.';

-- station_access — grants user access to a specific station
CREATE TABLE station_access (
    id           UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id      UUID         NOT NULL REFERENCES profiles(id)  ON DELETE CASCADE,
    station_id   UUID         NOT NULL,   -- FK added after stations table is created
    access_level access_level NOT NULL DEFAULT 'READ',
    granted_at   TIMESTAMPTZ  NOT NULL DEFAULT now(),
    granted_by   UUID         REFERENCES profiles(id)           ON DELETE SET NULL,
    UNIQUE (user_id, station_id)
);

COMMENT ON TABLE station_access IS 'Station-level access grants. Independent of role — a user can be HQ_OPERATOR but only see specific stations.';

-- =============================================================================
-- SECTION 5: STATIONS DOMAIN
-- =============================================================================

CREATE TABLE stations (
    id               UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    code             TEXT           UNIQUE NOT NULL,
    name             TEXT           NOT NULL,
    description      TEXT,
    station_type     station_type   NOT NULL,
    status           station_status NOT NULL DEFAULT 'ACTIVE',
    latitude         DOUBLE PRECISION,
    longitude        DOUBLE PRECISION,
    elevation_m      DOUBLE PRECISION,
    capacity         INTEGER,
    commissioned_at  DATE,
    created_at       TIMESTAMPTZ    NOT NULL DEFAULT now(),
    updated_at       TIMESTAMPTZ    NOT NULL DEFAULT now()
);

CREATE TRIGGER trg_stations_updated_at
    BEFORE UPDATE ON stations
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

COMMENT ON TABLE stations IS 'One row per Antarctic station. New stations are data, not schema changes.';
COMMENT ON COLUMN stations.code IS 'Short alphanumeric code: MAT, BHA, MAT2, etc.';

-- Now that stations exists, add the FK to station_access
ALTER TABLE station_access
    ADD CONSTRAINT fk_station_access_station
    FOREIGN KEY (station_id) REFERENCES stations(id) ON DELETE CASCADE;

-- station_areas — spatial/functional hierarchy within a station
CREATE TABLE station_areas (
    id             UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    station_id     UUID        NOT NULL REFERENCES stations(id)     ON DELETE CASCADE,
    parent_area_id UUID        REFERENCES station_areas(id)        ON DELETE SET NULL,
    name           TEXT        NOT NULL,
    area_type      TEXT,
    description    TEXT,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE station_areas IS 'Hierarchical areas within a station (e.g. Power System > Generator Room). Self-referential via parent_area_id.';

-- =============================================================================
-- SECTION 6: PERSONNEL DOMAIN
-- =============================================================================

CREATE TABLE personnel (
    id            UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id    UUID           REFERENCES profiles(id) ON DELETE SET NULL,
    employee_code TEXT           UNIQUE NOT NULL,
    full_name     TEXT           NOT NULL,
    designation   TEXT,
    organization  TEXT,
    phone         TEXT,
    email         TEXT,
    status        profile_status NOT NULL DEFAULT 'ACTIVE',
    created_at    TIMESTAMPTZ    NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ    NOT NULL DEFAULT now()
);

CREATE TRIGGER trg_personnel_updated_at
    BEFORE UPDATE ON personnel
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

COMMENT ON TABLE personnel IS 'Personnel records. A person may not have a login account (profile_id nullable). Tracks all expedition members.';

-- station_assignments — deployment history
CREATE TABLE station_assignments (
    id             UUID              PRIMARY KEY DEFAULT gen_random_uuid(),
    personnel_id   UUID              NOT NULL REFERENCES personnel(id)   ON DELETE CASCADE,
    station_id     UUID              NOT NULL REFERENCES stations(id)    ON DELETE CASCADE,
    station_role   TEXT,
    arrival_date   DATE              NOT NULL,
    departure_date DATE,
    status         assignment_status NOT NULL DEFAULT 'ACTIVE',
    notes          TEXT,
    created_at     TIMESTAMPTZ       NOT NULL DEFAULT now()
);

COMMENT ON TABLE station_assignments IS 'Each deployment of a person to a station. departure_date NULL means currently deployed.';

-- personnel_health_status — basic status only, no vitals
CREATE TABLE personnel_health_status (
    id           UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    personnel_id UUID          NOT NULL REFERENCES personnel(id) ON DELETE CASCADE,
    station_id   UUID          NOT NULL REFERENCES stations(id),
    status       health_status NOT NULL,
    condition    TEXT,
    notes        TEXT,
    recorded_at  TIMESTAMPTZ   NOT NULL DEFAULT now(),
    recorded_by  UUID          REFERENCES profiles(id) ON DELETE SET NULL
);

COMMENT ON TABLE personnel_health_status IS 'Basic health status log — status and optional free-text condition only. No vitals. Access restricted by RBAC.';

-- =============================================================================
-- SECTION 7: ASSETS DOMAIN
-- =============================================================================

CREATE TABLE asset_types (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT        UNIQUE NOT NULL,
    category    TEXT,
    description TEXT
);

COMMENT ON TABLE asset_types IS 'Lookup table of asset categories (Generator, Solar Panel, HVAC, etc.).';

CREATE TABLE assets (
    id               UUID              PRIMARY KEY DEFAULT gen_random_uuid(),
    station_id       UUID              NOT NULL REFERENCES stations(id),
    area_id          UUID              REFERENCES station_areas(id)  ON DELETE SET NULL,
    asset_type_id    UUID              NOT NULL REFERENCES asset_types(id),
    parent_asset_id  UUID              REFERENCES assets(id)         ON DELETE SET NULL,
    asset_code       TEXT              UNIQUE NOT NULL,
    name             TEXT              NOT NULL,
    manufacturer     TEXT,
    model            TEXT,
    serial_number    TEXT,
    status           asset_status      NOT NULL DEFAULT 'OPERATIONAL',
    criticality      asset_criticality NOT NULL DEFAULT 'MEDIUM',
    installation_date DATE,
    commissioned_at  DATE,
    metadata         JSONB,
    created_at       TIMESTAMPTZ       NOT NULL DEFAULT now(),
    updated_at       TIMESTAMPTZ       NOT NULL DEFAULT now()
);

CREATE TRIGGER trg_assets_updated_at
    BEFORE UPDATE ON assets
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

COMMENT ON TABLE assets IS 'Physical equipment. Self-referential (parent_asset_id) for hierarchical assets like battery banks containing individual batteries.';
COMMENT ON COLUMN assets.metadata IS 'Flexible JSONB for asset-specific technical specs (rated power, fuel type, etc.).';

-- asset_status_history — immutable status change log
CREATE TABLE asset_status_history (
    id         UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id   UUID         NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    old_status asset_status,
    new_status asset_status NOT NULL,
    reason     TEXT,
    changed_by UUID         REFERENCES profiles(id) ON DELETE SET NULL,
    changed_at TIMESTAMPTZ  NOT NULL DEFAULT now()
);

COMMENT ON TABLE asset_status_history IS 'Immutable audit trail of asset status transitions. Written by a trigger on assets.status update.';

-- Trigger to auto-write asset_status_history on status change
CREATE OR REPLACE FUNCTION log_asset_status_change()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.status IS DISTINCT FROM OLD.status THEN
        INSERT INTO asset_status_history (asset_id, old_status, new_status)
        VALUES (NEW.id, OLD.status, NEW.status);
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_asset_status_history
    AFTER UPDATE ON assets
    FOR EACH ROW EXECUTE FUNCTION log_asset_status_change();

-- =============================================================================
-- SECTION 8: SENSORS DOMAIN
-- =============================================================================

CREATE TABLE sensor_types (
    id           UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    name         TEXT        UNIQUE NOT NULL,
    description  TEXT,
    default_unit TEXT
);

COMMENT ON TABLE sensor_types IS 'Lookup table of sensor categories (TEMPERATURE, FUEL_LEVEL, etc.).';

CREATE TABLE sensors (
    id              UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    station_id      UUID          NOT NULL REFERENCES stations(id),
    asset_id        UUID          REFERENCES assets(id)       ON DELETE SET NULL,
    sensor_type_id  UUID          NOT NULL REFERENCES sensor_types(id),
    sensor_code     TEXT          UNIQUE NOT NULL,
    name            TEXT          NOT NULL,
    unit            TEXT          NOT NULL,
    status          sensor_status NOT NULL DEFAULT 'ACTIVE',
    last_reading_at TIMESTAMPTZ,
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ   NOT NULL DEFAULT now()
);

CREATE TRIGGER trg_sensors_updated_at
    BEFORE UPDATE ON sensors
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

COMMENT ON TABLE sensors IS 'Physical sensor instances. Linked to an asset; belongs to a station.';

CREATE TABLE sensor_configurations (
    id                         UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    sensor_id                  UUID            NOT NULL REFERENCES sensors(id) ON DELETE CASCADE,
    sampling_interval_seconds  INTEGER         NOT NULL,
    min_threshold              DOUBLE PRECISION,
    max_threshold              DOUBLE PRECISION,
    calibration_offset         DOUBLE PRECISION DEFAULT 0.0,
    effective_from             TIMESTAMPTZ     NOT NULL DEFAULT now(),
    notes                      TEXT
);

COMMENT ON TABLE sensor_configurations IS 'Versioned sensor configuration. The latest effective_from record is the active config.';

-- =============================================================================
-- SECTION 9: TELEMETRY DOMAIN
-- =============================================================================

CREATE TABLE energy_readings (
    time                TIMESTAMPTZ       NOT NULL,
    station_id          UUID              NOT NULL REFERENCES stations(id),
    energy_asset_id     UUID              REFERENCES assets(id),
    generation_kw       DOUBLE PRECISION,
    consumption_kw      DOUBLE PRECISION,
    battery_soc_pct     DOUBLE PRECISION,
    voltage_v           DOUBLE PRECISION,
    current_a           DOUBLE PRECISION,
    fuel_consumption_lph DOUBLE PRECISION,
    quality             reading_quality   NOT NULL DEFAULT 'GOOD',
    PRIMARY KEY (time, station_id)
);

COMMENT ON TABLE energy_readings IS 'Time-series energy telemetry. 30-day retention policy.';

CREATE TABLE environment_readings (
    time                 TIMESTAMPTZ     NOT NULL,
    station_id           UUID            NOT NULL REFERENCES stations(id),
    temperature_c        DOUBLE PRECISION,
    humidity_pct         DOUBLE PRECISION,
    pressure_hpa         DOUBLE PRECISION,
    wind_speed_mps       DOUBLE PRECISION,
    wind_direction_deg   DOUBLE PRECISION,
    solar_radiation_wm2  DOUBLE PRECISION,
    quality              reading_quality NOT NULL DEFAULT 'GOOD',
    PRIMARY KEY (time, station_id)
);

COMMENT ON TABLE environment_readings IS 'Time-series operational weather telemetry. 30-day retention policy.';

CREATE TABLE asset_readings (
    time      TIMESTAMPTZ      NOT NULL,
    asset_id  UUID             NOT NULL REFERENCES assets(id),
    sensor_id UUID             REFERENCES sensors(id),
    metric    TEXT             NOT NULL,
    value     DOUBLE PRECISION NOT NULL,
    unit      TEXT,
    quality   reading_quality  NOT NULL DEFAULT 'GOOD',
    PRIMARY KEY (time, asset_id, metric)
);

COMMENT ON TABLE asset_readings IS 'Generic time-series for asset/sensor metrics. 30-day retention.';

-- =============================================================================
-- SECTION 10: ENERGY DOMAIN
-- =============================================================================

CREATE TABLE energy_systems (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    station_id  UUID        NOT NULL REFERENCES stations(id),
    name        TEXT        NOT NULL,
    description TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE energy_sources (
    id               UUID               PRIMARY KEY DEFAULT gen_random_uuid(),
    energy_system_id UUID               NOT NULL REFERENCES energy_systems(id),
    source_type      energy_source_type NOT NULL,
    name             TEXT               NOT NULL,
    capacity_kw      DOUBLE PRECISION,
    status           asset_status       NOT NULL DEFAULT 'OPERATIONAL',
    created_at       TIMESTAMPTZ        NOT NULL DEFAULT now()
);

CREATE TABLE energy_assets (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    energy_source_id UUID NOT NULL REFERENCES energy_sources(id),
    asset_id         UUID NOT NULL REFERENCES assets(id),
    UNIQUE (energy_source_id, asset_id)
);

-- =============================================================================
-- SECTION 11: ENVIRONMENT DOMAIN (Scientific)
-- =============================================================================

CREATE TABLE scientific_observations (
    id               UUID             PRIMARY KEY DEFAULT gen_random_uuid(),
    station_id       UUID             NOT NULL REFERENCES stations(id),
    observation_type observation_type NOT NULL,
    observed_at      TIMESTAMPTZ      NOT NULL,
    value            DOUBLE PRECISION,
    text_value       TEXT,
    unit             TEXT,
    quality          reading_quality  NOT NULL DEFAULT 'GOOD',
    source           TEXT,
    metadata         JSONB,
    recorded_by      UUID             REFERENCES profiles(id) ON DELETE SET NULL,
    created_at       TIMESTAMPTZ      NOT NULL DEFAULT now()
);

COMMENT ON TABLE scientific_observations IS 'Scientific environmental observations. PERMANENT — not subject to 30-day telemetry retention.';

-- =============================================================================
-- SECTION 12: LOGISTICS DOMAIN
-- =============================================================================

CREATE TABLE inventory_items (
    id          UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT           NOT NULL,
    category    TEXT,
    unit        inventory_unit NOT NULL,
    description TEXT,
    created_at  TIMESTAMPTZ    NOT NULL DEFAULT now()
);

CREATE TABLE inventory (
    id                UUID             PRIMARY KEY DEFAULT gen_random_uuid(),
    station_id        UUID             NOT NULL REFERENCES stations(id),
    item_id           UUID             NOT NULL REFERENCES inventory_items(id),
    quantity          DOUBLE PRECISION NOT NULL DEFAULT 0,
    minimum_threshold DOUBLE PRECISION,
    updated_at        TIMESTAMPTZ      NOT NULL DEFAULT now(),
    UNIQUE (station_id, item_id),
    CONSTRAINT chk_quantity_non_negative CHECK (quantity >= 0)
);

-- shipments must exist before inventory_transactions references it
CREATE TABLE shipments (
    id                     UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    origin                 TEXT            NOT NULL,
    destination_station_id UUID            NOT NULL REFERENCES stations(id),
    status                 shipment_status NOT NULL DEFAULT 'PLANNED',
    dispatched_at          TIMESTAMPTZ,
    expected_at            TIMESTAMPTZ,
    delivered_at           TIMESTAMPTZ,
    notes                  TEXT,
    created_by             UUID            REFERENCES profiles(id) ON DELETE SET NULL,
    created_at             TIMESTAMPTZ     NOT NULL DEFAULT now()
);

CREATE TABLE inventory_transactions (
    id               UUID             PRIMARY KEY DEFAULT gen_random_uuid(),
    station_id       UUID             NOT NULL REFERENCES stations(id),
    item_id          UUID             NOT NULL REFERENCES inventory_items(id),
    transaction_type transaction_type NOT NULL,
    quantity_delta   DOUBLE PRECISION NOT NULL,
    notes            TEXT,
    transacted_by    UUID             REFERENCES profiles(id)  ON DELETE SET NULL,
    transacted_at    TIMESTAMPTZ      NOT NULL DEFAULT now(),
    shipment_id      UUID             REFERENCES shipments(id) ON DELETE SET NULL
);

CREATE OR REPLACE FUNCTION apply_inventory_transaction()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO inventory (station_id, item_id, quantity)
    VALUES (NEW.station_id, NEW.item_id, NEW.quantity_delta)
    ON CONFLICT (station_id, item_id)
    DO UPDATE SET
        quantity   = inventory.quantity + NEW.quantity_delta,
        updated_at = now();
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_apply_inventory_transaction
    AFTER INSERT ON inventory_transactions
    FOR EACH ROW EXECUTE FUNCTION apply_inventory_transaction();

CREATE TABLE shipment_items (
    id          UUID             PRIMARY KEY DEFAULT gen_random_uuid(),
    shipment_id UUID             NOT NULL REFERENCES shipments(id) ON DELETE CASCADE,
    item_id     UUID             NOT NULL REFERENCES inventory_items(id),
    quantity    DOUBLE PRECISION NOT NULL,
    CONSTRAINT chk_shipment_qty_positive CHECK (quantity > 0)
);

-- =============================================================================
-- SECTION 13: MAINTENANCE DOMAIN
-- =============================================================================

CREATE TABLE maintenance_records (
    id               UUID                 PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id         UUID                 NOT NULL REFERENCES assets(id),
    station_id       UUID                 NOT NULL REFERENCES stations(id),
    maintenance_type maintenance_type     NOT NULL,
    priority         maintenance_priority NOT NULL DEFAULT 'MEDIUM',
    status           maintenance_status   NOT NULL DEFAULT 'SCHEDULED',
    description      TEXT                 NOT NULL,
    scheduled_at     TIMESTAMPTZ,
    started_at       TIMESTAMPTZ,
    completed_at     TIMESTAMPTZ,
    performed_by     UUID                 REFERENCES profiles(id) ON DELETE SET NULL,
    created_by       UUID                 REFERENCES profiles(id) ON DELETE SET NULL,
    created_at       TIMESTAMPTZ          NOT NULL DEFAULT now(),
    updated_at       TIMESTAMPTZ          NOT NULL DEFAULT now()
);

CREATE TRIGGER trg_maintenance_updated_at
    BEFORE UPDATE ON maintenance_records
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE maintenance_events (
    id             UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    maintenance_id UUID        NOT NULL REFERENCES maintenance_records(id) ON DELETE CASCADE,
    event_type     TEXT        NOT NULL,
    description    TEXT        NOT NULL,
    recorded_by    UUID        REFERENCES profiles(id) ON DELETE SET NULL,
    recorded_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =============================================================================
-- SECTION 14: COMMANDS DOMAIN
-- =============================================================================

CREATE TABLE commands (
    id               UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    station_id       UUID           NOT NULL REFERENCES stations(id),
    created_by       UUID           NOT NULL REFERENCES profiles(id),
    command_type     command_type   NOT NULL,
    parameters       JSONB,
    status           command_status NOT NULL DEFAULT 'PENDING',
    rejection_reason TEXT,
    created_at       TIMESTAMPTZ    NOT NULL DEFAULT now(),
    expires_at       TIMESTAMPTZ,
    updated_at       TIMESTAMPTZ    NOT NULL DEFAULT now()
);

CREATE TRIGGER trg_commands_updated_at
    BEFORE UPDATE ON commands
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

COMMENT ON TABLE commands IS 'Commands issued by HQ. Station validates and executes. HQ never directly modifies physical station state.';

CREATE TABLE command_executions (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    command_id      UUID        NOT NULL REFERENCES commands(id) ON DELETE CASCADE,
    executed_by     UUID        REFERENCES profiles(id) ON DELETE SET NULL,
    result          TEXT,
    result_metadata JSONB,
    executed_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =============================================================================
-- SECTION 15: ALERTS DOMAIN
-- =============================================================================

CREATE TABLE alert_rules (
    id                   UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    station_id           UUID           NOT NULL REFERENCES stations(id),
    name                 TEXT           NOT NULL,
    description          TEXT,
    severity             alert_severity NOT NULL,
    condition_expression TEXT           NOT NULL,
    is_active            BOOLEAN        NOT NULL DEFAULT TRUE,
    created_by           UUID           REFERENCES profiles(id) ON DELETE SET NULL,
    created_at           TIMESTAMPTZ    NOT NULL DEFAULT now()
);

CREATE TABLE active_alerts (
    id              UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    station_id      UUID           NOT NULL REFERENCES stations(id),
    asset_id        UUID           REFERENCES assets(id)      ON DELETE SET NULL,
    sensor_id       UUID           REFERENCES sensors(id)     ON DELETE SET NULL,
    alert_rule_id   UUID           REFERENCES alert_rules(id) ON DELETE SET NULL,
    severity        alert_severity NOT NULL,
    alert_type      TEXT           NOT NULL,
    message         TEXT           NOT NULL,
    status          alert_status   NOT NULL DEFAULT 'ACTIVE',
    created_at      TIMESTAMPTZ    NOT NULL DEFAULT now(),
    acknowledged_at TIMESTAMPTZ,
    acknowledged_by UUID           REFERENCES profiles(id) ON DELETE SET NULL,
    expires_at      TIMESTAMPTZ
);

COMMENT ON TABLE active_alerts IS 'Live alerts only. Removed when resolved or expired — no permanent alert history.';

-- =============================================================================
-- SECTION 16: AUDIT DOMAIN
-- =============================================================================

CREATE TABLE audit_logs (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID        REFERENCES profiles(id)  ON DELETE SET NULL,
    station_id  UUID        REFERENCES stations(id)  ON DELETE SET NULL,
    action      TEXT        NOT NULL,
    entity_type TEXT        NOT NULL,
    entity_id   UUID,
    old_value   JSONB,
    new_value   JSONB,
    ip_address  INET,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE audit_logs IS 'Immutable append-only audit trail. RLS prevents user UPDATE/DELETE.';

-- =============================================================================
-- SECTION 17: INDEXES
-- =============================================================================

CREATE INDEX idx_user_roles_user           ON user_roles              (user_id);
CREATE INDEX idx_station_access_user       ON station_access          (user_id);
CREATE INDEX idx_station_access_station    ON station_access          (station_id);
CREATE INDEX idx_stations_code             ON stations                (code);
CREATE INDEX idx_stations_status           ON stations                (status);
CREATE INDEX idx_station_areas_station     ON station_areas           (station_id);
CREATE INDEX idx_personnel_profile         ON personnel               (profile_id);
CREATE INDEX idx_assignments_personnel     ON station_assignments      (personnel_id, status);
CREATE INDEX idx_assignments_station       ON station_assignments      (station_id,   status);
CREATE INDEX idx_health_personnel_time     ON personnel_health_status  (personnel_id, recorded_at DESC);
CREATE INDEX idx_assets_station_status     ON assets                  (station_id,   status);
CREATE INDEX idx_assets_code               ON assets                  (asset_code);
CREATE INDEX idx_assets_parent             ON assets                  (parent_asset_id);
CREATE INDEX idx_asset_hist_asset          ON asset_status_history    (asset_id,     changed_at DESC);
CREATE INDEX idx_sensors_station_status    ON sensors                 (station_id,   status);
CREATE INDEX idx_sensors_asset             ON sensors                 (asset_id);
CREATE INDEX idx_energy_readings_station   ON energy_readings         (station_id,   time DESC);
CREATE INDEX idx_env_readings_station      ON environment_readings    (station_id,   time DESC);
CREATE INDEX idx_asset_readings_asset      ON asset_readings          (asset_id,     time DESC);
CREATE INDEX idx_energy_sources_system     ON energy_sources          (energy_system_id);
CREATE INDEX idx_inventory_station         ON inventory               (station_id);
CREATE INDEX idx_inv_tx_station_item       ON inventory_transactions   (station_id,   item_id);
CREATE INDEX idx_inv_tx_time               ON inventory_transactions   (transacted_at DESC);
CREATE INDEX idx_shipments_station         ON shipments               (destination_station_id, status);
CREATE INDEX idx_maint_station_status      ON maintenance_records     (station_id,   status);
CREATE INDEX idx_maint_asset               ON maintenance_records     (asset_id);
CREATE INDEX idx_maint_events_record       ON maintenance_events      (maintenance_id);
CREATE INDEX idx_commands_station_status   ON commands                (station_id,   status);
CREATE INDEX idx_commands_created_by       ON commands                (created_by);
CREATE INDEX idx_command_exec_command      ON command_executions      (command_id);
CREATE INDEX idx_alerts_station_sev        ON active_alerts           (station_id,   severity, status);
CREATE INDEX idx_alerts_expires            ON active_alerts           (expires_at)   WHERE expires_at IS NOT NULL;
CREATE INDEX idx_audit_entity              ON audit_logs              (entity_type,  entity_id);
CREATE INDEX idx_audit_user_time           ON audit_logs              (user_id,      created_at DESC);
CREATE INDEX idx_audit_station_time        ON audit_logs              (station_id,   created_at DESC);
CREATE INDEX idx_sci_obs_station_type      ON scientific_observations (station_id,   observation_type);
CREATE INDEX idx_sci_obs_observed_at       ON scientific_observations (observed_at DESC);

-- =============================================================================
-- SECTION 18: ROW-LEVEL SECURITY
-- =============================================================================

ALTER TABLE profiles                ENABLE ROW LEVEL SECURITY;
ALTER TABLE roles                   ENABLE ROW LEVEL SECURITY;
ALTER TABLE permissions             ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_roles              ENABLE ROW LEVEL SECURITY;
ALTER TABLE role_permissions        ENABLE ROW LEVEL SECURITY;
ALTER TABLE station_access          ENABLE ROW LEVEL SECURITY;
ALTER TABLE stations                ENABLE ROW LEVEL SECURITY;
ALTER TABLE station_areas           ENABLE ROW LEVEL SECURITY;
ALTER TABLE personnel               ENABLE ROW LEVEL SECURITY;
ALTER TABLE station_assignments     ENABLE ROW LEVEL SECURITY;
ALTER TABLE personnel_health_status ENABLE ROW LEVEL SECURITY;
ALTER TABLE asset_types             ENABLE ROW LEVEL SECURITY;
ALTER TABLE assets                  ENABLE ROW LEVEL SECURITY;
ALTER TABLE asset_status_history    ENABLE ROW LEVEL SECURITY;
ALTER TABLE sensor_types            ENABLE ROW LEVEL SECURITY;
ALTER TABLE sensors                 ENABLE ROW LEVEL SECURITY;
ALTER TABLE sensor_configurations   ENABLE ROW LEVEL SECURITY;
ALTER TABLE energy_readings         ENABLE ROW LEVEL SECURITY;
ALTER TABLE environment_readings    ENABLE ROW LEVEL SECURITY;
ALTER TABLE asset_readings          ENABLE ROW LEVEL SECURITY;
ALTER TABLE energy_systems          ENABLE ROW LEVEL SECURITY;
ALTER TABLE energy_sources          ENABLE ROW LEVEL SECURITY;
ALTER TABLE energy_assets           ENABLE ROW LEVEL SECURITY;
ALTER TABLE scientific_observations ENABLE ROW LEVEL SECURITY;
ALTER TABLE inventory_items         ENABLE ROW LEVEL SECURITY;
ALTER TABLE inventory               ENABLE ROW LEVEL SECURITY;
ALTER TABLE inventory_transactions  ENABLE ROW LEVEL SECURITY;
ALTER TABLE shipments               ENABLE ROW LEVEL SECURITY;
ALTER TABLE shipment_items          ENABLE ROW LEVEL SECURITY;
ALTER TABLE maintenance_records     ENABLE ROW LEVEL SECURITY;
ALTER TABLE maintenance_events      ENABLE ROW LEVEL SECURITY;
ALTER TABLE commands                ENABLE ROW LEVEL SECURITY;
ALTER TABLE command_executions      ENABLE ROW LEVEL SECURITY;
ALTER TABLE alert_rules             ENABLE ROW LEVEL SECURITY;
ALTER TABLE active_alerts           ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs              ENABLE ROW LEVEL SECURITY;

-- ── Helper functions ──

CREATE OR REPLACE FUNCTION user_has_permission(perm_code TEXT)
RETURNS BOOLEAN LANGUAGE sql STABLE SECURITY DEFINER AS $$
    SELECT EXISTS (
        SELECT 1
        FROM user_roles ur
        JOIN role_permissions rp ON rp.role_id      = ur.role_id
        JOIN permissions p       ON p.id             = rp.permission_id
        WHERE ur.user_id = auth.uid() AND p.code = perm_code
    );
$$;

CREATE OR REPLACE FUNCTION user_has_station_access(sid UUID)
RETURNS BOOLEAN LANGUAGE sql STABLE SECURITY DEFINER AS $$
    SELECT EXISTS (
        SELECT 1 FROM station_access
        WHERE user_id = auth.uid() AND station_id = sid
    ) OR user_has_permission('station.manage');
$$;

-- ── PROFILES ──
CREATE POLICY "profiles_read"   ON profiles FOR SELECT USING (id = auth.uid() OR user_has_permission('personnel.read'));
CREATE POLICY "profiles_update" ON profiles FOR UPDATE USING (id = auth.uid());
CREATE POLICY "profiles_insert" ON profiles FOR INSERT WITH CHECK (user_has_permission('personnel.manage'));

-- ── ROLES / PERMISSIONS ──
CREATE POLICY "roles_read"       ON roles       FOR SELECT USING (auth.uid() IS NOT NULL);
CREATE POLICY "permissions_read" ON permissions FOR SELECT USING (auth.uid() IS NOT NULL);
CREATE POLICY "role_perm_manage" ON role_permissions FOR ALL USING (user_has_permission('station.manage'));

-- ── STATION ACCESS ──
CREATE POLICY "station_access_read"   ON station_access FOR SELECT USING (user_id = auth.uid() OR user_has_permission('station.manage'));
CREATE POLICY "station_access_manage" ON station_access FOR ALL   USING (user_has_permission('station.manage'));

-- ── STATIONS ──
CREATE POLICY "stations_read"   ON stations FOR SELECT USING (id IN (SELECT station_id FROM station_access WHERE user_id = auth.uid()) OR user_has_permission('station.manage'));
CREATE POLICY "stations_manage" ON stations FOR ALL   USING (user_has_permission('station.manage'));

-- ── STATION AREAS ──
CREATE POLICY "areas_read"   ON station_areas FOR SELECT USING (user_has_station_access(station_id));
CREATE POLICY "areas_manage" ON station_areas FOR ALL   USING (user_has_permission('station.manage'));

-- ── ASSETS ──
CREATE POLICY "assets_read"   ON assets FOR SELECT USING (user_has_station_access(station_id) AND user_has_permission('asset.read'));
CREATE POLICY "assets_manage" ON assets FOR ALL   USING (user_has_station_access(station_id) AND user_has_permission('asset.manage'));

-- ── ASSET HISTORY ──
CREATE POLICY "asset_hist_read" ON asset_status_history FOR SELECT
    USING (asset_id IN (SELECT id FROM assets WHERE user_has_station_access(station_id)) AND user_has_permission('asset.read'));

-- ── ASSET TYPES / SENSOR TYPES (lookup tables — any authenticated user) ──
CREATE POLICY "asset_types_read"  ON asset_types  FOR SELECT USING (auth.uid() IS NOT NULL);
CREATE POLICY "sensor_types_read" ON sensor_types FOR SELECT USING (auth.uid() IS NOT NULL);

-- ── PERSONNEL ──
CREATE POLICY "personnel_read"   ON personnel FOR SELECT USING (user_has_permission('personnel.read'));
CREATE POLICY "personnel_manage" ON personnel FOR ALL   USING (user_has_permission('personnel.manage'));

-- ── STATION ASSIGNMENTS ──
CREATE POLICY "assignments_read"   ON station_assignments FOR SELECT USING (user_has_station_access(station_id) AND user_has_permission('personnel.read'));
CREATE POLICY "assignments_manage" ON station_assignments FOR ALL   USING (user_has_permission('personnel.manage'));

-- ── HEALTH STATUS ──
CREATE POLICY "health_read"   ON personnel_health_status FOR SELECT USING (user_has_permission('health.read'));
CREATE POLICY "health_manage" ON personnel_health_status FOR ALL   USING (user_has_permission('health.manage'));

-- ── SENSORS ──
CREATE POLICY "sensors_read"   ON sensors FOR SELECT USING (user_has_station_access(station_id) AND user_has_permission('telemetry.read'));
CREATE POLICY "sensors_manage" ON sensors FOR ALL   USING (user_has_permission('asset.manage'));
CREATE POLICY "sensor_cfg_read"   ON sensor_configurations FOR SELECT USING (user_has_permission('telemetry.read'));
CREATE POLICY "sensor_cfg_manage" ON sensor_configurations FOR ALL   USING (user_has_permission('asset.manage'));

-- ── TELEMETRY ──
CREATE POLICY "energy_read"   ON energy_readings FOR SELECT USING (user_has_station_access(station_id) AND user_has_permission('energy.read'));
CREATE POLICY "energy_insert" ON energy_readings FOR INSERT WITH CHECK (user_has_station_access(station_id));
CREATE POLICY "env_read"      ON environment_readings FOR SELECT USING (user_has_station_access(station_id) AND user_has_permission('telemetry.read'));
CREATE POLICY "env_insert"    ON environment_readings FOR INSERT WITH CHECK (user_has_station_access(station_id));
CREATE POLICY "asset_rdg_read"   ON asset_readings FOR SELECT USING (asset_id IN (SELECT id FROM assets WHERE user_has_station_access(station_id)) AND user_has_permission('telemetry.read'));
CREATE POLICY "asset_rdg_insert" ON asset_readings FOR INSERT WITH CHECK (asset_id IN (SELECT id FROM assets WHERE user_has_station_access(station_id)));

-- ── ENERGY DOMAIN ──
CREATE POLICY "energy_sys_read"   ON energy_systems FOR SELECT USING (user_has_station_access(station_id) AND user_has_permission('energy.read'));
CREATE POLICY "energy_sys_manage" ON energy_systems FOR ALL   USING (user_has_permission('energy.manage'));
CREATE POLICY "energy_src_read"   ON energy_sources FOR SELECT USING (user_has_permission('energy.read'));
CREATE POLICY "energy_src_manage" ON energy_sources FOR ALL   USING (user_has_permission('energy.manage'));
CREATE POLICY "energy_assets_read"   ON energy_assets FOR SELECT USING (user_has_permission('energy.read'));
CREATE POLICY "energy_assets_manage" ON energy_assets FOR ALL   USING (user_has_permission('energy.manage'));

-- ── LOGISTICS ──
CREATE POLICY "inv_items_read"  ON inventory_items FOR SELECT USING (auth.uid() IS NOT NULL);
CREATE POLICY "inv_read"        ON inventory       FOR SELECT USING (user_has_station_access(station_id) AND user_has_permission('logistics.read'));
CREATE POLICY "inv_manage"      ON inventory       FOR ALL   USING (user_has_permission('logistics.manage'));
CREATE POLICY "inv_tx_read"     ON inventory_transactions FOR SELECT USING (user_has_station_access(station_id) AND user_has_permission('logistics.read'));
CREATE POLICY "inv_tx_insert"   ON inventory_transactions FOR INSERT WITH CHECK (user_has_permission('logistics.manage'));
CREATE POLICY "shipments_read"  ON shipments FOR SELECT USING (user_has_station_access(destination_station_id) AND user_has_permission('logistics.read'));
CREATE POLICY "shipments_manage" ON shipments FOR ALL  USING (user_has_permission('logistics.manage'));
CREATE POLICY "shipment_items_read"   ON shipment_items FOR SELECT USING (user_has_permission('logistics.read'));
CREATE POLICY "shipment_items_manage" ON shipment_items FOR ALL   USING (user_has_permission('logistics.manage'));

-- ── MAINTENANCE ──
CREATE POLICY "maint_read"   ON maintenance_records FOR SELECT USING (user_has_station_access(station_id) AND user_has_permission('maintenance.read'));
CREATE POLICY "maint_manage" ON maintenance_records FOR ALL   USING (user_has_permission('maintenance.manage'));
CREATE POLICY "maint_evt_read"   ON maintenance_events FOR SELECT USING (user_has_permission('maintenance.read'));
CREATE POLICY "maint_evt_manage" ON maintenance_events FOR ALL   USING (user_has_permission('maintenance.manage'));

-- ── COMMANDS ──
CREATE POLICY "cmd_create" ON commands FOR INSERT WITH CHECK (user_has_permission('command.create'));
CREATE POLICY "cmd_read"   ON commands FOR SELECT USING (user_has_station_access(station_id));
CREATE POLICY "cmd_update" ON commands FOR UPDATE USING (user_has_station_access(station_id) AND user_has_permission('command.execute'));
CREATE POLICY "cmd_exec_insert" ON command_executions FOR INSERT WITH CHECK (user_has_permission('command.execute'));
CREATE POLICY "cmd_exec_read"   ON command_executions FOR SELECT USING (command_id IN (SELECT id FROM commands WHERE user_has_station_access(station_id)));

-- ── ALERTS ──
CREATE POLICY "alert_rules_read"   ON alert_rules FOR SELECT USING (user_has_station_access(station_id) AND user_has_permission('alert.read'));
CREATE POLICY "alert_rules_manage" ON alert_rules FOR ALL   USING (user_has_permission('alert.manage'));
CREATE POLICY "alerts_read"   ON active_alerts FOR SELECT USING (user_has_station_access(station_id) AND user_has_permission('alert.read'));
CREATE POLICY "alerts_manage" ON active_alerts FOR ALL   USING (user_has_permission('alert.manage'));

-- ── AUDIT (append-only) ──
CREATE POLICY "audit_read"   ON audit_logs FOR SELECT USING (user_has_permission('audit.read'));
CREATE POLICY "audit_insert" ON audit_logs FOR INSERT WITH CHECK (TRUE);

-- ── SCIENTIFIC OBSERVATIONS ──
CREATE POLICY "sci_obs_read"   ON scientific_observations FOR SELECT USING (user_has_station_access(station_id) AND user_has_permission('telemetry.read'));
CREATE POLICY "sci_obs_insert" ON scientific_observations FOR INSERT WITH CHECK (user_has_station_access(station_id));

-- =============================================================================
-- SECTION 19: SEED DATA
-- =============================================================================

-- Roles
INSERT INTO roles (name, description) VALUES
    ('SUPER_ADMIN',      'Full unrestricted system access'),
    ('HQ_ADMIN',         'Headquarters-level administration'),
    ('HQ_OPERATOR',      'HQ monitoring and command issuance'),
    ('STATION_ADMIN',    'Station-level administration'),
    ('STATION_OPERATOR', 'Station daily operations'),
    ('ENGINEER',         'Engineering, maintenance, and asset management'),
    ('SCIENTIST',        'Scientific data access and observation recording'),
    ('VIEWER',           'Read-only access across permitted stations');

-- Permissions
INSERT INTO permissions (code, description) VALUES
    ('station.read',       'View station information'),
    ('station.manage',     'Create and modify stations'),
    ('asset.read',         'View assets and their status'),
    ('asset.manage',       'Create and modify assets'),
    ('personnel.read',     'View personnel records'),
    ('personnel.manage',   'Create and modify personnel records'),
    ('health.read',        'View personnel health status'),
    ('health.manage',      'Record and modify health status'),
    ('energy.read',        'View energy systems and telemetry'),
    ('energy.manage',      'Manage energy systems'),
    ('logistics.read',     'View inventory and shipments'),
    ('logistics.manage',   'Manage inventory and shipments'),
    ('maintenance.read',   'View maintenance records'),
    ('maintenance.manage', 'Create and manage maintenance records'),
    ('telemetry.read',     'Read sensor and telemetry data'),
    ('command.create',     'Issue commands to stations (HQ only)'),
    ('command.execute',    'Execute or reject commands at station level'),
    ('alert.read',         'View active alerts and rules'),
    ('alert.manage',       'Create, acknowledge, and resolve alerts'),
    ('audit.read',         'Read audit log entries');

-- SUPER_ADMIN: all permissions
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r, permissions p WHERE r.name = 'SUPER_ADMIN';

-- HQ_ADMIN
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r JOIN permissions p ON p.code IN (
    'station.read','station.manage','asset.read','asset.manage',
    'personnel.read','personnel.manage','health.read',
    'energy.read','energy.manage','logistics.read','logistics.manage',
    'maintenance.read','maintenance.manage','telemetry.read',
    'command.create','alert.read','alert.manage','audit.read'
) WHERE r.name = 'HQ_ADMIN';

-- HQ_OPERATOR
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r JOIN permissions p ON p.code IN (
    'station.read','asset.read','personnel.read','energy.read',
    'logistics.read','maintenance.read','telemetry.read','command.create','alert.read'
) WHERE r.name = 'HQ_OPERATOR';

-- STATION_ADMIN
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r JOIN permissions p ON p.code IN (
    'station.read','asset.read','asset.manage',
    'personnel.read','personnel.manage','health.read','health.manage',
    'energy.read','energy.manage','logistics.read','logistics.manage',
    'maintenance.read','maintenance.manage','telemetry.read',
    'command.execute','alert.read','alert.manage'
) WHERE r.name = 'STATION_ADMIN';

-- STATION_OPERATOR
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r JOIN permissions p ON p.code IN (
    'station.read','asset.read','personnel.read','health.read',
    'energy.read','logistics.read','maintenance.read','telemetry.read',
    'command.execute','alert.read','alert.manage'
) WHERE r.name = 'STATION_OPERATOR';

-- ENGINEER
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r JOIN permissions p ON p.code IN (
    'station.read','asset.read','asset.manage',
    'maintenance.read','maintenance.manage','energy.read','telemetry.read','alert.read'
) WHERE r.name = 'ENGINEER';

-- SCIENTIST
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r JOIN permissions p ON p.code IN (
    'station.read','telemetry.read','alert.read','energy.read','logistics.read'
) WHERE r.name = 'SCIENTIST';

-- VIEWER
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r JOIN permissions p ON p.code IN (
    'station.read','asset.read','energy.read','telemetry.read',
    'alert.read','logistics.read','maintenance.read','personnel.read'
) WHERE r.name = 'VIEWER';

-- Asset types
INSERT INTO asset_types (name, category) VALUES
    ('Generator',               'ENERGY'),
    ('Solar Panel Array',       'ENERGY'),
    ('Wind Turbine',            'ENERGY'),
    ('Battery Bank',            'ENERGY'),
    ('HVAC System',             'UTILITIES'),
    ('Water Treatment Plant',   'UTILITIES'),
    ('Boiler',                  'UTILITIES'),
    ('Fuel Tank',               'STORAGE'),
    ('Communication Equipment', 'COMMUNICATIONS'),
    ('Scientific Equipment',    'SCIENCE'),
    ('Vehicle',                 'TRANSPORT'),
    ('Backup Generator',        'ENERGY'),
    ('UPS System',              'ENERGY'),
    ('Water Storage Tank',      'STORAGE'),
    ('Weather Station',         'SCIENCE');

-- Sensor types
INSERT INTO sensor_types (name, default_unit, description) VALUES
    ('TEMPERATURE',     '°C',    'Ambient or surface temperature'),
    ('HUMIDITY',        '%',     'Relative humidity'),
    ('PRESSURE',        'hPa',   'Atmospheric or fluid pressure'),
    ('WIND_SPEED',      'm/s',   'Wind speed'),
    ('WIND_DIRECTION',  '°',     'Wind direction in degrees'),
    ('SOLAR_RADIATION', 'W/m²',  'Solar irradiance'),
    ('FUEL_LEVEL',      '%',     'Fuel tank level percentage'),
    ('WATER_LEVEL',     '%',     'Water tank level percentage'),
    ('POWER_OUTPUT',    'kW',    'Electrical power output'),
    ('BATTERY_SOC',     '%',     'Battery state of charge'),
    ('VOLTAGE',         'V',     'Electrical voltage'),
    ('CURRENT',         'A',     'Electrical current'),
    ('CO2_LEVEL',       'ppm',   'Carbon dioxide concentration'),
    ('NOISE_LEVEL',     'dB',    'Acoustic noise level'),
    ('FLOW_RATE',       'L/min', 'Liquid flow rate');

-- Stations
INSERT INTO stations (code, name, description, station_type, status, latitude, longitude, elevation_m, capacity, commissioned_at) VALUES
    ('MAT', 'Maitri',  'India''s second Antarctic research station located in Schirmacher Oasis', 'RESEARCH_STATION', 'ACTIVE', -70.7669, 11.7347, 130.0, 25, '1989-03-08'),
    ('BHA', 'Bharati', 'India''s third Antarctic research station on the Prydz Bay coast',        'RESEARCH_STATION', 'ACTIVE', -69.4065, 76.1921,  35.0, 47, '2012-03-18');

-- Inventory items
INSERT INTO inventory_items (name, category, unit) VALUES
    ('Diesel Fuel',           'FUEL',      'LITRE'),
    ('Aviation Fuel (ATF)',   'FUEL',      'LITRE'),
    ('Lubricating Oil',       'FUEL',      'LITRE'),
    ('Potable Water',         'UTILITIES', 'LITRE'),
    ('Food Rations (MRE)',    'FOOD',      'BOX'),
    ('Medical Supplies Kit',  'MEDICAL',   'BOX'),
    ('Spare Parts - General', 'EQUIPMENT', 'UNIT'),
    ('Batteries (AA)',        'EQUIPMENT', 'UNIT'),
    ('Propane Gas',           'FUEL',      'KILOGRAM'),
    ('Solar Panel (Spare)',   'EQUIPMENT', 'UNIT');

-- =============================================================================
-- SECTION 20: TELEMETRY RETENTION (pg_cron)
-- If pg_cron is unavailable on your Supabase plan, implement this as a
-- Supabase Edge Function triggered on a daily cron schedule instead.
-- =============================================================================

SELECT cron.schedule(
    'cleanup-telemetry-30d',
    '0 2 * * *',
    $$
        DELETE FROM energy_readings      WHERE time       < now() - INTERVAL '30 days';
        DELETE FROM environment_readings WHERE time       < now() - INTERVAL '30 days';
        DELETE FROM asset_readings       WHERE time       < now() - INTERVAL '30 days';
        DELETE FROM active_alerts        WHERE expires_at < now() AND status IN ('RESOLVED', 'EXPIRED');
    $$
);

-- =============================================================================
-- END OF MIGRATION 001
-- =============================================================================

COMMIT;
