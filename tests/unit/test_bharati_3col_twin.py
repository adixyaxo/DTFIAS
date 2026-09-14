"""
Automated Verification Suite for Bharati 3D Twin 3-Column Redesign and Ground Fixes.
Requirements verified:
- R1: Ground Fixes (app/static/js/three/station_3d_view.js)
  - Pipe rack A-frame 2.0m length and local y offset 0.18m
  - Flagpole plinth CylinderGeometry(0.4, 0.5, 0.6, 8)
  - Container depot gravel pad BoxGeometry(36, 0.15, 22) at Y=0.07
  - Main station stilt footings stiltFootingGeo CylinderGeometry(1.2, 1.5, 0.5, 10) at Y=0.25
- R2: 3-Column Interface Redesign (app/templates/bharati/station_twin.html)
  - Slim navbar py-2.5, ← HQ Dashboard back button linking to /hq/dashboard
  - Left Sidebar (200px) with 3D view modes, camera reset, screenshot, triangle budget
  - Center 3D canvas with container, tooltip, legend
  - Right Sidebar (288px) with relocated fault/satcom buttons, category filter tabs
  - In-place toggle between asset list and inline detail panel with ← Assets back button
- R3: Styling and Logic Wiring (station_twin.css & station_twin.js)
  - CSS classes for 3-column layout, sidebars, asset cards, category tabs
  - Alpine.js filteredAssets computed property, showAssetList state, selectAssetFromPanel, backToList
"""

import re
import pathlib
import pytest

REPO_ROOT = pathlib.Path(__file__).parent.parent.parent
STATION_3D_JS = REPO_ROOT / "app" / "static" / "js" / "three" / "station_3d_view.js"
STATION_TWIN_HTML = REPO_ROOT / "app" / "templates" / "bharati" / "station_twin.html"
STATION_TWIN_JS = REPO_ROOT / "app" / "static" / "js" / "station_twin.js"
STATION_TWIN_CSS = REPO_ROOT / "app" / "static" / "css" / "station_twin.css"


class TestR1GroundFixes:
    """R1: Ground Fixes in app/static/js/three/station_3d_view.js"""

    def test_pipe_rack_aframe_and_offset(self):
        content = STATION_3D_JS.read_text(encoding="utf-8")
        assert "THREE.CylinderGeometry(0.06, 0.06, 2.0, 6)" in content, (
            "Pipe rack A-frame geometry must have length 2.0m"
        )
        assert "aFrameLocalY = 0.18" in content, (
            "Pipe rack A-frame local y offset must be set to 0.18 to push feet to Y=0 cleanly"
        )
        assert "legL.position.set(x, aFrameLocalY, -0.4)" in content
        assert "legR.position.set(x, aFrameLocalY, 0.4)" in content

    def test_flagpole_concrete_plinth(self):
        content = STATION_3D_JS.read_text(encoding="utf-8")
        assert "THREE.CylinderGeometry(0.4, 0.5, 0.6, 8)" in content, (
            "Flagpole must include concrete plinth with CylinderGeometry(0.4, 0.5, 0.6, 8)"
        )
        assert "plinthGeo = new THREE.CylinderGeometry(0.4, 0.5, 0.6, 8)" in content
        assert "flagpoleGroup.add(pole, pennant, plinth)" in content

    def test_container_depot_gravel_pad(self):
        content = STATION_3D_JS.read_text(encoding="utf-8")
        assert "THREE.BoxGeometry(36, 0.15, 22)" in content, (
            "Container depot must include gravel pad BoxGeometry(36, 0.15, 22)"
        )
        assert "gravelPad.position.set(-41.6, 0.07, -24.4)" in content, (
            "Gravel pad must be positioned at Y=0.07 under the depot containers"
        )
        assert "containerDepotGroup.add(gravelPad)" in content

    def test_main_station_stilt_footings(self):
        content = STATION_3D_JS.read_text(encoding="utf-8")
        assert "stiltFootingGeo = new THREE.CylinderGeometry(1.2, 1.5, 0.5, 10)" in content, (
            "stiltFootingGeo must exist with CylinderGeometry(1.2, 1.5, 0.5, 10)"
        )
        assert "dummy.position.set(x, 0.25, z)" in content, (
            "Stilt footing pads must be placed at Y=0.25 to sit on bedrock at Y=0"
        )


class TestR2InterfaceRedesign:
    """R2: Minimal 3-column Interface Redesign in app/templates/bharati/station_twin.html"""

    def test_slim_navbar_and_back_button(self):
        content = STATION_TWIN_HTML.read_text(encoding="utf-8")
        assert "py-2.5" in content, "Navbar must be slimmed down to py-2.5"
        assert 'href="/hq/dashboard"' in content, "Navbar must contain link to /hq/dashboard"
        assert "HQ Dashboard" in content, "Navbar back button must link to HQ Dashboard"
        # Ensure fault/satcom buttons are NOT in navbar header
        header_match = re.search(r"<header.*?</header>", content, re.DOTALL)
        assert header_match is not None
        header_text = header_match.group(0)
        assert "simulateFault()" not in header_text, "Fault button must be relocated from navbar"
        assert "toggleSatcom()" not in header_text, "SATCOM button must be relocated from navbar"

    def test_left_sidebar_200px(self):
        content = STATION_TWIN_HTML.read_text(encoding="utf-8")
        assert "twin-left-sidebar" in content, "Left sidebar must have twin-left-sidebar class"
        assert "set3DViewMode('exterior')" in content
        assert "set3DViewMode('xray')" in content
        assert "set3DViewMode('hvac')" in content
        assert "set3DViewMode('thermal')" in content
        assert "set3DViewMode('structural')" in content
        assert "set3DViewMode('night')" in content
        assert "resetCamera3D()" in content
        assert "screenshot3D()" in content
        assert "triCount3D" in content

    def test_right_sidebar_288px_and_tabs(self):
        content = STATION_TWIN_HTML.read_text(encoding="utf-8")
        assert "twin-right-sidebar" in content, "Right sidebar must have twin-right-sidebar class"
        assert "simulateFault()" in content, "Right sidebar must contain relocated fault trigger"
        assert "toggleSatcom()" in content, "Right sidebar must contain relocated SATCOM toggle"
        # Category tabs
        assert "activeLayer==='all'" in content
        assert "activeLayer==='infrastructure'" in content
        assert "activeLayer==='energy'" in content
        assert "activeLayer==='environmental'" in content or "activeLayer==='environment'" in content
        assert "activeLayer==='logistics'" in content
        assert "activeLayer==='personnel'" in content

    def test_asset_list_and_inline_detail_panel(self):
        content = STATION_TWIN_HTML.read_text(encoding="utf-8")
        assert "x-show=\"showAssetList\"" in content
        assert "filteredAssets" in content
        assert "selectAssetFromPanel" in content
        assert "backToList()" in content
        assert "←" in content and "Assets" in content

    @pytest.mark.asyncio
    async def test_endpoint_renders_3col_layout_ok(self):
        """Verify the FastAPI endpoint /bharati/station-twin actually renders HTTP 200 with the 3col layout."""
        from httpx import AsyncClient, ASGITransport
        from main import app
        from infrastructure.security.authorization.rbac import create_access_token
        from uuid import uuid4

        token = create_access_token(
            data={"sub": str(uuid4()), "username": "test_operator", "roles": ["bharati_operator"]}
        )
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            ac.cookies.set("dtfias_session", token)
            response = await ac.get("/bharati/station-twin")
            assert response.status_code == 200
            html = response.text
            assert "twin-3col-container" in html
            assert "twin-left-sidebar" in html
            assert "twin-canvas-center" in html
            assert "twin-right-sidebar" in html
            assert 'href="/hq/dashboard"' in html
            assert "filteredAssets" in html
            assert "showAssetList" in html
            assert "selectAssetFromPanel" in html
            assert "backToList()" in html


class TestR3StylingAndWiring:
    """R3: Styling in station_twin.css and Alpine logic in station_twin.js"""

    def test_css_classes(self):
        content = STATION_TWIN_CSS.read_text(encoding="utf-8")
        assert ".twin-3col-container" in content
        assert ".twin-left-sidebar" in content
        assert "width: 200px" in content
        assert ".twin-right-sidebar" in content
        assert "width: 288px" in content
        assert ".twin-canvas-center" in content
        assert ".twin-tab-btn" in content
        assert ".twin-asset-list" in content
        assert ".twin-asset-card" in content
        assert ".twin-back-btn" in content

    def test_alpine_state_and_methods(self):
        content = STATION_TWIN_JS.read_text(encoding="utf-8")
        assert "showAssetList: true" in content
        assert "get filteredAssets()" in content
        assert "selectAssetFromPanel(id)" in content
        assert "backToList()" in content
        assert "_resolveAssetId" in content

    def test_alpine_filtered_assets_logic(self):
        """Execute the Alpine component definition in Node.js to test data and logic directly."""
        import subprocess
        js_test = """
        const fs = require('fs');
        global.window = { STATION_ID: 'bharati' };
        const code = fs.readFileSync('app/static/js/station_twin.js', 'utf8');
        const fn = new Function(code + '; return stationTwin();');
        const instance = fn();

        // Check initial state
        if (instance.showAssetList !== true) throw new Error('showAssetList should be true initially');
        if (instance.activeAsset !== null) throw new Error('activeAsset should be null initially');

        // Check filteredAssets: all
        instance.activeLayer = 'all';
        if (instance.filteredAssets.length !== instance.assets.length) {
            throw new Error(`filteredAssets mismatch: expected ${instance.assets.length}, got ${instance.filteredAssets.length}`);
        }

        // Check filteredAssets: energy
        instance.activeLayer = 'energy';
        const energyAssets = instance.filteredAssets;
        if (energyAssets.length !== 2) throw new Error(`Expected 2 energy assets, got ${energyAssets.length}`);
        if (!energyAssets.every(a => a.category === 'energy')) throw new Error('All should be energy');

        // Check selectAssetFromPanel
        instance.selectAssetFromPanel('power_plant');
        if (instance.showAssetList !== false) throw new Error('showAssetList should be false after selection');
        if (!instance.activeAsset || instance.activeAsset.id !== 'power_plant') throw new Error('activeAsset not set');

        // Check 3D slug resolution in selectAsset
        instance.selectAsset('power-plant');
        if (!instance.activeAsset || instance.activeAsset.id !== 'power_plant') throw new Error('Failed to resolve power-plant slug');

        instance.selectAsset('satcom');
        if (!instance.activeAsset || instance.activeAsset.id !== 'comms_satcom') throw new Error('Failed to resolve satcom slug');

        instance.selectAsset('main-hab');
        if (!instance.activeAsset || instance.activeAsset.id !== 'main_building') throw new Error('Failed to resolve main-hab slug');

        instance.selectAsset('pipe-rack');
        if (!instance.activeAsset || instance.activeAsset.id !== 'seawater_intake') throw new Error('Failed to resolve pipe-rack slug');

        // Check backToList
        instance.backToList();
        if (instance.showAssetList !== true) throw new Error('showAssetList should be true after backToList');
        if (instance.activeAsset !== null) throw new Error('activeAsset should be null after backToList');

        console.log('ALL_LOGIC_PASSED');
        """
        proc = subprocess.run(["node", "-e", js_test], capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert proc.returncode == 0, f"Node logic test failed: {proc.stderr}\n{proc.stdout}"
        assert "ALL_LOGIC_PASSED" in proc.stdout

    def test_3d_hover_tooltip_dict_lookup(self):
        """Verify that station_3d_view.js does NOT call .find on HOTSPOT_REGISTRY object."""
        content = STATION_3D_JS.read_text(encoding="utf-8")
        assert "HOTSPOT_REGISTRY.find" not in content, (
            "HOTSPOT_REGISTRY is an Object and must not call .find (causes TypeError)"
        )
        assert "HOTSPOT_REGISTRY[hoveredHotspot.name]" in content or "HOTSPOT_REGISTRY[slug]" in content

    def test_2d_to_3d_camera_focus_bridge(self):
        """Verify that window.focus3DHotspot is defined and exposed for 2D-to-3D camera fly-to."""
        content_3d = STATION_3D_JS.read_text(encoding="utf-8")
        assert "window.focus3DHotspot = function" in content_3d
        assert "focusHotspot: window.focus3DHotspot" in content_3d

        content_twin = STATION_TWIN_JS.read_text(encoding="utf-8")
        assert "window.focus3DHotspot(resolved || id)" in content_twin

    def test_all_21_hotspot_slugs_resolution(self):
        """Verify that every one of the 21 canonical hotspots in HOTSPOT_REGISTRY resolves to a known asset ID."""
        import subprocess
        test_script = """
        const fs = require('fs');
        global.window = { STATION_ID: 'bharati' };
        const code = fs.readFileSync('app/static/js/station_twin.js', 'utf8');
        const fn = new Function(code + '; return stationTwin();');
        const inst = fn();

        const HOTSPOTS_21 = [
          'power-plant', 'hvac', 'chp-heating', 'water-lss', 'workshop-garage',
          'main-hab', 'dining-mess', 'medical-bay', 'ocean-lounge', 'science-terrace',
          'meteo-mast', 'v-stilts', 'satcom', 'fuel-storage', 'pipe-rack',
          'heliport', 'container-depot', 'meltwater-tarn', 'flagpole-ridge',
          'meteo-science-lab', 'main-entrance'
        ];

        const validIds = new Set(inst.assets.map(a => a.id));
        for (const slug of HOTSPOTS_21) {
          const resolved = inst._resolveAssetId(slug);
          if (!validIds.has(resolved)) {
            throw new Error(`Slug ${slug} resolved to ${resolved}, which is not in assets`);
          }
        }
        console.log('ALL_21_HOTSPOTS_RESOLVED_OK');
        """
        proc = subprocess.run(["node", "-e", test_script], capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert proc.returncode == 0, f"Hotspot resolution failed: {proc.stderr}"
        assert "ALL_21_HOTSPOTS_RESOLVED_OK" in proc.stdout

    def test_acknowledge_alert_immediate_3d_update(self):
        """Verify that acknowledgeAlert updates 3D hotspot emissive state immediately."""
        content = STATION_TWIN_JS.read_text(encoding="utf-8")
        assert "acknowledgeAlert(assetId)" in content
        assert "window.update3DHotspot(a.id, a.status)" in content

