# Bharati Station: 3D Modeling Implementation Translation

Based on the architectural research (bof architekten, 134 containers, elevated stilts, aerodynamic shell), here is how to translate these physical facts into actionable Three.js programmatic geometry or GLTF/GLB workflows.

## 1. The Main Shell
*   **Avoid Over-Modeling:** Do not model all 134 individual shipping containers. The containers form the *inner skeleton*. 
*   **Procedural Extrusion:** For Three.js, model the *outer aerodynamic aluminum shell*. Use a `THREE.ExtrudeGeometry` based on a 2D `THREE.Shape` (30m width x 50m depth). Add `bevelEnabled: true` to smooth the edges, replicating the wind-tunnel-tested curved shell.

## 2. Elevated Stilts
*   **Geometry:** Use `THREE.CylinderGeometry` for the steel columns. 
*   **Grid Placement:** Array the stilts in a grid under the main shell.
*   **Cross-Bracing:** Crucial for realism. Connect the stilts using `THREE.LineSegments` in X-patterns to represent the structural cross-bracing that stabilizes the station against 200 mph winds.

## 3. The Panoramic Window (Second Floor)
*   **Geometry:** Use a `THREE.BoxGeometry` intersecting the North face of the extruded shell.
*   **Material:** Apply a highly emissive, transparent `MeshPhysicalMaterial` (e.g., glowing `--brand-mint`) to signify the high-performance glazing and provide a visual focal point for the digital twin.

## 4. External Hotspots
To ensure 1:1 mapping with the DTFIAS frontend telemetry requirements, these architectural assets must be modeled as separate, clickable groups:
*   `hotspot-main_building`: The primary extruded shell.
*   `hotspot-fuel_storage`: Array of 10-13 `CylinderGeometry` meshes representing the 300,000L fuel farm.
*   `hotspot-comms_satcom`: `SphereGeometry` (radomes) on the roof.
*   `hotspot-hvac`: Box arrays on the roof terrace.
*   `hotspot-heliport`: A large `CylinderGeometry` (radius ~15m) situated roughly 50m away from the main building, complete with a marked 'H' (`THREE.BoxGeometry` strips).

## 5. Environmental Scene
*   **Terrain:** Use a `THREE.PlaneGeometry` displaced with random noise to simulate the rocky permafrost of Larsemann Hills.
*   **Atmosphere:** Utilize a `THREE.Points` particle system flowing horizontally to simulate the aggressive Antarctic blizzards, enhancing the "digital twin" immersive experience without heavy rendering costs.

---
*Research synthesized for 3D digital twin architectural modeling accuracy.*
