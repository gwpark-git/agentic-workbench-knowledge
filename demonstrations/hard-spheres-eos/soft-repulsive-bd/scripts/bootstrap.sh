#!/bin/sh
set -eu
# Invoke from test_local/. All caches, temporary files, and installs stay here.
mkdir -p env tmp logs
python3 scripts/limited.py environment sh -c '
    uv venv env/venv --python /usr/bin/python3
    uv pip install --python env/venv/bin/python -r env/requirements.lock
' > logs/bootstrap.log 2>&1
