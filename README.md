# Harbor Watch — AIS Ship Tracking for A Coruña

Detects large transatlantic ships entering/docking at the Port of A Coruña using a HackRF SDR, scrapes vessel data from MarineTraffic + VesselFinder, generates a map image of the ship's route, and posts updates to X (Twitter).

## Hardware Setup

- **Raspberry Pi 3** with [HackRF One](https://github.com/mosmit/gnuradio/blob/master/gr-hier2/docs/INSTALL.md)
- [GNU Radio](http://gnuradio.org/) + `gr-air-modes`
- AIS mode: decode on 162 MHz

### Start gr-air-modes

```sh
sudo air_modes -v --lat 43.3705 --lon -8.3950 \
  -f 162e6 --gain 32 --json --range 0 \
  -o $HOME/harbor-watch/data/messages.csv
```

## Installation

\`\`\`sh
pip3 install -r requirements.txt
cp .env.example .env
# Fill in your X API credentials in .env
python3 src/main.py\`