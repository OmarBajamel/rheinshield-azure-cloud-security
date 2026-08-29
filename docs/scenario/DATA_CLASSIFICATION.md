# Data classification

| Level | Examples | Handling |
|---|---|---|
| PUBLIC | public-demo metrics, sanitized diagrams, release manifests | approved publication; integrity hash |
| INTERNAL | architecture decisions, operating metrics, non-sensitive configuration | workforce access; logged changes |
| CONFIDENTIAL | customer accounts, orders, employee identity, private endpoints | encryption, need-to-know RBAC, monitored access, retention limit |
| RESTRICTED | secrets, authentication material, raw incident evidence, tenant/subscription identifiers | Key Vault or ignored private evidence; privileged access; no public release |

Synthetic values inherit a label describing the represented class but remain explicitly `DataClassification=Synthetic` in the lab.
