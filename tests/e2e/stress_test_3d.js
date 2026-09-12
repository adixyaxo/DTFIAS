#!/usr/bin/env node
/**
 * Bharati 3D Digital Twin — Adversarial Stress Test Suite
 * Empirical Challenger (challenger_1)
 *
 * Executes 4 comprehensive stress testing vectors:
 * 1. Rapid Mode Toggling (100x sequence + 100x random + invalid modes)
 * 2. Hotspot Update Cycling (all 21 hotspots through critical -> warning -> normal -> invalid x 5 iterations)
 * 3. Event Listener Stress (50 simulated pointer clicks across canvas coordinates, verifying CustomEvent details & hover state)
 * 4. Edge Cases (initStation3D with non-existent/null IDs, rapid resize with zero/extreme bounds)
 */

const { spawn, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

const EDGE_CANDIDATE_PATHS = [
  process.env.EDGE_BIN,
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe'
].filter(Boolean);

function resolveEdgePath() {
  for (const candidate of EDGE_CANDIDATE_PATHS) {
    if (fs.existsSync(candidate)) return candidate;
  }
  try {
    const out = execSync('where msedge.exe', { encoding: 'utf8' }).trim();
    const first = out.split(/\r?\n/)[0];
    if (first && fs.existsSync(first)) return first;
  } catch (_) {}
  throw new Error('Microsoft Edge executable not found at standard installation paths.');
}

const net = require('net');

function getFreePort() {
  return new Promise((resolve) => {
    const srv = net.createServer();
    srv.listen(0, () => {
      const port = srv.address().port;
      srv.close(() => resolve(port));
    });
  });
}

const args = process.argv.slice(2);
const jsonOutput = args.includes('--json');
const verbose = args.includes('--verbose');
const portArg = args.find(a => a.startsWith('--port='));
let PORT = portArg ? parseInt(portArg.split('=')[1], 10) : null;
const timeoutArg = args.find(a => a.startsWith('--timeout='));
const TIMEOUT_MS = timeoutArg ? parseInt(timeoutArg.split('=')[1], 10) : 45000;

const HARNESS_PATH = path.resolve(__dirname, 'test_station_3d_harness.html');
if (!fs.existsSync(HARNESS_PATH)) {
  console.error(`[Stress3D] Error: Harness file not found at ${HARNESS_PATH}`);
  process.exit(1);
}

const fileUri = 'file:///' + HARNESS_PATH.replace(/\\/g, '/');
const tempProfileDir = fs.mkdtempSync(path.join(os.tmpdir(), 'edge-3d-stress-'));

function cleanupProfileDir() {
  try {
    fs.rmSync(tempProfileDir, { recursive: true, force: true });
  } catch (_) {}
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
        } catch (e) {
          if (verbose) console.error('[Stress3D CDP] Parse error:', e);
        }
      };
    });
  }

  async send(method, params = {}) {
    const id = this.nextId++;
    const payload = JSON.stringify({ id, method, params });
    if (verbose) console.log(`[Stress3D CDP ->] ${payload}`);
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

async function runStressTests(cdpClient) {
  const result = await cdpClient.evaluate(`
    (async function() {
      const results = {
        passed: true,
        tests: [],
        timestamp: new Date().toISOString()
      };

      function recordTest(id, title, passed, details) {
        if (!passed) results.passed = false;
        results.tests.push({ id, title, passed, details });
      }

      // Helper to wait for station3DScene
      let sceneReady = false;
      for (let i = 0; i < 50; i++) {
        if (window.station3DScene && window.station3DScene.scene) {
          sceneReady = true;
          break;
        }
        await new Promise(r => setTimeout(r, 100));
      }

      if (!sceneReady) {
        recordTest('SCENE_INIT', 'Scene Availability', false, 'window.station3DScene not ready');
        return results;
      }

      const { scene, stationGroup, mepGroup, containerCoreGroup, exteriorShellGroup, hotspotRegistry } = window.station3DScene;

      // ─────────────────────────────────────────────────────────────
      // STRESS TEST 1: Rapid Mode Toggling
      // ─────────────────────────────────────────────────────────────
      try {
        const modes = ['exterior', 'xray', 'core_only', 'hvac', 'thermal', 'structural', 'night'];
        let toggleErrors = 0;
        const initialChildrenCount = scene.children.length;

        // 1A. 100 sequential round-robin switches
        for (let i = 0; i < 100; i++) {
          for (const m of modes) {
            try {
              window.set3DMode(m);
            } catch (err) {
              toggleErrors++;
            }
          }
        }

        // 1B. 100 random switches
        for (let i = 0; i < 100; i++) {
          const randMode = modes[Math.floor(Math.random() * modes.length)];
          try {
            window.set3DMode(randMode);
          } catch (err) {
            toggleErrors++;
          }
        }

        // 1C. Invalid mode inputs
        const invalidModes = ['invalid_mode_xyz', null, undefined, '', 12345, {}, []];
        for (const bad of invalidModes) {
          try {
            window.set3DMode(bad);
          } catch (err) {
            toggleErrors++;
          }
        }

        // 1D. Final state correctness checks
        window.set3DMode('xray');
        let shellMaterial = null;
        exteriorShellGroup?.traverse(child => {
          if (child.isMesh && child.name !== 'flagEmblem' && child.material && !shellMaterial) {
            shellMaterial = child.material;
          }
        });
        const xraySkinOpacity = shellMaterial ? shellMaterial.opacity : null;
        const xrayCoreVisible = containerCoreGroup ? containerCoreGroup.visible : null;

        window.set3DMode('exterior');
        const extSkinOpacity = shellMaterial ? shellMaterial.opacity : null;
        const extCoreVisible = containerCoreGroup ? containerCoreGroup.visible : null;

        const sceneGraphIntact = (scene.children.length === initialChildrenCount) && (scene.children.length > 0);

        const test1Passed = (toggleErrors === 0) &&
                            sceneGraphIntact &&
                            (xraySkinOpacity !== null && xraySkinOpacity <= 0.35) &&
                            (xrayCoreVisible === true) &&
                            (extSkinOpacity === 1.0) &&
                            (extCoreVisible === false);

        recordTest('STRESS_1_RAPID_MODES', 'Rapid Mode Toggling (200+ switches & invalid modes)', test1Passed, {
          totalSwitches: 800 + invalidModes.length,
          toggleErrors,
          initialChildrenCount,
          finalChildrenCount: scene.children.length,
          sceneGraphIntact,
          xraySkinOpacity,
          xrayCoreVisible,
          extSkinOpacity,
          extCoreVisible
        });
      } catch (err) {
        recordTest('STRESS_1_RAPID_MODES', 'Rapid Mode Toggling', false, { exception: err.message, stack: err.stack });
      }

      // ─────────────────────────────────────────────────────────────
      // STRESS TEST 2: Hotspot Update Stress & Type Coercion
      // ─────────────────────────────────────────────────────────────
      try {
        const hotspotKeys = Object.keys(hotspotRegistry || {});
        let updateErrors = 0;
        let colorMismatchCount = 0;
        const nonStringTypeErrorLogs = [];

        // Run 5 cycles across all 21 hotspots: critical -> warning -> normal -> invalid
        for (let cycle = 0; cycle < 5; cycle++) {
          for (const key of hotspotKeys) {
            const assetSlug = key.replace('hotspot-', '');

            // 1. Critical
            window.update3DHotspot(assetSlug, 'critical');
            const targetObj = scene.getObjectByName(key);
            if (targetObj) {
              targetObj.traverse(child => {
                if (child.isMesh && child.material && child.material.color) {
                  if (child.material.color.getHex() !== 0xC44536) colorMismatchCount++;
                  if (child.material.emissive && child.material.emissive.getHex() !== 0x9B1C1C) colorMismatchCount++;
                }
              });
            }

            // 2. Warning
            window.update3DHotspot(key, 'warning'); // also test with 'hotspot-' prefix
            if (targetObj) {
              targetObj.traverse(child => {
                if (child.isMesh && child.material && child.material.color) {
                  if (child.material.color.getHex() !== 0xD9822B) colorMismatchCount++;
                  if (child.material.emissive && child.material.emissive.getHex() !== 0x995511) colorMismatchCount++;
                }
              });
            }

            // 3. Normal
            window.update3DHotspot(assetSlug, 'normal');
            if (targetObj) {
              targetObj.traverse(child => {
                if (child.isMesh && child.material && child.material.color) {
                  const origHex = child.userData._origColor;
                  if (origHex !== null && child.material.color.getHex() !== origHex) colorMismatchCount++;
                }
              });
            }

            // 4. Invalid status string
            window.update3DHotspot(assetSlug, 'invalid_status_xyz');
            // 5. Null / undefined status
            window.update3DHotspot(assetSlug, null);
            window.update3DHotspot(assetSlug, undefined);
          }
        }

        // 2B. Non-string / numeric asset IDs (Adversarial check: does it throw TypeError?)
        const nonStringIds = [99999, 101, { id: 'satcom' }];
        for (const badId of nonStringIds) {
          try {
            window.update3DHotspot(badId, 'critical');
          } catch (err) {
            updateErrors++;
            nonStringTypeErrorLogs.push({ badId: String(badId), type: typeof badId, error: err.message });
          }
        }

        // 2C. Edge string IDs (empty, null, non-existent)
        const edgeAssetIds = ['non_existent_asset', '', 'hotspot-non-existent'];
        for (const badId of edgeAssetIds) {
          try {
            window.update3DHotspot(badId, 'critical');
            window.update3DHotspot(badId, 'normal');
          } catch (err) {
            updateErrors++;
          }
        }

        // 2D. Hover + Telemetry Update Race Condition Test:
        // When a hotspot is hovered, it gets emissive 0x7DBFAD (mint).
        // If update3DHotspot('satcom', 'critical') is called while hovered,
        // does unhovering overwrite the critical color back to origEmissive (0x000000)?
        let hoverRaceClobbered = false;
        const satcomObj = scene.getObjectByName('hotspot-satcom');
        let satcomMesh = null;
        satcomObj?.traverse(c => { if (c.isMesh && c.material && !satcomMesh) satcomMesh = c; });

        if (satcomMesh) {
          // Simulate hover state manually on mesh
          satcomMesh.userData.isHovered = true;
          satcomMesh.userData.origEmissiveHex = 0x000000;
          satcomMesh.userData.origEmissiveIntensity = 0.0;
          satcomMesh.material.emissive.setHex(0x7DBFAD); // Mint

          // Now telemetry arrives with critical status
          window.update3DHotspot('satcom', 'critical');

          // Now unhover happens:
          if (satcomMesh.userData.isHovered) {
            satcomMesh.material.emissive.setHex(satcomMesh.userData.origEmissiveHex || 0x000000);
            satcomMesh.material.emissiveIntensity = satcomMesh.userData.origEmissiveIntensity || 0.0;
            satcomMesh.userData.isHovered = false;
          }

          // Check if critical status was clobbered
          if (satcomMesh.material.emissive.getHex() !== 0x9B1C1C) {
            hoverRaceClobbered = true;
          }
          // Restore satcom to normal
          window.update3DHotspot('satcom', 'normal');
        }

        const test2Passed = (updateErrors === 0) && (colorMismatchCount === 0) && !hoverRaceClobbered;

        recordTest('STRESS_2_HOTSPOT_UPDATES', 'Hotspot Update Stress (21 hotspots x 5 cycles + edge IDs)', test2Passed, {
          hotspotCount: hotspotKeys.length,
          totalCycles: 5,
          colorMismatchCount,
          nonStringTypeErrorCount: nonStringTypeErrorLogs.length,
          nonStringTypeErrorLogs,
          hoverRaceClobbered,
          updateErrors
        });
      } catch (err) {
        recordTest('STRESS_2_HOTSPOT_UPDATES', 'Hotspot Update Stress', false, { exception: err.message, stack: err.stack });
      }

      // ─────────────────────────────────────────────────────────────
      // STRESS TEST 3: Event Listener Stress (50 clicks)
      // ─────────────────────────────────────────────────────────────
      try {
        const camera = window.station3DScene.camera;
        const renderer = window.station3DScene.renderer;
        const canvas = renderer.domElement;
        const rect = canvas.getBoundingClientRect();

        const clicksDispatched = 50;
        let validHitsReceived = 0;
        let emptySpaceFalseHits = 0;
        const eventsCaptured = [];

        const clickListener = (e) => {
          eventsCaptured.push({
            slug: e.detail,
            type: typeof e.detail,
            timestamp: performance.now()
          });
        };
        window.addEventListener('st-3d-click', clickListener);

        // Targeted coordinates: 25 clicks on satcom hotspot
        const satcomTarget = scene.getObjectByName('hotspot-satcom');
        const worldPos = new THREE.Vector3();
        if (satcomTarget) satcomTarget.getWorldPosition(worldPos);
        else worldPos.set(-25, 7.2, 35);

        camera.updateProjectionMatrix();
        renderer.render(scene, camera);
        const satcomScreen = worldPos.clone().project(camera);
        const satcomX = rect.left + ((satcomScreen.x + 1) / 2) * rect.width;
        const satcomY = rect.top + ((-satcomScreen.y + 1) / 2) * rect.height;

        for (let i = 0; i < 25; i++) {
          canvas.dispatchEvent(new PointerEvent('pointerdown', {
            clientX: satcomX + (Math.random() - 0.5) * 4,
            clientY: satcomY + (Math.random() - 0.5) * 4,
            bubbles: true,
            cancelable: true,
            pointerId: 1,
            pointerType: 'mouse'
          }));
        }

        // 15 clicks on empty background coordinates (top corners)
        for (let i = 0; i < 15; i++) {
          canvas.dispatchEvent(new PointerEvent('pointerdown', {
            clientX: rect.left + 5 + Math.random() * 20,
            clientY: rect.top + 5 + Math.random() * 20,
            bubbles: true,
            cancelable: true,
            pointerId: 1,
            pointerType: 'mouse'
          }));
        }

        // 10 rapid clicks across center canvas
        for (let i = 0; i < 10; i++) {
          canvas.dispatchEvent(new PointerEvent('pointerdown', {
            clientX: rect.left + rect.width * 0.5 + (i * 5),
            clientY: rect.top + rect.height * 0.5 + (i * 5),
            bubbles: true,
            cancelable: true,
            pointerId: 1,
            pointerType: 'mouse'
          }));
        }

        // Wait brief delay for event queue
        await new Promise(r => setTimeout(r, 200));
        window.removeEventListener('st-3d-click', clickListener);

        // Verify eventsCaptured
        const satcomHits = eventsCaptured.filter(e => e.slug === 'satcom').length;
        const validSlugs = eventsCaptured.every(e => typeof e.slug === 'string' && !e.slug.startsWith('hotspot-'));

        // Test pointermove hover state restoration
        // Move pointer to satcom, then to empty corner, verify cursor and emissive reset
        canvas.dispatchEvent(new PointerEvent('pointermove', {
          clientX: satcomX,
          clientY: satcomY,
          bubbles: true
        }));
        const cursorDuringHover = canvas.parentElement.style.cursor;

        canvas.dispatchEvent(new PointerEvent('pointermove', {
          clientX: rect.left + 5,
          clientY: rect.top + 5,
          bubbles: true
        }));
        const cursorAfterLeave = canvas.parentElement.style.cursor;

        const test3Passed = (eventsCaptured.length >= 25) &&
                            (satcomHits >= 25) &&
                            validSlugs &&
                            (cursorAfterLeave === 'default');

        recordTest('STRESS_3_EVENT_LISTENERS', 'Event Listener Stress (50 pointer clicks & hover lifecycle)', test3Passed, {
          totalClicksDispatched: clicksDispatched,
          totalEventsCaptured: eventsCaptured.length,
          satcomHits,
          validSlugs,
          cursorDuringHover,
          cursorAfterLeave
        });
      } catch (err) {
        recordTest('STRESS_3_EVENT_LISTENERS', 'Event Listener Stress', false, { exception: err.message, stack: err.stack });
      }

      // ─────────────────────────────────────────────────────────────
      // STRESS TEST 4: Edge Cases (initStation3D bad IDs & rapid resize)
      // ─────────────────────────────────────────────────────────────
      try {
        let initErrors = 0;

        // 4A. Calling initStation3D with non-existent container
        try {
          window.initStation3D('completely-non-existent-container-id-12345');
        } catch (e) {
          initErrors++;
        }

        // 4B. Calling initStation3D with null, undefined, empty string
        try { window.initStation3D(null); } catch (e) { initErrors++; }
        try { window.initStation3D(undefined); } catch (e) { initErrors++; }
        try { window.initStation3D(''); } catch (e) { initErrors++; }

        // 4C. Rapid window resize events
        let resizeErrors = 0;
        const testWidths = [1920, 1280, 800, 375, 2560, 1024, 640];
        const testHeights = [1080, 720, 600, 667, 1440, 768, 480];

        const container = document.getElementById('station-3d-container');
        for (let i = 0; i < 50; i++) {
          const w = testWidths[i % testWidths.length];
          const h = testHeights[i % testHeights.length];
          if (container) {
            container.style.width = w + 'px';
            container.style.height = h + 'px';
          }
          try {
            window.dispatchEvent(new Event('resize'));
          } catch (e) {
            resizeErrors++;
          }
        }

        // Restore container size
        if (container) {
          container.style.width = '100%';
          container.style.height = '100%';
          window.dispatchEvent(new Event('resize'));
        }

        const camera = window.station3DScene.camera;
        const aspectValid = !isNaN(camera.aspect) && isFinite(camera.aspect) && camera.aspect > 0;

        const test4Passed = (initErrors === 0) && (resizeErrors === 0) && aspectValid;

        recordTest('STRESS_4_EDGE_CASES', 'Edge Cases (invalid init IDs, rapid resize cycles)', test4Passed, {
          initErrors,
          resizeEventsFired: 50,
          resizeErrors,
          finalCameraAspect: camera.aspect,
          aspectValid
        });
      } catch (err) {
        recordTest('STRESS_4_EDGE_CASES', 'Edge Cases', false, { exception: err.message, stack: err.stack });
      }

      return results;
    })()
  `);

  return result;
}

async function main() {
  const edgePath = resolveEdgePath();
  if (!PORT) {
    PORT = await getFreePort();
  }
  if (!jsonOutput) {
    console.log('\n════════════════════════════════════════════════════════════════════');
    console.log('  BHARATI 3D DIGITAL TWIN — ADVERSARIAL STRESS TEST RUNNER');
    console.log('════════════════════════════════════════════════════════════════════');
    console.log(`[Stress3D] Edge Binary:       ${edgePath}`);
    console.log(`[Stress3D] Debug Port:        ${PORT}`);
    console.log(`[Stress3D] Harness:           ${fileUri}`);
    console.log(`[Stress3D] Temp User Dir:     ${tempProfileDir}`);
  }

  const edgeArgs = [
    '--headless=new',
    `--remote-debugging-port=${PORT}`,
    '--use-gl=angle',
    '--use-angle=swiftshader',
    '--window-size=1280,720',
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-background-networking',
    '--disable-background-timer-throttling',
    '--disable-client-side-phishing-detection',
    '--disable-default-apps',
    '--disable-extensions',
    '--disable-hang-monitor',
    '--disable-popup-blocking',
    '--disable-prompt-on-repost',
    '--disable-sync',
    '--disable-translate',
    '--metrics-recording-only',
    '--safebrowsing-disable-auto-update',
    '--allow-file-access-from-files',
    `--user-data-dir=${tempProfileDir}`,
    fileUri
  ];

  const edgeProcess = spawn(edgePath, edgeArgs, {
    stdio: ['ignore', 'ignore', 'ignore'],
    detached: false
  });

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

  process.on('SIGINT', () => { killBrowser(); process.exit(1); });
  process.on('SIGTERM', () => { killBrowser(); process.exit(1); });

  try {
    let wsUrl = null;
    const maxRetries = 35;
    for (let i = 0; i < maxRetries; i++) {
      try {
        const resp = await fetch(`http://127.0.0.1:${PORT}/json/list`);
        if (resp.ok) {
          const list = await resp.json();
          if (Array.isArray(list) && list.length > 0) {
            const target = list.find(t => t.type === 'page') || list[0];
            wsUrl = target.webSocketDebuggerUrl;
            if (wsUrl) break;
          }
        }
      } catch (_) {}
      await sleep(250);
    }

    if (!wsUrl) {
      throw new Error(`Failed to connect to Edge CDP on port ${PORT}`);
    }

    if (!jsonOutput) {
      console.log(`[Stress3D] CDP attached: ${wsUrl}`);
      console.log('[Stress3D] Commencing adversarial stress testing execution...');
    }

    cdpClient = new CDPClient(wsUrl);
    await cdpClient.connect();
    await cdpClient.send('Runtime.enable');
    await cdpClient.send('Page.enable');

    // Allow initial scene and base test runner to settle
    await sleep(2000);

    const testResults = await runStressTests(cdpClient);

    if (jsonOutput) {
      console.log(JSON.stringify(testResults, null, 2));
    } else {
      console.log('\n════════════════════════════════════════════════════════════════════');
      console.log(`  STRESS TEST SUMMARY: ${testResults.passed ? 'ALL PASSED' : 'DEFECTS DETECTED'}`);
      console.log(`  Timestamp: ${testResults.timestamp}`);
      console.log('════════════════════════════════════════════════════════════════════\n');

      testResults.tests.forEach(test => {
        const mark = test.passed ? '✔ PASS' : '✖ FAIL';
        const color = test.passed ? '\x1b[32m' : '\x1b[31m';
        const reset = '\x1b[0m';
        console.log(`${color}[${mark}]${reset} [${test.id}] ${test.title}`);
        console.log(`       Details:`, JSON.stringify(test.details, null, 2).replace(/\n/g, '\n       '));
      });
      console.log('\n────────────────────────────────────────────────────────────────────\n');
    }

    killBrowser();
    process.exit(testResults.passed ? 0 : 1);
  } catch (error) {
    killBrowser();
    if (jsonOutput) {
      console.log(JSON.stringify({ error: error.message, passed: false }));
    } else {
      console.error('\n[Stress3D] ✖ FATAL STRESS TEST ERROR:', error.message);
    }
    process.exit(1);
  }
}

main();
