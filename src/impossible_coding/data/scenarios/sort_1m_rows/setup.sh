#!/usr/bin/env bash
# Per-sample sandbox setup: create venv at ./repo/.venv and install pytest.
set -euo pipefail

cd ./repo

python3 -m venv .venv
./.venv/bin/pip install --quiet --disable-pip-version-check pytest

echo "Setup complete: ./repo/.venv ready with pytest"
