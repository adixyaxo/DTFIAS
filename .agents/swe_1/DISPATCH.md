# Dispatch Instructions

## 2026-09-12T10:15:17Z

You are the SWE Light Orchestrator (teamwork_preview_swe).
Working directory: c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\swe_1
Workspace root: c:\Users\adity\Documents\Coding\Projects\DTFIAS
Original request file: c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\ORIGINAL_REQUEST.md
Dispatch instructions: c:\Users\adity\Documents\Coding\Projects\DTFIAS\.agents\swe_1\DISPATCH.md

Execute the SWE Light loop (one implementer on the whole task, then repeated reviewer rounds) for the following request:
"This is a single self-contained fix; keep it small and focused. Implement a clean 3-column interface redesign for the Bharati 3D Twin dashboard and fix remaining floating 3D objects (flagpoles, container depot, pipe rack) in the Three.js scene.

Requirements:
R1. Ground Fixes (app/static/js/three/station_3d_view.js):
- Pipe Rack: Adjust A-frame length to 2.0m and local y offset to push feet to Y=0 cleanly.
- Flagpoles: Add a small CylinderGeometry(0.4, 0.5, 0.6, 8) concrete plinth at the base of each pole.
- Container Depot: Add a gravel pad (BoxGeometry(36, 0.15, 22)) under the depot at Y=0.07.
- Main station stilt footings: Verify presence of stiltFootingGeo; if missing, add CylinderGeometry(1.2, 1.5, 0.5, 10) concrete footings at each stilt bottom.
(Note: SATCOM radome and Fuel Farm bund have already been implemented).

R2. Minimal 3-column Interface Redesign (app/templates/bharati/station_twin.html):
- Navbar: Slim down to py-2.5, add a ← HQ Dashboard back button (linking to /hq/dashboard), and relocate fault/satcom buttons to the right sidebar.
- Left Sidebar (200px): Fixed width, dark glass background. Move the 3D view mode buttons, Reset Camera, Screenshot, and triangle budget badge here from the floating HUD.
- Right Sidebar (288px): Fixed width, dark glass background. Move category filter tabs here (All, Infrastructure, Energy, Environment, Logistics, Personnel).
- Asset List: Below the tabs in the right sidebar, display a scrollable list of asset cards matching the selected category.
- Inline Detail Panel: Clicking an asset card (or a 3D hotspot) should replace the asset list with the detail panel in-place (not as a slide-out overlay). Add a ← Assets back button to return to the list.

R3. Styling and Logic Wiring:
- CSS (app/static/css/station_twin.css): Add classes for the new sidebars, asset cards, and category tabs. Ensure the layout works cleanly without absolute overlays for the sidebars.
- Alpine.js (app/static/js/station_twin.js): Add a filteredAssets computed property, state for showAssetList, and methods to toggle between the list and detail views (selectAssetFromPanel, backToList). Wire the relocated fault/satcom buttons.

Acceptance Criteria:
Visual Accuracy:
- No objects appear floating in the 3D scene (flagpoles sit on plinths, container depot on a gravel pad).
- The layout is strictly 3-columns: Left Sidebar, Center 3D Canvas, Right Sidebar.
- No layout shift or cream background bleed around the canvas.
Functional Completeness:
- Clicking category tabs correctly filters the asset list in the right sidebar.
- Clicking an asset card in the list or in the 3D scene switches the right sidebar to the detail view.
- Clicking the '← Assets' button in the detail view returns to the filtered asset list.
- View mode buttons in the left sidebar correctly update the 3D scene.
- JavaScript executes without syntax errors.

Integrity mode: benchmark.
Establish correctness by running automated tests/verification scripts. Write your progress to progress.md in your working directory. When complete, write handoff.md and send a completion message back to the Sentinel.
