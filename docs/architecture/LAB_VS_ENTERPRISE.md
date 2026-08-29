# Lab versus enterprise

| Concern | Single-subscription lab | Enterprise reference |
|---|---|---|
| Validation | `PLAN_VALIDATED` by mocked lab plan; no live apply | `READY_NOT_AUTHENTICATED`; static/provider validation only |
| Scope | Dedicated project resource group | Dedicated management-group hierarchy and subscriptions |
| Network | Compact segmented VNet | Hub/spoke with shared connectivity and private DNS |
| Policy | Audit/deny mix safe for teardown | Centrally assigned, stronger deny and remediation |
| Identity | Templates and project RBAC | PIM, access reviews, workload federation at scale |
| Resilience | Backup design, no paid DR deployment | Zone/region design with tested recovery |
| SOC | Content and fixtures | Central Sentinel workspace and operational process |
| Cost | Hard ceiling €20, 24-hour expiry | Budgeted service ownership and FinOps |

The lab is evidence of safe implementation mechanics, not a claim that a single subscription is a production landing zone.
