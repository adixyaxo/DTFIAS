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
    showAssetList: true,
    faultActive:   false,
    satcomOffline: false,
    show3D:        true,
    tickerIndex:   0,
    simulationTime: new Date('2026-09-05T12:30:00Z'),

    // HUD state
    view3DMode: 'exterior',
    triCount3D: null,

    init3DLoader() {
      const load3D = () => {
        const s = document.createElement('script');
        s.src = '/static/js/three/station_3d_view.js';
        s.onload = () => {
          if (typeof window.initStation3D === 'function') {
            window.initStation3D('station-3d-container');
          }
        };
        document.body.appendChild(s);
      };

      if (!window.THREE) {
        const t = document.createElement('script');
        t.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
        t.onload = load3D;
        document.head.appendChild(t);
      } else {
        load3D();
      }
    },

    /* ─── Ticker messages ────────────────────────── */
    tickerMessages: [
      '◈ System nominal — all critical systems operating within parameters.',
      '◈ Power Plant: Generator array output 282 kW — load factor 83%, monitor Gen 3 injector.',
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
        value: 145, decimals: 0, unit: 'kW',
        description: 'Diesel generator array — 3 × 100 kVA MAN CHP',
        /* Floor plan: Ground floor west — G G G generators */
        room: 'Generator Room — Ground Floor, West End',
        last_updated: new Date('2026-09-05T12:29:30Z'),
        stale: false,
        telemetry: [
          { key: 'MAN Gen 1',    value: '45',  unit: 'kW',    alert: false },
          { key: 'MAN Gen 2',    value: '48',  unit: 'kW',    alert: false },
          { key: 'MAN Gen 3',    value: '52',  unit: 'kW',    alert: true  },
          { key: 'Thermal Load', value: '110', unit: 'kWth',  alert: false },
          { key: 'Oil Press 3',  value: '190', unit: 'kPa',   alert: true  },
        ],
        alerts: [
          { time: '11:45', message: 'Gen 3 oil pressure critically low (190 kPa) — risk of seizure.', level: 'critical' },
        ],
      },
      {
        id: 'fuel_storage',
        label: 'Fuel Storage',
        category: 'energy',
        priority: 'P1',
        status: 'ok',
        value: 296000, decimals: 0, unit: 'L',
        description: '296 kL Jet A-1 automated fuel farm (13 tanks)',
        room: 'Fuel Farm — West Exterior, H1 Ground Level',
        last_updated: new Date('2026-09-05T12:20:00Z'),
        stale: false,
        telemetry: [
          { key: 'Total Reserves', value: '254,000', unit: 'L'       },
          { key: 'Active Tanks',   value: '11',      unit: 'of 13'   },
          { key: 'Day Tank',       value: '9.5',     unit: 'kL'      },
          { key: 'Days Left',      value: '220',     unit: 'days'    },
          { key: 'Next Transfer',  value: '5.2',     unit: 'days'    },
        ],
        alerts: [],
      },
      {
        id: 'seawater_intake',
        label: 'Water Supply',
        category: 'infrastructure',
        priority: 'P0',
        status: 'warning',
        value: 12, decimals: 1, unit: 'm',
        description: '~300m Trace-Heated Intake from Quilty Bay',
        room: 'Quilty Bay Intake / Ground Desalination Plant',
        last_updated: new Date('2026-09-05T12:29:00Z'),
        stale: false,
        telemetry: [
          { key: 'Intake Depth',   value: '12',    unit: 'm'     },
          { key: 'Pipeline Temp',  value: '1.2',   unit: '°C',   alert: true  },
          { key: 'Trace Current',  value: '6.2',   unit: 'A'     },
          { key: 'Trace Resist.',  value: '4.8',   unit: 'Ohms', alert: true  },
        ],
        alerts: [
          { time: '12:28', message: 'Trace heater resistance critically low (4.8 Ohms). Potential short circuit. Pipeline Temp 1.2°C.', level: 'critical' },
        ],
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
        value: window.STATION_ID === 'maitri' ? 25 : 72, decimals: 0, unit: 'on-station',
        description: 'Station headcount and rotation status',
        /* Floor plan: Living quarters — perimeter rooms north & south */
        room: 'Living Quarters — Upper Floor, North & South Corridors',
        last_updated: new Date('2026-09-05T12:00:00Z'),
        stale: false,
        telemetry: [
          { key: 'On Station',    value: window.STATION_ID === 'maitri' ? '25' : '72', unit: 'persons' },
          { key: 'Scientists',    value: '45', unit: ''        },
          { key: 'Support Staff', value: window.STATION_ID === 'maitri' ? '9' : '27',  unit: ''        },
          { key: 'Next Rotation', value: '42', unit: 'days'   },
          { key: 'Acc. Bunks',    value: window.STATION_ID === 'maitri' ? '25' : '72', unit: window.STATION_ID === 'maitri' ? 'of 65' : 'of 72'  },
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

      // Throttle simulation loop when document is hidden to conserve CPU and prevent background drift
      document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
          if (this._simLoop) {
            clearInterval(this._simLoop);
            this._simLoop = null;
          }
        } else {
          if (!this._simLoop) {
            this._simLoop = setInterval(() => this._tick(), 2000);
          }
        }
      });

      // Lazy load Three.js environment on init since it's the only view
      if (!window.THREE) {
        const threeScript = document.createElement('script');
        threeScript.src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js";
        threeScript.onload = () => {
          const orbitScript = document.createElement('script');
          orbitScript.src = "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js";
          orbitScript.onload = () => {
            const appScript = document.createElement('script');
            appScript.src = "/static/js/three/station_3d_view.js";
            appScript.onload = () => {
              // Listen for triangle count event BEFORE initializing station 3D
              window.addEventListener('3d-tri-count', (e) => {
                this.triCount3D = e.detail.toLocaleString();
              });
              if (window.initStation3D) {
                window.initStation3D('station-3d-container');
              }
              if (window.station3DScene && window.station3DScene.totalTriangles) {
                this.triCount3D = window.station3DScene.totalTriangles.toLocaleString();
              }
            };
            document.body.appendChild(appScript);
          };
          document.body.appendChild(orbitScript);
        };
        document.body.appendChild(threeScript);
      } else if (window.THREE && !window.station3DScene && window.initStation3D) {
        window.addEventListener('3d-tri-count', (e) => {
          this.triCount3D = e.detail.toLocaleString();
        });
        window.initStation3D('station-3d-container');
        if (window.station3DScene && window.station3DScene.totalTriangles) {
          this.triCount3D = window.station3DScene.totalTriangles.toLocaleString();
        }
      }
      if (window.station3DScene && window.station3DScene.totalTriangles && !this.triCount3D) {
        this.triCount3D = window.station3DScene.totalTriangles.toLocaleString();
      }
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
          const isMaitri = (window.STATION_ID === 'maitri');
          const maxKw = isMaitri ? 250 : 340;
          const targetKw = isMaitri ? 145 : 210;
          a.value = Math.max(0, Math.min(maxKw, a.value + (Math.random() - 0.5) * 4));
          // Gradually pull towards target
          if (Math.abs(a.value - targetKw) > 10) {
              a.value += (targetKw - a.value) * 0.1;
          }
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

        // Bridge to 3D if active
        if (this.show3D && typeof window.update3DHotspot === 'function') {
            window.update3DHotspot(a.id, a.status);
        }
      });

      /* sync active panel */
      if (this.activeAsset) {
        const fresh = this.assets.find(a => a.id === this.activeAsset.id);
        if (fresh) this.activeAsset = fresh;
      }
    },

    /* ─── Slug / alias mapping between 3D scene objects and 2D telemetry asset IDs ─── */
    _resolveAssetId(idOrSlug) {
      if (!idOrSlug) return null;
      const clean = String(idOrSlug).replace(/^hotspot-/, '');
      const SLUG_TO_ID = {
        'power-plant': 'power_plant',
        'power_plant': 'power_plant',
        'chp-heating': 'power_plant',
        'fuel-storage': 'fuel_storage',
        'fuel_storage': 'fuel_storage',
        'main-hab': 'main_building',
        'main-building': 'main_building',
        'main_building': 'main_building',
        'main-entrance': 'main_building',
        'v-stilts': 'main_building',
        'pipe-rack': 'seawater_intake',
        'seawater-intake': 'seawater_intake',
        'seawater_intake': 'seawater_intake',
        'water-lss': 'seawater_intake',
        'meltwater-tarn': 'seawater_intake',
        'hvac': 'hvac',
        'satcom': 'comms_satcom',
        'comms-satcom': 'comms_satcom',
        'comms_satcom': 'comms_satcom',
        'medical-bay': 'medical_bay',
        'medical_bay': 'medical_bay',
        'personnel-roster': 'personnel_roster',
        'personnel_roster': 'personnel_roster',
        'dining-mess': 'personnel_roster',
        'ocean-lounge': 'personnel_roster',
        'meteo-mast': 'environment_sensors',
        'meteo-science-lab': 'environment_sensors',
        'flagpole-ridge': 'environment_sensors',
        'science-terrace': 'environment_sensors',
        'environment-sensors': 'environment_sensors',
        'environment_sensors': 'environment_sensors',
        'heliport': 'heliport',
        'vehicle-fleet': 'vehicle_fleet',
        'vehicle_fleet': 'vehicle_fleet',
        'workshop-garage': 'vehicle_fleet',
        'container-depot': 'vehicle_fleet',
      };
      return SLUG_TO_ID[clean] || SLUG_TO_ID[clean.replace(/-/g, '_')] || clean.replace(/-/g, '_');
    },

    /* ─── Selection & Panel Navigation ───────────── */
    selectAsset(id) {
      const resolved = this._resolveAssetId(id);
      this.activeAsset = this.assets.find(a => a.id === resolved || a.id === id) || null;
      if (this.activeAsset) {
        this.showAssetList = false;
        if (this.activeLayer !== 'all' && this.activeLayer !== this.activeAsset.category) {
          this.activeLayer = (this.activeAsset.category === 'environmental') ? 'environmental' : this.activeAsset.category;
        }
        if (typeof window !== 'undefined' && typeof window.focus3DHotspot === 'function') {
          window.focus3DHotspot(resolved || id);
        }
      }
    },
    selectAssetFromPanel(id) {
      this.selectAsset(id);
      this.showAssetList = false;
    },
    backToList() {
      this.showAssetList = true;
      this.clearSelection();
    },
    clearSelection() {
      this.activeAsset = null;
      this.showAssetList = true;
    },

    /* ─── Fault simulation ───────────────────────── */
    simulateFault() {
      if (this.faultActive) return;
      const pp = this.assets.find(a => a.id === 'power_plant');
      pp.status   = 'critical';
      pp.priority = 'P0';
      pp.value    = 112;
      if (pp.telemetry) {
        pp.telemetry[0].value = '58'; pp.telemetry[0].alert = true;
        pp.telemetry[1].value = '54'; pp.telemetry[1].alert = true;
        pp.telemetry[2].value = '0';  pp.telemetry[2].alert = true;
      }
      pp.alerts.unshift({
        time: this._fmtTime(),
        message: '⛔ CRITICAL: Power output dropped to 112 kW (−60%). Generator array fault.',
        level: 'critical',
      });
      this.faultActive = true;
      this.tickerMessages.unshift('⛔ CRITICAL ALERT — Power Plant: output 112 kW (↓60%). Immediate attention required!');
      this.tickerIndex = 0;
      this.selectAsset('power_plant');
      if (this.show3D && window.update3DHotspot) window.update3DHotspot('power_plant', 'critical');

      setTimeout(() => {
        pp.status   = 'warning';
        pp.priority = 'P1';
        pp.value    = 282;
        this.faultActive = false;
        pp.alerts.unshift({
          time: this._fmtTime(),
          message: '✓ Power restored to 282 kW. Fault cleared — monitor Gen 3.',
          level: 'ok',
        });
        if (this.show3D && window.update3DHotspot) window.update3DHotspot('power_plant', 'warning');
      }, 30000);
    },

    /* ─── Remote actions ─────────────────────────── */
    toggleSatcom() {
      this.satcomOffline = !this.satcomOffline;
      const satcomAsset = this.assets.find(x => x.id === 'comms_satcom');
      if (satcomAsset) {
        satcomAsset.status = this.satcomOffline ? 'critical' : 'ok';
        satcomAsset.priority = this.satcomOffline ? 'P0' : 'P2';
        satcomAsset.value = this.satcomOffline ? 0 : 98.7;
        if (satcomAsset.telemetry) {
          satcomAsset.telemetry[0].value = this.satcomOffline ? '0' : '98.7';
          satcomAsset.telemetry[1].value = this.satcomOffline ? '0' : '512';
        }
        if (this.satcomOffline) {
          satcomAsset.alerts.unshift({ time: this._fmtTime(), message: '⛔ CRITICAL: SATCOM link lost. Falling back to edge computing mode.', level: 'critical' });
          this.tickerMessages.unshift('📡 SATCOM LOSS DETECTED — System operating autonomously in edge mode.');
          this.tickerIndex = 0;
          if (this.show3D && window.update3DHotspot) window.update3DHotspot('comms_satcom', 'critical');
        } else {
          satcomAsset.alerts.unshift({ time: this._fmtTime(), message: '✓ SATCOM link restored.', level: 'ok' });
          this.tickerMessages.unshift('📡 SATCOM RESTORED — Syncing telemetry buffer with HQ.');
          this.tickerIndex = 0;
          if (this.show3D && window.update3DHotspot) window.update3DHotspot('comms_satcom', 'ok');
        }
      }
    },
    
    toggle3D() {
      this.show3D = !this.show3D;
      if (this.show3D && !window.THREE) {
        // Lazy load Three.js first
        const threeScript = document.createElement('script');
        threeScript.src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js";
        threeScript.onload = () => {
          // Then load OrbitControls sequentially
          const orbitScript = document.createElement('script');
          orbitScript.src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/controls/OrbitControls.min.js";
          orbitScript.onload = () => {
            // Then load our 3D view script
            const appScript = document.createElement('script');
            appScript.src = "/static/js/three/station_3d_view.js";
            appScript.onload = () => {
              window.initStation3D('station-3d-container');
              // Pick up triangle count for HUD badge
              window.addEventListener('3d-tri-count', (e) => {
                this.triCount3D = e.detail.toLocaleString();
              }, { once: true });
            };
            document.body.appendChild(appScript);
          };
          document.body.appendChild(orbitScript);
        };
        document.body.appendChild(threeScript);
      } else if (this.show3D && window.THREE && !window.station3DScene && window.initStation3D) {
        window.initStation3D('station-3d-container');
      }
    },

    /* ─── HUD: 3D View Mode Switcher ─────────────── */
    set3DViewMode(mode) {
      this.view3DMode = mode;
      if (typeof window.set3DMode === 'function') {
        window.set3DMode(mode);
      }
    },

    /* ─── HUD: Camera Reset ──────────────────────── */
    resetCamera3D() {
      if (typeof window.resetCamera3D === 'function') {
        window.resetCamera3D();
      }
    },

    /* ─── HUD: Screenshot ────────────────────────── */
    screenshot3D() {
      if (typeof window.screenshot3D === 'function') {
        window.screenshot3D();
      }
    },

    acknowledgeAlert(assetId) {

      const a = this.assets.find(x => x.id === assetId);
      if (!a) return;
      if (a.status !== 'ok') {
        a.status = a.status === 'critical' ? 'warning' : 'ok';
      }
      a.alerts.unshift({ time: this._fmtTime(), message: 'Alert acknowledged by operator.', level: 'info' });
      if (this.show3D && typeof window.update3DHotspot === 'function') {
        window.update3DHotspot(a.id, a.status);
      }
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
    get filteredAssets() {
      if (!this.activeLayer || this.activeLayer === 'all') {
        return this.assets;
      }
      const layer = this.activeLayer.toLowerCase();
      return this.assets.filter(a => {
        if (layer === 'environment' || layer === 'environmental') {
          return a.category === 'environmental' || a.category === 'environment';
        }
        return a.category === layer;
      });
    },

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

    /* ─── Staleness Visual Enforcer (DOM Level) ────────── */
    enforceStalenessVisuals(hotspot, badge, data) {
      if (data.stale || (Date.now() - new Date(data.last_updated).getTime() > 60000)) {
          hotspot.classList.add('is-stale', 'st-hotspot-stale');
          if (badge) {
              badge.textContent = `LAST UPDATED ${this.formatTimeAgo(data.last_updated).toUpperCase()}`;
              badge.className = 'bg-status-stale text-on-surface-variant px-space-xs py-space-2xs rounded font-label-xs';
          }
      } else {
          hotspot.classList.remove('is-stale', 'st-hotspot-stale');
      }
    }
  };
}
