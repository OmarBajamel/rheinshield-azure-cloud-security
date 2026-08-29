$ErrorActionPreference = 'Stop'
python tools/evidence-collector/collect.py
Write-Host 'Local public evidence collected. Live collectors require authenticated project scope and write only to ignored evidence/private/.'
