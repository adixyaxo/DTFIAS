## 2026-09-12T05:05:00Z

### Role
Survey Explorer 2 (Architectural & Geometric Specifications)

### Task
Analyze the authoritative architectural specifications in `docs/bharati3d/` and synthesize the exact specifications for `app/static/js/three/station_3d_view.js`:
1. Read `docs/bharati3d/06-subagent_implementation_plan.md` and `docs/bharati3d/05-subagent_synthesis.md`.
2. Extract exact CAD coordinates and profiles:
   - P1 to P11 transverse hull shape (see doc 17 §3 vertex table) and extrusion length (50m, x=-25 to +25).
   - Quad V-stilts (outer & inner port/starboard coordinates, topWidth, height, leg thickness).
   - 28 vertical stilts grid and concrete footings.
   - Prow profile and 6-bay panoramic glazing mullions.
   - Penthouse module, access stairs, corner chamfer bevels, container core blocks (L0, L1, L2).
3. Extract site assets coordinates and geometries: SATCOM radome, fuel farm (13 tanks), helipad with 'H' marking, container depot (25 containers), trace-heated pipe rack, flagpole ridge (5x), meteo mast, meltwater tarn, terrain plane with noise displacement, blizzard particle system (3000 particles).
4. Extract MEP layers (11 exoskeleton portal bents, HVAC supply/return, hydronic heating loops, domestic water, electrical busway) and the exact color hex codes and opacity/visibility mapping for all 7 modes: `exterior`, `xray`, `core_only`, `hvac`, `thermal`, `structural`, `night`.
5. Extract the 21 hotspots in `HOTSPOT_REGISTRY` with exact labels and 3D anchor coordinates.
6. Produce a structured report at `.agents/explorer_survey_2/handoff.md`.
