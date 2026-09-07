# shared/constants/thresholds.py
"""
Physical and Operational Engineering Thresholds for Antarctic Stations.
Ground truth for rules engine, digital twin visualization, and alert triggers.
"""

# Electrical Microgrid Limits (kW)
BHARATI_MAX_GENERATION_KW = 340.0
BHARATI_NORMAL_LOAD_KW = 220.0
MAITRI_MAX_GENERATION_KW = 250.0
MAITRI_NORMAL_LOAD_KW = 160.0

# Energy Storage (%)
BATTERY_SOC_MIN_PCT = 25.0
BATTERY_SOC_CRITICAL_PCT = 15.0
BATTERY_SOC_NORMAL_PCT = 85.0

# Fuel Reserves (Days & Litres)
FUEL_RESERVE_WARNING_DAYS = 30.0
FUEL_RESERVE_CRITICAL_DAYS = 10.0
FUEL_STORAGE_CAPACITY_L_BHARATI = 120000.0
FUEL_STORAGE_CAPACITY_L_MAITRI = 80000.0

# Life Support & Thermal Limits (Celsius)
INDOOR_TEMP_TARGET_C = 21.0
INDOOR_TEMP_MIN_WARNING_C = 15.0
INDOOR_TEMP_CRITICAL_C = 5.0
OUTDOOR_TEMP_BLIZZARD_C = -35.0
GENERATOR_TEMP_MAX_C = 95.0

# Meteorological Storm Limits
WIND_SPEED_WARNING_MPS = 18.0   # ~65 km/h
WIND_SPEED_BLIZZARD_MPS = 25.0  # ~90 km/h (Storm condition)
WIND_SPEED_HURRICANE_MPS = 32.0 # ~115 km/h (Catastrophic polar gale)

# Telemetry Staleness (Seconds)
STALENESS_WARNING_SECONDS = 300   # 5 minutes
STALENESS_CRITICAL_SECONDS = 900  # 15 minutes
