# 3D Modeling Analysis: Northwest Oblique & Container Depot

> **Source Image:** `images/bharati/download (6).webp`  
> **Target Path:** `docs/bharati3d/09_northwest_oblique_and_container_depot.md`  
> **Classification:** Oblique Architectural Perspective & Staging Yard Layout  
> **Subject Focus:** Northern Seaward Facade, Rear Service Doors, Stilt Forest, External Stairs & ISO Container Staging

---

## 1. Viewpoint & Perspective Calibration

* **Projection Type:** Eye-Level Telephoto Perspective (~85mm focal length).
* **Camera Position:** Stationed on the rocky slope northwest of the meltwater tarn (~90m from the station), looking Southeast toward the rear entrance and north-facing seaward facade.
* **Aspect Ratio:** Standard 3:2 landscape photograph.
* **Lighting:** Bright, direct sub-zero Antarctic summer sunlight illuminating the northern facade and casting crisp geometric shadow planes along the western bevels.

---

## 2. Architectural & Site Engineering Breakdown

```
                            [ ROOF PENTHOUSE & ANTENNA MAST ]
                            ┌──────────────────────────────┐
                            │ 4x Exhausts  |  Meteo Masts  │
    ┌───────────────────────┴──────────────────────────────┴────────────────────────┐
    │                         NORTHERN ROOF BEVEL / HIPPED SKIN                     │
    ├───────────────────────────────────────────────────────┬───────────────────────┤
    │  [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]  │  [|][|][|][|][|][|]   │ (Rear Windows)
    │  16-BAY NORTHERN LONGITUDINAL WINDOW RIBBON          │  6-Bay Corridor Glass │
    ├───────────────────────────────────────────────────────┴───────────────────────┤
    │                         INWARD SLOPING FACADE BEVEL                           │
    ├───────────────────────────────────────┬───────────────────────────────────────┤
    │                                       │   [||||] Main Vehicle Shutter Door    │
    │   [ EXTERIOR STEEL ACCESS STAIRS ]    │   [ o ]  Personnel Airlock Door       │
    └───────────────────┬───────────────────┴───────────────────┬───────────────────┘
                        │                                       │
        [ STILT FOREST: CYLINDRICAL PILES ]         [ STILT FOREST: GROUND PADS ]
```

### 2.1. Dual Facade Geometry (North & West Convergence)
* **Corner Bevel Transition:** Highlights the continuous, wrap-around chamfered skin:
  * The vertical corners are not sharp 90° right angles; they feature a distinct **45° planar chamfer bevel (~1.2m wide)**, smoothing aerodynamic drag during severe polar blizzards.
* **Northern Longitudinal Window Ribbon:**
  * Displays the complete 16-bay window strip running the full length of the northern accommodation/laboratory wing (~42m continuous glass ribbon).
  * Recessed ~0.15m beneath the outer insulated aluminum cladding panel.
* **Rear Ground Utility Entrances:**
  * **Motorized Cargo Shutter:** Centered on the western ground floor (~4.5m W × 3.5m H) in matte industrial gray.
  * **Personnel Airlock Entry Door:** Positioned immediately to the right of the garage door (~1.2m W × 2.2m H) with a maritime porthole circular inspection window.

### 2.2. Substructure "Stilt Forest" Geometry
* **Column Distribution:**
  * Unlike the front prow (which uses angled V-stilts), the northern cantilever and central hull are supported by a dense grid of **vertical cylindrical structural steel columns**.
  * Column Diameter: ~0.40m.
  * Clear spacing between transverse column rows: ~4.8m.
* **External Access Staircase:**
  * An open-grate galvanized steel industrial staircase with handrails ascending from the bedrock terrace up to an exterior access airlock door on Level 1.
  * Flight angle: ~35°, width: ~1.2m.

### 2.3. Container Depot & External Staging Area
* **Container Inventory (Color/Branding Reference):**
  * **Hapag-Lloyd Orange:** 40ft high-cube containers (`#E85D04`).
  * **Evergreen Green:** 40ft standard dry container (`#008751`).
  * **Marine Red / Cor-Ten:** 20ft equipment modules (`#A63A2A`).
  * **Deep Maritime Blue:** 20ft storage units with white stencil markings (`#0B4F6C`).
* **Placement Cadence:** Positioned strategically around the crushed-rock apron to the north and west of the station, outside the wind-scour zone.

---

## 3. Quantitative 3D Metrics & Proportions

| Element | Real-World Dimension | Three.js World Units (1u = 1m) | Notes |
|:---|:---|:---|:---|
| **Northern Window Strip Length** | ~42.0m | `length: 42.0, height: 1.2` | 16 discrete window modules |
| **Corner Chamfer Bevel Width** | ~1.2m face width | 45° angle bevel | Seamless corner transition |
| **External Steel Staircase** | Rise: 3.5m, Run: 5.0m | Slope: ~35° | With 1.1m safety handrails |
| **Main Cargo Roll-Up Door** | 4.5m W × 3.5m H | `width: 4.5, height: 3.5` | Segmented steel slats |
| **Personnel Porthole Door** | 1.2m W × 2.2m H | `width: 1.2, height: 2.2` | Porthole diameter: 0.35m |
| **Standard 20ft ISO Container** | 6.06m L × 2.44m W × 2.59m H | `x: 6.06, y: 2.59, z: 2.44` | Instanced logistics assets |
| **Standard 40ft ISO Container** | 12.19m L × 2.44m W × 2.89m H | `x: 12.19, y: 2.89, z: 2.44`| High-cube variant |

---

## 4. Materials, PBR Shaders & Color Palette

```
Hex Color Reference:
Northern Aluminum Facade:   #B8C4C7  (High-reflectivity silver-gray under direct sun)
Window Inset Shadow:        #1A2426  (Dark contrast window frame cavity)
Hapag-Lloyd Container:      #E85D04  (Industrial logistics orange)
Evergreen Container:        #008751  (Marine freight dark green)
Textainer / Maritime Blue:  #0B4F6C  (Deep industrial cyan-blue)
Cor-Ten Rust Container:     #8C3828  (Weathered oxidized marine steel)
Galvanized Steel Stairs:    #CFD8DC  (Zinc-dipped open bar grating)
Granite Gravel Pad:         #9E8668  (Crushed Larsemann gneiss apron)
```

* **Aluminum Skin Shader (Direct Polar Sun):**
  * Base Color: `#B8C4C7`
  * Metalness: `0.80`
  * Roughness: `0.28` (sharp specular response displaying the crisp horizon reflection).
* **ISO Container Instanced Material:**
  * Multi-material array supporting random albedo tints (`#E85D04`, `#008751`, `#0B4F6C`, `#8C3828`) to populate the depot procedurally with minimal GPU draw calls.

---

## 5. Three.js Implementation Guidance

### 5.1. Procedural Container Yard Spawner
```javascript
// Instanced mesh for efficient container depot rendering
const containerGeo = new THREE.BoxGeometry(6.06, 2.59, 2.44);
const containerMat = new THREE.MeshStandardMaterial({ roughness: 0.65, metalness: 0.25 });
const containerInstancedMesh = new THREE.InstancedMesh(containerGeo, containerMat, 25);

// Set instance transforms and colors dynamically
const colors = [0xE85D04, 0x008751, 0x0B4F6C, 0x8C3828];
const dummy = new THREE.Object3D();
// ... populate positions matching the northwest gravel apron
```

### 5.2. Digital Twin Hotspot Anchors
* **`personnel_airlock_entrance`** `[-18.0, 3.5, -9.5]`: External stairway personnel muster and badge access point.
* **`logistics_shutter_bay`** `[-20.0, 1.8, 0.0]`: Ground mechanical cargo intake and vehicle deployment.
* **`container_depot_northwest`** `[-28.0, 0.0, -18.0]`: Active inventory tracking and supply logistics ledger.
* **`north_lab_ribbon`** `[0.0, 5.2, -10.0]`: Atmospheric science laboratory telemetry node.
