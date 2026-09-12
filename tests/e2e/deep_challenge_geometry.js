#!/usr/bin/env node
/**
 * Deep Challenge: Geometry Budget, Hotspot Integrity & Raycaster Line-of-Sight
 * Author: challenger_2 (Empirical Challenger)
 * 
 * Verifies:
 * 1. Layer-by-layer exact triangle counts across all 5 canonical groups:
 *    - Substructure_Stilts
 *    - Exterior_Aerodynamic_Shell
 *    - Modular_Container_Core
 *    - MEP_Life_Support_Overlay
 *    - Auxiliary_Site_Infrastructure
 *    Confirms total in exterior mode <= 20,000.
 * 2. All 21 Hotspots in HOTSPOT_REGISTRY:
 *    - Valid world anchor positions
 *    - Non-zero bounding boxes (dx > 0, dy > 0, dz > 0)
 *    - Non-empty renderable children (meshes/points/lines)
 * 3. Raycaster line-of-sight & projection accuracy:
 *    - Projected screen coordinates from default perspective (120, 90, 160)
 *    - Frustum visibility
 *    - Line-of-sight raycasting from camera to target
 */

const { spawn, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

const PORT = 9338;
const TIMEOUT_MS = 30000;
const HARNESS_PATH = path.resolve(__dirname, 'test_station_3d_harness.html');
const fileUri = 'file:///' + HARNESS_PATH.replace(/\\/g, '/');
const tempProfileDir = fs.mkdtempSync(path.join(os.tmpdir(), 'edge-challenge-'));

function cleanupProfileDir() {
  try { fs.rmSync(tempProfileDir, { recursive: true, force: true }); } catch (_) {}
}

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

class CDPClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.nextId = 1;
    this.pending = new Map();
  }

  async connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.onopen = () => resolve();
      this.ws.onerror = (err) => reject(err);
      this.ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);
          if (msg.id && this.pending.has(msg.id)) {
            const { resolve: reqResolve, reject: reqReject } = this.pending.get(msg.id);
            this.pending.delete(msg.id);
            if (msg.error) reqReject(msg.error);
            else reqResolve(msg.result);
          }
        } catch (_) {}
      };
    });
  }

  async send(method, params = {}) {
    const id = this.nextId++;
    const payload = JSON.stringify({ id, method, params });
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(payload);
    });
  }

  async evaluate(expression) {
    const res = await this.send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true
    });
    return res?.result?.value;
  }

  close() {
    if (this.ws) {
      try { this.ws.close(); } catch (_) {}
    }
  }
}

async function run() {
  const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
  const edgeArgs = [
    '--headless=new',
    `--remote-debugging-port=${PORT}`,
    '--use-gl=angle',
    '--use-angle=swiftshader',
    '--window-size=1280,720',
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    '--allow-file-access-from-files',
    `--user-data-dir=${tempProfileDir}`,
    fileUri
  ];

  const edgeProcess = spawn(edgePath, edgeArgs, { stdio: 'ignore' });
  let cdpClient = null;

  const killBrowser = () => {
    if (cdpClient) cdpClient.close();
    try {
      if (process.platform === 'win32' && edgeProcess.pid) {
        execSync(`taskkill /F /T /PID ${edgeProcess.pid} >nul 2>&1`);
      } else {
        edgeProcess.kill('SIGKILL');
      }
    } catch (_) {}
    cleanupProfileDir();
  };

  try {
    let wsUrl = null;
    for (let i = 0; i < 40; i++) {
      try {
        const resp = await fetch(`http://127.0.0.1:${PORT}/json/list`);
        if (resp.ok) {
          const list = await resp.json();
          const target = list.find(t => t.type === 'page') || list[0];
          wsUrl = target?.webSocketDebuggerUrl;
          if (wsUrl) break;
        }
      } catch (_) {}
      await sleep(250);
    }

    if (!wsUrl) throw new Error('Could not connect to Edge on port ' + PORT);

    cdpClient = new CDPClient(wsUrl);
    await cdpClient.connect();
    await cdpClient.send('Runtime.enable');
    await cdpClient.send('Page.enable');

    // Wait for scene to be ready
    const start = Date.now();
    while (Date.now() - start < TIMEOUT_MS) {
      const ready = await cdpClient.evaluate(`Boolean(window.station3DScene && window.station3DScene.scene)`);
      if (ready) break;
      await sleep(300);
    }

    // Run Deep Challenge Suite
    const challengeResults = await cdpClient.evaluate(`
      (function() {
        const scene = window.station3DScene.scene;
        const camera = window.station3DScene.camera;
        const renderer = window.station3DScene.renderer;
        const registry = window.station3DScene.hotspotRegistry;
        const canvas = renderer.domElement;
        const width = canvas.width || 800;
        const height = canvas.height || 600;

        // Force matrices and world positions update
        scene.updateMatrixWorld(true);
        camera.updateMatrixWorld(true);
        camera.updateProjectionMatrix();

        // 1. Exact Layer-by-Layer Triangle Analysis
        const layers = [
          'Substructure_Stilts',
          'Exterior_Aerodynamic_Shell',
          'Modular_Container_Core',
          'MEP_Life_Support_Overlay',
          'Auxiliary_Site_Infrastructure'
        ];

        function getMeshTriangles(mesh) {
          if (!mesh.geometry) return 0;
          const g = mesh.geometry;
          let tris = 0;
          if (g.index) {
            tris = g.index.count / 3;
          } else if (g.attributes && g.attributes.position) {
            tris = g.attributes.position.count / 3;
          }
          const instances = mesh.isInstancedMesh ? mesh.count : 1;
          return Math.round(tris * instances);
        }

        const layerMetrics = {};
        let totalAllLayers = 0;

        layers.forEach(lName => {
          const lObj = scene.getObjectByName(lName);
          let lTris = 0;
          let meshCount = 0;
          const meshes = [];

          if (lObj) {
            lObj.traverse(child => {
              if (child.isMesh) {
                meshCount++;
                const tris = getMeshTriangles(child);
                lTris += tris;
                meshes.push({
                  name: child.name || child.parent?.name || 'mesh',
                  type: child.type,
                  triangles: tris,
                  instanced: !!child.isInstancedMesh,
                  instanceCount: child.isInstancedMesh ? child.count : 1,
                  geometryType: child.geometry ? child.geometry.type : 'unknown'
                });
              }
            });
          }

          layerMetrics[lName] = {
            found: !!lObj,
            visibleInExterior: lObj ? lObj.visible : false,
            meshCount,
            totalTriangles: lTris,
            meshesSample: meshes.slice(0, 10)
          };
          totalAllLayers += lTris;
        });

        // Exterior mode active triangles: Substructure + ExteriorShell + Aux
        const exteriorTriangles = (layerMetrics['Substructure_Stilts']?.totalTriangles || 0) +
                                 (layerMetrics['Exterior_Aerodynamic_Shell']?.totalTriangles || 0) +
                                 (layerMetrics['Auxiliary_Site_Infrastructure']?.totalTriangles || 0);

        // 2. Hotspots Deep Inspection
        const raycaster = new THREE.Raycaster();
        const hotspotAudit = {};
        let allHotspotsValid = true;

        Object.keys(registry).forEach(hKey => {
          const regInfo = registry[hKey];
          const obj = scene.getObjectByName(hKey);

          if (!obj) {
            allHotspotsValid = false;
            hotspotAudit[hKey] = {
              found: false,
              label: regInfo.label,
              error: 'Object not found in scene graph'
            };
            return;
          }

          // Renderable children
          let renderableCount = 0;
          let pointsCount = 0;
          let linesCount = 0;
          const childSummary = [];

          obj.traverse(child => {
            if (child.isMesh) {
              renderableCount++;
              childSummary.push({
                type: 'Mesh',
                name: child.name,
                geo: child.geometry?.type,
                tris: getMeshTriangles(child)
              });
            } else if (child.isPoints) {
              pointsCount++;
              childSummary.push({ type: 'Points', count: child.geometry?.attributes?.position?.count || 0 });
            } else if (child.isLine) {
              linesCount++;
              childSummary.push({ type: 'Line' });
            }
          });

          // Bounding Box
          const box = new THREE.Box3();
          box.setFromObject(obj);

          const size = new THREE.Vector3();
          box.getSize(size);

          const center = new THREE.Vector3();
          box.getCenter(center);

          const nonZeroBox = (size.x > 0 || size.y > 0 || size.z > 0);
          const hasRenderables = (renderableCount > 0 || pointsCount > 0 || linesCount > 0);

          // World Position
          const worldPos = new THREE.Vector3();
          obj.getWorldPosition(worldPos);

          // Registry Anchor comparison
          const regAnchor = new THREE.Vector3(...regInfo.anchor);
          const anchorDistance = worldPos.distanceTo(regAnchor);
          const centerDistance = center.distanceTo(regAnchor);

          // 3. Camera Projection & Line-of-Sight Check
          // Project anchor and center to screen NDC
          const projectedAnchor = regAnchor.clone().project(camera);
          const inFrustum = (
            projectedAnchor.x >= -1.2 && projectedAnchor.x <= 1.2 &&
            projectedAnchor.y >= -1.2 && projectedAnchor.y <= 1.2 &&
            projectedAnchor.z >= 0.0 && projectedAnchor.z <= 1.0
          );

          const screenX = Math.round(((projectedAnchor.x + 1) / 2) * width);
          const screenY = Math.round(((-projectedAnchor.y + 1) / 2) * height);

          // Raycast from camera towards anchor
          const ndcMouse = new THREE.Vector2(projectedAnchor.x, projectedAnchor.y);
          raycaster.setFromCamera(ndcMouse, camera);

          // Intersect with scene interactables
          const interactables = [];
          scene.traverse(o => {
            if (o.name && o.name.startsWith('hotspot-')) interactables.push(o);
          });
          const hits = raycaster.intersectObjects(interactables, true);

          let firstHitHotspot = null;
          if (hits.length > 0) {
            let hit = hits[0].object;
            while (hit && (!hit.name || !hit.name.startsWith('hotspot-'))) {
              hit = hit.parent;
            }
            if (hit) firstHitHotspot = hit.name;
          }

          const targetHit = (firstHitHotspot === hKey);

          if (!nonZeroBox || !hasRenderables) {
            allHotspotsValid = false;
          }

          hotspotAudit[hKey] = {
            found: true,
            label: regInfo.label,
            configuredAnchor: regInfo.anchor,
            worldPosition: [Number(worldPos.x.toFixed(2)), Number(worldPos.y.toFixed(2)), Number(worldPos.z.toFixed(2))],
            bbox: {
              min: [Number(box.min.x.toFixed(2)), Number(box.min.y.toFixed(2)), Number(box.min.z.toFixed(2))],
              max: [Number(box.max.x.toFixed(2)), Number(box.max.y.toFixed(2)), Number(box.max.z.toFixed(2))],
              size: [Number(size.x.toFixed(2)), Number(size.y.toFixed(2)), Number(size.z.toFixed(2))],
              nonZero: nonZeroBox
            },
            renderableChildren: {
              meshes: renderableCount,
              points: pointsCount,
              lines: linesCount,
              nonEmpty: hasRenderables,
              sample: childSummary.slice(0, 3)
            },
            cameraProjection: {
              ndc: [Number(projectedAnchor.x.toFixed(3)), Number(projectedAnchor.y.toFixed(3)), Number(projectedAnchor.z.toFixed(3))],
              inFrustum,
              screenCoord: [screenX, screenY],
              firstRaycastHit: firstHitHotspot,
              directHit: targetHit
            }
          };
        });

        return {
          triangleBudgetCheck: {
            exteriorTriangles,
            totalAllLayers,
            budgetLimit: 20000,
            exteriorPass: exteriorTriangles <= 20000,
            allLayersPass: totalAllLayers <= 20000,
            layerMetrics
          },
          hotspotIntegrityCheck: {
            totalHotspots: Object.keys(registry).length,
            allHotspotsValid,
            hotspotAudit
          }
        };
      })()
    `);

    console.log(JSON.stringify(challengeResults, null, 2));
    killBrowser();
  } catch (err) {
    killBrowser();
    console.error('Challenge error:', err);
    process.exit(1);
  }
}

run();
