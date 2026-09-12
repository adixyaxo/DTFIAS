# 3D Modeling Analysis: Front Oblique Facade & Cantilever V-Stilts

> **Source Image:** `images/bharati/download.webp`  
> **Target Path:** `docs/bharati3d/04_front_oblique_facade_and_v_stilts.md`  
> **Classification:** Eye-Level Architectural Elevation & Cantilever Detail  
> **Subject Focus:** Aerodynamic Prow, Panoramic Raked Glazing, V-Stilts, Indian Mission Insignia & Distant Radome

---

## 1. Viewpoint & Perspective Calibration

* **Projection Type:** Ground-Level Eye-Level Perspective (~35mm standard lens, wide field-of-view ~63°).
* **Camera Position:** Ground-level camera (~1.8m above terrain), stationed ~40m East-Southeast of the station, looking up at a ~15° low-angle rake toward the cantilevered prow.
* **Aspect Ratio:** Standard 3:2 landscape photograph.
* **Lighting:** Low-angle, direct, crystal-clear polar sunlight highlighting the metallic bevels and generating sharp underbelly shadow planes.

---

## 2. Architectural & Geometric Breakdown

```
        ┌─────────────────────────────────────────────────────────────┐
        │                 UPPER ROOF FASCIA & OVERHANG                 │
        ├──────────────────────────┬──────────────────────────────────┤
        │                          │  [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]  │ (Longitudinal Window Strip)
        │  6-BAY PANORAMIC GLAZING │                                  │
        │  (Inward Rake Angle 15°) ├──────────────────────────────────┤
        │                          │  Tapered Bevel Panels            │
        │                          │  [🇮🇳 Indian Flag Insignia]       │
        ├──────────────────────────┴──────────────────────────────────┤
        │               AERODYNAMIC UNDERBELLY WEDGE                   │
        └──────────────┬───────────────────────────────┬──────────────┘
                      / \                             / \
                     /   \                           /   \
                    /     \                         /     \
             Front V-Stilt Legs               Rear V-Stilt Legs
             (Heavy Hollow Steel)             (Under Floor Beam)
                    │     │                         │     │
                 [Concrete Pad]                  [Concrete Pad]
```

### 2.1. The Cantilevered Prow & Panoramic Lounge
* **Geometric Form:** The eastern termination of the station forms a massive aerodynamic wedge reminiscent of an ocean vessel or aircraft fuselage.
* **Panoramic Glazing Array:**
  * Composed of **6 massive vertical glass bays** spanning the full height of the living deck (~3.0m H).
  * **Negative Rake Angle:** The glazing slopes inward from top to bottom at approximately **15° off-vertical**. This architectural choice prevents falling snow from adhering to the glass and reflects interior lighting downward.
  * Flanking Panels: The glazing is flanked on both corners by solid beveled aluminum cladding sections that seamlessly wrap into the longitudinal side walls.

### 2.2. V-Stilt Structural Support Architecture
* **Primary Cantilever Support:** Because the Level 1 floorplate extends ~10 meters beyond the ground-level core, it is supported by paired tubular steel stilts configured as inverted "V" bents:
  * **Front Pair:** Two heavy structural steel tubular legs (diameter ~0.45m) meeting at a common apex node under the primary floor transverse girder.
  * **Rear Pair:** Second V-bent positioned ~6 meters further back along the hull.
* **Anchor Base:** Anchored into substantial cast-in-place concrete footing blocks bolted directly into the hard granitic bedrock.
* **Underbelly Geometry:** The underside of the cantilever is clad in smooth, aerodynamic steel panels sloping upward toward the nose to channel high-speed blizzard winds under the building without turbulent drag.

### 2.3. Longitudinal Facade & Mission Identity
* **Upper Level Window Ribbon:** A horizontal band of recessed rectangular punch-out windows with matte dark frames running along the north-facing seaward wall.
* **Lower Inward-Sloping Facade:** Below the window strip, the wall slopes inward at ~25° toward the undercarriage.
* **National Emblem:** The official Indian Tricolor flag (saffron, white with navy Ashoka Chakra, green) is prominently painted on the chamfered lower corner panel near the front prow.

### 2.4. Auxiliary Infrastructure Visible in Frame
* **Ground Utility Core & Vehicle Bay:** Visible beneath the cantilever; houses mechanical infrastructure. A tracked polar utility vehicle (PistenBully with blue/red cab) is parked in the sheltered under-stilt apron.
* **Distant SATCOM Radome:** Visible to the far left on an elevated ridge—a massive white spherical geodesic dome mounted atop a steel truss lattice tower.
* **Foreground Pipe & Cable Rack:** Elevated aluminum truss tray supported on A-frame legs, carrying insulated red and silver heating/water pipelines.
* **Shipping Containers:** Stacked red intermodal containers with white lettering (`CHINARE`) on the left terrain.

---

## 3. Quantitative 3D Metrics & Proportions

| Feature | Estimated Measurement | 3D Space Coordinates / Size | Notes |
|:---|:---|:---|:---|
| **Prow Cantilever Length** | ~9.5m – 10.5m | Extends along +X axis | Past Level 0 utility footprint |
| **Panoramic Window Width** | ~12.0m total width | 6 bays × 2.0m width each | Full frontal facade span |
| **Window Height** | ~3.0m vertical height | `y: 3.0` | Inward rake: ~15° |
| **V-Stilt Tubular Diameter** | ~0.45m outer diameter | `radius: 0.225m` | Hollow structural steel tube |
| **V-Stilt Ground Stance Width** | ~7.0m between footing pads | `z: ±3.5m` | Transverse footing spread |
| **Under-Prow Ground Clearance** | ~3.5m at rear, ~4.8m at prow tip | `y: 3.5m -> 4.8m` | Upward angled underbelly |
| **SATCOM Radome Diameter** | ~10.0m spherical diameter | `radius: 5.0m` | Offset ~120m West-Southwest |

---

## 4. Materials, PBR Shaders & Color Palette

```
Hex Color Reference:
Exterior Aluminum Skin:     #C4CCCC  (Bright brushed aluminum under direct sun)
Underside Shadow Tone:      #2A3835  (Deep ambient shadow underbelly)
Panoramic Glazing (Direct): #1A2E28  (Deep bottle-green specular glass)
V-Stilt Steel Paint:        #E2E8E8  (Off-white / pale industrial gray epoxy)
Concrete Footing Pads:      #8F8D88  (Rough cast gray concrete)
Indian Flag Emblem:         #FF9933 (Saffron), #FFFFFF (White), #138808 (Green)
PistenBully Snowcat:        #005B94 (Deep cyan-blue body), #D62828 (Red cab accent)
```

* **Aerodynamic Hull Shader:**
  * Base Color: `#C4CCCC`
  * Metalness: `0.75`
  * Roughness: `0.30`
  * Clearcoat: `0.20` (subtle clearcoat sheen replicating fluoropolymer anti-weather coating).
* **V-Stilt Tubular Shader:**
  * Base Color: `#E2E8E8`
  * Metalness: `0.85`
  * Roughness: `0.35`

---

## 5. Three.js Procedural / Mesh Implementation Guide

### 5.1. Constructing the Cantilever Prow
```javascript
// Procedural outline cross-section for ExtrudeGeometry
const hullShape = new THREE.Shape();
hullShape.moveTo(0, 0);              // Rear underbelly anchor
hullShape.lineTo(10.0, 1.2);         // Upward sloped underbelly prow
hullShape.lineTo(11.0, 4.2);         // Inward raked 15° window plane
hullShape.lineTo(10.5, 4.6);         // Top roof chamfer bevel
hullShape.lineTo(0, 4.6);            // Roof deck line
hullShape.lineTo(0, 0);              // Close rear seam
```
* Extrude this profile symmetrically along the Z-axis with chamfered bevels.
* Separate the front polygon into an independent material slot for the `PanoramicGlassMaterial`.

### 5.2. V-Stilt Geometry
* Use `THREE.CylinderGeometry(0.225, 0.225, 4.5, 16)`.
* Create two instances, rotate along the Z-axis by `+22.5°` and `-22.5°`, and merge into `VStiltPairMesh`.

---

## 6. Digital Twin Hotspot & Subsystem Anchors

| Subsystem Anchor | Coordinate `[x, y, z]` | Description |
|:---|:---|:---|
| **`observation_deck_window`**| `[23.0, 5.2, 0.0]` | Front panoramic window looking out to Prydz Bay. |
| **`v_stilt_front_node`** | `[18.5, 3.2, 0.0]` | Primary structural support load-bearing node. |
| **`underbelly_clearance`** | `[15.0, 2.0, 0.0]` | Snowdrift avoidance corridor and sensor node. |
| **`pistenbully_parking`** | `[8.0, 0.0, 4.5]` | Polar vehicle fleet and traverse staging node. |
| **`pipe_rack_junction`** | `[20.0, 0.5, 12.0]` | Main heated trace pipeline distribution node. |
