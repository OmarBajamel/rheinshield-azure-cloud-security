# RheinShield Security Baseline v1.0.0

The initiative contains 14 controls. The safe lab assignment is non-enforcing `Audit`; production reference guidance may adopt `Deny` after impact analysis, exemptions, remediation testing, and owner approval.

| ID | Control | Lab effect | Production target | Evidence |
|---|---|---|---|---|
| RSP-001 | Allowed Germany West Central/West Europe | Audit | Deny | `infra/policies/controls.json` |
| RSP-002 | Required Project tag | Audit | Deny | policy test and compliance summary |
| RSP-003 | Owner/environment/classification/expiry tags | Audit | Deny | asset/lifecycle evidence |
| RSP-004 | Storage minimum TLS 1.2 | Audit | Deny | Terraform plan |
| RSP-005 | Storage HTTPS-only | Audit | Deny | Terraform plan |
| RSP-006 | Public blob access disabled | Audit | Deny | Terraform plan |
| RSP-007 | Storage public network assessed | Audit | Deny with approved exceptions | exception register |
| RSP-008 | Key Vault Azure RBAC | Audit | Deny | Terraform plan |
| RSP-009 | Key Vault purge protection | Audit | Deny | Terraform plan |
| RSP-010 | Public IP restrictions | Audit | Deny outside approved edge | architecture review |
| RSP-011 | No Internet SSH/RDP NSG rule | Audit | Deny | malicious policy fixture |
| RSP-012 | Managed identity on supported compute | Audit | Deny | workload identity evidence |
| RSP-013 | Diagnostic settings | AuditIfNotExists | DeployIfNotExists | monitoring coverage |
| RSP-014 | Storage shared-key access disabled | Audit | Deny | Terraform plan |

Each control includes purpose, scope, parameters, evidence, and framework tags in the source catalogue. Custom controls are used for an inspectable portfolio baseline; an enterprise rollout should prefer equivalent Microsoft built-ins where semantics and versioning match.
