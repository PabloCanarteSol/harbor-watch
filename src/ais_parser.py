# AIS message parser for gr-air-modes JSON output
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


NAV_STATUS_MAP = {
    0: "Under way (using engine)",
    1: "At anchor",
    2: "Moored",
    3: "Not defined (AIS v5+)",
    4: "Restricted manoeuvre",
}


class AisMessage:
    def __init__(self, mmsi, lat, lon, speed=None,
                 course=None, name="Unknown", imo=None,
                 typename="Unknown", length=None, width=None,
                 destination="", nav_status_code=None):
        self.mmsi = int(mmsi)
        self.lat = float(lat)
        self.lon = float(lon)
        self.speed = speed
        self.course = course
        self.name = name
        self.imo = imo
        self.typename = typename
        self.length = length
        self.width = width
        self.destination = destination
        self.navigation_status = NAV_STATUS_MAP.get(nav_status_code, "Unknown")
        self.timestamp = datetime.now()

    @property
    def is_transatlantic_candidate(self):
        if self.typename and self.typename.lower().startswith("fishing"):
            return False
        if self.typename and any(w in self.typename.lower()
                                 for w in ("pilot", "tug")):
            return False
        if self.length is not None and self.length < 60:
            return False
        return True

    def __repr__(self):
        return (f"AisMessage(MMSI={self.mmsi}, name={self.name!r}, "
                f"imo={self.imo}, lat={self.lat:.4f}, "
                f"lon={self.lon:.4f}, speed={self.speed}kn")


class AisParser:
    @staticmethod
    def parse_line(line):
        try:
            data = json.loads(line.strip())
            data["timestamp"] = datetime.now()
            return data if isinstance(data, dict) else None
        except (json.JSONDecodeError, ValueError):
            return None

    @staticmethod
    def parse_raw(raw_json):
        if not raw_json or "mms" not in raw_json:
            return None

        speed_val = float(raw_json["speed"]) if raw_json.get("speed") else None
        course_str = str(raw_json.get("course", "-1"))
        course_val = (float(course_str) if course_str.strip() != "-1" else None)
        imo_str = str(raw_json.get("imo", ""))

        return AisMessage(
            mmsi=raw_json["mms"],
            lat=float(raw_json.get("lat", 0)) / 1e7,
            lon=float(raw_json.get("lon", 0)) / 1e6,
            speed=speed_val,
            course=course_val,
            name=raw_json.get("name", "Unknown"),
            imo=(imo_str if imo_str else None),
            typename=raw_json.get("typename", "Unknown"),
            length=raw_json.get("length"),
            width=raw_json.get("width"),
            destination=raw_json.get("destination", ""),
            nav_status_code=int(raw_json.get("navstatus", -1)),
        )

    def parse_file(self, filepath):
        msgs = []
        try:
            with open(filepath) as fh:
                for line in fh:
                    raw = self.parse_line(line)
                    if raw:
                        m = self.parse_raw(raw)
                        if m:
                            msgs.append(m)
        except FileNotFoundError:
            logger.warning("File not found: %s", filepath)
        return msgs

    def parse_stream(self, lines):
        results = []
        for line in lines:
            raw = self.parse_line(line)
            if raw:
                m = self.parse_raw(raw)
                if m:
                    results.append(m)
        return results
