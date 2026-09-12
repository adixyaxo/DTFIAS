# 3D Modeling Analysis: Structural Steel Framework & MEP BIM Model

> **Source Image:** `images/bharati/download (12).webp`  
> **Target Path:** `docs/bharati3d/15_structural_steel_framework_and_mep_bim_model.md`  
> **Classification:** 3D Building Information Modeling (BIM) Axonometric / Engineering Systems  
> **Subject Focus:** Structural Steel Exoskeleton Bents, HVAC Duct Networks, Hydronic Heating Loops & MEP Plant Core

---

## 1. Viewpoint & Perspective Calibration

* **Projection Type:** Axonometric Isometric 3D Wireframe / Solid BIM Render.
* **Camera Angle:** High oblique axonometric elevation (~35° down-angle), looking down from the North-East toward South-West.
* **Aspect Ratio:** Standard 16:9 widescreen engineering diagram.
* **Significance for 3D Modeling:** This is the **authoritative MEP (Mechanical, Electrical, Plumbing) and structural steel framework specification**. It provides the internal routing of life support ducts, heating circuits, and structural bents needed for deep SCADA telemetry inspection.

---

## 2. Engineering Systems & MEP Color Taxonomy

```
    ┌────────────────────────────────────────────────────────────────────────┐
    │  ROOF PENTHOUSE MECHANICAL PLANT ROOM (AHUs & Heat Recovery Units)     │
    │  [Green Fresh Air Supply Ducts]  │  [Yellow Exhaust Return Air Ducts] │
    └──────────────────┬─────────────────────────────┬───────────────────────┘
                       │                             │
    ┌──────────────────▼─────────────────────────────▼───────────────────────┐
    │  STRUCTURAL STEEL PORTAL EXOSKELETON (Deep Blue I-Beams & Girts)       │
    │  • 11 Primary Transverse Bents with Chamfered Aerodynamic Profiles     │
    │  • Longitudinal Floor & Roof Stringers (Grid Spacing ~4.8m)            │
    ├────────────────────────────────────────────────────────────────────────┤
    │  HYDRONIC HEATING & LIFE SUPPORT DISTRIBUTION (Interstitial Plenum)    │
    │  • [Red Pipes]: High-Temp Combined Heat & Power (CHP) Hydronic Loops   │
    │  • [Blue Pipes]: Potable Water & Vacuum Waste Drainage Circuit         │
    │  • [Magenta/Cyan Trays]: 415V 3-Phase Power Busways & Telemetry Fiber  │
    └────────────────────────────────────────────────────────────────────────┘
                       │                             │
    ═══════════════════▼═════════════════════════════▼════════════════════════
    [ FOUNDATION STILTS: CYLINDRICAL PILES WITH DIAGONAL KNEE BRACES ]
```

### 2.1. Structural Steel Exoskeleton (Deep Blue `#2B3A8C`)
* **11 Transverse Portal Bents:**
  * The outer spaceframe consists of **11 primary welded structural steel portal bents** spaced evenly along the 50.0m hull at ~4.8m intervals.
  * Each bent follows the faceted aerodynamic cross-section:
    * Inward-angled lower leg forming the underbelly chamfer.
    * Vertical side girt supporting the window lintel and sill.
    * Inward-angled upper rafter forming the roof chamfer.
* **External Staircase Integration:**
  * The galvanized steel stair stringer is rigidly bolted to Portal Bent #4 on the northern facade, featuring 18 open-grate steps leading to the main Level 1 entry landing.

### 2.2. HVAC Air Handling & Ventilation Systems
* **Supply Air Ducts (Vibrant Green `#27AE60`):**
  * Originates from massive central Air Handling Units (AHUs) located in the central Level 2 penthouse.
  * Drops vertically through central risers and branches longitudinally east and west down the central corridor ceiling plenum, delivering filtered, tempered, and humidified fresh air into each living cabin and lab.
* **Return Air Ducts (Warm Yellow `#F1C40F`):**
  * Parallel return duct network collecting stale air from cabins and laboratories and routing it back to the energy-recovery heat exchangers in the penthouse.

### 2.3. Hydronic Heating & Fluid Networks
* **District Heating Loops (Vibrant Red `#E74C3C`):**
  * Circulates hot water heated by the jacket water and exhaust gas heat exchangers of the 3x Volvo Penta / Scania CHP diesel generators.
  * Runs through insulated underfloor conduits, feeding perimeter convective radiators and air heating coils to maintain +21°C interior comfort against -40°C polar exterior conditions.
* **Domestic Water & Greywater Lines (Blue `#2980B9`):**
  * Trace-heated piping carrying fresh water melted from the snow melter tank and routing wastewater to the Membrane Bioreactor (MBR) treatment plant.

---

## 3. Quantitative 3D Modeling Metrics

| Engineering Element | Cross-Section / Diameter | Three.js World Units (1u = 1m) | Notes |
|:---|:---|:---|:---|
| **Structural Steel Columns/Beams**| Heavy W-Shape / I-Beam 400mm | Box / Extruded profile | Blue structural steel |
| **Main HVAC Supply Trunk Duct** | 0.8m W × 0.5m H rectangular | `width: 0.8, height: 0.5` | Green ductwork in plenum |
| **Secondary Branch Ducts** | 0.4m diameter round spiratube| `radius: 0.2` | Feeds into cabins |
| **Primary Hydronic Heating Pipe** | 100mm nominal bore insulated | `radius: 0.05` | Red high-temp loop |
| **Domestic Water Service Pipe** | 50mm nominal bore insulated | `radius: 0.025` | Blue potable water loop |
| **Portal Bent Spacing** | 11 bents at 4.8m spacing | Repeat along X-axis | Total span: 48.0m |

---

## 4. Materials & Shader Palette for MEP Telemetry Modes

```
Hex Color Reference:
Structural Steel Frame:     #2B3A8C  (Industrial structural cobalt blue)
HVAC Fresh Air Supply:      #27AE60  (Vibrant environmental green)
HVAC Return / Exhaust Air:  #F1C40F  (Warm warning yellow)
Hydronic Heating (Supply):  #E74C3C  (High-temperature district heat red)
Hydronic Heating (Return):  #C0392B  (Lower temperature return burgundy)
Potable Domestic Water:     #2980B9  (Cold water supply royal blue)
Electrical Power Busway:    #8E44AD  (High-voltage 415V busway purple)
Instrumentation & Fiber:    #16A085  (SCADA telemetry cable teal)
```

---

## 5. Three.js Interactive SCADA "System Overlay" Architecture

This BIM model directly informs the implementation of the **subsystem overlay toggles** on the DTFIAS dashboard (e.g. `viewToggleHvac`, `viewToggleThermal`, `viewToggleSchematic`):

```javascript
// MEP Subsystem Layer Groups
const MEPGroup = new THREE.Group();

const structuralFrameMesh = new THREE.Mesh(steelBeamsGeo, blueSteelMat);
const hvacSupplyMesh = new THREE.Mesh(greenDuctsGeo, greenHvacMat);
const hvacReturnMesh = new THREE.Mesh(yellowDuctsGeo, yellowHvacMat);
const hydronicHeatingMesh = new THREE.Mesh(redPipesGeo, redHeatingMat);
const domesticWaterMesh = new THREE.Mesh(bluePipesGeo, blueWaterMat);

MEPGroup.add(structuralFrameMesh, hvacSupplyMesh, hvacReturnMesh, hydronicHeatingMesh, domesticWaterMesh);

// Toggle Layer Visibility via SCADA Dashboard Controls
function setMEPOverlay(systemName, isVisible) {
  if (systemName === 'hvac') {
    hvacSupplyMesh.visible = isVisible;
    hvacReturnMesh.visible = isVisible;
  } else if (systemName === 'heating') {
    hydronicHeatingMesh.visible = isVisible;
  } else if (systemName === 'structural') {
    structuralFrameMesh.visible = isVisible;
  }
}
```

---

## 6. Digital Twin Hotspot & Subsystem Anchors

| Subsystem Anchor | World Coordinate `[x, y, z]` | Description |
|:---|:---|:---|
| **`chp_heat_exchanger_primary`**| `[-6.0, 3.2, 0.0]` | Waste heat recovery loop from diesel gensets. |
| **`ahu_penthouse_central`** | `[0.0, 9.5, 0.0]` | Main air handling and heat recovery ventilation unit. |
| **`hydronic_distribution_manifold`**| `[-2.0, 4.2, 0.0]` | Underfloor district heating supply manifold. |
| **`freshwater_circulation_loop`**| `[4.0, 3.8, 2.0]` | Potable water pressure booster and UV sterilization node. |
| **`mep_service_riser_west`** | `[-12.0, 6.0, 0.0]`| Vertical pipe and cable chase between Level 0 and Level 1. |
