# Asset inventory

Recovery values are scenario requirements. Monitoring references central diagnostic settings unless stated otherwise.

| ID | Asset | Business owner | Technical owner | Class | Criticality | Dependencies | RTO/RPO | Monitoring |
|---|---|---|---|---|---|---|---|---|
| AST-001 | Marketplace web app | Head of Commerce | Workload Team | INTERNAL | High | edge, API, identity | 2h/4h | HTTP, errors, WAF |
| AST-002 | Order API | Head of Commerce | Workload Team | CONFIDENTIAL | Critical | identity, database, Key Vault | 1h/15m | traces, auth, latency |
| AST-003 | Order database | Head of Commerce | Data Team | CONFIDENTIAL | Critical | network, key service | 1h/15m | audit, backup, capacity |
| AST-004 | Catalogue store | Product Director | Data Team | INTERNAL | High | storage, app | 4h/4h | access, availability |
| AST-005 | Supplier API gateway | Supplier Manager | Integration Team | CONFIDENTIAL | High | identity, partners | 4h/1h | auth failures, throttling |
| AST-006 | Customer support system | Support Director | SaaS Owner | CONFIDENTIAL | Medium | identity, export | 8h/4h | sign-in, audit changes |
| AST-007 | Entra tenant | CIO | IAM Team | RESTRICTED | Critical | Microsoft control plane | 30m/15m | sign-in, audit, risk |
| AST-008 | Privileged access groups | CISO | IAM Team | RESTRICTED | Critical | Entra, PIM | 30m/15m | membership, activation |
| AST-009 | Emergency-access identities | CIO | IAM Team | RESTRICTED | Critical | Entra | 15m/0 | sign-in and credential use |
| AST-010 | Workload managed identities | Platform Owner | Platform Team | RESTRICTED | High | Azure RBAC | 2h/4h | token/resource access |
| AST-011 | GitHub OIDC identity | Platform Owner | DevSecOps | RESTRICTED | Critical | GitHub, Entra | 4h/24h | federation and role changes |
| AST-012 | GitHub source repository | CTO | DevSecOps | INTERNAL | High | GitHub | 8h/24h | branch, workflow, secret scan |
| AST-013 | Terraform state | Platform Owner | DevSecOps | RESTRICTED | Critical | storage, Entra | 4h/15m | access, versioning, locks |
| AST-014 | Hub virtual network | CIO | Network Team | INTERNAL | Critical | Azure fabric, DNS | 2h/4h | flow/NSG changes |
| AST-015 | Workload spoke | Head of Commerce | Network Team | INTERNAL | Critical | hub, DNS | 2h/4h | flow/peering/route |
| AST-016 | Private DNS zones | CIO | Network Team | INTERNAL | High | hub, endpoints | 4h/24h | record changes |
| AST-017 | Key Vault | CISO | Platform Team | RESTRICTED | Critical | Entra, network | 1h/0 | access, delete, throttling |
| AST-018 | Secure storage account | DPO | Platform Team | CONFIDENTIAL | High | Entra, network | 4h/1h | access, public settings |
| AST-019 | Log Analytics workspace | CISO | SOC Team | CONFIDENTIAL | Critical | diagnostic sources | 1h/15m | ingestion, retention, gaps |
| AST-020 | Microsoft Sentinel | CISO | SOC Team | CONFIDENTIAL | Critical | workspace, identity | 1h/15m | rules, incidents, automation |
| AST-021 | Defender posture data | CISO | Cloud Security | INTERNAL | High | subscriptions, policies | 8h/24h | recommendation freshness |
| AST-022 | Policy initiative | CIO | Cloud Governance | INTERNAL | High | Azure Policy | 4h/24h | assignment/compliance changes |
| AST-023 | Evidence repository | CISO | GRC Team | CONFIDENTIAL | High | collectors, sanitizer | 8h/24h | integrity, completeness |
| AST-024 | Backup vault/catalog | CIO | Operations | RESTRICTED | Critical | workloads, keys | 2h/0 | job success, restore test |
| AST-025 | Synthetic telemetry dataset | SOC Lead | Detection Engineering | PUBLIC | Medium | generator seed | 24h/24h | hash/reproducibility |
| AST-026 | Recruiter dashboard | Project Owner | DevSecOps | PUBLIC | Low | GitHub Pages | 24h/24h | build, links, privacy scan |
