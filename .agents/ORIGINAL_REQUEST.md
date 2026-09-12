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

## 2026-09-12T05:00:34Z

<USER_REQUEST>
# Teamwork Project Prompt — Draft

> Status: Ready for launch — awaiting user approval.
> Goal: Craft prompt → get user approval → delegate to teamwork_preview
> Requested team: Full team

Implement the Bharati 3D Digital Twin by executing the multi-agent implementation plan defined in `docs/bharati3d/06-subagent_implementation_plan.md` based on the architectural synthesis in `docs/bharati3d/05-subagent_synthesis.md`. The deliverable is a complete, performance-optimized Three.js module at `app/static/js/three/station_3d_view.js` featuring accurate geometry, MEP SCADA overlays, raycasted hotspots, and interactive modes. 

Working directory: c:\Users\adity\Documents\Coding\Projects\DTFIAS
Integrity mode: benchmark

## Requirements

### R1. Implement Core Station Geometry and Site Assets
Construct the main station hull (extruded P1-P11 profile), the V-stilt quad foundations, the container core, and all site assets (SATCOM radome, helipad, fuel tanks, terrain) exactly as specified in the docs. The objects must be organized in the scene graph with proper `hotspot-` prefixed names.

### R2. Implement MEP Overlays and Multi-Mode Rendering
Implement the 7 distinct rendering modes (exterior, xray, core_only, hvac, thermal, structural, night). The modes must toggle the visibility and opacity of the exterior skin, container core, and specific interior/MEP layers. Provide the `window.set3DMode` global bridge.

### R3. Raycasting and Hotspot Interaction
Implement raycasting against the 21 defined hotspots. The scene must emit the `st-3d-click` CustomEvent containing the asset slug when a hotspot is clicked. Provide the `window.update3DHotspot(assetId, status)` bridge to update material colors based on status (critical/warning/normal).

### R4. Performance Guard and Animation Loop
Implement an animation loop that updates blizzard particles and subtly floats the station. The total scene geometry must stay within the 20,000 triangle budget, enforced by a `checkGeometryBudget` function that logs warnings if exceeded.

## Acceptance Criteria

### Programmatic Scene Graph Verification
- [ ] A headless Puppeteer script loads the application (or a test harness) and verifies that `window.station3DScene.scene` contains the complete hierarchy (Substructure_Stilts, Exterior_Aerodynamic_Shell, Modular_Container_Core, MEP_Life_Support_Overlay, Auxiliary_Site_Infrastructure).
- [ ] A script verifies that all 21 hotspots from the `HOTSPOT_REGISTRY` exist in the scene graph as objects with names starting with `hotspot-`.

### Programmatic Interaction & State Verification
- [ ] A script invokes `window.set3DMode('xray')` and verifies that the `outerSkin` material opacity is reduced and `containerCore` becomes visible.
- [ ] A script invokes `window.update3DHotspot('power-plant', 'critical')` and verifies that the corresponding mesh material's emissive color changes to the specified critical hex value.
- [ ] A script dispatches a simulated pointer click on the canvas at a hotspot's calculated screen coordinates and verifies that the `st-3d-click` CustomEvent is fired on the `window` object.
## 2026-09-12T06:12:14Z

<USER_REQUEST>
# Teamwork Project Prompt — Draft

> Status: Step 9 — Ready for launch — awaiting user approval
> Goal: Craft prompt → get user approval → delegate to teamwork_preview
> Requested team: Full team

Refine the Bharati 3D Digital Twin visualization in `app/static/js/three/station_3d_view.js` to improve realism, fix placement bugs, and remove unwanted animations.

Working directory: c:\Users\adity\Documents\Coding\Projects\DTFIAS
Integrity mode: benchmark

## Requirements

### R1. Ground and Terrain Enhancements
- Expand the ground/land area significantly so that the background void is no longer visible around the edges of the station.
- Apply a mildly realistic grass/tundra ground texture or material to the terrain instead of a plain color.

### R2. Placement Fixes (Anchor Floating Objects)
- Fix the helipad so it is firmly anchored to the ground, eliminating any floating appearance.
- Fix the flag poles and flags so they are correctly grounded/attached and not floating in the air.

### R3. Remove Unwanted Animations
- The main building currently bobs up and down (floating animation). Remove this animation entirely; all architectural structures must remain static and firmly planted.

### R4. Color Scheme and Aesthetics
- Adjust the color scheme of the environment and assets to better match a realistic (but stylized) Antarctic/tundra research station vibe, ensuring good contrast and visual appeal.

## Acceptance Criteria

### Programmatic Verification
- [ ] A headless Puppeteer script verifies that the main station group's `position.y` remains strictly constant over multiple frames (no floating/bobbing animation).
- [ ] A script verifies that the ground/terrain mesh has been scaled up significantly (e.g., width/depth > 200) to cover the void.
- [ ] A script verifies that the helipad and flag geometries have their base Y-coordinates correctly aligned with the ground elevation.
- [ ] The scene geometry must remain within the 20,000 triangle performance budget, verified by the `checkGeometryBudget` function.
</USER_REQUEST>
