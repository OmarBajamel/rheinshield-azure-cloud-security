# Test strategy

RheinShield tests behavior at the lowest useful layer and keeps live/cloud proof distinct from offline confidence.

- Terraform: format, provider initialization without backend, validate, native tests, and static security review when binaries are available.
- Sentinel/Bicep: schema, query metadata, malicious/benign fixtures, MITRE/entity mappings, JSON syntax, API versions, Bicep build, and dry-run safety.
- Python: unit and integration tests for the API, generators, reproducibility, sanitizer, and evidence exporter; Ruff and MyPy provide static gates.
- Dashboard: TypeScript, ESLint, structural unit tests, production build, browser route/language/mobile checks, console/network errors, and accessibility scan.
- Release: secret/PII patterns, public bundle, screenshots, tracked files, hashes, SBOM, archives, URLs, and fresh clone.

Unavailable tools are recorded as external limitations; their checks are never claimed as passing.
