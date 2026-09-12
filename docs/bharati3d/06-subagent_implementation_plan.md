# Bharati Station 3D Digital Twin: Subagent Implementation Plan

Based on the architectural data and synthesis, the creation of the pure Three.js 3D model for the Bharati Research Station Digital Twin (DTFIAS) is divided among specialized subagents. This plan outlines the specific roles and detailed tasks for each subagent to efficiently develop the interactive 3D model.

## Subagent-1
**Role Name:** Core Structure Modeler
**Description:** 
Subagent-1 is responsible for generating the main structural body and foundation of the Bharati Station, ensuring high performance by abstracting the internal 134 modular containers.
*   **Aerodynamic Shell:** Implement the outer aerodynamic aluminum skin using `THREE.ExtrudeGeometry` based on a 30m x 50m 2D `THREE.Shape`. Crucially, utilize `bevelEnabled: true` to replicate the wind-tunnel-tested curved shell.
*   **Elevated Foundation:** Model the heavy-duty stilt system that elevates the structure above the permafrost. Create a grid array of `THREE.CylinderGeometry` to represent the columns. Connect these stilts using `THREE.LineSegments` in X-patterns to represent the vital structural cross-bracing.
*   **Panoramic Window:** Construct the distinct high-performance glass facade on the North end of the second floor. Intersect a `THREE.BoxGeometry` on the North face and apply a highly emissive, transparent `MeshPhysicalMaterial` (e.g., a glowing `--brand-mint`) to serve as a prominent visual focal point.

## Subagent-2
**Role Name:** External Assets & Infrastructure Modeler
**Description:** 
Subagent-2 is responsible for modeling the vital external infrastructure components that surround and sit atop the main station. These components represent key functional areas of the facility.
*   **Fuel Storage Farm:** Model the 300,000L fuel capacity as an interconnected array of 10-13 `THREE.CylinderGeometry` meshes placed near the main building to simulate the Jet A-1 storage tanks.
*   **HVAC Systems:** Construct geometric box arrays on the third-level roof terrace to represent the station's ventilation, heating, and exhaust systems.
*   **Communication Masts:** Model the C-band and Ku-band satellite radomes using `THREE.SphereGeometry` mounts strategically placed on the roof terrace.
*   **Bharati Heliport:** Create a large, flat `THREE.CylinderGeometry` (radius ~15m) located approximately 50m away from the main building on solid ground. Add 'H' markings on the surface using `THREE.BoxGeometry` strips.

## Subagent-3
**Role Name:** Environment & Effects Developer
**Description:** 
Subagent-3 is tasked with placing the station into an accurate representation of the harsh Larsemann Hills environment in Antarctica, optimizing visual impact without heavy rendering overhead.
*   **Terrain Generation:** Use a large `THREE.PlaneGeometry` displaced with random noise to simulate the rocky, uneven, ice-free coastal hills and permafrost, rather than a perfectly flat ice sheet.
*   **Atmospheric Particle System:** Implement an aggressive Antarctic blizzard simulation using a horizontal `THREE.Points` particle system. Ensure the visual flow of these particles demonstrates the wind passing smoothly *over* the aerodynamic shell and blowing *underneath* the elevated stilts to prevent snow accumulation.

## Subagent-4
**Role Name:** Assembly & Telemetry Integrator
**Description:** 
Subagent-4 serves as the coordinator who will integrate all models into a single cohesive Three.js scene, ensuring absolute compatibility with the DTFIAS frontend telemetry requirements.
*   **Scene Composition:** Position all sub-components relative to each other (e.g., ensuring the heliport is accurately 50m away and fuel storage pipes route logically towards the ground floor).
*   **Interactive Hotspot Tagging:** Group the raw geometries into separated, clickable groups with precise identifiers required by the telemetry system:
    *   Tag the main shell and living quarters group as `hotspot-main_building`.
    *   Tag the fuel farm group as `hotspot-fuel_storage`.
    *   Tag the roof ventilation array as `hotspot-hvac`.
    *   Tag the roof satellite radomes as `hotspot-comms_satcom`.
    *   Tag the heliport group as `hotspot-heliport`.
*   **Event Handling Readiness:** Expose these grouped objects in the Three.js scene graph so the frontend application can seamlessly attach raycasters and `onClick`/`onHover` UI overlays to them.
