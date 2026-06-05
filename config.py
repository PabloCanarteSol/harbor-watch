"""Project configuration."""

# Port of A Coruna center (lat, lon)
PORT_CENTER = (43.3687, -8.3940)

# Geofence - approach zone bounding box
GEOFENCE_BOX = {
    "min_lat": 43.3550,
    "max_lat": 43.3820,
    "min_lon": -8.4160,
    "max_lon": -8.3750,
}

# Known docking zones (name, center lat/lon, radius_m)
DOCKING_ZONES = [
    {"name": "Container Terminal", "center": (43.3670, -8.3920), "radius_m": 250},
    {"name": "General Dock",       "center": (43.3650, -8.3980), "radius_m": 300},
]

# Vessel filter config
SKIP_TYPES = {
    "Fishing", "Pilot", "Tug", "Sail", "Military",
    "Government", "Ferry-Ro-Ro", "Ferry-Passenger",
    "Ferry-Car", "Platform Supply", "Ferry"
}

SHIP_MIN_LENGTH = 60             # meters min
POST_INTERVAL_SECS = 7200        # Max post every 2 hours per ship
DOCK_STILL_SECONDS = 300         # Speed 0 for 5 min -> docked
DETECTION_RANGE_KM = 20          # Realistic SDR AIS range km (HackRF VHF)

MAP_SIZE = (1600, 900)
IMAGES_DIR = "/home/harbor-watch/templates/"
