# DTFIAS --- Frontend Endpoints, Stitch Prompts & Design System

## Purpose

This is the **frontend source of truth** for DTFIAS, the Digital Twin for Indian Antarctic Stations remote-operations platform. Use it to generate screens in Stitch and keep the frontend implementation consistent.

The visual concept is **scientific mission control + Antarctic operations + 2D/2.5D digital twin**. The station illustration is a spatial interface to operational data, not decorative artwork.

Project context: Maitri, Bharati, future expandable stations, and NCPOR HQ (National Centre for Polar and Ocean Research, Goa). The station reference material identifies Maitri as a research/logistics hub (Schirmacher Oasis), Bharati as a high-technology research station (Larsemann Hills), Maitri-II as a planned next-generation station with automated monitoring, and NCPOR HQ as the central operational authority.


# Frontend Endpoints & Stitch Screen Mapping

This document categorizes all UI screens downloaded from the Stitch project and maps them to their target FastAPI endpoints. This serves as the blueprint for integrating the frontend designs into the server-rendered Jinja2 architecture.

## 1. Authentication & Base
| Stitch Screen File | Original Name | Target FastAPI Endpoint | Description |
|--------------------|---------------|-------------------------|-------------|
| `screen2.html` | DTFIAS Secure Institutional Login Gateway | `/auth/login` | Main RBAC login screen. |
| `screen3.html` | Institutional Password Recovery Screen | `/auth/recover` | Password recovery/reset view. |

## 2. HQ / Continental Command Center (`/hq`)
| Stitch Screen File | Original Name | Target FastAPI Endpoint | Description |
|--------------------|---------------|-------------------------|-------------|
| `batch2_screen1.html` | NCPOR POLAR CMD / Antarctica Overview | `/hq` | Primary Dashboard for Continental Command. |
| `batch4_screen8.html` | Cross-Station Environmental & Geospatial | `/hq/environment` | Continental weather and climate tracking. |
| `batch4_screen5.html` | Continental Logistics, Convoy Tracking | `/hq/logistics` | Resupply and inter-station convoy logistics. |
| `batch4_screen6.html` | Cross-Station Microgrid Operations | `/hq/energy` | High-level energy overview across all stations. |
| `batch6_screen1.html` | Mission Operations & Madrid Protocol | `/hq/compliance` | Environmental compliance reporting. |
| `batch6_screen2.html` | Digital Twin Asset Registry | `/hq/stations` or `/hq/assets` | Global asset binding and tracking. |
| `batch6_screen3.html` | Cryptographic Audit Stream & FIPS 140-3 | `/hq/audit` | Global security and audit log ledger. |
| `batch6_screen4.html` | RBAC Governance & Permission Matrix | `/hq/users` | Multi-station user management. |
| `batch5_screen2.html` | Central Polar Telemetry Command | `/hq/telemetry` | Raw telemetry streams and global comms. |
| `batch5_screen1.html` | Emergency & Incident Protocol Control | `/hq/alerts` | Global alert triage and crisis management. |

## 3. Station Modules (Reusable for `/bharati` and `/maitri`)
*These screens define the subsystem views for a specific station. They will be integrated as Jinja2 templates that dynamically render Bharati or Maitri data based on the route.*

| Stitch Screen File | Original Name | Target FastAPI Endpoint | Description |
|--------------------|---------------|-------------------------|-------------|
| `batch4_screen1.html` | Bharati Station — Digital Twin Overview | `/{station_id}` | Main Station Dashboard. |
| `batch4_screen2.html` | 2D Isometric Digital Twin & Telemetry | `/{station_id}/twin` | 2.5D visual interactive map (SVG twin). |
| `batch2_screen3.html` | Station Digital Twin — 2D/Isometric | `/{station_id}/twin` | Alternate variant of the 2D digital twin. |
| `batch4_screen7.html` | Station Energy & Microgrid Operations | `/{station_id}/energy` | Station-specific energy monitoring. |
| `batch2_screen2.html` | Microgrid & Combined Heat/Power | `/{station_id}/energy` | Variant layout for energy distribution. |
| `batch5_screen3.html` | Habitat & Life Support | `/{station_id}/infrastructure`| HVAC, water, and structural integrity. |
| `batch5_screen4.html` | Environmental & Geospatial Sensor Analytics | `/{station_id}/environment`| Local weather and sensor readings. |
| `batch2_screen4.html` | Personnel Roster & Medical Readiness | `/{station_id}/logistics`| Station personnel and health tracking. |
| `batch4_screen9.html` | Station Alert Management | `/{station_id}/alerts` | Local station-level alert triage. |

## 4. Deep-Dive Components & Modals
| Stitch Screen File | Original Name | Target FastAPI Endpoint | Description |
|--------------------|---------------|-------------------------|-------------|
| `batch4_screen3.html` | Telemetry Console — CHP Generator #03 | HTMX Modal / Detail | Live view of a specific energy asset. |
| `batch4_screen4.html` | Physical Asset Detail — CHP Generator #03 | HTMX Modal / Detail | Specs and maintenance history of an asset. |

## Integration Strategy (Tailwind + Jinja2)
1. **Layout Inheritance**: A unified `tailwind.config` derived from these screens will be embedded in `app/templates/layouts/base.html`.
2. **Alpine Interactivity**: All sidebars, tabs, and dropdowns extracted from Stitch HTML will be wired with `x-data` and `x-show`.
3. **HTMX Navigation**: Main content areas will be swapped using HTMX (`hx-get`, `hx-target`) for SPA-like performance without a full JS framework.


------------------------------------------------------------------------

# 1. Master Design Language

## Product character

DTFIAS must feel:

-   Scientific
-   Operational
-   Institutional
-   Calm
-   Precise
-   Antarctic
-   Secure
-   Modern

It must **not** feel like:

-   generic SaaS
-   crypto/cyberpunk
-   gaming UI
-   consumer social software
-   excessive glassmorphism
-   neon dashboard
-   decorative 3D showcase

Use restrained geometry, strong hierarchy, compact technical data,
expanded premium whitespace (layout spacing has been globally increased by 30% to reduce congestion) and subtle hardware-accelerated core animations for interactive elements.

## Layout & Animation Standard

To maintain the premium minimalistic aesthetic:
- **Spacing**: Do not tightly pack UI elements. Always use the globally enhanced Tailwind `space-*` and `panel-gutter` tokens which are pre-scaled for premium breathing room.
- **Animation**: Do not use layout-thrashing animations. A global CSS rule sets a 0.25s ease-in-out transition for `opacity` and `transform` on interactive elements (buttons, inputs, cards, hotspots).

## Typography

The DTFIAS typography stack uses a structured 4-font hierarchy matching `.agents/brand_design/SKILL.md`:

| Font | Role | CSS Variable | Usage |
|------|------|-------------|-------|
| **Playfair Display** | Headings / Display | `--font-heading` | Page titles, hero banners, section headings, dashboard titles |
| **Playfair** | Body / Editorial | `--font-body` | Narrative copy, station mission summaries, callouts, descriptions |
| **Inter** | UI Chrome | `--font-ui` | Navigation, buttons, labels, form controls, tables, modal actions |
| **JetBrains Mono** | Monospace / Data | `--font-mono` | Sensor telemetry values, timestamps, GPS coordinates, asset codes |

Suggested scale:

| Element | Size | Target Font |
|---------|------|-------------|
| Hero / Display | 48–64 px | Playfair Display (700) |
| Page Title | 32–40 px | Playfair Display (600–700) |
| Section Title | 22–28 px | Playfair Display (600) |
| Card Title | 16–18 px | Inter (600) / Playfair Display |
| Body Text | 14–16 px | Playfair (400–500) |
| UI Chrome / Label | 12–14 px | Inter (400–600) |
| KPI Headline | 28–40 px | Inter (700) / Playfair Display |
| Telemetry / Code | 12–14 px | JetBrains Mono (500) |

Weights: 400, 500, 600, 700.

------------------------------------------------------------------------

# 2. Master Colour Palette

## Brand Base Palette

| Token | Hex | CSS Variable | Use |
|-------|-----|--------------|-----|
| Deep Green | `#1A312C` | `--brand-deep-green` | Headers, navigation, dark backgrounds, major headings, footer |
| Teal Green | `#428475` | `--brand-teal` | Buttons, active states, section accents, icons, highlights |
| Light Mint | `#C8E6D7` | `--brand-mint` | Background sections, info cards, hover states (`#E8F3EF` light tint) |
| Cream / Off-White | `#F5F2EB` | `--brand-cream` | Primary application background (`#F7F4ED` card surface) |
| Cream Dark / Border | `#E8E3D9` | `--brand-cream-dark` | Borders, dividers, subtle separators (`#D8E0DC`) |

## Light surfaces

  Token                   Hex
  ----------------------- -----------
  Primary text            `#20302C`
  Muted text              `#65736F`
  Border                  `#D8E0DC`
  Card                    `#FFFFFF`
  Dark surface            `#1A312C`
  Elevated dark surface   `#24423C`

## Dark surfaces

  Token          Hex
  -------------- -----------
  Background     `#10201D`
  Surface        `#1A312C`
  Elevated       `#24423C`
  Border         `#35544D`
  Primary text   `#F3F6F4`
  Muted text     `#B5C4BF`

------------------------------------------------------------------------

# 3. Semantic Status System

Semantic colors communicate state only.

## Normal --- Operational / Safe

Light surface:

-   Foreground: `#2E7D5B`
-   Background: `#E8F4EE`

Dark surface:

-   Foreground: `#63B88A`
-   Background: `rgba(99,184,138,0.12)`

Meaning: operating normally.

## Information --- General Update

Light:

-   Foreground: `#2878A8`
-   Background: `#E8F2F8`

Dark:

-   Foreground: `#5AA6D2`
-   Background: `rgba(90,166,210,0.12)`

Meaning: useful information; no immediate action.

## Attention --- Warning / Action May Be Required

Light:

-   Foreground: `#D9822B`
-   Background: `#FFF3E3`

Dark:

-   Foreground: `#F0A24A`
-   Background: `rgba(240,162,74,0.12)`

Meaning: abnormal condition requiring attention.

## Critical --- Emergency / Immediate Action

Light:

-   Foreground: `#C44536`
-   Background: `#FBE9E7`

Dark:

-   Foreground: `#E56B5D`
-   Background: `rgba(229,107,93,0.14)`

Meaning: serious problem requiring immediate action.

### Mandatory rule

**Do not use the same semantic foreground/background pair on every
surface.** Red and blue must adapt to light and dark backgrounds for
contrast. Semantic meaning remains constant while presentation changes.

Never rely on color alone. Pair color with text, icon or shape.

------------------------------------------------------------------------

# 4. Global Layout

Desktop is the primary operational experience.

``` text
┌───────────────────────────────────────────────────────────┐
│ HEADER                                                    │
├─────────────┬─────────────────────────────────────────────┤
│ SIDEBAR     │ MAIN CONTENT                                │
│             │                                             │
│ Overview    │                                             │
│ Stations    │                                             │
│ Twin        │                                             │
│ Environment │                                             │
│ Energy      │                                             │
│ Logistics   │                                             │
│ Personnel   │                                             │
│ Health      │                                             │
│ Research    │                                             │
│ Telemetry   │                                             │
│ Alerts      │                                             │
│ Simulation  │                                             │
│ Reports     │                                             │
│ Admin       │                                             │
└─────────────┴─────────────────────────────────────────────┘
```

Use 4--12px radii for controls/cards and 12--16px for large panels.
Avoid excessive pill-shaped UI.

------------------------------------------------------------------------

# 5. Frontend Browser Routes

## Public

``` text
/                  (Redirects to /hq/)
/auth/login
/auth/recover
```

## Station operations

``` text
/{station_id}/                     (Dashboard)
/{station_id}/twin                 (Digital Twin)
/{station_id}/environment          (Geospatial & Science)
/{station_id}/energy               (Microgrid)
/{station_id}/infrastructure       (Life Support)
/{station_id}/logistics            (Fuel & Supply)
/{station_id}/personnel            (Roster)
/{station_id}/health               (Medical Readiness)
/{station_id}/research             (Operations)
/{station_id}/telemetry            (Sensor Streams)
/{station_id}/alerts               (Local Triage)
/{station_id}/assets/:assetId
/{station_id}/assets/:assetId/telemetry
/{station_id}/assets/:assetId/history
```

## Global views (NCPOR HQ)

``` text
/hq/environment
/hq/energy
/hq/logistics
/hq/health
/hq/research
/hq/telemetry
/hq/alerts
/hq/simulations
/hq/reports
```

## Administration (NCPOR HQ)

``` text
/hq/stations
/hq/users
/hq/roles
/hq/assets
/hq/audit
/hq/settings
```

------------------------------------------------------------------------

# 6. Backend/API Endpoints Expected by the Frontend

These are API contracts, not browser routes.

``` text
GET  /api/stations
GET  /api/stations/:stationId
GET  /api/stations/:stationId/assets
GET  /api/stations/:stationId/environment
GET  /api/stations/:stationId/energy
GET  /api/stations/:stationId/logistics
GET  /api/stations/:stationId/personnel
GET  /api/stations/:stationId/health
GET  /api/stations/:stationId/research
GET  /api/stations/:stationId/telemetry
GET  /api/stations/:stationId/alerts
GET  /api/stations/:stationId/simulations

GET  /api/stations/:stationId/assets/:assetId
GET  /api/stations/:stationId/assets/:assetId/telemetry
GET  /api/stations/:stationId/assets/:assetId/history

GET  /api/environment
GET  /api/energy
GET  /api/logistics
GET  /api/personnel
GET  /api/health
GET  /api/research
GET  /api/telemetry
GET  /api/alerts
GET  /api/reports

GET  /api/admin/users
GET  /api/admin/roles
GET  /api/admin/stations
GET  /api/admin/assets
GET  /api/admin/audit
```

Mutating operations should be added according to the RBAC policy, for
example `POST`, `PATCH`, `DELETE`, acknowledge/resolve alert actions,
simulation execution and administration actions.

Frontend should call the FastAPI boundary rather than embedding
database/business logic in UI components.

------------------------------------------------------------------------

# 7. Shared UI Components

``` text
AppShell
TopHeader
Sidebar
Breadcrumbs
StationSelector
UserMenu

StatusBadge
OperationalIndicator
AlertBadge
Metric
KPI
DataTable
Timeline
FilterBar
DateRangeSelector

StationTwin
StationIllustration
Hotspot
Callout
ConnectorLine
TwinLayerSelector
AssetPanel

Chart
TimeSeriesChart
ComparisonChart
TelemetryTable

Modal
Drawer
Toast
ConfirmationDialog
LoadingState
EmptyState
ErrorState
OfflineState
```

------------------------------------------------------------------------

# 8. Digital Twin Design

Use a **2D/2.5D isometric scientific illustration**.

Do not require Blender, Three.js or WebGL for the first version.

Preferred pipeline:

``` text
Figma / illustration
       ↓
SVG
       ↓
HTML + SVG overlays
       ↓
interactive hotspots
       ↓
FastAPI data
```

Important station objects should have stable IDs:

``` text
maitri_main_building
maitri_power_plant_01
maitri_laboratory_01
maitri_medical_01
maitri_fuel_storage_01
maitri_water_system_01
maitri_waste_system_01
maitri_comms_01
```

The same concept should work for Bharati and future stations.

Hotspot behavior:

``` text
hover → highlight
click → select
select → open asset drawer/panel
```

Hotspot states:

``` text
● Operational
● Information
◉ Warning
◎ Critical
○ Offline
```

Use pulsing only for meaningful warnings/critical events.

------------------------------------------------------------------------

# 9. Route-by-Route Stitch Prompts

## `/` --- Landing

> Design the DTFIAS landing page, an institutional Antarctic
> remote-operations and digital-twin platform. Use Inter exclusively.
> Use Deep Green #1A312C, Teal Green #428475, Light Mint #E8F3EF and
> Warm Off-White #F7F4ED. Create a calm scientific hero titled "DTFIAS
> --- Antarctic Remote Operations & Digital Twin Platform". Show a
> refined 2D/isometric Antarctic visual connecting Maitri, Bharati and
> NCPOR HQ. Include mission, stations, environmental monitoring,
> infrastructure, logistics, personnel, digital twin and secure
> operations sections. Avoid stock-photo marketing, neon, excessive
> gradients, glassmorphism and generic SaaS patterns. Make it
> institutional, precise and production-quality.

## `/login`

> Design a secure institutional DTFIAS login screen. Use Deep Green
> #1A312C for the identity area, Warm Off-White #F7F4ED for the form
> area and Teal Green #428475 for interaction. Use Inter. Include email,
> password, sign-in, forgot password and authentication status. Use a
> subtle Antarctic station illustration. The screen should resemble
> secure mission-control software, not consumer SaaS. Use accessible
> focus states and restrained geometry.

## `/forgot-password`

> Design a minimal DTFIAS password-recovery screen using Inter, Warm
> Off-White #F7F4ED, Deep Green #1A312C and Teal Green #428475. Include
> email, recovery action, success state and return-to-login. Match the
> login design exactly.

## `/app/overview`

> Design the DTFIAS NCPOR command-center overview. This is the primary
> authenticated screen. Use a structured sidebar and compact header.
> Make an Antarctica operational map the dominant visual element,
> showing Maitri and Bharati with operational and communication states.
> Include concise KPIs for active stations, personnel, power, fuel,
> active alerts and data-link health. Add compact panels for alerts,
> energy, environment, logistics and recent telemetry. Use Warm
> Off-White #F7F4ED, Deep Green #1A312C and Teal Green #428475. Apply
> the complete light/dark semantic status system. Avoid card overload
> and generic SaaS styling.

## `/app/stations`

> Design the DTFIAS station directory for Maitri, Bharati and future
> stations. Treat stations as operational assets. Show location,
> operational status, personnel, power, fuel, communications, alerts and
> last synchronization. Use compact cards plus a comparison table.
> Include an authorized-only "Add Station" action. Make future station
> extensibility visually obvious. Use Inter and the exact DTFIAS
> palette.

## `/app/stations/:stationId`

> Design the individual station operational overview. Make a large
> 2D/isometric station illustration the primary visual object. Include
> interactive-looking hotspots for power, research, medical, water,
> waste, fuel, communications, environment and logistics. Surround it
> with concise KPIs for personnel, energy, fuel, environment,
> communications and alerts. Use the DTFIAS palette and semantic
> states. The illustration must feel like a digital twin, not
> decoration.

## `/app/stations/:stationId/digital-twin`

> Design the dedicated DTFIAS station digital-twin interface using a
> clean 2D/isometric scientific illustration. The station model is the
> dominant element. Add SVG/HTML hotspot markers and connector callouts
> for power infrastructure, laboratories, medical, water, waste, fuel,
> communications, environmental sensors, personnel and logistics. Hover
> highlights an object; click opens a side panel. Use restrained
> technical labels, Inter typography, Teal Green interaction accents and
> the complete semantic status system. Avoid fake cyberpunk 3D effects
> and excessive animation.

## `/app/stations/:stationId/assets/:assetId`

> Design an DTFIAS physical-asset detail screen. Show asset name,
> type, station, operational state, condition, maintenance state, linked
> sensors, key metrics, alerts and historical activity. Include a small
> visual reference to the selected station object. Prioritize readable
> engineering information over decorative cards. Use Inter and the
> established DTFIAS system.

## `/app/stations/:stationId/assets/:assetId/telemetry`

> Design the detailed telemetry view for one station asset. Show current
> readings, sensor health, communication state and high-quality
> time-series charts. Include metric and time-range selectors. Use
> compact engineering labels and units. Do not make every metric a card.
> Use semantic colors only for state.

## `/app/stations/:stationId/assets/:assetId/history`

> Design an asset history and maintenance timeline for DTFIAS. Show
> state changes, alerts, maintenance events, telemetry anomalies and
> important operational events chronologically. Use a dense but readable
> technical timeline with filters. Preserve the DTFIAS visual system.

## `/app/stations/:stationId/environment`

> Design the station environmental monitoring dashboard. Show
> temperature, wind, pressure, snow/environmental conditions, sensor
> health and historical trends. Include station context and time-range
> controls. Use scientific charts with clear units and restrained grids.
> Use blue only for informational data and the semantic status palette
> for actual state.

## `/app/stations/:stationId/energy`

> Design the station energy operations dashboard. Show generation,
> consumption, generator status, fuel availability, load and renewable
> contribution. Include an energy-flow visualization, KPI summary and
> historical trend. Make it look like engineering operations software,
> not a sustainability marketing page.

## `/app/stations/:stationId/logistics`

> Design the station logistics interface. Show inventory, incoming
> supplies, vehicles, vessels, route status and resupply windows. Use a
> geographic/logistics visual and a schedule/timeline. Highlight delays
> and supply risks with warning/critical semantic colors. Avoid
> travel-booking aesthetics.

## `/app/stations/:stationId/personnel`

> Design the station personnel operations screen. Show personnel, role,
> duty status, deployment and basic health status. Include capacity
> versus current personnel. Use a secure operational table. Do not
> expose unnecessary medical information. Apply role-aware access
> patterns.

## `/app/stations/:stationId/health`

> Design a privacy-conscious station health-status screen. Show only
> basic operational states: Normal, Ill, Under Observation, Restricted
> Duty and Medical Attention. Do not show vitals or detailed medical
> records. Make access restrictions visible where appropriate. Use
> semantic colors with text and icons.

## `/app/stations/:stationId/research`

> Design the station research-operations dashboard. Show active
> projects, research domain, personnel, equipment, station and
> data-collection status. Include a compact project/activity timeline.
> Make it feel like scientific operations software, not an academic
> paper repository.

## `/app/stations/:stationId/telemetry`

> Design the station telemetry console. Provide filters for asset,
> sensor, metric and time range. Show current readings, time-series
> charts, sensor health and communication state. Use precise units,
> technical labels and restrained grids. Communicate data freshness
> clearly.

## `/app/stations/:stationId/alerts`

> Design the station alert-management screen. Include station, source,
> category, severity, timestamp, description, acknowledgement and
> resolution state. Information uses #2878A8/#E8F2F8, Warning
> #D9822B/#FFF3E3 and Critical #C44536/#FBE9E7 on light surfaces, with
> lighter dark-surface variants. Critical alerts must be prominent
> without making the whole screen red.

## `/app/stations/:stationId/simulations`

> Design the station simulation workspace. Let users choose scenarios
> such as generator failure, fuel shortage, communication outage,
> extreme weather, personnel emergency or supply delay. Show baseline
> state, scenario parameters and projected effects on energy, logistics,
> personnel, infrastructure and alerts. Include a clear "Run Simulation"
> action and before/after results. Use warning/critical colors only to
> communicate consequences.

## `/app/environment`

> Design a cross-station environmental monitoring dashboard comparing
> Maitri, Bharati and future stations. Include geographic context,
> station comparison, current conditions, sensor health and time-series
> trends. Use a scientific research-console aesthetic and the exact
> DTFIAS palette.

## `/app/energy`

> Design the cross-station energy operations dashboard. Compare
> generation, consumption, fuel, generator load and renewable
> contribution across stations. Include energy-flow and historical trend
> visualizations. Use engineering-oriented hierarchy and restrained data
> visualization.

## `/app/logistics`

> Design the cross-station Antarctic logistics command interface. Show
> inventory, shipments, vessels, vehicles, route status and resupply
> windows. Use geographic context and a logistics timeline. Highlight
> operational risks with semantic warning/critical states.

## `/app/personnel`

> Design the cross-station personnel operations interface. Show station
> assignment, roles, duty status, capacity and basic health state.
> Include filters and a secure operational table. Keep medical
> information minimal and role-controlled.

## `/app/health`

> Design a cross-station basic health-status dashboard. Show aggregated
> operational health states by station and authorized personnel detail
> where permitted. Never display unnecessary medical information. Use
> Normal, Observation, Attention and Medical Attention states with
> semantic colors and text.

## `/app/research`

> Design the cross-station scientific research operations dashboard.
> Show projects, stations, research domains, personnel, equipment and
> data-collection status. Use a calm scientific operations aesthetic
> with the DTFIAS palette.

## `/app/telemetry`

> Design the global telemetry console for DTFIAS. Allow filtering by
> station, asset, sensor, metric and time range. Show current values,
> historical time-series charts and communication health. Use precise
> engineering formatting and visible data freshness.

## `/app/alerts`

> Design the global DTFIAS alert-management console. Include filters
> for station, severity, category, source, status and time. Show concise
> alert rows with timestamp and action state. Critical must be visually
> obvious but not visually dominant when there are no critical events.
> Preserve the semantic light/dark color system.

## `/app/simulations`

> Design the global DTFIAS scenario-planning workspace. Let users
> choose station and scenario, configure parameters and run simulations.
> Present baseline versus projected impact across energy, logistics,
> infrastructure, personnel and alerts. Use a decision-support visual
> language.

## `/app/reports`

> Design the DTFIAS operational reporting interface. Include daily
> station reports, energy, environment, logistics, personnel, incidents,
> telemetry exports and compliance reports. Use a structured list and
> document preview instead of oversized cards. Include
> station/date/report-type filters and export actions.

## `/app/admin`

> Design the restricted DTFIAS administration console. Include users,
> roles, stations, assets, permissions, system health and audit
> activity. Use a denser technical layout while preserving the same
> visual system. Make security and controlled access explicit.

## `/app/admin/users`

> Design the DTFIAS RBAC user-management screen. Show users, roles,
> station access, account status, last login and permission summaries.
> Include search/filter/create/edit actions where authorized. Make
> security administration clear and professional.

## `/app/admin/roles`

> Design the DTFIAS role and permission matrix. Cover stations,
> infrastructure, telemetry, personnel, basic health, logistics,
> research, alerts, simulations, reports and administration. Show
> read/write/manage distinctions clearly. Preserve the institutional
> visual system.

## `/app/admin/stations`

> Design the station-administration interface. Authorized administrators
> can view, create and configure stations. Include name, location,
> operational status, capacity, facilities and metadata. Make the
> generic multi-station architecture obvious.

## `/app/admin/assets`

> Design the DTFIAS asset-administration interface. Show assets by
> station, type, model-object ID, status, sensor relationships and
> configuration. Include authorized create/edit/archive controls. Make
> the link between physical assets and digital-twin objects explicit.

## `/app/admin/audit`

> Design the DTFIAS audit-log interface. Show user, action, resource,
> station, timestamp and result in a dense readable table. Include
> filters by user, station, action and date. Communicate traceability
> and accountability.

## `/app/settings`

> Design the DTFIAS user settings screen. Include profile,
> notifications, display, timezone, dashboard preferences and security.
> Use a clean configuration layout and preserve the exact DTFIAS
> design system.

------------------------------------------------------------------------

# 10. Master Stitch Prompt

Use this before generating the complete application:

> Design the complete DTFIAS frontend, an institutional Antarctic
> remote-operations and digital-twin platform for monitoring and
> managing Indian Antarctic research stations. Support Maitri, Bharati
> and future stations through a generic station architecture. Primary
> users are NCPOR HQ operators, station operations personnel,
> researchers, medical/logistics personnel and administrators with
> role-based access.
>
> The product must feel like scientific mission-control software: calm,
> precise, credible, operational, technical, secure and modern. Do not
> make it look like generic SaaS, crypto, cyberpunk, gaming or consumer
> software.
>
> Use Inter exclusively.
>
> Brand colors: Deep Green #1A312C, Teal Green #428475, Light Mint
> #E8F3EF, Warm Off-White #F7F4ED.
>
> Light semantic colors: Normal #2E7D5B/#E8F4EE, Information
> #2878A8/#E8F2F8, Warning #D9822B/#FFF3E3, Critical #C44536/#FBE9E7.
>
> Dark semantic colors: Normal #63B88A, Information #5AA6D2, Warning
> #F0A24A, Critical #E56B5D with low-opacity dark surfaces.
>
> Never use one semantic color indiscriminately across light and dark
> backgrounds. Adapt contrast while preserving meaning.
>
> The primary application experience is a command center with sidebar,
> header, station directory, Antarctica overview, station digital twin,
> environment, energy, logistics, personnel, basic health, research,
> telemetry, alerts, simulations, reports and administration.
>
> The digital twin uses a high-quality 2D/isometric scientific station
> illustration with HTML/SVG hotspots. Do not require a complex
> real-time 3D engine. Hotspots map to real operational asset
> identifiers and open detailed panels.
>
> Support LIVE, SYNCING, DEGRADED and OFFLINE states. Show last
> synchronization/data freshness timestamps. Do not claim data is live
> when it is cached.
>
> Keep medical data minimal and role-controlled. Use RBAC throughout
> navigation and data visibility.
>
> Use 4--12px radii for normal UI, 12--16px for large panels, restrained
> borders, minimal shadows, generous whitespace and subtle state-driven
> animation. Avoid excessive rounded cards, gradients, glassmorphism,
> neon colors and decorative 3D.
>
> Build all screens as one coherent design system with reusable
> components and consistent responsive behavior.

------------------------------------------------------------------------

# 11. Stitch Generation Sequence

Generate in this order:

### Foundation

1.  `/`
2.  `/login`
3.  `/app/overview`
4.  `/app/stations`

### Signature experience

5.  `/app/stations/:stationId`
6.  `/app/stations/:stationId/digital-twin`
7.  `/app/stations/:stationId/assets/:assetId`

### Operations

8.  environment
9.  energy
10. logistics
11. personnel
12. health
13. research

### Technical

14. telemetry
15. alerts
16. simulations
17. reports

### Administration

18. admin
19. users
20. roles
21. station administration
22. assets
23. audit
24. settings

Generate the shell and first four screens first. Then reuse the
established system for all other screens.

------------------------------------------------------------------------

# 12. Consistency Prompt

> Continue DTFIAS using the exact established design system from the
> previous screens. Do not invent a new visual language. Preserve Inter,
> Deep Green #1A312C, Teal Green #428475, Light Mint #E8F3EF, Warm
> Off-White #F7F4ED, the light/dark semantic status system, spacing,
> typography, borders, radii, sidebar, header, tables, charts, status
> badges and digital-twin components. Every new screen must look like
> part of the same scientific remote-operations product.

------------------------------------------------------------------------

# 13. Anti-Drift Prompt

> Do not redesign DTFIAS as a generic SaaS dashboard. Do not introduce
> purple, neon cyan, neon green, random gradients, excessive
> glassmorphism, giant rounded cards, cartoon illustrations, consumer
> onboarding, excessive pill buttons or decorative 3D. Do not use
> semantic red/blue arbitrarily. Preserve the institutional Antarctic
> scientific aesthetic and exact DTFIAS design tokens.

------------------------------------------------------------------------

# 14. Offline / Connectivity Language

Because Antarctic connectivity may be intermittent, connectivity is a
first-class UI state.

``` text
● LIVE
● SYNCING
● DEGRADED
● OFFLINE
```

When disconnected, show:

-   last known data timestamp
-   queued actions
-   synchronization state
-   locally available data

Never hide stale data without explaining its freshness.

------------------------------------------------------------------------

# 15. Accessibility

Every screen:

-   must have accessible contrast
-   must support keyboard navigation
-   must have visible focus states
-   must use semantic HTML
-   must label inputs
-   must not use color as the only status signal
-   must support reduced motion
-   must make tables readable
-   must provide loading, empty and error states

------------------------------------------------------------------------

# 16. Data Visualization

Charts:

-   show units
-   show time range
-   have readable axes
-   support tooltips
-   avoid 3D charts
-   avoid decorative gradients
-   use Teal Green as the primary neutral series
-   use blue for information
-   orange for warning
-   red for critical
-   use semantic colors only when state meaning is intended

------------------------------------------------------------------------

# 17. Documentation / Skill Updates

This file is the frontend visual source of truth.

Update or create:

### `docs/frontend-design-system.md`

Include:

-   Inter
-   brand tokens
-   light/dark semantic tokens
-   surfaces
-   typography
-   spacing
-   radii
-   accessibility
-   chart/table rules
-   digital-twin rules

### `docs/frontend-architecture.md`

Include:

-   browser route map
-   API boundary
-   AppShell
-   StationTwin
-   SVG hotspot architecture
-   generic station configuration
-   RBAC route/data protection
-   offline/sync behavior

### `skills/frontend.md`

The frontend skill must enforce:

1.  Inter typography.
2.  Exact DTFIAS palette.
3.  Separate semantic light/dark tokens.
4.  No arbitrary colors.
5.  2D/isometric digital twin.
6.  Reusable components.
7.  Generic multi-station architecture.
8.  RBAC-aware navigation and data visibility.
9.  Offline/degraded states.
10. Data freshness indicators.
11. Accessibility.
12. No generic SaaS visual drift.

### `README.md`

Add:

-   frontend design direction
-   route overview
-   Stitch workflow
-   link/reference to this document as the frontend source of truth

------------------------------------------------------------------------

# 18. Frontend Quality Gate

A screen is complete only when:

### Visual

-   [ ] Inter
-   [ ] exact DTFIAS colors
-   [ ] no arbitrary colors
-   [ ] correct light/dark semantic tokens
-   [ ] consistent spacing
-   [ ] consistent radius
-   [ ] restrained shadows/gradients
-   [ ] clear hierarchy

### UX

-   [ ] clear page title
-   [ ] clear station context
-   [ ] clear operational state
-   [ ] loading state
-   [ ] empty state
-   [ ] error state
-   [ ] offline/degraded state where applicable

### Data

-   [ ] units
-   [ ] timestamps/freshness
-   [ ] station context
-   [ ] status text + visual indicator
-   [ ] no false live-data claim

### Security

-   [ ] RBAC-aware
-   [ ] health data minimized
-   [ ] administrative actions restricted
-   [ ] auditability considered

### Digital twin

-   [ ] meaningful station illustration
-   [ ] stable asset IDs
-   [ ] hotspot hover
-   [ ] hotspot selection
-   [ ] status state
-   [ ] asset detail interaction

------------------------------------------------------------------------

# 19. Final Product Statement

DTFIAS should communicate:

> **A remote command interface for understanding and operating an
> Antarctic research station.**

The signature interaction is:

``` text
Antarctica
    ↓
Station
    ↓
2D/2.5D Digital Twin
    ↓
Infrastructure
    ↓
Asset
    ↓
Telemetry
    ↓
Alert / Decision
    ↓
Simulation / Action
```

The station illustration is therefore not a decorative hero image. It is
the visual bridge between the physical Antarctic station and the
operational data model.
