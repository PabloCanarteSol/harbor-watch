# Copilot Instructions for harbor-watch

## Context
AIS ship tracking daemon for Port of A Coruña. Uses HackRF SDR to capture AIS signals, filters large transatlantic ships, generates map images, and posts updates to X/Twitter.

## Tech Stack
- Python 3.10+
- gr-air-modes (for AIS signal processing via HackRF)
- SQLite for local data storage
- BeautifulSoup4 for web scraping (MarineTraffic/VesselFinder)
- Pillow for map image generation

## Run Commands
```bash
pip install -r requirements.txt
python3 main.py           # Full daemon loop
python3 -m py_compile src/*.py  # Syntax check only
```

## Code Style
- Snake_case variable/function names
- Type hints where meaningful
- Error handling: try/except with logging
- No bare except blocks - use specific exceptions
- Max line length: ~100 chars acceptable

## Key Dependencies
See `requirements.txt`. Don't add new deps without good reason.

## Architecture Overview
- `config.py` — Hardcoded params (Port of A Coruña, freq 162MHz)
- `src/ais_parser.py` — Parses JSON output from gr-air-modes with rate limiting
- `src/geofence.py` — Haversine distance + polygon checks for harbor/docking zones
- `src/map_generator.py` — Generate PNG maps with ship route overlays (OSM-based tiles)
- `src/scraper.py` — MarineTraffic/VesselFinder web scraping for vessel details + photos
- `src/twitter_poster.py` — Post updates via X/Twitter API v2 (bearer+OAuth tokens)
