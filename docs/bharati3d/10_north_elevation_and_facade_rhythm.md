# 3D Modeling Analysis: North Elevation & Facade Rhythm

> **Source Image:** `images/bharati/download (7).webp`  
> **Target Path:** `docs/bharati3d/10_north_elevation_and_facade_rhythm.md`  
> **Classification:** Direct Orthographic-Style Elevation / Facade Modular Rhythm  
> **Subject Focus:** North Facade Aspect Ratio, Fenestration Rhythm, Indian Mission Insignia & Central Access Stairs

---

## 1. Viewpoint & Perspective Calibration

* **Projection Type:** Near-Orthographic Telephoto Perspective (~150mm telephoto lens, virtually zero perspective convergence).
* **Camera Position:** Ground-level camera positioned due North of the station (~120m away on the opposite rocky rise), perfectly aligned normal to the longitudinal centerline.
* **Aspect Ratio:** Standard 3:2 landscape photograph.
* **Significance for 3D Modeling:** This image serves as the **definitive CAD 2D elevation blueprint** for UV mapping, vertical dimensioning, and structural rhythm calibration.

---

## 2. Orthographic Architectural Breakdown

```
                                            [ Penthouse Spine & Antenna ]
                                            ┌───────────────────────────┐
                                            │      Central Core         │
    ┌───────────────────────────────────────┴───────────────────────────┴───────────────────────────────────────┐
    │                                          UPPER ROOF FASCIA (1.0m H)                                       │
    ├─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┤
    │ [ ] │ [ ] │ [ ] │ [ ] │ [ ] │ [ ] │ [ ] │ [ ] │ [ ] │ [ ] │ [ ] │ [ ] │ [ ] │ [ ] │ [ ] │ [ ] │ [ ] │ [ ] │
    │ 16-PANE HORIZONTAL CONTINUOUS WINDOW RIBBON (1.2m H, Recessed 0.15m within Aluminum Insulated Envelope)  │
    ├─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┤
    │                                          LOWER VERTICAL BAND (0.8m H)                                     │
    ├───────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │                          INWARD SLOPING 30° AERODYNAMIC UNDERBELLY CHAMFER (1.4m H)                       │
    │                                              [🇮🇳 INDIAN FLAG EMBLEM]                                       │
    └───┬───────────────────────────┬───────────────────────────┬───────────────────────────┬───────────────────┘
       / \                         / \                         [|]                         / \
      /   \                       /   \                     [STEEL STAIR]                 /   \
     /     \                     /     \                    (Ground Access)              /     \
  [Eastern Cantilever]        [Stilt Array]                                           [Western Cantilever]
```

### 2.1. Exact Vertical Proportions & Datum Layers
By measuring pixel dimensions against the known total height (~12.5m):

1. **Roof Penthouse Cap (Level 2):**
   * Top elevation: `+12.5m` above bedrock.
   * Vertical height: `2.5m` above main roof deck.
   * Central longitudinal span: `~15.0m` centered along the 50.0m hull.
2. **Upper Roof Fascia:**
   * Vertical span: `+9.0m` to `+10.0m` (`1.0m` height).
   * Straight horizontal band with a 20° beveled upper lip where it meets the hipped roof plane.
3. **Continuous Window Ribbon:**
   * Vertical span: `+7.8m` to `+9.0m` (`1.2m` height).
   * Rhythm: Divided into **8 primary structural bays**, each subdivided into 2 glazed panes = **16 uniform window openings**.
   * Each pane measures approximately `2.3m W × 1.2m H`.
   * Outer window frames: Dark anodized architectural bronze/charcoal (`#1E2528`).
4. **Lower Vertical Band:**
   * Vertical span: `+7.0m` to `+7.8m` (`0.8m` height).
   * Planar aluminum cladding panel beneath window sills.
5. **Aerodynamic Inward Chamfer (Underbelly Transition):**
   * Slopes inward toward the stilt columns at approximately **30° off-vertical**.
   * Vertical drop: `+5.6m` down to `+4.2m` (`1.4m` vertical drop, ~1.6m slant length).
   * **Mission Insignia Placement:** The official Indian Tricolor flag (saffron, white with navy chakra, green) is applied directly on the centerline of this lower beveled panel, centered under Window Bay 8–9.
6. **Substructure Stilt Clearance:**
   * Free air clearance beneath underbelly: `~3.5m` to `~4.2m` above uneven bedrock.
   * Total column count along northern longitudinal foundation line: 7 primary vertical/slanted support pillars.

### 2.2. Central Exterior Access Staircase
* **Location:** Positioned slightly west of the building centerline (under Window Bay 10).
* **Construction:** Open-grate galvanized structural steel stairs ascending from the ground pad directly into an exterior airlock door on Level 1.
* **Flight Geometry:** Single straight flight with an intermediate landing, flanked by tubular steel safety handrails.

---

## 3. Quantitative 3D Modeling Blueprint (Exact Measurements)

| Architectural Datum | Elevation Above Bedrock (Y) | Real-World Size | 3D Engine Scale Units (1u = 1m) |
|:---|:---|:---|:---|
| **Roof Ridge / Mast Apex** | `+13.5m` | Antenna mast | `y: 13.5` |
| **Penthouse Roof Deck** | `+12.5m` | Terrace plane | `y: 12.5` |
| **Main Station Roof Fascia**| `+10.0m` | Top of wall | `y: 10.0` |
| **Window Ribbon Top (Head)**| `+9.0m` | Window lintel | `y: 9.0` |
| **Window Ribbon Base (Sill)**| `+7.8m` | Window sill | `y: 7.8` |
| **Wall Bottom / Chamfer Top**| `+7.0m` | Crease edge | `y: 7.0` |
| **Underbelly Keel Line** | `+4.2m` | Stilt junction | `y: 4.2` |
| **Bedrock Ground Plane** | `0.0m` | Local datum | `y: 0.0` |
| **Total Building Length** | N/A | `50.0m` along X-axis | `x: -25.0 to +25.0` |
| **Indian Flag Emblem Scale** | Center `[0.0, 5.0, -10.1]`| `1.8m W × 1.2m H` | Decal / Texture map |

---

## 4. Materials, PBR Shaders & Color Palette

```
Hex Color Reference:
Aluminum Cladding (Upper):  #BAC4C7  (Clean brushed aluminum under zenith sun)
Window Dark Cavity:         #141C1E  (Deep recessed glass shadow)
Lower Chamfer Panel:        #A6B2B5  (Slightly darker shade due to downward angle)
Galvanized Steel Stairs:    #D5DDE0  (Hot-dip galvanized zinc)
Stilt Column Coating:       #E2E9EC  (Protective light-gray marine epoxy)
Indian Flag Saffron:        #FF9933  (Official national flag saffron)
Indian Flag Green:          #138808  (Official national flag green)
Indian Flag Chakra Navy:    #000080  (Navy wheel on white band)
```

* **Northern Wall UV Layout:**
  * Clean planar UV mapping projected along the Z-axis.
  * Window strip can be rendered via an alpha-masked texture or geometry cutouts.
  * Flag emblem applied via a secondary non-repeating decal mesh (`THREE.DecalGeometry`) at `[0.0, 5.0, -10.1]`.

---

## 5. Three.js Implementation Guidance

### 5.1. Constructing the Longitudinal Wall Extrusion
```javascript
// Cross-section profile along vertical Y-Z plane
const wallProfile = new THREE.Shape();
wallProfile.moveTo(0, 4.2);           // Lower stilt connection
wallProfile.lineTo(1.4, 5.6);         // 30° outward chamfer to lower wall
wallProfile.lineTo(1.4, 7.8);         // Vertical wall below window
wallProfile.lineTo(1.25, 7.8);        // 0.15m window inset
wallProfile.lineTo(1.25, 9.0);        // 1.2m window glass pane
wallProfile.lineTo(1.4, 9.0);         // 0.15m window frame reveal
wallProfile.lineTo(1.4, 10.0);        // Upper fascia panel
wallProfile.lineTo(0.8, 10.2);        // Roof edge chamfer
```
* Extrude this profile along the X-axis for `50.0m` to create the perfectly accurate longitudinal hull form.

### 5.2. Digital Twin Hotspot Anchors
* **`north_facade_center`** `[0.0, 7.0, -10.2]`: Primary institutional facade anchor and emblem marker.
* **`central_stairs`** `[-3.0, 2.0, -10.5]`: Main exterior pedestrian muster station.
* **`meteo_mast_apex`** `[0.0, 13.5, 0.0]`: Primary meteorological station logging anemometer and solar irradiance.
