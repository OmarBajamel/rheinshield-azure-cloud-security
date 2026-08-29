# Business impact analysis

| Process | Maximum tolerable outage | RTO | RPO | Impact | Recovery dependency |
|---|---:|---:|---:|---|---|
| Workforce/customer authentication | 2 h | 30 min | 15 min | critical | Entra ID, emergency access, application cache |
| Order processing | 4 h | 1 h | 15 min | critical | workload, database, messaging, Key Vault |
| Marketplace browsing | 8 h | 2 h | 4 h | high | edge, app, catalogue store |
| Supplier integration | 8 h | 4 h | 1 h | high | API gateway, partner credentials, queue |
| Customer support | 24 h | 8 h | 4 h | medium | ticketing, identity, exports |
| Security monitoring | 2 h | 1 h | 15 min | critical | Log Analytics/Sentinel, collectors, evidence store |
| CI/CD | 24 h | 8 h | 24 h | medium | GitHub, OIDC, state backend |

Exercise recovery uses immutable IaC, configuration exports, documented break-glass access, region-pair design, and restore tests. These are scenario targets, not measured production service levels.
