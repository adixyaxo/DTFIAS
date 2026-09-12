# DTFIAS — Frontend Design & Domain Inconsistencies (Active Only)

> **Project:** Digital Twin for Indian Antarctic Stations (SIH26060)  
> **Document Authority:** Quality Assurance & Active Inconsistency Tracker  
> **Target Path:** `docs/testing/design_inconsistencies.md`  
> **Master Reference:** [`docs/testing/frontendInconsistency/active-remaining-bugs.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/testing/frontendInconsistency/active-remaining-bugs.md)  
> **Pruning Policy:** All completed/resolved items (INC-02 through INC-06, INC-08, INC-09, INC-11, INC-13, INC-14, Phase 1–4 roadmaps) have been verified against code and deleted. Only active, unresolved inconsistencies remain.

---

## 1. Active Inconsistency Matrix

| ID | Issue Category | Severity | Status | Primary Locations | Core Problem & Resolution |
|:---|:---|:---:|:---:|:---|:---|
| **INC-01** | **Station Domain Contamination** | **P0 (Critical)** | **RESOLVED** | `app/templates/station/twin.html`<br>`app/templates/station/infrastructure.html`<br>`app/templates/components/modals/asset_detail.html` | Parameterized generator hardware (Kirloskar/Cummins for Maitri vs Volvo Penta for Bharati) and added conditional SVG foundation rendering for Maitri bedrock pier footings vs Bharati hydraulic stilts. |
| **INC-10** | **Geographic Coordinates Drift** | **P2 (Medium)** | **RESOLVED** | `index.html`, `topnav.html`, `sidebar_maitri.html`, `hq/telemetry.html` | Standardized all coordinates across views to canonical `shared/constants/stations.py` values: Bharati `69°24'S, 76°11'E`, Maitri `70°46'S, 11°44'E`. |
| **INC-12** | **Personnel Headcount Contradictions** | **P2 (Medium)** | **RESOLVED** | `app/templates/hq/health.html`<br>`app/templates/station/twin.html`<br>`app/templates/hq/users.html` | Aligned all headcount statistics to canonical 42 active winter / 92 summer expedition numbers (24 BHT / 18 MTR) across health, twin, and users views. |
| **INC-15** | **Malformed CSS Syntax in Base Template** | **P2 (Medium)** | **RESOLVED** | `app/templates/layouts/base.html` (L70–85) | Replaced malformed CSS selector with clean, valid `.glass-panel` utility class and hover/active states. |

---

## 2. Active Inconsistency Specifications

### INC-01: Station Domain Contamination in Shared Templates (P0 Critical)
* **Status:** RESOLVED
* **Defect ID Cross-Reference:** `FE-CONTAM-001`
* **Evidence in Code & Fix:**
  - In `app/templates/station/twin.html`: Parameterized generator descriptions, titles, and telemetry labels using `{% if station_id == 'maitri' %}`. Added conditional SVG foundation rendering depicting Maitri's reinforced concrete bedrock pier footings instead of Bharati's hydraulic stilts.
  - In `app/templates/station/infrastructure.html`: Parameterized gen-set cards and subsystem labels to Kirloskar Polar 160/125 for Maitri.
* **Verification:** HTML rendering verified across `/bharati/station-twin`, `/maitri/station-twin`, `/bharati/infrastructure`, and `/maitri/infrastructure`.

---

### INC-10: Geographic Coordinates Drift (P2 Medium)
* **Status:** RESOLVED
* **Defect ID Cross-Reference:** `FE-CONTAM-003`
* **Evidence in Code & Fix:**
  - Standardized coordinates in `components/sidebar_maitri.html` (70°46'S), `hq/telemetry.html` (69°24'S, 76°11'E), `components/topnav.html`, and `station/twin.html` to canonical `shared/constants/stations.py`.
* **Verification:** Confirmed consistent coordinate displays across all station and HQ views.

---

### INC-12: Personnel Headcount Contradictions (P2 Medium)
* **Status:** RESOLVED
* **Defect ID Cross-Reference:** `FE-CONTAM-002`
* **Evidence in Code & Fix:**
  - `hq/health.html`: Updated to display 42 Active Expedition Roster (100% Fit • 24 BHT / 18 MTR).
  - `station/twin.html`: Dynamic crew habitat text renders 18 SOULS for Maitri and 24 SOULS for Bharati.
  - `hq/users.html`: Bound script displays 42 POLAR SOULS (24 BHT / 18 MTR).
* **Verification:** All headcount indicators consistently match canonical values from `shared/constants/stations.py`.

---

### INC-15: Malformed CSS Syntax in Base Template (P2 Medium)
* **Status:** RESOLVED
* **Defect ID Cross-Reference:** `FE-CSS-001`
* **Evidence in Code & Fix:**
  - `app/templates/layouts/base.html` lines 70–85: Replaced broken Tailwind class string selector with clean `.glass-panel` class with backdrop blur and smooth transitions.
* **Verification:** Validated CSS syntax passes without browser parser errors or stylesheet drops.

---

> For the comprehensive list of all remaining active defects across routing, responsive navigation, modals, and endpoints, see **[`docs/testing/frontendInconsistency/active-remaining-bugs.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/testing/frontendInconsistency/active-remaining-bugs.md)**.
