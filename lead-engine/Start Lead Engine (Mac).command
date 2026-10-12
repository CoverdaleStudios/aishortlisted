#!/bin/bash
# Double-click to start the Bin Caddie Lead Engine. First run installs what it needs (1-2 minutes).
cd "$(dirname "$0")" || exit 1
[ -d lead-engine ] && cd lead-engine
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is not installed. Download it from https://www.python.org/downloads/ , install it, then double-click this file again."
  open "https://www.python.org/downloads/" 2>/dev/null
  read -r -p "Press Enter to close." _; exit 1
fi
if [ ! -x .venv/bin/python ]; then
  echo "First-time setup: installing (this takes a minute or two)..."
  python3 -m venv .venv || { echo "Could not create the environment."; read -r -p "Press Enter to close." _; exit 1; }
  .venv/bin/python -m pip install --quiet --upgrade pip
  .venv/bin/python -m pip install --quiet -r requirements.txt || { echo "Install failed - check your internet connection."; read -r -p "Press Enter to close." _; exit 1; }
fi
.venv/bin/python -m leadengine.cli init >/dev/null
echo "Opening http://127.0.0.1:5050 in your browser. Keep this window open while you use it."
.venv/bin/python -m leadengine.cli serve --open
