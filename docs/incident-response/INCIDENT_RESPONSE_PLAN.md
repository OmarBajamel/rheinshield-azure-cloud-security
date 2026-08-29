# Incident response plan

## Severity and command

High incidents involving privileged identity, control weakening or suspected restricted data trigger the Incident Commander, SOC Lead, platform/workload owners, CISO, DPO/legal consultation and management liaison. Roles are separated: the Incident Commander decides priorities; analysts investigate; technical owners execute approved changes; the evidence custodian maintains chain and sanitization.

## Lifecycle

1. Prepare: contacts, access, evidence storage, KQL, playbooks, recovery and notification decision trees.
2. Detect/triage: validate telemetry, deduplicate, assign severity, clock, owner and legal-impact question.
3. Contain: prefer reversible, narrowly scoped actions; dry-run by default; protect logging and identity first.
4. Eradicate: remove unauthorized credentials/configuration and redeploy trusted baselines.
5. Recover: restore by BIA priority, validate health/control coverage and observe.
6. Learn: root cause, metrics, evidence closure, control improvements and executive acceptance.

Evidence uses UTC, stable IDs, SHA-256, source/provenance and access control. Raw tenant evidence remains ignored/private; public records are sanitized and separately hashed.
