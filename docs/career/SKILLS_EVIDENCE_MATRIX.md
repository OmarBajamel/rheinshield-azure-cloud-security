# Skills-to-evidence matrix

Baseline: **2026-08-29**. Vacancy signal comes from the 15-role German sample in [`GERMANY_JOB_ALIGNMENT.md`](GERMANY_JOB_ALIGNMENT.md). Statuses use only the repository's controlled vocabulary; none implies a live Azure deployment.

| Skill / employer signal | Inspectable evidence | Acceptance evidence | Status |
|---|---|---|---|
| Azure architecture / Landing Zones | `docs/architecture/`, `infra/enterprise-reference/`, `infra/lab/` | Terraform format/init/validate; independent architecture review | `READY_NOT_AUTHENTICATED` |
| Terraform / Azure Verified Modules | `infra/modules/`, `infra/lab/`, `infra/enterprise-reference/` | Lab mock plan test 1/1; all roots initialize/validate | `PLAN_VALIDATED` |
| Bicep | `sentinel/automation-rules/`, `sentinel/playbooks/` | 7/7 templates compiled with Bicep 0.46.1 | `FIXTURE_VALIDATED` |
| GitHub Actions / CI/CD | `.github/workflows/`, `scripts/` | Least-privilege permissions, full-SHA action pins, local gate results | `FIXTURE_VALIDATED` |
| Secretless Azure OIDC | `.github/workflows/azure-lab.yml`, `scripts/bootstrap-azure.*`, `docs/identity/OIDC_FEDERATION.md` | Exact repo/environment subject and exact pre-created RG scopes; no client secret | `READY_NOT_AUTHENTICATED` |
| Entra ID / IAM / least privilege | `identity/`, `docs/identity/` | RBAC, JML, PIM and access-review designs are machine-readable and reviewed | `READY_NOT_AUTHENTICATED` |
| Conditional Access / MFA | `identity/conditional-access/`, `docs/identity/CONDITIONAL_ACCESS_DESIGN.md` | Six report-only design records; exclusions and licensing documented | `READY_LICENSE_REQUIRED` |
| PIM and access reviews | `identity/pim/`, `identity/access-reviews/` | Approval, time limit, review cadence and license boundary recorded | `READY_LICENSE_REQUIRED` |
| Managed identity / Key Vault | `infra/modules/security/`, `infra/modules/workload/` | Mock lab plan; user-assigned identity and vault-scoped data role | `PLAN_VALIDATED` |
| Azure Policy / governance | `infra/policies/`, `docs/security/POLICY_BASELINE.md` | 14 definitions render/validate; authenticated assignment still required | `READY_NOT_AUTHENTICATED` |
| Defender for Cloud / XDR | `docs/evidence/CAPABILITY_MATRIX.md`, dashboard | Paid-plan boundary and unsupported live claims are explicit | `READY_LICENSE_REQUIRED` |
| Microsoft Sentinel / KQL | `sentinel/analytics-rules/`, `docs/sentinel/DETECTION_CATALOG.md` | 14 malicious fixtures trigger; 14 benign fixtures stay quiet | `FIXTURE_VALIDATED` |
| Hunting / MITRE ATT&CK | `sentinel/hunting-queries/`, `docs/sentinel/MITRE_COVERAGE.md` | Syntax/metadata reviewed; live table execution remains unavailable | `READY_NOT_AUTHENTICATED` |
| SOAR / playbooks | `sentinel/automation-rules/`, `sentinel/playbooks/`, `docs/sentinel/SOAR_SAFETY.md` | 3+3 templates compiled; disabled, connector-free, dry-run defaults | `FIXTURE_VALIDATED` |
| Log onboarding / telemetry | `docs/sentinel/SYNTHETIC_TELEMETRY.md`, `tools/synthetic-telemetry/`, `data/public-demo/telemetry.jsonl` | 738 deterministic events, 90 days, fixed seed and manifest hash | `FIXTURE_VALIDATED` |
| Incident response / investigation | `docs/incident-response/`, `data/public-demo/inc-001-timeline.json` | End-to-end chronology, evidence, containment and lessons learned | `FIXTURE_VALIDATED` |
| Logging and monitoring | `infra/modules/monitoring/`, diagnostic settings in Terraform | Mock lab plan and code review; no live ingestion | `PLAN_VALIDATED` |
| Secure workload / containers | `apps/secure-workload/`, `infra/modules/workload/` | Python API tests; internal Container Apps design; digest-only image input | `PLAN_VALIDATED` |
| Python / PowerShell / Bash automation | `tools/`, `scripts/`, `tests/` | Pytest, Ruff and selected strict MyPy results | `FIXTURE_VALIDATED` |
| Secure SDLC / vulnerability handling | `.github/workflows/ci.yml`, `docs/security/` | Static checks, dependency audit and release scans | `FIXTURE_VALIDATED` |
| NIS2 / BSIG / risk analysis | `docs/compliance/`, `docs/research/GERMAN_SOURCE_NOTES.md` | Current official sources, conditional applicability, 27 scored risks | `FIXTURE_VALIDATED` |
| ISO 27001 / BSI / MCSB mapping | `docs/compliance/CONTROL_EVIDENCE_MATRIX.md` | 20 evidence links; BSI Edition-2023 requirement IDs; no certification claim | `FIXTURE_VALIDATED` |
| BIA / resilience | `docs/scenario/BUSINESS_IMPACT_ANALYSIS.md`, `docs/operations/` | RTO/RPO assumptions and deterministic tabletop evidence | `FIXTURE_VALIDATED` |
| Cost governance / teardown | `docs/cost/`, `scripts/destroy-lab.*`, `artifacts/evidence/resource-lifecycle.json` | EUR 20 full-run gate; exact suffix-bound deletion; zero live spend observed | `FIXTURE_VALIDATED` |
| German and English communication | `README.md`, `README.de.md`, bilingual dashboard, career/social packages | Route/localization tests and independent recruiter review | `FIXTURE_VALIDATED` |

## Evidence quality boundary

`PLAN_VALIDATED` is used only where the mocked Terraform lab plan exercised the composed modules. Enterprise and standalone policy roots that received static/provider validation but no authenticated plan remain `READY_NOT_AUTHENTICATED`. `FIXTURE_VALIDATED` means deterministic offline evidence, not production efficacy. Independent review findings and resolutions are recorded in `docs/execution/REVIEW_FINDINGS.md`.
