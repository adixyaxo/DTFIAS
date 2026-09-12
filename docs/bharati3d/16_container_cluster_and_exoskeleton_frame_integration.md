# 3D Modeling Analysis: Container Cluster & Exoskeleton Frame Integration

> **Source Image:** `images/bharati/download (13).webp`  
> **Target Path:** `docs/bharati3d/16_container_cluster_and_exoskeleton_frame_integration.md`  
> **Classification:** Architectural CAD Axonometric / Structural Integration Render  
> **Subject Focus:** 134 Container Blocks, 11 Secondary Transverse Steel Bents, Roof Terrace Railing & Stilt Base Bearings

---

## 1. Viewpoint & Perspective Calibration

* **Projection Type:** Axonometric Isometric 3D Shaded Render (Parallel projection, ~30° oblique elevation).
* **Camera Angle:** Oblique view from North-East looking South-West toward the cantilever prow and northern elevation.
* **Aspect Ratio:** Cinematic 2:1 widescreen architectural render.
* **Lighting:** Studio directional sun with crisp ground drop shadows, emphasizing the spatial interstitial gap between the container blocks and the external structural steel frames.

---

## 2. Structural Integration & Assembly Breakdown

```
                         [ Level 2 Penthouse Roof Observation Deck ]
                         ┌─────────────────────────────────────────┐
                         │ Flat Terrace Deck with Steel Guardrail  │
    ┌────────────────────┴─────────────────────────────────────────┴────────────────────┐
    │          11 TRANSVERSE SECONDARY STEEL BENTS (Chamfered Spaceframe)               │
    ├───────────────────────────────────────────────────────────────────────────────────┤
    │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐     │
    │  │ 20' ISO│ │ 20' ISO│ │ 20' ISO│ │ 20' ISO│ │ 20' ISO│ │ 20' ISO│ │ 20' ISO│ ... │ (Container Modules)
    │  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘     │
    ├───────────────────────────────────────────────────────────────────────────────────┤
    │                  INTERSTITIAL THERMAL AND STRUCTURAL AIR GAP (0.8m)               │
    └──────────┬─────────────────────────────┬───────────────────────────┬──────────────┘
              / \                            │                          / \
             /   \                           │                         /   \
      [QUAD FRONT V-STILTS]          [VERTICAL STILTS WITH]     [REAR SUBSTRUCTURE]
      (Cantilever Prow Legs)         [DIAGONAL KNEE BRACES]     (Stair Anchor Bent)
```

### 2.1. The 11 Secondary Steel Bents
* **Structural Rhythm:**
  * Exactly **11 transverse portal frames (bents)** enclose the container assembly.
  * Spaced at **4.80m on center**, aligning with the structural corner posts of paired 20ft containers (`2.44m × 2 = 4.88m`).
* **Frame Cross-Section Profile:**
  * **Roof Rafter:** Slopes inward at ~15° from the fascia to form the hipped roof bevel.
  * **Side Girt:** Vertical strut creating the continuous window opening pocket.
  * **Bottom Haunch:** Slopes inward at ~30° to form the aerodynamic underbelly taper.
* **Girt Stringers:** 4 longitudinal cold-formed steel girts connect the 11 bents horizontally, providing the mounting substructure for the exterior insulated aluminum cassette panels.

### 2.2. Modular Container Block Topology
* **Container Cluster Arrangement:**
  * **Main Level 1:** Flat horizontal platform of 16 container rows arranged side-by-side, cantilevering outward beyond the ground floor footprint.
  * **Central Penthouse (Level 2):** Raised central block (4 containers long × 3 containers wide) directly supporting the rooftop terrace.
* **Terrace Decking:**
  * Positioned on the eastern half of the Level 2 penthouse roof.
  * Flat perimeter safety railing (~1.1m H) consisting of galvanized top rail, intermediate mid-rail, and kickplate.

### 2.3. Foundation Bearing Interfaces
* **Quad Prow V-Stilts:**
  * 4 heavy fabricated steel V-pillars supporting the transverse prow girder.
  * Base terminates in spherical steel pin-bearings mounted on wide concrete footing pads.
* **Intermediate Stilts:**
  * Vertical tubular steel columns augmented with diagonal tubular **knee braces** extending upward at 45° to stabilize the longitudinal floor beams against seismic and polar blizzard buffeting.
* **External Stair Attachment:**
  * The single-flight industrial steel access stairs are welded directly to the base of Transverse Bent #4.

---

## 3. Quantitative 3D Metrics & Proportions

| Component | Dimensions in Real World | Three.js World Units (1u = 1m) | Notes |
|:---|:---|:---|:---|
| **Transverse Bent Spacing** | 4.80m on center | Repeat along X: `x = i * 4.8` | 11 bents across 48m |
| **Bent Overall Height** | 10.0m (hull frame only) | `y: 10.0` | Excludes foundation stilts |
| **Bent Overall Width** | 20.0m at widest point | `z: 20.0` | Measured at window lintel |
| **Interstitial Stand-off Gap** | 0.75m – 0.90m | Gap between container & bent | Insulation & service void |
| **Terrace Guardrail Length** | 12.0m L × 7.5m W | `x: 12.0, z: 7.5` | Guardrail height: 1.1m |
| **Knee Brace Incline Angle** | 45° diagonal strut | `length: 2.8m` | Tubular steel strut |

---

## 4. Materials, PBR Shaders & Color Palette

```
Hex Color Reference:
Secondary Steel Exoskeleton: #A8B8C2  (Galvanized structural steel light gray)
Container Module Priming:   #D0D7D9  (Pale marine zinc primer)
Roof Terrace Deck:          #7F8C8D  (Non-slip industrial deck coating)
Safety Handrails:           #BDC3C7  (Bright galvanized tubular rail)
Pin-Bearing Baseplates:     #34495E  (Heavy structural forged steel)
Concrete Footing Pedestals: #7F8C8D  (Cast reinforced concrete)
```

* **Exoskeleton Steel Material:**
  * Material: `MeshStandardMaterial`
  * Base Color: `#A8B8C2`
  * Metalness: `0.85`
  * Roughness: `0.30` (crisp structural specular reflections).

---

## 5. Three.js Procedural Frame Generator Script

```javascript
// Procedural Bent Duplicator for Three.js
function buildExoskeletonBents(scene, bentProfileShape) {
  const bentGeometry = new THREE.ExtrudeGeometry(bentProfileShape, {
    depth: 0.35, // I-beam flange width
    bevelEnabled: false
  });
  
  const steelMaterial = new THREE.MeshStandardMaterial({
    color: 0xA8B8C2,
    metalness: 0.85,
    roughness: 0.30
  });

  const bentsGroup = new THREE.Group();
  const bentCount = 11;
  const bentSpacing = 4.8;
  const startX = -((bentCount - 1) * bentSpacing) / 2; // Centered at origin

  for (let i = 0; i < bentCount; i++) {
    const bentMesh = new THREE.Mesh(bentGeometry, steelMaterial);
    bentMesh.position.set(startX + (i * bentSpacing), 0, 0);
    bentsGroup.add(bentMesh);
  }

  scene.add(bentsGroup);
  return bentsGroup;
}
```

---

## 6. Digital Twin Hotspot & Subsystem Anchors

| Subsystem Anchor | World Coordinate `[x, y, z]` | Description |
|:---|:---|:---|
| **`portal_bent_01_prow`** | `[24.0, 5.0, 0.0]` | Front prow terminal structural load bent. |
| **`penthouse_terrace_deck`** | `[2.0, 11.5, 0.0]` | Rooftop observation and science logging terrace. |
| **`stair_anchor_bent_04`** | `[-9.6, 2.0, -10.0]` | North exterior stairs structural attachment joint. |
| **`rear_bent_11_workshop`** | `[-24.0, 5.0, 0.0]`| Western logistics workshop structural framing. |
