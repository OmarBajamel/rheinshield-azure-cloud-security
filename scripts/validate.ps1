$ErrorActionPreference = 'Stop'
npm run typecheck
npm run lint
python tools/detection-test-harness/validate.py
python tools/sanitization/scan_public.py
