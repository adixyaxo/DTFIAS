# 2.5D Interactive Station View — Agent Implementation Guide (SIH26060)

## 0. Purpose & Authority

This guide defines the engineering specification for building and maintaining the **2.5D interactive digital twin station view** for DTFIAS.
It guides AI coding agents and frontend engineers in parsing SVG schematics, wiring Alpine.js interactivity, displaying real-time telemetry, and integrating with FastAPI.

**Authoritative References:**
- **Structural Architecture:** [`docs/architecture.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/architecture.md)
- **Database & Asset Taxonomy:** [`docs/database.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/database.md) (v1 Lock)
- **Frontend Routes & Endpoints:** [`docs/frontend-endpoints.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/frontend-endpoints.md)
- **Brand Tokens & Status Colors:** [`.agents/brand_design/SKILL.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/.agents/brand_design/SKILL.md)

---

## 1. Project constraints this feature must respect

- [ ]  This is a **SCADA/HMI-style control panel**, not a 3D model — per `1-project-overview.md` §3. Don't add depth, lighting, or camera controls. Flat/isometric SVG only.
- [ ]  MVP station is **Bharati** (better-documented, more compact) per `1-project-overview.md` §5. Build the component to be station-agnostic from the start so Maitri is a config change, not a rewrite.
- [ ]  Data is simulated, not live — the twin must visibly represent **staleness/last-updated state**, not just current value. This is the project's actual technical differentiator (see `3-data-transmission-antarctic-to-hq.md` §6), so don't skip it to save time.
- [ ]  Every hotspot's status should map to one of the project's **priority tiers** (P0 critical / P1 operational / P2 bulk) — a P0 alert on a hotspot should look and behave differently (persistent, harder to dismiss, resent-until-acked) from a routine P1 status change.

---

## 2. Inputs to check for before starting

- [ ]  Confirm the SVG file exists at the agreed path (e.g. `/assets/stations/bharati.svg`) — don't assume; check the filesystem first.
- [ ]  Confirm each interactive region in the SVG has a stable id (see naming convention in `8-station-view-figma-guide.md` §4) — `hotspot-{asset-slug}`, kebab-case.
- [ ]  If ids are missing, malformed, or the file doesn't exist yet: stop and flag it rather than fabricating placeholder art yourself — the illustration is the human track's deliverable, not this one.
- [ ]  Get or define the list of asset ids expected for this station (see §5 for a starting list grounded in real Bharati/Maitri subsystems).

---

## 3. SVG audit & cleanup (Phase A)

- [ ]  Parse the SVG DOM and list every `<g>`/`<path>`/`<rect>` id present.
- [ ]  Verify each intended hotspot has a unique, stable id matching the `hotspot-*` convention — flag any mismatch back to the human track instead of silently renaming (renaming breaks the handoff doc).
- [ ]  Run the file through SVGO (or equivalent) to strip Figma export cruft, flatten redundant groups, and cut embedded raster bloat.
- [ ]  Add `<title>` elements inside each hotspot group for screen-reader accessibility.
- [ ]  Replace hardcoded fill/stroke colors with CSS custom properties (`var(--status-ok)`, etc.) so status-driven recoloring works without touching the SVG file again later.
- [ ]  Confirm `viewBox` is set (not fixed `width`/`height`) so the illustration scales responsively.

## 4. Component Architecture (FastAPI + Jinja2 + Alpine.js)

- **Station-Agnostic Layout**: Implement a parameterized template (`app/templates/station/twin.html` or `app/templates/bharati/station_twin.html`) driven by station route parameters (`/{station_id}/twin`).
- **Inline SVG Only**: Embed the SVG directly within the template (`{% include ... %}` or inline markup), **never** as an `<img>` tag — interactivity and CSS variable inheritance require DOM access to individual elements.
- **Client Runtime (`app/static/js/station_twin.js`)**: An Alpine.js component (`x-data="stationTwin()"`) manages hotspot bindings, hover highlights, and active selection state.
- **Asset Status Panel (`app/templates/components/asset_drawer.html`)**: The flyout drawer shown on hotspot click, displaying the asset's current value, operational status, threshold range, and freshness timestamp.
- **Layer Filters**: Implement category toggles (`Infrastructure`, `Energy`, `Environmental`, `Logistics`) to filter active hotspots without page reload.
- **Data Freshness / Staleness**: Reflect `stale: true` states distinctly (dimmed/desaturated hotspot + "last updated Xm ago" badge).

## 5. Data Contract

Per-asset telemetry schema delivered to the twin:

```json
{
  "asset_id": "power_plant",
  "name": "CHP Generator #01",
  "category": "energy",
  "priority": "P1",
  "status": "warning",
  "value": 282.4,
  "unit": "kW",
  "capacity_kw": 340.0,
  "last_updated": "2026-09-07T14:30:00Z",
  "stale": false
}
```

- Ensure a 1:1 mapping between `asset_id` values and SVG hotspot IDs (`hotspot-{asset_id}`).

**Starting asset list** (grounded in real, documented subsystems from `3-` and `4-` — extend as your simulation grows, don't invent unrelated ones for the MVP demo):

| asset_id | Real-world basis | Category | Source |
| --- | --- | --- | --- |
| `main_building` | Core habitable/lab structure | infrastructure | `4-stations-and-headquarters.md` |
| `power_plant` | Diesel generation (Bharati/Maitri) | energy | `4-stations-and-headquarters.md` §1 |
| `fuel_storage` | ~3 lakh litre automated fuel farm at Bharati | energy | `3-data-transmission-antarctic-to-hq.md` §4.3 |
| `hvac` | Heating/life-support | infrastructure | `3-data-transmission-antarctic-to-hq.md` §4.1 |
| `comms_satcom` | SATCOM/C-band ops link (not AGEOS) | infrastructure | `3-data-transmission-antarctic-to-hq.md` §1–2 |
| `medical_bay` | Personnel welfare | personnel | `4-stations-and-headquarters.md` |
| `personnel_roster` | Headcount/rotation status | personnel | `3-data-transmission-antarctic-to-hq.md` §4.3 |
| `environment_sensors` | Temp/wind/pressure/visibility | environmental | `3-data-transmission-antarctic-to-hq.md` §4.2 |
| `heliport` (Bharati only) | Aerial logistics | logistics | `4-stations-and-headquarters.md` §4 |
| `vehicle_fleet` | Resupply/ground transport | logistics | `3-data-transmission-antarctic-to-hq.md` §4.3 |

Deliberately **not** included: AGEOS/the X-S band earth station — it's ISRO infrastructure on a separate pipe and explicitly out of scope for this twin (see `3-data-transmission-antarctic-to-hq.md` §1).

## 6. Interactivity polish (Phase D)

- [ ]  Keyboard navigation: tab through hotspots, Enter/Space opens the panel.
- [ ]  Touch targets ≥44px for mobile; tap replaces hover for opening the panel on touch devices.
- [ ]  Animate with CSS transforms/opacity only (cheap, no layout thrash) — pulse for critical/P0, static color change for warning/P1, no animation for normal.
- [ ]  Confirm the layout re-scales correctly at your minimum supported viewport width without hotspots drifting off their targets (this is the specific failure mode of the PNG+absolute-position approach — inline SVG with relative coordinates avoids it).

## 7. Integration into the wider app (Phase E)

- [ ]  Build a station-selector screen (list/cards of stations with headline stats) that routes into `<StationTwin>` — needed regardless of whether you ship one station or two for the MVP.
- [ ]  Wire the layer toggle to the same four data categories used elsewhere in the app so this view stays consistent with the rest of the dashboard, not a separate visual language.
- [ ]  Hook up at least one **remote action** through a hotspot (acknowledge alert / adjust threshold / trigger a logged command) — this satisfies the MVP requirement in `1-project-overview.md` §5 that the dashboard isn't read-only.
- [ ]  Hook up a demo control (e.g. a hidden "simulate power dip" trigger) so the disaster scenario can be shown live by injecting a fault into the mock data stream and watching the corresponding hotspot update in real time during judging.

## 8. Acceptance checklist (Phase F)

- [ ]  Every hotspot is clickable and keyboard-reachable.
- [ ]  A status change in mock data visibly updates the correct hotspot without a full re-render/flash.
- [ ]  Layout holds at your team's minimum supported width.
- [ ]  A missing/unexpected SVG id logs a warning and degrades gracefully — it does not crash the view.
- [ ]  Color choices for status states pass a basic contrast check (don't rely on color alone — pair with icon/shape per accessibility best practice, since some judges/users may be color-blind).

---

## 9. File Structure in DTFIAS

```
DTFIAS/
├── app/
│   ├── routers/
│   │   ├── bharati/router.py          # GET /bharati/twin and /bharati/station-twin
│   │   └── maitri/router.py           # GET /maitri/twin and /maitri/station-twin
│   ├── static/
│   │   ├── js/
│   │   │   └── station_twin.js        # Alpine.js component and SVG hotspot binders
│   │   └── img/stations/
│   │       ├── bharati_isometric.svg  # Master vector illustration
│   │       └── maitri_isometric.svg
│   └── templates/
│       ├── components/
│       │   └── asset_drawer.html      # Flyout panel for selected asset telemetry
│       └── station/
│           └── twin.html              # Parameterized 2.5D station twin view
```

---

## 10. Implementation Pitfalls to Avoid

- Don't hardcode colors inside the SVG file itself — externalize to CSS variables (`var(--status-ok)`, `var(--status-warning)`, `var(--status-critical)`) so theme changes propagate instantly.
- Don't use `<img src="station.svg">` — you lose the ability to target individual elements with JS/CSS.
- Don't build separate SVG files per status combination — one master illustration, driven dynamically by telemetry data.
- Don't add Three.js/WebGL to the 2.5D view — 3D view is an optional lazy-loaded module (`station_3d_view.js` under `x-init`, C16), whereas the 2.5D twin is the primary zero-dependency SCADA interface.

---

## 11. Authoritative Related Documentation

- [`docs/architecture.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/architecture.md) — Four-layer architecture, constraints C1–C17, portal segregation
- [`docs/database.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/database.md) — Asset hierarchy, sensor configurations, and telemetry retention
- [`docs/frontend-endpoints.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/frontend-endpoints.md) — UI layout, component inventory, route mapping
- [`.agents/brand_design/SKILL.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/.agents/brand_design/SKILL.md) — Official color palette, status tokens, typography standards