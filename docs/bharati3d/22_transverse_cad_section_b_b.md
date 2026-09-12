# 3D Modeling Analysis: Transverse CAD Section B-B

> **Source Image:** `images/bharati/download (19).webp`  
> **Target Path:** `docs/bharati3d/22_transverse_cad_section_b_b.md`  
> **Classification:** Official Architectural Working CAD Transverse Section Blueprint  
> **Subject Focus:** Transverse Cross-Section (Axes E'–A'), Central Stair Hall, Multi-Layer Wall Insulation Build-Up & Symmetrical Entrances

---

## 1. Viewpoint & Document Calibration

* **Projection Type:** 2D Transverse Architectural Section (Section B-B).
* **Cut Plane:** Transverse vertical plane along Grid Axis 9, cutting across the full 20.0m width from South (Axis E) to North (Axis A).
* **Significance for 3D Modeling:** Provides the definitive **wall assembly material build-up, insulation thicknesses, central stairwell cross-section, and symmetrical exterior access stairs**.

---

## 2. Transverse Sectional Architecture Breakdown

```
                                            [ H4: +11.58m Penthouse Roof ]
                                            ┌────────────────────────────┐
                                            │ Level 2 Penthouse Stairwell│
    ┌───────────────────────────────────────┴────────────────────────────┴───────────────────────────────────────┐ [ H3: +8.95m Roof Deck ]
    │   [ South Living/Office ]   │        CENTRAL 3-STORY OPEN          │   [ North Living Cabin ]             │
    │   Cabin Volume              │        STAIRWELL HALL                │   Cabin Volume                       │
    ├─────────────────────────────┼──────────────────────────────────────┼──────────────────────────────────────┤ [ H2: +5.10m Level 1 Floor ]
    │   [ South Vestibule Entry ] │        Level 0 Lower Circulation     │   [ North Vestibule Entry ]          │
    └───┬─────────────────────────┴──────────────────────────────────────┴──────────────────────────┬────────────┘ [ H1: +2.60m Stilt Level ]
       / \                                                                                         / \
      /   \                                                                                       /   \
  [South 13-Step Stair]                                                                       [North 13-Step Stair]
  (18/28cm Rise/Tread)                                                                        (18/28cm Rise/Tread)
  ───┴───────────────────────────────────────┬─────────────────────────────────────────────────────┴──────────── 0.00m Bedrock
     E'          E                           C (Centerline)                                        A          A'
```

### 2.1. Central Stair Hall & Internal Circulation
* **Open Central Atrium:** A full-height open stairwell centered on Axis `C` (between axes `D` and `B`), functioning as the primary vertical spine for personnel and thermal chimney ventilation.
* **Corridor Symmetry:** Symmetrical internal corridors on Level 1 (width = `1.80m`) flanked by container cabins along the outer walls.

### 2.2. Multi-Layer Wall Assembly Build-Up (Material Specification)
Annotated directly on the drawing, the wall construction follows a rigorous high-performance thermal insulation specification:
1. **Interior Finish:** `3mm` heavy-duty non-slip rubber / linoleum flooring + `18mm` gypsum fiberboard lining.
2. **Acoustic Dampening:** `50mm` high-density acoustic sound insulation batting.
3. **Sub-floor Sheathing:** `20mm` structural timber planks with elastomeric airtight vapor barrier.
4. **Thermal Core:** `190mm` high-performance rigid mineral wool insulation (`λ ≈ 0.034 W/mK`).
5. **Structural Container Shell:** `2.0mm` corrugated Cor-Ten weather-resistant steel container wall.
6. **Thermal Buffer Cavity:** `600mm – 800mm` ventilated air gap within the structural steel bent spaceframe.
7. **Exterior Cladding:** `80mm` insulated aluminum sandwich cassette panels with fluoropolymer anti-weathering coating.

### 2.3. Symmetrical North & South Exterior Access Stairs
* Two identical industrial stair flights flank the station on axes `E–E'` (South) and `A–A'` (North):
  * **Step Dimensions:** Exactly **13 risers**, rise = **18.17 cm**, tread = **27.0 cm – 28.0 cm**.
  * **Handrails:** Tubular galvanized steel safety railings with mid-rail and kickplate.

---

## 3. Quantitative Transverse Dimensions Table

| Transverse Datum | Grid Axis | Distance from Centerline (X) | Elevation (Y) |
|:---|:---|:---|:---|
| **Centerline Axis C** | `C` | `0.0m` | Transverse center |
| **Inner Stilt / Wall Line** | `D` / `B` | `±4.80m` | `y: 2.6m -> 11.58m` |
| **Outer Container Wall Line**| `E` / `A` | `±8.40m` | `y: 2.6m -> 8.95m` |
| **Outer Chamfer Chine** | `E'` / `A'` | `±10.0m` | `y: 5.10m` (Maximum hull width = 20.0m) |
| **Exterior Stair Footing** | Beyond `E'` / `A'` | `±12.4m` | `y: 0.0m` bedrock touch-down |

---

## 4. Digital Twin Hotspot Anchors

| Subsystem Anchor | Local Coordinate `[x, y, z]` | Description |
|:---|:---|:---|
| **`atrium_central_stairwell`**| `[-4.8, 6.5, 0.0]` | Central vertical circulation and fire safety door node. |
| **`south_vestibule_airlock`** | `[-4.8, 3.8, 7.2]` | South exterior personnel entry and muster point. |
| **`north_vestibule_airlock`** | `[-4.8, 3.8, -7.2]`| North exterior personnel entry and muster point. |
| **`wall_thermal_flux_sensor`**| `[-4.8, 6.5, -9.8]`| Envelope thermal gradient and U-value sensor probe. |
