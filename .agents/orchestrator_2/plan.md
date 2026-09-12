# Execution Plan — Bharati 3D Digital Twin

## Objective
Implement and verify `app/static/js/three/station_3d_view.js` with:
- Procedural Three.js scene (no external GLB)
- P1-P11 extruded aerodynamic hull, quad V-stilts, container core, site assets (SATCOM radome, fuel farm, helipad, container depot, pipe rack, flagpoles, meteo mast, meltwater tarn, terrain, blizzard particle system)
- 7 rendering modes via `window.set3DMode` (exterior, xray, core_only, hvac, thermal, structural, night)
- 21 hotspots in `HOTSPOT_REGISTRY` with `hotspot-` prefix
- Raycasting, pointer hover emissive effect, `pointerdown` click dispatching `st-3d-click` CustomEvent
- Status bridge `window.update3DHotspot(assetId, status)` (critical/warning/normal)
- `checkGeometryBudget` performance guard (<= 20,000 triangles)
- `window.station3DScene` export
- Programmatic headless verification (scene hierarchy, 21 hotspots, mode toggles, status updates, simulated click CustomEvent)

## Phases
1. **Phase 0: Survey & Technical Environment Discovery**
   - Dispatch 3 Explorers (Codebase/Three.js assets, Testing infrastructure/Puppeteer/Node, Specification & CAD alignment).
   - Consolidate Feature Inventory into `PROJECT.md`.
2. **Phase 1: Dual Track — E2E Test Suite & Harness Setup**
   - Establish headless test harness (HTML test page, Node/Puppeteer or JSDOM/Three.js test runner) in `tests/e2e_3d/` or equivalent.
   - Publish `TEST_READY.md`.
3. **Phase 2: Implementation Track**
   - Milestone 1: Scene bootstrap, materials library, hull extrusion P1-P11, V-stilts, penthouse, container core, windows.
   - Milestone 2: Site assets, terrain, blizzard particles, MEP overlays (11 portal bents, HVAC, thermal, domestic water, electrical busway) with 7 rendering modes.
   - Milestone 3: Hotspot registry (21 items), raycasting, pointer hover, click dispatch (`st-3d-click`), `window.update3DHotspot`, performance guard (`checkGeometryBudget`), animation loop.
4. **Phase 3: Final Verification & Gating**
   - Run full E2E test suite.
   - Reviewer verification.
   - Challenger adversarial stress testing.
   - Forensic Integrity Audit (`teamwork_preview_auditor`).
   - Gate verdict & completion report.
