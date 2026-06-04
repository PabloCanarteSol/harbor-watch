# Geofence detection for Port of A Coruna
import logging, math, sys

sys.path.insert(0, str(__file__).rsplit("/", 2)[0])
from config import GEOFENCE_BOX, DOCKING_ZONES, PORT_CENTER

logger = logging.getLogger(__name__)


def haversine(lat1, lon1, lat2, lon2):
    # Distance in meters between two lat/lon points
    R = 6371001
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * 2 * math.asin(min(1.0, math.sqrt(a)))


def is_inside_geofence(lat, lon):
    # True if lat/lon inside the port approach geofence box
    return (GEOFENCE_BOX["min_lat"] <= lat <= GEOFENCE_BOX["max_lat"] and
            GEOFENCE_BOX["min_lon"] <= lon <= GEOFENCE_BOX["max_lon"])


def is_in_docking_zone(lat, lon):
    # Return zone name or None
    for zone in DOCKING_ZONES:
        zlat, zlon = zone["center"]
        dist = haversine(lat, lon, zlat, zlon)
        if dist <= zone["radius_m"]:
            logger.info("Ship at %s (%.0fm from center)", zone["name"], dist)
            return zone["name"]
    return None


def port_distance(lat, lon):
    # Meters from PORT_CENTER
    return haversine(lat, lon, PORT_CENTER[0], PORT_CENTER[1])
