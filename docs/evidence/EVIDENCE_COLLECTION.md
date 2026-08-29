# Evidence collection

`tools/evidence-collector/collect.py` inventories public JSON/CSV results, hashes every file, and records commit, timestamp, provenance, classification, and privacy status. Offline collection includes Terraform/tool availability, policy controls, Sentinel content, deterministic telemetry, tests, cost/lifecycle state, and publication evidence.

Live collection, when authenticated, is restricted to project-tagged resources and writes raw output only below ignored `evidence/private/` or `.private/`. A sanitizer produces stable aliases before anything is copied to `artifacts/evidence/`. No raw portal export enters screenshots or releases.
