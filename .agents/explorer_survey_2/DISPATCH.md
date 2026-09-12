# Task Assignment: Explorer 2 — Architectural Research & Bharati Physical Specs

## Objective
Investigate documentation and architectural research in the repository regarding Bharati station:
1. Check `docs/` (`docs/architecture.md`, `docs/2dFrontend.md`, `docs/database.md`, and any other doc files) and `GEMINI.md` / `CLAUDE.md`.
2. Find all architectural research, dimensions, shapes, materials, and features of Bharati Research Station:
   - R1: Main aerodynamic aluminum shell (extruded geometries, dimensions, 135 container structure, aluminum cladding, elevated stilt grid with cross-bracing, emissive North panoramic window).
   - R2: External assets & infrastructure: 300,000L cylindrical fuel farm, roof HVAC arrays, SATCOM radomes, 15m radius heliport 50m away from main building.
   - R3: Environment & effects: rocky Larsemann Hills terrain plane (displacement), horizontal blizzard particle system blowing underneath the station.
   - Any coordinates, scale factors, color palettes, materials (Three.js MeshStandardMaterial properties like roughness, metalness, colors).

## Input Context
- Project root: `C:\Users\adity\Documents\Coding\Projects\DTFIAS`
- Authoritative user request: `C:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\ORIGINAL_REQUEST.md`
- Constraints: Read-only investigation.

## Deliverable
Write your findings to `C:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\explorer_survey_2\handoff.md`.
Report:
- Specific architectural dimensions, geometric shapes, material properties, and positions.
- Recommendations for Three.js geometry construction (e.g. Shape + ExtrudeGeometry, CylinderGeometry, InstancedMesh, ShaderMaterial/Points for blizzard particles).
- Ground height, stilt layout, fuel farm layout, heliport placement.
