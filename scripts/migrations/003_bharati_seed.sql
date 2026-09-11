-- 003_bharati_seed.sql
-- Injects verified numerical data for Bharati Station into the database

BEGIN;

-- 1. Update Bharati Station metadata
UPDATE stations
SET 
    capacity = 72,
    elevation_m = 35.0,
    latitude = -69.4068, -- 69°24.41' S
    longitude = 76.1953 -- 76°11.72' E
WHERE code = 'BHA';

-- 2. Ensure Required Asset Types Exist
INSERT INTO asset_types (name, category, description)
VALUES 
    ('CHP Generator', 'ENERGY', 'Combined Heat and Power Generator'),
    ('Jet A-1 Fuel Tank', 'STORAGE', 'Insulated fuel storage tank'),
    ('Seawater Pipeline', 'UTILITIES', 'Electrically trace-heated seawater intake'),
    ('Desalination Plant', 'UTILITIES', 'Reverse osmosis desalination facility')
ON CONFLICT (name) DO NOTHING;

-- 3. Ensure Required Sensor Types Exist
INSERT INTO sensor_types (name, default_unit, description)
VALUES 
    ('TRACE_HEATER_CURRENT', 'A', 'Current drawn by trace heating cables'),
    ('TRACE_HEATER_RESISTANCE', 'Ohms', 'Electrical resistance of trace heating'),
    ('SMOKE_DETECTOR', 'State', 'Smoke detection status (0/1)'),
    ('SECURITY_CAMERA', 'State', 'Camera operational state (0/1)'),
    ('BMS_DATA_POINT', 'Mixed', 'General Building Management System data point')
ON CONFLICT (name) DO NOTHING;

-- We need the UUIDs to insert foreign keys
DO $$
DECLARE
    bharati_id UUID;
    chp_type_id UUID;
    tank_type_id UUID;
    pipe_type_id UUID;
    desal_type_id UUID;
    sys_energy_id UUID;
    src_chp_id UUID;
BEGIN
    SELECT id INTO bharati_id FROM stations WHERE code = 'BHA';
    
    SELECT id INTO chp_type_id FROM asset_types WHERE name = 'CHP Generator';
    SELECT id INTO tank_type_id FROM asset_types WHERE name = 'Jet A-1 Fuel Tank';
    SELECT id INTO pipe_type_id FROM asset_types WHERE name = 'Seawater Pipeline';
    SELECT id INTO desal_type_id FROM asset_types WHERE name = 'Desalination Plant';

    -- 4. Create Energy System and Source
    INSERT INTO energy_systems (station_id, name, description)
    VALUES (bharati_id, 'Bharati Primary Power System', '3x 100kVA CHP MAN Generators')
    RETURNING id INTO sys_energy_id;

    INSERT INTO energy_sources (energy_system_id, source_type, name, capacity_kw)
    VALUES (sys_energy_id, 'DIESEL', 'MAN CHP Plant', 300)
    RETURNING id INTO src_chp_id;

    -- 5. Insert 3x CHP Generators
    FOR i IN 1..3 LOOP
        WITH inserted_asset AS (
            INSERT INTO assets (station_id, asset_type_id, asset_code, name, manufacturer, model, status, criticality, metadata)
            VALUES (
                bharati_id, 
                chp_type_id, 
                'BHA-CHP-0' || i, 
                'CHP Generator ' || i, 
                'MAN', 
                '100kVA', 
                'OPERATIONAL', 
                'CRITICAL',
                '{"rated_power_kva": 100, "thermal_output_kw": 51.6}'::jsonb
            ) RETURNING id
        )
        INSERT INTO energy_assets (energy_source_id, asset_id)
        SELECT src_chp_id, id FROM inserted_asset;
    END LOOP;

    -- 6. Insert 13x Jet A-1 Fuel Tanks
    FOR i IN 1..13 LOOP
        INSERT INTO assets (station_id, asset_type_id, asset_code, name, status, criticality, metadata)
        VALUES (
            bharati_id, 
            tank_type_id, 
            'BHA-FUEL-TK-' || LPAD(i::text, 2, '0'), 
            'Jet A-1 Bulk Tank ' || i, 
            'OPERATIONAL', 
            'HIGH',
            '{"capacity_kl": 24, "fuel_type": "Jet A-1"}'::jsonb
        );
    END LOOP;

    -- 7. Insert Critical Water Infrastructure
    INSERT INTO assets (station_id, asset_type_id, asset_code, name, status, criticality, metadata)
    VALUES (
        bharati_id, 
        pipe_type_id, 
        'BHA-WTR-PIPE-01', 
        'Quilty Bay Intake Pipeline', 
        'OPERATIONAL', 
        'CRITICAL',
        '{"length_m": 300, "depth_m": 12, "trace_heated": true}'::jsonb
    );

    INSERT INTO assets (station_id, asset_type_id, asset_code, name, status, criticality)
    VALUES (
        bharati_id, 
        desal_type_id, 
        'BHA-WTR-RO-01', 
        'Main RO Desalination Plant', 
        'OPERATIONAL', 
        'CRITICAL'
    );

END $$;

COMMIT;
