"""
Bharati 3D Digital Twin — Automated Headless E2E Verification Suite.

Validates all 6 Acceptance Criteria (AC1–AC6) defined in the SIH26060 Bharati 3D
Digital Twin specification by running the standalone WebGL test harness inside
headless Microsoft Edge with ANGLE SwiftShader software rendering.
"""

import json
import os
import pathlib
import subprocess
import pytest

VERIFY_SCRIPT_PATH = pathlib.Path(__file__).parent / "verify_3d.js"
HARNESS_PATH = pathlib.Path(__file__).parent / "test_station_3d_harness.html"


@pytest.fixture(scope="module")
def station_3d_results():
    """
    Executes the headless Edge CDP test runner (verify_3d.js --json)
    once for the module and returns the structured verification dictionary.
    """
    assert VERIFY_SCRIPT_PATH.exists(), f"verify_3d.js not found at {VERIFY_SCRIPT_PATH}"
    assert HARNESS_PATH.exists(), f"test_station_3d_harness.html not found at {HARNESS_PATH}"

    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        free_port = s.getsockname()[1]

    # Execute Node.js CDP test runner with --json flag and dynamic ephemeral port
    cmd = ["node", str(VERIFY_SCRIPT_PATH), "--json", f"--port={free_port}", "--timeout=30000"]
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(VERIFY_SCRIPT_PATH.parent.parent.parent),
        timeout=50,
    )

    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()

    assert stdout, f"verify_3d.js produced no stdout. Stderr: {stderr}"

    try:
        data = json.loads(stdout)
    except json.JSONDecodeError as err:
        pytest.fail(
            f"Failed to parse verify_3d.js output as JSON: {err}\nStdout:\n{stdout}\nStderr:\n{stderr}"
        )

    return data


def _get_test(results: dict, test_id: str) -> dict:
    """Helper to locate a specific AC result by its ID."""
    tests = results.get("tests", [])
    match = next((t for t in tests if t.get("id") == test_id), None)
    assert match is not None, f"Test result for {test_id} not found in output: {tests}"
    return match


def test_station_3d_overall_status(station_3d_results):
    """Verifies that all 6 Acceptance Criteria passed overall."""
    passed = station_3d_results.get("passed", False)
    total = station_3d_results.get("total", 0)
    pass_count = station_3d_results.get("passCount", 0)
    fail_count = station_3d_results.get("failCount", 0)

    msg = (
        f"Overall 3D verification status: {pass_count}/{total} passed, {fail_count} failed.\n"
        f"Results payload:\n{json.dumps(station_3d_results, indent=2)}"
    )
    assert passed is True, msg


def test_ac1_hierarchy(station_3d_results):
    """
    AC1: Scene Graph 5-Layer Canonical Hierarchy.
    Verifies that Substructure_Stilts, Exterior_Aerodynamic_Shell,
    Modular_Container_Core, MEP_Life_Support_Overlay, and
    Auxiliary_Site_Infrastructure exist in window.station3DScene.scene.
    """
    test = _get_test(station_3d_results, "AC1_HIERARCHY")
    assert test["passed"] is True, (
        f"AC1 Hierarchy Check Failed:\n{json.dumps(test['details'], indent=2)}"
    )


def test_ac2_hotspots(station_3d_results):
    """
    AC2: 21 Hotspot Registry Names.
    Verifies that all 21 canonical hotspots from HOTSPOT_REGISTRY
    exist in the scene graph with the 'hotspot-' prefix and attach valid geometry.
    """
    test = _get_test(station_3d_results, "AC2_HOTSPOTS")
    assert test["passed"] is True, (
        f"AC2 Hotspots Check Failed:\n{json.dumps(test['details'], indent=2)}"
    )


def test_ac3_xray_mode(station_3d_results):
    """
    AC3: 7-Mode Matrix & X-Ray Material State.
    Verifies that window.set3DMode('xray') renders Modular_Container_Core visible,
    reduces outer skin opacity to <= 0.35, and all 7 modes execute without error.
    """
    test = _get_test(station_3d_results, "AC3_XRAY_MODE")
    assert test["passed"] is True, (
        f"AC3 Modes & X-Ray Check Failed:\n{json.dumps(test['details'], indent=2)}"
    )


def test_ac4_status_update(station_3d_results):
    """
    AC4: Status Bridge Telemetry Recolor.
    Verifies that window.update3DHotspot('power-plant', 'critical') updates the mesh
    emissive color to 0x9B1C1C and base color to 0xC44536, and warning/normal revert properly.
    """
    test = _get_test(station_3d_results, "AC4_UPDATE_HOTSPOT")
    assert test["passed"] is True, (
        f"AC4 Hotspot Status Check Failed:\n{json.dumps(test['details'], indent=2)}"
    )


def test_ac5_pointer_raycast(station_3d_results):
    """
    AC5: Raycast Pointer Click Dispatch.
    Verifies that projecting a 3D hotspot anchor to screen space and dispatching
    a pointerdown event triggers the 'st-3d-click' CustomEvent with the correct asset slug.
    """
    test = _get_test(station_3d_results, "AC5_POINTER_RAYCAST")
    assert test["passed"] is True, (
        f"AC5 Pointer Raycast Check Failed:\n{json.dumps(test['details'], indent=2)}"
    )


def test_ac6_triangle_budget(station_3d_results):
    """
    AC6: Scene Triangle Budget Compliance (<= 20,000).
    Verifies that total triangles in the scene graph do not exceed the
    20,000 budget in exterior mode and geometry budget verification is operational.
    """
    test = _get_test(station_3d_results, "AC6_TRIANGLE_BUDGET")
    assert test["passed"] is True, (
        f"AC6 Triangle Budget Check Failed:\n{json.dumps(test['details'], indent=2)}"
    )
