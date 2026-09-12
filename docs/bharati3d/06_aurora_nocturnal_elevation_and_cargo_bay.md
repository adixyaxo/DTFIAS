# 3D Modeling Analysis: Aurora Nocturnal Elevation & Cargo Bay

> **Source Image:** `images/bharati/download (3).webp`  
> **Target Path:** `docs/bharati3d/06_aurora_nocturnal_elevation_and_cargo_bay.md`  
> **Classification:** Night Operations / Atmospheric Environmental Lighting / Elevation Profile  
> **Subject Focus:** Aurora Australis Lighting, Southern Facade Ribbon Windows & Rear Cargo Roll-Up Entrance

---

## 1. Viewpoint & Perspective Calibration

* **Projection Type:** Low-Angle Ground Perspective (~24mm ultra-wide focal length).
* **Camera Position:** Stationed ~50m South-Southwest of the complex on the bedrock slope, looking up at a ~20° angle toward the southern longitudinal facade and western rear wall.
* **Aspect Ratio:** 16:9 cinematic widescreen photograph.
* **Atmospheric Lighting:** Deep polar night with spectacular Aurora Australis (Southern Lights) active overhead. Dominant ambient light is high-intensity emerald green (`#36D07A` / `#58E08C`), contrasting against the warm interior tungsten glow from the window ribbon.

---

## 2. Architectural & Environmental Breakdown

```
                             [ AURORA AUSTRALIS IONOSPHERIC CURTAIN ]
                             (Vibrant Emerald Green Ionized Nitrogen Glow)
                                                  ▼
                         ┌──────────────────────────────────────────────────┐
                         │              AERODYNAMIC ROOF PROFILE            │
                         ├──────────────────────────────────────────────────┤
   [ Rear Cargo Bay ]    │ [■] [■] [■] [■] [■] [■] [■] [■] [■] [■] [■] [■]  │ (Southern Window Ribbon)
  ┌──────────────────┐   ├──────────────────────────────────────────────────┤
  │ [||||] Roll-up   │   │             Tapered Chamfer Panel                │
  │ Shutter Doors    │   │             [🇮🇳 Indian Flag Insignia]            │
  └────────┬─────────┘   └────────────────────────┬─────────────────────────┘
           │                                      │
  [ Amber Floodlights ]                  [ Under-Stilt Inspection Glow ]
```

### 2.1. Structural Elevation Profile
* **Longitudinal Proportions:** Provides a pure silhouette of the station's full 50m southern length.
* **Rear Utility Terminal (Western End):**
  * Level 0 ground entry features a heavy-duty industrial roll-up shutter door (~3.6m W × 3.2m H) with vertical corrugated slats for vehicular equipment access.
  * Level 1 above the door features a 6-bay vertical window strip illuminating the rear interior corridor.
* **Penthouse Roofline:** Clear silhouette of the central stepped Level 2 mechanical spine rising ~2.8m above the main roof deck.

### 2.2. Fenestration & Lighting Contrast
* **Southern Window Band:** Continuous horizontal glass ribbon extending ~36 meters across the residential and laboratory sectors.
* **Dual Lighting Temperature:**
  * Western sectors: Cool white / high-CRI laboratory illumination (~5000K, hex `#E6F2FF`).
  * Eastern living sectors: Warm domestic tungsten illumination (~2700K, hex `#FFA834`).
* **Under-Stilt Lighting Array:**
  * Continuous low-profile amber LED safety floodlights mounted along the perimeter underbelly girder, casting downward illumination on the bedrock and foundation footings.

### 2.3. Environmental Context & Skybox Integration
* **Auroral Curtains:** Massive sinusoidal bands of emerald green light spanning across the upper hemisphere. In Three.js, this provides the exact color palette for night-time environment maps and custom GLSL auroral shaders.

---

## 3. Quantitative 3D Metrics & Proportions

| Feature | Estimated Measurement | Three.js World Units (1u = 1m) |
|:---|:---|:---|
| **Southern Window Ribbon Length** | ~36.0m continuous span | `length: 36.0, height: 1.2` |
| **Cargo Bay Shutter Door** | 3.6m W × 3.2m H | `width: 3.6, height: 3.2` |
| **Clearance Under Rear Hull** | ~2.2m at western rear | `y: 2.2` (slopes up to 3.5m) |
| **Roof Penthouse Setback** | 12.0m from western edge | `x: -12.0` offset from center |
| **Aurora Canopy Elevation** | Simulated ionosphere plane | `y: 120m` in sky dome |

---

## 4. Materials & Night Shader Specifications

```
Hex Color Reference:
Aurora Australis Peak:      #36D07A  (Vibrant ionized emerald green)
Aurora Ambient Wash:        #1A4D35  (Subtle atmospheric green haze)
Lab Window Emission:        #E6F2FF  (5000K daylight white fluorescent)
Hab Window Emission:        #FFA834  (2700K warm residential amber)
Under-Stilt Worklight:      #FF851B  (Amber sodium safety light)
Shadow Facade Cladding:     #121A18  (Deep dark-green ambient facade tone)
```

* **Aurora Australis Environment Shader:**
  * Custom Three.js vertex/fragment shader on a hemispherical inverted dome.
  * Modulates noise texture over time (`uTime * 0.05`) along UV coordinates with an additive emissive blend.
* **Window Glazing (Night Mode):**
  * Emissive Map: Alternating white and amber sections corresponding to laboratory and cabin floorplans.

---

## 5. Three.js Implementation Guidance

### 5.1. Auroral Night Lighting Setup
```javascript
// Ambient light reflecting the Southern Lights
const auroraAmbient = new THREE.AmbientLight(0x2A6A4E, 0.45);
scene.add(auroraAmbient);

// Directional green auroral tint from zenith
const auroraDirectional = new THREE.DirectionalLight(0x4EBA87, 0.65);
auroraDirectional.position.set(0, 50, -20);
scene.add(auroraDirectional);
```

### 5.2. Digital Twin Hotspot Anchors
* **`cargo_bay_doors`** `[-22.0, 1.6, 0.0]`: Heavy cargo, machinery, and container intake node.
* **`south_habitat_ribbon`** `[0.0, 5.2, 10.0]`: Crew quarters occupancy and thermal telemetry.
* **`aurora_space_weather_node`** `[0.0, 14.0, 0.0]`: Geomagnetic / ionospheric auroral monitoring sensor node.
