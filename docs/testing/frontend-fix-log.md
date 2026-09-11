
Finding ID: INC-09, INC-12, INC-15 (Modal dimensions)
Date: 2026-09-09
Changed Files:
  - app/templates/components/modals/asset_detail.html
  - app/templates/components/modals/alert_dialog.html
  - All templates with inline Playfair Display fonts
  - app/templates/hq/stations.html
  - app/templates/hq/telemetry.html
  - app/templates/station/dashboard.html
  - app/templates/station/twin.html
  - app/templates/station/logistics.html
  - app/templates/station/personnel.html
  - app/templates/station/health.html
Root Cause: Hardcoded values contradicting the stations.py constants; inline styles conflicting with Tailwind typography tokens; incorrect Tailwind spacing classes for modals.
Fix:
  - Removed all inline ont-family: 'Playfair Display' styles to let tailwind tokens govern typography.
  - Adjusted modal widths and paddings from w-64/pl-64 to w-72/pl-72 to align seamlessly with the master topnav and sidebar.
  - Replaced hardcoded headcounts (e.g. 46, 18/30) with dynamic Jinja variables {{ station.souls_winter }} and {{ station.souls_active }}.
  - Synchronized HQ summary screens to match the stations.py config precisely (92 Summer / 42 Winter).
  - Used Jinja conditionals in station personnel templates so Bharati and Maitri show distinct personnel names.
Tests: N/A (CSS/Markup visual verification)
Regression Checks: Verified layout spacing and grid structures.
Verification: Passed. Modals align, typography is consistent with tokens, headcounts match the backend constants.
