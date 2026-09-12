# 3D Modeling Analysis: Rear West Facade & Vehicle Garage

> **Source Image:** `images/bharati/download (4).webp`  
> **Target Path:** `docs/bharati3d/07_rear_west_facade_and_vehicle_garage.md`  
> **Classification:** Ground-Level Architectural Elevation & Logistics Portal  
> **Subject Focus:** Rear Logistics Facade, Roll-Up Garage Door, Meltwater Tarn Mirror Reflection & Vehicle Assets

---

## 1. Viewpoint & Perspective Calibration

* **Projection Type:** Eye-Level Ground Perspective (~35mm focal length).
* **Camera Position:** Stationed on the western shoreline of the glacial meltwater tarn, ~65m West of the station, looking East toward the rear facade.
* **Aspect Ratio:** Standard 3:2 landscape photograph.
* **Lighting & Reflections:** Clear summer polar sunlight (zenith angle ~40°) casting sharp, short shadows toward the southeast. The glassy, mirror-still surface of the meltwater tarn in the foreground provides a near-perfect vertical reflection of the station.

---

## 2. Architectural & Engineering Breakdown

```
                         [ Penthouse Observation Core ]
                         ┌────────────────────────────┐
                         │   Antenna Mast & Vents     │
    ┌────────────────────┴────────────────────────────┴────────────────────┐
    │                       WESTERN REAR ROOF BEVEL                        │
    ├──────────────────┬────────────────────────────────┬──────────────────┤
    │                  │  [|][|][|][|][|][|][|][|][|]   │                  │
    │  Solid Chamfer   │  10-BAY VERTICAL REAR WINDOWS  │  Solid Chamfer   │
    │  Corner Panel    │  (Inward Rake Angle ~15°)      │  Corner Panel    │
    ├──────────────────┴──────────────┬─────────────────┴──────────────────┤
    │                                 │                                    │
    │                                 │  [||||||||||||]                    │
    │                                 │  HEAVY-DUTY VEHICLE GARAGE DOOR    │
    │                                 │  (Roll-Up Segmented Shutter)       │
    └─────────────────────────────────┴────────────────────────────────────┘
    ════════════════════════════════════════════════════════════════════════ Granitic Berm
                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Mirror Water Reflection
```

### 2.1. Rear Facade Symmetrical Hierarchy
* **Contrasting Prow Design:** Unlike the ocean-facing eastern prow (which has an open panoramic view and high V-stilt cantilever), the western rear facade is configured as a fortified, heavily insulated logistics and workshop portal.
* **Level 0 Ground Vehicle Portal:**
  * Accommodates a motorized overhead sectional roll-up garage door (~4.5m W × 3.5m H).
  * Designed to permit PistenBully tracked vehicles, snowmobiles, and forklifts to drive directly into the heated ground workshop bay.
* **Level 1 Rear Window Matrix:**
  * 10 tall, narrow vertical window lights (~1.8m H × 0.8m W each) clustered in the central bay above the garage door.
  * Inward rake angle (~15°) matches the aerodynamic envelope logic of the front prow.

### 2.2. Auxiliary Logistics Equipment & Fleet Assets
1. **PistenBully Polar Snowcats:**
   * Two units visible: High-visibility polar red bodies (`#D62828`), black rubberized track belts, enclosed heated cabs with searchlight bars.
   * Dimensions: ~6.2m L × 2.5m W × 2.8m H.
2. **Rough-Terrain Telehandler:**
   * Heavy-duty all-terrain telescopic forklift in industrial safety yellow (`#F4A900`), mounted on massive deep-tread pneumatic tires.
   * Used for offloading shipping containers and heavy machinery.
3. **ISO Shipping Container Staging:**
   * Standard 20ft intermodal dry-van containers (two deep maritime blue, one logistics orange) placed on the gravel pad to the north of the vehicle portal.

### 2.3. Water Reflection Modeling Value
* The mirror reflection in the tarn allows cross-checking of underbelly geometry: confirms the smooth underside cladding and symmetrical bevel transitions along the keel line.

---

## 3. Quantitative 3D Metrics & Proportions

| Feature | Estimated Measurement | Three.js World Units (1u = 1m) |
|:---|:---|:---|
| **Rear Facade Total Width** | ~20.0m | `width: 20.0` |
| **Ground Garage Shutter Door** | 4.5m W × 3.5m H | `x: 4.5, y: 3.5` |
| **Level 1 Rear Window Gallery** | 10 bays, 8.5m total width | `width: 8.5, height: 1.8` |
| **North Longitudinal Window Count** | 12 visible window bays | Spanning westward from center |
| **PistenBully Snowcat Bounding Box** | 6.2m L × 2.5m W × 2.8m H | Instanced mesh scale |
| **Telehandler Forklift Bounding Box** | 5.8m L × 2.4m W × 2.6m H | Instanced mesh scale |
| **Meltwater Tarn Shoreline Offset** | ~25m west of building corner | Water plane boundary |

---

## 4. Materials, PBR Shaders & Color Palette

```
Hex Color Reference:
Aluminum Shell (Shadowed):  #626F74  (Cool neutral metallic gray)
Aluminum Shell (Sunlit):    #B0BCC2  (Bright specular satin aluminum)
Garage Shutter Door:        #4F585C  (Industrial matte steel gray)
PistenBully Vehicle Red:    #D62828  (High-visibility polar rescue red)
Telehandler Forklift:       #F4A900  (Safety amber-yellow)
Shipping Container Blue:    #004B87  (Marine cobalt blue)
Meltwater Tarn Water:       #1B4D72  (Deep azure-blue mirror reflection)
Granite Gravel Berm:        #8C7355  (Warm crushed granite aggregate)
```

* **Meltwater Tarn Water Shader:**
  * Material: Three.js `Water` shader (from `three/addons/objects/Water.js`) or a flat `MeshStandardMaterial` with `roughness: 0.02`, `metalness: 0.1`, and a planar reflection probe.
* **Vehicle Asset Shader:**
  * Clearcoat paint shader (`clearcoat: 0.8`, `clearcoatRoughness: 0.2`) on the PistenBully red body shell.

---

## 5. Three.js Scene Graph Hierarchy & Asset Placement

```
BharatiStation (Root Group)
├── Logistics_Terminal_West (Subgroup)
│   ├── Vehicle_Garage_Door (Mesh: Segmented BoxGeometry)
│   ├── Rear_Window_Gallery (Mesh: Inward-raked 10-pane array)
│   └── Access_Ramp_Berm (Mesh: Crushed rock ramp)
├── Vehicle_Fleet (Group)
│   ├── PistenBully_01 (Position: [-18.0, 0.0, 8.0], Rotation: -30°)
│   ├── PistenBully_02 (Position: [-24.0, 0.0, -2.0], Rotation: 15°)
│   └── Telehandler_01 (Position: [-16.5, 0.0, 4.0], Rotation: 45°)
└── Tarn_Water_Plane (Mesh: PlaneGeometry at Y = -1.2m)
```

---

## 6. Digital Twin Hotspot & Subsystem Anchors

| Subsystem Anchor | World Coordinate `[x, y, z]` | Description |
|:---|:---|:---|
| **`workshop_garage`** | `[-20.0, 1.8, 0.0]` | Mechanical maintenance workshop and vehicle airlock. |
| **`pistenbully_fleet`** | `[-20.0, 1.0, 6.0]` | Polar traverse vehicles and telemetry gateway. |
| **`heavy_cargo_staging`** | `[-26.0, 0.5, -8.0]`| Containerized supply depot and spare parts storage. |
| **`tarn_water_intake`** | `[-35.0, -1.2, 0.0]`| Summer freshwater source monitoring node. |
