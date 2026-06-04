# Scrape vessel data + photo from MarineTraffic and VesselFinder
import re
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")


def scrape_marinetraffic(name, mmsi=None):
    url = "https://www.marinetraffic.com/en/" + requests.utils.quote(name)
    logger.info("Scraping MarineTraffic: %s", name)
    try:
        resp = requests.get(url, headers={"User-Agent": UA}, timeout=15)
        resp.raise_for_status()
    except Exception as exc:
        logger.warning("MT scrape failed: %s", exc)
        return None

    data = {"source": "marinetraffic", "name": name}
    m = re.search(r'IMO[:\s]*(\d{6,7})', resp.text)
    if m:
        data["imo"] = m.group(1)
    gt = re.search(r'Gross[^<]*>(\d+)', resp.text)
    if gt:
        data["gross_tons"] = int(gt.group(1))
    dims = re.search(r'(\d{2,3})\s*x\s*(\d{1,3})', resp.text)
    if dims:
        data["length_m"] = int(dims.group(1))
        data["width_m"] = int(dims.group(2))
    logger.info("MT result: %d fields", len(data))
    return data if len(data) > 2 else None


def scrape_vesselfinder(name, mmsi=None):
    url = "https://www.vesselfinder.com/search/" + requests.utils.quote(name)
    logger.info("Scraping VesselFinder: %s", name)
    try:
        resp = requests.get(url, headers={"User-Agent": UA}, timeout=15)
        resp.raise_for_status()
    except Exception as exc:
        logger.warning("VF scrape failed: %s", exc)
        return None

    soup = BeautifulSoup(resp.text, "lxml")
    data = {"source": "vesselfinder", "name": name}
    for a_tag in soup.select("a"):
        href = a_tag.get("href", "")
        m = re.search(r'/vessel/?(\d{6,7})', href)
        if m:
            data["imo"] = m.group(1)
            break
    logger.info("VF result: %d fields", len(data))
    return data if len(data) > 2 else None


def lookup_vessel(name, mmsi=None):
    data = {}
    mt = scrape_marinetraffic(name, mmsi)
    if mt:
        data.update(mt)
    if not data or "imo" not in data:
        vf = scrape_vesselfinder(name, mmsi)
        if vf:
            data.update(vf)
    return data


def get_photo_url(imo=None, name=None):
    # VesselFinder direct thumbnail by IMO (most reliable!)
    if imo:
        url = f"https://img.vesselfinder.com/ship/{imo}.jpg"
        prep = requests.Request("HEAD", url).prepare()
        try:
            resp = requests.Session().send(prep, timeout=5)
            if resp.ok:
                return url
        except Exception:
            pass
    # MarineTraffic fallback - search for photo tag
    try:
        resp = requests.get(
            "https://www.marinetraffic.com/en/"
            + requests.utils.quote(name or ""),
            headers={"User-Agent": UA}, timeout=15)
        soup = BeautifulSoup(resp.text, "lxml")
        for img in soup.select("img"):
            src = img.get("src", "") or ""
            if src and any(kw in src.lower()
                            for kw in ["ship", "photo"]):
                return src
    except Exception as exc:
        logger.warning("Photo lookup failed: %s", exc)
    return None
