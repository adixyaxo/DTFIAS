# 🤖 2.5D Interactive Station View — Agent Implementation Guide (SIH26060)

## 0. Who this file is for

This file is written to be handed directly to a coding agent (Claude Code, Cursor, Cowork, etc.) as its brief for building the **interactive schematic/2.5D station view** — the "Should-Have" item in `1-project-overview.md` §5 ("Simple schematic/2D layout view showing which subsystem an alert maps to").

The companion file, **`8-station-view-figma-guide.md`**, is for the human/design side of this same feature — producing the actual illustration. This file assumes that artifact exists (or is being produced in parallel) and focuses entirely on the code: parsing the SVG, wiring interactivity, and integrating it into the rest of the app.

**Before starting, read:** `1-project-overview.md` (scope/MVP boundaries), `3-data-transmission-antarctic-to-hq.md` §4–6 (data categories and priority tiers — the status model below is built directly on this), and your team's `architecture.md` if one exists in the repo (referenced throughout the project files but not included in this set — if it's missing, ask the user for it or for the store-and-forward sync design before wiring live data).

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

## 4. Component architecture (Phase B)

- [ ]  Build a station-agnostic `<StationTwin stationId="bharati" />` component — don't hardcode Bharati-specific logic into it.
- [ ]  Inline the SVG (via `import ... ?react` / raw import / equivalent), **not** an `<img>` tag — interactivity requires DOM access to individual elements.
- [ ]  Create `hotspotConfig.ts`: an array mapping each SVG hotspot id → `{ assetId, label, category, dataKey }`.
- [ ]  Build `AssetStatusPanel` — the side panel shown on hotspot click, displaying the asset's current value, status, and last-updated time.
- [ ]  Implement a pure `statusToVisual(status, priority)` function returning a CSS class — keep visual logic out of the SVG and out of the panel component so it's testable in isolation.
- [ ]  Implement a category/layer toggle (Infrastructure / Energy / Environmental / Logistics — matching `3-data-transmission-antarctic-to-hq.md` §4) that filters which hotspots are visible/active, reusing the same underlying SVG.
- [ ]  Wire the component to the app's simulated data feed so it reflects `stale: true` states distinctly (dimmed/greyed hotspot + a small "last updated Xm ago" label), not just live values.

## 5. Data contract (Phase C)

Suggested per-asset schema — adjust field names to match your actual backend/simulation output, but keep the shape:

```json
{
  "asset_id": "power_plant",
  "category": "infrastructure",
  "priority": "P1",
  "status": "warning",
  "value": 742,
  "unit": "kW",
  "last_updated": "2026-08-23T06:24:00Z",
  "stale": false
}
```

- [ ]  Define matching TypeScript types.
- [ ]  Ensure a 1:1 mapping between `asset_id` values and SVG hotspot ids.

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

## 9. Suggested file structure

```
/src
  /components/StationTwin/
    StationTwin.tsx
    AssetStatusPanel.tsx
    hotspotConfig.ts
    statusToVisual.ts
    stationTwin.module.css
  /assets/stations/
    bharati.svg
    maitri.svg
  /types/
    stationAsset.ts
```

---

## 10. Pitfalls specific to this task

- Don't regenerate or redraw the illustration yourself — that's `8-station-view-figma-guide.md`'s job. If the art is missing, wrong, or low-quality, flag it back rather than working around it in code.
- Don't hardcode colors inside the SVG file itself — externalize to CSS variables so a single theme change updates every station view.
- Don't use `<img src="station.svg">` — you lose the ability to target individual elements with JS/CSS.
- Don't build a separate SVG per status combination — one illustration, driven entirely by data.
- Don't add 3D/WebGL "just in case" — it's explicitly de-scoped (`1-project-overview.md` §3, §5 Nice-to-Have).

---

## 11. Open questions to raise with the human team before/while building

- [ ]  Final call: Bharati only for MVP, or Bharati + Maitri from day one?
- [ ]  Does an `architecture.md` already exist with a finalized asset/category taxonomy? If so, this file's asset list (§5) should defer to it.
- [ ]  What's the actual simulated-data update interval, and should the "stale" threshold in the UI match it?
- [ ]  Confirm design tokens/color palette with whoever owns the Figma file in `8-station-view-figma-guide.md`, rather than picking arbitrary status colors independently.

---

## 12. Related files

- `1-project-overview.md` — MVP scope and feature priority
- `3-data-transmission-antarctic-to-hq.md` — data categories, priority tiers, message envelope
- `4-stations-and-headquarters.md` — real subsystem names/facts to ground the asset list
- `8-station-view-figma-guide.md` — companion file: how the illustration itself gets made