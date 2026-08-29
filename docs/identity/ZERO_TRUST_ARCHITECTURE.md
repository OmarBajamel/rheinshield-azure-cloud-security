# Zero Trust architecture

RheinShield applies **verify explicitly**, **least privilege**, and **assume breach** across workforce, guest, workload, CI/CD, and emergency access. Entra is the identity control plane; access decisions combine user/workload identity, target resource, authentication strength, device/session state, and risk signals when licensed.

## Personas and boundaries

- Platform and security administrators: eligible privilege, approval, MFA, short activation and protected admin session.
- SOC analysts: Sentinel Reader/Responder split; no infrastructure deployment permission.
- Workload operators and developers: application resource-group roles only; production duties separated.
- Auditors: time-bound read access with evidence export, never control-plane write.
- Contractors/suppliers: sponsor, expiry, access review, terms, and dedicated groups.
- Workloads and GitHub Actions: managed/federated identities, narrow audience and scope, no password or client secret.
- Emergency access: two cloud-only identities, independently secured and monitored, excluded only from policies that could cause lockout.

All tenant-changing examples are templates. No real account, tenant-wide policy, or privileged assignment is created by the default workflow.
