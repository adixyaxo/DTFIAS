# Execution Plan — Bharati 3D Digital Twin Refinement (orchestrator_3)

## Objective
Refine the Bharati 3D Digital Twin visualization in `app/static/js/three/station_3d_view.js` to improve realism, fix placement bugs, and remove unwanted animations per R1-R4 with programmatic verification.

## Requirements Breakdown
- **R1: Ground and Terrain Enhancements**
  - Expand ground/land mesh area significantly (width/depth > 200) to eliminate background void surrounding the station.
  - Apply realistic grass/tundra procedural texture/material running bundler-free (e.g. canvas-generated procedural texture or Three.js procedural material).
- **R2: Placement Fixes (Anchor Floating Objects)**
  - Anchor helipad firmly to ground, eliminating floating appearance.
  - Anchor flag poles and flags to ground/appropriate elevation without floating.
- **R3: Remove Unwanted Animations**
  - Remove main building bobbing/floating animation entirely (`stationGroup.position.y` remains strictly constant). All architectural structures static and firmly planted.
- **R4: Color Scheme and Aesthetics**
  - Adjust environment, sky/fog, lighting, and asset color schemes to match a realistic yet stylized Antarctic tundra research station vibe with high contrast and visual appeal.
- **Verification & Acceptance Criteria**
  - Headless verification script verifies:
    1. Main station group `position.y` strictly constant across frames.
    2. Ground/terrain mesh scaled > 200 in width and depth.
    3. Helipad and flag base Y-coordinates aligned with ground elevation.
    4. Scene geometry remains within 20,000 triangle budget (`checkGeometryBudget`).
    5. All 21 hotspots and 7 rendering modes function without regression.

## Multi-Agent Iteration Plan (Pattern 2B)
1. **Phase 1: Exploration & Investigation (3 Explorers in parallel)**
   - `explorer_refine_1`: Examine `station_3d_view.js` animation loop and building bobbing logic (R3), terrain geometry creation, sizing, and material generation (R1).
   - `explorer_refine_2`: Examine helipad and flagpole positioning, hierarchy, Y offsets relative to terrain surface elevation (R2), and lighting/color palette (R4).
   - `explorer_refine_3`: Examine `tests/e2e/test_station_3d_harness.html`, `tests/e2e/verify_3d.js`, and `tests/e2e/test_station_3d_verification.py` to identify required test additions for R1-R4 verification.
2. **Phase 2: Implementation (1 Worker)**
   - `worker_3d_refine`: Implement changes in `app/static/js/three/station_3d_view.js`, update test harness / verification scripts in `tests/e2e/`, run headless verification and pytest.
3. **Phase 3: Independent Review (2 Reviewers in parallel)**
   - `reviewer_refine_1`: Review code correctness, bundler-free compatibility (C17), Three.js contracts (C16), triangle budget, and visual design standards.
   - `reviewer_refine_2`: Review non-regression of 21 hotspots, 7 rendering modes, and test coverage.
4. **Phase 4: Adversarial Challenge (2 Challengers in parallel)**
   - `challenger_refine_1`: Verify constant station Y across frames, terrain bounds >200, helipad/flag anchor elevations.
   - `challenger_refine_2`: Verify triangle budget <= 20,000, 7 modes stress test, 21 hotspots integrity.
5. **Phase 5: Forensic Integrity Audit (1 Auditor)**
   - `auditor_refine_1`: Verify authentic procedural texture, genuine coordinate alignment, no hardcoded cheating.
6. **Phase 6: Gate Verdict & Completion**
   - Synthesize results, update GATE_STATUS.md, produce handoff.md, report to Sentinel.
