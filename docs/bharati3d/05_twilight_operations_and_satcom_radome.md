# 3D Modeling Analysis: Twilight Operations & SATCOM Radome

> **Source Image:** `images/bharati/bharati-research-station-at-antarctica-v0-lytsjtyplizd1.webp`  
> **Target Path:** `docs/bharati3d/05_twilight_operations_and_satcom_radome.md`  
> **Classification:** Twilight / Polar Night Operations & Telecommunications Detail  
> **Subject Focus:** Spherical Geodesic SATCOM Radome, Nocturnal Emissive Lighting, Stepped Roofline & Polar Aesthetic

---

## 1. Viewpoint & Perspective Calibration

* **Projection Type:** Eye-Level Telephoto Perspective (~85mm–105mm portrait focal length).
* **Camera Position:** Elevated rocky ridge ~80m South-Southwest of the main station complex, looking Northeast across the radome toward Prydz Bay.
* **Aspect Ratio:** Standard 3:2 landscape photograph.
* **Atmospheric Lighting:** Deep polar nautical twilight (blue hour). Ambient illumination is predominantly deep navy and indigo (`#0C1929`), with strong artificial amber emissive glows (`#FFA21F`) radiating from the interior station windows and ground worklights.

---

## 2. Architectural & Telecommunications Breakdown

```
                             [ Distant Frozen Sea Ice & Iceberg Shelf ]
                                                  ▲
                                                  │
          [ Main Station Core ]                   │                 [ Secondary Habitat Wing ]
        ┌───────────────────────┐                 │                 ┌───────────────────────┐
        │   Penthouse Exhausts  │                 │                 │  Continuous Strip     │
        │ ┌───────────────────┐ │                 │                 │  [■] [■] [■] [■] [■]  │
        │ │ [■][■][■][■][■]   │ │                 │                 └──────────┬────────────┘
        └─┴───────────────────┴─┘                 │                            │
                    │                             │                      Vertical Stilts
                    │                             │                      + Amber Ground Glow
                    │           [ GEODESIC SATCOM RADOME ]
                    │           ┌────────────────────────┐
                    │          /   Spherical Geodesic    \
                    │         │      Dielectric Shell     │
                    │          \   (Hex / Pent Facets)   /
                    │           └───────────┬────────────┘
                    │                       │
                    │            [ Circular Ring Truss ]
                    │            [ Tubular Steel Stilts]
                    ▼                       ▼
    ──────────────────────────────────────────────────────────────────────── Bedrock Ridge
```

### 2.1. The Spherical SATCOM Geodesic Radome
* **Geometry:** True spherical form faceted into a high-frequency **geodesic icosahedron / truncated icosahedron** pattern (alternating hexagonal and pentagonal fiberglass sandwich panels).
* **Dimensional Scale:**
  * Spherical Diameter: Approximately **10.0m to 11.0m**.
  * Base Elevation: Mounted on an elevated structural steel ring truss ~2.0m above local bedrock.
* **Substructure:** The ring beam is supported by 8 to 12 vertical cylindrical steel stilts with diagonal tension cross-rods anchored to concrete bedrock piers.
* **Material Appearance:** Off-white dielectric fiberglass with a satin specular finish. The twilight sky casts a deep cyan-blue gradient across its shadow side, while the low polar sun creates a crisp specular highlight along its western perimeter.

### 2.2. Nighttime Station Lighting & Emissive Windows
* **Interior Glow Color:** High-temperature tungsten/warm sodium glow (**2700K – 3000K**, hex `#FFAE33` to `#FF8C00`), providing high contrast against the cold `#0B1E19` Antarctic background.
* **Window Rhythms Visible:**
  * Main Living/Laboratory Block: 8 evenly spaced glowing rectangular window bays (~1.2m × 1.8m).
  * Secondary Wing (Right): 6 distinct illuminated windows with sharp black mullion silhouettes.
* **Ground Floodlights (Underbelly Illumination):**
  * Downward-facing halogen/LED worklights mounted beneath the Level 1 cantilever, illuminating the foundation stilts and ground perimeter in warm amber light to facilitate 24/7 winter maintenance and snowdrift monitoring.

### 2.3. Stepped Silhouette & Roof Features
* **Penthouse Profile:** Clear view of the vertical step between the Level 1 main roof and the Level 2 penthouse deck.
* **Chimney Clusters:** 4 vertical stainless steel exhaust pipes protruding above the penthouse roofline, venting heating boilers and diesel generators.
* **Wing Hierarchy:** Confirms that Bharati consists of a primary multi-level central hull flanked by interconnected wings, rather than a single monolithic block.

### 2.4. Trace-Heated Infrastructure in Foreground
* A continuous raised conduit track with safety handrail/truss snaking across the foreground ridge between the SATCOM station and the main facility, carrying power and high-speed fiber-optic telemetry cables.

---

## 3. Quantitative 3D Metrics & Proportions

| Element | Real-World Dimension | Three.js Scale Units (1u = 1m) | Notes |
|:---|:---|:---|:---|
| **Radome Sphere Radius** | 5.2m (10.4m diameter) | `radius: 5.2` | Center at `[-25.0, 7.2, 35.0]` |
| **Radome Base Ring Elevation**| 2.0m above ground | `y: 2.0` | 10.0m diameter circular ring |
| **Window Module Cutout** | 1.8m W × 1.2m H | `width: 1.8, height: 1.2` | Spacing: ~2.4m on center |
| **Emissive Light Intensity** | ~3,500 lumens / window | `emissiveIntensity: 1.8` | High contrast night render |
| **Ground Floodlight Cone** | 60° spot angle | `SpotLight(0xFFA020, 3.0)` | Positioned under floor deck |

---

## 4. Materials & Night Shader Specifications

```
Hex Color Reference:
SATCOM Dome Albedo:         #E6EDED  (Clean off-white fiberglass)
SATCOM Shadow Tone:         #23384A  (Deep indigo blue atmospheric shadow)
Glowing Window Emissive:    #FFAE33  (Warm tungsten polar interior glow)
Window Mullion Silhouette:  #0F1514  (Solid black structural window frame)
Underbelly Floodlight:      #FF9100  (Amber sodium/halogen worklight)
Polar Night Sky & Water:    #0B1622  (Deep midnight blue background)
```

* **Radome Dielectric Shader:**
  * Material: `MeshStandardMaterial`
  * Base Color: `#E6EDED`
  * Roughness: `0.35`
  * Metalness: `0.05` (dielectric non-metal composite)
  * Normal Map: Subtle hexagonal geodesic panel grid.
* **Nocturnal Window Material:**
  * Material: `MeshStandardMaterial`
  * Base Color: `#FFAE33`
  * Emissive: `#FF9900`
  * Emissive Intensity: `2.0`
  * Tone Mapped: `false` (to trigger bloom in Three.js UnrealBloomPass).

---

## 5. Three.js Night Mode & Digital Twin Implementation

### 5.1. Geodesic Radome Mesh Setup
```javascript
// Optimized low-poly geodesic radome
const radomeGeo = new THREE.IcosahedronGeometry(5.2, 2); // 80 faces
const radomeMat = new THREE.MeshStandardMaterial({
  color: 0xE6EDED,
  roughness: 0.35,
  metalness: 0.05,
  flatShading: true // Exaggerates the authentic geodesic facets
});
const radomeMesh = new THREE.Mesh(radomeGeo, radomeMat);
radomeMesh.position.set(-25.0, 7.2, 35.0);
```

### 5.2. Post-Processing & Night Lighting Setup
* **Ambient Light:** Low-intensity cold blue ambient light (`0x1A2B3C`, intensity `0.35`).
* **Directional Moon/Twilight:** Pale cyan directional light (`0x6B8BA4`, intensity `0.45`) simulating low polar nautical twilight.
* **Point Lights on Windows:** Use `PointLight` or glowing `MeshBasicMaterial` instances with Three.js `UnrealBloomPass` to achieve the authentic warm polar oasis aesthetic established in `.agents/brand_design/SKILL.md`.

---

## 6. Digital Twin Hotspot & Subsystem Anchors

| Subsystem Anchor | World Coordinate `[x, y, z]` | Description |
|:---|:---|:---|
| **`satcom_c_band_radome`** | `[-25.0, 7.2, 35.0]` | Primary GSAT-7A / ISRO Earth station tracking dish. |
| **`satcom_cable_link`** | `[-15.0, 1.2, 20.0]` | High-speed fiber-optic and power trace conduit. |
| **`main_hab_night_core`** | `[0.0, 5.5, 0.0]` | Living quarters nocturnal thermal monitoring node. |
| **`chp_exhaust_plume`** | `[-2.0, 10.0, 3.8]` | Generator exhaust emissions thermal sensor. |
| **`underbelly_floodlights`**| `[8.0, 2.8, -4.0]` | Stilt security and structural inspection lighting. |
