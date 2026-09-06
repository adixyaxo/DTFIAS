---
name: dtfias-brand-guidelines
description: Applies DTFIAS official brand colors, typography, and status color system to any frontend artifact. Use when implementing any visual design, component styling, status indicators, alerts, cards, navigation, or layouts for the Digital Twin for Indian Antarctic Stations project.
license: MIT
---

# DTFIAS Brand Guidelines

## Overview

The DTFIAS visual identity is built around a **deep Antarctic green** palette that conveys scientific authority, environmental connection, and operational precision. Every UI element MUST draw from this palette.

**Keywords**: branding, visual identity, color palette, typography, status colors, alert colors, DTFIAS design, Antarctic digital twin

---

## Brand Palette

### Base Colors

| Token | Hex | CSS Variable | Usage |
|-------|-----|-------------|-------|
| Deep Green | `#1A312C` | `--brand-deep-green` | Headers, navigation, dark backgrounds, footers, strong visual anchors |
| Teal Green | `#428475` | `--brand-teal` | Buttons, section headings, nav elements, cards, icons, highlights |
| Light Mint | `#C8E6D7` | `--brand-mint` | Background sections, info cards, hover states, subtle highlights |
| Cream / Off-White | `#F5F2EB` | `--brand-cream` | Main page backgrounds, content areas, cards, readable sections |
| Cream Dark | `#E8E3D9` | `--brand-cream-dark` | Borders, dividers, subtle separators |

```css
:root {
  --brand-deep-green:   #1A312C;
  --brand-teal:         #428475;
  --brand-mint:         #C8E6D7;
  --brand-cream:        #F5F2EB;
  --brand-cream-dark:   #E8E3D9;
}
```

---

## Status / Alert Color System

> **Critical rule:** The status colors have TWO variants — one for **light backgrounds** and one for **dark backgrounds**. Always use the correct variant for the context.

### Status Colors — Light Background Context

| State | Name | Main Color | Background Tint | CSS Variables |
|-------|------|-----------|-----------------|---------------|
| Normal / Safe | Dark Seafoam Green | `#2E7D5B` | `#E8F4EE` | `--status-ok`, `--status-ok-bg` |
| Informational | Steel Blue | `#2878A8` | `#E8F2F8` | `--status-info`, `--status-info-bg` |
| Warning / Attention | Neon Carrot | `#D9822B` | `#FFF3E3` | `--status-warning`, `--status-warning-bg` |
| Critical / Emergency | Brick Red | `#C44536` | `#FBE9E7` | `--status-critical`, `--status-critical-bg` |
| Stale / No data | Neutral Gray | `#6B7280` | `#F3F4F6` | `--status-stale`, `--status-stale-bg` |

### Status Colors — Dark Background Context (higher contrast variants)

| State | Dark-bg Color | CSS Variable |
|-------|--------------|--------------|
| Normal / Safe | `#4ABA83` | `--status-ok-dark` |
| Informational | `#5BA3D4` | `--status-info-dark` |
| Warning / Attention | `#F0A050` | `--status-warning-dark` |
| Critical / Emergency | `#E06050` | `--status-critical-dark` |
| Hard Offline | `#9B1C1C` | `--status-offline` |

```css
:root {
  /* Light background status */
  --status-ok:          #2E7D5B;
  --status-info:        #2878A8;
  --status-warning:     #D9822B;
  --status-critical:    #C44536;
  --status-stale:       #6B7280;
  --status-offline:     #9B1C1C;
  /* Light bg tints */
  --status-ok-bg:       #E8F4EE;
  --status-info-bg:     #E8F2F8;
  --status-warning-bg:  #FFF3E3;
  --status-critical-bg: #FBE9E7;
  --status-stale-bg:    #F3F4F6;
  /* Dark bg variants (brighter for contrast) */
  --status-ok-dark:       #4ABA83;
  --status-info-dark:     #5BA3D4;
  --status-warning-dark:  #F0A050;
  --status-critical-dark: #E06050;
}
```

---

## Typography

The DTFIAS type system uses **three fonts**, each with a distinct role:

| Font | Role | CSS Variable | Usage |
|------|------|-------------|-------|
| **Playfair Display** | Headings / Display | `--font-heading` | Page titles, section headings, dashboard titles, card headings |
| **Playfair** | Body / Editorial | `--font-body` | Important paragraphs, descriptions, callout text, station narrative copy |
| **Inter** | UI Chrome | `--font-ui` | Buttons, nav, labels, form inputs, table data, metadata |
| **JetBrains Mono** | Monospace | `--font-mono` | Sensor values, timestamps, coordinates, codes, telemetry readouts |

```html
<!-- Load from Google Fonts (single combined request) -->
<link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,300;0,14..32,400;0,14..32,500;0,14..32,600;0,14..32,700;0,14..32,800;1,14..32,400&family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,500;1,600;1,700&family=Playfair:ital,opsz,wght@0,5..1200,300;0,5..1200,400;0,5..1200,500;0,5..1200,600;0,5..1200,700;1,5..1200,300;1,5..1200,400;1,5..1200,500&display=swap" rel="stylesheet">
```

```css
:root {
  --font-heading: 'Playfair Display', Georgia, 'Times New Roman', serif;
  --font-body:    'Playfair', Georgia, 'Times New Roman', serif;
  --font-ui:      'Inter', system-ui, -apple-system, sans-serif;
  --font-mono:    'JetBrains Mono', ui-monospace, monospace;
}
```

### Usage Examples

```css
/* Page / section headings */
h1, h2, h3 { font-family: var(--font-heading); font-weight: 700; }

/* Station narrative / important descriptions */
.prose, .description, .callout { font-family: var(--font-body); }

/* All UI chrome — buttons, nav, forms, tables */
body, button, input, label { font-family: var(--font-ui); }

/* Telemetry, timestamps, sensor values */
.telemetry, time, code { font-family: var(--font-mono); }
```

### Why This Stack

- **Playfair Display** — high-contrast, optically corrected serif with strong Antarctic/scientific gravitas. Pairs the technical precision of the dashboard with editorial authority.
- **Playfair** — the text companion to Playfair Display. Works at paragraph size without sacrificing the serif character of the headings.
- **Inter** — neutral, highly legible at small sizes. Ideal for data-dense UI where readability at 11–13px is critical.
- **JetBrains Mono** — designed specifically for code and numbers; tabular figures and clear zero/O disambiguation essential for sensor data.

---

## SCADA / Dark Mode (Station Twin)

For the station twin dark SCADA interface, use the deep green dark palette:

```css
:root {
  --bg-deep:     #0B1C18;  /* green-black — main canvas */
  --bg-surface:  #122620;  /* dark teal surface */
  --bg-elevated: #1A312C;  /* deep green — panels, cards */
  --bg-glass:    rgba(18, 38, 32, 0.88);

  --border-subtle: rgba(66, 132, 117, 0.15);
  --border-medium: rgba(66, 132, 117, 0.30);
  --border-bright: rgba(66, 132, 117, 0.55);

  --accent-teal: #428475;
  --accent-mint: #7DBFAD;
  --accent-glow: rgba(66, 132, 117, 0.28);

  --text-primary:   #E8F2EE;
  --text-secondary: #7AA898;
  --text-muted:     #3E6358;
}
```

---

## Category Colors (Station Twin layers)

| Category | Color | Hex |
|----------|-------|-----|
| Infrastructure | Steel Blue | `#5E88C8` |
| Energy | Warm Orange | `#D9822B` |
| Environmental | Teal Brand | `#428475` |
| Logistics | Muted Purple | `#7B5EA7` |
| Personnel | Earthy Sienna | `#A0522D` |

---

## Alert Animation Rules

| Priority | Visual treatment |
|----------|-----------------|
| P0 / Critical | Persistent CSS pulse animation (`ring-expand` keyframe), `--status-critical-dark` on dark bg |
| P1 / Warning | Color change only, no animation, `--status-warning-dark` on dark bg |
| P2 / Normal | No animation, `--status-ok` or `--status-ok-dark` as appropriate |
| Stale | Desaturated + dimmed (`filter: saturate(0.15) brightness(0.6)`) + "last updated Xm ago" label |

---

## Anti-Patterns (Do NOT use)

- Blue/navy as a primary brand color (the old default Tailwind blues)
- Orange-cream "AI slop" combinations
- Pure white (`#FFFFFF`) backgrounds — use `--brand-cream` instead
- `Space Grotesk`, `Roboto`, `Arial` as primary typeface
- `#ff2d55` / `#30d158` / `#ff9f0a` Apple-style status colors
- Purple gradients on white backgrounds