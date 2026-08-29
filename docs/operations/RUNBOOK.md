# Operations runbook

Use public-demo by default. Generate data, validate Sentinel, run tests, and build before opening the dashboard. Azure operations require `azure-cost-safe-deploy`, a dedicated `rg-rheinshield-*` scope, and a saved teardown plan. Triage alerts through `INCIDENT_TRIAGE_RUNBOOK.md`; never execute containment on a real identity. After any lab proof, sanitize evidence, destroy the project group, verify absence, and remove federated credentials not intentionally retained.
