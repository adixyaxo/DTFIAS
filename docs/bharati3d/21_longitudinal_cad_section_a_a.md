# 3D Modeling Analysis: Longitudinal CAD Section A-A

> **Source Image:** `images/bharati/download (18).webp`  
> **Target Path:** `docs/bharati3d/21_longitudinal_cad_section_a_a.md`  
> **Classification:** Official Architectural Working CAD Longitudinal Section Blueprint  
> **Subject Focus:** Centerline Cross-Section (Axes 1–21), Millimeter-Accurate Floor Datums, Double-Height Garage & Cantilever Balcony

---

## 1. Viewpoint & Document Calibration

* **Projection Type:** 2D Longitudinal Architectural Section (Section A-A).
* **Cut Plane:** Longitudinal centerline cutting from West (Axis 1) to East (Axis 21).
* **Significance for 3D Modeling:** Provides the **exact vertical floor thicknesses, ceiling heights, structural slab build-ups, and vertical circulation paths** required to model the station's 3D interior with zero geometric collision.

---

## 2. Longitudinal Sectional Architecture Breakdown

```
    [ H4: +11.580m Penthouse Roof ]
    ┌─────────────────────────┐
    │ Air Condition AHU Plant │ [ Level 2 Penthouse Deck: +8.948m ]
    │ & Central Stair Core    │ ┌─────────────────────────────────────────────────────┐ [ Roof Level: +8.413m ]
    ├─────────────────────────┴─┴─────────────────────────────────────────────────────┤
    │ Dining Hall │ Cold Store │ Central Stair │ Toilets │ Entertainment │ Lounge/Bar │ Balcony (Prow)
    ├─────────────┴────────────┼───────────────┼─────────┴───────────────┴────────────┤ [ Level 1 Floor: +4.842m / +5.103m ]
    │ DOUBLE-HEIGHT GARAGE     │ Workshop      │ Storage │ Biology Lab   │            │
    │ (Vehicle Overhead Crane) │               │         │ Corridor      │            │
    └──────────────────────────┴───────────────┴─────────┴───────────────┘            │ [ Level 0 Floor: +1.834m / +2.596m ]
    ═══════════════════════════════════════════════════════════════════════════════════
    [ Stilt Bearing: 0.000m ] ─── Bedrock Surface ───────────────────────────── [ Stilts: 17, 19, 21 ]
```

### 2.1. Exact Vertical Elevations & Slab Thicknesses
* **Penthouse Roof Apex:** `+11.580m` (H4).
* **Main Hull Roof Deck:** `+8.413m` (finished roof) to `+8.948m` (parapet edge) (H3).
* **Level 1 Finished Floor Level (FFL):** `+4.842m` (structural steel top) to `+5.103m` (interior floor finish) (H2).
  * Floor slab thickness: `0.261m` (composite steel deck + acoustic insulation + rubber screed).
  * Clear ceiling height in Level 1 cabins/labs: `~2.70m`.
* **Level 0 Finished Floor Level (FFL):** `+1.834m` (lower stilt platform) to `+2.596m` (interior slab) (H1).
  * Clear ceiling height in Level 0 machinery bays: `~2.25m`.
* **Double-Height Vehicle Garage (Axes 1–5):**
  * Spans from `+1.834m` ground slab up to `+4.842m` bottom of Level 1 floor, with a recessed vehicle pit dropping to `0.000m` bedrock.
  * Clear vertical hoist height: `~4.40m`, accommodating an overhead travelling crane.

### 2.2. Vertical Circulation Spine (Axes 8–10)
* **Tri-Level Open Stairwell:**
  * Connects Level 0 machinery deck to Level 1 living deck and Level 2 penthouse.
  * **Level 0 to Level 1 Flight:** 16 steps, rise = 16.17 cm, tread = 27.0 cm.
  * **Level 1 to Level 2 Flight:** 17 steps, rise = 17.5 cm, tread = 28.0 cm.
* **Rooftop Exit:** The stairwell terminates in an enclosed vestibule on Level 2 opening directly onto the outdoor observation terrace.

### 2.3. Cantilevered Prow & Balcony (Axes 16–21)
* **Overhang Geometry:** Level 1 projects forward `12.0 meters` past the Level 0 foundation wall.
* **Terminus Balcony:** Features an enclosed glass-faced forward observation balcony (`balcony`) with an inward-raked 15° window wall at Axis 21.

---

## 3. Quantitative 3D Section Datums Table

| Architectural Level | Elevation Above Ground (Z-Up in CAD, Y-Up in Three.js) | Structural Feature |
|:---|:---|:---|
| **Level 2 Roof Deck** | `+11.580m` | Penthouse roof and exhaust flues |
| **Level 2 Terrace Deck**| `+8.948m` | Rooftop observation walking surface |
| **Main Station Roof** | `+8.413m` | Upper living deck ceiling plane |
| **Level 1 Finished Floor**| `+5.103m` | Main living and operations deck |
| **Level 0 Finished Floor**| `+2.596m` | Ground machinery and workshop floor |
| **Underbelly Keel Lowest**| `+1.834m` | Bottom of insulated under-chassis pan |
| **Bedrock Ground Datum** | `0.000m` | Natural Larsemann granite surface |

---

## 4. Digital Twin Hotspot Anchors

| Subsystem Anchor | Local Coordinate `[x, y, z]` | Description |
|:---|:---|:---|
| **`garage_overhead_crane`**| `[-18.0, 4.2, 0.0]` | Double-height garage crane load monitoring. |
| **`ahu_penthouse_room`** | `[-7.2, 10.2, 0.0]` | Level 2 central air conditioning and ventilation plant. |
| **`central_stairwell_riser`**| `[-4.8, 6.5, 0.0]` | Vertical circulation fire-door and egress monitoring. |
| **`prow_observation_balcony`**| `[23.0, 6.5, 0.0]` | Eastern prow panoramic glass observation balcony. |
