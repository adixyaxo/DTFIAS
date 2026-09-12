# Forensic Integrity Audit Report — Bharati 3D Digital Twin (SIH26060)

**Target Deliverables**:
- `app/static/js/three/station_3d_view.js`
- `app/static/js/station_twin.js`
- `tests/e2e/test_station_3d_harness.html`
- `tests/e2e/verify_3d.js`
- `tests/e2e/test_station_3d_verification.py`

**Integrity Profile**: General Project — **Benchmark Mode** (Maximum Strictness)  
**Binary Verdict**: **`CLEAN`** (ZERO INTEGRITY VIOLATIONS)

---

## 1. Observation

### 1.1 Source Code Static Analysis (`app/static/js/three/station_3d_view.js`)
- **Total Lines**: 1,271 lines, 53,447 bytes of pure procedural Three.js JavaScript.
- **External Model Loaders**: Grep inspection for `gltf`, `glb`, `objloader`, `gltfloader`, `fbx`, or remote asset fetches returned **zero matches**. The module constructs 100% of the geometries procedurally from first principles.
- **Procedural Geometries Verified**:
  - `THREE.ExtrudeGeometry`: Lines 363–387 construct the P1–P11 transverse hull contour using CAD blueprint coordinates (`(0, 2.60)`, `(-7.5, 3.40)`, `(-10.0, 5.10)`, `(-9.5, 8.95)`, `(-5.0, 10.10)`, `(-3.8, 11.58)`, `(3.8, 11.58)`, `(5.0, 10.10)`, `(9.5, 8.95)`, `(10.0, 5.10)`, `(7.5, 3.40)`) extruded 50.0m along the X-axis.
  - `THREE.CylinderGeometry`: Used for the tapered 4-segment V-stilt quad bents (lines 127–154), 28 vertical stilts, 28 footing pads, knee bracing struts, SATCOM tubular supports, fuel farm tanks, helipad perimeter/pole, pipe rack A-frames, flagpoles, and meteo mast.
  - `THREE.InstancedMesh`: 28 vertical stilts (`stiltsIM`), 28 concrete footing pads (`padsIM`), 13 fuel farm tanks (`fuelIM`), and 25 NW apron ISO containers (`depotIM`).
  - `THREE.IcosahedronGeometry`: Lines 712–716 construct the SATCOM geodesic radome with radius 5.2m and detail level 2 (exactly 80 triangular faces, `flatShading: true`).
  - `THREE.PlaneGeometry`: Lines 912–944 construct the 300m x 300m Larsemann Hills terrain with a 48x48 vertex resolution, algorithmic sinusoidal elevation displacement, Prydz Bay coastal drop, and a flattened bedrock datum (`Y = 0`) directly under the station. Also used for the meltwater tarn and a canvas-generated 24-spoke Indian National Flag emblem (`CanvasTexture`).
  - `THREE.Points` / `THREE.BufferGeometry`: Lines 947–974 generate 3,000 particles with individual velocity vectors simulating Antarctic katabatic blizzard drift with boundary reset loops.
- **Hotspot Registry & Scene Graph**:
  - All 21 canonical hotspots (`hotspot-power-plant`, `hotspot-hvac`, `hotspot-chp-heating`, `hotspot-water-lss`, `hotspot-workshop-garage`, `hotspot-main-hab`, `hotspot-dining-mess`, `hotspot-medical-bay`, `hotspot-ocean-lounge`, `hotspot-science-terrace`, `hotspot-meteo-mast`, `hotspot-v-stilts`, `hotspot-satcom`, `hotspot-fuel-storage`, `hotspot-pipe-rack`, `hotspot-heliport`, `hotspot-container-depot`, `hotspot-meltwater-tarn`, `hotspot-flagpole-ridge`, `hotspot-meteo-science-lab`, `hotspot-main-entrance`) are declared in `HOTSPOT_REGISTRY` (lines 22–44) and instantiated as interactive groups attached to the scene graph.
- **7-Mode SCADA Controller (`window.set3DMode`)**:
  - Lines 986–1056 genuinely manipulate exterior shell visibility/transparency (opacity 1.0 for exterior, 0.25 for xray, 0.15 for MEP), toggle `Modular_Container_Core` visibility, toggle MEP system sub-layers (`StructuralFrameMesh`, `HVACSupplyMesh`, `HVACReturnMesh`, `HydronicHeatMesh`), and reconfigure diurnal/nocturnal lighting and warm window emissive materials for night mode.
- **Status Bridge (`window.update3DHotspot`)**:
  - Lines 1154–1198 traverse the target group, cache original material attributes, clone/update mesh materials to `#C44536` / `#9B1C1C` (critical), `#D9822B` / `#995511` (warning), or restore original materials on normal.
- **Raycasting & Event Dispatch**:
  - Lines 1059–1151 use `THREE.Raycaster` with camera projection, apply emissive hover highlight (`#7DBFAD`, intensity 0.8), set `cursor = 'pointer'`, and dispatch `new CustomEvent('st-3d-click', { detail: assetSlug })` on `window` upon pointerdown.

### 1.2 Test Harness & Runner Analysis (`test_station_3d_harness.html` & `verify_3d.js`)
- `tests/e2e/test_station_3d_harness.html`:
  - `TestRunner3D` inspects real objects in `window.station3DScene.scene`.
  - `verifyHierarchy`: dynamically queries `scene.getObjectByName(layerName)` for all 5 layers and inspects `childrenCount`.
  - `verifyHotspots`: inspects all 21 keys, checks for child meshes, and asserts count is exactly 21.
  - `verifyModesAndXRay`: invokes `window.set3DMode('xray')` and asserts `coreVisible === true`, `opacity <= 0.35`, `transparent === true`, and iterates all 7 modes.
  - `verifyStatusBridge`: invokes `window.update3DHotspot('power-plant', 'critical')` and verifies actual hex `0x9B1C1C` and `0xC44536`.
  - `verifyPointerRaycast`: calculates world position of `hotspot-satcom`, projects to NDC screen space, dispatches genuine DOM `PointerEvent('pointerdown')` on canvas, and captures `st-3d-click`.
  - `verifyTriangleBudget`: traverses all meshes, computes indexed/position count / 3, multiplies by instanced counts, and asserts `totalTriangles <= 20000`.
  - Zero hardcoded boolean pass returns or dummy mocks found.
- `tests/e2e/verify_3d.js`:
  - Genuinely locates Microsoft Edge Chromium (`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`).
  - Spawns headless Edge with `--headless=new`, `--use-gl=angle`, `--use-angle=swiftshader`, `--remote-debugging-port=9222`.
  - Establishes genuine WebSocket CDP connection to `ws://127.0.0.1:9222/devtools/page/...`.
  - Evaluates `window.__TEST_RESULTS__` across CDP, formats output, and terminates browser processes cleanly.

### 1.3 Execution Verification Results
- **CDP Verification (`node tests/e2e/verify_3d.js`)**:
  ```text
  ════════════════════════════════════════════════════════════════════
    BHARATI 3D DIGITAL TWIN — HEADLESS E2E VERIFICATION RUNNER
  ════════════════════════════════════════════════════════════════════
  [Verify3D] Using Edge binary: C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
  [Verify3D] Debugging Port:    9222
  [Verify3D] Harness URI:       file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/tests/e2e/test_station_3d_harness.html
  [Verify3D] CDP attached: ws://127.0.0.1:9222/devtools/page/...
  [Verify3D] Awaiting 3D initialization and automated test execution...

  ════════════════════════════════════════════════════════════════════
    VERIFICATION RESULT: PASSED
    Tests: 6 | Passed: 6 | Failed: 0
    Timestamp: 2026-09-12T05:21:11.007Z
  ════════════════════════════════════════════════════════════════════
  [✔ PASS] [AC1_HIERARCHY] Scene Graph 5-Layer Canonical Hierarchy
  [✔ PASS] [AC2_HOTSPOTS] 21 Hotspot Registry Names Present in Scene
  [✔ PASS] [AC3_XRAY_MODE] 7-Mode Matrix & X-Ray Material State
  [✔ PASS] [AC4_UPDATE_HOTSPOT] Hotspot Status Emissive & Color Update
  [✔ PASS] [AC5_POINTER_RAYCAST] Raycast Pointer Click Dispatch (st-3d-click)
  [✔ PASS] [AC6_TRIANGLE_BUDGET] Scene Triangle Budget Compliance (<= 20,000)
  ```
- **Pytest E2E Suite (`pytest tests/e2e/test_station_3d_verification.py`)**:
  ```text
  collected 7 items
  tests\e2e\test_station_3d_verification.py .......                        [100%]
  ============================== 7 passed in 8.75s ==============================
  ```
- **Pytest Unit Suite (`pytest tests/unit`)**:
  ```text
  collected 7 items
  tests\unit\engine\test_core_services.py ...                              [ 42%]
  tests\unit\engine\test_portal_services.py ....                           [100%]
  ============================== 7 passed in 0.19s ==============================
  ```
- **Empirical Triangle & Geometry Audit (`tests/e2e/deep_challenge_geometry.js`)**:
  - Exterior Scene Triangles: **10,906** (Limit: <= 20,000) -> **PASS**
  - Total All Layers Triangles: **12,354** -> **PASS**
  - All 21 Hotspots verified with non-zero bounding boxes and valid renderable child meshes -> **PASS**

### 1.4 Architecture Compliance Checks (GEMINI.md)
- **C1 (Engine Layer Purity)**: Grep for `fastapi|sqlalchemy|asyncpg|jinja2|starlette` in `engine/` returned **0 matches**.
- **C13 (Service Role Key)**: Grep for `SUPABASE_SERVICE_ROLE_KEY` in `app/static/` and `app/templates/` returned **0 matches**.
- **C14 (Supabase Realtime in Browser)**: Grep for `supabase-js` / `createClient` in `app/static/` and `app/templates/` returned **0 matches**.
- **C16 (Lazy Loading of 3D)**: Three.js and `station_3d_view.js` are strictly absent from unconditional scripts in `app/templates/layouts/base.html`; lazy loaded on-demand in `station_twin.js` / `station_twin.html` via `toggle3D()`.

---

## 2. Logic Chain

1. **Premise**: Under Benchmark Mode integrity enforcement, any hardcoded test result, facade implementation, pre-populated verification output, copied/external model dependency, or fake test runner constitutes an automatic Integrity Violation.
2. **Analysis of 3D Implementation**:
   - Inspection of `app/static/js/three/station_3d_view.js` reveals genuine, fine-grained procedural math across 1,271 lines, matching the physical Bharati blueprints (50m length, P1–P11 elevation points, 22° V-stilts, 28 vertical stilts, 15° negative rake prow, 80-face SATCOM icosahedron, algorithmic terrain, 3,000 particle katabatic blizzard).
   - Zero external model files (GLTF/GLB/OBJ) are referenced or loaded.
   - All 21 hotspots are genuine `THREE.Group` instances with renderable meshes, attached to the canonical layers.
   - Mode switching (`window.set3DMode`) and telemetry recoloring (`window.update3DHotspot`) actively mutate material and scene properties.
   - Pointer events interact via actual Three.js Raycaster and camera projection matrices.
   - Therefore, the 3D implementation is an authentic, from-scratch engineering product.
3. **Analysis of Verification Suite**:
   - `test_station_3d_harness.html` exposes `TestRunner3D`, which directly inspects `window.station3DScene.scene`, computes actual geometry triangle counts, triggers actual mode mutations, projects coordinates, and catches dispatched DOM events.
   - `verify_3d.js` does not emit static or canned text; it spawns Edge in headless mode, connects via Chromium DevTools Protocol over WebSockets, drives ANGLE SwiftShader WebGL execution, and harvests runtime results.
   - `test_station_3d_verification.py` executes `verify_3d.js --json` as a subprocess and validates all 6 Acceptance Criteria.
4. **Conclusion**: No prohibited patterns exist. The deliverable fulfills all Benchmark Mode requirements authentically.

---

## 3. Caveats

- In headless Windows environments, running Chromium with SwiftShader software WebGL requires 15–25 seconds for shader initialization and browser startup. Subprocess timeouts in automated CI runners must be configured to at least 45 seconds to avoid false timeouts on resource-constrained hosts.
- Challenger stress tests highlighted that passing non-string values (e.g. integer or object IDs) to `window.update3DHotspot` throws a TypeError because `assetId.startsWith` expects a string. While this is an adversarial edge case not encountered in standard telemetry consumption (which uses string slugs), a type guard (`String(assetId)`) in production hardening is recommended.

---

## 4. Conclusion

**Final Assessment**: **`CLEAN`**

The Bharati 3D Digital Twin implementation (`station_3d_view.js`), frontend integration (`station_twin.js`), standalone test harness (`test_station_3d_harness.html`), CDP test runner (`verify_3d.js`), and pytest suite (`test_station_3d_verification.py`) represent a fully authentic, rigorous, from-scratch implementation. All 21 hotspots, 7 rendering modes, procedural geometries, raycast events, and performance budgets are verified empirically.

---

## 5. Verification Method

To independently verify these findings on any machine with Node.js and Python installed:

1. **Execute Headless CDP Verification**:
   ```bash
   node tests/e2e/verify_3d.js
   ```
   *Expected Output*: Exit code 0, all 6 ACs marked `[✔ PASS]`.

2. **Execute Pytest E2E Verification**:
   ```bash
   pytest tests/e2e/test_station_3d_verification.py -v
   ```
   *Expected Output*: 7 passed in under 15 seconds.

3. **Execute Procedural Triangle & Geometry Deep Challenge**:
   ```bash
   node tests/e2e/deep_challenge_geometry.js
   ```
   *Expected Output*: 10,906 exterior triangles (<= 20,000 limit), 21/21 valid hotspots.

4. **Verify Architecture Purity Constraints**:
   ```bash
   grep -rE "^(import|from) (fastapi|sqlalchemy|asyncpg|jinja2)" engine/
   grep -r "SUPABASE_SERVICE_ROLE_KEY" app/static/ app/templates/
   grep -r "supabase-js" app/static/ app/templates/
   ```
   *Expected Output*: Zero matches for all three commands.
