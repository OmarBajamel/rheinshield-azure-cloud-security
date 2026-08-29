---
name: azure-cost-safe-deploy
description: Plan or deploy the RheinShield Azure lab while enforcing its project scope, cost ceiling, evidence, and teardown invariants.
---

# RheinShield cost-safe Azure deployment

Operate only on resource groups whose resolved name starts with `rg-rheinshield-`. Read `docs/cost/COST_GUARD.md` and `artifacts/evidence/resource-lifecycle.json` before any mutation.

Require all of these before apply: an authenticated subscription context, no unexpected prefix collision, a current estimate below `RHEINSHIELD_MAX_INCREMENTAL_COST_EUR`, an expiry timestamp, and a saved destruction plan. Stop if any gate fails. Never broaden scope to tenant root, an existing management group, or unrelated identity policy.

Use report-only identity templates and minimal synthetic telemetry. After capture, sanitize evidence, destroy billable resources, query for remaining project-tagged resources, and record the result. Absence of live access is `READY_NOT_AUTHENTICATED`, not a failed deployment or approval request.
