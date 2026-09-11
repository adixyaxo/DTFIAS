# Bharati Station 3D Digital Twin — Implementation Plan

## 1. Architectural Analysis of Bharati Station

Based on real-world architectural data (bof Architekten / IMS), Bharati Station is a highly distinct, modern, and modular facility designed for extreme Antarctic conditions:

*   **Structure:** Constructed from **134 prefabricated shipping containers** assembled on-site.
*   **Form Factor:** The entire container assembly is wrapped in an aerodynamic, insulated aluminum skin to withstand 200 mph winds and -40°C temperatures.
*   **Elevation:** Built on steel stilts/columns to allow wind to blow underneath, preventing snowdrifts from burying the station and protecting the permafrost.
*   **Levels (3 Main Floors):**
    *   *Ground Floor:* Technical and operational spaces (laboratories, workshops, 3x MAN CHP generators, storage).
    *   *Second Floor:* Living quarters (24 single/double rooms), kitchen, dining, lounge, medical bay, fitness room. Features a massive panoramic glazed window on the north side.
    *   *Third Level (Roof):* Terrace for scientific observation, weather masts, and HVAC exhaust.
*   **External Assets:**
    *   *Fuel Farm:* 13x Jet A-1 tanks (~296 kL).
    *   *Seawater Intake:* 300m trace-heated pipeline stretching to Quilty Bay.
    *   *Helipad:* Elevated landing pad for aerial logistics.
    *   *SATCOM:* C-band satellite radome.

---

## 2. 3D Frontend Strategy & Constraints (C16)

The 3D model will serve as a high-fidelity interactive dashboard for the DTFIAS frontend. 
**Crucially, it must adhere to project constraint C16:** *Three.js (`station_3d_view.js`) must be lazy-loaded only, triggered by Alpine.js `x-init`, and never included in `layouts/base.html` as an unconditional script.*

### Tech Stack
*   **Renderer:** Three.js (WebGL)
*   **Model Format:** GLTF/GLB (optimized, low-poly, compressed) or programmatic Three.js geometries for minimal bundle size.
*   **Interactivity:** Three.js `Raycaster` for clicking 3D hotspots.
*   **State Management:** Alpine.js (syncing telemetry to the 3D scene).

---

## 3. Implementation Phases

### Phase 1: 3D Asset Generation & Optimization
Instead of a hyper-realistic heavy model, we will use a **minimalist, aesthetic "clay" or "wireframe-hologram" SCADA style** to match the dark Antarctic UI.

1.  **Main Building Mesh:**
    *   Model the aerodynamic outer shell (smooth, curved edges).
    *   Add the large panoramic window on the second floor with an emissive glowing material (`var(--brand-mint)`).
    *   Elevate the structure on cylindrical stilts.
2.  **External Asset Meshes:**
    *   Create 13 cylindrical fuel tanks.
    *   Create the helipad platform.
    *   Create the SATCOM dome.
3.  **Optimization:** Export as a single compressed `bharati_base.glb` file (< 2MB).

### Phase 2: Lazy-Loaded Three.js Infrastructure
Create `app/static/js/three/station_3d_view.js`.

```javascript
// Example Lazy-Load Pattern (Alpine.js)
// <div id="station-3d-container" x-data x-init="
//   const s = document.createElement('script');
//   s.src = '/static/js/three/station_3d_view.js';
//   s.onload = () => initStation3D('station-3d-container');
//   document.body.appendChild(s);
// "></div>
```

*   **Scene Setup:** Isometric orthographic camera or restricted perspective camera. Dark background matching `--bg-deep` (`#0B1C18`).
*   **Lighting:** Subtle ambient light + emissive materials for status indicators. No heavy dynamic shadows to ensure 60fps on low-end edge devices.

### Phase 3: Hotspots & Raycasting
Implement interactive 3D markers hovering over key subsystems.

*   **Subsystem Mapping:**
    *   `power_plant` (Ground floor west)
    *   `fuel_storage` (Exterior west)
    *   `seawater_intake` (Exterior pipeline)
    *   `hvac` (Roof / Third level)
    *   `medical_bay` (Second floor east)
*   **Visual Feedback:** 
    *   Normal (P2): Subtle pulse, `var(--status-ok-dark)`.
    *   Warning (P1): Solid `var(--status-warning-dark)`.
    *   Critical (P0): Aggressive strobe, `var(--status-critical-dark)`.

### Phase 4: Alpine.js / Telemetry Synchronization
Expose a global bridge function so the Alpine.js telemetry ticker (`stationTwin()`) can push state changes into the Three.js scene.

```javascript
// Bridge example
window.update3DHotspot = function(assetId, status, value) {
    if (window.station3DScene) {
        window.station3DScene.setHotspotColor(assetId, status);
    }
}
```
When a simulated fault occurs (e.g., SATCOM offline), the 3D SATCOM dome will instantly flash red and emit a particle effect or warning ring.

---

## 4. Definition of Done
- [ ] 3D container component created in `app/templates/bharati/`.
- [ ] `station_3d_view.js` dynamically injected via Alpine `x-init` (C16 Compliance).
- [ ] GLB model loads asynchronously with a loading spinner.
- [ ] Model accurately reflects the 134-container aerodynamic stilt architecture.
- [ ] Raycaster successfully detects clicks on 3D hotspots, opening the existing `asset_drawer.html` UI.
- [ ] Changing telemetry in Alpine.js instantly recolors the 3D meshes without dropping frames.
