# Bharati Antarctic Research Station — 3D Digital Twin Master Specification

> **Document Status:** Authoritative 3D Modeling Specification & CAD Master Blueprint  
> **Target Path:** `docs/bharati3d/00_bharati_3d_master_specification.md`  
> **Authority:** Synthesized from 22 architectural photographs, engineering BIM models, and official CAD construction blueprints (*bof architekten / IMS Ingenieurgesellschaft / NCPOR*).  
> **Implementation Target:** WebGL / Three.js Lazy-Loaded Digital Twin (Constraint C16) & GLTF/GLB Asset Pipeline.

---

## 1. Master Architectural Datums & Dimensions

All dimensions are calibrated directly from official longitudinal and transverse working CAD sections (`download (14)` through `download (19)`):

```
                                            [ H4: +11.580m Penthouse Apex ]
                                            ┌─────────────────────────────┐
                                            │ Level 2 Penthouse Terrace   │
    ┌───────────────────────────────────────┴─────────────────────────────┴───────────────────────────────────────┐ [ H3: +8.948m Roof Deck ]
    │                      LEVEL 1 LIVING & OPERATIONS DECK (24 Cabins, Dining, Lounge)                           │
    ├─────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ [ H2: +5.103m Level 1 Floor ]
    │  LEVEL 0 ENCLOSED UTILITY CORE (Axes 1–5)       │      OPEN-AIR CANTILEVER UNDERBELLY (Axes 15–21)          │
    │  (3x CHP Gensets, Workshop, Water Treatment)    │      (Clearance for 300 km/h Katabatic Wind Snowdrifts)   │
    └───┬─────────────────────────────────────────────┴───────────────────────────────────────────────────────────┘ [ H1: +2.596m Level 0 Stilt Base ]
        │                                                                                            │
     Vertical Stilts                                                                           Quad V-Stilts
  ──────┴────────────────────────────────────────────────────────────────────────────────────────────┴──────────── 0.000m Granite Bedrock
      Axis 1 (West) ◄────────────────────────────── 50.00 Meters ─────────────────────────────► Axis 21 (East Prow)
```

### 1.1. Absolute Coordinate & Elevation System (1 Unit = 1.0 Meter)
* **World Origin `(0.0, 0.0, 0.0)`:** Center of the station on bedrock datum, directly beneath Grid Axis 9 (Longitudinal) and Grid Axis C (Transverse).
* **`Y = 0.000m`:** Natural granitic bedrock surface.
* **`Y = +1.834m to +2.596m` (Datum H1):** Level 0 ground utility deck.
* **`Y = +4.842m to +5.103m` (Datum H2):** Level 1 living & operations deck.
* **`Y = +8.413m to +8.948m` (Datum H3):** Level 1 ceiling and main hipped roof fascia.
* **`Y = +11.580m` (Datum H4):** Level 2 central penthouse roof apex.
* **`Y = +13.500m`:** Meteorological sensor mast apex.

### 1.2. Principal Bounding Box
* **Length (X-axis):** **50.00m** (from Axis 1 western tail to Axis 21 eastern prow).
* **Width (Z-axis):** **20.00m** (maximum transverse width at outer chamfer chine, Axis E' to A').
* **Height (Y-axis):** **11.58m** (hull structure) / **13.50m** (including antenna mast).
* **Free Air Ground Clearance:** **~3.5m to ~4.8m** beneath the cantilevered eastern prow.

---

## 2. Three.js Scene Graph Hierarchy & Component Tree

To maintain strict 60 FPS performance in browser viewports while complying with constraint **C16**, the 3D model is organized into modular decoupled groups:

```
BharatiDigitalTwin (THREE.Group)
│
├── Substructure_Stilts (Group)
│   ├── Concrete_Footing_Pads (InstancedMesh: 28 cylinders on bedrock)
│   ├── Vertical_Stilt_Columns (InstancedMesh: 24 cylindrical columns)
│   ├── Quad_Prow_V_Stilts (Group: 4x fabricated tapered box-section bents)
│   └── Diagonal_Knee_Bracing (MergedMesh: structural cross-ties)
│
├── Exterior_Aerodynamic_Shell (Group)
│   ├── Main_Insulated_Cassette_Hull (BufferGeometry: beveled aerodynamic skin)
│   ├── Hipped_Roof_Panels (BufferGeometry: multi-faceted snow-shedding roof)
│   ├── Panoramic_Prow_Glazing (Mesh: 6-bay 15° inward-raked seaward glass)
│   ├── Ribbon_Window_Bands (Mesh: North & South continuous window strips)
│   ├── Penthouse_Terrace (Mesh: Level 2 observation deck & safety guardrail)
│   ├── Exhaust_Chimney_Cluster (Group: 3x generator exhaust flues)
│   ├── Symmetrical_Access_Stairs (Group: 2x 13-step external stair flights)
│   └── Indian_Flag_Emblem (DecalGeometry: lower 30° chamfer panel)
│
├── Modular_Container_Core (Group — Toggleable X-Ray Subsystem)
│   ├── Level0_Machinery_Block (MergedMesh: 3x CHP genset bays, workshop, water treatment)
│   ├── Level1_Living_Deck (MergedMesh: 24 crew cabins, dining mess, medical bay, ocean lounge)
│   └── Level2_Penthouse_Spine (MergedMesh: central stair hall & AHU plant)
│
├── MEP_Life_Support_Overlay (Group — SCADA Inspection Subsystem)
│   ├── HVAC_Supply_Ducts (MergedMesh: green #27AE60 supply network)
│   ├── HVAC_Return_Ducts (MergedMesh: yellow #F1C40F exhaust network)
│   ├── Hydronic_Heating_Loops (MergedMesh: red #E74C3C high-temp district heat)
│   └── Domestic_Water_Piping (MergedMesh: blue #2980B9 fresh & greywater lines)
│
└── Auxiliary_Site_Infrastructure (Group)
    ├── SATCOM_Geodesic_Radome (Mesh: 10.4m diameter icosahedron on ring truss)
    ├── Trace_Heated_Pipe_Rack (ExtrusionGeometry: pipeline tray on A-frames)
    ├── Helipad_Platform (Mesh: crushed-rock pad with H marking)
    ├── Logistics_Container_Depot (InstancedMesh: 25x colorful 20'/40' ISO containers)
    └── Larsemann_Terrain_Mesh (Displaced PlaneGeometry: bedrock & meltwater tarn)
```

---

## 3. Comprehensive PBR Material & Shader Palette

| Material Name | Base Color (Hex) | Roughness | Metalness | Special Shader Attributes | Real-World Component |
|:---|:---|:---:|:---:|:---|:---|
| **`AluminumFasciaMat`** | `#BAC4C7` | `0.28` | `0.80` | `clearcoat: 0.20` | Insulated exterior cassette skin |
| **`UnderbellyKeelMat`** | `#6E7D84` | `0.45` | `0.70` | Diffuse ambient shadow scattering | Tapered bottom wind shroud |
| **`ProwGlazingDayMat`** | `#1A312C` | `0.05` | `0.10` | `transmission: 0.85, ior: 1.52` | 6-bay panoramic observation glass |
| **`WindowEmissiveNightMat`**| `#FFAE33` | `0.20` | `0.00` | `emissive: #FF9900, intensity: 2.0` | 2700K tungsten nocturnal cabin glow |
| **`LabEmissiveNightMat`** | `#E6F2FF` | `0.20` | `0.00` | `emissive: #C8E2FF, intensity: 1.8` | 5000K daylight white lab glow |
| **`VStiltEpoxyMat`** | `#B0BFC5` | `0.25` | `0.85` | Smooth semi-gloss polyurethane | Fabricated box V-stilts |
| **`GalvanizedStairMat`** | `#CFD8DC` | `0.40` | `0.90` | Open zinc bar grating pattern | 13-step access stairways |
| **`RadomeFiberglassMat`** | `#E6EDED` | `0.35` | `0.05` | `flatShading: true` (geodesic facets) | 10.4m spherical SATCOM dome |
| **`GraniteBedrockMat`** | `#826B50` | `0.85` | `0.05` | Normal map: granite rock fractures | Larsemann Hills granitic gneiss |
| **`TarnWaterMat`** | `#1B4D72` | `0.02` | `0.10` | `transmission: 0.90, ior: 1.33` | Summer meltwater tarn lake |
| **`HVACSupplyMat`** | `#27AE60` | `0.30` | `0.20` | SCADA overlay: Fresh air supply | Green ventilation ducts |
| **`HydronicHeatMat`** | `#E74C3C` | `0.30` | `0.50` | SCADA overlay: CHP hot water | Red district heating loops |

---

## 4. Master Digital Twin Hotspot & Telemetry Registry

Every subsystem in the DTFIAS architecture maps directly to a verified 3D anchor coordinate `[X, Y, Z]` relative to station origin `(0, 0, 0)`:

| Hotspot ID | 3D Anchor `[x, y, z]` | Domain Subsystem | Associated Telemetry Sensors |
|:---|:---:|:---|:---|
| **`hotspot-power-plant`** | `[-19.2, 2.8, 7.2]` | Microgrid Energy | 3x Volvo Penta / Scania Gensets (kW load, RPM, oil temp, fuel flow) |
| **`hotspot-hvac`** | `[-7.2, 10.2, 0.0]` | Life Support & Hab | AHU supply temp, return air CO2 ppm, heat recovery efficiency % |
| **`hotspot-chp-heating`** | `[-6.0, 3.2, 0.0]` | District Heat | Primary/secondary hydronic loop temperatures, boiler pressure |
| **`hotspot-water-lss`** | `[-19.2, 2.8, -7.2]` | Environmental LSS | Snow melter tank volume (kL), MBR filtration flux, UV status |
| **`hotspot-workshop-garage`**| `[-18.0, 3.8, 0.0]` | Logistics & Fleet | PistenBully readiness, overhead crane status, garage bay door |
| **`hotspot-main-hab`** | `[0.0, 5.5, 0.0]` | Crew Quarters | 24 cabins occupancy, interior ambient temp (+21°C), fire loops |
| **`hotspot-dining-mess`** | `[-18.0, 6.5, 0.0]` | Living Operations | Galley power consumption, multi-year food stock inventory |
| **`hotspot-medical-bay`** | `[-14.4, 6.5, -7.2]` | Health & Telemed | Telemedicine uplink status, pharmacy cold-chain temperature |
| **`hotspot-ocean-lounge`** | `[19.0, 6.5, 0.0]` | Crew Welfare | Prow panoramic lounge, bar, solar radiation flux |
| **`hotspot-science-terrace`**| `[2.0, 11.5, 0.0]` | Science Operations | Rooftop radiation sensors, ozone spectrometer, cloud lidar |
| **`hotspot-meteo-mast`** | `[0.0, 13.5, 0.0]` | Meteorological | Wind speed (kts), wind direction, barometric pressure (hPa) |
| **`hotspot-v-stilts`** | `[18.5, 2.1, 0.0]` | Structural Health | Foundation strain gauges, hydraulic balance pressure (bar) |
| **`hotspot-satcom`** | `[-25.0, 7.2, 35.0]` | Telecommunications | GSAT-7A / ISRO C-band link signal-to-noise ratio, latency (ms) |
| **`hotspot-fuel-storage`** | `[-80.0, 4.0, -35.0]`| Logistics Fuel | 13x Jet A-1 fuel farm tanks (296 kL bulk reserves, fuel temp) |
| **`hotspot-pipe-rack`** | `[0.0, 0.8, 12.0]` | Infrastructure | Seawater intake heat-trace circuit status, pipe freeze alarm |
| **`hotspot-heliport`** | `[-85.0, 4.0, -95.0]`| Flight Operations | Helipad windsock, aviation fuel dispenser, Medevac flight log |

---

## 5. Frontend Runtime Implementation & Constraint C16

Project constraint **C16** strictly mandates that Three.js is never loaded in the base page waterfall. The 3D view must be dynamically injected upon user navigation:

```html
<!-- App Template: app/templates/bharati/station_twin.html -->
<div id="station-3d-container" class="relative w-full h-[720px] rounded-xl overflow-hidden bg-background select-none"
     x-data="{ viewMode: 'exterior', activeHotspot: null }"
     x-init="
       const script = document.createElement('script');
       script.src = '/static/js/three/station_3d_view.js';
       script.onload = () => {
         window.initStation3D('station-3d-container', {
           modelUrl: '/static/assets/models/bharati_base.glb',
           hotspots: window.BHARATI_HOTSPOTS
         });
       };
       document.body.appendChild(script);
     ">
  <!-- Interactive Viewport HUD Controls -->
  <div class="absolute top-4 left-4 z-20 flex gap-2">
    <button @click="set3DMode('exterior')" class="px-3 py-1 bg-surface-container rounded font-label-xs">EXTERIOR</button>
    <button @click="set3DMode('xray')" class="px-3 py-1 bg-surface-container rounded font-label-xs">X-RAY CONTAINER</button>
    <button @click="set3DMode('hvac')" class="px-3 py-1 bg-surface-container rounded font-label-xs">HVAC SCADA</button>
    <button @click="set3DMode('thermal')" class="px-3 py-1 bg-surface-container rounded font-label-xs">THERMAL MESH</button>
  </div>
</div>
```

---

## 6. Complete Documentation Registry

| Document File | Topic / Scope |
|:---|:---|
| **[`00_bharati_3d_master_specification.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/00_bharati_3d_master_specification.md)** | **Master 3D Specification & CAD Blueprint (This Document)** |
| [`01_construction_sequence_and_container_grid.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/01_construction_sequence_and_container_grid.md) | 134-Container Structural Core & 8-Phase CAD Assembly Sequence |
| [`02_aerial_masterplan_and_coastline.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/02_aerial_masterplan_and_coastline.md) | Masterplan Topography, Siting, Ridge Placement & Prydz Bay |
| [`03_southwest_roof_facets_and_penthouse.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/03_southwest_roof_facets_and_penthouse.md) | Multi-Planar Roof Envelope, Penthouse Terrace & South Ribbon |
| [`04_front_oblique_facade_and_v_stilts.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/04_front_oblique_facade_and_v_stilts.md) | Cantilevered Prow, 15° Raked Panoramic Window & Indian Insignia |
| [`05_twilight_operations_and_satcom_radome.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/05_twilight_operations_and_satcom_radome.md) | 10.4m Geodesic Radome & 2700K Tungsten Nocturnal Shaders |
| [`06_aurora_nocturnal_elevation_and_cargo_bay.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/06_aurora_nocturnal_elevation_and_cargo_bay.md) | Aurora Australis Atmosphere, Southern Elevation & Rear Shutter |
| [`07_rear_west_facade_and_vehicle_garage.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/07_rear_west_facade_and_vehicle_garage.md) | Western Logistics Facade, Roll-Up Garage & PistenBully Fleet |
| [`08_maritime_ice_harbor_and_resupply_logistics.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/08_maritime_ice_harbor_and_resupply_logistics.md) | *Ivan Papanin* Polar Cargo Vessel, Fast-Ice Berthing & Cranes |
| [`09_northwest_oblique_and_container_depot.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/09_northwest_oblique_and_container_depot.md) | 45° Aerodynamic Corner Chamfers, Stilt Forest & Container Yard |
| [`10_north_elevation_and_facade_rhythm.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/10_north_elevation_and_facade_rhythm.md) | True Orthographic North Elevation & 16-Pane Window Rhythm |
| [`11_cantilever_v_stilts_and_underbelly_aerodynamics.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/11_cantilever_v_stilts_and_underbelly_aerodynamics.md) | Quad Fabricated V-Stilts & Aerodynamic Dihedral Keel Shroud |
| [`12_panoramic_landscape_and_helipad_infrastructure.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/12_panoramic_landscape_and_helipad_infrastructure.md) | Helipad Staging, Helicopter Flight Approach & Regional Basin |
| [`13_conceptual_assembly_container_plus_skin.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/13_conceptual_assembly_container_plus_skin.md) | Architectural Concept (`container + skin`) & X-Ray Visualizer |
| [`14_prefabrication_and_shipping_logistics_workflow.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/14_prefabrication_and_shipping_logistics_workflow.md) | Prefabrication in Germany to Heavy Crawler Crane Polar Erection |
| [`15_structural_steel_framework_and_mep_bim_model.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/15_structural_steel_framework_and_mep_bim_model.md) | 3D MEP BIM Model: Steel Bents, HVAC Ducts & Hydronic Loops |
| [`16_container_cluster_and_exoskeleton_frame_integration.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/16_container_cluster_and_exoskeleton_frame_integration.md) | 11 Transverse Steel Portal Bents at 4.80m Cadence & Roof Deck |
| [`17_front_prow_cad_elevation_and_datums.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/17_front_prow_cad_elevation_and_datums.md) | Front Prow CAD Elevation, Datums H1–H4 & 13-Step Symmetrical Stairs |
| [`18_east_longitudinal_cad_elevation.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/18_east_longitudinal_cad_elevation.md) | True East Longitudinal CAD Elevation across Grid Axes 1–21 |
| [`19_level_0_ground_floor_cad_plan.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/19_level_0_ground_floor_cad_plan.md) | Level 0 Ground Floor CAD Plan: 3x CHP Gensets, Labs & Workshop |
| [`20_level_1_living_deck_cad_plan.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/20_level_1_living_deck_cad_plan.md) | Level 1 Living Deck CAD Plan: 24 Cabins, Dining, Hospital, Lounge |
| [`21_longitudinal_cad_section_a_a.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/21_longitudinal_cad_section_a_a.md) | Longitudinal CAD Section A-A: Exact Millimeter Vertical Datums |
| [`22_transverse_cad_section_b_b.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/bharati3d/22_transverse_cad_section_b_b.md) | Transverse CAD Section B-B: 3-Story Stair Hall & Wall Build-Up |
