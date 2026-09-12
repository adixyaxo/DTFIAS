## 2026-09-12T05:10:00Z

### Role
E2E Test Infrastructure Worker (`worker_test_infra`)

### Working Directory
`c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\worker_test_infra`

### Exclusive Write Ownership
- `tests/e2e/test_station_3d_harness.html`
- `tests/e2e/verify_3d.js`
- `tests/e2e/test_station_3d_verification.py`
- `TEST_READY.md` (at project root)

### Mandatory Inputs to Read
1. `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\ORIGINAL_REQUEST.md`
2. `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\orchestrator_2\PROJECT.md`
3. `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\explorer_survey_3\handoff.md`
4. `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\explorer_survey_2\handoff.md`

### Task Description
Implement the automated headless 3D verification suite as designed in `explorer_survey_3/handoff.md`:
1. Create `tests/e2e/test_station_3d_harness.html`:
   - Standalone HTML page with viewport `#station-3d-container` and diagnostic test runner panel.
   - Loads Three.js r128, OrbitControls, and `../../app/static/js/three/station_3d_view.js`.
   - Defines `TestRunner3D` class validating all 6 Acceptance Criteria:
     - **AC1: Hierarchy**: Verifies `Substructure_Stilts`, `Exterior_Aerodynamic_Shell`, `Modular_Container_Core`, `MEP_Life_Support_Overlay`, and `Auxiliary_Site_Infrastructure` exist in `window.station3DScene.scene`.
     - **AC2: 21 Hotspots**: Verifies all 21 hotspots from `HOTSPOT_REGISTRY` exist in scene graph with `hotspot-` prefix and have geometry/meshes.
     - **AC3: 7 Modes & X-Ray**: Verifies `window.set3DMode('xray')` makes `Modular_Container_Core.visible === true` and outer skin opacity <= 0.35 (transparent). Tests toggling other modes (`exterior`, `hvac`, `thermal`, `structural`, `night`, `core_only`).
     - **AC4: Status Bridge**: Calls `window.update3DHotspot('power-plant', 'critical')`, verifies emissive hex is `0x9B1C1C` and color hex is `0xC44536`. Tests `warning` and `normal`.
     - **AC5: Raycast Pointer Click**: Projects `hotspot-satcom` anchor to 2D canvas coordinates, dispatches `pointerdown` event, listens for and verifies `st-3d-click` CustomEvent on `window` with `event.detail === 'satcom'`.
     - **AC6: Performance Budget**: Traverses all scene meshes, sums triangles, verifies total <= 20,000 in exterior mode, verifies `checkGeometryBudget` works.
   - Stores results in `window.__TEST_RESULTS__ = { passed: boolean, total: number, passCount: number, failCount: number, tests: [...] }`.
2. Create `tests/e2e/verify_3d.js`:
   - Node.js script using native `fetch` and `WebSocket` (zero external npm packages) to connect via CDP to Microsoft Edge at `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`.
   - Spawns Edge with `--headless=new --remote-debugging-port=9222 --use-gl=angle --use-angle=swiftshader --window-size=1280,720 --disable-gpu --no-first-run`.
   - Connects to `/json/list`, gets WebSocket URL, evaluates `window.__TEST_RESULTS__` after tests complete, prints detailed report to console, kills Edge process, and exits with code 0 on PASS, 1 on FAIL.
3. Create `tests/e2e/test_station_3d_verification.py`:
   - Pytest test case executing Edge headless via Python subprocess or CDP and asserting test suite passes.
4. Create `TEST_READY.md` at project root with runner command, test summary, and coverage table.

### Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

### Output Requirements
- Write your handoff report to `c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\worker_test_infra\handoff.md`.
- Report completion back to parent via `send_message`.
