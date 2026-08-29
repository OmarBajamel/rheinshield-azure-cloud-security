#!/usr/bin/env bash
set -euo pipefail
command -v node >/dev/null || { echo 'Node.js 22+ is required.' >&2; exit 1; }
command -v python >/dev/null || { echo 'Python 3.11+ is required.' >&2; exit 1; }
npm ci
python -m pip install -e '.[dev]'
echo 'RheinShield bootstrap complete.'
