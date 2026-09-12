const { spawn, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

const PORT = 9340;
const HARNESS_PATH = path.resolve(__dirname, 'test_station_3d_harness.html');
const fileUri = 'file:///' + HARNESS_PATH.replace(/\\/g, '/');
const tempProfileDir = fs.mkdtempSync(path.join(os.tmpdir(), 'edge-ray-'));

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const edgeArgs = [
  '--headless=new',
  '--remote-debugging-port=' + PORT,
  '--use-gl=angle',
  '--use-angle=swiftshader',
  '--window-size=1280,720',
  '--disable-gpu',
  '--allow-file-access-from-files',
  '--user-data-dir=' + tempProfileDir,
  fileUri
];

const edgeProcess = spawn(edgePath, edgeArgs, { stdio: 'ignore' });

setTimeout(async () => {
  try {
    const listRes = await fetch('http://127.0.0.1:' + PORT + '/json/list');
    const list = await listRes.json();
    const wsUrl = (list.find(t => t.type === 'page') || list[0]).webSocketDebuggerUrl;
    const ws = new WebSocket(wsUrl);
    ws.onopen = async () => {
      let id = 1;
      const send = (method, params = {}) => new Promise(res => {
        const cur = id++;
        const onMsg = (e) => {
          const d = JSON.parse(e.data);
          if (d.id === cur) {
            ws.removeEventListener('message', onMsg);
            res(d.result);
          }
        };
        ws.addEventListener('message', onMsg);
        ws.send(JSON.stringify({ id: cur, method, params }));
      });

      await send('Runtime.enable');
      await new Promise(r => setTimeout(r, 2500));

      const res = await send('Runtime.evaluate', {
        expression: `
          (function() {
            const scene = window.station3DScene.scene;
            const camera = window.station3DScene.camera;
            const raycaster = new THREE.Raycaster();
            const results = {};

            const interiorTargets = ['hotspot-dining-mess', 'hotspot-medical-bay', 'hotspot-power-plant', 'hotspot-water-lss'];

            ['exterior', 'xray', 'core_only'].forEach(mode => {
              window.set3DMode(mode);
              scene.updateMatrixWorld(true);
              results[mode] = {};

              interiorTargets.forEach(targetName => {
                const target = scene.getObjectByName(targetName);
                const box = new THREE.Box3().setFromObject(target);
                const center = new THREE.Vector3();
                box.getCenter(center);

                const projected = center.clone().project(camera);
                raycaster.setFromCamera(new THREE.Vector2(projected.x, projected.y), camera);

                const interactables = [];
                scene.traverse(o => {
                  if (o.name && o.name.startsWith('hotspot-')) interactables.push(o);
                });
                const hits = raycaster.intersectObjects(interactables, true);

                const hitNames = hits.slice(0, 3).map(h => {
                  let p = h.object;
                  while (p && (!p.name || !p.name.startsWith('hotspot-'))) p = p.parent;
                  return p ? p.name : 'unknown';
                });

                results[mode][targetName] = {
                  projected: [Number(projected.x.toFixed(2)), Number(projected.y.toFixed(2))],
                  firstHit: hitNames[0] || 'none',
                  allHits: hitNames
                };
              });
            });

            return results;
          })()
        `,
        returnByValue: true
      });

      if (res?.exceptionDetails) {
        console.error('EVAL EXCEPTION:', JSON.stringify(res.exceptionDetails, null, 2));
      } else {
        console.log(JSON.stringify(res?.result?.value || res, null, 2));
      }

      ws.close();
      edgeProcess.kill();
      try { fs.rmSync(tempProfileDir, { recursive: true, force: true }); } catch(_) {}
      process.exit(0);
    };
  } catch(e) {
    console.error('Err:', e);
    edgeProcess.kill();
    try { fs.rmSync(tempProfileDir, { recursive: true, force: true }); } catch(_) {}
    process.exit(1);
  }
}, 3000);
