# 3D Modeling Analysis: Aerial Masterplan & Coastline Context

> **Source Image:** `images/bharati/download (1).webp`  
> **Target Path:** `docs/bharati3d/02_aerial_masterplan_and_coastline.md`  
> **Classification:** High-Altitude Aerial Masterplan / Environmental Context  
> **Subject Focus:** Geographic Orientation, Terrain Topography, Coastal Proximity & Auxiliary Compounds

---

## 1. Viewpoint & Perspective Calibration

* **Projection Type:** Natural Perspective Aerial (Wide-angle aerial photograph, ~28mm equivalent focal length).
* **Camera Position:** High-altitude oblique aerial (~150m–200m altitude above ground), looking North-Northeast toward Prydz Bay and the Southern Ocean.
* **Aspect Ratio:** Standard 3:2 landscape photograph.
* **Sun & Lighting Angle:** Mid-day summer polar sun (~35° solar elevation), originating from the upper-left (Northwest), casting soft directional shadows toward the Southeast.

---

## 2. Masterplan & Spatial Topography

```
                     [ PRYDZ BAY / SOUTHERN OCEAN ]
                     (Expedition Ship Anchored ~1.5 km Offshore)
                                    ▲
                                    │ North
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~┼~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Coastline
                   [ Coastal Road & Pump Station ]
                                    │
       [ Fuel Tank Farm &           │          [ Heliport & Remote
         Container Storage ]        │            Science Huts ]
                 ▲                  │                  ▲
                 │ (Pipe Rack)      │                  │
                 └──────────┐       │       ┌──────────┘
                            ▼       ▼       ▼
                     ┌─────────────────────────────┐
                     │   BHARATI MAIN COMPLEX      │
                     │  (Elevated on Stilt Ridge)  │
                     └─────────────────────────────┘
                                    │
    [ Meltwater Tarn / Pond ]       │       [ Bedrock Promontory / Flag ]
```

### 2.1. Orientation & Siting
* **Building Longitude Axis:** Aligned roughly East-Southeast to West-Northwest (azimuth ~110°–290°).
* **Seaward Facade (North):** Faces Prydz Bay directly to maximize natural daylight and grant unobstructed panoramic observation of maritime ice conditions.
* **Ridge Placement:** The complex is strategically positioned on the crest of a granitic bedrock ridge. This elevation prevents meltwater pooling during peak summer and ensures blizzard winds blow cleanly beneath and around the structure.

### 2.2. Surrounding Topographic Elements
1. **Granite Bedrock (Larsemann Hills Gneiss):**
   * Rolling, undulating topography with rounded ridges, gullies, and scree slopes.
   * Coloration: Warm ochre, rusty brown, weathered bronze, and exposed gray bedrock.
2. **Glacial Meltwater Tarns:**
   * Prominent frozen freshwater tarn immediately adjacent to the station's western flank (visible as bluish-white ice with dark melted fringes).
3. **Trace-Heated Service Conduits:**
   * Elevated pipeline trays mounted on lightweight triangular aluminum lattice stands snaking outward across the terrain toward the water intake and fuel storage areas.
4. **Logistics & Staging Compounds:**
   * Staging yard positioned ~80m northwest of the main station, containing modular ISO containers (blue, red, white) and tracked construction equipment.
5. **Maritime Context:**
   * Deep navy/ultramarine coastal waters (~300m–500m downslope) with distant tabular icebergs on the polar horizon.

---

## 3. Quantitative 3D Metrics & Site Scale

| Metric | Real-World Dimension (Estimated) | 3D World Units (1u = 1m) |
|:---|:---|:---|
| **Distance to Coastline** | ~350m – 450m | 400m North |
| **Bedrock Ridge Elevation** | ~35m above sea level (ASL) | +35m Y-elevation |
| **Western Meltwater Tarn Area** | ~60m × 40m elliptical footprint | 60m × 40m plane |
| **Service Pipeline Tray Width** | ~1.2m wide double-pipe tray | 1.2m wide extrusion |
| **Secondary Container Yard Offset** | ~80m northwest of main building | `[-75m, +5m, -40m]` |
| **Expedition Ship (Reference)** | ~120m ice-class cargo vessel | Background prop scale |

---

## 4. Materials & Environmental Lighting Palette

```
Hex Color Reference:
Larsemann Granite Bedrock:  #826B50  (Warm ochre / rusty desert-rock tone)
Glacial Tarn Ice:           #A3C1C6  (Cyan / pale mint frozen surface)
Southern Ocean Deep Water:  #152E4D  (Deep ultramarine polar sea)
Main Station Envelope:      #CED6D6  (Reflective matte aluminum)
Marine Shipping Containers: #1E4D79  (Oceanic blue ISO containers)
```

* **Environment HDRI Lighting:**
  * Clean, sub-zero Antarctic summer sky: Clear zenith blue (`#4C7EA9`) fading to pale icy cyan at the horizon (`#D3E5EB`).
  * High ambient contrast with sharp directional shadows.
* **Terrain Material Shader:**
  * Roughness: `0.85` (non-specular rock).
  * Normal map: High-frequency granite noise + low-frequency erosion gullies.

---

## 5. Three.js Site Environment Construction Strategy

### 5.1. Low-Poly Terrain Mesh (`EnvironmentTerrainMesh`)
* **Mesh Type:** Displaced `PlaneGeometry` (e.g., 200m × 200m grid with 64×64 subdivisions) or optimized low-poly decimation of real-world USGS/NCPOR DEM elevation data.
* **Elevation Profile:**
  * Station pad flattened at `Y = 0.0`.
  * North slope dropping toward sea level (`Y = -35.0` at `Z = -350.0`).
  * Western depression for the meltwater tarn (`Y = -3.5`).
* **Water Surfaces:** Single low-poly plane with subtle roughness (`0.1`) and high transmission for the frozen tarn.

### 5.2. Level of Detail (LOD) Recommendations
* **LOD 0 (Station Focus, < 80m camera distance):** High-detail station hull, visible stilts, full pipe racks.
* **LOD 1 (Site Overview, 80m–400m camera distance):** Low-poly station hull (single beveled box), simplified pipe lines, terrain mesh.
* **LOD 2 (Continental View, > 400m camera distance):** Low-poly terrain, station represented by bounding volume with glowing window emissive texture.

---

## 6. Digital Twin Hotspot & Subsystem Anchors

| Subsystem Anchor | World Coordinate `[x, y, z]` | Description |
|:---|:---|:---|
| **`station_main`** | `[0.0, 0.0, 0.0]` | Center of main station habitat on ridge crest. |
| **`seawater_intake_pipeline`**| `[-15.0, -1.5, -45.0]` | Trace-heated pipeline heading toward Quilty Bay. |
| **`fuel_storage_annex`** | `[-80.0, 4.0, -35.0]` | Secondary container and fuel drum staging yard. |
| **`quilty_bay_anchorage`** | `[250.0, -35.0, -450.0]`| Coastal marine logistics and resupply ship mooring. |
| **`meltwater_reservoir`** | `[-55.0, -4.0, 10.0]` | Freshwater glacier meltwater tarn monitoring point. |
