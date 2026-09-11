# DTFIAS: Project Charter, Overview & System Boundaries

> **Document Status:** Authoritative Project Specification & Scope Charter  
> **Target Path:** `docs/project-overview.md`  
> **Owner Agent:** Documentation Agent / DTFIAS Engineering  
> **Challenge Code:** SIH26060 (Smart India Hackathon 2026)  
> **Last Verified:** September 2026  

---

## 1. Project Identity & Problem Statement

### 1.1 Context & Background
India maintains two active year-round scientific research stations in Antarctica:
- **Maitri** (commissioned 1989, Schirmacher Oasis)
- **Bharati** (commissioned 2012, Larsemann Hills)

Both stations operate under the administrative and scientific coordination of the **National Centre for Polar and Ocean Research (NCPOR)**, Ministry of Earth Sciences, Government of India.

Operating in Antarctica poses extreme challenges:
- Temperatures dropping below -40°C with wind gusts exceeding 250 km/h.
- Extreme isolation for 8 to 9 months during the polar winter with no physical evacuation or resupply possibilities.
- High-latency, bandwidth-constrained, and weather-disrupted satellite communications (SATCOM).
- Critical dependence on diesel Combined Heat and Power (CHP) generators and life-support HVAC systems where subsystem failures constitute immediate life-safety emergencies.

### 1.2 Problem Statement (SIH26060)
Currently, station subsystem data (energy, fuel reserves, HVAC climate control, environmental metrics, and inventory) is monitored through localized disparate SCADA displays and manual status logs. NCPOR Headquarters in Goa lacks a consolidated, real-time, digital-twin-driven command interface capable of:
1. Providing holistic visual situation awareness across all polar assets.
2. Synchronizing station state reliably over intermittent polar SATCOM links.
3. Facilitating safe, audited remote command overrides from HQ during critical incidents.
4. Extensibly supporting future stations (e.g., Maitri-II) without architectural refactoring.

**DTFIAS (Digital Twin for Indian Antarctic Stations)** solves this problem by delivering a robust, low-bandwidth, resilient digital twin platform connecting Antarctic research stations with NCPOR Headquarters.

---

## 2. Project Goals & Objectives

1. **Unified Situation Awareness:** Real-time visual monitoring of station systems via an interactive 2.5D Digital Twin layout, telemetry readouts, and consolidated KPIs.
2. **Polar-Resilient Telemetry:** Server-side push architecture (SSE) paired with local store-and-forward buffering to survive SATCOM outages without data loss.
3. **Safety-Centric Command & Control:** Secure, authenticated, and cryptographically audited command dispatch from HQ to station actuators with dual-validation workflows.
4. **Predictive Life-Support & Energy Management:** Microgrid load balancing, fuel depletion forecasting, and automated anomaly detection across power generation and HVAC systems.
5. **Zero-Friction Deployment:** A bundler-free, lightweight web interface engineered to load smoothly even over constrained Antarctic satellite uplinks.
6. **Multi-Station Extensibility:** Row-based relational station modeling allowing instant onboarding of future bases (such as Maitri-II or temporary summer camps).

---

## 3. Scope & System Boundaries

### 3.1 In-Scope Capabilities
- **Digital Twin 2.5D Visualizations:** Scalable Vector Graphics (SVG) station layouts with dynamic asset hotspots for Bharati and Maitri (`docs/2dFrontend.md`).
- **Telemetry Ingestion & Processing:** High-throughput time-series ingestion for energy microgrids, ambient polar weather, indoor climate HVAC, and asset status.
- **Alert & Anomaly Engine:** Multi-tier threshold evaluation (`P0` Life-Safety Critical, `P1` Operational Warning, `P2` Informational Advisory).
- **HQ Remote Operations:** Centralized monitoring of all stations, remote command dispatch, role-based access management, and immutable audit logs.
- **Station-Level Portals:** Dedicated operational consoles for station commanders, engineers, and scientists at Maitri and Bharati.
- **Resilience Engine:** Store-and-forward write buffer (`in_process_write_buffer.py`) designed to absorb SATCOM network dropouts.

### 3.2 Explicit Non-Goals & Out-of-Scope Items
- **AGEOS Satellite Imagery Ingestion:** The Antarctic Ground Station for Earth Observation Satellites (AGEOS) is operated independently by ISRO/NRSC on dedicated high-speed links. Raw synthetic aperture radar (SAR) and optical payload downloads are **strictly excluded**.
- **Local Hardware SCADA Drivers:** DTFIAS does not write low-level PLC register drivers (e.g. Modbus RTU, BACnet serial). It ingests structured telemetry via standardized async API endpoints and message streams.
- **Public Unauthenticated Portal:** DTFIAS is an institutional defence/scientific operations platform; zero public guest access is permitted.
- **Client-Side Heavy 3D Bundles:** Heavy WebGL 3D scenes requiring megabytes of bundle assets are strictly avoided in standard dashboards; lightweight SVG 2.5D views are the primary UI, with Three.js strictly lazy-loaded on demand (Constraint C16).

---

## 4. Key Terminology & Definitions

| Term | Definition in DTFIAS |
| :--- | :--- |
| **Digital Twin** | A software model of physical Antarctic station infrastructure continuously synchronized with real-time and historical sensor telemetry. |
| **Hotspot** | An interactive SVG element (`hotspot-{asset_id}`) representing a physical building, generator, or asset within the station twin view. |
| **SATCOM** | Satellite Communications (GSAT-7A / Inmarsat / C-band) linking polar stations to the Indian mainland. |
| **Store-and-Forward** | Local disk-backed or in-memory write buffer that accumulates sensor readings during SATCOM dropouts and flushes them to HQ upon link recovery. |
| **P0 Alert** | Life-safety critical emergency (e.g. total generator trip in winter, HVAC failure below freezing inside habitat, toxic gas leak). Requires persistent audio-visual alerting. |
| **P1 Alert** | High-priority operational warning (e.g. fuel reserve below 20%, single generator phase imbalance). Requires operational acknowledgment. |
| **P2 Alert** | Informational advisory (e.g. scheduled filter replacement due, minor telemetry packet jitter). |
| **CHP** | Combined Heat and Power generation, recycling engine jacket/exhaust heat into domestic heating. |
| **v1 Lock** | The canonical 25-table relational PostgreSQL schema defined in `docs/database.md` and `scripts/migrations/001_initial_schema.sql`. |

---

## 5. Architectural Assumptions & Constraints

1. **High Latency & Low Bandwidth:** Network connections from Antarctica have round-trip times of 600–1200 ms and limited bandwidth. Web assets must load without heavy npm bundles (Constraint C17).
2. **Server-Side Realtime:** The browser must never connect directly to cloud database listeners (Constraint C14); all events are fanned out via server-side Server-Sent Events (SSE).
3. **Four-Layer Separation:** The repository strictly enforces clean architectural boundaries: Interface (`app/`), Domain (`engine/`), Implementation (`infrastructure/`), and Vocabulary (`shared/`).
4. **Life-Safety Auditability:** Any action affecting physical station hardware (commands, threshold updates, administrative changes) must be permanently recorded in `audit_logs` (Constraint C7).
