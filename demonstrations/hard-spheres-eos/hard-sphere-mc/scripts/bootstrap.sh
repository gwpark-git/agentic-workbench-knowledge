#!/bin/sh
set -eu
mkdir -p env/site logs tmp
python3 scripts/limited.py environment uv pip install --python /usr/bin/python3 --target env/site -r env/requirements-extension.lock > logs/bootstrap-repeat.log 2>&1
