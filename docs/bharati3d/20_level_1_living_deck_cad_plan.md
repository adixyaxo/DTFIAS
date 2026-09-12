# 3D Modeling Analysis: Level 1 Living Deck CAD Plan

> **Source Image:** `images/bharati/download (17).webp`  
> **Target Path:** `docs/bharati3d/20_level_1_living_deck_cad_plan.md`  
> **Classification:** Official Architectural Working CAD Floor Plan Blueprint  
> **Subject Focus:** Level 1 Living & Operations Deck, 24 Crew Cabins, Dining Mess, Medical Bay, Sauna & Ocean Lounge

---

## 1. Viewpoint & Document Calibration

* **Projection Type:** 2D Architectural CAD Floor Plan (Level 1 / Main Living Deck).
* **Reference System:** Grid Axes **1 to 21** (Longitudinal) × Grid Axes **A to E** (Transverse).
* **Significance for 3D Modeling:** This plan defines the complete **interior living quarters, 24 individual cabins, medical facilities, communal dining, and panoramic ocean lounge** for the interior 3D digital twin.

---

## 2. Functional Layout & Spatial Distribution (Level 1)

```
       1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19    20    21
  A ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │ Gym        │ Medical Room       │Prayer│ Cab │ Cab │ Cab │ Cab │ Cab │ Cab │ Cab │ Cab │ Cab │ Cab │ Cab │ Cab │ Cab │ (13 North
  B ├────────────┴────────────────────┴──────┼─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┤  Cabins)
    │                                        │                   │ Sauna │ Entertainment │                             │
    │          COMMUNAL DINING MESS          │  Kitchen & Pantry │ Toilet│ Hall / Cinema │      PANORAMIC OCEAN        │
    │             (36 Seats)                 │  Cold Storage     │Laundr.│ (Auditorium)  │       LOUNGE & BAR          │
  D ├────────────┬───────────┬───────────────┼─────┬─────┬─────┬─────┴───────┴───────────────┼─────────────────────────────┤
    │ Library    │ Computer  │ Administration│ Cab │ Cab │ Cab │ Cab │ Cab │ Cab │ Cab │ Cab │ Cab │ Cab │ Cab │             │ (11 South
  E └────────────┴───────────┴───────────────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────────────┘  Cabins)
```

### 2.1. Overwinter Crew Accommodation (24 Cabins)
* **Single / Double Cabins:** Exactly **24 modular living cabins** distributed along the outer perimeter walls to provide external daylight via the window ribbons:
  * **13 Cabins on North Wall (Axes 8–21, A–B):** Seaward view looking across Prydz Bay.
  * **11 Cabins on South Wall (Axes 8–20, D–E):** Inland view looking toward the continental ice sheet.
* **Cabin Dimensions:** Standard modular container division (~2.4m W × 3.6m L), fitted with bed, study desk, wardrobe, and heating radiator.

### 2.2. Communal Life & Dining Facilities (Axes 1–6)
* **Dining Hall (Axes 1–4, B–D):** Seating capacity for 36 personnel with tables overlooking the western tarn.
* **Commercial Galley & Kitchen (Axes 4–6, B–C):** Commercial induction ranges, dishwashers, and food prep counters.
* **Walk-In Cold Storage (Axes 4–6, C–D):** Deep freeze and dry food storage rooms insulated to preserve multi-year food reserves.
* **Fitness Gym (Axes 1–3, A–B):** Treadmills, rowers, and weight benches for polar overwinter physical conditioning.

### 2.3. Health & Welfare Facilities
* **Medical Infirmary (Axes 3–6, A–B):** Examination bed, surgical lighting, telemedicine terminal, pharmacy dispensary, and emergency patient isolation.
* **Finnish Sauna & Showers (Axes 11–12, B–C):** Traditional cedar-lined dry sauna essential for crew psychological wellbeing during polar night.
* **Entertainment Cinema (Axes 13–15, B–D):** Tiered seating auditorium with AV projection for all-hands briefings and movie screenings.

### 2.4. Ocean Lounge & Bar (Axes 17–21, B–D)
* **The Jewel of Bharati:** Positioned at the eastern tip inside the cantilevered prow.
* **Panoramic Glazing:** Surrounded by the 6-bay floor-to-ceiling glass prow overlooking the Southern Ocean.
* **Furnishings:** Lounge armchairs, coffee tables, and full beverage bar counter (`bar`).

---

## 3. Quantitative 3D Interior Bounding Boxes

| Sector / Room | Grid Range | Bounding Box (L × W × H) | Center Position `[x, y, z]` |
|:---|:---|:---|:---|
| **Panoramic Lounge & Bar** | Axes 17–21, B–D | `10.5m × 8.0m × 3.0m` | `[+18.5, 6.5, 0.0]` |
| **Dining Mess Hall** | Axes 1–4, B–D | `9.6m × 8.0m × 3.0m` | `[-18.0, 6.5, 0.0]` |
| **Medical Infirmary** | Axes 3–6, A–B | `7.2m × 4.8m × 2.8m` | `[-14.4, 6.5, -7.2]` |
| **Fitness Gym** | Axes 1–3, A–B | `7.2m × 4.8m × 2.8m` | `[-19.2, 6.5, -7.2]` |
| **Sauna & Hygiene Suite** | Axes 11–12, B–C | `4.8m × 4.8m × 2.8m` | `[+2.4, 6.5, -2.4]` |
| **Cinema Auditorium** | Axes 13–15, B–D | `7.2m × 8.0m × 3.0m` | `[+7.2, 6.5, 0.0]` |
| **Standard Crew Cabin** | 1 Bay (2.4m W) | `2.4m × 3.6m × 2.6m` | Instanced along corridors |

---

## 4. Digital Twin Hotspot Anchors

| Subsystem Anchor | Local Coordinate `[x, y, z]` | Description |
|:---|:---|:---|
| **`panoramic_ocean_lounge`** | `[19.0, 6.5, 0.0]` | Eastern prow crew lounge and social node. |
| **`medical_bay_infirmary`** | `[-14.4, 6.5, -7.2]` | Telemedicine readiness and medical stock inventory. |
| **`communal_dining_mess`** | `[-18.0, 6.5, 0.0]` | Galley energy load and food rationing tracker. |
| **`crew_quarters_north`** | `[5.0, 6.5, -8.0]` | Northern residential wing occupancy and heating. |
| **`crew_quarters_south`** | `[5.0, 6.5, 8.0]` | Southern residential wing occupancy and heating. |
| **`telecom_radio_office`** | `[-12.0, 6.5, 7.2]` | VHF/HF radio communication and satellite voice node. |
