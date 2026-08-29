# Platform landing zone

Status: `READY_NOT_AUTHENTICATED`; static/provider validation passed, but no authenticated management-group plan ran. Tenant Root Group is explicitly out of scope, and the input accepts only a dedicated management-group ID named `rheinshield-*`.

| Layer | Enterprise reference | Owner | Evidence |
|---|---|---|---|
| Management | Log Analytics, Sentinel, policy, Defender posture | Security Platform | `infra/enterprise-reference/` |
| Connectivity | Hub/spoke, private DNS, egress control | Cloud Platform | `docs/architecture/NETWORK_ARCHITECTURE.md` |
| Identity | Entra groups, PIM, access reviews, workload federation | IAM | `identity/` |
| Online | Public commerce ingress, private application/data tiers | Product Platform | `infra/modules/workload/` |
| Corp | Private enterprise workloads | Cloud Platform | Reference only |
| Sandbox | Isolated experimentation with expiry and SKU guard | Cloud Governance | Policy baseline |

Subscription vending validates owner, classification, region, budget, network pattern, logging, and expiry before provisioning. Production recommendations include remote state, privileged approval, locks after deployment, cross-region recovery, and Policy remediation identities; the disposable lab intentionally avoids controls that could block teardown.
