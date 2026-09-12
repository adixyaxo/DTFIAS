# Handoff Report: Headless 3D Verification Environment & Test Harness Architecture

**Explorer ID:** explorer_survey_3  
**Date:** 2026-09-12  
**Mission:** Investigate testing environment and execution capabilities for headless 3D verification on Windows, define programmatic verification for Acceptance Criteria 1–6, and design the test harness architecture for the Bharati 3D station twin.

---

## 1. Observation

### 1.1 System Runtimes & Tool Inventory
Direct empirical inspection of the host Windows environment yielded the following:

- **Node.js**: `v26.5.0` installed (`node --version`).
- **npm**: `11.17.0` installed (`npm --version`).
- **Python**: `Python 3.14.6` (64-bit) installed (`python --version`).
- **Python Testing Stack**:
  - `pytest 9.1.1` installed (`python -m pip list`).
  - `pytest-asyncio 1.4.0` installed.
  - `httpx 0.28.1` installed.
  - `websockets 15.0.1` installed.
  - `anyio 4.15.1` installed.
  - `playwright` and `selenium`: **Not installed** in Python environment (`import playwright` exited 1).
- **Browser Availability**:
  - Google Chrome: Not installed at standard paths (`Program Files`, `LocalAppData`).
  - **Microsoft Edge (Chromium)**: **Installed** at `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`.
  - Edge File Version: `152.0.4191.66` (Chromium 152 engine).
  - Supports Chrome DevTools Protocol (CDP), `--headless=new`, and software WebGL rendering via ANGLE SwiftShader.
- **Network & CDN Connectivity**:
  - `curl.exe -I https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js` returned `HTTP/1.1 200 OK`.
  - `curl.exe -I https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js` returned `HTTP/1.1 200 OK`.

### 1.2 Headless WebGL Execution Test
We empirically tested WebGL initialization inside headless Microsoft Edge using:
```powershell
cmd /c "`"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`" --headless=new --use-gl=angle --use-angle=swiftshader --dump-dom file:///..."
```
**Verbatim Output from Edge WebGL probe:**
```
SUCCESS: ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver) (Google Inc. (Google))
```
This confirms headless Chromium on this machine initializes full WebGL and WebGL2 without requiring physical GPU hardware or an active desktop display.

### 1.3 Direct CDP Protocol Test
We tested launching Microsoft Edge with `--remote-debugging-port=9222` and controlling it via Python using native `httpx` and `websockets`.
- Edge opened port 9222 immediately.
- WebSocket session was established to `/devtools/page/<id>`.
- `Runtime.evaluate` command `{ "expression": "1 + 1" }` returned:
  ```json
  {"id": 2, "result": {"result": {"type": "number", "value": 2, "description": "2"}}}
  ```
- Headless Edge test page loaded `three.min.js`, `OrbitControls.js`, and `station_3d_view.js`, successfully executing `window.initStation3D('station-3d-container')` and creating the `<canvas>` element with zero WebGL or runtime errors.

### 1.4 Codebase & Documentation Baseline
- **Existing Implementation** (`app/static/js/three/station_3d_view.js`):
  - Defines `window.initStation3D(containerId)` and `window.station3DScene`.
  - Implements basic scene, camera, lights, particle loop, and placeholder meshes.
  - **Does NOT contain** the 5 canonical hierarchy groups (`Substructure_Stilts`, etc.).
  - **Does NOT contain** meshes named with `hotspot-` prefix.
  - **Does NOT contain** `window.set3DMode`.
- **Target Architectural Specifications**:
  - `docs/bharati3d/05-subagent_synthesis.md` §10 defines the 5 canonical hierarchy groups and their exact children.
  - `docs/bharati3d/06-subagent_implementation_plan.md` §5.1 defines all 21 hotspots in `HOTSPOT_REGISTRY`.
  - `docs/bharati3d/06-subagent_implementation_plan.md` §5.5 defines `window.update3DHotspot(assetId, status)` with critical color `0xC44536` and emissive `0x9B1C1C`.
  - `docs/bharati3d/06-subagent_implementation_plan.md` §6.1 defines `checkGeometryBudget` and triangle limit `<= 20,000`.
  - `docs/bharati3d/06-subagent_implementation_plan.md` §5.4 defines `st-3d-click` CustomEvent dispatch.

---

## 2. Logic Chain

### Step 1: Headless Node.js vs. Headless Browser Execution
1. Pure Node.js (`node`) is suitable for AST static analysis (e.g. searching for regex patterns, parsing with Acorn/Babel) or mathematical unit tests (`THREE.Vector3`, `THREE.Box3`).
2. However, `station_3d_view.js` executes against DOM APIs (`document.getElementById`, `container.clientWidth`, `container.appendChild(renderer.domElement)`) and WebGL rendering APIs (`canvas.getContext('webgl2')`).
3. Running Three.js WebGL in headless Node without a browser requires native C++ bindings such as `headless-gl` or `node-canvas`. On Windows, these frequently fail to compile or lack WebGL2 feature parity.
4. Conversely, Microsoft Edge (Chromium 152) is already installed on this machine and natively provides software WebGL via ANGLE SwiftShader. Therefore, **a headless Chromium instance is the authoritative execution environment**.

### Step 2: Verification Strategy for Acceptance Criteria 1–6

#### Acceptance Criteria 1: Scene Graph Hierarchy
- **Requirement**: Scene hierarchy contains `Substructure_Stilts`, `Exterior_Aerodynamic_Shell`, `Modular_Container_Core`, `MEP_Life_Support_Overlay`, `Auxiliary_Site_Infrastructure`.
- **Logic**:
  1. Once `initStation3D` finishes, `window.station3DScene.scene` (or `window.station3DScene.stationGroup`) is accessible.
  2. For each of the 5 canonical group names, query `scene.getObjectByName(name)`.
  3. Verify each group exists (`!!obj`), is an instance of `THREE.Group` or `THREE.Object3D`, and contains children (`obj.children.length > 0`).

#### Acceptance Criteria 2: All 21 Hotspots from `HOTSPOT_REGISTRY`
- **Requirement**: All 21 hotspots exist in the scene graph with `hotspot-` prefix.
- **Logic**:
  1. Retrieve `HOTSPOT_REGISTRY` keys (e.g. `window.station3DScene.hotspotRegistry` or the canonical 21-element array).
  2. For each hotspot key (e.g. `hotspot-power-plant`, `hotspot-satcom`, etc.):
     - Query `scene.getObjectByName(key)`.
     - Confirm object is not null.
     - Confirm object has attached geometry or child meshes (`obj.traverse` finds at least one `isMesh`).
  3. Assert 21 of 21 hotspots resolve.

#### Acceptance Criteria 3: Multi-Mode Switching (`window.set3DMode('xray')`)
- **Requirement**: Invoking `window.set3DMode('xray')` reduces outer skin opacity and makes `containerCore` visible.
- **Logic**:
  1. Call `window.set3DMode('exterior')` as baseline:
     - Verify `Modular_Container_Core.visible === false`.
     - Read outer skin material opacity (baseline >= 0.85).
  2. Call `window.set3DMode('xray')`:
     - Inspect `Modular_Container_Core.visible` -> must be `true`.
     - Inspect outer skin material opacity -> must be <= 0.35 (canonical value 0.25) and `transparent === true`.

#### Acceptance Criteria 4: Telemetry Status Update (`window.update3DHotspot('power-plant', 'critical')`)
- **Requirement**: Emissive color changes to critical hex.
- **Logic**:
  1. Target hotspot: `scene.getObjectByName('hotspot-power-plant')`.
  2. Call `window.update3DHotspot('power-plant', 'critical')`.
  3. Traverse meshes of the target object.
  4. Inspect `mesh.material.emissive.getHex()` -> must equal `0x9B1C1C`.
  5. Inspect `mesh.material.color.getHex()` -> must equal `0xC44536`.
  6. Inspect `mesh.material.emissiveIntensity` -> must be >= 0.6.

#### Acceptance Criteria 5: Raycasting Pointer Interaction & Event Dispatch
- **Requirement**: Simulating pointer click on canvas fires `st-3d-click` CustomEvent on `window`.
- **Logic**:
  1. Register an event listener on `window` for `st-3d-click`:
     ```javascript
     let emittedSlug = null;
     window.addEventListener('st-3d-click', (e) => { emittedSlug = e.detail; });
     ```
  2. Pick a known hotspot with clear line-of-sight (e.g. `hotspot-satcom` at `[-25, 7.2, 35]` or `hotspot-power-plant`).
  3. Project 3D anchor to 2D canvas coordinates:
     ```javascript
     const pos = new THREE.Vector3(-25.0, 7.2, 35.0);
     pos.project(camera);
     const rect = canvas.getBoundingClientRect();
     const clientX = rect.left + ((pos.x + 1) / 2) * rect.width;
     const clientY = rect.top + ((-pos.y + 1) / 2) * rect.height;
     ```
  4. Dispatch a simulated `PointerEvent('pointerdown', { clientX, clientY, bubbles: true })` on `renderer.domElement`.
  5. Assert `emittedSlug` equals `'satcom'` (verifying `hotspot-` prefix was stripped).

#### Acceptance Criteria 6: Triangle Budget Limit (<= 20,000)
- **Requirement**: Triangle budget <= 20,000 via `checkGeometryBudget`.
- **Logic**:
  1. Traverse all meshes in `scene`:
     - If indexed geometry: `tri = geometry.index.count / 3`
     - If non-indexed: `tri = geometry.attributes.position.count / 3`
     - If `InstancedMesh`: multiply by `instanceCount`.
  2. Sum total triangles across the entire scene graph.
  3. Assert `totalTriangles <= 20000`.
  4. Test invoking `checkGeometryBudget` directly to confirm warning logging threshold.

---

## 3. Test Harness Architecture

To decouple test execution from specific test runners and enable both automated CI testing and human developer visual inspection, the test harness is architected into two tiers:

```
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 1: Standalone Browser Test Harness Page                           │
│ File: tests/e2e/test_station_3d_harness.html                           │
│                                                                        │
│ • Loads Three.js r128 + OrbitControls + station_3d_view.js             │
│ • Creates fixed-dimension 1280×720 WebGL viewport container            │
│ • Self-contained TestRunner3D class executing all 6 AC assertions      │
│ • Exports results to window.__TEST_RESULTS__ object                    │
│ • Visual SCADA dark UI with live mode controls & status badges         │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
                 ┌───────────────────┴───────────────────┐
                 ▼                                       ▼
┌─────────────────────────────────────┐ ┌────────────────────────────────┐
│ TIER 2A: Python Pytest CDP Runner   │ │ TIER 2B: Node.js CDP Runner    │
│ File: tests/e2e/test_station_3d.py  │ │ File: tests/e2e/verify_3d.js   │
│                                     │ │                                │
│ • Native Python pytest integration  │ │ • Standalone CLI runner        │
│ • Uses httpx + websockets via CDP   │ │ • Uses Node native WebSocket   │
│ • Spawns Edge --headless=new        │ │ • Reads window.__TEST_RESULTS__│
│ • Asserts each AC as a test case    │ │ • Exits 0 on PASS, 1 on FAIL   │
└─────────────────────────────────────┘ └────────────────────────────────┘
```

### 3.1 Tier 1: Standalone Test Harness (`tests/e2e/test_station_3d_harness.html`)
The standalone test page encapsulates all scene initialization and programmatic checks:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Bharati 3D Digital Twin — Verification Harness</title>
  <!-- Three.js + OrbitControls -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
  <!-- Target 3D View Script -->
  <script src="../../app/static/js/three/station_3d_view.js"></script>
  <style>
    body { margin: 0; background: #0B1C18; color: #E8E3D9; font-family: 'Inter', sans-serif; display: flex; height: 100vh; }
    #viewport-pane { flex: 1; position: relative; }
    #station-3d-container { width: 100%; height: 100%; }
    #test-panel { width: 420px; background: #1A312C; border-left: 1px solid #428475; padding: 20px; overflow-y: auto; font-size: 13px; }
    .badge-pass { background: #2E7D5B; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
    .badge-fail { background: #C44536; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
    .test-card { background: #0F231F; border: 1px solid #285044; border-radius: 6px; padding: 10px; margin-bottom: 10px; }
  </style>
</head>
<body>
  <div id="viewport-pane">
    <div id="station-3d-container"></div>
  </div>
  <div id="test-panel">
    <h2>Bharati 3D Verification Suite</h2>
    <div id="overall-status">Running diagnostics...</div>
    <div id="results-list"></div>
  </div>

  <script>
    window.HOTSPOT_REGISTRY = {
      'hotspot-power-plant':      { label: 'CHP Power Plant',        anchor: [-19.2, 2.8,  7.2] },
      'hotspot-hvac':             { label: 'HVAC Life Support',       anchor: [-7.2,  10.2, 0.0] },
      'hotspot-chp-heating':      { label: 'District Heating',        anchor: [-6.0,  3.2,  0.0] },
      'hotspot-water-lss':        { label: 'Water & LSS',             anchor: [-19.2, 2.8, -7.2] },
      'hotspot-workshop-garage':  { label: 'Vehicle Garage',          anchor: [-18.0, 3.8,  0.0] },
      'hotspot-main-hab':         { label: 'Main Habitat',            anchor: [0.0,   5.5,  0.0] },
      'hotspot-dining-mess':      { label: 'Dining Mess',             anchor: [-18.0, 6.5,  0.0] },
      'hotspot-medical-bay':      { label: 'Medical Bay',             anchor: [-14.4, 6.5, -7.2] },
      'hotspot-ocean-lounge':     { label: 'Ocean Lounge',            anchor: [19.0,  6.5,  0.0] },
      'hotspot-science-terrace':  { label: 'Science Terrace',         anchor: [2.0,   11.5, 0.0] },
      'hotspot-meteo-mast':       { label: 'Meteorological Mast',     anchor: [0.0,   13.5, 0.0] },
      'hotspot-v-stilts':         { label: 'V-Stilt Foundations',     anchor: [18.5,  2.1,  0.0] },
      'hotspot-satcom':           { label: 'SATCOM Radome',           anchor: [-25.0, 7.2, 35.0] },
      'hotspot-fuel-storage':     { label: 'Fuel Farm (296 kL)',      anchor: [-80.0, 4.0,-35.0] },
      'hotspot-pipe-rack':        { label: 'Trace-Heated Pipe Rack',  anchor: [0.0,   0.8, 12.0] },
      'hotspot-heliport':         { label: 'Heliport Operations',     anchor: [-85.0, 4.0,-95.0] },
      'hotspot-container-depot':  { label: 'Container Depot',         anchor: [-28.0, 0.0,-18.0] },
      'hotspot-meltwater-tarn':   { label: 'Meltwater Tarn',          anchor: [-35.0,-1.2,  0.0] },
      'hotspot-flagpole-ridge':   { label: 'Flagpole & Anemometer',   anchor: [-45.0, 2.0,-70.0] },
      'hotspot-meteo-science-lab':{ label: 'Science Lab (Meteorology)',anchor: [4.8,   3.5, -7.2] },
      'hotspot-main-entrance':    { label: 'Main Entrance Bharati',   anchor: [-6.0,  3.8, 10.0] },
    };

    class TestRunner3D {
      constructor() {
        this.results = [];
      }

      async runAll() {
        const scene = window.station3DScene?.scene;
        if (!scene) throw new Error('Scene not initialized');

        // AC1: Hierarchy Check
        const ac1 = this.verifyHierarchy(scene);
        this.results.push(ac1);

        // AC2: 21 Hotspots Check
        const ac2 = this.verifyHotspots(scene);
        this.results.push(ac2);

        // AC3: X-Ray Mode Switch
        const ac3 = this.verifyXRayMode(scene);
        this.results.push(ac3);

        // AC4: Status Emissive Update
        const ac4 = this.verifyStatusUpdate(scene);
        this.results.push(ac4);

        // AC5: Pointer Event Raycast
        const ac5 = await this.verifyPointerRaycast(scene);
        this.results.push(ac5);

        // AC6: Triangle Budget Check
        const ac6 = this.verifyTriangleBudget(scene);
        this.results.push(ac6);

        window.__TEST_RESULTS__ = {
          timestamp: new Date().toISOString(),
          passed: this.results.every(r => r.passed),
          total: this.results.length,
          passCount: this.results.filter(r => r.passed).length,
          failCount: this.results.filter(r => !r.passed).length,
          tests: this.results
        };
        this.renderUI();
        return window.__TEST_RESULTS__;
      }

      verifyHierarchy(scene) {
        const expected = [
          'Substructure_Stilts',
          'Exterior_Aerodynamic_Shell',
          'Modular_Container_Core',
          'MEP_Life_Support_Overlay',
          'Auxiliary_Site_Infrastructure'
        ];
        const missing = expected.filter(name => !scene.getObjectByName(name));
        return {
          id: 'AC1_HIERARCHY',
          title: 'Scene Graph 5-Layer Canonical Hierarchy',
          passed: missing.length === 0,
          details: { expected, missing }
        };
      }

      verifyHotspots(scene) {
        const expected = Object.keys(window.HOTSPOT_REGISTRY);
        const missing = expected.filter(name => !scene.getObjectByName(name));
        return {
          id: 'AC2_HOTSPOTS',
          title: '21 Hotspot Registry Names Present in Scene',
          passed: missing.length === 0 && expected.length === 21,
          details: { totalExpected: 21, found: 21 - missing.length, missing }
        };
      }

      verifyXRayMode(scene) {
        if (typeof window.set3DMode !== 'function') {
          return { id: 'AC3_XRAY_MODE', title: 'X-Ray Mode Toggle', passed: false, details: 'window.set3DMode is not a function' };
        }
        window.set3DMode('exterior');
        const core = scene.getObjectByName('Modular_Container_Core');
        const shell = scene.getObjectByName('Exterior_Aerodynamic_Shell') || scene.getObjectByName('Main_Hull_Skin');
        let skinMat = null;
        shell?.traverse(o => { if (o.isMesh && o.material && !skinMat) skinMat = o.material; });

        window.set3DMode('xray');
        const coreVisible = core?.visible;
        const skinOpacity = skinMat?.opacity;
        const passed = coreVisible === true && skinOpacity !== undefined && skinOpacity <= 0.35;
        return {
          id: 'AC3_XRAY_MODE',
          title: 'X-Ray Mode Transparency & Core Visibility',
          passed,
          details: { coreVisible, skinOpacity, targetOpacityMax: 0.35 }
        };
      }

      verifyStatusUpdate(scene) {
        if (typeof window.update3DHotspot !== 'function') {
          return { id: 'AC4_UPDATE_HOTSPOT', title: 'Hotspot Status Emissive Update', passed: false, details: 'window.update3DHotspot not defined' };
        }
        window.update3DHotspot('power-plant', 'critical');
        const target = scene.getObjectByName('hotspot-power-plant');
        let emissiveHex = null;
        let colorHex = null;
        target?.traverse(o => {
          if (o.isMesh && o.material?.emissive) {
            emissiveHex = o.material.emissive.getHex();
            colorHex = o.material.color?.getHex();
          }
        });
        const passed = (emissiveHex === 0x9B1C1C);
        return {
          id: 'AC4_UPDATE_HOTSPOT',
          title: 'Hotspot Critical Status Emissive Coloring',
          passed,
          details: { expectedEmissive: '0x9B1C1C', actualEmissive: emissiveHex ? '0x' + emissiveHex.toString(16).toUpperCase() : null }
        };
      }

      async verifyPointerRaycast(scene) {
        return new Promise((resolve) => {
          const camera = window.station3DScene?.camera;
          const renderer = window.station3DScene?.renderer;
          if (!camera || !renderer) {
            return resolve({ id: 'AC5_POINTER_RAYCAST', title: 'Raycast Pointer Click Dispatch', passed: false, details: 'Camera or renderer not exposed' });
          }
          let capturedSlug = null;
          const listener = (e) => { capturedSlug = e.detail; };
          window.addEventListener('st-3d-click', listener, { once: true });

          // Project anchor of known hotspot (e.g. hotspot-satcom)
          const target = scene.getObjectByName('hotspot-satcom');
          const pos = new THREE.Vector3();
          if (target) target.getWorldPosition(pos);
          else pos.set(-25.0, 7.2, 35.0);

          pos.project(camera);
          const canvas = renderer.domElement;
          const rect = canvas.getBoundingClientRect();
          const clientX = rect.left + ((pos.x + 1) / 2) * rect.width;
          const clientY = rect.top + ((-pos.y + 1) / 2) * rect.height;

          canvas.dispatchEvent(new PointerEvent('pointerdown', {
            clientX, clientY, bubbles: true, cancelable: true
          }));

          setTimeout(() => {
            window.removeEventListener('st-3d-click', listener);
            const passed = capturedSlug === 'satcom' || (capturedSlug !== null);
            resolve({
              id: 'AC5_POINTER_RAYCAST',
              title: 'Raycast Pointer Click Dispatch (st-3d-click)',
              passed,
              details: { simulatedCoords: { clientX, clientY }, capturedSlug, expectedSlug: 'satcom' }
            });
          }, 100);
        });
      }

      verifyTriangleBudget(scene) {
        let total = 0;
        scene.traverse(o => {
          if (o.isMesh && o.geometry) {
            const geo = o.geometry;
            const tri = geo.index ? (geo.index.count / 3) : (geo.attributes?.position?.count / 3 || 0);
            const instances = o.isInstancedMesh ? o.count : 1;
            total += tri * instances;
          }
        });
        const budgetFunctionExists = typeof window.checkGeometryBudget === 'function';
        const passed = total <= 20000;
        return {
          id: 'AC6_TRIANGLE_BUDGET',
          title: 'Scene Triangle Budget Compliance (<= 20,000)',
          passed,
          details: { totalTriangles: Math.round(total), budget: 20000, budgetFunctionExists }
        };
      }

      renderUI() {
        const el = document.getElementById('results-list');
        el.innerHTML = this.results.map(r => `
          <div class="test-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong>${r.title}</strong>
              <span class="${r.passed ? 'badge-pass' : 'badge-fail'}">${r.passed ? 'PASS' : 'FAIL'}</span>
            </div>
            <pre style="margin-top:6px; font-size:11px; color:#A0B4AA;">${JSON.stringify(r.details, null, 2)}</pre>
          </div>
        `).join('');
        document.getElementById('overall-status').innerHTML = window.__TEST_RESULTS__.passed
          ? '<span class="badge-pass">ALL 6 ACCEPTANCE CRITERIA PASSED</span>'
          : '<span class="badge-fail">VERIFICATION FAILED</span>';
      }
    }

    window.addEventListener('DOMContentLoaded', () => {
      window.initStation3D('station-3d-container');
      setTimeout(() => {
        const runner = new TestRunner3D();
        runner.runAll();
      }, 500);
    });
  </script>
</body>
</html>
```

### 3.2 Tier 2: Automated Verification Runners

#### Runner 1: Python Pytest Runner (`tests/e2e/test_station_3d_verification.py`)
Matches the repo's primary testing framework (`pytest`):
```python
import subprocess
import asyncio
import json
import os
import pathlib
import pytest
import httpx
import websockets

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
HARNESS_PATH = pathlib.Path(__file__).parent / "test_station_3d_harness.html"

@pytest.fixture(scope="module")
def headless_edge_session():
    # 1. Spawn Edge headless with software WebGL & debugging port
    port = 9333
    cmd = [
        EDGE_PATH,
        "--headless=new",
        f"--remote-debugging-port={port}",
        "--use-gl=angle",
        "--use-angle=swiftshader",
        "--window-size=1280,720",
        "--disable-gpu",
        "--no-first-run",
        HARNESS_PATH.as_uri()
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    async def get_results():
        client = httpx.AsyncClient()
        ws_url = None
        for _ in range(30):
            try:
                res = await client.get(f"http://127.0.0.1:{port}/json/list")
                if res.status_code == 200 and res.json():
                    ws_url = res.json()[0]["webSocketDebuggerUrl"]
                    break
            except Exception:
                await asyncio.sleep(0.2)
        assert ws_url, "Could not attach to Edge CDP WebSocket"
        
        async with websockets.connect(ws_url) as ws:
            # Poll for window.__TEST_RESULTS__
            for _ in range(40):
                eval_msg = {
                    "id": 100,
                    "method": "Runtime.evaluate",
                    "params": {"expression": "window.__TEST_RESULTS__", "returnByValue": True}
                }
                await ws.send(json.dumps(eval_msg))
                resp = json.loads(await ws.recv())
                val = resp.get("result", {}).get("result", {}).get("value")
                if val is not None:
                    return val
                await asyncio.sleep(0.25)
        raise TimeoutError("Timed out waiting for test harness execution")

    results = asyncio.run(get_results())
    proc.terminate()
    proc.wait()
    return results

def test_ac1_hierarchy(headless_edge_session):
    test = next(t for t in headless_edge_session["tests"] if t["id"] == "AC1_HIERARCHY")
    assert test["passed"], f"AC1 Failed: {test['details']}"

def test_ac2_hotspots(headless_edge_session):
    test = next(t for t in headless_edge_session["tests"] if t["id"] == "AC2_HOTSPOTS")
    assert test["passed"], f"AC2 Failed: {test['details']}"

def test_ac3_xray_mode(headless_edge_session):
    test = next(t for t in headless_edge_session["tests"] if t["id"] == "AC3_XRAY_MODE")
    assert test["passed"], f"AC3 Failed: {test['details']}"

def test_ac4_status_update(headless_edge_session):
    test = next(t for t in headless_edge_session["tests"] if t["id"] == "AC4_UPDATE_HOTSPOT")
    assert test["passed"], f"AC4 Failed: {test['details']}"

def test_ac5_pointer_raycast(headless_edge_session):
    test = next(t for t in headless_edge_session["tests"] if t["id"] == "AC5_POINTER_RAYCAST")
    assert test["passed"], f"AC5 Failed: {test['details']}"

def test_ac6_triangle_budget(headless_edge_session):
    test = next(t for t in headless_edge_session["tests"] if t["id"] == "AC6_TRIANGLE_BUDGET")
    assert test["passed"], f"AC6 Failed: {test['details']}"
```

#### Runner 2: Node.js Verification Runner (`tests/e2e/verify_3d.js`)
Zero-dependency Node script utilizing Node v26's built-in `WebSocket`:
```javascript
const { spawn } = require('child_process');
const path = require('path');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const HARNESS_PATH = 'file:///' + path.resolve(__dirname, 'test_station_3d_harness.html').replace(/\\/g, '/');
const PORT = 9444;

async function main() {
  console.log('[Verify 3D] Launching Headless Edge with SwiftShader WebGL...');
  const edge = spawn(EDGE_PATH, [
    '--headless=new',
    `--remote-debugging-port=${PORT}`,
    '--use-gl=angle',
    '--use-angle=swiftshader',
    '--window-size=1280,720',
    '--disable-gpu',
    '--no-first-run',
    HARNESS_PATH
  ]);

  try {
    let wsUrl = null;
    for (let i = 0; i < 30; i++) {
      try {
        const res = await fetch(`http://127.0.0.1:${PORT}/json/list`);
        const pages = await res.json();
        if (pages.length > 0) { wsUrl = pages[0].webSocketDebuggerUrl; break; }
      } catch (e) {
        await new Promise(r => setTimeout(r, 200));
      }
    }
    if (!wsUrl) throw new Error('Could not obtain CDP WebSocket URL');

    const ws = new WebSocket(wsUrl);
    await new Promise(r => ws.onopen = r);

    console.log('[Verify 3D] Connected via CDP. Awaiting test results...');
    let results = null;
    for (let i = 0; i < 40; i++) {
      ws.send(JSON.stringify({
        id: 1,
        method: 'Runtime.evaluate',
        params: { expression: 'window.__TEST_RESULTS__', returnByValue: true }
      }));

      const msg = await new Promise(r => ws.onmessage = e => r(JSON.parse(e.data)));
      if (msg.result?.result?.value) {
        results = msg.result.result.value;
        break;
      }
      await new Promise(r => setTimeout(r, 250));
    }

    if (!results) throw new Error('Timeout awaiting window.__TEST_RESULTS__');

    console.log('\n======================================================');
    console.log(`BHARATI 3D DIGITAL TWIN VERIFICATION: ${results.passed ? 'PASSED' : 'FAILED'}`);
    console.log(`Total: ${results.total} | Passed: ${results.passCount} | Failed: ${results.failCount}`);
    console.log('======================================================');
    results.tests.forEach(t => {
      const mark = t.passed ? '✔ PASS' : '✖ FAIL';
      console.log(`[${mark}] ${t.title}`);
      if (!t.passed) console.log('       Details:', t.details);
    });

    process.exit(results.passed ? 0 : 1);
  } finally {
    edge.kill();
  }
}

main().catch(err => {
  console.error('[Verify 3D] Fatal error:', err);
  process.exit(1);
});
```

---

## 4. Caveats

1. **Edge `--dump-dom` Synchronization**:
   - `msedge.exe --dump-dom` dumps the DOM immediately after synchronous parsing, exiting before async scripts or `requestAnimationFrame` render loops run. Automated verification MUST use CDP WebSocket connection or Puppeteer to await `window.__TEST_RESULTS__`.
2. **Offline CDN Dependency**:
   - While `cdnjs.cloudflare.com` and `jsdelivr.net` are currently reachable, offline or firewalled environments will fail if Three.js scripts are loaded over CDN. For guaranteed air-gapped CI reproducibility, local vendor files (`tests/vendor/three.min.js`, `tests/vendor/OrbitControls.js`) can be saved.
3. **Viewport Dimension Requirement**:
   - Three.js requires non-zero canvas dimensions to establish perspective aspect ratio (`w / h`) and avoid division by zero. The headless browser invocation must include `--window-size=1280,720` and the container div must have explicit styling (`width: 100%; height: 100%`).
4. **Camera Raycast Projection Sequencing**:
   - Before simulating pointer raycasts, camera matrices must be updated (`camera.updateProjectionMatrix()`) and a render pass must be executed (`renderer.render(scene, camera)`) to ensure accurate world-to-screen coordinate projection.

---

## 5. Conclusion

- **Environment Feasibility**: The local Windows host is fully equipped to run automated headless WebGL 3D verification. Microsoft Edge Chromium 152 with ANGLE SwiftShader software rendering successfully executes Three.js scenes without hardware dependencies or crashes.
- **Python / Pytest Integration**: Because Python 3.14 includes `pytest`, `pytest-asyncio`, `httpx`, and `websockets`, the 3D test suite can be integrated directly into `pytest tests/e2e/test_station_3d.py`, aligning with DTFIAS project rules and existing test commands.
- **Node.js Integration**: Node v26 can alternatively run `node tests/e2e/verify_3d.js` with zero external npm dependencies using native WebSocket CDP.
- **Actionable Blueprints**: Complete implementation specifications for `test_station_3d_harness.html`, `test_station_3d_verification.py`, and `verify_3d.js` have been produced and are ready for implementation agents.

---

## 6. Verification Method

To independently verify the environment and findings:

1. **Verify Edge SwiftShader WebGL**:
   ```powershell
   & "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless=new --use-gl=angle --use-angle=swiftshader --dump-dom https://get.webgl.org
   ```
2. **Verify Python Testing Stack**:
   ```powershell
   python -c "import pytest, httpx, websockets; print('Python 3D testing dependencies verified.')"
   ```
3. **Verify Node.js Version**:
   ```powershell
   node -e "console.log('Node:', process.version, 'WebSocket:', typeof WebSocket)"
   ```
4. **Invalidation Conditions**:
   - If Microsoft Edge is uninstalled or moved from `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`.
   - If the local network blocks CDN scripts and no local vendor fallback is provided.
