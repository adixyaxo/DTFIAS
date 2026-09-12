# Bharati Station — 3D Digital Twin Sub-Agent Synthesis

> **Authority:** Synthesized from deep analysis of all 29 documents in `docs/bharati3d/`, including 22 photographic analyses, BIM/MEP specifications, and 6 official CAD blueprints (elevations, floor plans, sections).  
> **World Origin:** `(0.0, 0.0, 0.0)` = centre of station on bedrock datum, beneath Grid Axis 9 (longitudinal) and Grid Axis C (transverse). 1 unit = 1 metre. Y-axis is UP.

---

## 1. Core Architecture & Absolute Dimensions

Bharati Station (Larsemann Hills, 69°24′S 76°11′E) was designed by **bof architekten / IMS Ingenieurgesellschaft** for NCPOR and completed in 2012. It won the **European Steel Design Award (2013)**.

### 1.1 Structural Formula: `container + skin = research base`
- **134 ISO shipping containers** (20ft primary: 6.06 m × 2.44 m × 2.59 m) form the internal structural skeleton.
- **11 transverse portal steel bents** spaced at 4.80 m on-centre wrap and surround the container stack.
- An **aerodynamic insulated aluminum cladding skin** (80 mm sandwich cassette panels with fluoropolymer coating) envelopes everything, separated by a **0.6–0.8 m thermal buffer cavity**.
- The station is wind-tunnel tested to withstand **300 km/h katabatic blizzards**.

### 1.2 Authoritative Bounding Box & Datums (from CAD blueprints 17–22)
```
Principal Bounding Box:
  Length (X-axis):  50.00 m  (Axis 1 western tail → Axis 21 eastern prow)
  Width  (Z-axis):  20.00 m  (outer chamfer chine E' to A')
  Height (Y-axis):  11.58 m hull / 13.50 m incl. met. mast

Vertical Datum System (Y-Up, 1 unit = 1 m):
  Y =  0.000 m   →  Natural granitic bedrock surface (Larsemann Hills)
  Y = +1.834 m   →  Underbelly keel lowest point
  Y = +2.596 m   →  Level 0 Finished Floor Level (H1 / stilt bearing)
  Y = +5.103 m   →  Level 1 Finished Floor Level (H2 / living deck)
  Y = +8.413 m   →  Main hull roof (H3 lower)
  Y = +8.948 m   →  Roof deck / parapet fascia (H3 upper)
  Y =+11.580 m   →  Level 2 penthouse apex (H4)
  Y =+13.500 m   →  Meteorological mast apex

Transverse Profile Vertices (for ExtrudeGeometry Shape):
  P1  Z = 0.0,    Y = +2.60  (keel centre)
  P2  Z = ±7.5,   Y = +3.40  (stilt haunch)
  P3  Z = ±10.0,  Y = +5.10  (widest hull chine, H2)
  P4  Z = ±9.5,   Y = +8.95  (roof fascia, H3)
  P5  Z = ±5.0,   Y =+10.10  (hipped roof ridge)
  P6  Z = ±3.8,   Y =+11.58  (penthouse apex, H4)
```

---

## 2. Three-Level Spatial Layout

### Level 0 — Ground Utility Core (Y: +1.834 m → +5.103 m)
| Room / System | Grid Range | Centre `[x, y, z]` |
|:---|:---|:---|
| 3× CHP Diesel Gensets (Volvo Penta/Scania 320 kVA) | Axes 1–5, D–E | `[-19.2, 2.8, 7.2]` |
| Vehicle Workshop & Tracked PistenBully Garage (overhead crane) | Axes 1–5, B–D | `[-18.0, 3.8, 0.0]` |
| Water Treatment / MBR / Snow Melter | Axes 1–5, A–B | `[-19.2, 2.8, -7.2]` |
| "Bharati" Main Entrance Airlock | Axes 8–9 | `[-6.0, 3.8, 10.0]` |
| Meteorology & Geomagnetism Labs | Axes 11–15, A–B | `[4.8, 3.5, -7.2]` |
| Earth Science & Physiology Labs | Axes 11–15, D–E | `[4.8, 3.5, 7.2]` |
- Axes 15–21: **completely open air cantilever underbelly** (free clearance 3.5–4.8 m) for unimpeded blizzard wind passage.
- Double-height garage hoist height: 4.40 m.

### Level 1 — Living & Operations Deck (Y: +5.103 m → +8.413 m)
| Room / System | Grid Range | Centre `[x, y, z]` |
|:---|:---|:---|
| Panoramic Ocean Lounge & Bar | Axes 17–21, B–D | `[19.0, 6.5, 0.0]` |
| Communal Dining Mess (36 seats) | Axes 1–4, B–D | `[-18.0, 6.5, 0.0]` |
| Medical Infirmary + Telemedicine | Axes 3–6, A–B | `[-14.4, 6.5, -7.2]` |
| Fitness Gym | Axes 1–3, A–B | `[-19.2, 6.5, -7.2]` |
| Sauna & Hygiene Suite | Axes 11–12, B–C | `[2.4, 6.5, -2.4]` |
| Cinema / Auditorium | Axes 13–15, B–D | `[7.2, 6.5, 0.0]` |
| 13 Crew Cabins (North wall, seaward) | Axes 8–21, A–B | Along north wall |
| 11 Crew Cabins (South wall, inland) | Axes 8–20, D–E | Along south wall |
- Cabin size: 2.4 m W × 3.6 m L. Clear ceiling: ~2.70 m.

### Level 2 — Penthouse & Rooftop Terrace (Y: +8.948 m → +11.580 m)
- Central penthouse spine: 15.0 m L × 7.5 m W × 2.8 m H, offset `[0.0, 9.5, 0.0]`
- Houses: central AHU plant rooms, heat recovery units, 3× vertical CHP exhaust flues (1.2 m above roofline)
- Rooftop terrace: flat walking deck, galvanized safety railing (1.1 m H), science instruments, meteorological mast

---

## 3. Substructure & Foundation System

### Vertical Stilts (Central Grid)
- Cylindrical hollow steel sections, diameter ≈ 0.40 m
- Grid spacing: 4.8 m longitudinal × ~9.6 m transverse
- **Diagonal knee braces** (45° tubular struts, 2.8 m length) stabilise against polar blizzard lateral loads
- 28 anchor footing pads cast into granitic bedrock

### Quad Cantilever V-Stilts (Eastern Prow, Axes ~17–21)
- **4 distinct fabricated box-section V-bents** (NOT simple cylinders — tapered trapezoidal hollow box sections):
  - 2× Outer V-stilts: transverse spread ±8.75 m (`[18.5, 2.1, ±8.75]`)
  - 2× Inner V-stilts: transverse spread ±4.80 m (`[18.5, 1.3, ±4.80]`)
- V-stilt height: 4.2 m. Leg incline: 22° off-vertical.
- Top section: 0.8 m × 0.5 m (broad apex). Taper to 0.35 m × 0.35 m pin-joint base.
- Material: anti-corrosive marine polyurethane epoxy `#B0BFC5`, Metalness 0.85, Roughness 0.25

### Access Stairs
- **Two symmetrical 13-step external steel staircases** on North and South faces (axes E–E′ and A–A′)
- Rise = 18 cm, Tread = 28 cm, Total rise = 2.34 m, Slope = 32.7°
- Positions: `[18.0, 2.3, ±9.5]`

---

## 4. Exterior Aerodynamic Shell — Geometry Details

### Main Hull Profile (for ExtrudeGeometry)
Extrude the transverse shape P1→P11 along the X-axis for 50.0 m, centred at origin:
- The south-facing wall has a **30° inward underbelly chamfer**
- 16-bay window ribbon: Y `+7.8 m` to `+9.0 m` (height 1.2 m), recessed 0.15 m inward, each pane 2.3 m W
- Roof slopes: ~20° perimeter bevel shedding snow

### Cantilevered Prow (Axes 15–21, eastern end)
- **6-bay panoramic glazing** at +15° negative rake (inward from top to bottom), centred on transverse axis
- Full prow depth: ~10.5 m cantilever past the Level 0 wall
- Ground clearance at prow tip: 4.8 m
- Flanked by chamfered opaque corner return panels

### Rear Logistics Facade (Axes 1–3, western end)
- Heavy-duty roll-up vehicle shutter door: 4.5 m W × 3.5 m H
- Personnel airlock door: 1.2 m W × 2.2 m H (with 0.35 m porthole)
- 10-bay vertical rear window gallery

### Corner Chamfers
- All four longitudinal corners feature **45° planar chamfer bevels (~1.2 m face width)** for aerodynamic drag reduction

### Indian National Flag Emblem
- Applied as `THREE.DecalGeometry` on the north facade lower chamfer panel
- Dimensions: 1.8 m W × 1.2 m H, centred at `[0.0, 5.0, -10.1]`
- Colors: Saffron `#FF9933`, White, Green `#138808`, Chakra Navy `#000080`

---

## 5. Comprehensive PBR Material Library (from master spec + photographic analysis)

| Material ID | Hex Base Color | Roughness | Metalness | Special | Component |
|:---|:---|:---:|:---:|:---|:---|
| `AluminumFasciaMat` | `#BAC4C7` | 0.28 | 0.80 | clearcoat: 0.20 | Main exterior skin |
| `RoofPanelMat` | `#4F6D7A` | 0.35 | 0.85 | — | Hipped roof cladding |
| `UnderbellyKeel` | `#8E9EA4` | 0.45 | 0.70 | — | Aerodynamic underside |
| `ProwGlazingDay` | `#1A312C` | 0.05 | 0.10 | transmission:0.85, ior:1.52 | 6-bay panoramic glass |
| `WindowRibbon` | `#1A2E28` | 0.05 | 0.10 | transmission:0.80 | Side window bands |
| `NightWindowWarm` | `#FFAE33` | 0.20 | 0.00 | emissive:#FF9900, intensity:2.0 | 2700K cabin glow |
| `NightWindowLab` | `#E6F2FF` | 0.20 | 0.00 | emissive:#C8E2FF, intensity:1.8 | 5000K lab glow |
| `VStiltEpoxy` | `#B0BFC5` | 0.25 | 0.85 | — | Fabricated box V-stilts |
| `GalvStairs` | `#CFD8DC` | 0.40 | 0.90 | flatShading: false | 13-step stair flights |
| `RadomeFiberglass` | `#E6EDED` | 0.35 | 0.05 | flatShading:true | Geodesic SATCOM dome |
| `GraniteBedrockMat` | `#826B50` | 0.85 | 0.05 | normalMap: granite | Larsemann Hills rock |
| `TarnWaterMat` | `#1B4D72` | 0.02 | 0.10 | transmission:0.90, ior:1.33 | Glacial meltwater tarn |
| `HVACSupplyGreen` | `#27AE60` | 0.30 | 0.20 | SCADA overlay | Fresh air supply ducts |
| `HVACReturnYellow` | `#F1C40F` | 0.30 | 0.20 | SCADA overlay | Exhaust return ducts |
| `HydronicHeatRed` | `#E74C3C` | 0.30 | 0.50 | SCADA overlay | CHP hot water loops |
| `DomesticWaterBlue` | `#2980B9` | 0.30 | 0.20 | SCADA overlay | Potable water piping |
| `SteelFrameBlue` | `#2B3A8C` | 0.45 | 0.80 | SCADA overlay | Structural bents |
| `ContainerGreen` | `#5C9E68` | 0.70 | 0.20 | X-Ray mode | Crew cabin containers |
| `ContainerWhite` | `#DCE4E4` | 0.70 | 0.20 | X-Ray mode | Laboratory containers |
| `ContainerOrange` | `#C85A32` | 0.70 | 0.20 | X-Ray mode | Engineering containers |

---

## 6. Complete Hotspot Registry

All hotspots emit `CustomEvent('st-3d-click', { detail: assetSlug })` on click.

### Station Core Hotspots
| Hotspot ID | World Coords `[x, y, z]` | Domain | Key Telemetry |
|:---|:---:|:---|:---|
| `hotspot-power-plant` | `[-19.2, 2.8, 7.2]` | Microgrid | 3× gensets: kW load, RPM, fuel flow |
| `hotspot-hvac` | `[-7.2, 10.2, 0.0]` | Life Support | AHU temp, CO₂ ppm, heat recovery % |
| `hotspot-chp-heating` | `[-6.0, 3.2, 0.0]` | District Heat | Hydronic loop temps, boiler pressure |
| `hotspot-water-lss` | `[-19.2, 2.8, -7.2]` | Environmental LSS | Snow melter kL, MBR flux, UV status |
| `hotspot-workshop-garage` | `[-18.0, 3.8, 0.0]` | Logistics & Fleet | PistenBully status, overhead crane |
| `hotspot-main-hab` | `[0.0, 5.5, 0.0]` | Crew Quarters | 24-cabin occupancy, interior °C, fire |
| `hotspot-dining-mess` | `[-18.0, 6.5, 0.0]` | Living Ops | Galley power, food stock |
| `hotspot-medical-bay` | `[-14.4, 6.5, -7.2]` | Health | Telemedicine uplink, pharmacy temp |
| `hotspot-ocean-lounge` | `[19.0, 6.5, 0.0]` | Crew Welfare | Solar flux, occupancy |
| `hotspot-science-terrace` | `[2.0, 11.5, 0.0]` | Science Ops | Ozone spectrometer, cloud lidar |
| `hotspot-meteo-mast` | `[0.0, 13.5, 0.0]` | Meteorology | Wind speed/dir, pressure (hPa) |
| `hotspot-v-stilts` | `[18.5, 2.1, 0.0]` | Structural Health | Foundation strain, hydraulic pressure |
| `hotspot-main-entrance` | `[-6.0, 3.8, 10.0]` | Access Control | Personnel muster, door status |
| `hotspot-meteo-science-lab` | `[4.8, 3.5, -7.2]` | Science | Atmospheric sensor data hub |

### Exterior / Site Hotspots
| Hotspot ID | World Coords `[x, y, z]` | Domain | Key Telemetry |
|:---|:---:|:---|:---|
| `hotspot-satcom` | `[-25.0, 7.2, 35.0]` | Telecom | GSAT-7A link SNR, latency (ms) |
| `hotspot-fuel-storage` | `[-80.0, 4.0, -35.0]` | Fuel Logistics | 13× Jet A-1 tanks, 296 kL, fuel temp |
| `hotspot-pipe-rack` | `[0.0, 0.8, 12.0]` | Infrastructure | Trace-heat circuit status, freeze alarm |
| `hotspot-heliport` | `[-85.0, 4.0, -95.0]` | Flight Ops | Windsock, aviation fuel, Medevac log |
| `hotspot-container-depot` | `[-28.0, 0.0, -18.0]` | Logistics | Inventory tracking, supply ledger |
| `hotspot-meltwater-tarn` | `[-35.0, -1.2, 0.0]` | Environmental | Freshwater source monitoring |
| `hotspot-flagpole-ridge` | `[-45.0, 2.0, -70.0]` | Meteorology | Anemometer, territorial marker |
| `hotspot-maritime-harbor` | `[-200.0, -35.0, -1200.0]` | Maritime Ops | Ship mooring, container offload |
| `hotspot-aurora-sensor` | `[0.0, 14.0, 0.0]` | Space Weather | Geomagnetic / ionospheric monitoring |

---

## 7. MEP Overlay System (SCADA Modes)

The BIM model (doc `15`) defines the internal engineering system topology:

| System | Color Code | Three.js Mesh Group |
|:---|:---|:---|
| Structural Steel Bents (11×) | `#2B3A8C` | `StructuralFrameMesh` |
| HVAC Fresh Air Supply | `#27AE60` | `HVACSupplyMesh` |
| HVAC Exhaust Return | `#F1C40F` | `HVACReturnMesh` |
| Hydronic District Heating | `#E74C3C` | `HydronicHeatMesh` |
| Domestic Water & Greywater | `#2980B9` | `DomesticWaterMesh` |
| Power Busway 415V | `#8E44AD` | `ElectricalBuswayMesh` |
| SCADA Fiber/Telemetry | `#16A085` | `InstrumentationMesh` |

Toggle function: `setMEPOverlay(systemName, isVisible)` — already defined in Three.js code.

---

## 8. Environmental Scene

### Terrain
- `THREE.PlaneGeometry(300, 300, 64, 64)` displaced with noise to simulate Larsemann Hills gneiss ridges
- Station pad flattened at Y=0. North slope drops to Y=−35 at Z=−350 (sea level).
- West depression for meltwater tarn (60 m × 40 m ellipse, Y=−3.5)
- Terrain color: `#826B50`, roughness 0.85

### Meltwater Tarn
- Flat plane at Y=−1.2, offset `[-35, -1.2, 0]`
- Material: `TarnWaterMat` — deep azure `#1B4D72`, roughness 0.02, transmission 0.90

### Blizzard Particle System
- `THREE.Points`, 3000 particles, primary drift in +X direction
- Color: `#C8E6D7`, size 0.8, additive blending, opacity 0.6

### SATCOM Geodesic Radome
- `THREE.IcosahedronGeometry(5.2, 2)` — 80 faces, `flatShading: true` for authentic geodesic look
- Position: `[-25.0, 7.2, 35.0]`
- Ring truss base: cylinder radius 5.0 m, 8–12 support stilts

### Helipad
- Elevated crushed-granite gravel pad at `[-85.0, 4.0, -95.0]`
- Flat cylinder geometry (radius 15 m, height 0.5 m)
- "H" marking in `THREE.BoxGeometry` strips, ring in `THREE.RingGeometry`
- 5× flagpoles at `[-45.0, 2.0, -70.0]`, 8 m height, 3 m spacing

### Fuel Farm (13 tanks)
- `THREE.InstancedMesh` of CylinderGeometry at `[-80.0, 4.0, -35.0]`
- Color: dark slate `#34495E`, arranged in 3-row grid

### Aurora Australis (Night Mode)
- Hemispherical inverted dome with custom GLSL shader
- Aurora ambient light: `0x2A6A4E`, intensity 0.45
- Aurora directional: `0x4EBA87`, intensity 0.65 from zenith

---

## 9. Rendering Modes

| Mode ID | Description | Mesh Changes |
|:---|:---|:---|
| `exterior` | Default — full aluminum skin visible | outerSkin opacity=1.0, containerCore hidden |
| `xray` | Semi-transparent skin, colour-coded containers | outerSkin opacity=0.25 transparent, containerCore visible |
| `core_only` | Raw container stack only | outerSkin hidden, containerCore visible |
| `hvac` | MEP HVAC duct overlay | MEPGroup hvac layers visible |
| `thermal` | Hydronic heating overlay | MEPGroup heating layer visible |
| `structural` | Steel bent exoskeleton | MEPGroup structural layer visible |
| `night` | Nocturnal shaders + emissive windows | Switch to NightWindowWarm/Lab materials |

---

## 10. Scene Graph Hierarchy (Canonical)

```
BharatiDigitalTwin (THREE.Group)
│
├── Substructure_Stilts
│   ├── Concrete_Footing_Pads       (InstancedMesh: 28 cylinder pads on bedrock)
│   ├── Vertical_Stilt_Columns      (InstancedMesh: 28 cylindrical columns, dia 0.4m)
│   ├── Diagonal_Knee_Braces        (MergedMesh: 45° tubular cross-ties)
│   └── Quad_Prow_V_Stilts          (Group: 4× tapered box-section bents via createVStiltBent())
│
├── Exterior_Aerodynamic_Shell
│   ├── Main_Hull_Skin              (BufferGeometry: extruded transverse profile × 50m)
│   ├── Hipped_Roof_Panels          (BufferGeometry: multi-planar snow-shedding facets)
│   ├── Underbelly_Keel_Shroud      (BufferGeometry: aerodynamic pan, V-dihedral)
│   ├── Panoramic_Prow_Glazing      (Mesh: 6-bay 15° inward-raked glass)
│   ├── North_Ribbon_Windows        (Mesh: 16-pane continuous band)
│   ├── South_Ribbon_Windows        (Mesh: ribbon across residential/lab sector)
│   ├── Penthouse_Terrace_Module    (BoxGeometry 15×7.5×2.8m)
│   ├── Chimney_Cluster_3x          (Group: 3× exhaust flues, stainless)
│   ├── Symmetrical_Access_Stairs   (Group: 2× 13-step galvanized flights)
│   ├── Corner_Chamfer_Bevels       (Group: 4× 45° bevel strip panels)
│   └── Indian_Flag_Emblem          (DecalGeometry at [0.0, 5.0, -10.1])
│
├── Modular_Container_Core          (Group — toggleable X-Ray mode)
│   ├── Level0_Utility_Block        (MergedMesh — terracotta #C85A32)
│   ├── Level1_Living_Deck          (MergedMesh — green #5C9E68 cabins, white #DCE4E4 labs)
│   └── Level2_Penthouse_Spine      (MergedMesh — grey #DCE4E4)
│
├── MEP_Life_Support_Overlay        (Group — SCADA inspection, hidden by default)
│   ├── StructuralFrameMesh         (11 portal bents, #2B3A8C)
│   ├── HVACSupplyMesh              (#27AE60 green ducts)
│   ├── HVACReturnMesh              (#F1C40F yellow ducts)
│   ├── HydronicHeatMesh            (#E74C3C red pipes)
│   ├── DomesticWaterMesh           (#2980B9 blue pipes)
│   └── ElectricalBuswayMesh        (#8E44AD purple busway)
│
└── Auxiliary_Site_Infrastructure
    ├── SATCOM_Geodesic_Radome      (IcosahedronGeometry r=5.2m at [-25,7.2,35])
    ├── Helipad_Platform            (CylinderGeometry r=15m at [-85,4,-95])
    ├── Fuel_Tank_Farm_13x          (InstancedMesh at [-80,4,-35])
    ├── Container_Depot_NW          (InstancedMesh 25× ISO boxes at [-28,0,-18])
    ├── Trace_Heated_Pipe_Rack      (ExtrusionGeometry along terrain)
    ├── Flagpole_Array_5x           (Group at [-45,2,-70])
    ├── Meltwater_Tarn              (PlaneGeometry at [-35,-1.2,0])
    └── Larsemann_Terrain_Mesh      (Displaced PlaneGeometry 300×300)
```

---

## 11. Performance Triangle Budget

| Component | Target Triangles | Strategy |
|:---|:---:|:---|
| Foundation stilts + pads | ≤ 1,200 | InstancedMesh, 8-segment cylinders |
| V-stilt quad set | ≤ 800 | 4-segment CylinderGeometry (box effect) |
| Knee braces | ≤ 600 | Merged thin cylinders |
| Main hull shell | ≤ 2,400 | Extruded profile, minimal bevel segments |
| Roof + penthouse | ≤ 1,400 | Chamfered BoxGeometry + custom roof mesh |
| Glazing panes | ≤ 1,200 | Simple planes with PhysicalMaterial |
| Access stairs (2×) | ≤ 800 | Merged step arrays |
| MEP overlay (all layers) | ≤ 4,000 | Only loaded when mode active |
| Container core (x-ray) | ≤ 2,400 | 3 merged block meshes |
| Site assets (helipad, radome, fuel) | ≤ 3,000 | InstancedMesh for repeated elements |
| Terrain + tarn | ≤ 2,000 | PlaneGeometry subdivisions |
| Blizzard particles | 3,000 pts | THREE.Points (not triangles) |
| **Total target** | **≤ 20,000** | Well within 60 FPS budget |

---

*Synthesized from 29 source documents: 01–04 early guides, 00 master spec, photographic analyses 02–16, and official CAD blueprints 17–22. Each dimension cross-referenced across multiple sources.*
