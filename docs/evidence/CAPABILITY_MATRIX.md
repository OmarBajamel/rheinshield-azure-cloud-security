# Capability matrix

Verified 2026-08-29. `UNCOMMITTED` is replaced by the release commit in the final packaging pass.

| Capability | Architecture | Validation | Evidence | Cost | License | Limitation |
|---|---|---|---|---|---|---|
| Enterprise landing zone | Multi-subscription ALZ via AVM | `READY_NOT_AUTHENTICATED` | `infra/enterprise-reference/` | No apply | Enterprise permissions | Static/provider validation only; no authenticated plan |
| Single-subscription lab | Three pre-created project RGs plus composed modules | `PLAN_VALIDATED` | `infra/lab/` | Gate required | Azure subscription | Mock plan passed; no authenticated plan/apply |
| Network segmentation | Hub/spoke reference; compact lab VNet | `PLAN_VALIDATED` | `infra/modules/network/` | Low lab design | Standard Azure | Live routing unverified |
| Central monitoring | Log Analytics / diagnostics | `PLAN_VALIDATED` | `infra/modules/monitoring/` | Cost-gated ingestion | Azure | No live workspace |
| Secure workload | Managed identity, Key Vault, structured API logs | `PLAN_VALIDATED` | `apps/secure-workload/` | Local plus mock plan | Azure for identity | API fixtures and mock IaC plan; Azure identity not live |
| Policy baseline | 14 versioned controls | `FIXTURE_VALIDATED` | `infra/policies/controls.json` | None offline | Azure for assignment | No compliance scan |
| Entra role model | Eight personas and separation of duties | `READY_NOT_AUTHENTICATED` | `identity/rbac/` | None | Entra | Design reviewed; no tenant assignments |
| Conditional Access | Six report-only design records | `READY_LICENSE_REQUIRED` | `identity/conditional-access/` | None | P1/P2 features vary | Design schema only; not deployed |
| PIM | Eligible, time-bound privileged access | `READY_LICENSE_REQUIRED` | `identity/pim/` | License-dependent | Entra ID P2 | Design only |
| Access reviews | Quarterly supplier/privileged certification | `READY_LICENSE_REQUIRED` | `identity/access-reviews/` | License-dependent | Entra ID Governance | Fixture evidence only |
| GitHub OIDC | Federated, exact-RG-scoped deployment identity | `READY_NOT_AUTHENTICATED` | `docs/identity/OIDC_FEDERATION.md` | None | Azure/GitHub | Bootstrap implemented; credential not created |
| Defender for Cloud | Foundational CSPM first | `READY_NOT_AUTHENTICATED` | `defender-status.json` | Paid plans skipped | Subscription/plan | No secure-score claim |
| Sentinel analytics | 14 KQL analytics rules | `FIXTURE_VALIDATED` | `detection-test-results.json` | None offline | Sentinel live requires Azure | Fixture efficacy only |
| Threat hunting | Five hunting queries | `READY_NOT_AUTHENTICATED` | `sentinel/hunting-queries/` | None offline | Sentinel live requires Azure | Structure reviewed; queries not fixture/live executed |
| Workbooks | Three validated templates | `FIXTURE_VALIDATED` | `sentinel/workbooks/` | None offline | Sentinel live requires Azure | Not rendered in portal |
| SOAR | Three automation rules and three disabled playbooks | `FIXTURE_VALIDATED` | `sentinel/playbooks/` | None offline | Logic Apps live | All actions dry-run |
| Synthetic telemetry | 738 deterministic events | `FIXTURE_VALIDATED` | `telemetry-manifest.json` | None | None | Not production telemetry |
| Incident exercise | INC-001 identity chain | `FIXTURE_VALIDATED` | `docs/incident-response/` | None | None | Tabletop simulation |
| Risk and compliance | 27 risks, 20 controls, four framework views | `FIXTURE_VALIDATED` | `docs/compliance/` | None | No certification | Legal conclusion conditional |
| Recruiter dashboard | Eight bilingual, responsive routes | `FIXTURE_VALIDATED` | `src/main.tsx` | Static hosting | None | Public synthetic data only |

The machine-readable equivalent is `artifacts/evidence/capability-matrix.json`.
