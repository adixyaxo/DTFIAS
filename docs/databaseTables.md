## Table `profiles`

Application user profiles — 1:1 with auth.users. Supabase manages authentication; this table manages application identity.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `full_name` | `text` |  |
| `employee_code` | `text` |  Unique |
| `designation` | `text` |  Nullable |
| `organization` | `text` |  Nullable |
| `phone` | `text` |  Nullable |
| `status` | `profile_status` |  |
| `avatar_url` | `text` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `roles`

Application roles. Users are assigned one or more roles via user_roles.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `name` | `text` |  Unique |
| `description` | `text` |  Nullable |
| `created_at` | `timestamptz` |  |

## Table `permissions`

Fine-grained permission codes. Assigned to roles via role_permissions.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `code` | `text` |  Unique |
| `description` | `text` |  Nullable |

## Table `user_roles`

Many-to-many: a user can hold multiple roles.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `user_id` | `uuid` | Primary |
| `role_id` | `uuid` | Primary |
| `assigned_at` | `timestamptz` |  |
| `assigned_by` | `uuid` |  Nullable |

## Table `role_permissions`

Many-to-many: a role grants multiple permissions.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `role_id` | `uuid` | Primary |
| `permission_id` | `uuid` | Primary |

## Table `station_access`

Station-level access grants. Independent of role — a user can be HQ_OPERATOR but only see specific stations.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `user_id` | `uuid` |  |
| `station_id` | `uuid` |  |
| `access_level` | `access_level` |  |
| `granted_at` | `timestamptz` |  |
| `granted_by` | `uuid` |  Nullable |

## Table `stations`

One row per Antarctic station. New stations are data, not schema changes.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `code` | `text` |  Unique |
| `name` | `text` |  |
| `description` | `text` |  Nullable |
| `station_type` | `station_type` |  |
| `status` | `station_status` |  |
| `latitude` | `float8` |  Nullable |
| `longitude` | `float8` |  Nullable |
| `elevation_m` | `float8` |  Nullable |
| `capacity` | `int4` |  Nullable |
| `commissioned_at` | `date` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `station_areas`

Hierarchical areas within a station (e.g. Power System > Generator Room). Self-referential via parent_area_id.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `station_id` | `uuid` |  |
| `parent_area_id` | `uuid` |  Nullable |
| `name` | `text` |  |
| `area_type` | `text` |  Nullable |
| `description` | `text` |  Nullable |
| `created_at` | `timestamptz` |  |

## Table `personnel`

Personnel records. A person may not have a login account (profile_id nullable). Tracks all expedition members.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `profile_id` | `uuid` |  Nullable |
| `employee_code` | `text` |  Unique |
| `full_name` | `text` |  |
| `designation` | `text` |  Nullable |
| `organization` | `text` |  Nullable |
| `phone` | `text` |  Nullable |
| `email` | `text` |  Nullable |
| `status` | `profile_status` |  |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `station_assignments`

Each deployment of a person to a station. departure_date NULL means currently deployed.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `personnel_id` | `uuid` |  |
| `station_id` | `uuid` |  |
| `station_role` | `text` |  Nullable |
| `arrival_date` | `date` |  |
| `departure_date` | `date` |  Nullable |
| `status` | `assignment_status` |  |
| `notes` | `text` |  Nullable |
| `created_at` | `timestamptz` |  |

## Table `personnel_health_status`

Basic health status log — status and optional free-text condition only. No vitals. Access restricted by RBAC.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `personnel_id` | `uuid` |  |
| `station_id` | `uuid` |  |
| `status` | `health_status` |  |
| `condition` | `text` |  Nullable |
| `notes` | `text` |  Nullable |
| `recorded_at` | `timestamptz` |  |
| `recorded_by` | `uuid` |  Nullable |

## Table `asset_types`

Lookup table of asset categories (Generator, Solar Panel, HVAC, etc.).

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `name` | `text` |  Unique |
| `category` | `text` |  Nullable |
| `description` | `text` |  Nullable |

## Table `assets`

Physical equipment. Self-referential (parent_asset_id) for hierarchical assets like battery banks containing individual batteries.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `station_id` | `uuid` |  |
| `area_id` | `uuid` |  Nullable |
| `asset_type_id` | `uuid` |  |
| `parent_asset_id` | `uuid` |  Nullable |
| `asset_code` | `text` |  Unique |
| `name` | `text` |  |
| `manufacturer` | `text` |  Nullable |
| `model` | `text` |  Nullable |
| `serial_number` | `text` |  Nullable |
| `status` | `asset_status` |  |
| `criticality` | `asset_criticality` |  |
| `installation_date` | `date` |  Nullable |
| `commissioned_at` | `date` |  Nullable |
| `metadata` | `jsonb` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `asset_status_history`

Immutable audit trail of asset status transitions. Written by a trigger on assets.status update.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `asset_id` | `uuid` |  |
| `old_status` | `asset_status` |  Nullable |
| `new_status` | `asset_status` |  |
| `reason` | `text` |  Nullable |
| `changed_by` | `uuid` |  Nullable |
| `changed_at` | `timestamptz` |  |

## Table `sensor_types`

Lookup table of sensor categories (TEMPERATURE, FUEL_LEVEL, etc.).

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `name` | `text` |  Unique |
| `description` | `text` |  Nullable |
| `default_unit` | `text` |  Nullable |

## Table `sensors`

Physical sensor instances. Linked to an asset; belongs to a station.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `station_id` | `uuid` |  |
| `asset_id` | `uuid` |  Nullable |
| `sensor_type_id` | `uuid` |  |
| `sensor_code` | `text` |  Unique |
| `name` | `text` |  |
| `unit` | `text` |  |
| `status` | `sensor_status` |  |
| `last_reading_at` | `timestamptz` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `sensor_configurations`

Versioned sensor configuration. The latest effective_from record is the active config.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `sensor_id` | `uuid` |  |
| `sampling_interval_seconds` | `int4` |  |
| `min_threshold` | `float8` |  Nullable |
| `max_threshold` | `float8` |  Nullable |
| `calibration_offset` | `float8` |  Nullable |
| `effective_from` | `timestamptz` |  |
| `notes` | `text` |  Nullable |

## Table `energy_readings`

Time-series energy telemetry. 30-day retention policy.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `time` | `timestamptz` | Primary |
| `station_id` | `uuid` | Primary |
| `energy_asset_id` | `uuid` |  Nullable |
| `generation_kw` | `float8` |  Nullable |
| `consumption_kw` | `float8` |  Nullable |
| `battery_soc_pct` | `float8` |  Nullable |
| `voltage_v` | `float8` |  Nullable |
| `current_a` | `float8` |  Nullable |
| `fuel_consumption_lph` | `float8` |  Nullable |
| `quality` | `reading_quality` |  |

## Table `environment_readings`

Time-series operational weather telemetry. 30-day retention policy.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `time` | `timestamptz` | Primary |
| `station_id` | `uuid` | Primary |
| `temperature_c` | `float8` |  Nullable |
| `humidity_pct` | `float8` |  Nullable |
| `pressure_hpa` | `float8` |  Nullable |
| `wind_speed_mps` | `float8` |  Nullable |
| `wind_direction_deg` | `float8` |  Nullable |
| `solar_radiation_wm2` | `float8` |  Nullable |
| `quality` | `reading_quality` |  |

## Table `asset_readings`

Generic time-series for asset/sensor metrics. 30-day retention.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `time` | `timestamptz` | Primary |
| `asset_id` | `uuid` | Primary |
| `sensor_id` | `uuid` |  Nullable |
| `metric` | `text` | Primary |
| `value` | `float8` |  |
| `unit` | `text` |  Nullable |
| `quality` | `reading_quality` |  |

## Table `energy_systems`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `station_id` | `uuid` |  |
| `name` | `text` |  |
| `description` | `text` |  Nullable |
| `created_at` | `timestamptz` |  |

## Table `energy_sources`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `energy_system_id` | `uuid` |  |
| `source_type` | `energy_source_type` |  |
| `name` | `text` |  |
| `capacity_kw` | `float8` |  Nullable |
| `status` | `asset_status` |  |
| `created_at` | `timestamptz` |  |

## Table `energy_assets`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `energy_source_id` | `uuid` |  |
| `asset_id` | `uuid` |  |

## Table `scientific_observations`

Scientific environmental observations. PERMANENT — not subject to 30-day telemetry retention.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `station_id` | `uuid` |  |
| `observation_type` | `observation_type` |  |
| `observed_at` | `timestamptz` |  |
| `value` | `float8` |  Nullable |
| `text_value` | `text` |  Nullable |
| `unit` | `text` |  Nullable |
| `quality` | `reading_quality` |  |
| `source` | `text` |  Nullable |
| `metadata` | `jsonb` |  Nullable |
| `recorded_by` | `uuid` |  Nullable |
| `created_at` | `timestamptz` |  |

## Table `inventory_items`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `name` | `text` |  |
| `category` | `text` |  Nullable |
| `unit` | `inventory_unit` |  |
| `description` | `text` |  Nullable |
| `created_at` | `timestamptz` |  |

## Table `inventory`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `station_id` | `uuid` |  |
| `item_id` | `uuid` |  |
| `quantity` | `float8` |  |
| `minimum_threshold` | `float8` |  Nullable |
| `updated_at` | `timestamptz` |  |

## Table `shipments`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `origin` | `text` |  |
| `destination_station_id` | `uuid` |  |
| `status` | `shipment_status` |  |
| `dispatched_at` | `timestamptz` |  Nullable |
| `expected_at` | `timestamptz` |  Nullable |
| `delivered_at` | `timestamptz` |  Nullable |
| `notes` | `text` |  Nullable |
| `created_by` | `uuid` |  Nullable |
| `created_at` | `timestamptz` |  |

## Table `inventory_transactions`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `station_id` | `uuid` |  |
| `item_id` | `uuid` |  |
| `transaction_type` | `transaction_type` |  |
| `quantity_delta` | `float8` |  |
| `notes` | `text` |  Nullable |
| `transacted_by` | `uuid` |  Nullable |
| `transacted_at` | `timestamptz` |  |
| `shipment_id` | `uuid` |  Nullable |

## Table `shipment_items`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `shipment_id` | `uuid` |  |
| `item_id` | `uuid` |  |
| `quantity` | `float8` |  |

## Table `maintenance_records`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `asset_id` | `uuid` |  |
| `station_id` | `uuid` |  |
| `maintenance_type` | `maintenance_type` |  |
| `priority` | `maintenance_priority` |  |
| `status` | `maintenance_status` |  |
| `description` | `text` |  |
| `scheduled_at` | `timestamptz` |  Nullable |
| `started_at` | `timestamptz` |  Nullable |
| `completed_at` | `timestamptz` |  Nullable |
| `performed_by` | `uuid` |  Nullable |
| `created_by` | `uuid` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `maintenance_events`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `maintenance_id` | `uuid` |  |
| `event_type` | `text` |  |
| `description` | `text` |  |
| `recorded_by` | `uuid` |  Nullable |
| `recorded_at` | `timestamptz` |  |

## Table `commands`

Commands issued by HQ. Station validates and executes. HQ never directly modifies physical station state.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `station_id` | `uuid` |  |
| `created_by` | `uuid` |  |
| `command_type` | `command_type` |  |
| `parameters` | `jsonb` |  Nullable |
| `status` | `command_status` |  |
| `rejection_reason` | `text` |  Nullable |
| `created_at` | `timestamptz` |  |
| `expires_at` | `timestamptz` |  Nullable |
| `updated_at` | `timestamptz` |  |

## Table `command_executions`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `command_id` | `uuid` |  |
| `executed_by` | `uuid` |  Nullable |
| `result` | `text` |  Nullable |
| `result_metadata` | `jsonb` |  Nullable |
| `executed_at` | `timestamptz` |  |

## Table `alert_rules`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `station_id` | `uuid` |  |
| `name` | `text` |  |
| `description` | `text` |  Nullable |
| `severity` | `alert_severity` |  |
| `condition_expression` | `text` |  |
| `is_active` | `bool` |  |
| `created_by` | `uuid` |  Nullable |
| `created_at` | `timestamptz` |  |

## Table `active_alerts`

Live alerts only. Removed when resolved or expired — no permanent alert history.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `station_id` | `uuid` |  |
| `asset_id` | `uuid` |  Nullable |
| `sensor_id` | `uuid` |  Nullable |
| `alert_rule_id` | `uuid` |  Nullable |
| `severity` | `alert_severity` |  |
| `alert_type` | `text` |  |
| `message` | `text` |  |
| `status` | `alert_status` |  |
| `created_at` | `timestamptz` |  |
| `acknowledged_at` | `timestamptz` |  Nullable |
| `acknowledged_by` | `uuid` |  Nullable |
| `expires_at` | `timestamptz` |  Nullable |

## Table `audit_logs`

Immutable append-only audit trail. RLS prevents user UPDATE/DELETE.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `user_id` | `uuid` |  Nullable |
| `station_id` | `uuid` |  Nullable |
| `action` | `text` |  |
| `entity_type` | `text` |  |
| `entity_id` | `uuid` |  Nullable |
| `old_value` | `jsonb` |  Nullable |
| `new_value` | `jsonb` |  Nullable |
| `ip_address` | `inet` |  Nullable |
| `created_at` | `timestamptz` |  |

## Custom Types / Enums

### `access_level`

`READ` | `WRITE` | `ADMIN`

### `alert_severity`

`CRITICAL` | `HIGH` | `MEDIUM` | `LOW` | `INFO`

### `alert_status`

`ACTIVE` | `ACKNOWLEDGED` | `RESOLVED` | `EXPIRED`

### `asset_criticality`

`CRITICAL` | `HIGH` | `MEDIUM` | `LOW`

### `asset_status`

`OPERATIONAL` | `DEGRADED` | `UNDER_MAINTENANCE` | `DECOMMISSIONED` | `STANDBY`

### `assignment_status`

`ACTIVE` | `COMPLETED` | `CANCELLED`

### `command_status`

`PENDING` | `RECEIVED` | `VALIDATED` | `REJECTED` | `EXECUTING` | `EXECUTED` | `FAILED` | `EXPIRED`

### `command_type`

`SYSTEM_CONTROL` | `SENSOR_CONTROL` | `ENERGY_CONTROL` | `LOGISTICS_CONTROL` | `PERSONNEL_CONTROL` | `ALERT_CONTROL`

### `energy_source_type`

`DIESEL` | `SOLAR` | `WIND` | `BATTERY` | `HYBRID`

### `health_status`

`HEALTHY` | `ILL` | `INJURED` | `UNDER_OBSERVATION` | `MEDICAL_LEAVE` | `UNFIT`

### `inventory_unit`

`LITRE` | `KILOGRAM` | `UNIT` | `METRE` | `KILOWATT_HOUR` | `BOX` | `PALLET`

### `maintenance_priority`

`CRITICAL` | `HIGH` | `MEDIUM` | `LOW`

### `maintenance_status`

`SCHEDULED` | `IN_PROGRESS` | `COMPLETED` | `CANCELLED` | `DEFERRED`

### `maintenance_type`

`INSPECTION` | `PREVENTIVE` | `CORRECTIVE` | `EMERGENCY` | `CALIBRATION` | `UPGRADE`

### `observation_type`

`AIR_TEMPERATURE` | `SNOW_OBSERVATION` | `ICE_OBSERVATION` | `ATMOSPHERIC_PRESSURE` | `WIND_OBSERVATION` | `PRECIPITATION` | `VISIBILITY` | `UV_INDEX` | `SEA_ICE_EXTENT`

### `profile_status`

`ACTIVE` | `INACTIVE` | `SUSPENDED`

### `reading_quality`

`GOOD` | `UNCERTAIN` | `BAD` | `MISSING`

### `sensor_status`

`ACTIVE` | `INACTIVE` | `FAULTY` | `CALIBRATING`

### `shipment_status`

`PLANNED` | `DISPATCHED` | `IN_TRANSIT` | `DELIVERED` | `CANCELLED`

### `station_status`

`ACTIVE` | `INACTIVE` | `UNDER_MAINTENANCE` | `DECOMMISSIONED`

### `station_type`

`RESEARCH_STATION` | `SUMMER_CAMP` | `FIELD_BASE` | `RELAY_STATION`

### `transaction_type`

`RECEIVED` | `CONSUMED` | `TRANSFERRED` | `ADJUSTED` | `DISPOSED`

## RLS Policies

### `profiles`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `profiles_read` | SELECT | public | PERMISSIVE | `((id = auth.uid()) OR user_has_permission('personnel.read'::text))` | — |
| `profiles_update` | UPDATE | public | PERMISSIVE | `(id = auth.uid())` | — |
| `profiles_insert` | INSERT | public | PERMISSIVE | — | `user_has_permission('personnel.manage'::text)` |

### `roles`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `roles_read` | SELECT | public | PERMISSIVE | `(auth.uid() IS NOT NULL)` | — |

### `permissions`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `permissions_read` | SELECT | public | PERMISSIVE | `(auth.uid() IS NOT NULL)` | — |

### `role_permissions`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `role_perm_manage` | ALL | public | PERMISSIVE | `user_has_permission('station.manage'::text)` | — |

### `station_access`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `station_access_read` | SELECT | public | PERMISSIVE | `((user_id = auth.uid()) OR user_has_permission('station.manage'::text))` | — |
| `station_access_manage` | ALL | public | PERMISSIVE | `user_has_permission('station.manage'::text)` | — |

### `stations`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `stations_read` | SELECT | public | PERMISSIVE | `((id IN ( SELECT station_access.station_id    FROM station_access   WHERE (station_access.user_id = auth.uid()))) OR user_has_permission('station.manage'::text))` | — |
| `stations_manage` | ALL | public | PERMISSIVE | `user_has_permission('station.manage'::text)` | — |

### `station_areas`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `areas_read` | SELECT | public | PERMISSIVE | `user_has_station_access(station_id)` | — |
| `areas_manage` | ALL | public | PERMISSIVE | `user_has_permission('station.manage'::text)` | — |

### `assets`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `assets_read` | SELECT | public | PERMISSIVE | `(user_has_station_access(station_id) AND user_has_permission('asset.read'::text))` | — |
| `assets_manage` | ALL | public | PERMISSIVE | `(user_has_station_access(station_id) AND user_has_permission('asset.manage'::text))` | — |

### `asset_status_history`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `asset_hist_read` | SELECT | public | PERMISSIVE | `((asset_id IN ( SELECT assets.id    FROM assets   WHERE user_has_station_access(assets.station_id))) AND user_has_permission('asset.read'::text))` | — |

### `asset_types`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `asset_types_read` | SELECT | public | PERMISSIVE | `(auth.uid() IS NOT NULL)` | — |

### `sensor_types`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `sensor_types_read` | SELECT | public | PERMISSIVE | `(auth.uid() IS NOT NULL)` | — |

### `personnel`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `personnel_read` | SELECT | public | PERMISSIVE | `user_has_permission('personnel.read'::text)` | — |
| `personnel_manage` | ALL | public | PERMISSIVE | `user_has_permission('personnel.manage'::text)` | — |

### `station_assignments`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `assignments_read` | SELECT | public | PERMISSIVE | `(user_has_station_access(station_id) AND user_has_permission('personnel.read'::text))` | — |
| `assignments_manage` | ALL | public | PERMISSIVE | `user_has_permission('personnel.manage'::text)` | — |

### `personnel_health_status`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `health_read` | SELECT | public | PERMISSIVE | `user_has_permission('health.read'::text)` | — |
| `health_manage` | ALL | public | PERMISSIVE | `user_has_permission('health.manage'::text)` | — |

### `shipment_items`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `shipment_items_manage` | ALL | public | PERMISSIVE | `user_has_permission('logistics.manage'::text)` | — |
| `shipment_items_read` | SELECT | public | PERMISSIVE | `user_has_permission('logistics.read'::text)` | — |

### `sensors`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `sensors_read` | SELECT | public | PERMISSIVE | `(user_has_station_access(station_id) AND user_has_permission('telemetry.read'::text))` | — |
| `sensors_manage` | ALL | public | PERMISSIVE | `user_has_permission('asset.manage'::text)` | — |

### `sensor_configurations`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `sensor_cfg_read` | SELECT | public | PERMISSIVE | `user_has_permission('telemetry.read'::text)` | — |
| `sensor_cfg_manage` | ALL | public | PERMISSIVE | `user_has_permission('asset.manage'::text)` | — |

### `energy_readings`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `energy_read` | SELECT | public | PERMISSIVE | `(user_has_station_access(station_id) AND user_has_permission('energy.read'::text))` | — |
| `energy_insert` | INSERT | public | PERMISSIVE | — | `user_has_station_access(station_id)` |

### `environment_readings`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `env_read` | SELECT | public | PERMISSIVE | `(user_has_station_access(station_id) AND user_has_permission('telemetry.read'::text))` | — |
| `env_insert` | INSERT | public | PERMISSIVE | — | `user_has_station_access(station_id)` |

### `asset_readings`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `asset_rdg_read` | SELECT | public | PERMISSIVE | `((asset_id IN ( SELECT assets.id    FROM assets   WHERE user_has_station_access(assets.station_id))) AND user_has_permission('telemetry.read'::text))` | — |
| `asset_rdg_insert` | INSERT | public | PERMISSIVE | — | `(asset_id IN ( SELECT assets.id    FROM assets   WHERE user_has_station_access(assets.station_id)))` |

### `energy_systems`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `energy_sys_read` | SELECT | public | PERMISSIVE | `(user_has_station_access(station_id) AND user_has_permission('energy.read'::text))` | — |
| `energy_sys_manage` | ALL | public | PERMISSIVE | `user_has_permission('energy.manage'::text)` | — |

### `energy_sources`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `energy_src_read` | SELECT | public | PERMISSIVE | `user_has_permission('energy.read'::text)` | — |
| `energy_src_manage` | ALL | public | PERMISSIVE | `user_has_permission('energy.manage'::text)` | — |

### `energy_assets`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `energy_assets_read` | SELECT | public | PERMISSIVE | `user_has_permission('energy.read'::text)` | — |
| `energy_assets_manage` | ALL | public | PERMISSIVE | `user_has_permission('energy.manage'::text)` | — |

### `inventory_items`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `inv_items_read` | SELECT | public | PERMISSIVE | `(auth.uid() IS NOT NULL)` | — |

### `inventory`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `inv_read` | SELECT | public | PERMISSIVE | `(user_has_station_access(station_id) AND user_has_permission('logistics.read'::text))` | — |
| `inv_manage` | ALL | public | PERMISSIVE | `user_has_permission('logistics.manage'::text)` | — |

### `inventory_transactions`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `inv_tx_read` | SELECT | public | PERMISSIVE | `(user_has_station_access(station_id) AND user_has_permission('logistics.read'::text))` | — |
| `inv_tx_insert` | INSERT | public | PERMISSIVE | — | `user_has_permission('logistics.manage'::text)` |

### `shipments`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `shipments_read` | SELECT | public | PERMISSIVE | `(user_has_station_access(destination_station_id) AND user_has_permission('logistics.read'::text))` | — |
| `shipments_manage` | ALL | public | PERMISSIVE | `user_has_permission('logistics.manage'::text)` | — |

### `maintenance_records`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `maint_read` | SELECT | public | PERMISSIVE | `(user_has_station_access(station_id) AND user_has_permission('maintenance.read'::text))` | — |
| `maint_manage` | ALL | public | PERMISSIVE | `user_has_permission('maintenance.manage'::text)` | — |

### `maintenance_events`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `maint_evt_read` | SELECT | public | PERMISSIVE | `user_has_permission('maintenance.read'::text)` | — |
| `maint_evt_manage` | ALL | public | PERMISSIVE | `user_has_permission('maintenance.manage'::text)` | — |

### `commands`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `cmd_create` | INSERT | public | PERMISSIVE | — | `user_has_permission('command.create'::text)` |
| `cmd_read` | SELECT | public | PERMISSIVE | `user_has_station_access(station_id)` | — |
| `cmd_update` | UPDATE | public | PERMISSIVE | `(user_has_station_access(station_id) AND user_has_permission('command.execute'::text))` | — |

### `command_executions`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `cmd_exec_insert` | INSERT | public | PERMISSIVE | — | `user_has_permission('command.execute'::text)` |
| `cmd_exec_read` | SELECT | public | PERMISSIVE | `(command_id IN ( SELECT commands.id    FROM commands   WHERE user_has_station_access(commands.station_id)))` | — |

### `alert_rules`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `alert_rules_read` | SELECT | public | PERMISSIVE | `(user_has_station_access(station_id) AND user_has_permission('alert.read'::text))` | — |
| `alert_rules_manage` | ALL | public | PERMISSIVE | `user_has_permission('alert.manage'::text)` | — |

### `active_alerts`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `alerts_read` | SELECT | public | PERMISSIVE | `(user_has_station_access(station_id) AND user_has_permission('alert.read'::text))` | — |
| `alerts_manage` | ALL | public | PERMISSIVE | `user_has_permission('alert.manage'::text)` | — |

### `audit_logs`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `audit_read` | SELECT | public | PERMISSIVE | `user_has_permission('audit.read'::text)` | — |
| `audit_insert` | INSERT | public | PERMISSIVE | — | `true` |

### `scientific_observations`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `sci_obs_read` | SELECT | public | PERMISSIVE | `(user_has_station_access(station_id) AND user_has_permission('telemetry.read'::text))` | — |
| `sci_obs_insert` | INSERT | public | PERMISSIVE | — | `user_has_station_access(station_id)` |

