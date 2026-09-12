# Bharati Station: 3D Implementation Synthesis

This document synthesizes the architectural facts of the Bharati Research Station (Larsemann Hills, Antarctica) and provides strategic guidelines for translating its physical properties into a programmatic Digital Twin using Three.js.

## 1. Core Architecture & Bounding Volumes
Designed by bof architekten, Bharati is built to withstand extreme polar conditions. It is constructed from 134 modular shipping containers wrapped in an aerodynamic insulated skin.
*   **Three.js Strategy (Main Shell):** To maintain performance, avoid modeling individual containers. Focus entirely on the outer aerodynamic aluminum shell. Use `THREE.ExtrudeGeometry` based on a 30m x 50m 2D `THREE.Shape`, utilizing `bevelEnabled: true` to replicate the wind-tunnel-tested curved shell.
*   **Three.js Strategy (Elevated Foundation):** The entire structure sits elevated on heavy-duty stilts to insulate the permafrost and allow blizzards to pass underneath. Model this using a grid array of `THREE.CylinderGeometry`. Crucially, add X-pattern cross-bracing using `THREE.LineSegments` to achieve structural realism.

## 2. Spatial Layout & Key Features
The station spans ~2,500m² across three functional levels: Ground (Technical & Power), Second Floor (Residential & Living), and Third Level (Roof Terrace).
*   **Three.js Strategy (North Panoramic Window):** The second floor features a massive, high-performance glass facade. Replicate this visually striking feature by intersecting a `THREE.BoxGeometry` on the North face. Apply a highly emissive, transparent `MeshPhysicalMaterial` (e.g., a glowing `--brand-mint`) to serve as the visual focal point of the model.

## 3. Exterior Assets & Interactive Hotspots
To ensure a 1:1 mapping with the DTFIAS frontend telemetry requirements, the surrounding architectural elements must be modeled as separated, clickable groups with precise IDs:
*   **`hotspot-main_building`:** The primary aerodynamic shell and living quarters.
*   **`hotspot-fuel_storage`:** Represents the 300,000L fuel farm (Jet A-1). Model as an interconnected array of 10-13 `THREE.CylinderGeometry` meshes near the main building, piping into the ground-floor CHP plant.
*   **`hotspot-hvac`:** Box arrays on the roof terrace representing ventilation and exhaust systems.
*   **`hotspot-comms_satcom`:** C-band and Ku-band satellite radomes, modeled using `THREE.SphereGeometry` mounts on the roof.
*   **`hotspot-heliport`:** Situated ~50m away for Kamov helicopters, model using a large flat `THREE.CylinderGeometry` (radius ~15m) on solid ground, marked with 'H' markings made of `THREE.BoxGeometry` strips.

## 4. Environmental Scene Context
Bharati is located in the rocky, coastal permafrost of the Larsemann Hills, close to Quilty Bay.
*   **Three.js Strategy (Terrain & Weather):** Generate the surrounding terrain using a `THREE.PlaneGeometry` displaced with random noise to simulate rocky, uneven hills (rather than a flat ice sheet). To convey the extreme climate without heavy rendering overhead, implement a horizontal `THREE.Points` particle system to simulate relentless Antarctic blizzards flowing underneath the station's stilts.

---
*Synthesized from the Bharati Station Architectural Overview, Spatial Layout, Exterior Assets, and 3D Modeling guides.*
