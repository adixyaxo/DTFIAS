# Original User Request

## 2026-09-11T17:01:57Z

<USER_REQUEST>
Build a complete, pure Three.js 3D model of the Bharati Research Station based on the existing architectural research and implementation plan, ensuring it is ready for telemetry integration.

Working directory: `C:\Users\adity\Documents\Coding\Projects\DTFIAS`
Integrity mode: benchmark

## Requirements

### R1. Core Structure
Build the main aerodynamic aluminum shell using extruded geometries, the elevated stilt grid with cross-bracing, and the emissive North panoramic window. Do not model individual interior containers.

### R2. External Assets & Infrastructure
Model the 300,000L cylindrical fuel farm, roof HVAC arrays, SATCOM radomes, and the 15m radius heliport situated 50m away from the main building.

### R3. Environment & Effects
Generate a displaced plane for the rocky Larsemann Hills terrain and a horizontal particle system to simulate the Antarctic blizzard blowing underneath the station.

### R4. Assembly & Telemetry Integration
Assemble all components into a cohesive scene and overwrite the existing `app/static/js/three/station_3d_view.js` file with the final implementation. Group the specific interactive geometries and assign them precise names (`hotspot-main_building`, `hotspot-fuel_storage`, `hotspot-comms_satcom`, `hotspot-hvac`, `hotspot-heliport`, `hotspot-environment_sensors`) so the frontend raycaster can hook into them.

## Acceptance Criteria

### Automated Verification
- [ ] A test HTML file must be generated to load the 3D scene independently.
- [ ] The scene must load in the test HTML file without any WebGL console errors.
- [ ] An automated script (e.g., parsing the AST or running a headless browser test) must successfully verify that all required `hotspot-*` IDs are present in the final generated JavaScript code.
</USER_REQUEST>
