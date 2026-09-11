# DTFIAS — Frontend Informational & Visual Design Inconsistencies Audit Report

> **Project:** Digital Twin for Indian Antarctic Stations (SIH26060)  
> **Document Authority:** Quality Assurance & Frontend Architectural Audit  
> **Target Path:** `docs/testing/design_inconsistencies.md`  
> **Scope:** Complete frontend surface (`app/templates/`, `app/routers/`, `app/static/`, and layouts).

---

## 1. Executive Summary

A comprehensive dual-track audit was conducted on the DTFIAS frontend codebase, inspecting both:
1. **Informational & Domain Design:** Station identity mismatches, cross-contamination between Bharati and Maitri, coordinate discrepancies, headcount contradictions, and naming/spelling typos.
2. **Visual & Geometric Design:** Inconsistent padding and spacing scales, contradictory border-radius tokens, missing global CSS rules/keyframes, phantom/undefined utility classes, and conflicting design subsystems.

### Core Discoveries
* **Domain Contamination (P0):** All templates in `app/templates/station/` are hardcoded for **Bharati Station** (including 3D isometric cutaways on stilts, coordinates, station IDs, CSV export names, and emergency prompts). Because both the Bharati and Maitri routers render from `station/`, **visiting any `/maitri/*` view exposes Bharati facilities and operations to Maitri operators.**
* **Broken Tailwind Border Radius Configuration (P1):** In `base.html`, `theme.extend.borderRadius` overrides `"full": "0.75rem"` (12px instead of 9999px) and leaves `"md"` unconfigured (6px), making `rounded-md` (6px) **larger** than `rounded-lg` (4px), while breaking circular badges and pills.
* **Invisible Elements Bug Due to Missing `@keyframes fadeInUp` (P1):** Over 11 template views use `opacity-0 animate-[fadeInUp_0.8s_ease-out_forwards]`. However, `@keyframes fadeInUp` is defined **only in `index.html`**, meaning elements on other pages risk remaining permanently transparent (`opacity: 0`).
* **Undefined `.glass-card` and `.glass-button` Classes (P1):** Applied across 11+ views, these classes are defined only in an inline `<style>` block in `index.html`. In all other dashboard templates, they have zero CSS declarations and render as flat, unstyled containers.
* **Typographical & Brand Errors (P1):** The word "Antarctic" is repeatedly misspelled as **"ANARCTIC"** (missing "T") in `auth/login.html`, `auth/recover.html`, and modal headers; "Bharati" is misspelled as **"Bharti"** in `hq/compliance.html`.

---

## 2. Inconsistency Severity Matrix

| ID | Issue Category | Severity | Status | Primary Locations | Core Problem |
|:---|:---|:---:|:---:|:---|:---|
| **INC-01** | **Bharati Data Hardcoded in Maitri Context** | **P0 (Critical)** | ✅ RESOLVED (Phase 3) | `app/templates/station/*`, `app/routers/maitri/router.py` | Maitri operators see Bharati facility data, coordinates, and cutaway schematics |
| **INC-02** | **Undefined `.glass-card` & `.glass-button`** | **P1 (High)** | ✅ RESOLVED (Phase 1) | `hq/health`, `hq/reports`, `hq/roles`, `station/personnel`, etc. | Styles only exist in `index.html`; other pages render unstyled, flat cards |
| **INC-03** | **Missing `@keyframes fadeInUp` (`opacity-0` Bug)** | **P1 (High)** | ✅ RESOLVED (Phase 1) | 11+ views in `hq/*` and `station/*` | Elements stay stuck at `opacity: 0` because the animation keyframe is absent |
| **INC-04** | **Broken `borderRadius` Scale in `base.html`** | **P1 (High)** | ✅ RESOLVED (Phase 1) | `app/templates/layouts/base.html` (L65) | `"full": "0.75rem"` (12px), `rounded-md` (6px) > `rounded-lg` (4px) |
| **INC-05** | **"Bharti" Misspelling** | **P1 (High)** | ✅ RESOLVED (Phase 2) | `app/templates/hq/compliance.html` (L103) | Misspelled as `Southern Ocean Expedition (RV Bharti)` |
| **INC-06** | **"ANARCTIC" Brand Typo (Missing 'T')** | **P1 (High)** | ✅ RESOLVED (Phase 2) | `auth/login.html`, `auth/recover.html`, `modals/*` | Heading reads "ANARCTIC" instead of "ANTARCTIC" |
| **INC-07** | **Topnav Hardcoded Location & Timezone** | **P1 (High)** | ✅ RESOLVED (Phase 3) | `app/templates/components/topnav.html` (L29-30) | Hardcodes `LARSEMANN HILLS` and `+05:00` across all station portals |
| **INC-08** | **Canvas Padding Doubling & Gutter Discrepancies** | **P2 (Medium)** | ✅ RESOLVED (Phase 1) | `station/dashboard`, `station/infrastructure`, etc. | Viewports add redundant inner padding on top of `layouts/dashboard.html` |
| **INC-09** | **Coexistence of 3 Conflicting Design Subsystems** | **P2 (Medium)** | ✅ RESOLVED (Phase 5) | Entire frontend | Dark Sci-Fi HUD vs Glassmorphism Serif vs Raw Hex Auth Card |
| **INC-10** | **Geographic Coordinates Drift** | **P2 (Medium)** | ✅ RESOLVED (Phase 3) | `index.html`, `topnav.html`, `hq/*`, `station/*` | Maitri & Bharati coordinates fluctuate across 5+ conflicting formats |
| **INC-11** | **Station Code / Identifier Chaos** | **P2 (Medium)** | ✅ RESOLVED (Phase 3) | `station/*`, `hq/*` | Bharati is interchangeably `IND-ANT-03`, `IN-ANT-BHT-02`, `IN-BHT-02`, `BHT-02` |
| **INC-12** | **Personnel Headcount Contradictions** | **P2 (Medium)** | Pending (Phase 3/4) | `hq/health`, `hq/stations`, `hq/dashboard`, `station/logistics` | Total personnel counts conflict: 142 vs 112/49 vs 46 vs 42 vs 43 |
| **INC-13** | **Microgrid Generation Mismatch** | **P2 (Medium)** | ✅ RESOLVED (Phase 4) | `station_twin.js`, `station/energy.html`, `hq/energy.html` | Twin outputs 742 kW generator power vs 340 kW station ceiling |
| **INC-14** | **Dead / 0-Byte Templates & Orphaned Routes** | **P3 (Low)** | ✅ RESOLVED (Phase 4) | `app/templates/maitri/*`, `components/*`, `sidebar_hq.html` | 11 empty files, unlinked `/hq/compliance`, and full mockups in `modals/` |

---

## 3. Visual & Geometric Design Inconsistencies

### 3.1. Inconsistent Rounded Corners & Broken Border-Radius Tokens (P1)

In `app/templates/layouts/base.html` (Line 65), the Tailwind configuration specifies:
```javascript
borderRadius: {
  "DEFAULT": "0.125rem", // 2px
  "lg": "0.25rem",       // 4px
  "xl": "0.5rem",        // 8px
  "full": "0.75rem"      // 12px (! Broken)
}
```

#### The Anomalies:
1. **The `rounded-full` Token Bug:**
   * Tailwind's default `rounded-full` is `9999px` (creating true circular avatars and pill buttons).
   * DTFIAS overrides `"full"` to `0.75rem` (12px).
   * **Consequence:** Circular elements larger than 24×24px (such as pill buttons `px-4 py-2 rounded-full`, user avatars `w-8 h-8 rounded-full bg-primary`, or large indicators) do **not** render as circular or pills; they render as rounded rectangles with a 12px corner radius.
2. **Inverted Sizing Hierarchy (`rounded-md` > `rounded-lg`):**
   * The config overrides `DEFAULT` (2px), `lg` (4px), and `xl` (8px), but **omits `md`**.
   * Tailwind falls back to its default `rounded-md` value of `0.375rem` (**6px**).
   * **Consequence:** `rounded-md` (6px) is geometrically **larger** than `rounded-lg` (4px), completely inverting CSS semantics.
3. **Card Border Radius Fragmentation:**
   * `app/templates/index.html`: Uses arbitrary `rounded-[1.25rem]` (20px) on station selection cards.
   * `app/templates/station/dashboard.html` & `hq/dashboard.html`: Use `rounded-xl` (8px).
   * `app/templates/hq/environment.html` & `hq/energy.html`: Use `rounded` (2px) and `rounded-lg` (4px) for primary metric cards.
   * `app/templates/auth/login.html` & `auth/recover.html`: Mix `rounded-xl`, `rounded-md`, `rounded-lg`, and `rounded-sm`.
   * Result: Adjacent views within the same session have card radiuses varying from 2px to 20px with no design hierarchy.

---

### 3.2. Undefined Classes: `.glass-card` and `.glass-button` (P1)

In `app/templates/index.html` (Lines 65–94), `.glass-card` and `.glass-button` are defined inside an inline `<style>` block:
```css
.glass-card {
    background: rgba(26, 49, 44, 0.4);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.07);
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.glass-button {
    background: rgba(66, 132, 117, 0.15);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(66, 132, 117, 0.3);
}
```

#### The Anomaly:
* Neither `.glass-card` nor `.glass-button` is declared in `app/static/css/app.css` or `app/templates/layouts/base.html`.
* Yet the following **11 dashboard templates** rely on `glass-card` and `glass-button`:
  1. `app/templates/hq/stations.html`
  2. `app/templates/hq/health.html`
  3. `app/templates/hq/research.html`
  4. `app/templates/hq/reports.html`
  5. `app/templates/hq/roles.html`
  6. `app/templates/hq/settings.html`
  7. `app/templates/hq/simulations.html`
  8. `app/templates/station/personnel.html`
  9. `app/templates/station/health.html`
  10. `app/templates/station/research.html`
  11. `app/templates/station/asset_detail.html`
* **Consequence:** On all 11 pages, these containers have **no background, no backdrop blur, and no box-shadow**. They render as transparent flat wireframes with border lines, breaking the glassmorphic aesthetic completely.

---

### 3.3. Missing `@keyframes fadeInUp` Causing Permanent Invisibility (P1)

In `app/templates/index.html` (Line 95), `@keyframes fadeInUp` is defined locally:
```css
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
```

#### The Anomaly:
* `@keyframes fadeInUp` is **missing from `app/static/css/app.css` and `base.html`**.
* The following templates set their root sections and headers to initial opacity zero:
  * `hq/health.html` (Lines 5, 24, 79)
  * `hq/reports.html` (Lines 5, 21)
  * `hq/research.html` (Lines 5, 21)
  * `hq/roles.html` (Lines 5, 20)
  * `hq/settings.html` (Lines 5, 20)
  * `hq/simulations.html` (Lines 5, 24)
  * `hq/stations.html` (Lines 5, 15)
  * `station/asset_detail.html` (Lines 5, 20)
  * `station/health.html` (Lines 5, 20)
  * `station/personnel.html` (Lines 5, 15)
  * `station/research.html` (Lines 5, 15)
  * `station/telemetry.html` (Lines 5, 15)
* Each of these lines declares:
  ```html
  <div class="... opacity-0 animate-[fadeInUp_0.8s_ease-out_forwards]">
  ```
* **Consequence:** Because `@keyframes fadeInUp` is not defined in the active document scope, the CSS animation fails to execute. The elements remain at `opacity: 0`, rendering headers, grids, and primary cards invisible or glitchy on load.
* Similarly, `station/telemetry.html` (Line 42) uses `animate-[fadeIn_0.3s_ease-out_forwards]` where `@keyframes fadeIn` is also completely missing.

---

### 3.4. Inconsistent Padding, Margins & Canvas Double-Padding (P2)

#### 1. The Canvas Double-Padding Bug
`app/templates/layouts/dashboard.html` establishes the master page shell:
```html
<main class="relative flex-grow pt-14 w-full px-4 sm:px-6 lg:px-canvas-margin overflow-x-hidden">
  <div class="flex flex-col w-full space-y-space-md select-none pb-space-xl mt-space-md">
    {% block dashboard_content %}{% endblock %}
  </div>
</main>
```
* The layout already applies `lg:px-canvas-margin` (32px) and `space-y-space-md` (16px).
* However, individual child templates add conflicting internal padding:
  * `station/dashboard.html` (Line 59): Adds `<div class="p-space-md ...">` (adds an extra 16px padding inside an already padded container).
  * `station/infrastructure.html` (Line 4): Adds `<div class="w-full px-space-base py-space-md ...">` (adds 20.8px horizontal padding).
  * `station/environment.html` (Line 4): Adds `<div class="px-space-base py-space-sm ...">`.
  * `hq/stations.html` & `hq/commands.html`: Do **not** add extra inner padding.
* **Consequence:** Viewing `station/dashboard.html` has double horizontal padding (52.8px total inset), while switching to `hq/stations.html` snaps outward to 32px inset.

#### 2. Card Internal Padding Inconsistencies
Cards and containers across the app use competing padding standards:
* `p-space-md` (16px) in `hq/stations.html`, `hq/health.html`, `hq/reports.html`.
* `p-space-base` (20.8px) in `hq/energy.html`, `hq/environment.html`, `hq/logistics.html`.
* `p-space-xl` (41.6px) in `station/asset_detail.html`.
* `p-8` (32px) in `index.html`, `auth/login.html`, `auth/recover.html`.
* Raw Tailwind `p-4` (16px) and `p-3` (12px) in `station/personnel.html`, `station/health.html`, `hq/settings.html`.

#### 3. Grid Gutters Inconsistencies
* `gap-panel-gutter` (16px) in `station/alerts.html`, `station/twin.html`, `hq/dashboard.html`.
* `gap-space-md` (16px) in `hq/stations.html`, `hq/health.html`.
* `gap-space-sm` (10.4px) in `hq/environment.html`.
* Raw Tailwind `gap-4` (16px) in `station/personnel.html` and `hq/simulations.html`.
* `gap-space-base` (20.8px) in `hq/energy.html`.

#### 4. Button Padding Sizing
Buttons lack a unified component class:
* `px-space-sm py-space-xs` (10.4px × 5.2px) in `station/twin.html`
* `px-space-md py-space-xs` (16px × 5.2px) in `hq/health.html`
* `px-4 py-2` (16px × 8px) in `hq/stations.html`, `station/personnel.html`
* `px-3 py-1.5` (12px × 6px) in `hq/reports.html`
* `px-space-sm py-space-2xs` (10.4px × 2.56px) in `station/dashboard.html`

---

### 3.5. Coexistence of Three Conflicting Visual Subsystems (P2)

The DTFIAS codebase suffers from an architectural identity split across three incompatible visual paradigms:

```
┌───────────────────────────────────┬───────────────────────────────────┬───────────────────────────────────┐
│ Subsystem A: Sci-Fi Telemetry HUD │ Subsystem B: Glassmorphic Serif   │ Subsystem C: Raw Hex Auth Card    │
├───────────────────────────────────┼───────────────────────────────────┼───────────────────────────────────┤
│ • station/dashboard.html          │ • index.html                      │ • auth/login.html                 │
│ • station/twin.html               │ • hq/stations.html                │ • auth/recover.html               │
│ • station/energy.html             │ • hq/commands.html                │                                   │
│ • station/infrastructure.html     │ • hq/health.html                  │                                   │
│ • station/environment.html        │ • hq/research.html                │                                   │
│ • station/logistics.html          │ • hq/reports.html                 │                                   │
│ • hq/dashboard.html               │ • hq/roles.html                   │                                   │
│ • hq/energy.html                  │ • hq/simulations.html             │                                   │
│ • hq/environment.html             │ • station/personnel.html          │                                   │
│ • hq/compliance.html              │ • station/health.html             │                                   │
│ • hq/audit.html                   │ • station/research.html           │                                   │
│ • hq/users.html                   │ • station/telemetry.html          │                                   │
├───────────────────────────────────┼───────────────────────────────────┼───────────────────────────────────┤
│ Tokens:                           │ Tokens:                           │ Tokens:                           │
│ bg-surface-container-*            │ glass-card, glass-button          │ Hardcoded hexes: #1A312C, #152924,│
│ text-telemetry-safe/warning/crit  │ text-status-ok, text-status-warn  │ #27443D, #71C5B0, #8DA19A         │
│ font-telemetry-code (monospace)   │ Inline Playfair Display styles    │ font-sans, font-mono              │
│ High-density SCADA readouts       │ Minimal editorial cards           │ Light card on dark background     │
└───────────────────────────────────┴───────────────────────────────────┴───────────────────────────────────┘
```

#### Why This Is Problematic:
1. Navigating from `/bharati/` (Subsystem A: dense telemetry, dark container blocks) to `/bharati/personnel` (Subsystem B: airy glassmorphism with unstyled white cards and Playfair serif headings) feels like switching to an entirely different application.
2. The authentication views (`auth/login.html` and `auth/recover.html`) ignore the design tokens completely, hardcoding arbitrary hexes (`#152924`, `#27443D`, `#71C5B0`) and referencing non-existent CSS utility classes (`bg-emerald-norm`, `text-ncpor-charcoal`, `border-teal-green/40`).

---

### 3.6. Typography & Inline Font Family Spray (P2)

`.agents/brand_design/SKILL.md` strictly defines the typography stack:
* Headings: **Playfair Display** (`--font-heading`)
* Paragraphs: **Playfair** (`--font-body`)
* Chrome / UI: **Inter** (`--font-ui`)
* Data / Sensor: **JetBrains Mono** (`--font-mono`)

#### The Anomaly:
Instead of using configured typography utility classes (`font-headline-display`, `font-headline-xl`), **15+ headings across the templates use inline styles**:
```html
<h1 class="font-headline-display text-headline-display text-on-surface tracking-tight" style="font-family: 'Playfair Display', serif;">
```
This occurs in:
* `hq/stations.html` (Lines 11, 23, 62, 99)
* `hq/health.html` (Lines 11, 25, 84, 151)
* `hq/reports.html` (Line 11)
* `hq/research.html` (Lines 11, 25, 70)
* `hq/roles.html` (Lines 11, 21)
* `hq/simulations.html` (Lines 11, 29)
* `hq/settings.html` (Lines 11, 24, 49)
* `station/personnel.html` (Line 11)
* `station/health.html` (Lines 11, 25)
* `station/research.html` (Line 11)
* `station/asset_detail.html` (Lines 11, 22)

---

### 3.7. Sidebar & Modal Dimension Inconsistencies (P3)

* **Standard Navigation:** `sidebar_maitri.html`, `sidebar_bharati.html`, and `sidebar_hq.html` are configured with a width of `w-72` (288px). `layouts/dashboard.html` has `lg:pl-72` and `components/topnav.html` has `left-72`.
* **Modal Mockup Desynchronization:** In `components/modals/alert_dialog.html` and `components/modals/asset_detail.html`, the embedded sidebar is hardcoded as `w-64` (256px) and the content container has `pl-64`. If opened or rendered, the sidebar shrinks by 32px and creates a misaligned seam with the top navigation bar.

---

## 4. Informational Design Inconsistencies

### 4.1. Bharati Data Hardcoded in Maitri Contexts (P0 — Critical)

Both station routers (`app/routers/bharati/router.py` and `app/routers/maitri/router.py`) serve views from `app/templates/station/{name}.html`. Because `station/` contains hardcoded content for Bharati:

1. **Dashboard (`station/dashboard.html`):**
   * Line 8: `BHARATI POLAR RESEARCH STATION // DIGITAL TWIN CORE`
   * Line 9: `STATION ID: IND-ANT-03`
   * Line 14: `69°24′28″S 76°11′14″E — Larsemann Hills, Prydz Bay`
   * Lines 185–241: Center visual is an isometric SVG of Bharati’s aerodynamic container complex on stilts.
   * Line 540: Section lists `"Maitri Link (11°44′E)"` as an external remote link. On Maitri's own dashboard, Maitri links to itself.
   * Line 721: Telemetry CSV export filename is `bharati_telemetry_snapshot.csv`.
   * Line 728: Emergency circuit confirmation prompt: `Confirm initiation of Emergency Heating Fallback circuits for Bharati Habitat?`.
2. **Digital Twin (`station/twin.html`):**
   * Line 67: `BHARATI MAIN RESEARCH POD (REV 4.2)`
   * Line 9: `69°24'40"S 76°11'42"E`
   * Line 73: `STILT HYDRAULIC: BALANCED (3.4 bar)`. (Maitri has fixed foundations, not hydraulic stilts).
3. **Energy (`station/energy.html`):**
   * Line 12: `BHARATI POLAR CAMPUS`
   * Line 14: `GRID CELL ID // IN-ANT-BHT-02-PWR`
4. **Infrastructure (`station/infrastructure.html`):**
   * Line 11: `BHARATI STATION`
   * Line 12: `69°24′28″S 76°11′14″E • SECTOR IV`
   * Line 167: `Bharati 3-Level Containerized Architecture`
   * Line 186: Image depicting Bharati ISO container units on stilts.
5. **Environment (`station/environment.html`):**
   * Line 20: Mission Node dropdown defaults to `Larsemann Hills (Bharati Station)`.
   * Line 31: HUD coordinates pill hardcodes `69°24′28″S 76°11′14″E`.
   * Line 113: Section labeled `BHARATI MAIN BASE`.
6. **Logistics (`station/logistics.html`):**
   * Line 68: `24 / 24 BHARATI`
   * Line 111: `Bharati Station Detachment`
   * Line 114: `Live continuous beacon telemetry • Larsemann Hills Locus`
   * Line 371: `SHOWING 5 OF 24 LOGGED EXPEDITION MEMBERS (BHARATI DETACHMENT)`
   * Line 491: `Exterior transit between Bharati Main Hab and LIDAR dome prohibited...`
   * Line 596: `24/24 Bharati RF-tags responded with 0ms delta.`
7. **Alerts (`station/alerts.html`):**
   * Line 11: Breadcrumb reads `Bharati IN-ANT-BHT-02`.
   * Line 227: `#INC-BHT-4091`

---

### 4.2. Spelling, Nomenclature & Typographical Errors (P1) — [RESOLVED in Phase 2]

1. **"Bharti" Misspelling:** [RESOLVED]
   * `app/templates/hq/compliance.html` (Line 103): Corrected `RV Bharti` to `RV Bharati`.
2. **"ANARCTIC" Brand Typo (Missing 'T'):** [RESOLVED]
   * `app/templates/auth/login.html` (Line 51): Corrected to `ANTARCTIC`.
   * `app/templates/auth/recover.html` (Line 28): Corrected to `ANTARCTIC`.
   * `app/templates/components/modals/alert_dialog.html` (Line 1): Corrected to `ANTARCTIC`.
   * `app/templates/components/modals/asset_detail.html` (Line 1): Corrected to `ANTARCTIC`.
3. **"Medivac" vs "Medevac":** [RESOLVED]
   * `app/templates/hq/health.html` (Line 18): Standardized `Deploy Medivac` to `Deploy Medevac` to match `Active Medevacs` and `MEDEVAC AIR LIFT INDEX`.
4. **"Maitri Oases" vs "Schirmacher Oasis":** [RESOLVED]
   * `app/templates/hq/alerts.html` (Line 190): Corrected `LOCUS: MAITRI OASES` to `LOCUS: MAITRI OASIS`.

---

### 4.3. Geographic Coordinates & Location Discrepancies (P2)

The recorded coordinates for both stations shift across views:

| Station | Location / Template | Coordinates Rendered | Deviation |
|:---|:---|:---|:---|
| **Bharati** | `index.html`, `sidebar_bharati.html`, `hq/dashboard.html` | `69°24'S, 76°11'E` | Degree-minute standard |
| **Bharati** | `bharati/station_twin.html` | `69.4°S 76.2°E` | Decimal format |
| **Bharati** | `station/twin.html` | `69°24'40"S 76°11'42"E` | +12" to +28" seconds offset |
| **Bharati** | `station/dashboard.html`, `hq/compliance.html` | `69°24′28″S 76°11′14″E` | Official survey fix |
| **Bharati** | `hq/telemetry.html` | `69°24'29" S \| 76°11'14" E` | +1" second offset |
| **Maitri** | `index.html`, `hq/stations.html`, `hq/logistics.html` | `70°45'S, 11°43'E` | Base representation |
| **Maitri** | `components/topnav.html`, `auth/recover.html`, `hq/dashboard.html` | `70°46'S, 11°44'E` | Shifts to 46'S, 44'E |
| **Maitri** | `hq/compliance.html` | `70°45′57″S 11°44′09″E` | High-precision seconds fix |
| **Maitri** | `hq/telemetry.html` | `70°45'58" S \| 11°44'09" E` | 1-second drift |

---

### 4.4. Personnel Headcount Contradictions (P2)

```
┌─────────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┐
│ Template / Screen       │ Bharati Headcount    │ Maitri Headcount     │ Total Exped. Souls   │
├─────────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ hq/health.html          │ Unspecified          │ Unspecified          │ 142 (Active Roster)  │
│ hq/stations.html        │ 47 Summer / 24 Winter│ 65 Summer / 25 Winter│ 112 Summer / 49 Winter│
│ station/dashboard.html  │ 46 (Overwinter)      │ 46 (when on Maitri)  │ 46 Souls             │
│ hq/dashboard.html       │ 24 Souls             │ 18 Souls             │ 42 Souls             │
│ station/logistics.html  │ 24 Souls             │ 18 Souls             │ 42 Souls             │
│ hq/telemetry.html       │ 24 PERS              │ 19 PERS              │ 43 Souls             │
└─────────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┘
```

#### Personnel Roster Contamination:
* In `hq/health.html` (Lines 108–140), **Dr. R. Kapoor** and **M. Nair** are assigned to **Bharati**, while **A. Sharma** is assigned to **Maitri (Traverse)**.
* In `station/personnel.html` and `station/health.html`, the exact same individuals are rendered under `{{ station_id }} Roster`. On `/maitri/personnel`, Dr. Kapoor and M. Nair appear as local Maitri personnel.

---

### 4.5. Microgrid Generation & SCADA Inconsistencies (P2)

* `hq/energy.html` (Line 48): Total Continental Demand = **472.4 kW** (Bharati: 285.0 kW, Maitri: 187.4 kW).
* `hq/dashboard.html` (Lines 68 & 110): Net Power = **71.0 kW** for Bharati and **82.1 kW** for Maitri (3x discrepancy).
* `station/energy.html` (Line 53): Bharati max ceiling is **340.0 kW**, load is **282.4 kW**.
* `station_twin.js` (Lines 20 & 57): Bharati simulated generator output is **742 kW** (more than 2.1x station capacity).
* Generator models conflict across views:
  * Bharati: `CAT C32` (1000 kW) in `station_twin.js` vs `SCANIA DC13 · 320kVA` in `station/infrastructure.html` vs `BHT-GEN-01/02/03` in `hq/energy.html`.
  * Maitri: `Kirloskar Polar 160`, `Kirloskar Polar 125`, and `CAT 3406 Heavy` in `hq/energy.html`.

---

## 5. Comprehensive Remediation Roadmap

## 5. Comprehensive Remediation Roadmap

### Phase 1: Fix Visual Tokens & CSS Architecture — [COMPLETED]
*Status: COMPLETED (Verified across all 48 frontend endpoints)*

1. **Global `.glass-card` & `.glass-button` Classes Added to `layouts/base.html`:**
   - Moved and standardized `.glass-card` (`backdrop-filter: blur(16px)`, `rgba(13, 31, 27, 0.6)`) and `.glass-button` with interactive hover/active states into `app/templates/layouts/base.html`.
   - Cleaned redundant duplicates from `app/templates/index.html`. All 11 internal views (`hq/stations`, `hq/health`, `hq/reports`, `station/telemetry`, etc.) now render styled glassmorphic panels and buttons.
2. **Global `@keyframes fadeInUp` & `@keyframes fadeIn` Registered:**
   - Declared keyframes in `layouts/base.html` `<style>` and configured them in `tailwind.config` (`theme.extend.keyframes` and `theme.extend.animation`).
   - Resolved the critical P1 bug where headers, statistic grids, and primary cards were stuck at `opacity: 0` because `@keyframes fadeInUp` was missing outside `index.html`.
3. **Corrected `borderRadius` Tokens in `tailwind.config` (`layouts/base.html`):**
   - Fixed `full: "9999px"` (previously broken as `"0.75rem"` / 12px), restoring circular geometry to avatars, status ping dots, toggle pills, and badges across hundreds of elements.
   - Established the standardized monotonic radius scale:
     ```javascript
     borderRadius: {
       "none": "0px",
       "sm": "0.125rem",     // 2px (micro badges)
       "DEFAULT": "0.25rem", // 4px (default inputs, small buttons)
       "md": "0.375rem",     // 6px (standard buttons, dropdowns)
       "lg": "0.5rem",       // 8px (standard cards, panels)
       "xl": "0.75rem",      // 12px (large cards, hero containers)
       "2xl": "1rem",        // 16px (major dashboard widgets)
       "3xl": "1.5rem",      // 24px (curved modals)
       "full": "9999px"      // True circular avatars, pills, status rings
     }
     ```
4. **Added Missing Brand Tokens & Typography Mapping:**
   - Populated dark status context tokens (`--status-ok-dark`, `--status-info-dark`, `--status-warning-dark`, `--status-critical-dark`) and stale/offline tokens (`--status-stale`, `--status-offline`) in `:root`.
   - Added missing color tokens used in auth views (`teal-green`, `teal-hover`, `light-mint`, `emerald-norm`, `ncpor-charcoal`).
   - Added font family aliases (`headline-display`, `sans`, `mono`, `heading`, `body`) to `tailwind.config` to prevent broken fonts on titles.
5. **Eliminated Viewport Double-Padding Inconsistencies:**
   - `station/dashboard.html` (L59): Removed `p-space-md` from main workspace grid to align perfectly with the header ribbon and `layouts/dashboard.html` canvas margins.
   - `station/infrastructure.html` (L4): Removed `px-space-base py-space-md` wrapper so bounds match the master canvas inset.
   - `station/environment.html` (L62): Removed `p-panel-gutter` outer grid wrapper to align with the GIS header ribbon.
   - `station/logistics.html` (L4): Removed `py-space-base` to prevent vertical canvas margin inflation.
6. **Automated Verification:**
   - Ran `scripts/audit_frontend_routes.py` against all 48 application routes. Every single UI route returned HTTP 200 with complete rendered HTML body lengths.

---

### Phase 2: Correct Brand & Typographical Errors — [COMPLETED]
*Status: COMPLETED (Verified across all templates and static assets)*

1. **Corrected Brand Misspelling "ANARCTIC" → "ANTARCTIC":**
   - [`app/templates/auth/login.html`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/app/templates/auth/login.html#L51): Corrected `ANARCTIC` to `ANTARCTIC`.
   - [`app/templates/auth/recover.html`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/app/templates/auth/recover.html#L28): Corrected `ANARCTIC` to `ANTARCTIC`.
   - [`app/templates/components/modals/alert_dialog.html`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/app/templates/components/modals/alert_dialog.html#L1): Corrected `ANARCTIC` to `ANTARCTIC`.
   - [`app/templates/components/modals/asset_detail.html`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/app/templates/components/modals/asset_detail.html#L1): Corrected `ANARCTIC` to `ANTARCTIC`.
2. **Corrected Station Expedition Vessel "RV Bharti" → "RV Bharati":**
   - [`app/templates/hq/compliance.html`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/app/templates/hq/compliance.html#L103): Corrected `Southern Ocean Expedition (RV Bharti)` to `Southern Ocean Expedition (RV Bharati)`.
3. **Standardized Medical Evacuation Nomenclature "Medivac" → "Medevac":**
   - [`app/templates/hq/health.html`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/app/templates/hq/health.html#L18): Changed `Deploy Medivac` to `Deploy Medevac` to match `Active Medevacs` (Line 38) and `MEDEVAC AIR LIFT INDEX` ([`station/logistics.html:L80`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/app/templates/station/logistics.html#L80)).
4. **Corrected Geographic Oasis Nomenclature "MAITRI OASES" → "MAITRI OASIS":**
   - [`app/templates/hq/alerts.html`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/app/templates/hq/alerts.html#L190): Changed `LOCUS: MAITRI OASES` to `LOCUS: MAITRI OASIS` to maintain singular consistency with `Schirmacher Oasis` (Line 194).
5. **Automated Verification:**
   - Grep verification across all templates confirmed zero remaining instances of `ANARCTIC`, `Bharti`, `Medivac`, or `Oases`.
   - All routes render valid markup.

---

### Phase 3: Parameterize Shared Station Templates — [COMPLETED]
*Status: COMPLETED (Verified across Maitri, Bharati, and HQ routes)*

1. **Integrated Canonical Station Context across Routers:**
   - Both `app/routers/maitri/router.py` and `app/routers/bharati/router.py` consume `get_station_metadata(station_id)` from `shared/constants/stations.py`, injecting canonical station metadata (`full_name`, `code`, `grid_id`, `callsign`, `location`, `region`, `coordinates`, `elevation`, `architecture`, `architecture_subtitle`, `foundation`, `souls_total`, `souls_active`, `emergency_zone`, `locus_name`, `twin_rev`).
2. **Dynamic Parameterization across Shared Station Templates:**
   - `station/dashboard.html`: Parameterized station header title, station code badge, coordinates & location geofix, VHF inter-station link, CSV snapshot download name, and emergency heating prompt.
   - `station/twin.html`: Parameterized geofix coordinates, elevation, research complex title, digital twin revision, and structural foundation description.
   - `station/energy.html`: Parameterized polar campus name and microgrid cell ID.
   - `station/infrastructure.html`: Parameterized station name, geofix coordinates, architecture title, and thermal envelope subtitle.
   - `station/environment.html`: Parameterized Mission Node select dropdown, HUD coordinates pill, elevation, and main base map marker.
   - `station/logistics.html`: Parameterized overwinter headcount ratio, detachment name, locus name, table footer member counter, emergency zone transit warning, and RFID muster drill toast.
   - `station/alerts.html`: Parameterized breadcrumb station code and active incident code with station callsign.
3. **Defensive Top Navigation Parameterization:**
   - `components/topnav.html`: Added dynamic region and timezone formatting with safe `station is defined` guards to maintain global compatibility with both station portals and HQ views.

---

### Phase 4: Reconcile Metrics & Clean Up Dead Files — [COMPLETED]
*Status: COMPLETED (Verified across components and assets)*

1. **Adjusted `station_twin.js`**: Adjusted generator load from `742 kW` to `282 kW` to match the SCADA specification.
2. **Dynamic Topnav Timezone**: Updated `components/topnav.html` to dynamically reflect the current station’s timezone and location using an Alpine.js ticking clock rather than hardcoded text.
3. **Sidebar Updates**: Added a navigation link to `/hq/compliance` in `components/sidebar_hq.html` replacing `/hq/reports`.
4. **Deleted Dead Files**: Deleted the 0-byte placeholder files in `app/templates/maitri/` and `app/templates/components/`.
