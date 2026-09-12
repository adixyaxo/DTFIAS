# Project: Bharati 3D Digital Twin (DTFIAS)

## Architecture
- Single procedural Three.js module at `app/static/js/three/station_3d_view.js` (bundler-free, lazy-loaded via Alpine.js `x-init` / `toggle3D()`).
- Scene Graph Hierarchy:
  - `Substructure_Stilts`: 4 Quad V-stilt bents + 28 vertical stilts + 28 concrete footing pads + knee braces.
  - `Exterior_Aerodynamic_Shell`: Extruded P1-P11 hull (50m L, X: -25 to +25), 6-bay panoramic prow (15° rake, 5 mullions), penthouse, access stairs (2x 13-step), corner chamfers.
  - `Modular_Container_Core`: L0 utility block (`ctnOrange`), L1 living deck (`ctnGreen`/`ctnWhite`), L2 penthouse (`ctnWhite`).
  - `MEP_Life_Support_Overlay`: 11 exoskeleton portal bents, HVAC supply/return ducts, hydronic heat loops, domestic water, electrical busway.
  - `Auxiliary_Site_Infrastructure`: SATCOM geodesic radome (80 faces), fuel farm (13 tanks, InstancedMesh), helipad ('H' mark, ring, windsock), container depot (25 boxes), pipe rack, flagpoles (5x), meteo mast, meltwater tarn, noise-displaced terrain plane, blizzard particle system (3,000 particles).
- 7 Rendering Modes via `window.set3DMode(mode)`: `exterior`, `xray`, `core_only`, `hvac`, `thermal`, `structural`, `night`.
- 21 Canonical Hotspots with `hotspot-` prefix in `HOTSPOT_REGISTRY`.
- Raycasting: pointermove emissive highlight (`#7DBFAD`, 0.8); pointerdown fires `st-3d-click` CustomEvent on `window`.
- Telemetry/Status Bridge: `window.update3DHotspot(assetId, status)` (critical: `#C44536` / `#9B1C1C`, warning: `#D9822B` / `#995511`, normal: revert).
- Performance Guard: `checkGeometryBudget(geometry, label)` enforcing <= 20,000 triangles total in exterior mode.
- Global Scene Export: `window.station3DScene = { scene, camera, renderer, stationGroup, mepGroup, setMode, updateHotspot, hotspotRegistry }`.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | WebGL Renderer & Scene Bootstrap | WebGLRenderer, ACESFilmicToneMapping, PCFSoftShadowMap, camera at (120, 90, 160), OrbitControls | M1 | 06-subagent §1 |
| 2 | Brand Lighting & Fog | Deep green ambient (`#1A312C`), polar sun (`#7DBFAD`), teal backfill (`#428475`), fog (`#0B1C18`), night aurora lighting | M1 | 06-subagent §1.3 |
| 3 | Material Library (`window._bm`) | Shared PBR standard/physical materials (hull, roof, keel, glazing, warm window, stilts, concrete, container colors) | M1 | 06-subagent §2.1 |
| 4 | Transverse Hull Profile P1–P11 | Exact CAD extruded profile (50m L along X: -25 to +25), recessed window ribbon (Y=7.8 to 9.0) | M1 | 17-blueprint §3 |
| 5 | Quad Cantilever V-Stilts | 4 bents (outer/inner port/starboard) with 22° incline, 4-segment tapered box sections | M1 | 11-blueprint |
| 6 | 28 Vertical Stilts & Footing Pads | Instanced cylindrical stilts + 28 concrete footing pads at Y=0 + knee bracing | M1 | 06-subagent §2.2 |
| 7 | 6-Bay Panoramic Prow Window | 15° negative rake prow profile, 5 vertical mullions, day/night glazing materials | M1 | 06-subagent §2.5 |
| 8 | Penthouse, Stairs & Chamfers | Level 2 penthouse, 2x 13-step access stairs (rise 0.18, tread 0.28), 4x 45° corner chamfers, Indian flag decal | M1 | 06-subagent §2.6, §2.7 |
| 9 | Modular Container Core (X-Ray) | L0 utility (`ctnOrange`), L1 living deck (`ctnGreen`/`ctnWhite`), L2 penthouse (`ctnWhite`) | M1 | 06-subagent §2.9 |
| 10 | SATCOM Geodesic Radome | IcosahedronGeometry (r=5.2, 80 faces, flatShading), ring truss base, 10 stilts at [-25, 7.2, 35] | M2 | 06-subagent §3.1 |
| 11 | Fuel Farm (13 Tanks) | InstancedMesh of 13 cylindrical tanks (296 kL) in 3 rows at [-80, 4, -35] | M2 | 06-subagent §3.2 |
| 12 | Helipad with 'H' Marking | Cylinder (r=15), 'H' marking geometry, outer ring (r=13-13.5), windsock at [-85, 4, -95] | M2 | 06-subagent §3.3 |
| 13 | Container Depot (NW Apron) | InstancedMesh of 25 ISO boxes (5x5 grid, cycled 4 colors) at [-28, 0, -18] | M2 | 06-subagent §3.4 |
| 14 | Trace-Heated Pipe Rack & Flagpoles | Extruded double-pipe tray along curve + 5x flagpoles at [-45, 2, -70] + meteo mast | M2 | 06-subagent §3.5, §3.6, §3.7 |
| 15 | Meltwater Tarn & Terrain Plane | Displaced plane (300x300, 64x64, pad flattened at Y=0) + water plane at [-35, -1.2, 0] | M2 | 06-subagent §3.8, §3.9 |
| 16 | Blizzard Particle System | 3,000 particles drifting with katabatic wind, boundary reset loop | M2 | 06-subagent §3.10 |
| 17 | MEP Exoskeleton Structural Bents | 11 portal bents at 4.8m spacing (`#2B3A8C`, `StructuralFrameMesh`) | M2 | 06-subagent §4.1 |
| 18 | HVAC Supply & Return Ducts | Green trunk + 24 drops (`#27AE60`) + yellow return (`#F1C40F`) | M2 | 06-subagent §4.2, §4.3 |
| 19 | Hydronic Heat, Water & Electrical | Red hydronic loops (`#E74C3C`), blue domestic water (`#2980B9`), purple busway (`#8E44AD`) | M2 | 06-subagent §4.4, §4.5, §4.6 |
| 20 | 7-Mode Rendering State Matrix | `window.set3DMode`: exterior, xray, core_only, hvac, thermal, structural, night | M2 | 06-subagent §1.4, §4 |
| 21 | 21 Hotspots Registry & Names | All 21 hotspots named with `hotspot-` prefix matching canonical `HOTSPOT_REGISTRY` | M3 | 06-subagent §5.1 |
| 22 | Raycaster & Hover Effect | Pointermove raycasting with emissive highlight (`#7DBFAD`, 0.8) and pointer cursor | M3 | 06-subagent §5.2, §5.3 |
| 23 | Click Dispatcher (`st-3d-click`) | Pointerdown raycast walking up to `hotspot-*` group, firing `st-3d-click` with asset slug | M3 | 06-subagent §5.4 |
| 24 | Telemetry Status Bridge | `window.update3DHotspot(assetId, status)` handling critical (`#C44536`/`#9B1C1C`), warning (`#D9822B`), normal | M3 | 06-subagent §5.5 |
| 25 | Performance Guard (<= 20k tris) | `checkGeometryBudget(geometry, label)` enforcing <= 20,000 triangles total in exterior mode | M3 | 06-subagent §6.1 |
| 26 | Animation Loop & Global Export | RequestAnimationFrame loop (station float, radome rotation, blizzard particles) + `window.station3DScene` | M3 | 06-subagent §6.2, §6.5 |
| 27 | OrbitControls Integration | Enable OrbitControls in loader (`station_twin.js`) and safe check in 3D module | M3 | survey_1 handoff |
| 28 | Standalone HTML Test Harness | `tests/e2e/test_station_3d_harness.html` with `TestRunner3D` validating AC1–AC6 and exporting `window.__TEST_RESULTS__` | E2E | survey_3 handoff |
| 29 | Headless Node CDP Verification Script | `tests/e2e/verify_3d.js` executing Edge `--headless=new` via native WebSocket CDP | E2E | survey_3 handoff |
| 30 | Pytest E2E Verification Integration | `tests/e2e/test_station_3d_verification.py` running in standard pytest suite | E2E | survey_3 handoff |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| Survey | Survey & Technical Discovery | Survey codebase, CAD datums, test environment | none | DONE |
| E2E | E2E Test Infra Track | Standalone HTML harness (`test_station_3d_harness.html`), Node CDP runner (`verify_3d.js`), Pytest runner, publish `TEST_READY.md` | Survey | DONE |
| M1 | Core Scene & Station Hull Geometry | Renderer, camera, brand lighting, materials, P1-P11 hull extrusion, quad V-stilts, 28 vertical stilts, prow glazing, penthouse, container core | Survey | DONE |
| M2 | Site Assets, MEP Overlays & 7 Modes | SATCOM radome, fuel farm, helipad, container depot, pipe rack, flagpoles, tarn, terrain, blizzard particles, MEP meshes, 7-mode state machine (`window.set3DMode`) | M1 | DONE |
| M3 | Hotspots, Raycasting & Telemetry Bridge | 21 hotspots in scene, raycaster hover & click (`st-3d-click`), `window.update3DHotspot`, performance guard (<=20k tris), animation loop, `window.station3DScene` export, OrbitControls loading in `station_twin.js` | M2 | DONE |
| Final | E2E Test Suite Pass & Adversarial Hardening | Execute full automated test suite (AC1–AC6), Reviewer verification, Challenger verification, Forensic Integrity Audit | E2E, M3 | DONE |

## Interface Contracts
### Global Functions:
- `window.initStation3D(containerId)`: Bootstraps the scene into the specified DOM container element.
- `window.set3DMode(mode)`: Sets rendering mode (`'exterior'`, `'xray'`, `'core_only'`, `'hvac'`, `'thermal'`, `'structural'`, `'night'`).
- `window.update3DHotspot(assetId, status)`: Sets status styling on `hotspot-${assetId}` (`'critical'`, `'warning'`, `'normal'`).
- `window.station3DScene`: Scene export exposing `{ scene, camera, renderer, stationGroup, mepGroup, setMode, updateHotspot, hotspotRegistry }`.

### Custom Events:
- `st-3d-click`: Emitted on `window` on raycast pointerdown hit. `event.detail` is the asset slug (e.g. `'power-plant'`).
