$ErrorActionPreference = 'Stop'
npm run release:check
python tools/release/build_release.py
python tools/sanitization/scan_public.py
python tools/evidence-collector/collect.py
