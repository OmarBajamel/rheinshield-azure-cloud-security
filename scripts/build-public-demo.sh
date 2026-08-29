#!/usr/bin/env bash
set -euo pipefail
python tools/synthetic-telemetry/generate.py
npm run build
