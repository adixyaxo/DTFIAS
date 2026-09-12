# Handoff Report — Adversarial Stress Testing & Empirical Verification of Bharati 3D Module

**Agent**: `challenger_1` (Empirical Challenger: critic, specialist)  
**Milestone**: Bharati 3D Digital Twin Adversarial Stress Testing  
**Status**: `REQUEST_CHANGES` (Defects Identified)  
**Timestamp**: 2026-09-12T05:29:30Z  

---

## 1. Observation

### 1.1 Baseline E2E Suite Results
- **Command**: `node tests/e2e/verify_3d.js`
  - **Result**: PASSED (6/6 tests passed in ~6.0s)
  - **Output**:
    ```
    [✔ PASS] [AC1_HIERARCHY] Scene Graph 5-Layer Canonical Hierarchy
    [✔ PASS] [AC2_HOTSPOTS] 21 Hotspot Registry Names Present in Scene
    [✔ PASS] [AC3_XRAY_MODE] 7-Mode Matrix & X-Ray Material State
    [✔ PASS] [AC4_UPDATE_HOTSPOT] Hotspot Status Emissive & Color Update
    [✔ PASS] [AC5_POINTER_RAYCAST] Raycast Pointer Click Dispatch (st-3d-click)
    [✔ PASS] [AC6_TRIANGLE_BUDGET] Scene Triangle Budget Compliance (<= 20,000)
    ```
- **Command**: `pytest tests/e2e/test_station_3d_verification.py`
  - **Result**: PASSED (7 passed in 5.36s)

### 1.2 Adversarial Stress Suite Results
- **Tool Command**: `node tests/e2e/stress_test_3d.js`
- **Output**:
  ```
  ════════════════════════════════════════════════════════════════════
    BHARATI 3D DIGITAL TWIN — ADVERSARIAL STRESS TEST RUNNER
  ════════════════════════════════════════════════════════════════════
  [✔ PASS] [STRESS_1_RAPID_MODES] Rapid Mode Toggling (200+ switches & invalid modes)
         Details: {
           "totalSwitches": 807,
           "toggleErrors": 0,
           "initialChildrenCount": 8,
           "finalChildrenCount": 8,
           "sceneGraphIntact": true,
           "xraySkinOpacity": 0.25,
           "xrayCoreVisible": true,
           "extSkinOpacity": 1,
           "extCoreVisible": false
         }
  [✖ FAIL] [STRESS_2_HOTSPOT_UPDATES] Hotspot Update Stress (21 hotspots x 5 cycles + edge IDs)
         Details: {
           "hotspotCount": 21,
           "totalCycles": 5,
           "colorMismatchCount": 0,
           "nonStringTypeErrorCount": 3,
           "nonStringTypeErrorLogs": [
             {
               "badId": "99999",
               "type": "number",
               "error": "assetId.startsWith is not a function"
             },
             {
               "badId": "101",
               "type": "number",
               "error": "assetId.startsWith is not a function"
             },
             {
               "badId": "[object Object]",
               "type": "object",
               "error": "assetId.startsWith is not a function"
             }
           ],
           "hoverRaceClobbered": true,
           "updateErrors": 3
         }
  [✔ PASS] [STRESS_3_EVENT_LISTENERS] Event Listener Stress (50 pointer clicks & hover lifecycle)
         Details: {
           "totalClicksDispatched": 50,
           "totalEventsCaptured": 31,
           "satcomHits": 25,
           "validSlugs": true,
           "cursorDuringHover": "pointer",
           "cursorAfterLeave": "default"
         }
  [✔ PASS] [STRESS_4_EDGE_CASES] Edge Cases (invalid init IDs, rapid resize cycles)
         Details: {
           "initErrors": 0,
           "resizeEventsFired": 50,
           "resizeErrors": 0,
           "finalCameraAspect": 1.2356687898089171,
           "aspectValid": true
         }
  ```

### 1.3 Code Inspection of Defects in `app/static/js/three/station_3d_view.js`

#### Defect A: Uncaught TypeError on Non-String Asset ID
- **File**: `app/static/js/three/station_3d_view.js`, lines 1154-1158:
  ```javascript
  1154: window.update3DHotspot = function(assetId, status) {
  1155:   if (!assetId) return;
  1156:   const lookupName = assetId.startsWith('hotspot-') ? assetId : 'hotspot-' + assetId;
  1157:   const target = scene.getObjectByName(lookupName);
  1158:   if (!target) return;
  ```
  - **Verbatim Error**: `TypeError: assetId.startsWith is not a function`
  - **Reproduction**: Calling `window.update3DHotspot(12345, 'critical')` or passing numeric asset primary keys from telemetry JSON payloads crashes callers.

#### Defect B: Race Condition between Hover Highlight and Telemetry Status Recolor
- **File**: `app/static/js/three/station_3d_view.js`, lines 1093-1124 and lines 1163-1193:
  - When pointer hovers over a hotspot (lines 1115-1118):
    ```javascript
    child.userData.origEmissiveHex = child.material.emissive.getHex(); // e.g. 0x000000
    child.userData.origEmissiveIntensity = child.material.emissiveIntensity;
    child.userData.isHovered = true;
    child.material.emissive.setHex(0x7DBFAD); // brand mint hover highlight
    ```
  - While hovered, if a telemetry update arrives via `window.update3DHotspot(assetId, 'critical')` (lines 1171-1175):
    ```javascript
    obj.material = obj.material.clone();
    obj.material.emissive.setHex(0x9B1C1C); // red critical
    ```
  - When the user's mouse moves away (unhover, lines 1099-1104):
    ```javascript
    child.material.emissive.setHex(child.userData.origEmissiveHex || 0x000000);
    child.material.emissiveIntensity = child.userData.origEmissiveIntensity !== undefined
      ? child.userData.origEmissiveIntensity
      : 0.0;
    child.userData.isHovered = false;
    ```
  - **Result**: The unhover handler blindly resets the mesh emissive back to `origEmissiveHex` (which was `0x000000` captured before the alert arrived), completely wiping out the critical alert visual styling from the 3D scene!

---

## 2. Logic Chain

1. **Step 1 (Baseline Verification)**:
   - Observation 1.1 shows that all 6 core Acceptance Criteria (`AC1_HIERARCHY`, `AC2_HOTSPOTS`, `AC3_XRAY_MODE`, `AC4_UPDATE_HOTSPOT`, `AC5_POINTER_RAYCAST`, `AC6_TRIANGLE_BUDGET`) successfully pass under both `node verify_3d.js` and `pytest test_station_3d_verification.py`.
   - The scene graph hierarchy, 21 hotspots, 7 rendering modes, raycast click dispatch, and triangle budget (<= 20,000) are all fundamentally sound under nominal conditions.

2. **Step 2 (Rapid Mode Toggling Stress)**:
   - Observation 1.2 (`STRESS_1_RAPID_MODES`) executed 807 mode switches (100 sequential round-robin across 7 modes, 100 random, and 7 invalid mode types).
   - Zero exceptions occurred (`toggleErrors: 0`), `scene.children.length` remained exactly 8, `xraySkinOpacity` was 0.25 (<= 0.35 limit), and final state transitions restored cleanly.
   - The SCADA mode state machine is resilient against rapid UI clicking and invalid mode arguments.

3. **Step 3 (Hotspot Update Stress & Type Coercion)**:
   - Observation 1.2 & 1.3 (`STRESS_2_HOTSPOT_UPDATES`) tested 5 cycles of 21 hotspots (105 updates per state). Valid string slugs update color and emissive properties with 0 mismatches.
   - However, when non-string IDs (e.g. integer asset IDs `99999` or `{id: 'satcom'}`) are passed, line 1156 unconditionally invokes `assetId.startsWith()`. Since `Number.prototype` does not implement `startsWith`, an uncaught `TypeError` is thrown.
   - Observation 1.3 demonstrates that the hover handler and telemetry update bridge maintain independent, unsynchronized caches of `origEmissiveHex`. When an alert arrives while an asset is hovered, unhovering clobbers the active critical alert emissive back to `0x000000`. In a mission-critical Antarctic station SCADA twin, an operator moving their mouse over an asset must not erase emergency alert highlights.

4. **Step 4 (Event Listener & Edge Case Stress)**:
   - Observation 1.2 (`STRESS_3_EVENT_LISTENERS` and `STRESS_4_EDGE_CASES`) proved that 50 pointer clicks across coordinates accurately emit `st-3d-click` with clean asset slugs (25/25 on satcom, 0 false triggers on empty canvas corners), pointer cursors revert cleanly to default, calling `initStation3D` with non-existent or null IDs logs gracefully without unhandled exceptions, and 50 rapid resize events do not corrupt the camera aspect ratio or WebGL viewport.

5. **Step 5 (Conclusion Derivation)**:
   - Because Defects A and B represent real runtime failure modes in the public telemetry bridge `window.update3DHotspot`, the 3D module cannot be approved without surgical fixes. The verdict is `REQUEST_CHANGES`.

---

## 3. Caveats

- **WebGL Hardware Acceleration**: All headless tests were executed using ANGLE SwiftShader software rendering inside headless Microsoft Edge. Physical GPU hardware driver edge cases (e.g. driver crashes on mobile WebGL) were not tested directly.
- **Continuous Multi-Hour Run**: Tests ran for up to ~1,000 animation frames. Prolonged continuous multi-day execution memory leaks (e.g. browser tab open for 72 hours) were not profiled.
- No other caveats.

---

## 4. Conclusion & Required Changes

**Verdict**: `REQUEST_CHANGES`

### Required Fix in `app/static/js/three/station_3d_view.js`

1. **Fix Defect A (Type Coercion for Asset IDs)**:
   In `window.update3DHotspot` (line 1154):
   ```javascript
   window.update3DHotspot = function(assetId, status) {
     if (!assetId) return;
     const strId = String(assetId);
     const lookupName = strId.startsWith('hotspot-') ? strId : 'hotspot-' + strId;
     const target = scene.getObjectByName(lookupName);
     if (!target) return;
   ```

2. **Fix Defect B (Synchronize Hover Cache with Telemetry Updates)**:
   In `window.update3DHotspot` (around line 1170):
   When setting status to `'critical'`, `'warning'`, or `'normal'`, update `obj.userData.origEmissiveHex` and `obj.userData.origEmissiveIntensity` so that if `obj.userData.isHovered` is true, unhovering restores to the active status emissive instead of wiping it out:
   ```javascript
   const targetEmissiveHex = (status === 'critical') ? 0x9B1C1C : ((status === 'warning') ? 0x995511 : (obj.userData._origEmissive || 0x000000));
   const targetEmissiveIntensity = (status === 'critical') ? 0.8 : ((status === 'warning') ? 0.6 : (obj.userData._origEmissiveIntensity || 0.0));

   if (obj.userData.isHovered) {
     obj.userData.origEmissiveHex = targetEmissiveHex;
     obj.userData.origEmissiveIntensity = targetEmissiveIntensity;
   }
   ```

---

## 5. Verification Method

To independently reproduce the findings and verify the fixes:

1. **Run Base E2E Suite**:
   ```bash
   node tests/e2e/verify_3d.js
   pytest tests/e2e/test_station_3d_verification.py
   ```
   *Expected*: All 6/6 and 7/7 AC tests pass.

2. **Run Adversarial Stress Test Suite**:
   ```bash
   node tests/e2e/stress_test_3d.js
   ```
   *Current Observation*:
   - `STRESS_1_RAPID_MODES`: PASS
   - `STRESS_2_HOTSPOT_UPDATES`: FAIL (`nonStringTypeErrorCount: 3`, `hoverRaceClobbered: true`)
   - `STRESS_3_EVENT_LISTENERS`: PASS
   - `STRESS_4_EDGE_CASES`: PASS

3. **Post-Fix Invalidation Condition**:
   After applying the two surgical fixes above to `station_3d_view.js`, re-run:
   ```bash
   node tests/e2e/stress_test_3d.js
   ```
   *Expected Post-Fix*: `STRESS TEST SUMMARY: ALL PASSED` (4/4 PASS, exit code 0).
