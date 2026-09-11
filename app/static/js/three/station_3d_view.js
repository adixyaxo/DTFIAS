/**
 * Bharati Station 3D Digital Twin - Extreme Detail SCADA Hologram
 * Lazy-loaded via Alpine.js on the dashboard.
 */
window.initStation3D = function(containerId) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error("3D Container not found");
        return;
    }
    container.innerHTML = "";

    // 1. Scene Setup
    const scene = new THREE.Scene();
    // Deep dark teal-green background matching --bg-deep
    scene.background = new THREE.Color(0x0B1C18);
    // Add subtle fog for depth and blizzard feel
    scene.fog = new THREE.FogExp2(0x0B1C18, 0.004);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 1, 1000);
    camera.position.set(120, 90, 160);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);

    // Controls (OrbitControls injected dynamically if available, otherwise just manual spin)
    let orbitControls = null;
    if (typeof THREE.OrbitControls !== 'undefined') {
        orbitControls = new THREE.OrbitControls(camera, renderer.domElement);
        orbitControls.enableDamping = true;
        orbitControls.dampingFactor = 0.05;
        orbitControls.maxPolarAngle = Math.PI / 2 - 0.05; // don't go below ground
        orbitControls.target.set(0, 10, 0);
    } else {
        camera.lookAt(0, 10, 0);
    }

    // 2. Lighting - Dramatic Holographic lighting
    const ambientLight = new THREE.AmbientLight(0x1A312C, 2.0); // Brand deep green
    scene.add(ambientLight);

    const mainLight = new THREE.DirectionalLight(0x7DBFAD, 1.5); // Mint accent
    mainLight.position.set(50, 100, 50);
    mainLight.castShadow = true;
    mainLight.shadow.mapSize.width = 2048;
    mainLight.shadow.mapSize.height = 2048;
    mainLight.shadow.camera.near = 0.5;
    mainLight.shadow.camera.far = 300;
    mainLight.shadow.camera.left = -100;
    mainLight.shadow.camera.right = 100;
    mainLight.shadow.camera.top = 100;
    mainLight.shadow.camera.bottom = -100;
    scene.add(mainLight);

    const backLight = new THREE.DirectionalLight(0x428475, 1.0); // Brand teal
    backLight.position.set(-50, 50, -50);
    scene.add(backLight);

    const stationGroup = new THREE.Group();
    scene.add(stationGroup);

    // 3. SCADA Hologram Materials
    // Core material: transparent blue/green with high tech finish
    const matHoloSolid = new THREE.MeshStandardMaterial({
        color: 0x1A312C,
        emissive: 0x05100C,
        roughness: 0.2,
        metalness: 0.8,
        transparent: true,
        opacity: 0.85,
    });
    const matGlass = new THREE.MeshPhysicalMaterial({
        color: 0xC8E6D7,
        emissive: 0x224433,
        transparent: true,
        opacity: 0.6,
        roughness: 0.1,
        transmission: 0.9,
        thickness: 0.5
    });
    const lineMat = new THREE.LineBasicMaterial({ color: 0x428475, transparent: true, opacity: 0.5 });
    const activeLineMat = new THREE.LineBasicMaterial({ color: 0x7DBFAD, transparent: true, opacity: 0.9 });

    // Utility function to add wireframe edges to a mesh
    function addWireframe(mesh, material = lineMat) {
        const edges = new THREE.EdgesGeometry(mesh.geometry);
        const line = new THREE.LineSegments(edges, material);
        mesh.add(line);
    }

    // 4. Constructing Bharati Station
    
    // A. The Ground (Antarctic Ice/Rock)
    const groundGeo = new THREE.PlaneGeometry(300, 300, 32, 32);
    // Displace ground slightly to make it look like uneven ice/rock
    const pos = groundGeo.attributes.position;
    for (let i = 0; i < pos.count; i++) {
        pos.setZ(i, Math.random() * 2 - 1);
    }
    groundGeo.computeVertexNormals();
    const groundMat = new THREE.MeshStandardMaterial({ 
        color: 0x07110D, 
        roughness: 0.9,
        wireframe: true, // SCADA grid look
        transparent: true,
        opacity: 0.3
    });
    const ground = new THREE.Mesh(groundGeo, groundMat);
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -10;
    ground.receiveShadow = true;
    scene.add(ground);

    // B. The Stilts Structure
    const stiltGroup = new THREE.Group();
    const stiltRadius = 0.4;
    const stiltHeight = 16;
    const stiltGeo = new THREE.CylinderGeometry(stiltRadius, stiltRadius, stiltHeight, 8);
    
    // Create a grid of stilts
    for (let x = -30; x <= 30; x += 15) {
        for (let z = -12; z <= 12; z += 12) {
            const stilt = new THREE.Mesh(stiltGeo, matHoloSolid);
            stilt.position.set(x, -2, z);
            stilt.castShadow = true;
            addWireframe(stilt);
            stiltGroup.add(stilt);
        }
    }
    // Cross bracing (X shapes)
    const braceMat = new THREE.LineBasicMaterial({ color: 0x428475, opacity: 0.3, transparent: true });
    for (let x = -30; x < 30; x += 15) {
        const points1 = [new THREE.Vector3(x, -10, 12), new THREE.Vector3(x+15, 6, 12)];
        const points2 = [new THREE.Vector3(x+15, -10, 12), new THREE.Vector3(x, 6, 12)];
        const geo1 = new THREE.BufferGeometry().setFromPoints(points1);
        const geo2 = new THREE.BufferGeometry().setFromPoints(points2);
        stiltGroup.add(new THREE.Line(geo1, braceMat), new THREE.Line(geo2, braceMat));
    }
    stationGroup.add(stiltGroup);

    // C. Main Building Shell (Aerodynamic structure composed of containers)
    // We'll build the primary block, and then slice the edges
    const bldgWidth = 80;
    const bldgDepth = 30;
    const bldgHeight = 14;

    const mainShape = new THREE.Shape();
    mainShape.moveTo(-bldgWidth/2, -bldgDepth/2);
    mainShape.lineTo(bldgWidth/2, -bldgDepth/2);
    mainShape.lineTo(bldgWidth/2, bldgDepth/2);
    mainShape.lineTo(-bldgWidth/2, bldgDepth/2);
    mainShape.lineTo(-bldgWidth/2, -bldgDepth/2);

    const extrudeSettings = {
        steps: 1,
        depth: bldgHeight,
        bevelEnabled: true,
        bevelThickness: 2,
        bevelSize: 2,
        bevelOffset: 0,
        bevelSegments: 3
    };

    const bldgGeo = new THREE.ExtrudeGeometry(mainShape, extrudeSettings);
    // Rotate to lie flat
    bldgGeo.rotateX(Math.PI / 2);
    const mainBuilding = new THREE.Mesh(bldgGeo, matHoloSolid);
    mainBuilding.position.set(0, 20, 0); // raised on stilts
    mainBuilding.castShadow = true;
    mainBuilding.receiveShadow = true;
    mainBuilding.name = "hotspot-main_building";
    addWireframe(mainBuilding, activeLineMat);
    stationGroup.add(mainBuilding);

    // D. Windows / Glazing
    const glassWidth = bldgWidth - 10;
    const glassGeo = new THREE.BoxGeometry(glassWidth, 6, 2);
    const glassMeshFront = new THREE.Mesh(glassGeo, matGlass);
    glassMeshFront.position.set(0, 14, bldgDepth/2 + 0.5);
    addWireframe(glassMeshFront, new THREE.LineBasicMaterial({color: 0xC8E6D7, opacity: 0.8, transparent: true}));
    
    const glassMeshBack = new THREE.Mesh(glassGeo, matGlass);
    glassMeshBack.position.set(0, 14, -bldgDepth/2 - 0.5);
    addWireframe(glassMeshBack, new THREE.LineBasicMaterial({color: 0xC8E6D7, opacity: 0.8, transparent: true}));
    
    stationGroup.add(glassMeshFront, glassMeshBack);

    // E. Roof Details (HVAC / Comms / Environment Sensors)
    const roofY = 20;
    
    // HVAC Units
    const hvacGroup = new THREE.Group();
    hvacGroup.name = "hotspot-hvac";
    const hvacGeo = new THREE.BoxGeometry(4, 3, 4);
    for(let i=0; i<4; i++) {
        const hvac = new THREE.Mesh(hvacGeo, matHoloSolid);
        hvac.position.set(-20 + (i*12), roofY + 1.5, -5);
        addWireframe(hvac);
        hvacGroup.add(hvac);
    }
    stationGroup.add(hvacGroup);

    // SATCOM Domes
    const satcomGroup = new THREE.Group();
    satcomGroup.name = "hotspot-comms_satcom";
    const domeGeo = new THREE.SphereGeometry(3.5, 32, 16, 0, Math.PI*2, 0, Math.PI/2);
    const dome1 = new THREE.Mesh(domeGeo, matHoloSolid);
    dome1.position.set(25, roofY, 5);
    addWireframe(dome1);
    const dome2 = new THREE.Mesh(domeGeo, matHoloSolid);
    dome2.position.set(15, roofY, 5);
    addWireframe(dome2);
    satcomGroup.add(dome1, dome2);
    stationGroup.add(satcomGroup);

    // Weather/Environment Mast
    const mastGroup = new THREE.Group();
    mastGroup.name = "hotspot-environment_sensors";
    const mastGeo = new THREE.CylinderGeometry(0.2, 0.2, 12, 8);
    const mast = new THREE.Mesh(mastGeo, matHoloSolid);
    mast.position.set(-35, roofY + 6, 8);
    addWireframe(mast);
    mastGroup.add(mast);
    stationGroup.add(mastGroup);

    // F. External Assets: Fuel Farm
    const fuelGroup = new THREE.Group();
    fuelGroup.name = "hotspot-fuel_storage";
    const tankGeo = new THREE.CylinderGeometry(2, 2, 8, 16);
    let tankCount = 0;
    for(let i=0; i<3; i++) {
        for(let j=0; j<5; j++) {
            if(tankCount >= 13) break;
            const tank = new THREE.Mesh(tankGeo, matHoloSolid);
            tank.position.set(-45 + (j * 5), -6, -45 + (i * 5));
            tank.castShadow = true;
            addWireframe(tank);
            fuelGroup.add(tank);
            tankCount++;
        }
    }
    stationGroup.add(fuelGroup);

    // G. External Assets: Heliport
    const helipadGroup = new THREE.Group();
    helipadGroup.name = "hotspot-heliport";
    const padGeo = new THREE.CylinderGeometry(18, 18, 1, 32);
    const padMat = new THREE.MeshStandardMaterial({ color: 0x1A312C, emissive: 0x0B1C18, roughness: 0.6 });
    const pad = new THREE.Mesh(padGeo, padMat);
    pad.position.set(60, -9.5, 30);
    pad.receiveShadow = true;
    addWireframe(pad);
    helipadGroup.add(pad);
    
    // Helipad H marker and ring
    const ringGeo = new THREE.RingGeometry(15, 15.5, 32);
    const ringMat = new THREE.MeshBasicMaterial({ color: 0x7DBFAD, side: THREE.DoubleSide });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = Math.PI / 2;
    ring.position.set(60, -8.9, 30);
    helipadGroup.add(ring);
    
    const hGeo = new THREE.BoxGeometry(6, 0.2, 1.5);
    const hMat = new THREE.MeshBasicMaterial({ color: 0x7DBFAD });
    const h1 = new THREE.Mesh(hGeo, hMat); h1.position.set(60, -8.9, 27);
    const h2 = new THREE.Mesh(hGeo, hMat); h2.position.set(60, -8.9, 33);
    const h3 = new THREE.BoxGeometry(1.5, 0.2, 6);
    const h3Mesh = new THREE.Mesh(h3, hMat); h3Mesh.position.set(60, -8.9, 30);
    helipadGroup.add(h1, h2, h3Mesh);
    stationGroup.add(helipadGroup);

    // 5. Blizzard Particle System
    const particleCount = 3000;
    const particlesGeo = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    const particleVelocities = [];

    for (let i = 0; i < particleCount; i++) {
        // distribute over a wide volume
        particlePositions[i*3] = (Math.random() - 0.5) * 300; // x
        particlePositions[i*3 + 1] = Math.random() * 100 - 10; // y
        particlePositions[i*3 + 2] = (Math.random() - 0.5) * 300; // z
        
        particleVelocities.push({
            x: (Math.random() - 0.5) * 0.2 + 0.5, // strong wind in +x
            y: -Math.random() * 0.3 - 0.1,        // falling down
            z: (Math.random() - 0.5) * 0.2        // slight drift in z
        });
    }
    particlesGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    const particleMat = new THREE.PointsMaterial({
        color: 0xC8E6D7,
        size: 0.8,
        transparent: true,
        opacity: 0.6,
        blending: THREE.AdditiveBlending
    });
    const particleSystem = new THREE.Points(particlesGeo, particleMat);
    scene.add(particleSystem);


    // 6. RAYCASTING & ALPINE BRIDGE
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    let hoveredObject = null;

    // Hover effect
    container.addEventListener('pointermove', (event) => {
        const rect = container.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);
        
        const interactables = [];
        stationGroup.traverse((child) => {
            if (child.name && child.name.startsWith('hotspot-')) {
                interactables.push(child);
            }
        });

        const intersects = raycaster.intersectObjects(interactables, false);
        
        // Reset previous hover
        if (hoveredObject && (!intersects.length || intersects[0].object !== hoveredObject)) {
            if (hoveredObject.material.emissive) {
                hoveredObject.material.emissiveIntensity = hoveredObject.userData.origEmissiveIntensity || 0;
            }
            hoveredObject = null;
            container.style.cursor = 'grab';
        }

        if (intersects.length > 0) {
            const hit = intersects[0].object;
            // Ensure we don't highlight the entire ground or non-interactive parts unnecessarily
            if (hit !== hoveredObject) {
                hoveredObject = hit;
                if (hoveredObject.material.emissive !== undefined) {
                    hoveredObject.userData.origEmissiveIntensity = hoveredObject.material.emissiveIntensity;
                    hoveredObject.material.emissiveIntensity = 0.8;
                    hoveredObject.material.emissive.setHex(0x7DBFAD); // hover color
                }
                container.style.cursor = 'pointer';
            }
        }
    });

    container.addEventListener('pointerdown', (event) => {
        const rect = container.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);
        
        const interactables = [];
        stationGroup.traverse((child) => {
            if (child.name && child.name.startsWith('hotspot-')) {
                interactables.push(child);
            }
        });

        const intersects = raycaster.intersectObjects(interactables, false);
        if (intersects.length > 0) {
            let hit = intersects[0].object;
            // If we hit a child inside a group (like a single fuel tank), get the group name
            let name = hit.name;
            if(!name && hit.parent && hit.parent.name.startsWith('hotspot-')) {
                name = hit.parent.name;
            }

            if (name) {
                const assetId = name.replace('hotspot-', '');
                // Dispatch event to be caught by Alpine.js in the DOM
                window.dispatchEvent(new CustomEvent('st-3d-click', { detail: assetId }));
            }
        }
    });

    // Global bridge for Alpine to push state down to 3D
    window.update3DHotspot = function(assetId, status) {
        const target = scene.getObjectByName('hotspot-' + assetId);
        if (!target) return;
        
        // Function to apply material changes to an object and all its children
        const applyStatus = (obj) => {
            if (obj.material && obj.material !== matGlass) {
                // Clone material so we don't change everything sharing it
                obj.material = obj.material.clone();
                if (status === 'critical') {
                    obj.material.color.setHex(0xC44536);
                    obj.material.emissive.setHex(0x9B1C1C);
                    obj.material.emissiveIntensity = 0.6;
                } else if (status === 'warning') {
                    obj.material.color.setHex(0xD9822B);
                    obj.material.emissive.setHex(0x995511);
                    obj.material.emissiveIntensity = 0.5;
                } else {
                    obj.material.color.setHex(0x1A312C);
                    obj.material.emissive.setHex(0x05100C);
                    obj.material.emissiveIntensity = 1.0; // default for hologram
                }
            }
            if (obj.children) {
                obj.children.forEach(child => {
                    // Don't modify wireframes
                    if (!(child instanceof THREE.LineSegments || child instanceof THREE.Line)) {
                       applyStatus(child);
                    }
                });
            }
        };
        applyStatus(target);
    };

    // 7. ANIMATION LOOP
    const clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);
        
        const delta = clock.getDelta();
        const time = clock.getElapsedTime();

        if (orbitControls) orbitControls.update();

        // Slow hover of the station (floating effect)
        stationGroup.position.y = Math.sin(time * 0.5) * 1.5;

        // Rotate satcom domes slowly
        satcomGroup.children.forEach((dome, i) => {
            dome.rotation.y = time * 0.5 * (i % 2 === 0 ? 1 : -1);
        });
        
        // Update particles (Blizzard)
        const positions = particleSystem.geometry.attributes.position.array;
        for (let i = 0; i < particleCount; i++) {
            positions[i*3] += particleVelocities[i].x;
            positions[i*3+1] += particleVelocities[i].y;
            positions[i*3+2] += particleVelocities[i].z;

            // Reset particle if it goes out of bounds
            if (positions[i*3+1] < -10 || positions[i*3] > 150) {
                positions[i*3] = (Math.random() - 0.5) * 300 - 150;
                positions[i*3+1] = 100;
                positions[i*3+2] = (Math.random() - 0.5) * 300;
            }
        }
        particleSystem.geometry.attributes.position.needsUpdate = true;

        renderer.render(scene, camera);
    }
    animate();

    // Handle Window Resize
    window.addEventListener('resize', () => {
        if(!container) return;
        const w = container.clientWidth;
        const h = container.clientHeight;
        renderer.setSize(w, h);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
    });

    // Expose scene for interactions
    window.station3DScene = { scene, group: stationGroup };
    console.log("Bharati 3D Twin (Extreme Detail) Initialized successfully.");
};
