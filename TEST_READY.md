# Automated E2E 3D Verification Suite — Bharati Digital Twin

> **Digital Twin for Indian Antarctic Stations (SIH26060)**  
> **Status:** Test Infrastructure Deployed & Operational  
> **Coverage:** 100% of Acceptance Criteria AC1–AC6  
> **Execution Mode:** Headless Chromium (Microsoft Edge) with ANGLE SwiftShader WebGL

---

## 1. Executive Summary

The automated end-to-end verification suite for the Bharati Station 3D Digital Twin (`app/static/js/three/station_3d_view.js`) is fully implemented, verified, and operational.

It provides a dual-tier testing architecture:
1. **Interactive / Standalone WebGL Test Harness (`tests/e2e/test_station_3d_harness.html`)**: A rich, standalone HTML5 test page featuring a live WebGL viewport, an interactive Antarctic SCADA diagnostics panel, mode/status controls, and an embedded `TestRunner3D` that exports comprehensive results to `window.__TEST_RESULTS__`.
2. **Zero-Dependency Headless Node CDP Runner (`tests/e2e/verify_3d.js`)**: A standalone test runner using Node.js native `fetch` and `WebSocket` (no `node_modules` or npm packages required) that launches Microsoft Edge headless with ANGLE SwiftShader software WebGL, attaches via Chrome DevTools Protocol (CDP), and asserts the full test suite.
3. **Pytest Integration Module (`tests/e2e/test_station_3d_verification.py`)**: Integrates seamlessly with the repo's existing `pytest` test suite, executing each acceptance criterion as an independent test function.

---

## 2. Test Execution Commands

### A. Run via Pytest (Standard CI / Test Suite)
```bash
pytest tests/e2e/test_station_3d_verification.py -v
```

### B. Run via Node.js CLI (Fast Headless Verification)
```bash
node tests/e2e/verify_3d.js
```

### C. Run via Node.js CLI with Machine-Readable JSON Output
```bash
node tests/e2e/verify_3d.js --json
```

### D. Interactive Visual Inspection in Browser
Open the harness directly in any modern browser:
```bash
start msedge tests/e2e/test_station_3d_harness.html
# or
start chrome tests/e2e/test_station_3d_harness.html
```

---

## 3. Acceptance Criteria Coverage Matrix

| AC Code | Requirement | Verification Method | Target Contract / Pass Condition | Status |
|:---|:---|:---|:---|:---:|
| **AC1** | **Scene Graph 5-Layer Hierarchy** | `verifyHierarchy(scene)` | Confirms `Substructure_Stilts`, `Exterior_Aerodynamic_Shell`, `Modular_Container_Core`, `MEP_Life_Support_Overlay`, and `Auxiliary_Site_Infrastructure` exist in `window.station3DScene.scene` and contain child geometries. | **OPERATIONAL** |
| **AC2** | **21 Hotspot Registry Completeness** | `verifyHotspots(scene)` | Verifies all 21 canonical hotspots defined in `HOTSPOT_REGISTRY` exist with `hotspot-` prefix and attach valid renderable geometry (`isMesh`, `isPoints`, or `isLine`). | **OPERATIONAL** |
| **AC3** | **7-Mode Matrix & X-Ray Material State** | `verifyModesAndXRay(scene)` | Invokes `window.set3DMode('xray')` and asserts `Modular_Container_Core.visible === true` and outer skin `opacity <= 0.35` (`transparent === true`). Verifies error-free switching across all 7 modes: `exterior`, `xray`, `core_only`, `hvac`, `thermal`, `structural`, `night`. | **OPERATIONAL** |
| **AC4** | **Status Bridge Telemetry Recolor** | `verifyStatusBridge(scene)` | Calls `window.update3DHotspot('power-plant', 'critical')` and verifies mesh `emissive === 0x9B1C1C` and `color === 0xC44536`. Validates `warning` (`0xD9822B`/`0x995511`) and `normal` reverts. | **OPERATIONAL** |
| **AC5** | **Raycast Pointer Interaction (`st-3d-click`)** | `verifyPointerRaycast(scene)` | Projects 3D anchor of target hotspot (`hotspot-satcom`) to 2D canvas coordinates, dispatches a `pointerdown` event, and verifies that `st-3d-click` CustomEvent is fired on `window` with matching asset slug (e.g. `'satcom'`). | **OPERATIONAL** |
| **AC6** | **Scene Triangle Budget Compliance** | `verifyTriangleBudget(scene)` | Traverses all scene meshes (including instanced geometry), sums indexed/non-indexed polygon counts, asserts total `<= 20,000` triangles in exterior mode, and verifies `checkGeometryBudget` function exists. | **OPERATIONAL** |

---

## 4. Test Infrastructure Architecture

```
                                  ┌────────────────────────────────────────┐
                                  │ tests/e2e/test_station_3d_harness.html │
                                  │                                        │
                                  │ • Loads Three.js r128 + OrbitControls  │
                                  │ • Loads static/js/three/...view.js     │
                                  │ • Executes TestRunner3D (AC1 - AC6)    │
                                  │ • Renders SCADA Dark Diagnostics Panel │
                                  │ • Populates window.__TEST_RESULTS__    │
                                  └───────────────────┬────────────────────┘
                                                      │
                                   Evaluated via CDP WebSocket
                                                      │
                       ┌──────────────────────────────┴──────────────────────────────┐
                       ▼                                                             ▼
┌──────────────────────────────────────────────┐              ┌──────────────────────────────────────────────┐
│          tests/e2e/verify_3d.js              │              │ tests/e2e/test_station_3d_verification.py    │
│                                              │              │                                              │
│ • Node.js v20+ CLI Runner                    │              │ • Pytest test suite module                   │
│ • Zero external npm dependencies             │              │ • Uses verify_3d.js fixture                  │
│ • Spawns Edge --headless=new                 │              │ • Individual tests per AC:                   │
│ • ANGLE SwiftShader software WebGL           │              │     - test_station_3d_overall_status         │
│ • Native fetch & WebSocket CDP Client        │              │     - test_ac1_hierarchy                     │
│ • Formatted ANSI terminal report             │              │     - test_ac2_hotspots                      │
│ • Exit 0 on PASS / 1 on FAIL                 │              │     - test_ac3_xray_mode                     │
│ • Supports --json flag for automation        │              │     - test_ac4_status_update                 │
│                                              │              │     - test_ac5_pointer_raycast               │
│                                              │              │     - test_ac6_triangle_budget               │
└──────────────────────────────────────────────┘              └──────────────────────────────────────────────┘
```

---

## 5. Software WebGL Environment Details

- **Browser Executable**: `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` (Chromium 152 engine).
- **Headless Engine**: Modern headless Chromium (`--headless=new`).
- **Software Rendering Pipeline**: ANGLE with Vulkan SwiftShader device (`--use-gl=angle --use-angle=swiftshader`).
- **Isolation Guarantee**: Every headless run provisions a dedicated unique temporary profile directory (`--user-data-dir=...`) and deletes it on exit, preventing port collision or singleton browser lockouts.
- **Physical GPU Dependency**: None. SwiftShader performs CPU-based rasterization, allowing complete CI execution on headless virtual machines, runners, and servers without GPU hardware.

---

## 6. Implementation Progress & Transition to Green

When executed against the initial placeholder file, the test suite accurately and genuinely verifies:
- `AC6_TRIANGLE_BUDGET`: **PASS** (baseline placeholder contains 5,736 triangles, well below the 20,000 budget limit).
- `AC1` through `AC5`: **FAIL** with descriptive diagnostic reports highlighting the missing canonical hierarchy layers, the remaining 19 hotspots, the un-implemented `window.set3DMode`, the un-implemented `window.update3DHotspot`, and the un-exposed camera/renderer.

As `worker_3d_impl` deploys the full Bharati station model into `app/static/js/three/station_3d_view.js`, each test will turn from **FAIL** to **PASS** until all 6 Acceptance Criteria are green.
