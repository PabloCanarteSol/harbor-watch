# harbor-watch

Track AIS ships entering Port of A Coruna via HackRF SDR. Posts updates with map images to X (Twitter).

## Features
- **AIS signal captu** using gr-air-modes on 162 MHz band
- **Geofence detection** for harbor entrance + docking zones
- **Large ship filtering** -- only tracks vessels worth reporting (>500 GRT, no ferries)
- **Map image generation** -- OSM-based PNG with ship route overlay
- **Automatic X/Twitter posting** -- ship name, route image, docking status
- Web scraping data enrichment from MarineTraffic/VesselFinder

## Tech Stack
Python 3.10+ | gr-air-modes (HackRF) | SQLite | Pillow | BeautifulSoup4

## Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/PabloCanarteSol/harbor-watch.git
cd harbor-watch 
```

### 2. Run setup script (handles venv + deps)

```bash
./setup.sh
```

This will:
- Create a Python virtualenv (`.venv`)
- Install production deps (`requests`, `beautifulsoup4`, `Pillow`, etc.)
- Install test deps (`pytest`))
- Copy `.env.example -> .env` (if needed)

### 3. Configure your environment

Edit `.env` with your X/Twitter API keys and any optional settings.

| Var | Required | Purpose |
|-----|----------|---------| 
| `X_BEARER_TOKEN` | Yes | X API token for posting |
| `X_API_KEY` | Yes | X OAuth 1.0a consumer key |
| `X_API_SECRET` | Yes | X OAuth 1.0a secret |
| `X_ACCESS_TOKEN` | Yes | User access token |
| `X_ACCESS_TOKEN_SECRET` | Yes | User access secret |

### 4. Run the daemon

```bash
source .venv/bin/activate 
python3 main.py
```

Or one-liner:
```bash
.venv/bin/python main.py
```

## Hardware & Prerequisites

- Raspberry Pi 3 (or any Linux machine with network)
- HackRF One connected via USB or SDR dongle
- gr-air-modes installed locally
   - See: https://github.com/antirez/gr-air-modes 
   - Or from package manager: sudo apt install gr-air-modes

## Project Structure

See full tree in repo root directory listing above.

Key files:
- setup.sh            Run this first (venv + deps auto)
- config.py           Harbor coords, freq, range config
- main.py             Daemon orchestrator loop entrypoint point overall today...)

## Running Tests

Install test deps first if not already setup:

```bash
./setup.sh
python3 -m pytest tests/ -v 
```

Or one-liner after venv activation:
``bash
.venv/bin/python -m pytest tests/ -v
```

## Contributing

PRs welcome! See [PULL_REQUEST_TEMPLATE](.github/PULL_REQUEST_TEMPLATE.md) for guidelines.

### Quick Check Before Pushing

```bash 
./setup.sh
.venv/bin/python -m pytest tests/ -v 
```

## License

MIT
