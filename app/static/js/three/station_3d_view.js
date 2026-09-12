/**
 * Bharati Station 3D Digital Twin - Master SCADA Hologram
 * Digital Twin for Indian Antarctic Stations (SIH26060)
 * Lazy-loaded via Alpine.js on the dashboard / station twin.
 *
 * Architecture:
 * - Substructure_Stilts: Quad V-stilts (4 bents, 22° angle) + 28 vertical stilts grid + concrete footings + knee bracing
 * - Exterior_Aerodynamic_Shell: P1-P11 extruded profile (50m L) + 6-bay prow + penthouse + stairs + chamfers + flag
 * - Modular_Container_Core: L0 utility block, L1 living deck, L2 penthouse spine (X-ray core)
 * - MEP_Life_Support_Overlay: 11 portal bents, HVAC supply/return, hydronic heat, domestic water, electrical busway
 * - Auxiliary_Site_Infrastructure: SATCOM radome (80 faces), fuel farm (13 tanks), helipad, container depot (25 boxes),
 *                                  pipe rack, flagpoles (5x), meteo mast, tarn, terrain, blizzard (3,000 particles)
 * - 7 SCADA Rendering Modes via window.set3DMode(mode)
 * - 21 Canonical Hotspots in HOTSPOT_REGISTRY with raycaster hover/click and window.update3DHotspot bridge
 * - Performance guard checkGeometryBudget (<= 20,000 triangles total in exterior mode)
 */

(function () {
  'use strict';

  // 21 Canonical Hotspots Registry
  const HOTSPOT_REGISTRY = {
    'hotspot-power-plant': { label: 'CHP Power Plant', anchor: [-19.2, 2.8, 7.2] },
    'hotspot-hvac': { label: 'HVAC Life Support', anchor: [-7.2, 10.2, 0.0] },
    'hotspot-chp-heating': { label: 'District Heating', anchor: [-6.0, 3.2, 0.0] },
    'hotspot-water-lss': { label: 'Water & LSS', anchor: [-19.2, 2.8, -7.2] },
    'hotspot-workshop-garage': { label: 'Vehicle Garage', anchor: [-18.0, 3.8, 0.0] },
    'hotspot-main-hab': { label: 'Main Habitat', anchor: [0.0, 5.5, 0.0] },
    'hotspot-dining-mess': { label: 'Dining Mess', anchor: [-18.0, 6.5, 0.0] },
    'hotspot-medical-bay': { label: 'Medical Bay', anchor: [-14.4, 6.5, -7.2] },
    'hotspot-ocean-lounge': { label: 'Ocean Lounge', anchor: [19.0, 6.5, 0.0] },
    'hotspot-science-terrace': { label: 'Science Terrace', anchor: [2.0, 11.5, 0.0] },
    'hotspot-meteo-mast': { label: 'Meteorological Mast', anchor: [0.0, 13.5, 0.0] },
    'hotspot-v-stilts': { label: 'V-Stilt Foundations', anchor: [18.5, 2.1, 0.0] },
    'hotspot-satcom': { label: 'SATCOM Radome', anchor: [-25.0, 7.2, 35.0] },
    'hotspot-fuel-storage': { label: 'Fuel Farm (296 kL)', anchor: [-80.0, 4.0, -35.0] },
    'hotspot-pipe-rack': { label: 'Trace-Heated Pipe Rack', anchor: [0.0, 0.8, 12.0] },
    'hotspot-heliport': { label: 'Heliport Operations', anchor: [-85.0, 4.0, -95.0] },
    'hotspot-container-depot': { label: 'Container Depot', anchor: [-28.0, 0.0, -18.0] },
    'hotspot-meltwater-tarn': { label: 'Meltwater Tarn', anchor: [-35.0, -1.2, 0.0] },
    'hotspot-flagpole-ridge': { label: 'Flagpole & Anemometer', anchor: [-45.0, 2.0, -70.0] },
    'hotspot-meteo-science-lab': { label: 'Science Lab (Meteorology)', anchor: [4.8, 3.5, -7.2] },
    'hotspot-main-entrance': { label: 'Main Entrance Bharati', anchor: [-6.0, 3.8, 10.0] },
  };

  // Performance Guard: Triangle Budget Checker
  function checkGeometryBudget(geometry, label) {
    if (!geometry) return 0;
    const tri = geometry.index
      ? geometry.index.count / 3
      : (geometry.attributes && geometry.attributes.position ? geometry.attributes.position.count / 3 : 0);
    if (tri > 20000) {
      console.warn(`[Bharati3D] Triangle budget exceeded: ${label} = ${tri.toFixed(0)} triangles`);
    }
    return tri;
  }
  window.checkGeometryBudget = checkGeometryBudget;

  // Count total triangles in an object tree
  function countTriangles(obj) {
    let count = 0;
    obj.traverse(child => {
      if (child.isMesh && child.geometry) {
        const g = child.geometry;
        const tri = g.index
          ? g.index.count / 3
          : (g.attributes && g.attributes.position ? g.attributes.position.count / 3 : 0);
        const instances = child.isInstancedMesh ? child.count : 1;
        count += tri * instances;
      }
    });
    return count;
  }

  // Generate procedural canvas texture for Indian National Flag tricolor & Chakra
  function createFlagTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 170;
    const ctx = canvas.getContext('2d');
    if (!ctx) return null;

    const h3 = canvas.height / 3;
    // Saffron top stripe
    ctx.fillStyle = '#FF9933';
    ctx.fillRect(0, 0, canvas.width, h3);
    // White middle stripe
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, h3, canvas.width, h3);
    // Green bottom stripe
    ctx.fillStyle = '#138808';
    ctx.fillRect(0, h3 * 2, canvas.width, h3);

    // Ashoka Chakra (Navy Blue #000080) in center of white band
    const cx = canvas.width / 2;
    const cy = canvas.height / 2;
    const r = h3 * 0.42;

    ctx.strokeStyle = '#000080';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.stroke();

    // Inner hub
    ctx.fillStyle = '#000080';
    ctx.beginPath();
    ctx.arc(cx, cy, r * 0.18, 0, Math.PI * 2);
    ctx.fill();

    // 24 spokes
    ctx.lineWidth = 1.2;
    for (let i = 0; i < 24; i++) {
      const angle = (i * Math.PI) / 12;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx + Math.cos(angle) * r, cy + Math.sin(angle) * r);
      ctx.stroke();
    }

    const tex = new THREE.CanvasTexture(canvas);
    tex.wrapS = THREE.ClampToEdgeWrapping;
    tex.wrapT = THREE.ClampToEdgeWrapping;
    return tex;
  }

  // High-fidelity procedural V-Stilt bent generator (4-segment tapered box)
  function createVStiltBent(topWidth, height, legThickness, stiltMat) {
    const bentGroup = new THREE.Group();
    const legGeo = new THREE.CylinderGeometry(
      legThickness * 1.5, // Top radius (broad)
      legThickness * 0.8, // Bottom radius (tapered)
      height,
      4                   // 4 radial segments = fabricated rectangular box section
    );
    checkGeometryBudget(legGeo, 'VStiltLeg');

    const halfSpread = topWidth * 0.25;
    const inclineAngle = Math.atan2(halfSpread, height);

    const leftLeg = new THREE.Mesh(legGeo, stiltMat);
    leftLeg.position.set(-halfSpread, height * 0.5, 0);
    leftLeg.rotation.z = inclineAngle;
    leftLeg.castShadow = true;
    leftLeg.receiveShadow = true;

    const rightLeg = new THREE.Mesh(legGeo, stiltMat);
    rightLeg.position.set(halfSpread, height * 0.5, 0);
    rightLeg.rotation.z = -inclineAngle;
    rightLeg.castShadow = true;
    rightLeg.receiveShadow = true;

    bentGroup.add(leftLeg, rightLeg);
    return bentGroup;
  }

  // Primary entry point called by Alpine.js
  window.initStation3D = function (containerId) {
    const container = document.getElementById(containerId);
    if (!container) {
      console.error('[Bharati3D] Container not found:', containerId);
      return;
    }
    container.innerHTML = '';

    const width = container.clientWidth || 800;
    const height = container.clientHeight || 600;

    // 1. SCENE BOOTSTRAP & RENDERER
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0B1C18); // DTFIAS --bg-deep
    scene.fog = new THREE.FogExp2(0x0B1C18, 0.004);

    const camera = new THREE.PerspectiveCamera(45, width / height, 1, 2000);
    camera.position.set(120, 90, 160); // NE oblique perspective

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    container.appendChild(renderer.domElement);

    // OrbitControls (safe check)
    let orbitControls = null;
    if (typeof THREE.OrbitControls !== 'undefined') {
      orbitControls = new THREE.OrbitControls(camera, renderer.domElement);
      orbitControls.enableDamping = true;
      orbitControls.dampingFactor = 0.05;
      orbitControls.maxPolarAngle = Math.PI / 2 - 0.05; // Lock above bedrock datum
      orbitControls.target.set(0, 6, 0);
    } else {
      camera.lookAt(0, 6, 0);
    }

    // 2. BRAND LIGHTING SYSTEM (Day & Night)
    const ambientLight = new THREE.AmbientLight(0x1A312C, 2.0); // Brand deep green
    scene.add(ambientLight);

    const mainSun = new THREE.DirectionalLight(0x7DBFAD, 1.5); // Brand polar mint sun
    mainSun.position.set(50, 100, 50);
    mainSun.castShadow = true;
    mainSun.shadow.mapSize.width = 2048;
    mainSun.shadow.mapSize.height = 2048;
    mainSun.shadow.camera.near = 0.5;
    mainSun.shadow.camera.far = 350;
    mainSun.shadow.camera.left = -120;
    mainSun.shadow.camera.right = 120;
    mainSun.shadow.camera.top = 120;
    mainSun.shadow.camera.bottom = -120;
    scene.add(mainSun);

    const backFill = new THREE.DirectionalLight(0x428475, 1.0); // Brand teal backlight
    backFill.position.set(-50, 50, -50);
    scene.add(backFill);

    // Night lighting sources (initially zero intensity)
    const moonLight = new THREE.DirectionalLight(0x6B8BA4, 0.0);
    moonLight.position.set(0, 80, -30);
    scene.add(moonLight);

    const auroraAmbient = new THREE.AmbientLight(0x2A6A4E, 0.0);
    scene.add(auroraAmbient);

    const auroraDirect = new THREE.DirectionalLight(0x4EBA87, 0.0);
    auroraDirect.position.set(0, 50, -20);
    scene.add(auroraDirect);

    // 3. SHARED MATERIAL LIBRARY
    window._bm = {
      hull: new THREE.MeshStandardMaterial({ color: 0xBAC4C7, roughness: 0.28, metalness: 0.80 }),
      roof: new THREE.MeshStandardMaterial({ color: 0x4F6D7A, roughness: 0.35, metalness: 0.85 }),
      keel: new THREE.MeshStandardMaterial({ color: 0x8E9EA4, roughness: 0.45, metalness: 0.70 }),
      glazingDay: new THREE.MeshStandardMaterial({ color: 0x1A312C, roughness: 0.10, metalness: 0.90, transparent: true, opacity: 0.85 }),
      winWarm: new THREE.MeshStandardMaterial({ color: 0xFFAE33, emissive: 0xFF9900, emissiveIntensity: 2.0 }),
      winLab: new THREE.MeshStandardMaterial({ color: 0xE6F2FF, emissive: 0xC8E2FF, emissiveIntensity: 1.8 }),
      vstilt: new THREE.MeshStandardMaterial({ color: 0xB0BFC5, roughness: 0.25, metalness: 0.85 }),
      stairs: new THREE.MeshStandardMaterial({ color: 0xCFD8DC, roughness: 0.40, metalness: 0.90 }),
      concrete: new THREE.MeshStandardMaterial({ color: 0x6D6B66, roughness: 0.80, metalness: 0.05 }),
      ctnGreen: new THREE.MeshStandardMaterial({ color: 0x5C9E68, roughness: 0.70, metalness: 0.20 }),
      ctnWhite: new THREE.MeshStandardMaterial({ color: 0xDCE4E4, roughness: 0.70, metalness: 0.20 }),
      ctnOrange: new THREE.MeshStandardMaterial({ color: 0xC85A32, roughness: 0.70, metalness: 0.20 }),
      fuelTank: new THREE.MeshStandardMaterial({ color: 0x34495E, roughness: 0.55, metalness: 0.40 }),
      radome: new THREE.MeshStandardMaterial({ color: 0xE6EDED, roughness: 0.35, metalness: 0.05, flatShading: true }),
      tarnWater: new THREE.MeshStandardMaterial({ color: 0x1B4D72, roughness: 0.02, metalness: 0.1, transparent: true, opacity: 0.85 }),
      graniteBedrock: new THREE.MeshStandardMaterial({ color: 0x826B50, roughness: 0.85, metalness: 0.10 }),
      steelMep: new THREE.MeshStandardMaterial({ color: 0x2B3A8C, roughness: 0.30, metalness: 0.85 }),
      hvacSupply: new THREE.MeshStandardMaterial({ color: 0x27AE60, roughness: 0.40, metalness: 0.30 }),
      hvacReturn: new THREE.MeshStandardMaterial({ color: 0xF1C40F, roughness: 0.40, metalness: 0.30 }),
      hydronicHeat: new THREE.MeshStandardMaterial({ color: 0xE74C3C, roughness: 0.35, metalness: 0.40 }),
      domesticWater: new THREE.MeshStandardMaterial({ color: 0x2980B9, roughness: 0.35, metalness: 0.40 }),
      electricalBusway: new THREE.MeshStandardMaterial({ color: 0x8E44AD, roughness: 0.40, metalness: 0.50 }),
    };

    // 4. CANONICAL SCENE GROUPS
    const stationGroup = new THREE.Group();
    stationGroup.name = 'stationGroup';

    const substructureGroup = new THREE.Group();
    substructureGroup.name = 'Substructure_Stilts';

    const exteriorShellGroup = new THREE.Group();
    exteriorShellGroup.name = 'Exterior_Aerodynamic_Shell';

    const containerCoreGroup = new THREE.Group();
    containerCoreGroup.name = 'Modular_Container_Core';
    containerCoreGroup.visible = false; // Hidden in default exterior mode

    const mepGroup = new THREE.Group();
    mepGroup.name = 'MEP_Life_Support_Overlay';
    mepGroup.visible = false; // Hidden in default exterior mode

    const auxGroup = new THREE.Group();
    auxGroup.name = 'Auxiliary_Site_Infrastructure';

    // ─── 5. SUBSTRUCTURE: QUAD V-STILTS & 28 VERTICAL STILTS GRID ───
    const vStiltsGroup = new THREE.Group();
    vStiltsGroup.name = 'hotspot-v-stilts';

    // Quad V-Stilts (4 bents under cantilever prow):
    // Outer port: [18.5, 0.0, 8.75], topWidth: 8.75m, height: 4.2m
    const vBentOuterPort = createVStiltBent(8.75, 4.2, 0.45, window._bm.vstilt);
    vBentOuterPort.position.set(18.5, 0.0, 8.75);
    vStiltsGroup.add(vBentOuterPort);

    // Outer starboard: [18.5, 0.0, -8.75], topWidth: 8.75m, height: 4.2m
    const vBentOuterStbd = createVStiltBent(8.75, 4.2, 0.45, window._bm.vstilt);
    vBentOuterStbd.position.set(18.5, 0.0, -8.75);
    vStiltsGroup.add(vBentOuterStbd);

    // Inner port: [14.0, 0.0, 4.80], topWidth: 4.80m, height: 4.2m
    const vBentInnerPort = createVStiltBent(4.80, 4.2, 0.40, window._bm.vstilt);
    vBentInnerPort.position.set(14.0, 0.0, 4.80);
    vStiltsGroup.add(vBentInnerPort);

    // Inner starboard: [14.0, 0.0, -4.80], topWidth: 4.80m, height: 4.2m
    const vBentInnerStbd = createVStiltBent(4.80, 4.2, 0.40, window._bm.vstilt);
    vBentInnerStbd.position.set(14.0, 0.0, -4.80);
    vStiltsGroup.add(vBentInnerStbd);

    substructureGroup.add(vStiltsGroup);

    // 28 Vertical Stilts Grid (Axes 1 to 15, x = -24 to +9.6, z = ±8.4, ±4.8)
    const stiltHeight = 3.2;
    const stiltGeo = new THREE.CylinderGeometry(0.20, 0.20, stiltHeight, 8);
    checkGeometryBudget(stiltGeo, 'VerticalStilts');
    const stiltsIM = new THREE.InstancedMesh(stiltGeo, window._bm.vstilt, 28);
    stiltsIM.castShadow = true;
    stiltsIM.receiveShadow = true;

    // 28 Concrete Footing Pads at Y=0
    const padGeo = new THREE.CylinderGeometry(0.60, 0.60, 0.20, 8);
    checkGeometryBudget(padGeo, 'FootingPads');
    const padsIM = new THREE.InstancedMesh(padGeo, window._bm.concrete, 28);
    padsIM.receiveShadow = true;

    // Knee bracing struts (45° tubular braces)
    const braceGeo = new THREE.CylinderGeometry(0.08, 0.08, 2.6, 6);
    checkGeometryBudget(braceGeo, 'KneeBracing');
    const bracesGroup = new THREE.Group();

    const xAxes = [-24.0, -19.2, -14.4, -9.6, -4.8, 0.0, 4.8]; // 7 transverse axes
    const zLines = [-8.4, -4.8, 4.8, 8.4];                      // 4 columns per axis = 28 total
    let stiltIdx = 0;
    const dummy = new THREE.Object3D();

    xAxes.forEach(x => {
      zLines.forEach(z => {
        // Stilt column matrix
        dummy.position.set(x, stiltHeight * 0.5, z);
        dummy.rotation.set(0, 0, 0);
        dummy.scale.set(1, 1, 1);
        dummy.updateMatrix();
        stiltsIM.setMatrixAt(stiltIdx, dummy.matrix);

        // Footing pad matrix
        dummy.position.set(x, 0.10, z);
        dummy.updateMatrix();
        padsIM.setMatrixAt(stiltIdx, dummy.matrix);

        // Knee brace attached to column
        const brace = new THREE.Mesh(braceGeo, window._bm.vstilt);
        brace.position.set(x, 2.0, z);
        brace.rotation.z = (x < 0 ? 1 : -1) * 0.65;
        bracesGroup.add(brace);

        stiltIdx++;
      });
    });
    stiltsIM.instanceMatrix.needsUpdate = true;
    padsIM.instanceMatrix.needsUpdate = true;

    substructureGroup.add(stiltsIM);
    substructureGroup.add(padsIM);
    substructureGroup.add(bracesGroup);

    // ─── 6. EXTERIOR AERODYNAMIC SHELL (P1-P11 PROFILE & ASSETS) ───
    const mainHabGroup = new THREE.Group();
    mainHabGroup.name = 'hotspot-main-hab';

    // Transverse profile P1-P11 from CAD elevation blueprint 17
    const hullShape = new THREE.Shape();
    hullShape.moveTo(0.0, 2.60);     // P1: Keel bottom center
    hullShape.lineTo(-7.5, 3.40);    // P2: Port stilt haunch
    hullShape.lineTo(-10.0, 5.10);   // P3: Port outer chine (H2)
    hullShape.lineTo(-9.5, 8.95);    // P4: Port upper fascia (H3)
    hullShape.lineTo(-5.0, 10.10);   // P5: Port roof ridge
    hullShape.lineTo(-3.8, 11.58);   // P6: Penthouse port apex (H4)
    hullShape.lineTo(3.8, 11.58);    // P7: Penthouse starboard apex (H4)
    hullShape.lineTo(5.0, 10.10);    // P8: Starboard roof ridge
    hullShape.lineTo(9.5, 8.95);     // P9: Starboard upper fascia (H3)
    hullShape.lineTo(10.0, 5.10);    // P10: Starboard outer chine (H2)
    hullShape.lineTo(7.5, 3.40);     // P11: Starboard stilt haunch
    hullShape.closePath();

    const extrudeSettings = {
      steps: 1,
      depth: 50.0,           // 50m length along X-axis
      bevelEnabled: false,   // Exact blueprint profile
    };
    const hullGeo = new THREE.ExtrudeGeometry(hullShape, extrudeSettings);
    // Align extruded depth along X-axis centered from x = -25.0 to +25.0
    hullGeo.rotateY(Math.PI / 2);
    hullGeo.translate(-25.0, 0, 0);
    checkGeometryBudget(hullGeo, 'MainHullExtrude');

    const hullMesh = new THREE.Mesh(hullGeo, window._bm.hull);
    hullMesh.castShadow = true;
    hullMesh.receiveShadow = true;
    mainHabGroup.add(hullMesh);

    // Recessed Ribbon Window Bands (North & South walls, Y = 7.8 to 9.0)
    const ribbonGeo = new THREE.BoxGeometry(46.0, 1.2, 0.15);
    checkGeometryBudget(ribbonGeo, 'RibbonWindows');

    const northRibbon = new THREE.Mesh(ribbonGeo, window._bm.glazingDay);
    northRibbon.position.set(0, 8.4, -9.55);
    mainHabGroup.add(northRibbon);

    const southRibbon = new THREE.Mesh(ribbonGeo, window._bm.glazingDay);
    southRibbon.position.set(0, 8.4, 9.55);
    mainHabGroup.add(southRibbon);

    // Vertical window mullions along north and south ribbon bays
    const mullionGeo = new THREE.BoxGeometry(0.08, 1.2, 0.18);
    for (let x = -20; x <= 20; x += 2.4) {
      const nMul = new THREE.Mesh(mullionGeo, window._bm.roof);
      nMul.position.set(x, 8.4, -9.55);
      mainHabGroup.add(nMul);

      const sMul = new THREE.Mesh(mullionGeo, window._bm.roof);
      sMul.position.set(x, 8.4, 9.55);
      mainHabGroup.add(sMul);
    }

    // 6-Bay Panoramic Prow Glazing (15° negative rake at eastern tip x = +24.5)
    const prowGlazingGroup = new THREE.Group();
    const prowGlazingGeo = new THREE.BoxGeometry(0.12, 3.0, 12.0);
    checkGeometryBudget(prowGlazingGeo, 'ProwGlazing');
    const prowGlazingMesh = new THREE.Mesh(prowGlazingGeo, window._bm.glazingDay);
    prowGlazingMesh.position.set(24.5, 6.6, 0.0);
    prowGlazingMesh.rotation.z = -0.26; // ~15° negative rake inward slope
    prowGlazingGroup.add(prowGlazingMesh);

    // 5 vertical structural mullions across the 6 prow bays
    const prowMullionGeo = new THREE.BoxGeometry(0.18, 3.0, 0.15);
    const mullionZ = [-4.0, -2.0, 0.0, 2.0, 4.0];
    mullionZ.forEach(z => {
      const m = new THREE.Mesh(prowMullionGeo, window._bm.roof);
      m.position.set(24.5, 6.6, z);
      m.rotation.z = -0.26;
      prowGlazingGroup.add(m);
    });
    mainHabGroup.add(prowGlazingGroup);

    // Level 2 Penthouse at [0, 10.34, 0]
    const penthouseGeo = new THREE.BoxGeometry(15.0, 2.8, 7.5);
    checkGeometryBudget(penthouseGeo, 'Penthouse');
    const penthouseMesh = new THREE.Mesh(penthouseGeo, window._bm.roof);
    penthouseMesh.position.set(0.0, 10.34, 0.0);
    penthouseMesh.castShadow = true;
    mainHabGroup.add(penthouseMesh);

    // Penthouse perimeter safety railing
    const railBarGeo = new THREE.BoxGeometry(14.8, 0.05, 0.05);
    const railNorth = new THREE.Mesh(railBarGeo, window._bm.stairs);
    railNorth.position.set(0.0, 11.9, -3.7);
    const railSouth = new THREE.Mesh(railBarGeo, window._bm.stairs);
    railSouth.position.set(0.0, 11.9, 3.7);
    mainHabGroup.add(railNorth, railSouth);

    // 3x CHP Generator Exhaust Flues at [-9.6, 12.2, 3.5]
    const flueGeo = new THREE.CylinderGeometry(0.15, 0.15, 1.4, 8);
    checkGeometryBudget(flueGeo, 'ExhaustFlues');
    [-0.5, 0.0, 0.5].forEach(offset => {
      const flue = new THREE.Mesh(flueGeo, window._bm.stairs);
      flue.position.set(-9.6 + offset, 12.2, 3.5);
      flue.castShadow = true;
      mainHabGroup.add(flue);
    });

    // 4x 45° Corner Chamfer Bevels at hull extremities
    const chamferGeo = new THREE.BoxGeometry(1.2, 6.5, 0.08);
    const chamfers = [
      { pos: [-24.8, 6.5, -9.8], rotY: Math.PI / 4 },
      { pos: [-24.8, 6.5, 9.8], rotY: -Math.PI / 4 },
      { pos: [24.8, 6.5, -9.8], rotY: -Math.PI / 4 },
      { pos: [24.8, 6.5, 9.8], rotY: Math.PI / 4 },
    ];
    chamfers.forEach(ch => {
      const chamferMesh = new THREE.Mesh(chamferGeo, window._bm.roof);
      chamferMesh.position.set(ch.pos[0], ch.pos[1], ch.pos[2]);
      chamferMesh.rotation.y = ch.rotY;
      mainHabGroup.add(chamferMesh);
    });

    // 2x Symmetrical 13-step Industrial Access Stairs
    function createStaircase(sideMultiplier) {
      const stairGroup = new THREE.Group();
      const stepWidth = 1.2;
      const stepDepth = 0.28;
      const stepRise = 0.18;
      const stepGeo = new THREE.BoxGeometry(stepDepth, stepRise, stepWidth);

      for (let i = 0; i < 13; i++) {
        const step = new THREE.Mesh(stepGeo, window._bm.stairs);
        step.position.set(i * stepDepth, i * stepRise, 0);
        step.castShadow = true;
        stairGroup.add(step);
      }

      // Handrails
      const railGeo = new THREE.CylinderGeometry(0.03, 0.03, 4.4, 6);
      const handrail = new THREE.Mesh(railGeo, window._bm.stairs);
      handrail.position.set(6 * stepDepth, 6 * stepRise + 0.9, stepWidth * 0.5);
      handrail.rotation.z = -0.57; // 32.7° slope
      stairGroup.add(handrail);

      stairGroup.position.set(18.0, 0.0, sideMultiplier * 9.5);
      return stairGroup;
    }
    const portStairs = createStaircase(1);
    const stbdStairs = createStaircase(-1);
    mainHabGroup.add(portStairs, stbdStairs);

    // Indian National Flag Emblem on North Chamfer Panel
    const flagTexture = createFlagTexture();
    const flagMat = new THREE.MeshStandardMaterial({
      map: flagTexture,
      roughness: 0.3,
      metalness: 0.1,
    });
    const flagGeo = new THREE.PlaneGeometry(1.8, 1.2);
    checkGeometryBudget(flagGeo, 'IndianFlag');
    const flagMesh = new THREE.Mesh(flagGeo, flagMat);
    flagMesh.name = 'flagEmblem';
    flagMesh.position.set(0.0, 5.0, -10.08);
    flagMesh.rotation.x = -0.45; // Match chamfer panel slope
    mainHabGroup.add(flagMesh);

    exteriorShellGroup.add(mainHabGroup);

    // Science Terrace Hotspot Object atop Penthouse
    const sciTerraceGroup = new THREE.Group();
    sciTerraceGroup.name = 'hotspot-science-terrace';
    const sciDeckGeo = new THREE.BoxGeometry(6.0, 0.2, 5.0);
    const sciDeckMesh = new THREE.Mesh(sciDeckGeo, window._bm.stairs);
    sciDeckMesh.position.set(2.0, 11.5, 0.0);
    sciTerraceGroup.add(sciDeckMesh);
    exteriorShellGroup.add(sciTerraceGroup);

    // Main Entrance Airlock Hotspot Object
    const entranceGroup = new THREE.Group();
    entranceGroup.name = 'hotspot-main-entrance';
    const entranceDoorGeo = new THREE.BoxGeometry(1.5, 2.2, 0.2);
    const entranceDoorMesh = new THREE.Mesh(entranceDoorGeo, window._bm.vstilt);
    entranceDoorMesh.position.set(-6.0, 3.8, 9.9);
    entranceGroup.add(entranceDoorMesh);
    exteriorShellGroup.add(entranceGroup);

    // ─── 7. MODULAR CONTAINER CORE (X-RAY LAYER & INTERIOR HOTSPOTS) ───
    // L0 Utility Block (Terracotta / Orange)
    const l0Geo = new THREE.BoxGeometry(24.0, 3.8, 19.0);
    checkGeometryBudget(l0Geo, 'L0_Utility_Block');
    const l0Mesh = new THREE.Mesh(l0Geo, window._bm.ctnOrange);
    l0Mesh.position.set(-12.0, 2.8, 0.0);
    containerCoreGroup.add(l0Mesh);

    // L1 Living Deck (North = Green, South = White)
    const l1NorthGeo = new THREE.BoxGeometry(48.0, 3.0, 9.5);
    checkGeometryBudget(l1NorthGeo, 'L1_Living_North');
    const l1NorthMesh = new THREE.Mesh(l1NorthGeo, window._bm.ctnGreen);
    l1NorthMesh.position.set(0.0, 6.5, -4.75);
    containerCoreGroup.add(l1NorthMesh);

    const l1SouthGeo = new THREE.BoxGeometry(48.0, 3.0, 9.5);
    checkGeometryBudget(l1SouthGeo, 'L1_Living_South');
    const l1SouthMesh = new THREE.Mesh(l1SouthGeo, window._bm.ctnWhite);
    l1SouthMesh.position.set(0.0, 6.5, 4.75);
    containerCoreGroup.add(l1SouthMesh);

    // L2 Penthouse Spine (White)
    const l2Geo = new THREE.BoxGeometry(15.0, 2.5, 7.5);
    checkGeometryBudget(l2Geo, 'L2_Penthouse_Spine');
    const l2Mesh = new THREE.Mesh(l2Geo, window._bm.ctnWhite);
    l2Mesh.position.set(0.0, 9.8, 0.0);
    containerCoreGroup.add(l2Mesh);

    // Interior Functional Hotspot Modules (Interactive containers inside core)
    const interiorHotspots = [
      { id: 'hotspot-power-plant', pos: [-19.2, 2.8, 7.2], size: [4.8, 2.4, 3.5], mat: window._bm.ctnOrange },
      { id: 'hotspot-water-lss', pos: [-19.2, 2.8, -7.2], size: [4.8, 2.4, 3.5], mat: window._bm.ctnOrange },
      { id: 'hotspot-workshop-garage', pos: [-18.0, 3.8, 0.0], size: [6.0, 2.8, 4.5], mat: window._bm.ctnOrange },
      { id: 'hotspot-chp-heating', pos: [-6.0, 3.2, 0.0], size: [4.8, 2.2, 3.5], mat: window._bm.ctnOrange },
      { id: 'hotspot-dining-mess', pos: [-18.0, 6.5, 0.0], size: [6.0, 2.4, 4.5], mat: window._bm.ctnGreen },
      { id: 'hotspot-medical-bay', pos: [-14.4, 6.5, -7.2], size: [4.8, 2.4, 3.5], mat: window._bm.ctnWhite },
      { id: 'hotspot-ocean-lounge', pos: [19.0, 6.5, 0.0], size: [6.0, 2.4, 6.0], mat: window._bm.winLab },
      { id: 'hotspot-meteo-science-lab', pos: [4.8, 3.5, -7.2], size: [4.8, 2.4, 3.5], mat: window._bm.ctnGreen },
    ];
    interiorHotspots.forEach(hs => {
      const g = new THREE.Group();
      g.name = hs.id;
      const bGeo = new THREE.BoxGeometry(hs.size[0], hs.size[1], hs.size[2]);
      const m = new THREE.Mesh(bGeo, hs.mat);
      m.position.set(hs.pos[0], hs.pos[1], hs.pos[2]);
      g.add(m);
      containerCoreGroup.add(g);
    });

    // ─── 8. MEP LIFE SUPPORT OVERLAYS (6 SCADA LAYERS) ───
    // 8.1 StructuralFrameMesh: 11 portal bents at 4.8m spacing
    const structFrameGroup = new THREE.Group();
    structFrameGroup.name = 'StructuralFrameMesh';
    structFrameGroup.visible = false;

    const bentShape = new THREE.Shape();
    bentShape.moveTo(0.0, 2.60);
    bentShape.lineTo(-7.5, 3.40);
    bentShape.lineTo(-10.0, 5.10);
    bentShape.lineTo(-9.5, 8.95);
    bentShape.lineTo(-5.0, 10.10);
    bentShape.lineTo(-3.8, 11.58);
    bentShape.lineTo(3.8, 11.58);
    bentShape.lineTo(5.0, 10.10);
    bentShape.lineTo(9.5, 8.95);
    bentShape.lineTo(10.0, 5.10);
    bentShape.lineTo(7.5, 3.40);
    bentShape.closePath();

    const bentGeo = new THREE.ExtrudeGeometry(bentShape, { depth: 0.35, bevelEnabled: false });
    bentGeo.rotateY(Math.PI / 2);
    checkGeometryBudget(bentGeo, 'ExoskeletonBent');

    for (let i = 0; i < 11; i++) {
      const bent = new THREE.Mesh(bentGeo, window._bm.steelMep);
      bent.position.set(-24.0 + i * 4.8, 0, 0);
      structFrameGroup.add(bent);
    }
    mepGroup.add(structFrameGroup);

    // 8.2 HVACSupplyMesh: Green trunk + 24 vertical drops
    const hvacSupplyGroup = new THREE.Group();
    hvacSupplyGroup.name = 'HVACSupplyMesh';
    hvacSupplyGroup.visible = false;

    const supTrunkGeo = new THREE.BoxGeometry(42.0, 0.5, 0.8);
    checkGeometryBudget(supTrunkGeo, 'HVACSupplyTrunk');
    const supTrunk = new THREE.Mesh(supTrunkGeo, window._bm.hvacSupply);
    supTrunk.position.set(0.0, 9.0, 0.0);
    hvacSupplyGroup.add(supTrunk);

    const dropGeo = new THREE.CylinderGeometry(0.12, 0.12, 2.4, 8);
    for (let i = -11; i <= 12; i++) {
      const drop = new THREE.Mesh(dropGeo, window._bm.hvacSupply);
      drop.position.set(i * 1.8, 7.8, (i % 2 === 0 ? 1 : -1) * 3.5);
      hvacSupplyGroup.add(drop);
    }
    mepGroup.add(hvacSupplyGroup);

    // 8.3 HVACReturnMesh: Yellow parallel duct
    const hvacReturnGroup = new THREE.Group();
    hvacReturnGroup.name = 'HVACReturnMesh';
    hvacReturnGroup.visible = false;

    const retTrunkGeo = new THREE.BoxGeometry(42.0, 0.45, 0.7);
    checkGeometryBudget(retTrunkGeo, 'HVACReturnTrunk');
    const retTrunk = new THREE.Mesh(retTrunkGeo, window._bm.hvacReturn);
    retTrunk.position.set(0.0, 9.0, 1.2);
    hvacReturnGroup.add(retTrunk);
    mepGroup.add(hvacReturnGroup);

    // 8.4 HydronicHeatMesh: Red perimeter loops
    const hydronicGroup = new THREE.Group();
    hydronicGroup.name = 'HydronicHeatMesh';
    hydronicGroup.visible = false;

    const heatPipeGeo = new THREE.BoxGeometry(44.0, 0.12, 0.12);
    const pipeNorth = new THREE.Mesh(heatPipeGeo, window._bm.hydronicHeat);
    pipeNorth.position.set(0.0, 3.2, -7.0);
    const pipeSouth = new THREE.Mesh(heatPipeGeo, window._bm.hydronicHeat);
    pipeSouth.position.set(0.0, 3.2, 7.0);
    hydronicGroup.add(pipeNorth, pipeSouth);
    mepGroup.add(hydronicGroup);

    // 8.5 DomesticWaterMesh: Blue potable/greywater circuit
    const waterGroup = new THREE.Group();
    waterGroup.name = 'DomesticWaterMesh';
    waterGroup.visible = false;

    const waterPipeGeo = new THREE.BoxGeometry(38.0, 0.08, 0.08);
    const waterPipe = new THREE.Mesh(waterPipeGeo, window._bm.domesticWater);
    waterPipe.position.set(-2.0, 3.0, -2.5);
    waterGroup.add(waterPipe);
    mepGroup.add(waterGroup);

    // 8.6 ElectricalBuswayMesh: Purple busway trays
    const buswayGroup = new THREE.Group();
    buswayGroup.name = 'ElectricalBuswayMesh';
    buswayGroup.visible = false;

    const busGeo = new THREE.BoxGeometry(46.0, 0.10, 0.40);
    const busNorth = new THREE.Mesh(busGeo, window._bm.electricalBusway);
    busNorth.position.set(0.0, 8.5, -1.0);
    const busSouth = new THREE.Mesh(busGeo, window._bm.electricalBusway);
    busSouth.position.set(0.0, 8.5, 1.0);
    buswayGroup.add(busNorth, busSouth);
    mepGroup.add(buswayGroup);

    // Rooftop HVAC Hotspot Unit atop penthouse
    const hvacHotspotGroup = new THREE.Group();
    hvacHotspotGroup.name = 'hotspot-hvac';
    const ahuGeo = new THREE.BoxGeometry(4.0, 1.5, 2.5);
    const ahuMesh = new THREE.Mesh(ahuGeo, window._bm.hvacSupply);
    ahuMesh.position.set(-7.2, 10.2, 0.0);
    hvacHotspotGroup.add(ahuMesh);
    mepGroup.add(hvacHotspotGroup);

    // Attach primary station groups
    stationGroup.add(substructureGroup);
    stationGroup.add(exteriorShellGroup);
    stationGroup.add(containerCoreGroup);
    stationGroup.add(mepGroup);
    scene.add(stationGroup);

    // ─── 9. AUXILIARY SITE INFRASTRUCTURE & ENVIRONMENT ───
    // 9.1 SATCOM Geodesic Radome: IcosahedronGeometry(5.2, 2) => 80 faces
    const satcomGroup = new THREE.Group();
    satcomGroup.name = 'hotspot-satcom';
    satcomGroup.position.set(-25.0, 7.2, 35.0);

    const radomeGeo = new THREE.IcosahedronGeometry(5.2, 2);
    checkGeometryBudget(radomeGeo, 'SatcomRadome');
    const satcomDomeMesh = new THREE.Mesh(radomeGeo, window._bm.radome);
    satcomDomeMesh.castShadow = true;
    satcomGroup.add(satcomDomeMesh);

    // Ring truss base at Y = 2.0 (relative to group Y=7.2 -> offset -5.2)
    const satcomBaseGeo = new THREE.CylinderGeometry(5.0, 5.0, 0.3, 32);
    checkGeometryBudget(satcomBaseGeo, 'SatcomBase');
    const satcomBase = new THREE.Mesh(satcomBaseGeo, window._bm.stairs);
    satcomBase.position.set(0, -5.0, 0);
    satcomGroup.add(satcomBase);

    // 10 Tubular Stilts supporting SATCOM base
    const satcomStiltGeo = new THREE.CylinderGeometry(0.12, 0.12, 2.2, 8);
    for (let i = 0; i < 10; i++) {
      const angle = (i * Math.PI * 2) / 10;
      const st = new THREE.Mesh(satcomStiltGeo, window._bm.vstilt);
      st.position.set(Math.cos(angle) * 4.8, -6.1, Math.sin(angle) * 4.8);
      satcomGroup.add(st);
    }
    auxGroup.add(satcomGroup);

    // 9.2 Fuel Farm: 13 Cylindrical Tanks (296 kL bulk reserves)
    const fuelFarmGroup = new THREE.Group();
    fuelFarmGroup.name = 'hotspot-fuel-storage';

    const tankGeo = new THREE.CylinderGeometry(2.5, 2.5, 8.0, 16);
    checkGeometryBudget(tankGeo, 'FuelTank');
    const fuelIM = new THREE.InstancedMesh(tankGeo, window._bm.fuelTank, 13);
    fuelIM.castShadow = true;
    fuelIM.receiveShadow = true;

    // 3 rows: Row 1 (5 tanks), Row 2 (5 tanks), Row 3 (3 tanks)
    const fuelPositions = [];
    for (let c = 0; c < 5; c++) fuelPositions.push([-80.0 + c * 6.0, 4.0, -35.0]);
    for (let c = 0; c < 5; c++) fuelPositions.push([-80.0 + c * 6.0, 4.0, -42.0]);
    for (let c = 0; c < 3; c++) fuelPositions.push([-74.0 + c * 6.0, 4.0, -49.0]);

    fuelPositions.forEach((pos, idx) => {
      dummy.position.set(pos[0], pos[1], pos[2]);
      dummy.rotation.set(0, 0, 0);
      dummy.scale.set(1, 1, 1);
      dummy.updateMatrix();
      fuelIM.setMatrixAt(idx, dummy.matrix);
    });
    fuelIM.instanceMatrix.needsUpdate = true;
    fuelFarmGroup.add(fuelIM);
    auxGroup.add(fuelFarmGroup);

    // 9.3 Helipad with 'H' Marking & Windsock
    const helipadGroup = new THREE.Group();
    helipadGroup.name = 'hotspot-heliport';
    helipadGroup.position.set(-85.0, 4.0, -95.0);

    const padGeo3D = new THREE.CylinderGeometry(15.0, 15.0, 0.5, 32);
    checkGeometryBudget(padGeo3D, 'HelipadBase');
    const padMesh = new THREE.Mesh(padGeo3D, window._bm.concrete);
    padMesh.receiveShadow = true;
    helipadGroup.add(padMesh);

    // Border ring (r = 13.0 to 13.5m)
    const ringGeo = new THREE.RingGeometry(13.0, 13.5, 64);
    checkGeometryBudget(ringGeo, 'HelipadRing');
    const ringMat = new THREE.MeshBasicMaterial({ color: 0xFFFFFF, side: THREE.DoubleSide });
    const ringMesh = new THREE.Mesh(ringGeo, ringMat);
    ringMesh.rotation.x = -Math.PI / 2;
    ringMesh.position.y = 0.26;
    helipadGroup.add(ringMesh);

    // 'H' Marking geometry
    const hBarGeo = new THREE.BoxGeometry(0.8, 0.05, 6.0);
    const hCrossGeo = new THREE.BoxGeometry(3.0, 0.05, 0.8);
    const hLeg1 = new THREE.Mesh(hBarGeo, ringMat);
    hLeg1.position.set(-1.5, 0.27, 0);
    const hLeg2 = new THREE.Mesh(hBarGeo, ringMat);
    hLeg2.position.set(1.5, 0.27, 0);
    const hCross = new THREE.Mesh(hCrossGeo, ringMat);
    hCross.position.set(0, 0.27, 0);
    helipadGroup.add(hLeg1, hLeg2, hCross);

    // Windsock at pad perimeter
    const poleGeo = new THREE.CylinderGeometry(0.05, 0.05, 4.0, 8);
    const poleMesh = new THREE.Mesh(poleGeo, window._bm.stairs);
    poleMesh.position.set(14.0, 2.0, 0);
    const sockGeo = new THREE.CylinderGeometry(0.18, 0.08, 1.6, 8);
    const sockMat = new THREE.MeshStandardMaterial({ color: 0xE85D04, roughness: 0.5 });
    const sockMesh = new THREE.Mesh(sockGeo, sockMat);
    sockMesh.position.set(14.8, 3.8, 0);
    sockMesh.rotation.z = Math.PI / 2;
    helipadGroup.add(poleMesh, sockMesh);
    auxGroup.add(helipadGroup);

    // 9.4 Container Depot (NW Apron, 25 ISO Boxes, 5x5 Grid)
    const containerDepotGroup = new THREE.Group();
    containerDepotGroup.name = 'hotspot-container-depot';

    const isoBoxGeo = new THREE.BoxGeometry(6.06, 2.59, 2.44);
    checkGeometryBudget(isoBoxGeo, 'ISOContainer');
    const depotMat = new THREE.MeshStandardMaterial({ roughness: 0.6, metalness: 0.3 });
    const depotIM = new THREE.InstancedMesh(isoBoxGeo, depotMat, 25);
    depotIM.castShadow = true;
    depotIM.receiveShadow = true;

    const depotPalette = [0xE85D04, 0x008751, 0x0B4F6C, 0x8C3828];
    let ctnIdx = 0;
    for (let r = 0; r < 5; r++) {
      for (let c = 0; c < 5; c++) {
        dummy.position.set(-28.0 - r * 6.8, 1.30, -18.0 - c * 3.2);
        dummy.rotation.set(0, (r % 2 === 0 ? 0 : 0.05), 0);
        dummy.scale.set(1, 1, 1);
        dummy.updateMatrix();
        depotIM.setMatrixAt(ctnIdx, dummy.matrix);
        depotIM.setColorAt(ctnIdx, new THREE.Color(depotPalette[(r + c) % 4]));
        ctnIdx++;
      }
    }
    depotIM.instanceMatrix.needsUpdate = true;
    if (depotIM.instanceColor) depotIM.instanceColor.needsUpdate = true;
    containerDepotGroup.add(depotIM);
    auxGroup.add(containerDepotGroup);

    // 9.5 Trace-Heated Pipe Rack on A-Frames
    const pipeRackGroup = new THREE.Group();
    pipeRackGroup.name = 'hotspot-pipe-rack';
    pipeRackGroup.position.set(0.0, 0.8, 12.0);

    const pipeGeo = new THREE.BoxGeometry(32.0, 0.20, 0.60);
    checkGeometryBudget(pipeGeo, 'PipeRackTray');
    const pipeMesh = new THREE.Mesh(pipeGeo, window._bm.stairs);
    pipeRackGroup.add(pipeMesh);

    // A-Frames every 6 meters
    const aFrameGeo = new THREE.CylinderGeometry(0.06, 0.06, 1.8, 6);
    for (let x = -15; x <= 15; x += 6) {
      const legL = new THREE.Mesh(aFrameGeo, window._bm.vstilt);
      legL.position.set(x, -0.4, -0.4);
      legL.rotation.x = 0.2;
      const legR = new THREE.Mesh(aFrameGeo, window._bm.vstilt);
      legR.position.set(x, -0.4, 0.4);
      legR.rotation.x = -0.2;
      pipeRackGroup.add(legL, legR);
    }
    auxGroup.add(pipeRackGroup);

    // 9.6 Flagpole Ridge (5 Masts)
    const flagpoleGroup = new THREE.Group();
    flagpoleGroup.name = 'hotspot-flagpole-ridge';
    flagpoleGroup.position.set(-45.0, 2.0, -70.0);

    const mastGeo = new THREE.CylinderGeometry(0.04, 0.04, 8.0, 6);
    checkGeometryBudget(mastGeo, 'FlagpoleMast');
    for (let i = 0; i < 5; i++) {
      const pole = new THREE.Mesh(mastGeo, window._bm.stairs);
      pole.position.set(i * 3.0, 4.0, 0);
      pole.castShadow = true;

      // Pennant cloth
      const pennantGeo = new THREE.PlaneGeometry(0.9, 0.6);
      const pennantMat = new THREE.MeshBasicMaterial({
        color: (i === 0 ? 0xFF9933 : (i === 1 ? 0x428475 : 0xE6EDED)),
        side: THREE.DoubleSide
      });
      const pennant = new THREE.Mesh(pennantGeo, pennantMat);
      pennant.position.set(i * 3.0 + 0.45, 7.5, 0);
      flagpoleGroup.add(pole, pennant);
    }
    auxGroup.add(flagpoleGroup);

    // 9.7 Meteorological Mast atop Penthouse
    const meteoMastGroup = new THREE.Group();
    meteoMastGroup.name = 'hotspot-meteo-mast';
    meteoMastGroup.position.set(0.0, 13.5, 0.0);

    const meteoMastGeo = new THREE.CylinderGeometry(0.06, 0.06, 5.0, 6);
    checkGeometryBudget(meteoMastGeo, 'MeteoMast');
    const meteoPole = new THREE.Mesh(meteoMastGeo, window._bm.stairs);
    meteoMastGroup.add(meteoPole);

    // Anemometer cross-arms
    const armGeo = new THREE.CylinderGeometry(0.02, 0.02, 1.6, 6);
    const arm = new THREE.Mesh(armGeo, window._bm.stairs);
    arm.position.set(0, 2.2, 0);
    arm.rotation.z = Math.PI / 2;
    meteoMastGroup.add(arm);
    auxGroup.add(meteoMastGroup);

    // 9.8 Meltwater Tarn
    const tarnGroup = new THREE.Group();
    tarnGroup.name = 'hotspot-meltwater-tarn';
    tarnGroup.position.set(-35.0, -1.2, 0.0);

    const tarnGeo = new THREE.PlaneGeometry(60.0, 40.0, 1, 1);
    checkGeometryBudget(tarnGeo, 'TarnWaterPlane');
    const tarnMesh = new THREE.Mesh(tarnGeo, window._bm.tarnWater);
    tarnMesh.rotation.x = -Math.PI / 2;
    tarnGroup.add(tarnMesh);
    auxGroup.add(tarnGroup);

    // 9.9 Displaced Granite Terrain Plane (Pad flattened at Y=0)
    const terrainGeo = new THREE.PlaneGeometry(300, 300, 48, 48);
    terrainGeo.rotateX(-Math.PI / 2);
    const posAttr = terrainGeo.attributes.position;

    for (let i = 0; i < posAttr.count; i++) {
      const vx = posAttr.getX(i);
      const vz = posAttr.getZ(i);
      const distFromCenter = Math.sqrt(vx * vx + vz * vz);

      if (distFromCenter < 35.0) {
        // Flat bedrock pad directly under the station
        posAttr.setY(i, 0.0);
      } else {
        // Natural rocky Antarctic ridge displacement
        let elevation = Math.sin(vx * 0.03) * 2.5 + Math.cos(vz * 0.03) * 2.2;
        // North slope drops down to Prydz Bay ocean level
        if (vz < -40.0) {
          elevation -= (Math.abs(vz) - 40.0) * 0.22;
        }
        // Western tarn depression
        const distTarn = Math.sqrt((vx + 35.0) ** 2 + vz ** 2);
        if (distTarn < 25.0) {
          elevation -= (1.0 - distTarn / 25.0) * 3.5;
        }
        posAttr.setY(i, elevation);
      }
    }
    terrainGeo.computeVertexNormals();
    checkGeometryBudget(terrainGeo, 'TerrainPlane');

    const terrainMesh = new THREE.Mesh(terrainGeo, window._bm.graniteBedrock);
    terrainMesh.receiveShadow = true;
    auxGroup.add(terrainMesh);

    // 9.10 Blizzard Particle System (3,000 particles)
    const particleCount = 3000;
    const particleGeo = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    const particleVelocities = [];

    for (let i = 0; i < particleCount; i++) {
      particlePositions[i * 3] = (Math.random() - 0.5) * 300;
      particlePositions[i * 3 + 1] = Math.random() * 110 - 10;
      particlePositions[i * 3 + 2] = (Math.random() - 0.5) * 300;

      // Katabatic wind drifting through elevated underbelly
      particleVelocities.push({
        x: 0.35 + Math.random() * 0.35,
        y: -0.12 - Math.random() * 0.15,
        z: (Math.random() - 0.5) * 0.15,
      });
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));

    const particleMat = new THREE.PointsMaterial({
      color: 0xC8E6D7,
      size: 0.8,
      blending: THREE.AdditiveBlending,
      transparent: true,
      opacity: 0.65,
    });
    const particleSystem = new THREE.Points(particleGeo, particleMat);
    auxGroup.add(particleSystem);

    scene.add(auxGroup);

    // Log total exterior triangle count and verify against budget
    const totalExteriorTriangles = countTriangles(stationGroup) + countTriangles(auxGroup);
    console.log(`[Bharati3D] Total exterior geometry triangles: ${totalExteriorTriangles} (Budget: <= 20,000)`);
    if (totalExteriorTriangles > 20000) {
      console.warn(`[Bharati3D] WARNING: Total exterior geometry exceeds 20,000 triangle budget!`);
    }

    // ─── 10. SCADA 7-MODE CONTROLLER ───
    window.set3DMode = function (mode) {
      const m = mode || 'exterior';

      const isExterior = (m === 'exterior' || m === 'night');
      const isCoreOnly = (m === 'core_only');
      const isXRay = (m === 'xray');
      const isMEPMode = (m === 'hvac' || m === 'thermal' || m === 'structural');

      // 1. Exterior shell visibility & transparency
      exteriorShellGroup.visible = !isCoreOnly;
      const targetOpacity = isExterior ? 1.0 : (isXRay ? 0.25 : (isMEPMode ? 0.15 : 1.0));
      const targetTransparent = !isExterior;

      exteriorShellGroup.traverse(child => {
        if (child.isMesh && child.name !== 'flagEmblem') {
          if (child.material) {
            child.material.transparent = targetTransparent;
            child.material.opacity = targetOpacity;
            child.material.needsUpdate = true;
          }
        }
      });

      // 2. Modular Container Core visibility
      containerCoreGroup.visible = (isXRay || isCoreOnly);

      // 3. MEP Overlays visibility & selective system activation
      mepGroup.visible = isMEPMode;
      const sMesh = mepGroup.getObjectByName('StructuralFrameMesh');
      const hSupMesh = mepGroup.getObjectByName('HVACSupplyMesh');
      const hRetMesh = mepGroup.getObjectByName('HVACReturnMesh');
      const hydMesh = mepGroup.getObjectByName('HydronicHeatMesh');
      const watMesh = mepGroup.getObjectByName('DomesticWaterMesh');
      const busMesh = mepGroup.getObjectByName('ElectricalBuswayMesh');

      if (sMesh) sMesh.visible = (m === 'structural');
      if (hSupMesh) hSupMesh.visible = (m === 'hvac');
      if (hRetMesh) hRetMesh.visible = (m === 'hvac');
      if (hydMesh) hydMesh.visible = (m === 'thermal');
      if (watMesh) watMesh.visible = false;
      if (busMesh) busMesh.visible = false;

      // 4. Lighting & Nocturnal Glazing
      if (m === 'night') {
        mainSun.intensity = 0.05;
        backFill.intensity = 0.05;
        ambientLight.color.setHex(0x1A2B3C);
        ambientLight.intensity = 0.35;
        moonLight.intensity = 0.45;
        auroraAmbient.intensity = 0.45;
        auroraDirect.intensity = 0.65;

        prowGlazingMesh.material = window._bm.winWarm;
        northRibbon.material = window._bm.winWarm;
        southRibbon.material = window._bm.winWarm;
      } else {
        mainSun.intensity = 1.5;
        backFill.intensity = 1.0;
        ambientLight.color.setHex(0x1A312C);
        ambientLight.intensity = 2.0;
        moonLight.intensity = 0.0;
        auroraAmbient.intensity = 0.0;
        auroraDirect.intensity = 0.0;

        prowGlazingMesh.material = window._bm.glazingDay;
        northRibbon.material = window._bm.glazingDay;
        southRibbon.material = window._bm.glazingDay;
      }

      console.log(`[Bharati3D] SCADA Mode switched to: ${m}`);
    };

    // ─── 11. RAYCASTING, HOVER HIGHLIGHT & CLICK DISPATCH ───
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    let hoveredHotspot = null;
    const hotspotStatusMap = {};

    function getInteractables() {
      const list = [];
      scene.traverse(obj => {
        if (obj.name && obj.name.startsWith('hotspot-')) {
          list.push(obj);
        }
      });
      return list;
    }

    container.addEventListener('pointermove', event => {
      const rect = container.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const interactables = getInteractables();
      const intersects = raycaster.intersectObjects(interactables, true);

      let currentHitHotspot = null;
      if (intersects.length > 0) {
        let hit = intersects[0].object;
        while (hit && (!hit.name || !hit.name.startsWith('hotspot-'))) {
          hit = hit.parent;
        }
        if (hit && hit.name && hit.name.startsWith('hotspot-')) {
          currentHitHotspot = hit;
        }
      }

      if (hoveredHotspot !== currentHitHotspot) {
        // Restore previous hovered object
        if (hoveredHotspot) {
          const activeStatus = hotspotStatusMap[hoveredHotspot.name];
          hoveredHotspot.traverse(child => {
            if (child.isMesh && child.userData.isHovered) {
              if (child.material && child.material.emissive !== undefined) {
                let restoreEmissiveHex = child.userData.origEmissiveHex !== undefined
                  ? child.userData.origEmissiveHex
                  : 0x000000;
                let restoreIntensity = child.userData.origEmissiveIntensity !== undefined
                  ? child.userData.origEmissiveIntensity
                  : 0.0;

                if (activeStatus === 'critical') {
                  restoreEmissiveHex = 0x9B1C1C;
                  restoreIntensity = 0.8;
                } else if (activeStatus === 'warning') {
                  restoreEmissiveHex = 0x995511;
                  restoreIntensity = 0.6;
                }

                child.material.emissive.setHex(restoreEmissiveHex);
                child.material.emissiveIntensity = restoreIntensity;
              }
              child.userData.isHovered = false;
            }
          });
        }

        hoveredHotspot = currentHitHotspot;

        // Apply emissive highlight to newly hovered hotspot
        if (hoveredHotspot) {
          hoveredHotspot.traverse(child => {
            if (child.isMesh && child.material && child.material.emissive !== undefined) {
              if (!child.userData.isHovered) {
                child.userData.origEmissiveHex = child.material.emissive.getHex();
                child.userData.origEmissiveIntensity = child.material.emissiveIntensity;
                child.userData.isHovered = true;
              }
              child.material.emissive.setHex(0x7DBFAD); // Brand mint highlight
              child.material.emissiveIntensity = 0.8;
            }
          });
          container.style.cursor = 'pointer';
        } else {
          container.style.cursor = 'default';
        }
      }
    });

    container.addEventListener('pointerdown', event => {
      const rect = container.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const interactables = getInteractables();
      const intersects = raycaster.intersectObjects(interactables, true);

      if (intersects.length > 0) {
        let hit = intersects[0].object;
        while (hit && (!hit.name || !hit.name.startsWith('hotspot-'))) {
          hit = hit.parent;
        }
        if (hit && hit.name && hit.name.startsWith('hotspot-')) {
          const assetSlug = hit.name.replace('hotspot-', '');
          console.log(`[Bharati3D] Hotspot clicked: ${assetSlug}`);
          window.dispatchEvent(new CustomEvent('st-3d-click', { detail: assetSlug }));
        }
      }
    });

    // ─── 12. TELEMETRY STATUS BRIDGE (window.update3DHotspot) ───
    window.update3DHotspot = function (assetId, status) {
      if (!assetId) return;
      const idStr = (typeof assetId === 'object' && assetId !== null && assetId.id)
        ? String(assetId.id)
        : String(assetId ?? '');
      if (!idStr) return;
      const lookupName = idStr.startsWith('hotspot-') ? idStr : 'hotspot-' + idStr;
      hotspotStatusMap[lookupName] = status;
      const target = scene.getObjectByName(lookupName);
      if (!target) return;

      target.traverse(obj => {
        if (obj.isMesh && !(obj instanceof THREE.LineSegments || obj instanceof THREE.Line)) {
          if (obj.material) {
            // Save original attributes on first encounter
            if (!obj.userData._origMaterial) {
              obj.userData._origMaterial = obj.material;
              obj.userData._origColor = obj.material.color ? obj.material.color.getHex() : null;
              obj.userData._origEmissive = obj.material.emissive ? obj.material.emissive.getHex() : 0;
              obj.userData._origEmissiveIntensity = obj.material.emissiveIntensity !== undefined ? obj.material.emissiveIntensity : 0;
            }

            const targetColorHex = (status === 'critical') ? 0xC44536 : ((status === 'warning') ? 0xD9822B : (obj.userData._origColor));
            const targetEmissiveHex = (status === 'critical') ? 0x9B1C1C : ((status === 'warning') ? 0x995511 : (obj.userData._origEmissive || 0x000000));
            const targetEmissiveIntensity = (status === 'critical') ? 0.8 : ((status === 'warning') ? 0.6 : (obj.userData._origEmissiveIntensity || 0.0));

            // If mesh is currently hovered, ensure unhover cache preserves the active alert styling
            if (obj.userData.isHovered) {
              obj.userData.origEmissiveHex = targetEmissiveHex;
              obj.userData.origEmissiveIntensity = targetEmissiveIntensity;
            }

            // Only update/clone if status actually changed
            if (obj.userData._currentStatus === status) {
              return;
            }
            obj.userData._currentStatus = status;

            if (status === 'critical' || status === 'warning') {
              if (!obj.userData._isClonedMaterial) {
                obj.material = obj.material.clone();
                obj.userData._isClonedMaterial = true;
              }
              if (obj.material.color && targetColorHex !== null) {
                obj.material.color.setHex(targetColorHex);
              }
              if (obj.material.emissive) {
                obj.material.emissive.setHex(targetEmissiveHex);
                obj.material.emissiveIntensity = targetEmissiveIntensity;
              }
            } else {
              // Normal status -> restore original material properties
              if (obj.userData._origMaterial) {
                obj.material = obj.userData._origMaterial;
                obj.userData._isClonedMaterial = false;
              }
              if (obj.material.color && obj.userData._origColor !== null) {
                obj.material.color.setHex(obj.userData._origColor);
              }
              if (obj.material.emissive) {
                obj.material.emissive.setHex(obj.userData._origEmissive || 0x000000);
                obj.material.emissiveIntensity = obj.userData._origEmissiveIntensity || 0.0;
              }
            }
            obj.material.needsUpdate = true;
          }
        }
      });
    };

    // ─── 13. ANIMATION LOOP ───
    const clock = new THREE.Clock();

    function animate() {
      requestAnimationFrame(animate);

      const delta = clock.getDelta();
      const time = clock.getElapsedTime();

      if (orbitControls) orbitControls.update();

      // Subtle ambient station vertical float (period ~12s, magnitude 1.5m)
      stationGroup.position.y = Math.sin(time * 0.524) * 1.5;

      // Slow SATCOM radome rotation (0.5 rpm)
      if (satcomDomeMesh) {
        satcomDomeMesh.rotation.y = time * 0.052;
      }

      // Blizzard particle animation
      const pos = particleSystem.geometry.attributes.position.array;
      for (let i = 0; i < particleCount; i++) {
        pos[i * 3] += particleVelocities[i].x;
        pos[i * 3 + 1] += particleVelocities[i].y;
        pos[i * 3 + 2] += particleVelocities[i].z;

        // Reset particles that drift out of bounds
        if (pos[i * 3] > 150 || pos[i * 3 + 1] < -10) {
          pos[i * 3] = -150 + Math.random() * 20;
          pos[i * 3 + 1] = 80 + Math.random() * 20;
          pos[i * 3 + 2] = (Math.random() - 0.5) * 300;
        }
      }
      particleSystem.geometry.attributes.position.needsUpdate = true;

      renderer.render(scene, camera);
    }
    animate();

    // ─── 14. RESIZE HANDLER ───
    window.addEventListener('resize', () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      if (w > 0 && h > 0) {
        renderer.setSize(w, h);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
      }
    });

    // ─── 15. SCENE EXPORT ───
    window.station3DScene = {
      scene,
      camera,
      renderer,
      stationGroup,
      mepGroup,
      substructureGroup,
      exteriorShellGroup,
      containerCoreGroup,
      auxGroup,
      setMode: window.set3DMode,
      updateHotspot: window.update3DHotspot,
      hotspotRegistry: HOTSPOT_REGISTRY,
      checkGeometryBudget,
    };

    console.log(`[Bharati3D] Digital Twin initialized. Active hotspots: ${Object.keys(HOTSPOT_REGISTRY).length}`);
  };

})();
