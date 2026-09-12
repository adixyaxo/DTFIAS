# Scope: Bharati 3D Digital Twin Refinement (orchestrator_3)

## Architecture
- Target File: `app/static/js/three/station_3d_view.js`
- Test Harness: `tests/e2e/test_station_3d_harness.html`
- Test Runner: `tests/e2e/verify_3d.js`
- Pytest Suite: `tests/e2e/test_station_3d_verification.py`

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---|---|---|---|
| 1 | Terrain Expansion (R1) | Expand terrain width & depth > 200 to eliminate void | M1 | DISPATCH.md / ORIGINAL_REQUEST.md |
| 2 | Procedural Tundra Texture (R1) | Procedural canvas / tundra shader material (bundler-free) | M1 | DISPATCH.md / ORIGINAL_REQUEST.md |
| 3 | Anchor Helipad (R2) | Eliminate floating helipad, anchor firmly to ground elevation | M1 | DISPATCH.md / ORIGINAL_REQUEST.md |
| 4 | Anchor Flagpoles & Flags (R2) | Ground flagpoles and flags at proper terrain elevation | M1 | DISPATCH.md / ORIGINAL_REQUEST.md |
| 5 | Remove Building Bobbing (R3) | Keep main station position.y strictly constant over time | M1 | DISPATCH.md / ORIGINAL_REQUEST.md |
| 6 | Antarctic Tundra Color Palette (R4) | Realistic/stylized Antarctic research station aesthetic | M1 | DISPATCH.md / ORIGINAL_REQUEST.md |
| 7 | Verification: Headless Station Y (AC1) | Verify station position.y constant across animation frames | M1 | DISPATCH.md / ORIGINAL_REQUEST.md |
| 8 | Verification: Terrain Scale (AC2) | Verify terrain bounding box width/depth > 200 | M1 | DISPATCH.md / ORIGINAL_REQUEST.md |
| 9 | Verification: Object Y-Alignment (AC3) | Verify helipad & flag base Y-coordinates meet ground | M1 | DISPATCH.md / ORIGINAL_REQUEST.md |
| 10 | Verification: Performance Guard (AC4) | Triangle count <= 20,000 via checkGeometryBudget | M1 | DISPATCH.md / ORIGINAL_REQUEST.md |
| 11 | Verification: Regression Suite (AC5) | All 21 hotspots & 7 modes intact and functioning | M1 | DISPATCH.md / ORIGINAL_REQUEST.md |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|---|---|---|---|
| M1 | Bharati 3D Refinement & Verification | Implement R1-R4 & automated verification scripts | None | IN_PROGRESS |

## Interface Contracts
- `window.initStation3D(containerId, options)` remains standard entry point.
- `window.station3DScene` exports scene, camera, renderer, stationGroup, terrainMesh, etc.
- `window.set3DMode(mode)` supports all 7 modes: `exterior`, `xray`, `core_only`, `hvac`, `thermal`, `structural`, `night`.
- `window.update3DHotspot(assetId, status)` recolors meshes and updates emissive materials.
- `window.checkGeometryBudget()` returns triangle budget compliance (<= 20,000).
