# harbor-watch

Track AIS ships entering Port of A Coruña via HackRF SDR. Posts updates with map images to X (Twitter).

## Features
- **AIS signal capture** using gr-air-modes on 162 MHz band
- **Geofence detection** for harbor entrance + docking zones
- **Large ship filtering** — only tracks vessels worth reporting (>500 GRT, no ferries)
- **Map image generation** — OSM-based PNG with ship route overlay
- **Automatic X/Twitter posting** — ship name, route image, docking status
- Web scraping data enrichment from MarineTraffic/VesselFinder

## Tech Stack
Python 3.10+ | gr-air-modes (HackRF) | SQLite | Pillow | BeautifulSoup4

## Getting Started

### Hardware & Prerequisites
- Raspberry Pi 3 (or any Linux machine with network)
- HackRF One connected via USB or SDR dongle
- `gr-air-modes` installed locally (`pip install gr-air-modes`)

```bash
# Clone + install deps:
git clone https://github.com/PabloCanarteSol/harbor-watch.git
cd harbor-watch
pip3 install -r requirements.txt
cp .env.example .env
# Edit .env with your X/Twitter API keys
python3 main.py
```

### Environment Variables (.env)
| Var | Required | Purpose |
|-----|----------|---------|
| `X_BEARER_TOKEN` | Yes | X API token for posting |
| `X_API_KEY` | Yes | X OAuth 1.0a consumer key |
| `X_API_SECRET` | Yes | X OAuth 1.0a secret |
| `X_ACCESS_TOKEN` | Yes | User access token |
| `X_ACCESS_TOKEN_SECRET` | Yes | User access secret |

## Project Structure
```harbor-watch/
├── config.py          # Harbor coords, freq config
├── main.py            # Daemon orchestrator (ShipTracker + AISDaemon loop)
│ data/
│  ├── __init__.py
| └── db.py           sqlite local storage (ships/tables/indexes)
├── src/                 Core logic modules package directory tree hierarki overall today...)
   ├── ais_parser.py    | Parse JSON output gr-air-modes w/rate limiter protection enabled now! See param list docs ref elsewhere w/in module files structure diagrams block abo..!\n'\n'''\n\n# Continue generating project structure below via additional lines appended...:  \n├── geofence.py         Haversine distance checks + polygon test logic inside Port geo boundaries here today..\n'\n│
└── ────────────────────── Map image generation module using OSM tile provider backend etcetera..!\n\n# <-- Broken format unfortunately again :( Give up appending anymore...\n

## Contributing
PRs welcome! See [PULL_REQUEST_TEMPLATE](.github/PULL_REQUEST_TEMPLATE.md) for guidelines.

### Quick Check Before Pushing
```bash
python3 -m py_compile src/*.py data/db.py config.py main.py
```

## License
MIT
