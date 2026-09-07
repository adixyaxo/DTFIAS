# shared/constants/stations.py
"""
Canonical station metadata for DTFIAS.
Used across app routers, templates, and engine services.
"""
from typing import TypedDict


class StationMetadata(TypedDict):
    id: str
    name: str
    full_name: str
    code: str
    grid_id: str
    callsign: str
    location: str
    region: str
    coordinates: str
    coordinates_short: str
    elevation: str
    established: int
    architecture: str
    architecture_subtitle: str
    foundation: str
    souls_total: int
    souls_winter: int
    souls_summer: int
    souls_active: int
    capacity_kw: float
    load_kw: float
    load_pct: float
    generator_models: str
    primary_link: str
    comms_sat: str
    export_prefix: str
    external_link_name: str
    external_link_coords: str
    emergency_zone: str
    locus_name: str
    twin_rev: str


STATIONS_CONFIG: dict[str, StationMetadata] = {
    "bharati": {
        "id": "bharati",
        "name": "Bharati",
        "full_name": "BHARATI POLAR RESEARCH STATION // DIGITAL TWIN CORE",
        "code": "IND-ANT-03",
        "grid_id": "IN-ANT-BHT-02-PWR",
        "callsign": "BHT-02",
        "location": "Larsemann Hills, Prydz Bay",
        "region": "Larsemann Hills",
        "coordinates": "69°24′28″S 76°11′14″E",
        "coordinates_short": "69°24'S, 76°11'E",
        "elevation": "35m ASL",
        "established": 2012,
        "architecture": "Bharati 3-Level Containerized Architecture",
        "architecture_subtitle": "134 Prefabricated ISO Container Units on Elevated Hydraulic Stilts",
        "foundation": "Hydraulic Stilt Elevation (3.4 bar balanced)",
        "souls_total": 24,
        "souls_winter": 24,
        "souls_summer": 47,
        "souls_active": 24,
        "capacity_kw": 340.0,
        "load_kw": 282.4,
        "load_pct": 83.0,
        "generator_models": "CAT C32 / Scania DC13 CHP Fleet",
        "primary_link": "Maitri Link (11°44′E)",
        "comms_sat": "GSAT-7A Ku-Band / ISRO-SCN",
        "export_prefix": "bharati",
        "external_link_name": "Maitri Link (11°44′E)",
        "external_link_coords": "70°46′S, 11°44′E",
        "emergency_zone": "Bharati Habitat",
        "locus_name": "Larsemann Hills Locus",
        "twin_rev": "REV 4.2",
    },
    "maitri": {
        "id": "maitri",
        "name": "Maitri",
        "full_name": "MAITRI POLAR RESEARCH STATION // DIGITAL TWIN CORE",
        "code": "IND-ANT-02",
        "grid_id": "IN-ANT-MTR-01-PWR",
        "callsign": "MTR-01",
        "location": "Schirmacher Oasis, Queen Maud Land",
        "region": "Schirmacher Oasis",
        "coordinates": "70°45′58″S 11°44′09″E",
        "coordinates_short": "70°46'S, 11°44'E",
        "elevation": "117m ASL",
        "established": 1989,
        "architecture": "Maitri Structural Steel Dual-Block Complex",
        "architecture_subtitle": "Reinforced Modular Steel Complex with Insulated Panels on Solid Bedrock",
        "foundation": "Solid Concrete Pier Footings on Schirmacher Bedrock",
        "souls_total": 18,
        "souls_winter": 18,
        "souls_summer": 45,
        "souls_active": 18,
        "capacity_kw": 250.0,
        "load_kw": 187.4,
        "load_pct": 75.0,
        "generator_models": "Kirloskar Polar 160 / Polar 125 & CAT Heavy",
        "primary_link": "Bharati Link (76°11′E)",
        "comms_sat": "GSAT-7A / Inmarsat Fleet",
        "export_prefix": "maitri",
        "external_link_name": "Bharati Link (76°11′E)",
        "external_link_coords": "69°24′S, 76°11′E",
        "emergency_zone": "Maitri Main Complex",
        "locus_name": "Schirmacher Oasis Locus",
        "twin_rev": "REV 2.1",
    },
}


def get_station_metadata(station_id: str) -> StationMetadata:
    """Retrieve canonical metadata for a given station ID, defaulting to Bharati."""
    return STATIONS_CONFIG.get(station_id.lower(), STATIONS_CONFIG["bharati"])
