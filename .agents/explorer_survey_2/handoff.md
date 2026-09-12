# Bharati Station 3D Digital Twin — Architectural & Geometric Specifications

> **Author:** Explorer Survey 2 (`explorer_survey_2`)  
> **Source Documents:** `docs/bharati3d/00` through `docs/bharati3d/22` (specifically `05-subagent_synthesis.md`, `06-subagent_implementation_plan.md`, `17_front_prow_cad_elevation_and_datums.md`, `11_cantilever_v_stilts_and_underbelly_aerodynamics.md`, `15_structural_steel_framework_and_mep_bim_model.md`, `16_container_cluster_and_exoskeleton_frame_integration.md`)  
> **Target File:** `app/static/js/three/station_3d_view.js`  
> **Date:** 2026-09-12  

---

## 1. Observation

### 1.1 Source Documents Inspected
Direct inspection of the authoritative documentation in `docs/bharati3d/` reveals:
1. `docs/bharati3d/05-subagent_synthesis.md` lines 18–42: Defines the principal bounding box (`50.0m L × 20.0m W × 11.58m H`), vertical datums (`Y=0.0m` bedrock, `Y=+1.834m` keel, `Y=+2.596m` H1 Level 0 stilt bearing, `Y=+5.103m` H2 Level 1 finished floor, `Y=+8.948m` H3 roof deck fascia, `Y=+11.580m` H4 penthouse apex, `Y=+13.500m` meteo mast apex), and transverse profile vertices P1–P6.
2. `docs/bharati3d/17_front_prow_cad_elevation_and_datums.md` lines 63–80 (§3): Sets out the complete 11-vertex transverse hull profile table (`P1` through `P11`) with exact local coordinates.
3. `docs/bharati3d/11_cantilever_v_stilts_and_underbelly_aerodynamics.md` lines 44–85, 114–143: Details the 4 fabricated box-section V-stilts (outer spread `±8.75m`, inner spread `±4.80m`, height `4.2m`, incline `22°`, 4-segment tapered box sections) with the procedural generator `createVStiltBent()`.
4. `docs/bharati3d/06-subagent_implementation_plan.md` lines 308–365, 583–606: Specifies the 11 transverse exoskeleton bents at 4.8m spacing, the 6 MEP systems (colors `#2B3A8C`, `#27AE60`, `#F1C40F`, `#E74C3C`, `#2980B9`, `#8E44AD`), the 7 rendering modes (`exterior`, `xray`, `core_only`, `hvac`, `thermal`, `structural`, `night`), and the mode visibility matrix.
5. `docs/bharati3d/06-subagent_implementation_plan.md` lines 375–399: Specifies the authoritative 21 hotspots in `HOTSPOT_REGISTRY` with exact string keys, labels, and world coordinates.
6. `docs/bharati3d/06-subagent_implementation_plan.md` lines 214–291: Specifies all 10 auxiliary site assets (SATCOM radome, fuel farm with 13 tanks, helipad with 'H' marking, 25-container depot, trace-heated pipe rack, 5x flagpole array, meteo mast, meltwater tarn, displaced terrain plane, and 3000-particle blizzard system).
7. `app/static/js/three/station_3d_view.js` lines 147–283: Currently implements a simplified placeholder model with an arbitrary rectangular box (`80 × 30 × 14`), generic cylindrical stilts without V-stilts, only 6 legacy hotspots (`hotspot-main_building`, `hotspot-fuel_storage`, `hotspot-comms_satcom`, `hotspot-hvac`, `hotspot-heliport`, `hotspot-environment_sensors`), zero MEP layers, and no mode controller.

---

## 2. Logic Chain

### 2.1 Coordinate System and World Datum
- **World Origin `(0.0, 0.0, 0.0)`**: Center of the station on the natural granitic bedrock surface directly beneath Grid Axis 9 (longitudinal) and Grid Axis C (transverse centerline).
- **Coordinate Convention**:
  - `+X` = East (toward ocean-facing cantilever prow, Grid Axis 21)
  - `-X` = West (toward logistics vehicle garage and tarn, Grid Axis 1)
  - `+Y` = Up (elevation above bedrock datum)
  - `+Z` = South (inland-facing wall, Grid Axes D & E)
  - `-Z` = North (seaward-facing wall overlooking Prydz Bay, Grid Axes A & B)
- **Scale**: 1 Three.js unit = 1.0 real-world meter.

### 2.2 Transverse Hull Profile P1–P11 & Extrusion Geometry
From CAD Elevation Blueprint `17_front_prow_cad_elevation_and_datums.md` §3, the transverse cross-section is defined in the local 2D shape plane (where Local X maps to World Z, Local Y maps to World Y):

| Vertex | Local X (World Z) | Local Y (World Y) | CAD Datum | Physical Architectural Description |
|:---|:---:|:---:|:---:|:---|
| **P1** | `0.0m` | `+2.60m` | H1 | Central underbelly keel lowest point / stilt connection plate |
| **P2** | `-7.5m` | `+3.40m` | — | Port transverse stilt haunch junction |
| **P3** | `-10.0m` | `+5.10m` | H2 | Port outer bevel / widest hull chine (Level 1 Finished Floor) |
| **P4** | `-9.5m` | `+8.95m` | H3 | Port upper roof fascia corner (Level 1 ceiling / roof deck) |
| **P5** | `-5.0m` | `+10.10m`| — | Port hipped roof slope transition |
| **P6** | `-3.8m` | `+11.58m`| H4 | Penthouse roof port apex |
| **P7** | `+3.8m` | `+11.58m`| H4 | Penthouse roof starboard apex |
| **P8** | `+5.0m` | `+10.10m`| — | Starboard hipped roof slope transition |
| **P9** | `+9.5m` | `+8.95m` | H3 | Starboard upper roof fascia corner |
| **P10**| `+10.0m` | `+5.10m` | H2 | Starboard outer bevel / widest hull chine |
| **P11**| `+7.5m` | `+3.40m` | — | Starboard transverse stilt haunch junction |

**Shape Extrusion Settings:**
```javascript
const hullShape = new THREE.Shape();
hullShape.moveTo(0.0, 2.60);     // P1
hullShape.lineTo(-7.5, 3.40);    // P2
hullShape.lineTo(-10.0, 5.10);   // P3
hullShape.lineTo(-9.5, 8.95);    // P4
hullShape.lineTo(-5.0, 10.10);   // P5
hullShape.lineTo(-3.8, 11.58);   // P6
hullShape.lineTo(3.8, 11.58);    // P7
hullShape.lineTo(5.0, 10.10);    // P8
hullShape.lineTo(9.5, 8.95);     // P9
hullShape.lineTo(10.0, 5.10);    // P10
hullShape.lineTo(7.5, 3.40);     // P11
hullShape.closePath();

const extrudeSettings = {
  steps: 1,
  depth: 50.0,            // 50m along X-axis
  bevelEnabled: false,    // Exact profile, bevel encoded in vertices
};
const hullGeo = new THREE.ExtrudeGeometry(hullShape, extrudeSettings);
// Center along X-axis from x = -25.0 to +25.0:
hullGeo.rotateY(Math.PI / 2);
hullGeo.translate(-25.0, 0, 0);
```
- **Window Ribbon Recess**: Cutout/recess of 0.15m inward from `Y = +7.8m` to `+9.0m` (height 1.2m) along the north and south longitudinal walls. North side has 16 uniform bays (`2.3m W × 1.2m H`), south side has 12–14 bays.

### 2.3 Substructure: Quad Cantilever V-Stilts & 28 Vertical Stilts Grid
1. **Quad Cantilever V-Stilts (Axes 17–21, Eastern Prow)**:
   - Supports the 10.5m cantilevered prow past the Level 0 core.
   - Four distinct fabricated box-section V-bents (using 4-segment `CylinderGeometry` for the tapered rectangular box section effect):
     - **Outer Port Bent**: Center at `[18.5, 1.05, +8.75]`, `topWidth = 8.75m`, `height = 4.2m`, `legThickness = 0.45m`, leg incline `22°` (`rotation.z = ±Math.atan2(topWidth * 0.25, height)`).
     - **Outer Starboard Bent**: Center at `[18.5, 1.05, -8.75]`, `topWidth = 8.75m`, `height = 4.2m`.
     - **Inner Port Bent**: Center at `[14.0, 1.05, +4.80]`, `topWidth = 4.80m`, `height = 4.2m`.
     - **Inner Starboard Bent**: Center at `[14.0, 1.05, -4.80]`, `topWidth = 4.80m`, `height = 4.2m`.
   - Material: `VStiltEpoxy` (`color: 0xB0BFC5`, `metalness: 0.85`, `roughness: 0.25`).
   - Group Name: `hotspot-v-stilts`.

2. **28 Vertical Stilts Grid & Concrete Footings (Axes 1–16)**:
   - **Columns**: 28 cylindrical steel columns rendered via `THREE.InstancedMesh`.
     - Diameter: `0.40m` (radius `0.20m`), `segments: 8`.
     - Height varies from `H = 2.60m` (at Level 0 stilt bearing) down to bedrock terrain level.
     - Grid layout: Longitudinal spacing `4.80m` on center (Axes 1, 3, 5, 7, 9, 11, 13, 15) × Transverse spacing at `Z = ±4.80m` and `Z = ±8.40m`.
   - **Concrete Footing Pads**: 28 flat cylinder pads `THREE.InstancedMesh` with `CylinderGeometry(0.6, 0.6, 0.2, 8)` at `Y = 0.00m`. Material: `0x6D6B66`, roughness `0.80`.
   - **Diagonal Knee Bracing**: Merged `BufferGeometry` of tubular struts `CylinderGeometry(0.08, 0.08, 2.8, 6)` inclined at 45° between columns and floor girders.

### 2.4 Prow Profile & 6-Bay Panoramic Glazing
- **Prow Longitudinal Profile**:
  ```javascript
  const prowShape = new THREE.Shape();
  prowShape.moveTo(0.0, 0.0);       // Rear underbelly anchor
  prowShape.lineTo(10.0, 1.2);      // Upward sloped underbelly prow
  prowShape.lineTo(11.0, 4.2);      // Inward-raked 15° window base
  prowShape.lineTo(10.5, 4.6);      // Top roof chamfer bevel
  prowShape.lineTo(0.0, 4.6);       // Roof deck line
  prowShape.closePath();
  ```
- **6-Bay Glazing**:
  - Total width: `12.0m` centered on Axis C (`Z = -6.0m` to `+6.0m`), flanked by solid corner return panels (`Z = ±6.0m` to `±10.0m`).
  - Height: `3.0m` (from Level 1 floor `Y = +5.10m` to ceiling `Y = +8.10m`).
  - Negative rake angle: `15°` inward slope from top to bottom.
  - 5 vertical structural mullions: `BoxGeometry(0.10, 3.0, 0.25)` spaced at `Z = -4.0, -2.0, 0.0, +2.0, +4.0`.
  - Material: Day mode = `ProwGlazingDay` (`color: 0x1A312C`, `roughness: 0.05`, `transmission: 0.85`, `ior: 1.52`); Night mode = `NightWindowWarm` (`color: 0xFFAE33`, `emissive: 0xFF9900`, `intensity: 2.0`).

### 2.5 Penthouse Module, Access Stairs & Corner Chamfers
1. **Level 2 Penthouse**:
   - `BoxGeometry(15.0, 2.8, 7.5)` centered at `[0.0, 10.34, 0.0]`.
   - Roof terrace safety railing: `12.0m L × 7.5m W × 1.1m H` galvanized pipe railing (`0xCFD8DC`) on eastern half.
   - 3x CHP generator exhaust flues: `CylinderGeometry(0.15, 0.15, 1.2, 8)` stainless steel (`0xE8ECEF`) at `[-9.6, 12.2, 3.5]`.
2. **Symmetrical 13-Step Access Stairs (2×)**:
   - Port Flight: `[18.0, 2.3, +9.5]`
   - Starboard Flight: `[18.0, 2.3, -9.5]`
   - Dimensions: Exactly 13 steps per flight, rise = `0.18m`, tread = `0.28m`, total rise = `2.34m`, slope = `32.7°`, stair width = `1.2m` (`BoxGeometry(0.28, 0.18, 1.2)` per tread). Galvanized zinc steel (`0xCFD8DC`, metalness `0.90`, roughness `0.40`).
3. **Corner Chamfer Bevels**:
   - 4× planar bevel panels at 45°, face width `1.2m`, smoothing all 4 vertical longitudinal corners.
4. **Modular Container Core (X-Ray Group)**:
   - `Level0_Utility_Block`: `BoxGeometry(24.0, 3.8, 20.0)` at `[-12.0, 2.8, 0.0]`, terracotta/orange `ctnOrange` (`0xC85A32`).
   - `Level1_Living_Deck`: `BoxGeometry(48.0, 3.0, 20.0)` at `[0.0, 6.5, 0.0]`, green `ctnGreen` (`0x5C9E68`) on North side, white `ctnWhite` (`0xDCE4E4`) on South side.
   - `Level2_Penthouse_Spine`: `BoxGeometry(15.0, 2.5, 7.5)` at `[0.0, 9.8, 0.0]`, white `ctnWhite` (`0xDCE4E4`).
   - Hidden in default `exterior` mode; visible in `xray` and `core_only` modes.
5. **Indian National Flag Emblem**:
   - `THREE.DecalGeometry` / textured quad on north lower 30° chamfer panel at `[0.0, 5.0, -10.1]`, dimensions `1.8m W × 1.2m H`. Colors: Saffron `#FF9933`, White, Green `#138808`, Navy Chakra `#000080`.

### 2.6 Exterior Site Assets & Environment
1. **SATCOM Geodesic Radome**:
   - `THREE.IcosahedronGeometry(5.2, 2)` (80 triangular faces, `flatShading: true`).
   - World position: `[-25.0, 7.2, 35.0]`.
   - Ring truss base: `CylinderGeometry(5.0, 5.0, 0.3, 32)` at `Y = 2.0m`, supported on 10 tubular steel stilts.
   - Material: Off-white dielectric fiberglass (`0xE6EDED`, roughness `0.35`, metalness `0.05`).
   - Group Name: `hotspot-satcom`.
2. **Fuel Farm (13 Cylindrical Tanks, 296 kL bulk reserves)**:
   - `THREE.InstancedMesh` of `CylinderGeometry(2.5, 2.5, 8.0, 16)`, count = 13.
   - Base center: `[-80.0, 4.0, -35.0]`. Arranged in 3 rows spaced 5.0m apart.
   - Material: Dark slate fuel tanks (`0x34495E`, roughness `0.55`, metalness `0.40`).
   - Group Name: `hotspot-fuel-storage`.
3. **Helipad with 'H' Marking**:
   - Platform: `CylinderGeometry(15.0, 15.0, 0.5, 32)` at `[-85.0, 4.0, -95.0]`.
   - Marking: 'H' letter from 3× `BoxGeometry` strips (width 1.5m, bar length 6.0m) + outer border ring `RingGeometry(13.0, 13.5, 64)`.
   - Windsock on 3m pole at pad perimeter.
   - Group Name: `hotspot-heliport`.
4. **Container Depot (NW Apron, 25 Containers)**:
   - `THREE.InstancedMesh` of 20ft ISO containers `BoxGeometry(6.06, 2.59, 2.44)`, count = 25.
   - Center: `[-28.0, 0.0, -18.0]`, arranged in a 5×5 staging grid.
   - Colors cycled: Orange `#E85D04`, Green `#008751`, Maritime Blue `#0B4F6C`, Cor-Ten Rust `#8C3828`.
   - Group Name: `hotspot-container-depot`.
5. **Trace-Heated Pipe Rack**:
   - Extruded double-pipe tray (width `1.2m`, standoff `0.8m`) on A-frame supports every 6m along a curve connecting building to fuel farm and seawater intake.
   - Anchor: `[0.0, 0.8, 12.0]`.
   - Group Name: `hotspot-pipe-rack`.
6. **Flagpole Ridge (5× Masts)**:
   - 5× `CylinderGeometry(0.04, 0.04, 8.0, 6)` at `[-45.0, 2.0, -70.0]`, spaced 3.0m apart.
   - Group Name: `hotspot-flagpole-ridge`.
7. **Meteorological Mast**:
   - `CylinderGeometry(0.06, 0.06, 5.0, 6)` at `[0.0, 13.5, 0.0]` atop penthouse with horizontal cross-arms.
   - Group Name: `hotspot-meteo-mast`.
8. **Meltwater Tarn**:
   - `PlaneGeometry(60.0, 40.0)` at `[-35.0, -1.2, 0.0]`, rotated `X = -Math.PI / 2`.
   - Material: `TarnWaterMat` (`0x1B4D72`, roughness `0.02`, transmission `0.90`, ior `1.33`).
   - Group Name: `hotspot-meltwater-tarn`.
9. **Terrain Plane with Noise Displacement**:
   - `THREE.PlaneGeometry(300, 300, 64, 64)` displaced with procedural noise.
   - Station pad flattened at `Y = 0.0m` (radius ~30m). North slope drops to `Y = -35.0m` at `Z = -350.0m` (sea level). Western tarn depression at `Y = -3.5m`.
   - Material: `0x826B50` (Larsemann gneiss rock), roughness `0.85`.
10. **Blizzard Particle System**:
    - Exactly **3,000 particles** (`THREE.Points`).
    - Volume: `[-150, 150] × [-10, 100] × [-150, 150]`.
    - PointMaterial: `color: 0xC8E6D7`, `size: 0.8`, `blending: THREE.AdditiveBlending`, `opacity: 0.6`.
    - Velocity: `vx = +0.3 to +0.7` (katabatic wind blowing through elevated underbelly), `vy = -0.1 to -0.3`, `vz = ±0.1`.
    - Boundary reset: if `pos.x > 150 || pos.y < -10`, reset to `x = -150`, `y = 80 + rand*20`.

### 2.7 MEP Overlays & 7-Mode Rendering State Matrix
1. **MEP Layer Meshes**:
   - **Structural Steel Frame (`StructuralFrameMesh`)**: 11 portal bents at 4.8m spacing (`X = -24.0m` to `+24.0m`). Color: Industrial Cobalt Blue `#2B3A8C`, metalness `0.85`, roughness `0.30`.
   - **HVAC Fresh Air Supply (`HVACSupplyMesh`)**: Main trunk `BoxGeometry(0.8, 0.5, 42.0)` at `[0.0, 9.0, 0.0]` + 24 vertical cabin branch drops `CylinderGeometry(0.2, 0.2, 3.0)`. Color: Vibrant Green `#27AE60`.
   - **HVAC Exhaust Return (`HVACReturnMesh`)**: Parallel trunk offset by 1.0m. Color: Warm Yellow `#F1C40F`.
   - **Hydronic Heating Loops (`HydronicHeatMesh`)**: District heating tubes along underfloor perimeter. Color: Primary Red `#E74C3C` (Return burgundy `#C0392B`).
   - **Domestic Water & Greywater (`DomesticWaterMesh`)**: Potable and greywater circuits from snow melter to MBR. Color: Royal Blue `#2980B9`.
   - **Electrical Power Busway (`ElectricalBuswayMesh`)**: 2× 415V 3-phase busway ducts `BoxGeometry(0.4, 0.1, 48.0)` along corridor ceiling. Color: Purple `#8E44AD`.

2. **Complete 7-Mode Matrix Table**:

| Mode ID | Description | `outerSkin.opacity` / `visible` | `containerCore.visible` | `MEPGroup.visible` & Active Mesh | Lighting Configuration |
|:---|:---|:---:|:---:|:---|:---|
| `exterior` | Default day exterior | `1.0` (opaque) / `true` | `false` | `false` (all hidden) | Day sun (`#7DBFAD` 1.5, `#428475` 1.0) |
| `xray` | Semi-transparent inspection | `0.25` (transparent) / `true` | `true` | `false` | Day sun |
| `core_only`| Container skeleton | `false` (hidden) | `true` | `false` | Day sun |
| `hvac` | Ventilation SCADA | `0.15` (transparent) / `true` | `false` | `true` (`HVACSupplyMesh`, `HVACReturnMesh`) | Day sun |
| `thermal` | District heat SCADA | `0.15` (transparent) / `true` | `false` | `true` (`HydronicHeatMesh`) | Day sun |
| `structural`| Exoskeleton inspection | `0.15` (transparent) / `true` | `false` | `true` (`StructuralFrameMesh`) | Day sun |
| `night` | Nocturnal / Aurora mode | `1.0` (opaque) / `true` | `false` | `false` | Night aurora (`0x2A6A4E`, `0x4EBA87`), moonlight (`0x6B8BA4`), emissive windows (`#FFAE33` / `#E6F2FF`) |

### 2.8 Authoritative 21-Hotspot Registry (`HOTSPOT_REGISTRY`)
Every hotspot object in the Three.js scene MUST be named with the exact prefix `hotspot-` and provide an interactive bounding volume or group matching these exact coordinates:

| # | Hotspot ID | Label | World Anchor `[x, y, z]` | Domain Subsystem | Target Telemetry |
|:---:|:---|:---|:---:|:---|:---|
| 1 | `hotspot-power-plant` | `CHP Power Plant` | `[-19.2, 2.8, 7.2]` | Microgrid Energy | 3x gensets: kW load, RPM, fuel flow |
| 2 | `hotspot-hvac` | `HVAC Life Support` | `[-7.2, 10.2, 0.0]` | Life Support & Hab | AHU temp, CO₂ ppm, heat recovery % |
| 3 | `hotspot-chp-heating` | `District Heating` | `[-6.0, 3.2, 0.0]` | District Heat | Hydronic loop temps, boiler pressure |
| 4 | `hotspot-water-lss` | `Water & LSS` | `[-19.2, 2.8, -7.2]` | Environmental LSS | Snow melter kL, MBR flux, UV status |
| 5 | `hotspot-workshop-garage` | `Vehicle Garage` | `[-18.0, 3.8, 0.0]` | Logistics & Fleet | PistenBully status, overhead crane |
| 6 | `hotspot-main-hab` | `Main Habitat` | `[0.0, 5.5, 0.0]` | Crew Quarters | 24-cabin occupancy, interior °C, fire |
| 7 | `hotspot-dining-mess` | `Dining Mess` | `[-18.0, 6.5, 0.0]` | Living Ops | Galley power, food stock |
| 8 | `hotspot-medical-bay` | `Medical Bay` | `[-14.4, 6.5, -7.2]` | Health & Telemed | Telemedicine uplink, pharmacy temp |
| 9 | `hotspot-ocean-lounge` | `Ocean Lounge` | `[19.0, 6.5, 0.0]` | Crew Welfare | Solar flux, occupancy, ocean view |
| 10 | `hotspot-science-terrace` | `Science Terrace` | `[2.0, 11.5, 0.0]` | Science Ops | Ozone spectrometer, cloud lidar |
| 11 | `hotspot-meteo-mast` | `Meteorological Mast` | `[0.0, 13.5, 0.0]` | Meteorology | Wind speed/dir, pressure (hPa) |
| 12 | `hotspot-v-stilts` | `V-Stilt Foundations` | `[18.5, 2.1, 0.0]` | Structural Health | Foundation strain, hydraulic balance |
| 13 | `hotspot-satcom` | `SATCOM Radome` | `[-25.0, 7.2, 35.0]` | Telecom | GSAT-7A link SNR, latency (ms) |
| 14 | `hotspot-fuel-storage` | `Fuel Farm (296 kL)` | `[-80.0, 4.0, -35.0]` | Fuel Logistics | 13x Jet A-1 tanks, fuel temp |
| 15 | `hotspot-pipe-rack` | `Trace-Heated Pipe Rack`| `[0.0, 0.8, 12.0]` | Infrastructure | Heat-trace circuit, freeze alarm |
| 16 | `hotspot-heliport` | `Heliport Operations` | `[-85.0, 4.0, -95.0]` | Flight Operations | Windsock, aviation fuel, Medevac |
| 17 | `hotspot-container-depot` | `Container Depot` | `[-28.0, 0.0, -18.0]` | Logistics | Inventory tracking, supply ledger |
| 18 | `hotspot-meltwater-tarn` | `Meltwater Tarn` | `[-35.0, -1.2, 0.0]` | Environmental | Freshwater source monitoring |
| 19 | `hotspot-flagpole-ridge` | `Flagpole & Anemometer` | `[-45.0, 2.0, -70.0]` | Meteorology | Anemometer, territorial marker |
| 20 | `hotspot-meteo-science-lab`| `Science Lab (Meteorology)`| `[4.8, 3.5, -7.2]` | Science | Atmospheric sensor data hub |
| 21 | `hotspot-main-entrance` | `Main Entrance Bharati` | `[-6.0, 3.8, 10.0]` | Access Control | Personnel muster, door status |

---

## 3. Caveats

1. **Maritime Harbor Scope**: While `docs/bharati3d/08_maritime_ice_harbor_and_resupply_logistics.md` specifies the *Ivan Papanin* cargo ship and ice harbor at `[-200.0, -35.0, -1200.0]`, this asset is located 1.2 km away from the main complex. In accordance with `docs/bharati3d/06-subagent_implementation_plan.md` §5.1, the 21 hotspots in the active scene registry focus on the station complex and immediate site apron (< 100m). The distant ice harbor should be an optional background group or excluded to keep the triangle count strictly within the 20,000 budget.
2. **ISRO AGEOS Ground Station**: In strict adherence to `GEMINI.md §9`, the AGEOS / ISRO X-S band earth station is a distinct standalone facility and is explicitly **out of scope** for this digital twin.
3. **Internal Container Modeling**: Constraint R1 and doc 04 specifically mandate: "Do not model individual interior containers. The containers form the inner skeleton." The X-ray layer should be represented by 3 merged volumetric blocks (`Level0_Utility_Block`, `Level1_Living_Deck`, `Level2_Penthouse_Spine`) rather than 134 separate heavy meshes.

---

## 4. Conclusion

The architectural investigation of `docs/bharati3d/` provides the 100% verified, authoritative mathematical blueprints required to replace the existing placeholder in `app/static/js/three/station_3d_view.js`. 

Key takeaways for the implementing agent:
1. Replace the generic rounded box with the exact **P1–P11 extruded profile** (`X: -25.0 to +25.0m`).
2. Replace the uniform cylindrical grid with the **Quad V-stilt cantilever bents** at `X = 18.5m` and the **28 instanced vertical stilts** with concrete footing pads.
3. Implement the **6-bay inward-raked (15°) panoramic prow window** with 5 vertical mullions.
4. Implement all **10 auxiliary site assets** (SATCOM geodesic radome with 80 faces, 13-tank fuel farm, helipad with 'H' marking, 25-container depot, pipe rack, 5x flagpoles, meteo mast, meltwater tarn, noise-displaced terrain plane, and 3000-particle blizzard system).
5. Add the **MEP overlay groups** (11 structural bents, HVAC supply/return, hydronic heating, domestic water, electrical busway) and wire up the **7 rendering modes** (`exterior`, `xray`, `core_only`, `hvac`, `thermal`, `structural`, `night`) via `window.set3DMode(mode)`.
6. Register and name all **21 hotspots** with `hotspot-` prefix, wiring raycast click dispatch to `window.dispatchEvent(new CustomEvent('st-3d-click', { detail: assetSlug }))` and status updates to `window.update3DHotspot(assetId, status)`.
7. Enforce the **20,000 triangle performance budget** with `checkGeometryBudget()` to guarantee smooth 60 FPS execution in WebGL.

---

## 5. Verification Method

To verify these specifications against the codebase and documentation:
1. **Cross-Check CAD Vertices**:
   ```bash
   # Verify P1-P11 profile in doc 17
   grep -A 15 "P1" docs/bharati3d/17_front_prow_cad_elevation_and_datums.md
   ```
2. **Verify V-Stilt Generator Formula**:
   ```bash
   # Verify createVStiltBent in doc 11
   grep -A 25 "createVStiltBent" docs/bharati3d/11_cantilever_v_stilts_and_underbelly_aerodynamics.md
   ```
3. **Verify 21-Hotspot Registry**:
   ```bash
   # Verify HOTSPOT_REGISTRY in doc 06
   grep -A 25 "const HOTSPOT_REGISTRY" docs/bharati3d/06-subagent_implementation_plan.md
   ```
4. **Verify MEP Taxonomy & Modes**:
   ```bash
   # Verify mode matrix and color codes in doc 06
   grep -A 15 "Rendering Mode State Machine" docs/bharati3d/06-subagent_implementation_plan.md
   ```
5. **Verify Constraint Compliance**:
   ```bash
   # Ensure no forbidden dependencies in Three.js frontend asset (C14, C13)
   grep -E "createClient|supabase-js|SUPABASE_SERVICE_ROLE_KEY" app/static/js/three/station_3d_view.js
   ```
