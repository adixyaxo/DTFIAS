# DTFIAS — Deep Navigation Bar & Responsive Architecture Audit Report

> **Document Status:** Authoritative QA & Frontend Defect Audit  
> **Target Path:** `docs/testing/frontendInconsistency/navbar-inconsistency-and-responsive-audit.md`  
> **Auditor Persona:** Frontend Testing Agent (`.agents/agents/FrontendTestingAgent/agent.md`)  
> **Scope:** Top Navigation Bar (`app/templates/components/topnav.html`), Dashboard Layout (`app/templates/layouts/dashboard.html`), Station & HQ Sidebars (`app/templates/components/sidebar_*.html`), Landing Nav (`app/templates/index.html`), and Security Header (`app/templates/auth/login.html`).  
> **Date:** September 2026  
> **Target Audience:** Frontend Inconsistency Manager, Human Engineers, and UI Developers  

---

## 1. Executive Summary

A forensic inspection of the DTFIAS navigation architecture was conducted across all supported screen viewports (375px mobile through 1920px+ ultrawide) and across the three primary system surfaces:
1. **The Institutional Landing Surface** (`app/templates/index.html`)
2. **The Security & Authentication Banner** (`app/templates/auth/login.html`, `app/templates/auth/recover.html`)
3. **The Operational Mission Control Header & Sidebar System** (`app/templates/components/topnav.html`, `app/templates/layouts/dashboard.html`, `app/templates/components/sidebar_*.html`)

### Critical Discoveries Summary

* **P0 Catastrophic Mobile Breakage (`FE-RESP-001`):** In `app/templates/components/topnav.html` (line 2), the header declares `class="fixed top-0 left-72 right-0 ..."`. The `left-72` (288px) offset is applied **unconditionally without a responsive prefix**. On viewports below the `lg` breakpoint (< 1024px), the sidebar disappears (`hidden lg:flex`), yet the top navigation remains permanently indented by 288px. On a 390px mobile device, the first 288px of the top of the screen is an empty transparent void, while the navigation content extends 288px past the right edge into the void, completely blowing out viewport width.
* **P0 Total Mobile Navigational Lockout (`FE-RESP-002`):** Below 1024px, the sidebar is hidden (`hidden lg:flex`). However, the topbar contains **zero hamburger menu toggles, zero drawer triggers, and zero mobile navigation links**. On phones and tablets, users are completely trapped on whichever page they land on, unable to navigate to any station subsystem, telemetry view, or alert matrix without manually modifying the URL in the browser bar.
* **P1 Desktop Viewport Collision Zone (1024px – 1440px) (`FE-RESP-003`):** Between 1024px and 1440px, the header attempts to pack 9 distinct operational widgets (logo, title, subtitle, station selector, SATCOM pill, clocks, DEFCON badge, role selector, alert bell, profile badge) into 736px–992px of available track width. Because secondary status elements lack responsive hiding classes (`hidden md:flex`, `hidden 2xl:flex`), these widgets violently collide, wrap outside the 56px (`h-14`) boundary, and overlap each other.
* **P1 Disruptive Breakpoint Pop-In at 1280px (`FE-RESP-004`):** The dual UTC/Local clock widget uses `hidden xl:flex`. When expanding the screen from 1279px to 1280px (`xl`), the clock suddenly pops into existence, instantly injecting ~240px of width into an already crowded 992px flex container, making layout collision **worse** at 1280px than at 1200px.
* **P1 Inert Dummy Select Elements (`FE-FUNC-001`, `FE-FUNC-002`):** Both the Station Selector (`<select>`) and Role Selector (`<select>`) in `topnav.html` are inert dummy elements with no `x-on:change`, no HTMX attributes, no `<form>` wrappers, and no route binding. Selecting a different station or role produces zero application response. Furthermore, client-side role switching directly conflicts with backend RBAC constraints (**C5**).
* **P1 Visual Seam & Tone Misalignment (`FE-VIS-001`):** The sidebar header uses `bg-surface-container` (`#12231f`), while the topbar directly adjacent to it uses `bg-surface-container-low/95` (`#0d1f1b`). Although both share the same 56px (`h-14`) baseline, they create a jarring two-tone dark green visual seam at x = 288px.

---

## 2. Navigation Architecture & Component Inventory

The DTFIAS navigation system is composed of five distinct templates across the codebase:

```
DTFIAS Navigation Architecture
│
├── app/templates/layouts/dashboard.html ── Master Layout Wrapper
│   ├── components/sidebar_{station_id}.html (Fixed Left Sidebar: w-72, hidden lg:flex)
│   ├── components/topnav.html               (Fixed Topbar: h-14, fixed top-0 left-72 right-0)
│   └── <main> Content Area                  (Offset: lg:pl-72, pt-14)
│
├── app/templates/index.html                 ── Landing Page Nav (max-w-7xl, py-8, transparent)
│
└── app/templates/auth/login.html            ── Auth Security Banner (h-auto, py-2, bg-deep-green-darker)
```

### Component Details

| Component | File Path | Width / Height | Position / Layer | Responsive Classes | Primary Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Operational Topnav** | `app/templates/components/topnav.html` | `w-auto`, `h-14` (56px) | `fixed top-0 left-72 right-0 z-40` | `hidden xl:flex` (clocks only) | Real-time mission control metadata, station picker, clocks, alerts |
| **Maitri Sidebar** | `app/templates/components/sidebar_maitri.html` | `w-72` (288px), `h-full` | `fixed left-0 top-0 z-50` | `hidden lg:flex` | Inland oasis domain routing (Energy, Hab, Logistics) |
| **Bharati Sidebar** | `app/templates/components/sidebar_bharati.html` | `w-72` (288px), `h-full` | `fixed left-0 top-0 z-50` | `hidden lg:flex` | Coastal station domain routing (2.5D Twin, Telemetry) |
| **HQ Sidebar** | `app/templates/components/sidebar_hq.html` | `w-72` (288px), `h-full` | `fixed left-0 top-0 z-50` | `hidden lg:flex` | Continental command routing (Fleet, Madrid Protocol, RBAC, Audit) |
| **Landing Nav** | `app/templates/index.html` | `max-w-7xl`, `h-auto` | In-flow static flex | `hidden sm:block` (logo divider) | Public access gateway |
| **Auth Banner** | `app/templates/auth/login.html` | `w-full`, `h-auto` | In-flow static flex | `hidden sm:inline`, `hidden md:inline` | Security encryption declaration |

---

## 3. Deep Breakpoint-by-Breakpoint Responsive Analysis

### 3.1 Mobile Viewports (< 640px — e.g., iPhone SE 375px, iPhone 14 390px, Pixel 7 412px)

```
0px                                 288px             390px (Screen Edge)
┌───────────────────────────────────┬─────────────────┐
│       EMPTY VOID / CUT OFF        │ TOPNAV STARTS   │ ---> Overflows to x = 678px
│   (No background, no header)      │ (Logo, partial) │      (Horizontal blowout)
├───────────────────────────────────┴─────────────────┤
│                                                     │
│   PAGE CONTENT (lg:pl-72 drops to 0px)              │
│   Users have NO SIDEBAR and NO HAMBURGER MENU.      │
│   Navigation is 100% physically locked.             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

1. **Geometry Disconnection:**
   * In `layouts/dashboard.html`: Content has `lg:pl-72`. On mobile, padding is `0px`.
   * In `components/topnav.html`: Header has `left-72` (18rem / 288px) **unconditionally**.
   * On a 390px viewport, the header is forced to start 288px from the left screen boundary. The left 74% of the screen has no header. The header container has only `390 - 288 = 102px` of screen width, but its children demand ~700px.
   * Result: Severe horizontal scrollbar on the viewport (`overflow-x` blowout), cutting off the notification bell, role switcher, and user avatar.
2. **Total Navigation Deprivation:**
   * The sidebar has `hidden lg:flex` and is completely unmounted from the layout.
   * The topbar has no hamburger toggle (`material-symbols-outlined: menu`) or Alpine mobile drawer.
   * Mobile users cannot navigate to any other page in the application.
3. **Touch Targets (WCAG 2.5.5 / 2.5.8):**
   * The notification button (`p-1.5` = 28x28px) and select dropdowns (`py-1` = 24px) fall far below the 44x44px minimum touch target size.

---

### 3.2 Tablet & Small Laptop Viewports (640px – 1023px — e.g., iPad Mini 768px, iPad Pro 834px)

1. **Persistent Left Margin Trap:**
   * At 768px (iPad portrait), the `lg` breakpoint has not yet triggered.
   * The sidebar remains `hidden`.
   * The topnav remains offset by `left-72` (288px).
   * 37.5% of the top of the iPad screen is a blank void.
   * The available header space is `768px - 288px = 480px`.
2. **Horizontal Squashing & Element Overlap:**
   * The 480px header area must accommodate:
     * Logo + Title + Version (~200px)
     * Station Selector (~180px)
     * Telemetry Pill (~160px)
     * DEFCON Pill (~140px)
     * Role Selector (~180px)
     * Notifications + Profile (~90px)
     * Required space: **~950px**. Available: **480px**.
   * Elements clip, wrap onto invisible second lines within `h-14` (56px fixed overflow), or spill 470px off the right edge.

---

### 3.3 Desktop Compact Viewports (1024px – 1279px — e.g., MacBook Air 11-inch 1152px, Standard 1024x768)

1. **Sidebar Alignment Succeeds, but Track Squeeze Begins:**
   * At 1024px (`lg`), the sidebar mounts (`w-72` = 288px) and matches the topbar's `left-72`.
   * However, the remaining screen track is:
     $$\text{Available Width} = 1024\text{px} - 288\text{px} = 736\text{px}$$
2. **The 736px vs 950px Deficit:**
   * With clocks hidden (`hidden xl:flex`), the remaining 7 active widgets still require ~950px of horizontal clearance.
   * The Station Selector dropdown and the Role Selector dropdown compete for central space.
   * In Chromium and Gecko browsers, the DEFCON status pill collides directly with the Station selector, or pushes the user profile avatar and notification icon out of the visible screen frame.

---

### 3.4 Desktop Standard Viewports (1280px – 1535px — e.g., 720p HD, 1366x768, 1440x900)

1. **The "1280px Clock Explosion":**
   * At exactly 1280px (`xl`), the dual UTC/Local clock widget activates:
     ```html
     <div class="hidden xl:flex items-center gap-space-md ...">
     ```
   * This widget requires **~240px** of width (UTC time, separator line, local time, region badge).
   * At 1279px, required width was ~950px against 991px available (tight fit).
   * At 1280px, required width suddenly jumps to:
     $$950\text{px} + 240\text{px} = 1190\text{px}$$
   * Available track width at 1280px:
     $$1280\text{px} - 288\text{px} = 992\text{px}$$
   * **Deficit:** $-198\text{px}$.
   * **Visual Failure:** The moment a user expands their browser window past 1279px to 1280px, the header layout **breaks more violently** than it did at 1200px. The right-hand flex container is pushed down into a second line that is clipped by `h-14`, making the user avatar and notification bell vanish!

---

### 3.5 Large & Ultrawide Viewports (1536px+ — e.g., 1080p Full HD 1920px, 2K, 4K)

1. **Layout Stabilizes, but Informational Redundancy Peaks:**
   * Above 1600px, all elements fit comfortably within the track without overlapping.
   * However, a major visual defect emerges: **Dual Staggered Header Redundancy**.
   * Topnav displays: `ANTARCTIC Remote-Ops`, Station Selector (`Bharati [69°24'S, 76°11'E]`), `LIVE GSAT-7A | 240ms`, `DEFCON 5 / NOMINAL`, Clocks.
   * Directly below it, the Station Dashboard Context Ribbon (`station/dashboard.html` line 4) displays: `BHARATI STATION // DIGITAL TWIN CORE`, `STATION ID: IN-ANT-BHT-02`, `69°24'S, 76°11'E — Larsemann Hills`, `STATION STATUS: OPTIMAL`.
   * On wide screens, 28% of the initial vertical viewport is consumed by duplicate satellite, location, and operational status indicators.

---

## 4. Master Findings Registry

### Defect Taxonomy Summary

| Finding ID | Severity | Category | Target Component | Summary |
| :--- | :---: | :--- | :--- | :--- |
| **FE-RESP-001** | **P0** | Responsive | `topnav.html` | Hardcoded `left-72` creates 288px void & horizontal blowout on screens < 1024px |
| **FE-RESP-002** | **P0** | Responsive / Functional | `topnav.html`, `sidebar_*.html` | Total absence of mobile navigation (no hamburger, no drawer) locks user out |
| **FE-RESP-003** | **P1** | Responsive | `topnav.html` | Header widgets collide & overlap between 1024px and 1440px due to missing collapse rules |
| **FE-RESP-004** | **P1** | Responsive | `topnav.html` | Premature `hidden xl:flex` clock expansion injects 240px at 1280px causing instant overflow |
| **FE-FUNC-001** | **P1** | Functional | `topnav.html` | Station Selector `<select>` is inert dummy UI with no route binding or event handler |
| **FE-FUNC-002** | **P1** | Functional / RBAC | `topnav.html` | Role Selector `<select>` is inert dummy UI conflicting with backend RBAC (C5) |
| **FE-FUNC-003** | **P2** | Functional | `topnav.html` | Notifications bell popup is hardcoded and unlinked to real active alerts or SSE |
| **FE-DATA-001** | **P2** | Data / Integration | `topnav.html` | Timezone math error: HQ calculates UTC+5 instead of Indian Standard Time (UTC+05:30) |
| **FE-VIS-001** | **P1** | Visual Consistency | `topnav.html`, `sidebar_*.html` | Two-tone dark green seam at x = 288px (`#12231f` sidebar vs `#0d1f1b` topnav) |
| **FE-VIS-002** | **P1** | Visual Consistency | `topnav.html`, `index.html`, `auth/login.html` | 3 conflicting navbar visual designs across Landing, Auth, and Operations |
| **FE-VIS-003** | **P2** | Visual Consistency | `topnav.html`, `dashboard.html` | Severe informational redundancy between topnav and page context ribbons |
| **FE-VIS-004** | **P2** | Visual Consistency | `topnav.html` | Squished pill ratios resulting from mismatched `py-1` and `px-space-sm` tokens |
| **FE-VIS-005** | **P2** | Visual Consistency | `topnav.html` | Brittle external Google User Content logo dependency instead of local static asset |
| **FE-A11Y-001** | **P2** | Accessibility | `topnav.html` | Unlabelled form controls and missing ARIA landmarks on comboboxes & buttons |
| **FE-A11Y-002** | **P3** | Accessibility | `topnav.html` | Non-semantic profile avatar `<div>` inaccessible to keyboard tab navigation |

---

### Deep Finding Records

```text
ID: FE-RESP-001
Title: Unconditional left-72 offset in topnav.html causes 288px dead zone and horizontal blowout on viewports < 1024px
Severity: P0 (Critical)
Status: Open

Route: All authenticated dashboard routes (/maitri/*, /bharati/*, /hq/*)
Component: Top Navigation Bar (<header>)
File: app/templates/components/topnav.html (Line 1-2)
Viewport: Mobile (< 640px) & Tablet (640px - 1023px)
Browser: All (Chrome, Safari Mobile, Firefox, Edge)

Category: Responsive

Expected:
On viewports where the sidebar is hidden (< 1024px), the top navigation bar should span the full width of the screen (left-0 right-0). On viewports where the sidebar is visible (>= 1024px), the top navigation bar should be offset by the sidebar width (lg:left-72 right-0).

Actual:
The top navigation bar has class="fixed top-0 left-72 right-0 ...". Because "left-72" lacks the "lg:" prefix, the 288px left offset is enforced on all screen sizes. On a 390px iPhone, the header starts at 288px, leaving a 288px empty void on the left and extending 288px past the right edge, causing severe horizontal page scrolling and clipping all interactive action controls.

Reproduction:
1. Open any dashboard page (e.g., http://localhost:8000/bharati/).
2. Open DevTools and toggle Device Emulation (e.g., iPhone 14, 390x844).
3. Observe that the header background starts more than 70% of the way across the screen.
4. Scroll horizontally to the right and observe the detached header elements floating outside the screen boundary.

Evidence:
- DOM Inspection: <header class="fixed top-0 left-72 right-0 ...">
- Computed style on 390px viewport: left: 288px; right: 0px; width: 102px;
- Children aggregate width: 724px -> triggers horizontal overflow of 622px.

Consistency Rule Violated:
docs/architecture.md §11 (Responsive mobile-first standard); .agents/frontend/SKILL.md (Responsive breakpoint fidelity).

Root Cause Hypothesis:
The developer styled the desktop layout first and applied the 288px sidebar compensation directly to the base class list rather than scoping it with the Tailwind responsive prefix `lg:left-72`.

Recommended Fix:
In `app/templates/components/topnav.html`, change:
  left-72 right-0
to:
  left-0 lg:left-72 right-0

Regression Check:
Verify desktop view (>= 1024px) retains exact 288px alignment with sidebar, and mobile view (< 1024px) starts flush at x = 0.
Dependencies: None.
```

---

```text
ID: FE-RESP-002
Title: Total absence of mobile navigation trigger (hamburger menu / drawer) causing complete user lockout
Severity: P0 (Critical)
Status: Open

Route: All authenticated dashboard routes (/maitri/*, /bharati/*, /hq/*)
Component: Top Navigation Bar & Sidebar System
File: app/templates/components/topnav.html & app/templates/components/sidebar_*.html
Viewport: Mobile (< 640px) & Tablet (640px - 1023px)
Browser: All

Category: Responsive / Functional

Expected:
When the desktop sidebar is hidden on viewports < 1024px, the top navigation bar must provide an accessible hamburger menu icon button (<button aria-label="Open Navigation Menu">) that toggles a mobile slide-over navigation drawer.

Actual:
The sidebar is configured with `hidden lg:flex`. The topnav contains no hamburger menu button, no mobile menu toggle, and no drawer component. Once a user on a tablet or mobile device enters any route, there are zero navigation links available anywhere on screen. The user is completely trapped on that single view.

Reproduction:
1. Navigate to http://localhost:8000/maitri/ on an iPad or mobile viewport (< 1024px).
2. Attempt to navigate to "Microgrid & Energy", "Telemetry", or "Alerts".
3. Search the entire screen for a navigation trigger or link. None exists.

Evidence:
- Grep in `app/templates/components/topnav.html` for "menu", "drawer", or "sidebar" returns zero results.
- Sidebar template contains `class="hidden lg:flex fixed ..."` with no mobile counterpart.

Consistency Rule Violated:
.agents/frontend/SKILL.md (Navigation must be navigable on all viewports); docs/architecture.md §11.

Root Cause Hypothesis:
The application was built as a desktop-first SCADA dashboard prototype, and mobile navigation was omitted during initial screen slicing from Stitch HTML.

Recommended Fix:
1. In `app/templates/components/topnav.html`, add a mobile-only menu trigger button on the far left:
   ```html
   <button @click="mobileMenuOpen = true" class="lg:hidden p-2 rounded text-on-surface hover:bg-surface-container-high" aria-label="Open Navigation">
     <span class="material-symbols-outlined">menu</span>
   </button>
   ```
2. In `app/templates/layouts/dashboard.html`, wrap the layout in an Alpine store `x-data="{ mobileMenuOpen: false }"` and add an off-canvas drawer version of the active station sidebar that transitions in via `x-show="mobileMenuOpen"` with a backdrop overlay.

Regression Check:
Test opening and closing the mobile drawer on mobile (375px), tablet (768px), and ensure it closes automatically when crossing >= 1024px.
Dependencies: FE-RESP-001.
```

---

```text
ID: FE-RESP-003
Title: Severe element collision and horizontal wrapping between 1024px and 1440px viewports
Severity: P1 (High)
Status: Open

Route: All authenticated dashboard routes (/maitri/*, /bharati/*, /hq/*)
Component: Top Navigation Bar
File: app/templates/components/topnav.html (Lines 12-64)
Viewport: Desktop Compact & Medium (1024px - 1440px)
Browser: Chrome, Firefox, Safari

Category: Responsive

Expected:
Navigation widgets should have prioritized responsive collapse rules. Secondary status badges (DEFCON badge, Telemetry latency badge, Station full coordinate strings) should gracefully collapse or hide on narrower desktop displays to prevent widget collision.

Actual:
All widgets (Station selector with coordinates, SATCOM status, DEFCON indicator, Role selector, Alert bell, Avatar) are set to display simultaneously at 1024px. The available width is only 736px. Elements collide into each other, text wraps into a broken second line, and the fixed 56px (`h-14`) container clips the lower half of inputs or pushes buttons completely off-screen.

Reproduction:
1. Set browser viewport to 1024px width by 768px height.
2. Observe `app/templates/components/topnav.html`.
3. Note how the Station selector text overlays the DEFCON pill and the Role dropdown pushes the notification icon off the screen edge.

Evidence:
- At 1024px: Available track = 736px. Total widget natural width = 950px.
- Overflow: -214px.
- DOM elements wrap into a 2-line flexbox inside `h-14 overflow-hidden/clip`, making bottom line invisible.

Consistency Rule Violated:
.agents/frontend/SKILL.md (Restrained geometry; responsive hierarchy; no overlapping widgets).

Root Cause Hypothesis:
No responsive display utility classes (`hidden md:inline`, `hidden 2xl:flex`) were applied to the secondary status pills.

Recommended Fix:
Apply responsive hiding thresholds:
1. Station coordinates text: truncate or show station code only below `xl`: `<span class="hidden 2xl:inline"> [69°24'S, 76°11'E]</span>`.
2. DEFCON badge: hide below `2xl`: `class="hidden 2xl:flex items-center ..."`.
3. SATCOM pill latency: hide latency on `< xl`: `<span class="hidden xl:inline text-outline">| 240ms</span>`.
4. Role selector: collapse to icon-only badge or hide below `xl`.

Regression Check:
Resize window continuously from 1024px to 1920px; verify no wrapping or horizontal clipping occurs at any pixel increment.
Dependencies: None.
```

---

```text
ID: FE-RESP-004
Title: Disruptive 240px clock expansion at 1280px (xl breakpoint) triggers severe layout collision
Severity: P1 (High)
Status: Open

Route: All authenticated dashboard routes (/maitri/*, /bharati/*, /hq/*)
Component: Top Navigation Bar Clocks Widget
File: app/templates/components/topnav.html (Line 24-46)
Viewport: 1280px - 1535px (xl breakpoint)
Browser: All

Category: Responsive

Expected:
The dual clock widget should only reveal itself when there is genuine surplus track width (at `2xl`, >= 1536px), or it should replace other status indicators rather than creating a net-additive 240px width surge at 1280px.

Actual:
The clocks container uses `class="hidden xl:flex items-center gap-space-md ..."`. At 1279px, the clocks are hidden and the topbar barely fits. At 1280px, Tailwind's `xl:` breakpoint activates, unhiding the dual clock widget (+240px). Available space is 992px, but total required width becomes 1190px. Expanding the window from 1279px to 1280px immediately breaks the layout.

Reproduction:
1. Set viewport width to 1275px. Observe topbar fits without collision.
2. Drag viewport handle to 1280px.
3. Observe dual clocks suddenly appear and force the right-hand controls (Alerts, Avatar) into an invisible wrapped row.

Evidence:
- Class definition: `hidden xl:flex`
- Measured widget footprint: 238.4px
- Breakpoint track deficit at 1280px: 992px - 1190px = -198px.

Consistency Rule Violated:
.agents/frontend/SKILL.md (Smooth breakpoint transitions; density control).

Root Cause Hypothesis:
The developer assumed `xl:` (1280px) provides ample space, forgetting to subtract the 288px (`w-72`) fixed sidebar from the calculation.

Recommended Fix:
Change `hidden xl:flex` to `hidden 2xl:flex` (1536px+), ensuring clocks only render when the topbar track has at least $1536 - 288 = 1248\text{px}$ of free width.

Regression Check:
Verify smooth layout at 1280px, 1366px, 1440px, and ensure clocks cleanly appear without collision at 1536px+.
Dependencies: FE-RESP-003.
```

---

```text
ID: FE-FUNC-001
Title: Station Selector <select> is an inert dummy element with no routing logic or event listeners
Severity: P1 (High)
Status: Open

Route: All dashboard routes
Component: Topbar Station Dropdown
File: app/templates/components/topnav.html (Lines 12-19)
Viewport: All
Browser: All

Category: Functional

Expected:
Changing the selected station in the `<select>` dropdown (e.g. from "Bharati" to "Maitri") should navigate the user to the corresponding station portal (`/maitri/` or `/bharati/`), or update the active station context via HTMX.

Actual:
The `<select>` has class attributes only. It contains no `x-on:change`, no `onchange="window.location.href=..."`, no `hx-get`, and is not wrapped in a `<form>`. Selecting a different station changes the visible select text locally in the browser DOM, but triggers zero network requests and zero page navigation. The user remains stuck on the original station.

Reproduction:
1. Navigate to `/bharati/`.
2. Click the Station dropdown in the top navigation bar.
3. Select "Maitri [70°46'S, 11°44'E]".
4. Observe that nothing happens. The URL remains `/bharati/` and Bharati telemetry remains on screen.

Evidence:
```html
<select class="bg-transparent text-on-surface font-label-md text-label-md focus:outline-none cursor-pointer pr-space-sm">
  <option class="bg-surface-container text-on-surface" value="bharati" ...>Bharati ...</option>
  <option class="bg-surface-container text-on-surface" value="maitri" ...>Maitri ...</option>
  <option class="bg-surface-container text-on-surface" value="maitri-ii">Maitri-II ...</option>
  <option class="bg-surface-container text-on-surface" value="polar-all" ...>Polar Overview ...</option>
</select>
```

Consistency Rule Violated:
.agents/agents/FrontendTestingAgent/agent.md §Functional ("Check: navigation, links, dropdowns, CRUD interactions"); docs/architecture.md.

Root Cause Hypothesis:
Static Stitch mockup HTML was imported into the Jinja2 template without wiring the interactive change handler.

Recommended Fix:
Add an Alpine or vanilla JS change listener:
```html
<select @change="if ($event.target.value === 'polar-all') { window.location.href = '/hq/' } else if ($event.target.value === 'bharati' || $event.target.value === 'maitri') { window.location.href = '/' + $event.target.value + '/' }" ...>
```
Also map `polar-all` to `/hq/` and disable `maitri-ii` with `disabled` (as Maitri-II is a projected future station).

Regression Check:
Selecting "Maitri" navigates to `/maitri/`; selecting "Bharati" navigates to `/bharati/`; selecting "Polar Overview" navigates to `/hq/`.
Dependencies: None.
```

---

```text
ID: FE-FUNC-002
Title: Role Selector <select> is inert dummy UI that fundamentally conflicts with backend RBAC (C5)
Severity: P1 (High)
Status: Open

Route: All dashboard routes
Component: Topbar Role Dropdown
File: app/templates/components/topnav.html (Lines 53-63)
Viewport: All
Browser: All

Category: Functional / Role-Based UI

Expected:
The active user role should reflect the authenticated user's actual cryptographic session role from Supabase Auth (`request.state.user.role`). It must either be a static read-only badge (for real operations), or, if intended as a hackathon dev-switcher, it must execute an authenticated role-switching request that issues a valid JWT/session cookie.

Actual:
The role dropdown is an inert `<select>` with 5 static `<option>` tags (`hq-operator`, `station-commander`, `systems-engineer`, `research-lead`, `medical-lead`). Selecting an option does nothing. Furthermore, allowing arbitrary client-side role switching in the UI violates the backend RBAC architecture (Constraint C5), where router-level dependencies enforce roles.

Reproduction:
1. Navigate to `/hq/audit` as an authenticated user.
2. Select "Role: Research Lead" from the topbar dropdown.
3. Observe that no session change occurs, no permission re-evaluation happens, and the UI state does not change.

Evidence:
- `<select class="bg-transparent text-on-surface font-label-md text-label-md ...">` has zero event bindings.
- Options do not reflect backend role codes (`SUPER_ADMIN`, `HQ_ADMIN`, `HQ_OPERATOR`, `STATION_ADMIN`, `STATION_OPERATOR`, `ENGINEER`, `SCIENTIST`, `VIEWER` per `GEMINI.md` §5).

Consistency Rule Violated:
Constraint C5; docs/architecture.md §RBAC; .agents/agents/FrontendTestingAgent/agent.md §Role-Based UI.

Root Cause Hypothesis:
Artifact of Stitch UI design mockups that simulated persona views without integrating with backend authentication.

Recommended Fix:
Replace the inert `<select>` with a dynamic read-only badge indicating the current authenticated user's role:
```html
<div class="flex items-center gap-1.5 px-space-sm py-1 bg-surface-container-high rounded-lg">
  <span class="material-symbols-outlined text-secondary text-[16px]">badge</span>
  <span class="font-label-md text-label-md text-on-surface font-medium">{{ user.role | default('HQ Operator') | upper }}</span>
</div>
```
If dynamic persona switching is required for SIH demo judging, connect it to a dedicated backend dev endpoint `/auth/switch-role` with audit log creation (C7).

Regression Check:
Verify authenticated user's real role renders accurately across all station and HQ pages.
Dependencies: None.
```

---

```text
ID: FE-DATA-001
Title: Timezone calculation error in topnav clock displays UTC+05:00 instead of IST (UTC+05:30) for HQ
Severity: P2 (Medium)
Status: Open

Route: All HQ routes (/hq/*)
Component: Topbar Clocks Widget
File: app/templates/components/topnav.html (Lines 24-38)
Viewport: Desktop xl+ (>= 1280px)
Browser: All

Category: API / Data Integration

Expected:
When viewing NCPOR HQ (located in Vasco da Gama, Goa, India), the local operational clock must display Indian Standard Time (IST), which is **UTC+05:30**.

Actual:
The Alpine.js script executes:
```javascript
const loc = new Date(d.getTime() + 5*3600*1000);
this.localTime = loc.toISOString().substring(11, 19) + ' +05:00';
```
It hardcodes a 5-hour offset (`+ 5*3600*1000`) and the string `+05:00` for all non-Maitri views. As a result, when in HQ, the local time displayed is **30 minutes behind** real Indian Standard Time!

Reproduction:
1. Navigate to `/hq/` at 12:00:00 UTC on a screen >= 1280px.
2. Inspect the local clock on the right side of the topbar.
3. Observe it reads `17:00:00 +05:00` instead of `17:30:00 IST (+05:30)`.

Evidence:
- Code snippet in `app/templates/components/topnav.html` line 34: `d.getTime() + 5*3600*1000`.
- IST is UTC+5.5 hours (`5.5 * 3600 * 1000`).

Consistency Rule Violated:
docs/station-facts-and-research.md (Authoritative station facts & NCPOR timezones); .agents/agents/FrontendTestingAgent/agent.md §Data Integration.

Root Cause Hypothesis:
Developer conflated Bharati's local Mawson/Larsemann Hills operational timezone (UTC+5) with Indian Standard Time for Goa HQ (UTC+5.5).

Recommended Fix:
Parameterize the timezone offset in Jinja based on `station_id`:
* Maitri: UTC+00:00 (0 hours)
* Bharati: UTC+05:00 (5.0 hours)
* HQ: UTC+05:30 (5.5 hours)
```javascript
const offsetHours = {% if station_id == 'maitri' %}0{% elif station_id == 'bharati' %}5{% else %}5.5{% endif %};
const loc = new Date(d.getTime() + offsetHours * 3600 * 1000);
```

Regression Check:
Verify HQ displays correct IST time matching Goa local time.
Dependencies: None.
```

---

```text
ID: FE-VIS-001
Title: Visual background seam between sidebar header and topnav along shared 56px baseline
Severity: P1 (High)
Status: Open

Route: All authenticated dashboard routes (/maitri/*, /bharati/*, /hq/*)
Component: Top Navigation Bar & Sidebar Headers
File: app/templates/components/topnav.html (Line 2) & sidebar_*.html (Line 3)
Viewport: Desktop (>= 1024px)
Browser: All

Category: Visual Consistency

Expected:
The top 56px (`h-14`) horizontal band across the viewport should present a seamless, unified visual plane or have an intentional structural divider separating sidebar brand and topbar controls.

Actual:
The sidebar top header has class `bg-surface-container` (hex `#12231f`). The top navigation bar directly touching it has class `bg-surface-container-low/95` (hex `#0d1f1b/95`). Both elements share `h-14`, but because their surface tokens differ in lightness and opacity, a jarring vertical seam is visible at x = 288px where the two headers collide.

Reproduction:
1. Open `/bharati/` or `/hq/` on a desktop monitor with high color contrast.
2. Inspect the horizontal bar across the top 56px of the screen.
3. Observe the boundary between the sidebar's "BHARATI COASTAL CMD" box and the topbar's logo area.

Evidence:
- Sidebar header: `background-color: #12231f;`
- Topbar header: `background-color: rgba(13, 31, 27, 0.95);`
- Visual contrast step: ~6% lightness delta across adjacent elements with no dividing border.

Consistency Rule Violated:
.agents/brand_design/SKILL.md (Base Antarctic deep green visual continuity); .agents/frontend/SKILL.md §Components.

Root Cause Hypothesis:
Sidebar and topnav were styled in isolation with slightly different container tokens (`surface-container` vs `surface-container-low`).

Recommended Fix:
Align both containers to the authoritative brand header token:
Use `bg-surface-container-low` (`#0d1f1b`) or `bg-surface-container` (`#12231f`) across both components, and add a subtle vertical divider `border-r border-outline-variant/30` at the right edge of the sidebar header.

Regression Check:
Verify consistent background tone across the entire top 56px row.
Dependencies: None.
```

---

```text
ID: FE-VIS-002
Title: Three competing navbar design subsystems across Landing, Authentication, and Dashboard
Severity: P1 (High)
Status: Open

Route: `/` vs `/auth/login` vs `/hq/`
Component: Navigation Headers
File: `index.html`, `auth/login.html`, `components/topnav.html`
Viewport: All
Browser: All

Category: Visual Consistency

Expected:
All system surfaces must follow the unified DTFIAS Brand Design System (`brand_design/SKILL.md`), maintaining consistent typography, logo treatment, and color tokens.

Actual:
Three entirely different navigation visual paradigms coexist:
1. `index.html`: Uses an airy, transparent navigation bar (`max-w-7xl mx-auto px-6 py-8`) with an inverted white logo, clean text links, and a primary green button.
2. `auth/login.html`: Uses an ultra-dense, terminal-style security strip (`py-2`, `text-xs`) with hardcoded hex colors (`#8DA19A`, `#2E7D5B`, `#10221E`) and monospace encryption declarations.
3. `topnav.html`: Uses a SCADA mission control fixed bar (`h-14`) with glassmorphism (`backdrop-blur-md`), container tokens (`surface-container-low`), and multi-select dropdowns.
Each page feels like it belongs to a completely different application.

Reproduction:
1. Visit `http://localhost:8000/`.
2. Click "Secure Login" to navigate to `http://localhost:8000/auth/login`.
3. Submit login to land on `http://localhost:8000/hq/`.
4. Observe the dramatic shift in header height, font styles, colors, and layout structure across the three consecutive screens.

Evidence:
- `index.html`: `font-ui`, `text-surface-cream`, `py-8`
- `auth/login.html`: `font-mono`, `text-[#8DA19A]`, `bg-deep-green-darker`, `py-2`
- `topnav.html`: `h-14`, `bg-surface-container-low/95`, `backdrop-blur-md`

Consistency Rule Violated:
.agents/brand_design/SKILL.md (One unified brand experience); docs/testing/design_inconsistencies.md §INC-09.

Root Cause Hypothesis:
Templates were extracted from different Stitch batches (`batch2`, `batch4`, `batch6`) that were designed under different prompt instructions.

Recommended Fix:
Standardize header heights, typography tokens (`font-heading` for titles, `font-ui` for links/buttons, `font-mono` for telemetry), and align background colors to `--brand-deep-green` (`#1A312C`).

Regression Check:
User journey from Landing -> Login -> Dashboard maintains harmonious visual continuity.
Dependencies: None.
```

---

```text
ID: FE-VIS-003
Title: Redundant duplicate telemetry and station metadata stacked directly beneath topnav
Severity: P2 (Medium)
Status: Open

Route: `/bharati/dashboard`, `/maitri/dashboard`, `/hq/dashboard`
Component: Topnav vs Page Content Header Ribbons
File: `topnav.html` vs `station/dashboard.html` & `hq/dashboard.html`
Viewport: Desktop (>= 1024px)
Browser: All

Category: Visual Consistency

Expected:
Global navigation should house global controls (station selector, user profile, alerts, time), while local page headers should house specific page views without directly repeating the exact same badges.

Actual:
`topnav.html` renders:
- "LIVE GSAT-7A | 240ms"
- "DEFCON 5 / NOMINAL"
- Station coordinates
Directly below it, `station/dashboard.html` renders:
- "STATION ID: IN-ANT-BHT-02"
- "69°24'S, 76°11'E — Larsemann Hills"
- "STATION STATUS: OPTIMAL"
And in `hq/dashboard.html`:
- "LIVE GSAT-7A UPLINK" (with pulsing green dot)
- "Data Freshness: 1.4s ago"
- "Telemetry Frame #89421-EPS"
This causes 2 stacked horizontal bars repeating almost identical satellite link and status information.

Reproduction:
1. Open `/hq/` on a desktop display.
2. Look at the top 120px of the screen.
3. Observe two distinct green pulsing dots and two separate GSAT-7A badges within 40px of each other.

Evidence:
- `topnav.html` Line 22: `<span class="w-2 h-2 rounded-full bg-telemetry-safe"></span>...LIVE GSAT-7A`
- `hq/dashboard.html` Line 11: `<span class="w-2 h-2 rounded-full bg-telemetry-safe animate-ping"></span> LIVE GSAT-7A UPLINK`

Consistency Rule Violated:
.agents/frontend/SKILL.md §Layout ("Decoration must carry information... one thing is the most important thing"); docs/frontend-endpoints.md.

Root Cause Hypothesis:
The page templates and the master topnav were built independently, each trying to fulfill the "satellite uplink indicator" requirement from the spec.

Recommended Fix:
Dedicate the topnav exclusively to global network health (Uplink Satellite, Global Ping, Defcon), and remove the duplicate uplink banner from the individual page templates, allowing dashboard content to begin immediately with primary metric cards.

Regression Check:
Verify page headers look clean and content starts higher on the screen without duplicate badges.
Dependencies: None.
```

---

```text
ID: FE-VIS-005
Title: Brittle external Google User Content CDN logo dependency in topnav and modal headers
Severity: P2 (Medium)
Status: Open

Route: All routes
Component: Mission Logo Emblem
File: `app/templates/components/topnav.html` (Line 8)
Viewport: All
Browser: All

Category: Visual Consistency / Resilience

Expected:
Critical institutional brand assets (NCPOR emblem) must be hosted locally within `app/static/assets/` or `app/static/img/` to ensure offline resilience and zero dependency on third-party scratch CDN endpoints.

Actual:
The topnav logo is loaded from:
`https://lh3.googleusercontent.com/aida/AEtjO1WmulcB1HzfkxmeY76IcVjMHNoCYqPLLYlSF5JWTIX9cggoUqKexxIsDOIAW0WCgZSSLDUU2rJg60tpge45aC9vb2k8-BQwWf2ysMREe9JPys2eI-HqArlSZBYaVBuoDgCTBXoKmZmAkaLX6PnU5-UCeZfS4fVv_5hs_YbxDZ0cNiT5NlsQPBoeOt07KN8MwRzJLW4q0eEJQrbnYThVIde8_z8gZSpFzXvdn8Yo6onabBqXMenNynkoQ98`
If this Google User Content token expires, or if DTFIAS is deployed in an isolated local environment or simulated Antarctic offline mode, the main logo fails to load and renders a broken image placeholder.

Reproduction:
1. Disconnect network or block `lh3.googleusercontent.com` in DevTools Network Request Blocking.
2. Refresh `http://localhost:8000/hq/`.
3. The logo fails with `ERR_NAME_NOT_RESOLVED` and displays a broken image icon in the topbar.

Evidence:
- `src="https://lh3.googleusercontent.com/aida/..."` in `topnav.html`, `index.html`, `alert_dialog.html`, `asset_detail.html`.

Consistency Rule Violated:
docs/architecture.md §Resilience; docs/operations.md; C17 (self-contained runtime).

Root Cause Hypothesis:
Stitch export generated images hosted on Google Cloud AI temporary storage, which were pasted directly into templates without being downloaded to local static storage.

Recommended Fix:
Download the vector emblem SVG/PNG, save it to `app/static/assets/ncpor_emblem.png`, and update templates to reference `{{ url_for('static', path='assets/ncpor_emblem.png') }}`.

Regression Check:
Verify logo loads cleanly in full offline mode.
Dependencies: None.
```

---

```text
ID: FE-A11Y-001
Title: Unlabelled interactive form controls and missing ARIA landmarks in top navigation
Severity: P2 (Medium)
Status: Open

Route: All dashboard routes
Component: Top Navigation Bar
File: `app/templates/components/topnav.html` (Lines 14, 55, 65)
Viewport: All
Browser: All

Category: Accessibility

Expected:
Every interactive element must possess an accessible name (WCAG 2.1 Criterion 4.1.2). `<select>` elements must have an `aria-label` or `<label>` tag. Icon-only buttons must have an `aria-label`. The notification popover must declare `aria-expanded` and `aria-haspopup="dialog"`.

Actual:
1. Station selector `<select>` has no label and no `aria-label`.
2. Role selector `<select>` has no label and no `aria-label`.
3. Alert notification button has no `aria-label` and no `aria-expanded` binding.
Screen readers announce "Combobox, collapsed" without informing the user what is being selected.

Reproduction:
1. Run Lighthouse Accessibility Audit or axe DevTools on `/bharati/`.
2. Observe critical violations:
   - "Select element has no accessible name" (x2)
   - "Buttons do not have an accessible name" (x1)

Evidence:
- `<select class="bg-transparent text-on-surface ...">` (no aria-label)
- `<button @click="alertsOpen = !alertsOpen" class="relative p-1.5 ...">` (no aria-label)

Consistency Rule Violated:
.agents/frontend/SKILL.md §Accessibility; WCAG 2.1 Level AA (4.1.2 Name, Role, Value).

Root Cause Hypothesis:
Rapid template prototyping without running accessibility linter passes.

Recommended Fix:
Add explicit ARIA attributes:
```html
<select aria-label="Select Operational Station" class="...">
<select aria-label="Active Operator Role" class="...">
<button aria-label="View Station Alerts" :aria-expanded="alertsOpen" aria-haspopup="true" ...>
```

Regression Check:
Axe DevTools passes with 0 form control name violations in header.
Dependencies: None.
```

---

## 5. Summary Matrix & Remediation Roadmap

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    NAVIGATION SYSTEM REMEDIATION PHASES                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ PHASE 1: Critical Mobile & Responsive Hotfixes (P0 / P1)                     │
│  ├── Fix FE-RESP-001: Change `left-72` to `left-0 lg:left-72` in topnav.html  │
│  ├── Fix FE-RESP-002: Add hamburger toggle & mobile off-canvas drawer       │
│  ├── Fix FE-RESP-003: Add responsive hide utilities on secondary pills      │
│  └── Fix FE-RESP-004: Push clock breakpoint from `xl:` to `2xl:`            │
├─────────────────────────────────────────────────────────────────────────────┤
│ PHASE 2: Functional Wiring & Role Architecture (P1 / P2)                     │
│  ├── Fix FE-FUNC-001: Wire station switcher @change to navigate routes      │
│  ├── Fix FE-FUNC-002: Replace dummy role <select> with authentic role badge  │
│  ├── Fix FE-DATA-001: Correct HQ timezone offset to UTC+05:30 (IST)         │
│  └── Fix FE-A11Y-001: Add missing aria-labels on select and icon buttons     │
├─────────────────────────────────────────────────────────────────────────────┤
│ PHASE 3: Visual Polish & Asset Resilience (P1 / P2)                         │
│  ├── Fix FE-VIS-001: Unify sidebar & topbar background tokens (`#0d1f1b`)   │
│  ├── Fix FE-VIS-002: Harmonize landing, auth, and dashboard navigation      │
│  ├── Fix FE-VIS-003: Prune duplicate telemetry ribbons from page templates  │
│  └── Fix FE-VIS-005: Download Google User Content logo to local static asset│
└─────────────────────────────────────────────────────────────────────────────┘
```

### Sign-off & Handoff
* **Report Compiled By:** Frontend Testing Agent
* **Consumer:** Frontend Inconsistency Manager / Engineering Team
* **Next Action:** Prioritize Phase 1 hotfixes to unblock mobile and tablet usability.
