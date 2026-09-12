# Plan — Bharati 3D Model Orchestration

## Objective
Build a complete, pure Three.js 3D model of the Bharati Research Station based on existing architectural research and plan, ensuring it is ready for telemetry integration with automated verification.

## Phases
1. **Phase 0: Survey**
   - Spawn 3 Explorers:
     - Explorer 1: Inspect existing 3D files (`app/static/js/three/station_3d_view.js`, static assets, templates, vendor Three.js scripts).
     - Explorer 2: Inspect documentation (`docs/architecture.md`, `docs/2dFrontend.md`, `GEMINI.md`, etc.) for architectural research and specs for Bharati station.
     - Explorer 3: Inspect frontend integration points (raycasting, telemetry hooks, hotspots, Alpine.js / HTMX wiring) and headless testing environment.
   - Merge findings into `PROJECT.md § Feature Inventory` and architecture.

2. **Phase 1: Test Infrastructure & Verification Harness**
   - Test harness to verify:
     - Presence and AST structure of all required hotspot IDs (`hotspot-main_building`, `hotspot-fuel_storage`, `hotspot-comms_satcom`, `hotspot-hvac`, `hotspot-heliport`, `hotspot-environment_sensors`).
     - Test HTML file to load Three.js scene independently.
     - WebGL / console error checks.

3. **Phase 2: Implementation (Worker)**
   - Implement `app/static/js/three/station_3d_view.js`:
     - R1: Core structure (extruded aluminum shell, elevated stilt grid with cross-bracing, emissive North panoramic window).
     - R2: External assets (300kL cylindrical fuel farm, roof HVAC arrays, SATCOM radomes, 15m heliport 50m away).
     - R3: Environment & effects (displaced Larsemann Hills terrain, blizzard particle system).
     - R4: Grouping, naming of interactive geometries for raycaster/telemetry, standalone test HTML page.

4. **Phase 3: Multi-Agent Verification**
   - Reviewers (2)
   - Challengers (2)
   - Forensic Auditor (1)
   - Gate verification.

5. **Phase 4: Synthesis & Final Reporting**
   - Completion report to parent via `send_message`.
