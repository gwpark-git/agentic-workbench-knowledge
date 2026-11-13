#!/bin/sh
set -eu
# Invoke from test_local/. Existing named simulation outputs will be overwritten.
# Use a fresh copy when retaining original results for comparison.
python3 scripts/limited.py verification env/venv/bin/python scripts/verify.py > logs/verification-repeat.log 2>&1
python3 scripts/limited.py main_simulations env/venv/bin/python scripts/study.py main > logs/main-repeat.log 2>&1
python3 scripts/limited.py timestep_simulations env/venv/bin/python scripts/study.py timestep > logs/timestep-repeat.log 2>&1
python3 scripts/limited.py analysis env/venv/bin/python scripts/analyze.py > logs/analysis-repeat.log 2>&1
