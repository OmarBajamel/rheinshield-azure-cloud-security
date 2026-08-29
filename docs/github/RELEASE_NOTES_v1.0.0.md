# RheinShield v1.0.0

First portfolio release of RheinShield, a bilingual NIS2-aligned Azure landing-zone and security-operations case study using synthetic data.

## Highlights

- Azure Landing Zone enterprise reference with AVM 0.21.0 and a separately scoped five-module lab.
- Terraform 1.16.0, AzureRM 5.3.0, AzAPI 2.12.0, TFLint 0.64.0, native mock test, and 14-control IaC security gate.
- Zero Trust/RBAC/Conditional Access/PIM/access-review/JML/OIDC designs with explicit license and live-status boundaries.
- Fourteen KQL analytics rules, five hunting queries, three workbooks, three automation rules, and three disabled dry-run playbooks.
- Deterministic 738-event telemetry and full INC-001 investigation.
- Twenty-seven risks and twenty evidence controls mapped across NIS2/BSIG, ISO 27001:2022, BSI IT-Grundschutz, and stable MCSB v1.
- Eight-route English/German React dashboard with desktop/mobile screenshots, browser checks, and automated privacy controls.

## Validation boundary

The composed lab is `PLAN_VALIDATED` by a mocked Terraform plan. Enterprise and standalone policy roots passed static/provider validation but remain `READY_NOT_AUTHENTICATED` because no authenticated plan ran. Detections, incident data, and public evidence are `FIXTURE_VALIDATED`; Azure live, Defender, Conditional Access, and PIM remain `READY_NOT_AUTHENTICATED` or `READY_LICENSE_REQUIRED`. No Azure resource or credential was created in this run.

Release assets include a sanitized source/evidence archive, checksums, SBOM, CV one-pager, and LinkedIn media package. Nothing was posted to LinkedIn.
