# Handoff Report: Frontend 3D Digital Twin Survey

> **Agent**: `explorer_survey_1`  
> **Role**: Codebase & Frontend Assets Investigation  
> **Target**: Bharati Station 3D Digital Twin Assets, Libraries, Templates & Constraints  
> **Date**: 2026-09-12  

---

## 1. Observation

### 1.1 Files in `app/static/js/three/`
- Directory path: `app/static/js/three/`
- Contents: Exactly **one** file exists:
  - `app/static/js/three/station_3d_view.js` (18,730 bytes, 480 lines).
- There are **no other files** or vendor libraries in `app/static/js/three/`.

#### Analysis of existing `station_3d_view.js`
- **Global Entry Point**: Defines `window.initStation3D(containerId)` (lines 5–10). Clears container and injects WebGL canvas.
- **Scene & Fog**:
  - `scene.background = new THREE.Color(0x0B1C18)` (matches `--bg-deep`, line 16).
  - `scene.fog = new THREE.FogExp2(0x0B1C18, 0.004)` (line 18).
- **Camera & Perspective**:
  - `new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 1, 1000)` positioned at `(120, 90, 160)` (lines 20–21).
- **Controls Conditional Check**:
  - Lines 32–40:
    ```javascript
    let orbitControls = null;
    if (typeof THREE.OrbitControls !== 'undefined') {
        orbitControls = new THREE.OrbitControls(camera, renderer.domElement);
        orbitControls.enableDamping = true;
        orbitControls.dampingFactor = 0.05;
        orbitControls.maxPolarAngle = Math.PI / 2 - 0.05; // don't go below ground
        orbitControls.target.set(0, 10, 0);
    } else {
        camera.lookAt(0, 10, 0);
    }
    ```
- **Hotspot IDs Implemented in Existing Geometry**:
  1. `hotspot-main_building` (line 183): Beveled extruded geometry (`ExtrudeGeometry`, 80m × 30m × 14m) elevated on stilts.
  2. `hotspot-hvac` (line 205): Group containing 4 rooftop box meshes.
  3. `hotspot-comms_satcom` (line 217): Group containing 2 hemispherical radomes (`SphereGeometry`).
  4. `hotspot-environment_sensors` (line 230): Cylindrical mast mesh on roof.
  5. `hotspot-fuel_storage` (line 240): Group of 13 cylindrical fuel tanks in a 3×5 grid.
  6. `hotspot-heliport` (line 258): Cylindrical landing pad with ring and 'H' marking geometry.
- **Particle System**: 3,000 particles with drift velocities simulating an Antarctic blizzard blowing underneath the station (lines 285–312).
- **Raycasting & Event Dispatching**:
  - Pointermove and pointerdown handlers registered on `container` (lines 320–389).
  - Raycaster filters children whose names start with `hotspot-`.
  - Dispatches event to DOM on click:
    `window.dispatchEvent(new CustomEvent('st-3d-click', { detail: assetId }));` (line 386).
- **State Bridge**:
  - Defines `window.update3DHotspot(assetId, status)` (lines 392–425) modifying `emissive` and `color` (`critical`: `#C44536`, `warning`: `#D9822B`, normal: `#1A312C`).
- **Exported Global State**:
  - `window.station3DScene = { scene, group: stationGroup };` (line 477).

---

### 1.2 Three.js Loading in Templates
#### `app/templates/layouts/base.html`
- Lines 134–140:
  ```html
  <!-- Mandatory Vendor Stack (C17) -->
  <script src="/static/vendor/htmx.min.js"></script>
  <script src="/static/vendor/htmx-ext-sse.js"></script>
  <script src="/static/vendor/alpine.min.js" defer></script>
  <script src="/static/vendor/apexcharts.min.js"></script>
  <link href="/static/css/app.css" rel="stylesheet">
  <!-- Tailwind CSS (CDN) -->
  <script src="https://cdn.tailwindcss.com"></script>
  ```
- **Zero Three.js scripts** exist in `base.html`. Confirmed 100% compliant with constraint C16.

#### `app/templates/bharati/station_twin.html`
- Line 92:
  ```html
  <!-- ─── 3D Station Hologram (Lazy-Loaded) ─── -->
  <div id="station-3d-container" class="absolute inset-0 w-full h-full" x-show="show3D" x-cloak>
     <!-- Three.js renderer will be injected here by station_3d_view.js -->
  </div>
  ```
- Line 60:
  ```html
  <button class="..." @click="toggle3D()" :aria-pressed="show3D" aria-label="Toggle 3D View">
    <span class="material-symbols-outlined text-[18px]">view_in_ar</span>
    <span x-text="show3D ? '2.5D View' : '3D View'"></span>
  </button>
  ```
- **Observation**: `station_twin.html` does **not** contain an inline `x-init` attribute on `<div id="station-3d-container">`. Instead, script injection is deferred until the user clicks the "3D View" button via `toggle3D()` in `app/static/js/station_twin.js`.

#### Dynamic Injection in `app/static/js/station_twin.js`
- Lines 418–435:
  ```javascript
  toggle3D() {
    this.show3D = !this.show3D;
    if (this.show3D && !window.THREE) {
      // Lazy load Three.js first
      const threeScript = document.createElement('script');
      threeScript.src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js";
      threeScript.onload = () => {
          // Then load our 3D view script
          const appScript = document.createElement('script');
          appScript.src = "/static/js/three/station_3d_view.js";
          appScript.onload = () => {
              window.initStation3D('station-3d-container');
          };
          document.body.appendChild(appScript);
      };
      document.body.appendChild(threeScript);
    }
  },
  ```

---

### 1.3 Vendor & CDN Libraries Availability
#### Local Vendor Directory (`app/static/vendor/`)
- Directory listing of `app/static/vendor/`:
  - `alpine.min.js` (44,758 bytes)
  - `apexcharts.min.js` (539,664 bytes)
  - `htmx-ext-sse.js` (8,896 bytes)
  - `htmx.min.js` (42,042 bytes)
- **Result**: No Three.js library or OrbitControls file is present in `app/static/vendor/`.

#### CDN References
- Three.js library version: **Three.js r128** from CDN:
  `https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`
- **OrbitControls**: **NOT loaded anywhere**.
  - `station_twin.js` does not create any script tag for OrbitControls.
  - As a direct consequence, `typeof THREE.OrbitControls` evaluates to `'undefined'` at runtime, leaving `orbitControls = null` in `station_3d_view.js`. Camera orbit/pan/zoom is currently inactive.

---

### 1.4 Verification of GEMINI.md Constraints

| Constraint Code | Specification | Observed Status | Evidence |
|:---|:---|:---|:---|
| **C13** | Supabase service-role key: backend env vars only. Never in `app/static/` or `app/templates/`. | **PASSED** | `grep -r "SUPABASE_SERVICE_ROLE_KEY" app/static/ app/templates/` → 0 matches. |
| **C14** | Supabase Realtime: server-side only. No `supabase-js` Realtime in browser. | **PASSED** | `grep -rE "(supabase-js\|createClient\()" app/static/ app/templates/` → 0 matches. |
| **C16** | Three.js/`station_3d_view.js`: lazy-loaded only. Never in `layouts/base.html` unconditional scripts. | **PASSED** | `layouts/base.html` contains no Three.js scripts. `tests/e2e/test_frontend_comprehensive.py` confirms absence in rendered base dashboard & twin routes. |
| **C17** | Bundler-free runtime: Tailwind via CDN `<script src="https://cdn.tailwindcss.com">`. No npm build pipeline required. | **PASSED** | All mandatory scripts loaded directly in browser. No webpack, vite, or bundler dependency required to render. |

---

## 2. Logic Chain

1. **Premise**: `station_3d_view.js` requires `THREE.OrbitControls` to support interactive rotation and panning, as explicitly coded in lines 32–40:
   `if (typeof THREE.OrbitControls !== 'undefined') { orbitControls = new THREE.OrbitControls(camera, renderer.domElement); ... }`
2. **Observation**: In `station_twin.js:toggle3D()`, only `three.min.js` is loaded prior to `station_3d_view.js`. OrbitControls is neither loaded from CDN nor vendored in `app/static/vendor/`.
3. **Deduction**: In the current application, `THREE.OrbitControls` is permanently `undefined`. The camera is locked to a static angle (`camera.lookAt(0, 10, 0)`), preventing user interaction.
4. **Recommendation**: To enable camera orbiting while adhering to C16 and C17, `station_twin.js` must inject the r128 OrbitControls companion script (e.g. `https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/controls/OrbitControls.min.js`) sequentially after `three.min.js` and before `station_3d_view.js`, or bundle it into `app/static/vendor/three/`.

5. **Premise**: GEMINI.md Section 7 states:
   `<div id="station-3d-container" x-data x-init="const s = document.createElement('script'); s.src = '/static/js/three/station_3d_view.js'; s.onload = () => initStation3D('station-3d-container'); document.body.appendChild(s);"></div>`
6. **Observation**: `bharati/station_twin.html` currently uses a button toggle (`toggle3D()`) to show/hide the 3D twin, keeping the 2.5D SVG twin as default.
7. **Deduction**: While deferring Three.js until button click is compliant with C16 (since it is lazy-loaded and absent from `base.html`), an automated test or headless verification script loading `station_twin.html` without clicking "3D View" will find an empty `#station-3d-container`.
8. **Recommendation**: Automated tests verifying 3D initialization must either trigger the `toggle3D()` method or provide a standalone test harness page (`tests/3d_harness.html` or similar).

9. **Premise**: The architectural master specification (`docs/bharati3d/00_bharati_3d_master_specification.md`, `05-subagent_synthesis.md`, `06-subagent_implementation_plan.md`) mandates 21 distinct `hotspot-*` IDs, 7 SCADA rendering modes via `window.set3DMode(mode)`, and precise extruded P1-P11 profiles.
10. **Observation**: The existing `station_3d_view.js` contains a working MVP prototype with only 6 hotspots (`hotspot-main_building`, `hotspot-hvac`, `hotspot-comms_satcom`, `hotspot-environment_sensors`, `hotspot-fuel_storage`, `hotspot-heliport`) and 0 mode controls.
11. **Deduction**: The existing `station_3d_view.js` represents a functional baseline prototype, but needs a complete architectural upgrade to satisfy the full requirements of the Bharati 3D implementation plan.

---

## 3. Caveats

1. **No Headless WebGL Environment Executed**: During this survey, WebGL shader execution and framerate performance were not evaluated in a live headless browser (e.g. Puppeteer with swiftshader/angle).
2. **Network Dependency for CDN**: Because Three.js r128 is loaded from `cdnjs.cloudflare.com`, environments without internet connectivity will fail to load the 3D twin unless local vendor copies (`app/static/vendor/three/`) are provided.

---

## 4. Conclusion

1. **Repository Layout & Purity**: The frontend architecture conforms strictly to GEMINI.md constraints (C13, C14, C16, C17). No service keys or browser Supabase clients exist. Three.js is completely absent from `base.html`.
2. **Existing Implementation Status**: `app/static/js/three/station_3d_view.js` is a functioning 480-line prototype featuring basic procedural geometries, 6 hotspots, raycasting, status recoloring via `window.update3DHotspot`, and blizzard particles.
3. **Critical Missing Dependency**: OrbitControls is NOT loaded. Adding `https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/controls/OrbitControls.min.js` to the dynamic loading chain in `station_twin.js` (or local vendoring) is necessary for user camera rotation.
4. **Path to Full Master Specification**: To reach the target state defined in `docs/bharati3d/06-subagent_implementation_plan.md`, `station_3d_view.js` must be expanded from 6 to 21 hotspots, implement the 7 rendering modes via `window.set3DMode`, construct the extruded P1-P11 aerodynamic shell and quad cantilever V-stilts, and integrate the MEP SCADA overlays.

---

## 5. Verification Method

### 5.1 Static Verification Commands
Run the following commands in powershell from the project root:

```powershell
# 1. Verify C13 (Zero Supabase service keys in frontend)
grep -r "SUPABASE_SERVICE_ROLE_KEY" app/static/ app/templates/
# Expected output: zero matches

# 2. Verify C14 (Zero browser Supabase clients)
grep -rE "(supabase-js|createClient\()" app/static/ app/templates/
# Expected output: zero matches

# 3. Verify C16 (Three.js absent from base.html)
grep -i "three" app/templates/layouts/base.html
# Expected output: zero matches

# 4. Verify existing hotspots in station_3d_view.js
grep -oE "hotspot-[a-zA-Z0-9_-]+" app/static/js/three/station_3d_view.js | sort -u
# Expected output:
# hotspot-comms_satcom
# hotspot-environment_sensors
# hotspot-fuel_storage
# hotspot-heliport
# hotspot-hvac
# hotspot-main_building
```

### 5.2 Automated Test Suite
Run the frontend comprehensive test suite:
```powershell
pytest tests/e2e/test_frontend_comprehensive.py -k "test_threejs_lazy_loading_c16"
```
Verification passes if `test_threejs_lazy_loading_c16` succeeds, confirming that Three.js is not present in initial HTML waterfalls and `station-3d-container` is present in the station twin template.

### 5.3 Invalidation Conditions
This report's conclusions are invalidated if:
- Any script tag for Three.js is added to `app/templates/layouts/base.html`.
- The loading URL in `station_twin.js` is switched to an incompatible Three.js major version without testing.
