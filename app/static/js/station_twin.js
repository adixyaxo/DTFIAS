/* ═══════════════════════════════════════════════════════════
   BHARATI STATION DIGITAL TWIN — station_twin.js
   Alpine.js component + simulated telemetry engine
   Data contract mirrors docs/2dFrontend.md §5
   ═══════════════════════════════════════════════════════════ */

function stationTwin() {
  return {

    /* ─── State ─────────────────────────────────── */
    activeAsset:   null,
    activeLayer:   'all',
    faultActive:   false,
    tickerIndex:   0,
    simulationTime: new Date('2026-09-05T12:30:00Z'),

    /* ─── Ticker messages ────────────────────────── */
    tickerMessages: [
      '◈ System nominal — all critical systems operating within parameters.',
      '◈ Power Plant: Generator array output 742 kW — load factor 87%, monitor Gen 3 injector.',
      '◈ Environment: −18.4 °C · Wind 32 km/h NE · Visibility 8 km · Barometer 989 hPa.',
      '◈ Vehicle Fleet: Last telemetry 70 min ago — approaching stale threshold.',
      '◈ SATCOM: C-Band uplink stable at 98.7%. Next comms window in 2 h 14 m.',
      '◈ Personnel: 24 on-station. Next crew rotation in 42 days.',
    ],

    /* ─── Asset data (10 subsystems from floor plans) ─── */
    assets: [
      {
        id: 'main_building',
        label: 'Main Structure',
        category: 'infrastructure',
        priority: 'P1',
        status: 'ok',
        value: 98.2, decimals: 1, unit: '%',
        description: 'Structural integrity and habitation systems',
        room: 'Full Building — H1 through H4',
        /* SVG coord: centre of building face, upper section */
        svgX: 625, svgY: 315,
        last_updated: new Date('2026-09-05T12:28:00Z'),
        stale: false,
        telemetry: [
          { key: 'Internal Temp',  value: '21.3',  unit: '°C'     },
          { key: 'Humidity',       value: '42',    unit: '%'      },
          { key: 'Air Pressure',   value: '989',   unit: 'hPa'    },
          { key: 'Occupancy',      value: '24',    unit: 'persons'},
          { key: 'Fire Alarm',     value: 'Clear', unit: ''       },
        ],
        alerts: [],
      },
      {
        id: 'power_plant',
        label: 'Power Plant',
        category: 'energy',
        priority: 'P1',
        status: 'warning',
        value: 742, decimals: 0, unit: 'kW',
        description: 'Diesel generator array — 3 × CAT C32 units',
        /* Floor plan: Ground floor west — G G G generators */
        room: 'Generator Room — Ground Floor, West End',
        svgX: 290, svgY: 430,
        last_updated: new Date('2026-09-05T12:29:30Z'),
        stale: false,
        telemetry: [
          { key: 'Gen 1 Output', value: '248', unit: 'kW',    alert: false },
          { key: 'Gen 2 Output', value: '252', unit: 'kW',    alert: false },
          { key: 'Gen 3 Output', value: '242', unit: 'kW',    alert: true  },
          { key: 'Fuel Burn',    value: '185', unit: 'L/hr',  alert: true  },
          { key: 'Load Factor',  value: '87',  unit: '%',     alert: true  },
          { key: 'Coolant Temp', value: '88',  unit: '°C'                 },
        ],
        alerts: [
          { time: '11:45', message: 'Gen 3 output below nominal — fuel injector check advised.', level: 'warning' },
        ],
      },
      {
        id: 'fuel_storage',
        label: 'Fuel Storage',
        category: 'energy',
        priority: 'P1',
        status: 'ok',
        value: 187400, decimals: 0, unit: 'L',
        description: '~3 lakh L automated diesel fuel farm (Bharati)',
        room: 'Fuel Farm — West Exterior, H1 Ground Level',
        svgX: 155, svgY: 568,
        last_updated: new Date('2026-09-05T12:20:00Z'),
        stale: false,
        telemetry: [
          { key: 'Tank A',   value: '62,400', unit: 'L'       },
          { key: 'Tank B',   value: '58,800', unit: 'L'       },
          { key: 'Tank C',   value: '66,200', unit: 'L'       },
          { key: 'Capacity', value: '300,000',unit: 'L total' },
          { key: 'Fill',     value: '62.5',   unit: '%'       },
          { key: 'Temp',     value: '−4',     unit: '°C'      },
        ],
        alerts: [],
      },
      {
        id: 'hvac',
        label: 'HVAC / Life Support',
        category: 'infrastructure',
        priority: 'P0',
        status: 'ok',
        value: 21.3, decimals: 1, unit: '°C',
        description: 'Heating, ventilation and life-support array',
        /* Floor plan: Centre of building, lower floor */
        room: 'HVAC Plant Room — Lower Floor, Center (Col 10–12)',
        svgX: 625, svgY: 440,
        last_updated: new Date('2026-09-05T12:30:00Z'),
        stale: false,
        telemetry: [
          { key: 'Zone A Temp',    value: '21.3',  unit: '°C'    },
          { key: 'Zone B Temp',    value: '20.8',  unit: '°C'    },
          { key: 'Boiler Output',  value: '145',   unit: 'kW'    },
          { key: 'Ventilation',    value: '3,200', unit: 'm³/hr' },
          { key: 'CO₂ Level',      value: '512',   unit: 'ppm'   },
          { key: 'O₂ Partial P',  value: '20.8',  unit: '%'     },
        ],
        alerts: [],
      },
      {
        id: 'comms_satcom',
        label: 'SATCOM Link',
        category: 'infrastructure',
        priority: 'P0',
        status: 'ok',
        value: 98.7, decimals: 1, unit: '%',
        description: 'C-Band SATCOM uplink (ops channel, not AGEOS)',
        room: 'Satellite Facility — West Exterior',
        svgX: 68, svgY: 535,
        last_updated: new Date('2026-09-05T12:29:00Z'),
        stale: false,
        telemetry: [
          { key: 'Link Quality', value: '98.7', unit: '%'     },
          { key: 'Uplink Rate',  value: '512',  unit: 'kbps'  },
          { key: 'Downlink',     value: '2048', unit: 'kbps'  },
          { key: 'Elevation',    value: '34',   unit: '°'     },
          { key: 'Next Window',  value: '2h 14m',unit: ''     },
          { key: 'Signal Noise', value: '−108', unit: 'dBm'   },
        ],
        alerts: [],
      },
      {
        id: 'medical_bay',
        label: 'Medical Bay',
        category: 'personnel',
        priority: 'P0',
        status: 'ok',
        value: 0, decimals: 0, unit: 'active cases',
        description: 'Medical facility — personnel health monitoring',
        /* Floor plan: Upper floor, medical room centre-right */
        room: 'Medical Room — Upper Floor, Col 14–16',
        svgX: 760, svgY: 315,
        last_updated: new Date('2026-09-05T12:15:00Z'),
        stale: false,
        telemetry: [
          { key: 'Active Cases',   value: '0',    unit: ''   },
          { key: 'Defibrillator',  value: 'Ready',unit: ''   },
          { key: 'O₂ Supply',      value: '98',   unit: '%'  },
          { key: 'Med Fridge',     value: '4.2',  unit: '°C' },
          { key: 'Room Temp',      value: '22.0', unit: '°C' },
        ],
        alerts: [],
      },
      {
        id: 'personnel_roster',
        label: 'Personnel Roster',
        category: 'personnel',
        priority: 'P1',
        status: 'ok',
        value: 24, decimals: 0, unit: 'on-station',
        description: 'Station headcount and rotation status',
        /* Floor plan: Living quarters — perimeter rooms north & south */
        room: 'Living Quarters — Upper Floor, North & South Corridors',
        svgX: 875, svgY: 310,
        last_updated: new Date('2026-09-05T12:00:00Z'),
        stale: false,
        telemetry: [
          { key: 'On Station',    value: '24', unit: 'persons' },
          { key: 'Scientists',    value: '16', unit: ''        },
          { key: 'Support Staff', value: '8',  unit: ''        },
          { key: 'Next Rotation', value: '42', unit: 'days'   },
          { key: 'Acc. Bunks',    value: '24', unit: 'of 25'  },
        ],
        alerts: [],
      },
      {
        id: 'environment_sensors',
        label: 'Env. Sensors',
        category: 'environmental',
        priority: 'P2',
        status: 'ok',
        value: -18.4, decimals: 1, unit: '°C',
        description: 'Ambient environmental monitoring array',
        /* Floor plan: Roof instrumentation at H4 */
        room: 'Roof Instrumentation — H4 Platform (Col 9–11)',
        svgX: 625, svgY: 232,
        last_updated: new Date('2026-09-05T12:29:00Z'),
        stale: false,
        telemetry: [
          { key: 'Ambient Temp',  value: '−18.4', unit: '°C'  },
          { key: 'Wind Speed',    value: '32',    unit: 'km/h' },
          { key: 'Wind Dir',      value: 'NE',    unit: ''     },
          { key: 'Pressure',      value: '989',   unit: 'hPa' },
          { key: 'Visibility',    value: '8.0',   unit: 'km'  },
          { key: 'UV Index',      value: '0.2',   unit: ''    },
        ],
        alerts: [],
      },
      {
        id: 'heliport',
        label: 'Heliport',
        category: 'logistics',
        priority: 'P2',
        status: 'ok',
        value: 1, decimals: 0, unit: 'pad',
        description: 'Aerial logistics — helicopter landing pad',
        /* Floor plan: East exterior (right end of building) */
        room: 'East Exterior — Helipad Platform, H1 Ground',
        svgX: 1198, svgY: 595,
        last_updated: new Date('2026-09-05T10:00:00Z'),
        stale: false,
        telemetry: [
          { key: 'Pad Status',  value: 'Clear',     unit: ''      },
          { key: 'Wind (pad)',  value: '28',        unit: 'km/h'  },
          { key: 'Last Flight', value: '6 h ago',   unit: ''      },
          { key: 'Next Flight', value: 'TBD',       unit: ''      },
        ],
        alerts: [],
      },
      {
        id: 'vehicle_fleet',
        label: 'Vehicle Fleet',
        category: 'logistics',
        priority: 'P2',
        status: 'stale',
        value: 3, decimals: 0, unit: 'active',
        description: 'Ground transport — snowcats and support vehicles',
        room: 'Vehicle Bay & External Ground Area',
        svgX: 498, svgY: 640,
        last_updated: new Date('2026-09-05T11:20:00Z'),
        stale: true,
        telemetry: [
          { key: 'Snowcat 1',   value: 'Deployed', unit: ''  },
          { key: 'Snowcat 2',   value: 'Maint.',   unit: ''  },
          { key: 'Forklift',    value: 'Active',   unit: ''  },
          { key: 'Fuel Level',  value: '78',       unit: '%' },
        ],
        alerts: [
          { time: '11:20', message: 'Snowcat 2 — GPS telemetry offline. Manual check required.', level: 'warning' },
        ],
      },
    ],

    /* ─── Lifecycle ──────────────────────────────── */
    init() {
      this._simLoop   = setInterval(() => this._tick(), 2000);
      this._tickLoop  = setInterval(() => {
        this.tickerIndex = (this.tickerIndex + 1) % this.tickerMessages.length;
      }, 5500);
    },

    destroy() {
      clearInterval(this._simLoop);
      clearInterval(this._tickLoop);
    },

    /* ─── Simulation tick (every 2 s) ────────────── */
    _tick() {
      this.simulationTime = new Date(this.simulationTime.getTime() + 2000);
      const now = this.simulationTime;

      this.assets.forEach(a => {
        /* --- random value drift --- */
        if (a.id === 'power_plant' && !this.faultActive) {
          a.value = Math.max(680, Math.min(860, a.value + (Math.random() - 0.5) * 8));
          if (a.telemetry) {
            a.telemetry[0].value = String(Math.round(a.value * 0.334));
            a.telemetry[1].value = String(Math.round(a.value * 0.340));
            a.telemetry[2].value = String(Math.round(a.value * 0.326));
          }
        }
        if (a.id === 'environment_sensors') {
          a.value = parseFloat((a.value + (Math.random() - 0.5) * 0.15).toFixed(1));
          if (a.telemetry) {
            a.telemetry[0].value = String(a.value);
            a.telemetry[1].value = String(Math.round(28 + Math.random() * 6));
          }
        }
        if (a.id === 'hvac') {
          a.value = parseFloat((a.value + (Math.random() - 0.5) * 0.06).toFixed(1));
          if (a.telemetry) a.telemetry[0].value = String(a.value);
        }
        if (a.id === 'fuel_storage' && !this.faultActive) {
          /* slow drain */
          a.value = Math.max(0, a.value - 1.5);
        }

        /* --- staleness check --- */
        if (a.id !== 'vehicle_fleet') {
          const ageMin = (now - new Date(a.last_updated)) / 60000;
          a.stale = ageMin > 45;
          /* refresh timestamp for active assets */
          if (!a.stale && Math.random() < 0.25) a.last_updated = now;
        }
      });

      /* sync active panel */
      if (this.activeAsset) {
        const fresh = this.assets.find(a => a.id === this.activeAsset.id);
        if (fresh) this.activeAsset = fresh;
      }
    },

    /* ─── Selection ──────────────────────────────── */
    selectAsset(id) {
      this.activeAsset = this.assets.find(a => a.id === id) || null;
    },
    clearSelection() { this.activeAsset = null; },

    /* ─── Fault simulation ───────────────────────── */
    simulateFault() {
      if (this.faultActive) return;
      const pp = this.assets.find(a => a.id === 'power_plant');
      pp.status   = 'critical';
      pp.priority = 'P0';
      pp.value    = 312;
      if (pp.telemetry) {
        pp.telemetry[0].value = '108'; pp.telemetry[0].alert = true;
        pp.telemetry[1].value = '112'; pp.telemetry[1].alert = true;
        pp.telemetry[2].value = '92';  pp.telemetry[2].alert = true;
      }
      pp.alerts.unshift({
        time: this._fmtTime(),
        message: '⛔ CRITICAL: Power output dropped to 312 kW (−58%). Generator array fault.',
        level: 'critical',
      });
      this.faultActive = true;
      this.tickerMessages.unshift('⛔ CRITICAL ALERT — Power Plant: output 312 kW (↓58%). Immediate attention required!');
      this.tickerIndex = 0;
      this.selectAsset('power_plant');

      setTimeout(() => {
        pp.status   = 'warning';
        pp.priority = 'P1';
        pp.value    = 742;
        this.faultActive = false;
        pp.alerts.unshift({
          time: this._fmtTime(),
          message: '✓ Power restored to 742 kW. Fault cleared — monitor Gen 3.',
          level: 'ok',
        });
      }, 30000);
    },

    /* ─── Remote actions ─────────────────────────── */
    acknowledgeAlert(assetId) {
      const a = this.assets.find(x => x.id === assetId);
      if (!a) return;
      if (a.status !== 'ok') {
        a.status = a.status === 'critical' ? 'warning' : 'ok';
      }
      a.alerts.unshift({ time: this._fmtTime(), message: 'Alert acknowledged by operator.', level: 'info' });
    },
    adjustThreshold(assetId) {
      /* In production: opens a modal for threshold config */
      const a = this.assets.find(x => x.id === assetId);
      if (a) a.alerts.unshift({ time: this._fmtTime(), message: 'Threshold adjustment dialog opened (stub).', level: 'info' });
    },
    logCommand(assetId) {
      const a = this.assets.find(x => x.id === assetId);
      if (a) a.alerts.unshift({ time: this._fmtTime(), message: 'Manual inspection logged by operator.', level: 'info' });
    },

    /* ─── Computed helpers ───────────────────────── */
    isVisible(asset) {
      return this.activeLayer === 'all' || asset.category === this.activeLayer;
    },

    countByStatus(status) {
      return this.assets.filter(a => a.status === status).length;
    },

    getStatusColor(status) {
      return { critical:'#ff2d55', warning:'#ff9f0a', ok:'#30d158', stale:'#636366', offline:'#ff453a' }[status] || '#636366';
    },

    getStatusIcon(status) {
      return { critical:'⛔', warning:'⚠', ok:'✓', stale:'⟳', offline:'✗' }[status] || '?';
    },

    get tickerMessage() { return this.tickerMessages[this.tickerIndex]; },

    /* ─── Formatters ─────────────────────────────── */
    formatSimTime() {
      return this.simulationTime.toISOString().substr(11, 8) + ' UTC';
    },

    formatTimeAgo(date) {
      const ms   = this.simulationTime - new Date(date);
      const sec  = Math.floor(ms / 1000);
      const min  = Math.floor(sec / 60);
      const hr   = Math.floor(min / 60);
      if (sec  < 60) return 'just now';
      if (min  < 60) return `${min} m ago`;
      return `${hr} h ${min % 60} m ago`;
    },

    _fmtTime() {
      return this.simulationTime.toISOString().substr(11, 5);
    },
  };
}
