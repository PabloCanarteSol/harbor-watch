#!/usr/bin/env bash
set -e

echo "=== harbor-watch setup ===" 

# Check Python version
python3 --version || { echo "ERROR: python3 required"; exit 1; } 

# Create virtualenv if it does not exist
VENV_DIR="$(pwd)/.venv" 
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating venv..." 
    python3 -m venv "$VENV_DIR"
fi

# Activate + install deps
. "$VENV_DIR/bin/activate" 
echo "Installing production deps..." 
pip install --quiet --upgrade pip 
pip install --quiet -r requirements.txt || echo "WARN: some prod deps failed (optional)" 

# Check test deps too
[ -f requirements-test.txt ] && pip install --quiet -r requirements-test.txt || true 

.env check
if [ ! -f .env ]; then 
    cp .env.example .env 
    echo "Created .env from template — edit it now!" 
else
    echo ".env exists - ok" 
fi


# Show summary
echo "=== Setup done === "
echo "To run: source .venv/bin/activate && python3 main.py "
