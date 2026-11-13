#!/bin/sh
set -eu
# Run from hard_sphere_extension/. Existing named outputs are overwritten.
TASK_PYTHON="$(python3 -c 'from pathlib import Path; print(Path.cwd().parent/"env/venv/bin/python")')"
python3 scripts/limited.py verification "$TASK_PYTHON" scripts/verify.py > logs/verification-repeat.log 2>&1
python3 scripts/limited.py main_simulations "$TASK_PYTHON" scripts/hs_mc.py main > logs/main-repeat.log 2>&1
python3 scripts/limited.py size_simulations "$TASK_PYTHON" scripts/hs_mc.py size > logs/size-repeat.log 2>&1
python3 scripts/limited.py proposal_simulations "$TASK_PYTHON" scripts/hs_mc.py proposal > logs/proposal-repeat.log 2>&1
python3 scripts/limited.py analysis "$TASK_PYTHON" scripts/analyze.py > logs/analysis-repeat.log 2>&1
