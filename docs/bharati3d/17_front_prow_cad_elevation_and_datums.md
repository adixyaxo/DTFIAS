# 3D Modeling Analysis: Front Prow CAD Elevation & Datum Grid

> **Source Image:** `images/bharati/download (14).webp`  
> **Target Path:** `docs/bharati3d/17_front_prow_cad_elevation_and_datums.md`  
> **Classification:** Official Architectural Working CAD Elevation / Cross-Sectional Blueprint  
> **Subject Focus:** Front Prow Proportions, Datums H1–H4, Structural Axes E'–A' & Symmetrical Access Stairs

---

## 1. Viewpoint & Document Calibration

* **Projection Type:** Pure 2D Orthographic Front Elevation CAD Drawing (*bof architekten / IMS*).
* **Viewing Vector:** Looking directly West along the longitudinal centerline (facing the ocean-facing prow).
* **Grid Coordinate Axes:**
  * Horizontal Level Datums: `H1`, `H2`, `H3`, `H4`.
  * Transverse Column Grid: `E'`, `E`, `D'`, `D`, `C` (centerline), `B`, `B'`, `A`, `A'`.
* **Significance for 3D Modeling:** Establishes the exact transverse profile curves, bevel angles, window mullions, and stilt bearings for the 3D digital twin.

---

## 2. Orthographic Architectural Breakdown

```
                                            [ H4: +11.58m Penthouse Apex ]
                                            ┌────────────────────────────┐
                                            │ Penthouse Terrace & Rail   │
    ┌───────────────────────────────────────┴────────────────────────────┴───────────────────────────────────────┐ [ H3: +8.95m Roof Deck ]
    │  [ Blind Corner ]  [          6-BAY PANORAMIC PROW GLAZING         ]  [ Blind Corner ]                    │
    ├───────────────────┬─────────────────────────────────────────────────┬─────────────────────────────────────┤ [ H2: +5.10m Level 1 Floor ]
    │                   │   Level 0 Recessed Utility Windows (Underbelly) │                                     │
    └───┬───────────────┴───────────────┬─────────────────┬───────────────┴───────────────┬─────────────────────┘ [ H1: +2.60m Level 0 Stilt Bearing ]
       / \                             / \               / \                             / \
      /   \                           /   \             /   \                           /   \
     /     \                         /     \           /     \                         /     \
  [13-Step Stair]              [Axis D': V-Stilt] [Axis C: Center]  [Axis B': V-Stilt]   [13-Step Stair]
  (18/28cm Rise/Tread)                                                                   (18/28cm Rise/Tread)
  ───┴─────────────────────────────┴───────────────┴───────────────┴─────────────────────┴────────────────────── 0.00m Bedrock
     E'          E                 D'              D   C   B               B'            A           A'
```

### 2.1. Horizontal Elevation Datums
* **`H4` (Penthouse Apex):** `+11.58m` above natural bedrock. Apex of central observation roof.
* **`H3` (Main Living Roof Deck):** `+8.95m`. Top of Level 1 ceiling and roof fascia.
* **`H2` (Level 1 Finished Floor):** `+5.10m`. Main living and laboratory deck.
* **`H1` (Level 0 Stilt Base Bearing):** `+2.60m`. Underbelly stilt connection plate elevation.
* **`0.00m` (Ground Datum):** Natural Larsemann Hills granitic bedrock.

### 2.2. Transverse Grid Alignment (Axes E' through A')
* **Total Transverse Width:** Approximately **20.0m** from outer bevel tip `E'` to `A'`.
* **Structural Prow V-Stilts:** Located at Grid Axes **`D'`** and **`B'`**, forming structural A-frames/V-frames supporting the Level 1 cantilever.
* **Vertical Intermediate Stilts:** Located at Grid Axes **`E`**, **`D`**, **`C`** (centerline), **`B`**, and **`A`**.
* **External Symmetrical Access Stairs:**
  * Two identical industrial steel staircases descend symmetrically from the Level 1 access airlocks on axes `E–E'` and `A–A'`.
  * **Stair Cadence:** Exactly **13 steps**, rise = **18 cm**, tread = **28 cm** (total rise = 2.34m, slope = 32.7°).

### 2.3. Front Prow Envelope & Fenestration
* **Central Panoramic Window:** 6 tall vertical glass bays centered on Axis `C` (between axes `D` and `B`).
* **Flanking Chamfered Return Panels:** Opaque insulated panels on the outer flanks (between `E'–D` and `B–A'`).
* **Penthouse Observation Terrace:** Features a continuous horizontal ventilation louver grille and steel perimeter safety handrail on datum `H3`–`H4`.

---

## 3. Quantitative 3D Vector Vertices (Front Profile)

For procedural Three.js `Shape` modeling:

| Vertex Point | Local X (Transverse) | Local Y (Elevation) | Description |
|:---|:---|:---|:---|
| **P1** (Keel Bottom) | `0.0m` | `+2.60m` (H1) | Central underbelly lowest point |
| **P2** (Port Chine) | `-7.5m` | `+3.40m` | Transverse stilt haunch junction |
| **P3** (Port Outer Bevel) | `-10.0m` | `+5.10m` (H2) | Widest outer hull corner point |
| **P4** (Port Top Fascia) | `-9.5m` | `+8.95m` (H3) | Upper roof fascia corner |
| **P5** (Port Roof Ridge) | `-5.0m` | `+10.10m` | Main hipped roof slope transition |
| **P6** (Penthouse Port) | `-3.8m` | `+11.58m` (H4) | Penthouse roof top corner |
| **P7** (Penthouse Starboard)| `+3.8m` | `+11.58m` (H4) | Penthouse roof top corner |
| **P8** (Starboard Ridge) | `+5.0m` | `+10.10m` | Main hipped roof slope transition |
| **P9** (Starboard Fascia) | `+9.5m` | `+8.95m` (H3) | Upper roof fascia corner |
| **P10** (Starboard Outer) | `+10.0m` | `+5.10m` (H2) | Widest outer hull corner point |
| **P11** (Starboard Chine) | `+7.5m` | `+3.40m` | Transverse stilt haunch junction |

---

## 4. Digital Twin Hotspot Anchors

| Subsystem Anchor | World Coordinate `[x, y, z]` | Description |
|:---|:---|:---|
| **`prow_panoramic_center`** | `[24.0, 6.5, 0.0]` | Front 6-bay panoramic observation node. |
| **`staircase_port_access`** | `[18.0, 2.3, 9.5]` | 13-step external personnel entrance stairs. |
| **`staircase_stbd_access`** | `[18.0, 2.3, -9.5]`| 13-step external personnel entrance stairs. |
| **`v_stilt_b_prime`** | `[18.5, 1.3, -5.0]`| Structural load cell at Grid Axis B'. |
| **`v_stilt_d_prime`** | `[18.5, 1.3, 5.0]` | Structural load cell at Grid Axis D'. |
