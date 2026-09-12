# 3D Modeling Analysis: East Longitudinal CAD Elevation

> **Source Image:** `images/bharati/download (15).webp`  
> **Target Path:** `docs/bharati3d/18_east_longitudinal_cad_elevation.md`  
> **Classification:** Official Architectural Working CAD Elevation Blueprint  
> **Subject Focus:** Longitudinal Profile (Grid Axes 1–21), Central Entrance Airlock, Roof Penthouse & Stilt Column Spacing

---

## 1. Viewpoint & Document Calibration

* **Projection Type:** Pure 2D Orthographic Longitudinal Elevation CAD Drawing (*bof architekten / IMS*).
* **Drawing Title:** `ELEVATION EAST`.
* **Grid Coordinate Axes:** 21 primary structural grid axes numbered **1 through 21** spaced along the 50.0m hull length.
* **Significance for 3D Modeling:** The definitive longitudinal CAD blueprint defining the spacing of all 11 structural bents, the exact position of the "Bharati" main entrance portal, chimney stacks, and stilt columns.

---

## 2. Longitudinal Architectural Breakdown (Grid Axes 1 to 21)

```
                              [ Axes 6-9: Penthouse ]   [ Axes 9-14: Terrace Deck ]
                              ┌─────────────────────┐   ┌─────────────────────────┐
                              │ 3x Exhaust Chimneys │   │ Observation Guardrail   │
    ┌─────────────────────────┴─────────────────────┴───┴─────────────────────────┴─────────────────────────┐
    │ [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]   │ (Window Ribbon)
    ├───────────────────────────────────────────┬───────────────────────────────────────────────────────────┤
    │                                           │  [ BHARATI ] Main Entrance Airlock                        │
    │  [ Ground Utility / Generator Bay ]       │  [ STAIRS  ] External Steel Flight                        │
    └───┬───────────┬───────────┬───────────┬───┴─────┬─────────────────┬───────────┬───────────┬───────────┘
        │           │           │           │         │                 │           │           │
     Axis 1      Axis 2      Axis 3      Axis 4    Axis 8            Axis 17     Axis 19     Axis 21
    [ ── Level 0 Ground Utility Footprint ── ]             [ ── Open Air Cantilever Underbelly ── ]
```

### 2.1. Structural Grid Rhythm (Axes 1 to 21)
* **Overall Span:** Exactly **50.0m** from outer nose tip at Axis 1 to prow tip at Axis 21.
* **Bay Spacing:** Uniform grid spacing of **2.40m** between numbered grid axes (`21 axes × 2.40m ≈ 48.0m` + overhangs).
* **Structural Bento Alignments (11 Bents):**
  * Portal bents are placed on alternating axes: Axis 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21.

### 2.2. Functional Zonation Along Longitudinal Axis
1. **Axes 1–5 (Western Substructure):**
   * Level 0 is enclosed, housing the heavy workshop, emergency garage, and 3x diesel generator sets.
   * Short vertical stilts resting directly on bedrock.
2. **Axes 6–9 (Central Mechanical Core & Penthouse):**
   * Central core rising to `+11.58m` apex.
   * Houses central stairwell, air conditioning plant, and 3x vertical exhaust flues protruding from the roof.
3. **Axes 8–9 (Main Station Entrance Portal):**
   * Centrally located ground-level airlock vestibule with high-contrast dark portal frame.
   * Clearly marked with institutional lettering: **`Bharati`**.
   * Served by an exterior steel access staircase with intermediate landing.
4. **Axes 9–14 (Rooftop Science Observation Terrace):**
   * Flat walking deck on Level 2 with galvanized steel perimeter handrails.
5. **Axes 15–21 (Eastern Cantilever Lounge & Open Underbelly):**
   * Level 0 is entirely open underneath to allow unimpeded katabatic wind passage.
   * Long cylindrical foundation stilts on Axes 17, 19, and 21 supporting the overhanging living deck and panoramic prow.

---

## 3. Quantitative 3D Modeling Dimensions

| Grid Range | Structural Function | Longitudinal Offset (X) | Elevation (Y) |
|:---|:---|:---|:---|
| **Axis 1** | Western hull nose tip | `x = -24.0m` | `y: 4.2m -> 10.0m` |
| **Axes 1–5** | Level 0 Generator / Workshop | `x = -24.0m to -14.4m` | `y: 0.0m -> 4.2m` |
| **Axes 6–9** | Penthouse AHU / Chimneys | `x = -12.0m to -4.8m` | `y: 10.0m -> 11.58m` |
| **Axes 8–9** | "Bharati" Main Entrance Door | `x = -7.2m to -4.8m` | `y: 2.6m -> 5.1m` |
| **Axes 9–14** | Roof Observation Terrace | `x = -4.8m to +7.2m` | `y: 8.95m -> 10.05m` |
| **Axes 15–21** | Open Air Cantilever Underbelly | `x = +9.6m to +24.0m` | `y: 0.0m -> 4.8m` (Clearance) |
| **Axis 21** | Eastern prow tip | `x = +24.0m` | `y: 4.2m -> 10.0m` |

---

## 4. Digital Twin Hotspot Anchors

| Subsystem Anchor | World Coordinate `[x, y, z]` | Description |
|:---|:---|:---|
| **`main_entrance_bharati`** | `[-6.0, 3.8, 10.0]` | Main station entrance airlock with "Bharati" signage. |
| **`chp_chimneys_axes_6_7`** | `[-9.6, 12.2, 3.5]` | 3x generator exhaust thermal emission sensors. |
| **`stilt_column_axis_17`** | `[14.4, 2.2, 8.5]` | Eastern cantilever primary load cell column. |
| **`stilt_column_axis_21`** | `[24.0, 2.4, 0.0]` | Front prow terminal foundation bearing. |
