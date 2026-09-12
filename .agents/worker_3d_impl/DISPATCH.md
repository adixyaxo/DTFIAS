## 2026-09-12T05:10:00Z

### Role
Three.js 3D Implementation Worker (`worker_3d_impl`)

### Working Directory
`c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\worker_3d_impl`

### Exclusive Write Ownership
- `app/static/js/three/station_3d_view.js`
- `app/static/js/station_twin.js` (only for adding OrbitControls script tag if needed)

### Mandatory Inputs to Read
1. `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\ORIGINAL_REQUEST.md`
2. `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\orchestrator_2\PROJECT.md`
3. `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\explorer_survey_2\handoff.md` (authoritative CAD datums, vertices, geometries, 21 hotspots, 7 modes)
4. `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\explorer_survey_1\handoff.md` (frontend assets and OrbitControls loader findings)
5. `docs/bharati3d/06-subagent_implementation_plan.md`
6. `docs/bharati3d/05-subagent_synthesis.md`
7. `GEMINI.md` (C13, C14, C16, C17)

### Task Description
Implement the complete, production-ready, performance-optimized Three.js module at `app/static/js/three/station_3d_view.js` adhering strictly to the architecture:

1. **Scene Bootstrap & Controls (Agent 1 scope)**:
   - `window.initStation3D(containerId)` entry point.
   - `THREE.WebGLRenderer({ antialias: true, alpha: true })`, pixel ratio capped at 2, ACESFilmicToneMapping, exposure 1.2, PCFSoftShadowMap.
   - `THREE.PerspectiveCamera(45, w/h, 1, 2000)` at `(120, 90, 160)`.
   - OrbitControls check: `if (typeof THREE.OrbitControls !== 'undefined')` with damping 0.05, maxPolarAngle `Math.PI/2 - 0.05`, target `(0, 6, 0)`.
   - Brand Lighting: Ambient `#1A312C` (intensity 2.0), Main Sun `#7DBFAD` (1.5) at `[50, 100, 50]`, Back fill `#428475` (1.0) at `[-50, 50, -50]`, Fog `#0B1C18` density 0.004.
   - Night mode lighting helper for aurora and moonlight.

2. **Material Library (Agent 2.1 scope)**:
   - Shared materials stored in `window._bm`: `hull` (`0xBAC4C7`), `roof` (`0x4F6D7A`), `keel` (`0x8E9EA4`), `glazingDay` (`0x1A312C`, transmission 0.85), `winWarm` (`0xFFAE33`, emissive `0xFF9900`), `winLab` (`0xE6F2FF`), `vstilt` (`0xB0BFC5`), `stairs` (`0xCFD8DC`), `concrete` (`0x6D6B66`), `ctnGreen` (`0x5C9E68`), `ctnWhite` (`0xDCE4E4`), `ctnOrange` (`0xC85A32`), etc.

3. **Substructure & Main Station Geometry (Agent 2 scope)**:
   - **Canonical Groups in Scene Hierarchy**:
     - `Substructure_Stilts`: Quad V-stilts group (`hotspot-v-stilts`) with 4 bents (outer port `[18.5, 1.05, 8.75]`, outer starboard `[18.5, 1.05, -8.75]`, inner port `[14.0, 1.05, 4.80]`, inner starboard `[14.0, 1.05, -4.80]`, 22° incline) + 28 vertical stilts grid (`InstancedMesh`, diameter 0.4, height varying) + 28 concrete footing pads at Y=0 + knee bracing.
     - `Exterior_Aerodynamic_Shell`: Extruded hull geometry using exact transverse profile P1–P11 from CAD blueprint 17 (P1 [0, 2.60], P2 [-7.5, 3.40], P3 [-10, 5.10], P4 [-9.5, 8.95], P5 [-5, 10.10], P6 [-3.8, 11.58], P7 [3.8, 11.58], P8 [5, 10.10], P9 [9.5, 8.95], P10 [10, 5.10], P11 [7.5, 3.40]) extruded 50.0m along X (x = -25 to +25). Recessed ribbon window cutout Y=7.8 to 9.0. Group named `hotspot-main-hab`.
     - 6-bay panoramic prow glazing (15° negative rake, 5 vertical mullions at Z = -4, -2, 0, 2, 4) at x=+24 prow tip.
     - Level 2 Penthouse at `[0, 10.34, 0]`, perimeter railing, 3 exhaust flues.
     - Access stairs (2x symmetrical 13-step flights at `[18, 2.3, ±9.5]`, rise 0.18, tread 0.28, slope 32.7°).
     - 4x 45° corner chamfer bevels.
     - Modular Container Core (`Modular_Container_Core`): `Level0_Utility_Block` (`ctnOrange`), `Level1_Living_Deck` (`ctnGreen` / `ctnWhite`), `Level2_Penthouse_Spine` (`ctnWhite`). Hidden by default, visible in `xray` and `core_only`.
     - Indian flag emblem decal/quad on north chamfer panel.

4. **Auxiliary Site Infrastructure (Agent 3 scope)**:
   - `Auxiliary_Site_Infrastructure` group containing:
     - `hotspot-satcom`: IcosahedronGeometry (r=5.2, 80 faces, flatShading), ring truss base, 10 stilts at `[-25, 7.2, 35]`.
     - `hotspot-fuel-storage`: 13 cylindrical tanks (InstancedMesh) in 3 rows at `[-80, 4, -35]`.
     - `hotspot-heliport`: Platform cylinder (r=15), 'H' marking geometry, outer ring (r=13-13.5), windsock at `[-85, 4, -95]`.
     - `hotspot-container-depot`: 25 ISO boxes (InstancedMesh, 5x5 grid, 4 colors cycled) at `[-28, 0, -18]`.
     - `hotspot-pipe-rack`: Extruded double-pipe tray on A-frames at `[0, 0.8, 12]`.
     - `hotspot-flagpole-ridge`: 5 flagpoles at `[-45, 2, -70]`.
     - `hotspot-meteo-mast`: Mast atop penthouse at `[0, 13.5, 0]`.
     - `hotspot-meltwater-tarn`: Water plane at `[-35, -1.2, 0]`.
     - Terrain plane: 300x300 plane displaced, pad flattened at Y=0.
     - Blizzard particle system: 3,000 particles drifting with katabatic wind, reset boundary.

5. **MEP SCADA Overlays & 7 Modes (Agent 4 scope)**:
   - `MEP_Life_Support_Overlay` group containing:
     - `StructuralFrameMesh`: 11 exoskeleton portal bents at 4.8m spacing (`#2B3A8C`).
     - `HVACSupplyMesh`: Green trunk + 24 drops (`#27AE60`).
     - `HVACReturnMesh`: Yellow parallel duct (`#F1C40F`).
     - `HydronicHeatMesh`: Red hydronic loops (`#E74C3C`).
     - `DomesticWaterMesh`: Blue water circuit (`#2980B9`).
     - `ElectricalBuswayMesh`: Purple busway trays (`#8E44AD`).
   - `window.set3DMode(mode)`:
     - Handles all 7 modes: `exterior`, `xray`, `core_only`, `hvac`, `thermal`, `structural`, `night`.
     - Toggles outerSkin opacity/transparency, containerCore visibility, MEP layers, and day/night lighting per the mode matrix table in `explorer_survey_2/handoff.md`.

6. **Hotspot Registry & Interaction (Agent 5 scope)**:
   - Populate `HOTSPOT_REGISTRY` with all 21 canonical entries (see `explorer_survey_2/handoff.md §2.8`).
   - Ensure every hotspot object has name `hotspot-<slug>`.
   - Pointermove handler: raycasts interactables, applies emissive highlight (`#7DBFAD`, intensity 0.8) and restores on leave; changes cursor to pointer.
   - Pointerdown handler: raycasts on click, walks up to `hotspot-*` ancestor group, extracts asset slug (`obj.name.replace('hotspot-', '')`), and dispatches:
     `window.dispatchEvent(new CustomEvent('st-3d-click', { detail: assetSlug }));`.
   - Telemetry status bridge `window.update3DHotspot(assetId, status)`:
     - `critical`: color `0xC44536`, emissive `0x9B1C1C`, intensity 0.8.
     - `warning`: color `0xD9822B`, emissive `0x995511`, intensity 0.6.
     - `normal`: restores default material color/emissive.
     - Clones material so individual hotspot mesh instances can be recolored without affecting global materials.

7. **Performance Guard, Animation Loop & Export (Agent 6 scope)**:
   - `checkGeometryBudget(geometry, label)`: counts triangles and warns if budget exceeded. Scene total geometry must stay <= 20,000 triangles in exterior mode.
   - Animation loop (`requestAnimationFrame`): updates particle positions, subtle station float (`Math.sin(t * 0.524) * 1.5`), slow SATCOM radome rotation, orbit controls update, render.
   - Resize listener updating renderer and camera aspect.
   - Scene export:
     ```javascript
     window.station3DScene = {
       scene, camera, renderer, stationGroup, mepGroup,
       setMode: window.set3DMode,
       updateHotspot: window.update3DHotspot,
       hotspotRegistry: HOTSPOT_REGISTRY,
     };
     ```

8. **Update `app/static/js/station_twin.js`**:
   - In `toggle3D()`, add loading of OrbitControls (`https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/controls/OrbitControls.min.js`) sequentially after `three.min.js` so user orbiting works seamlessly.

### Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

### Output Requirements
- Write your handoff report to `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\worker_3d_impl\handoff.md`.
- Report completion back to parent via `send_message`.
