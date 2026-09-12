# 3D Modeling Analysis: Southwest Roof Facets & Penthouse Deck

> **Source Image:** `images/bharati/download (2).webp`  
> **Target Path:** `docs/bharati3d/03_southwest_roof_facets_and_penthouse.md`  
> **Classification:** Oblique Aerial Architectural Detail / Roof Geometry  
> **Subject Focus:** Aerodynamic Roof Faceting, Penthouse Observation Terrace, Glazing Strips & Stilt Anchors

---

## 1. Viewpoint & Perspective Calibration

* **Projection Type:** Natural Perspective (Medium telephoto aerial photograph, ~70mm equivalent).
* **Camera Angle:** High oblique elevation (~40°–45° down-angle), looking from Southwest toward Northeast.
* **Aspect Ratio:** Standard 4:3 photograph.
* **Lighting & Reflections:** Intense low-zenith polar daylight producing metallic specular glints across the roof panel seams and highlighting the geometric breaklines between planar facets.

---

## 2. Architectural & Geometric Breakdown

```
                         [ Central Observation Terrace / Penthouse ]
                         ┌─────────────────────────────────────────┐
                         │   Guardrail Perimeter & Science Deck    │
      ▲ Sloped Facet     │   (Exhaust Flues on Southern Edge)      │     ▲ Sloped Facet
    ┌─┴──────────────────┴─────────────────────────────────────────┴─────┴─┐
    │                                                                       │
    │                      HIPPED AERODYNAMIC ROOF SKIN                     │
    │                   (Multi-Planar Insulated Panels)                     │
    ├───────────────────────────────────────────────────────────────────────┤
    │  [ ] [ ] [ ] [ ] [ ] [ ]  Continuous Strip Ribbon Windows [ ] [ ] [ ] │ (South Facade)
    ├───────────────────────────────────────────────────────────────────────┤
    │                      Tapered Inward Underbelly Bevel                  │
    └───────┬─────────────────────────────┬─────────────────────────┬───────┘
            │                             │                         │
      Vertical Stilt                 Vertical Stilt           Angled V-Stilt
      Foundation                     Foundation               Under Cantilever
```

### 2.1. Multi-Planar Roof Envelope
* **Aerodynamic Chamfering:** The roof is not a simple flat extrusion. It is designed as an inverted shallow tray with multi-faceted beveled edges:
  * **Perimeter Bevel:** Slopes inward at approximately 20° from the vertical fascia to shed heavy snow buildup and prevent wind vortex formation.
  * **Longitudinal Slope:** Shallow pitch of 3°–5° directing snowmelt toward internal heated drainage gullies.
* **Panelization Pattern:**
  * The main roof surface is divided into modular structural bays (visible as sharp panel seam lines spaced ~3.0m apart).
  * 16 primary transverse panel strips span across the longitudinal axis.

### 2.2. Level 2 Penthouse & Terrace
* **Footprint:** Centrally located on the roof, measuring approximately 15.0m L × 7.5m W × 2.8m H.
* **Observation Platform:** Flat wooden or metal-grate walking deck on the eastern half of the penthouse roof, surrounded by a 1.1m high galvanized steel perimeter safety railing.
* **Exhaust & Ventilation Flues:**
  * Cluster of 4 stainless steel vertical exhaust flues situated on the southern wall of the penthouse (generator CHP and heating furnace exhaust).
  * Height: ~1.2m above penthouse roofline.

### 2.3. Window Bands (Glazing Rhythm)
* **South (Inland) Facade:**
  * A continuous horizontal ribbon window band recessed ~0.15m within the insulated panel envelope.
  * Composed of 20+ uniform rectangular double-glazed window modules (~1.2m H × 1.8m W).
* **East (Seaward) Facade:**
  * Dramatic multi-bay floor-to-ceiling panoramic glass observation lounge overlooking the ocean.
  * Glazing is angled inward from top to bottom (negative rake angle ~15°) to minimize internal glare and prevent snow accumulation against the glass.

### 2.4. Substructure & Stilt Geometry
* **Column Configuration:**
  * **Core Columns:** Vertical cylindrical steel stilts supporting the main container floor grid.
  * **Cantilever V-Stilts:** Paired diagonal steel struts forming an inverted "V" truss supporting the overhanging eastern panoramic lounge.
* **Anchor Footings:** Each column terminates in an exposed reinforced concrete pier cap pinned with heavy rock bolts into the granite bedrock.

---

## 3. Quantitative 3D Metrics & Proportions

| Component | Dimensions in Meters | Three.js Scale (1u = 1m) | Notes |
|:---|:---|:---|:---|
| **Roof Overall Bounding Box** | 50.0m L × 20.0m W | `x: 50.0, z: 20.0` | Outer boundary at fascia edge |
| **Penthouse Module** | 15.0m L × 7.5m W × 2.8m H | `x: 15.0, y: 2.8, z: 7.5` | Offset `[0.0, 8.5, -1.0]` |
| **Rooftop Guardrail Height** | 1.1m | `y: 1.1` | Pipe diameter: 0.05m |
| **South Window Strip Height** | 1.2m | `y: 1.2` | Vertical offset: 4.8m from bedrock |
| **V-Stilt Spread Angle** | 45° included angle | Rotation: `±22.5°` | 2x structural tubular struts |
| **Pipe Rack Width & Standoff** | 1.2m tray, 0.8m above ground | Extruded path along terrain | Double insulated thermal conduit |

---

## 4. Materials, PBR Shaders & Color Palette

```
Hex Color Reference:
Roof Panel Cladding:        #4F6D7A  (Reflective steel-blue under polar sky)
Facade Fascia Panels:       #9BA8A8  (Light aluminum silver matte)
Window Glazing Tint:        #1A312C  (DTFIAS deep brand green tint in reflection)
Terrace Handrail Steel:     #D1D8DB  (Galvanized zinc steel)
Exhaust Flues:              #E8ECEF  (High-specular polished stainless steel)
```

* **Roof Skin Shader (PBR):**
  * Base Color: `#4F6D7A` to `#718894` (subtle metallic blue-gray).
  * Roughness: `0.35` (semi-gloss to reflect ambient sky).
  * Metalness: `0.85` (predominantly metallic response).
* **Window Glazing Shader:**
  * Base Color: `#0A1C17`.
  * Transmission: `0.85`.
  * Roughness: `0.05` (mirror-smooth specular reflections).
  * IOR (Index of Refraction): `1.52` (standard architectural glass).

---

## 5. Three.js Modeling Implementation Guide

### 5.1. Mesh Construction Technique
1. **Main Roof Mesh (`RoofComplexGeometry`):**
   * Do NOT use a flat plane. Construct using an extruded polygon with beveled upper vertices or a custom subdivided `BufferGeometry`.
   * Cut out the central rectangular aperture where the penthouse seats.
2. **Penthouse & Observation Deck (`PenthouseMesh`):**
   * Chamfered box geometry with recessed doors on the east terrace face.
   * Railing: Low-poly instance of thin cylinders or an alpha-masked ribbon texture to save draw calls.
3. **V-Stilt Assembly (`CantileverTrussGroup`):**
   * Two `CylinderGeometry` primitives (radius = 0.2m, length = 4.2m) angled at 22.5° off-vertical and merged into a single geometry.

### 5.2. Recommended Polygon Target
* Roof Shell: 600 triangles.
* Penthouse & Railings: 800 triangles.
* Window Insets & Frames: 1,200 triangles.
* Substructure Stilts & Piers: 1,400 triangles.

---

## 6. Digital Twin Hotspot & Subsystem Anchors

| Subsystem Hotspot | Local Coordinate `[x, y, z]` | Description |
|:---|:---|:---|
| **`panoramic_lounge`** | `[22.0, 5.0, 0.0]` | Eastern multi-bay observation lounge with ocean view. |
| **`science_terrace`** | `[2.5, 9.2, 0.0]` | Rooftop observation deck for meteorological logging. |
| **`generator_exhausts`** | `[-2.0, 9.8, 3.8]` | Thermal and exhaust sensor monitoring point. |
| **`v_stilt_cantilever`** | `[18.0, 1.5, 0.0]` | High-stress structural load cell monitoring node. |
| **`south_pipe_rack`** | `[0.0, 0.8, 12.0]` | Trace-heated pipeline thermal sensor node. |
