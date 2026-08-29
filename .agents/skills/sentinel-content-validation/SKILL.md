---
name: sentinel-content-validation
description: Validate RheinShield Sentinel analytics, hunts, workbooks, automation rules, playbooks, and deterministic fixtures without requiring Azure.
---

# RheinShield Sentinel validation

Run `python tools/detection-test-harness/validate.py` from the repository root. Treat malicious and benign fixture expectations separately; never describe fixture precision or recall as production efficacy.

Check every rule for an ID, current API decision, KQL query, severity, tactics, entity mapping, table dependency, false-positive guidance, and tuning owner. Confirm automation actions remain disabled or dry-run unless explicitly scoped to disposable lab entities. Record counts only from generated evidence in `artifacts/evidence/detection-test-results.json`.
