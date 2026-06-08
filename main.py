# Harbor Watch - Main entry point
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime as _dt, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from data.db import AISDB, init_db, last_lat
from src.ais_parser import AisParser
from src.geofence import is_inside_geofence, is_in_docking_zone
from src.map_generator import generate_map
from src.scraper import lookup_vessel
from src.twitter_poster import TwitterPoster

_tw: TwitterPoster | None = None
DB: AISDB | None = None


def get_tw():
    global _tw
    if _tw:
        return _tw
    kw = {}
    pairs = [
        (os.getenv("X_BEARER_TOKEN"), "bearer_token"),
        (os.getenv("X_API_KEY"), "api_key"),
        (os.getenv("X_API_SECRET"), "api_secret"),
        (os.getenv("X_ACCESS_TOKEN"), "access_token"),
        (os.getenv("X_ACCESS_TOKEN_SECRET"), "ats"),
    ]
    for v, k in pairs:
        if v:
            kw[k] = v
    _tw = TwitterPoster(**kw)
    return _tw


class ShipTracker:
    """Track ships entering / docking harbor."""

    def __init__(self):
        self.rp: dict[str, _dt] = {}
        self.sr: dict[str, _dt] = {}
        self._kip: set[str] = set()
        self._dm: set[str] = set()

    def sp(self, msi: str) -> bool:
        now = _dt.now()
        last = self.rp.get(msi)
        if not last:
            return True
        delta = (now - last).total_seconds()
        self.rp[msi] = now
        return delta > 60

    def pm(self, msi: str) -> bool:
        last = self.sr.get(msi)
        if not last:
            return True
        delta = (_dt.now() - last).total_seconds()
        self.sr[msi] = _dt.now()
        return delta > 30


class ProcMgr:
    """Manage gr-air-modes process."""

    def __init__(self, rx_f: int):
        self.cmd: list[str] = [
            config.AIR_MODES_BIN,
              "-f", str(config.RX_FREQ),
              "-g", "16",
              "-s", "2M",
              "--ais",
           ]
        self.p: subprocess.Popen | None = None


    def start(self) -> bool:
        if self.p and self.p.poll() is None:
            return True
        self.p = subprocess.Popen(
            self.cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        logger.info("Started %s pid=%d", "air_modes", self.p.pid)
        return True

    def stop(self):
        if not self.p:
            return
        try:
            self.p.terminate()
            _wait_term(self.p)
        except Exception as e:
            logger.warning("Stop error: %s", e)
        finally:
            logger.info("Stopped %s", "air_modes")

    def alive(self) -> bool:
        if not self.p:
            return False
        rc = self.p.poll()
        if rc is None:
            return True
        try:
            self.start()
            return True
        except Exception as e:
            logger.error("Restart failed: %s", e)
        return False

    @staticmethod
    def chk():
      cmd = config.AIR_MODES_BIN
      if not os.path.isfile(cmd):
          logger.warning(
              "%s not found - install gr-air-modes first!",
               "air_modes",
           )
          sys.exit(1)


def _wait_term(p: subprocess.Popen, t=20):
    d = 0
    while d < t and p.poll() is None:
        time.sleep(0.3)
        d += 0.3
    if d >= t and p.poll() is None:
        p.kill()


class AISDaemon:
    """Main daemon loop."""

    def __init__(self):
        self.trk = ShipTracker()
        self.prc = ProcMgr(config.RX_FREQ)
        self.parser = AisParser()
        if DB is None:
            init_db()
        self._load_cached()

    def _load_cached(self):
        for row in AISDB.get_recent(hours=config.RECENT_HRS):
            msi = row.get("msi")
            ts  = parse_ts(row.get("ts"))
            if msi and ts:
                self.trk.rp[msi] = ts
                self.trk._kip.add(msi)

    def run(self):
        ProcMgr.chk()
        self.prc.start()
        logger.info("Monitoring %s [PID %d]", "air_modes", self.prc.p.pid)
        buf = ""
        while True:
            line = decode_line(self.prc.p.stdout)
            if not line:
                time.sleep(0.1)
                continue
            buf += line
            while "\n" in buf:
                ln, buf = buf.split("\n", 1)
                self.after_fix(ln)

    def after_fix(self, js: str):
        rec = None
        try:
            rec = json.loads(js)
        except (json.JSONDecodeError, ValueError):
            return
        lat = rec.get("lat")
        lon = rec.get("lon")
        if not lat or not lon:
            return
        msi = str(rec.get("msi", ""))
        if len(msi) < 3:
            return
        inside = is_inside_geofence(lat, lon)
        if not inside:
            self.trk._kip.discard(msi)
            if msi in self.trk.rp:
                del self.trk.rp[msi]
            return
        ts     = rec.get("ts", 0) or 0
        msg_ty = int(rec.get("msg_type", 0))
        dock   = is_in_docking_zone(lat, lon)
        AISDB.insert(msi=msi, name=rec.get("name", "?"), lat=lat, lon=lon, ts=ts)
        if msg_ty != 1 or lat == last_lat(msi):
            return
        rec["cog"] = float(rec.get("cog", 0) or 0)
        rec["sog"] = float(rec.get("sog", 0) or 0)
        if not self.trk.sp(msi):
            return
        img_dir   = os.path.join(os.getcwd(), "data", "img")
        os.makedirs(img_dir, exist_ok=True)
        fp = generate_map(
            img_dir=img_dir,
            lat=lat,
            lon=lon,
            cog=float(rec.get("cog", 0) or 0),
            sog=float(rec.get("sof", 0) or 0),
        )
        info     = lookup_vessel(msi)
        tw       = get_tw()
        if tw and post_entry(tw, msi, rec.get("name", "?"), info, fp):
            logger.info("Posted entry for %s", msi)
        self.trk._kip.add(msi)


def decode_line(stream) -> str:
    try:
        return stream.readline().decode(errors="replace")
    except Exception:
        return ""


def parse_ts(raw):
    """Convert timestamp to datetime object."""
    if raw is None or raw == "":
        return None
    try:
        return _dt.fromtimestamp(int(raw))
    except (ValueError, TypeError):
        return None   # noqa E501


def post_entry(tw, msi: str, name: str, info, img_path: str) -> bool:
    """Build ship entry tweet + optional scrapes info."""
    txt = base = ""
    extra = []
    if info:     # noqa E501
        for field_name in ["type", "grot", "flag"]:      # noqa E742
            v = info.get(field_name)       # noqa: E742
            if v:    # noqa E501
                extra.append(f"{field_name}={v}")         # noqa:E501
    base += f"{name or '?'} (MSI {msi})"    # noqa E501
    txt += base + " " + ", ".join(extra)     # noqa E501
    tw.post_tweet(txt, image_path=img_path)     # noqa:E501
    return True


if __name__ == "__main__":    # noqa: E501
    d = AISDaemon()
    d.run()

