# 3D Modeling Analysis: Level 0 Ground Floor CAD Plan

> **Source Image:** `images/bharati/download (16).webp`  
> **Target Path:** `docs/bharati3d/19_level_0_ground_floor_cad_plan.md`  
> **Classification:** Official Architectural Working CAD Floor Plan Blueprint  
> **Subject Focus:** Level 0 Machinery Core, 3x CHP Diesel Gensets, Water Treatment, Laboratories & Vehicle Workshop

---

## 1. Viewpoint & Document Calibration

* **Projection Type:** 2D Architectural CAD Floor Plan (Level 0 / Ground Deck).
* **Reference System:** Grid Axes **1 to 21** (Longitudinal) × Grid Axes **A to E** (Transverse).
* **Significance for 3D Modeling:** This plan provides the exact **interior room bounding boxes, partition wall layout, and machinery placements** for the lower deck of the 3D digital twin.

---

## 2. Functional Zonation & Room Ledger (Level 0)

```
       1      2      3      4      5      6      7      8      9     10     11     12     13     14     15     16  17  18  19  20  21
  A ┌──────────────────────────────────────────────────────────┬──────────────────────────────────────────┐
    │ Waste   Grey   Water   Water               Vestibule     │ Storage   Laboratory   Laboratory        │
    │ Water   Water  Storage Dist.               (Entrance)    │           Meteorology  Geomagnetism      │
  B ├─────────────────────────────────────┬──────────────┬─────┴──────────────────────────────┬───────────┤
    │                                     │              │                                    │ Biology & │
    │       VEHICLE WORKSHOP & GARAGE     │   Workshop   │         STORAGE & AIRLOCKS         │ Environm. │
    │   (Tracked Polar Snowcat Bay)       │              │                                    │           │
  D ├─────────────────────────────────────┴──────────────┼─────┬──────────────────────────────┴───────────┤
    │ Generator 1  | Generator 2  | Generator 3  | Day   │     │ Storage   Earth Science  Physiology  │
    │ (Volvo/Scania 320kVA CHP)   | (Firewall 90 min)    │     │           Laboratory     Laboratory  │
  E └────────────────────────────────────────────────────┴─────┴──────────────────────────────────────────┘
```

### 2.1. Sector 1: Microgrid & Energy Generation (Axes 1–5, D–E)
* **Equipment Allocation:**
  * **Generator 1 (`G`), Generator 2 (`G`), Generator 3 (`G`):** Three heavy-duty polar diesel gensets (Volvo Penta D13 / Scania DC13, 320 kVA each) positioned in separate acoustically insulated, 90-minute fire-rated bays.
  * **Fuel Day Tank Room:** Directly adjacent to Generator 3, holding buffered Jet A-1 fuel for immediate generator feeding.

### 2.2. Sector 2: Mechanical Workshop & Vehicle Garage (Axes 1–5, B–D)
* **Garage Footprint:** Accommodates a full-size tracked PistenBully or snowmobile fleet for maintenance.
* **Overhead Crane Hoist:** Structural I-beam hoist tracks (`DEMAG` overhead travelling crane) spanning the ceiling of the workshop for engine swaps.
* **External Roll-up Door:** Direct vehicular exit to the western snow ramp on Axis 1.

### 2.3. Sector 3: Life Support & Water Management (Axes 1–5, A–B)
* **Water Treatment Plant:**
  * Raw water storage tanks (heated snow melter tanks).
  * Greywater recycling filtration system.
  * Membrane Bioreactor (MBR) sewage and wastewater treatment plant.

### 2.4. Sector 4: Central Circulation & Cargo Hoist (Axes 8–10, A–E)
* **Central Stairwell:** Tri-level open steel staircase connecting Level 0 to Level 1 and Level 2.
* **Vertical Cargo Lifting Hatch:** A 2.0m × 2.0m floor hatch with hoist crane allowing heavy equipment to be lifted directly from the ground workshop into the Level 1 storage area.

### 2.5. Sector 5: Scientific Laboratory Wing (Axes 11–16, A–E)
* **Meteorology Laboratory:** North perimeter bay with automated weather sensor consoles.
* **Geomagnetism Laboratory:** Magnetometer data logging terminal.
* **Biology & Environmental Science Lab:** Clean benches, sample incubators, and fume hoods.
* **Earth Science & Human Physiology Lab:** Medical telemetry consoles and seismic logging terminals.

---

## 3. Quantitative 3D Interior Bounding Boxes

| Room / Subsystem | Grid Range | Bounding Box Dimensions (L × W × H) | Center Position `[x, y, z]` |
|:---|:---|:---|:---|
| **Generator Bay (3x Gensets)**| Axes 1–5, D–E | `9.6m × 4.8m × 3.2m` | `[-19.2, 3.4, 7.2]` |
| **Vehicle Workshop / Garage** | Axes 1–5, B–D | `12.0m × 8.0m × 4.2m` | `[-18.0, 3.8, 0.0]` |
| **Water Treatment Plant** | Axes 1–5, A–B | `9.6m × 4.8m × 3.2m` | `[-19.2, 3.4, -7.2]` |
| **Central Stair & Vestibule** | Axes 8–10, B–D | `4.8m × 8.0m × 3.5m` | `[-4.8, 3.5, 0.0]` |
| **Meteorology & Geo Labs** | Axes 11–15, A–B | `12.0m × 4.8m × 3.0m` | `[+4.8, 3.5, -7.2]` |
| **Earth & Physiology Labs** | Axes 11–15, D–E | `12.0m × 4.8m × 3.0m` | `[+4.8, 3.5, +7.2]` |

---

## 4. Digital Twin Hotspot Anchors

| Subsystem Anchor | Local Coordinate `[x, y, z]` | Description |
|:---|:---|:---|
| **`genset_01_scada`** | `[-21.6, 2.8, 7.2]` | Microgrid generator 01 operational telemetry. |
| **`genset_02_scada`** | `[-19.2, 2.8, 7.2]` | Microgrid generator 02 operational telemetry. |
| **`genset_03_scada`** | `[-16.8, 2.8, 7.2]` | Microgrid generator 03 operational telemetry. |
| **`mbr_sewage_treatment`** | `[-21.6, 2.8, -7.2]`| Environmental Madrid Protocol wastewater plant. |
| **`snow_melter_tank`** | `[-16.8, 2.8, -7.2]`| Potable water reserves and thermal melting coils. |
| **`meteo_science_lab`** | `[4.8, 3.5, -7.2]` | Real-time atmospheric sensor data hub. |
