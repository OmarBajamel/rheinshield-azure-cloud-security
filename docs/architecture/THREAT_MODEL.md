# Threat model

## Method

STRIDE-style threats are prioritized through the risk register's 5×5 likelihood-impact model. Trust boundaries are public user → application ingress → workload identity → data services; GitHub → federated identity → project resource group; and telemetry → SOC → evidence export.

| Threat | Boundary | Primary controls | Detection | Residual concern |
|---|---|---|---|---|
| Password spraying | User / Entra | MFA and CA template | RS001–RS003 | License-dependent identity risk |
| Privilege escalation | Identity / control plane | PIM, SoD, time-bound roles | RS004–RS006 | Live PIM not validated |
| Public exposure | Network / data | NSG and policy baseline | RS007, RS009 | Private endpoint DNS needs live proof |
| Telemetry suppression | Workload / SOC | Diagnostic policy and separate ownership | RS008 | Cross-workspace resilience |
| Secret theft | CI / Azure | OIDC, managed identity, Key Vault RBAC | RS005, RS013 | Bootstrap role lifecycle |
| Collection/exfiltration | Application / storage | Least privilege and logging | RS010, RS012 | Production volume tuning |

All simulated entities are synthetic and isolated from real systems.
