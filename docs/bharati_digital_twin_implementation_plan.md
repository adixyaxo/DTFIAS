# Bharati Station Digital Twin Implementation Plan

## 1. Executive Summary & Context

The initial phase of the DTFIAS project successfully established the database connection, authentication, and core infrastructure. The current goal is to accurately configure the Digital Twin application specifically for the **Bharati Research Station**, utilizing the newly extracted, verified numerical and technical dataset (`docs/data/`).

This implementation plan details the step-by-step phases required to update the **Project Information**, **Backend/Database**, and **Frontend** to accurately reflect Bharati's exact physical and technical properties, establishing a high-fidelity digital twin.

---

## 2. Phase 1: Project Information & Documentation Updates

Before code implementation, the project's documentation must reflect the verified Bharati statistics.

1. **Update `docs/station-facts-and-research.md`:**
   - **Coordinates:** `69°24.41′ S; 76°11.72′ E`
   - **Elevation:** `~35 m above mean sea level`
   - **Area:** `~2 km²` operational area; `2162 m²` main building floor area.
   - **Building Structure:** 134 prefabricated containers, 401.551 tonnes, 83 GEWI piles.
   - **Capacity:** Summer capacity `72` (47 in main building, 25 in emergency shelters). Winter capacity `~24`.
   - **Power Infrastructure:** 3 × 100 kVA CHP generators (MAN make), total capacity 300 kVA.
   - **Fuel Infrastructure:** Jet A-1 fuel farm capacity `296 kL` (~300 kL / 13 tanks of ~24 kL).
   - **Sensors/Automation:** ~1000 BMS data points, ~180 field devices, ~230 smoke detectors, 15 security cameras.
   - **Water Supply:** Seawater intake from Quilty Bay (~12 m depth), pumped through a ~300 m electrically trace-heated pipeline.

---

## 3. Phase 2: Database and Backend Engine Updates

The backend requires strict alignment with the specific architectural parameters of Bharati.

### 3.1. Seed Data Alignment (`scripts/migrations/`)
- Update `001_initial_schema.sql` (or create `003_bharati_seed.sql`) to inject the correct asset IDs:
  - Add exactly `3` CHP generators (`100 kVA` each) into the `energy_assets` table.
  - Add exactly `13` Jet A-1 fuel tanks (`24 kL` each) into the `assets` or `energy_sources` table.
  - Register the `seawater_intake_pipeline` and `desalination_plant` as critical assets.
  - Define `230` smoke detectors and `15` security cameras in the `sensors` table.

### 3.2. Proposed Digital Platform Implementations (`engine/services/`)
We must implement the algorithmic foundation for the ML/predictive maintenance features outlined in the technical notes.
1. **Seawater Intake Predictive Maintenance (`engine/services/core/water_service.py`):**
   - Create logic to monitor `trace_heater_current`, `trace_heater_resistance`, and `pipeline_temperature`.
   - Implement an anomaly detection rule: if resistance drops or temperature approaches freezing despite current flow, generate a `HIGH` priority alert.
2. **Generator Predictive Maintenance (`engine/services/core/energy_service.py`):**
   - Monitor `rpm`, `oil_pressure`, `exhaust_temperature`, and `operating_hours`.
   - Track major maintenance milestones (10,000 / 20,000 / 40,000 hours).
3. **HVAC Optimization (`engine/services/core/environment_service.py`):**
   - Correlate `indoor_co2` with `fresh_air_intake` and `heating_demand` to optimize Jet A-1 consumption.
4. **Fuel Burn-Rate Modeling (`engine/services/core/logistics_service.py`):**
   - Calculate daily consumption of Jet A-1 and Polar Diesel.
   - Project remaining operational days based on current 296 kL farm capacity and predict the next resupply requirement window (transfer happens every 8-10 days from the main farm to the day tank).

### 3.3. Security & RBAC Enforcements
- Define the explicit roles from the documentation into the `roles` table: `Scientist`, `Engineer`, `Medical Staff`, `Administrator`, `Station Commander`, `Remote NCPOR Operator`.
- Enforce the C7 Audit Log constraint explicitly when roles issue critical manual overrides on automated systems.

---

## 4. Phase 3: Frontend Interface Updates

The frontend must visually represent Bharati's unique infrastructure and fulfill the offline-first/cognitive load requirements.

### 4.1. Dashboard UI Redesign (`app/templates/bharati/`)
- **Digital UI Requirements Checklist:**
  - Simple navigation, High contrast, Clear icons.
  - Minimal steps, prominent critical alarms, low cognitive load (specifically designed to combat winter isolation cognitive fatigue).
- **Offline-First Indicators:** Implement visual cues in the top navigation bar when edge-computing is running autonomously due to satellite communication loss.

### 4.2. The 2.5D Station Twin (`app/static/js/three/station_3d_view.js` and SVGs)
- Map the Bharati 134-container layout (30m x 53.2m).
- Render 3 specific levels:
  - **Level 1 (Ground):** Labs, cold storage, electrical infrastructure.
  - **Level 2 (First Floor):** 24 bedrooms, kitchen, dining, library, fitness, medical operating theatre.
  - **Level 3 (Terrace):** Local HVAC, scientific experiments.
- **Specific Hotspots (SVG Overlays):**
  - `hotspot-chp-generators` (3 units)
  - `hotspot-fuel-farm` (13 tanks)
  - `hotspot-seawater-intake` (~300m pipeline towards Quilty Bay)
  - `hotspot-ageos` (ISRO S/X band satellite ground station)
  - `hotspot-helipad` (Main 900 m² helipad)

### 4.3. High-Priority Alert Monitoring
Ensure the frontend specifically prioritizes rendering real-time alarms for the highest-priority systems:
1. Seawater trace heating (Water supply failure risk).
2. CHP generators (Predictive maintenance).
3. Fuel tanks (Remaining days prediction).
4. HVAC (Energy optimization).
5. Fire/water-leak detection.

---

## 5. Execution Strategy

We will tackle this implementation phase by phase:
- **Phase A:** Seed the database with the verified Bharati numerical data to ensure all backend telemetry services have accurate entities to reference.
- **Phase B:** Implement the predictive maintenance business logic in the `engine/` layer (strictly adhering to Constraint C1).
- **Phase C:** Update the Jinja2 templates and the 2.5D SVG/Three.js twin to visualize these systems in real-time.
