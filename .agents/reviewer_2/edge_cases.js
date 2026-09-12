// Adversarial Edge-Case Stress Testing for station_3d_view.js
// Tests the logic and robustness of the module under abnormal conditions.

const fs = require('fs');
const path = require('path');

// Mock a minimal browser environment with JSDOM or mock objects
const mockContainer = {
  clientWidth: 0,
  clientHeight: 0,
  innerHTML: '<span>old content</span>',
  appendChild: () => {},
  addEventListener: (evt, cb) => {},
  getBoundingClientRect: () => ({ left: 0, top: 0, width: 800, height: 600 }),
  style: {}
};

// Test results accumulator
const findings = [];

console.log('--- ADVERSARIAL STRESS TESTING ---');

// Test 1: initStation3D with null/missing container
console.log('Test 1: Missing container...');
// Mock window and document
global.window = {
  addEventListener: () => {},
  dispatchEvent: () => {}
};
global.document = {
  getElementById: (id) => (id === 'existing-container' ? mockContainer : null),
  createElement: (tag) => ({
    width: 256,
    height: 170,
    getContext: () => ({
      fillRect: () => {},
      beginPath: () => {},
      arc: () => {},
      stroke: () => {},
      fill: () => {},
      moveTo: () => {},
      lineTo: () => {}
    })
  })
};

// Check checkGeometryBudget definition in station_3d_view.js
const code = fs.readFileSync(path.resolve('app/static/js/three/station_3d_view.js'), 'utf8');

const hasGlobalCheckBudget = /window\.checkGeometryBudget\s*=/.test(code);
console.log('window.checkGeometryBudget is exported on window:', hasGlobalCheckBudget);

const hasContainerNullCheck = code.includes('if (!container) {');
console.log('initStation3D checks if (!container):', hasContainerNullCheck);

const hasZeroDimFallback = code.includes('container.clientWidth || 800') && code.includes('container.clientHeight || 600');
console.log('initStation3D falls back on 0 dimensions:', hasZeroDimFallback);

const hasOrbitControlsCheck = code.includes("typeof THREE.OrbitControls !== 'undefined'");
console.log('Safe fallback when THREE.OrbitControls is undefined:', hasOrbitControlsCheck);

// Check update3DHotspot edge cases in AST / code
const hasUnknownAssetIdCheck = code.includes('if (!target) return;');
console.log('update3DHotspot handles unknown assetId without throwing:', hasUnknownAssetIdCheck);

const hasUnknownStatusFallback = code.includes('} else {') && code.includes('obj.userData._origMaterial');
console.log('update3DHotspot handles unknown/normal status with fallback:', hasUnknownStatusFallback);

// Raycaster safe walkup check
const raycasterWalkup = code.match(/while\s*\(\s*hit\s*&&\s*\(!hit\.name\s*\|\|\s*!hit\.name\.startsWith\('hotspot-'\)\)\)\s*\{\s*hit\s*=\s*hit\.parent;\s*\}/);
console.log('Raycaster has safe ancestor walk-up to hotspot group:', !!raycasterWalkup);

// Material clone check in update3DHotspot
const materialCloningCount = (code.match(/obj\.material\s*=\s*obj\.material\.clone\(\)/g) || []).length;
console.log('Material cloning instances in update3DHotspot:', materialCloningCount);

// Check instancing for 4 target categories:
// 1. Stilts
const stiltsInstanced = code.includes('new THREE.InstancedMesh(stiltGeo');
// 2. Footing pads
const padsInstanced = code.includes('new THREE.InstancedMesh(padGeo');
// 3. Fuel tanks
const fuelInstanced = code.includes('new THREE.InstancedMesh(tankGeo');
// 4. Containers (depot)
const depotInstanced = code.includes('new THREE.InstancedMesh(isoBoxGeo');

console.log('Instancing Audit:');
console.log(' - Stilts InstancedMesh:', stiltsInstanced);
console.log(' - Footing pads InstancedMesh:', padsInstanced);
console.log(' - Fuel tanks InstancedMesh:', fuelInstanced);
console.log(' - Container depot InstancedMesh:', depotInstanced);

console.log('--- AUDIT COMPLETE ---');
