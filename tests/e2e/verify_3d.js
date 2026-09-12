#!/usr/bin/env node
/**
 * Bharati 3D Digital Twin — Automated Headless E2E Verification Runner
 * Connects directly to Microsoft Edge Chromium via Chrome DevTools Protocol (CDP).
 * Zero external npm dependencies (uses native fetch & WebSocket in Node 20+).
 */

const { spawn, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

// Standard candidate paths for Microsoft Edge on Windows
const EDGE_CANDIDATE_PATHS = [
  process.env.EDGE_BIN,
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe'
].filter(Boolean);

function resolveEdgePath() {
  for (const candidate of EDGE_CANDIDATE_PATHS) {
    if (fs.existsSync(candidate)) {
      return candidate;
    }
  }
  // Try finding via 'where' on Windows
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

// Parse command line arguments
const args = process.argv.slice(2);
const jsonOutput = args.includes('--json');
const verbose = args.includes('--verbose');
const portArg = args.find(a => a.startsWith('--port='));
let PORT = portArg ? parseInt(portArg.split('=')[1], 10) : null;
const timeoutArg = args.find(a => a.startsWith('--timeout='));
const TIMEOUT_MS = timeoutArg ? parseInt(timeoutArg.split('=')[1], 10) : 25000;

const HARNESS_PATH = path.resolve(__dirname, 'test_station_3d_harness.html');
if (!fs.existsSync(HARNESS_PATH)) {
  console.error(`[Verify3D] Error: Harness file not found at ${HARNESS_PATH}`);
  process.exit(1);
}

// Form file:// URI
const fileUri = 'file:///' + HARNESS_PATH.replace(/\\/g, '/');

// Create dedicated temporary profile directory to prevent port locking with existing browser sessions
const tempProfileDir = fs.mkdtempSync(path.join(os.tmpdir(), 'edge-3d-verify-'));

function cleanupProfileDir() {
  try {
    fs.rmSync(tempProfileDir, { recursive: true, force: true });
  } catch (_) {}
}

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Simple CDP Client implementation using native WebSocket & fetch
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
          if (verbose) console.error('[Verify3D CDP] Error parsing message:', e);
        }
      };
    });
  }

  async send(method, params = {}) {
    const id = this.nextId++;
    const payload = JSON.stringify({ id, method, params });
    if (verbose) console.log(`[Verify3D CDP ->] ${payload}`);
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

async function main() {
  const edgePath = resolveEdgePath();
  if (!PORT) {
    PORT = await getFreePort();
  }
  if (!jsonOutput) {
    console.log('\n════════════════════════════════════════════════════════════════════');
    console.log('  BHARATI 3D DIGITAL TWIN — HEADLESS E2E VERIFICATION RUNNER');
    console.log('════════════════════════════════════════════════════════════════════');
    console.log(`[Verify3D] Using Edge binary: ${edgePath}`);
    console.log(`[Verify3D] Debugging Port:    ${PORT}`);
    console.log(`[Verify3D] Harness URI:       ${fileUri}`);
    console.log(`[Verify3D] Temp User Dir:     ${tempProfileDir}`);
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

  const killBrowser = async () => {
    try {
      if (cdpClient) {
        await cdpClient.send('Browser.close');
        cdpClient.close();
      }
    } catch (_) {}
    await new Promise(r => setTimeout(r, 300));
    try {
      if (edgeProcess && edgeProcess.exitCode === null) {
        edgeProcess.kill();
      }
    } catch (_) {}
    cleanupProfileDir();
  };

  process.on('SIGINT', async () => { await killBrowser(); process.exit(1); });
  process.on('SIGTERM', async () => { await killBrowser(); process.exit(1); });

  try {
    // 1. Wait for Edge DevTools port to open
    let wsUrl = null;
    const maxRetries = 35;
    for (let i = 0; i < maxRetries; i++) {
      try {
        const resp = await fetch(`http://127.0.0.1:${PORT}/json/list`);
        if (resp.ok) {
          const list = await resp.json();
          if (Array.isArray(list) && list.length > 0) {
            // Find target matching our harness or take first page
            const target = list.find(t => t.type === 'page') || list[0];
            wsUrl = target.webSocketDebuggerUrl;
            if (wsUrl) break;
          }
        }
      } catch (_) {
        // Port not ready yet
      }
      await sleep(250);
    }

    if (!wsUrl) {
      throw new Error(`Failed to establish CDP connection to Edge on port ${PORT} within timeout.`);
    }

    if (!jsonOutput) {
      console.log(`[Verify3D] CDP attached: ${wsUrl}`);
      console.log('[Verify3D] Awaiting 3D initialization and automated test execution...');
    }

    // 2. Connect via WebSocket CDP
    cdpClient = new CDPClient(wsUrl);
    await cdpClient.connect();
    await cdpClient.send('Runtime.enable');
    await cdpClient.send('Page.enable');

    // 3. Poll for window.__TEST_RESULTS__
    const startTime = Date.now();
    let testResults = null;

    while (Date.now() - startTime < TIMEOUT_MS) {
      try {
        const val = await cdpClient.evaluate('window.__TEST_RESULTS__');
        if (val && typeof val === 'object' && Array.isArray(val.tests) && val.tests.length >= 6) {
          testResults = val;
          break;
        }
      } catch (e) {
        if (verbose) console.log('[Verify3D] Polling evaluate note:', e.message);
      }
      await sleep(300);
    }

    if (!testResults) {
      // Dump console / DOM snippet if timed out
      const dom = await cdpClient.evaluate('document.body.innerText');
      throw new Error(`Timed out after ${TIMEOUT_MS}ms waiting for window.__TEST_RESULTS__.\nPage text snapshot:\n${dom}`);
    }

    // 4. Output Results
    if (jsonOutput) {
      // Clean JSON stream for machine consumption
      console.log(JSON.stringify(testResults, null, 2));
    } else {
      console.log('\n════════════════════════════════════════════════════════════════════');
      console.log(`  VERIFICATION RESULT: ${testResults.passed ? 'PASSED' : 'FAILED'}`);
      console.log(`  Tests: ${testResults.total} | Passed: ${testResults.passCount} | Failed: ${testResults.failCount}`);
      console.log(`  Timestamp: ${testResults.timestamp}`);
      console.log('════════════════════════════════════════════════════════════════════\n');

      testResults.tests.forEach((test, idx) => {
        const mark = test.passed ? '✔ PASS' : '✖ FAIL';
        const color = test.passed ? '\x1b[32m' : '\x1b[31m';
        const reset = '\x1b[0m';
        console.log(`${color}[${mark}]${reset} [${test.id}] ${test.title}`);
        if (!test.passed) {
          console.log(`       Details:`, JSON.stringify(test.details, null, 2).replace(/\n/g, '\n       '));
        }
      });
      console.log('\n────────────────────────────────────────────────────────────────────\n');
    }

    await killBrowser();
    process.exit(testResults.passed ? 0 : 1);
  } catch (error) {
    await killBrowser();
    if (jsonOutput) {
      console.log(JSON.stringify({ error: error.message, passed: false }));
    } else {
      console.error('\n[Verify3D] ✖ FATAL VERIFICATION ERROR:', error.message);
    }
    process.exit(1);
  }
}

main();
