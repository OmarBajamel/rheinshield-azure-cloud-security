# Control evidence matrix

Mappings are concise, educational cross-references; they do not confer certification or legal compliance. BSI requirement IDs were verified against the official Edition 2023 compendium; a dash in MCSB means no direct control was asserted.

| ID | Control | Status | NIS2/BSIG | ISO 27001:2022 | BSI IT-Grundschutz Edition 2023 | MCSB v1 | Evidence |
|---|---|---|---|---|---|---|---|
| CTL-001 | Asset inventory and ownership | FIXTURE_VALIDATED | BSIG §30(2)1 | ISO A.5.9 | BSI ORP.1.A2 | MCSB AM-1 | docs/scenario/ASSET_INVENTORY.md |
| CTL-002 | Risk method and treatment | FIXTURE_VALIDATED | BSIG §30(1) | ISO 6.1 / A.5.4 | BSI ISMS.1.A7/A10 | MCSB GS-1 | docs/compliance/RISK_REGISTER.md |
| CTL-003 | Identity and least privilege | READY_NOT_AUTHENTICATED | BSIG §30(2)9 | ISO A.5.15/A.5.18 | BSI ORP.4.A2/A4 | MCSB PA-1 | docs/identity/RBAC_MATRIX.md |
| CTL-004 | Strong authentication | READY_LICENSE_REQUIRED | BSIG §30(2)10 | ISO A.8.5 | BSI ORP.4.A21 | MCSB IM-6 | identity/conditional-access/policies.json |
| CTL-005 | Workload identity/OIDC | READY_NOT_AUTHENTICATED | BSIG §30(2)5/9 | ISO A.5.16/A.8.2 | BSI ORP.4.A13/A15 | MCSB IM-3 | docs/identity/OIDC_FEDERATION.md |
| CTL-006 | Network segmentation | PLAN_VALIDATED | BSIG §30(2)1 | ISO A.8.20/A.8.22 | BSI NET.1.1.A4/A22 | MCSB NS-1 | infra/modules/network/main.tf |
| CTL-007 | Secrets and cryptography | PLAN_VALIDATED | BSIG §30(2)8 | ISO A.8.24 | BSI CON.1.A1/A4 | MCSB DP-5 | infra/modules/security/main.tf |
| CTL-008 | Secure configuration policy | FIXTURE_VALIDATED | BSIG §30(2)1/4 | ISO A.8.9 | BSI OPS.1.1.2.A7/A11 | MCSB PV-2 | infra/policies/controls.json |
| CTL-009 | Central logging | PLAN_VALIDATED | BSIG §30(2)1/2 | ISO A.8.15 | BSI OPS.1.1.5.A3/A6 | MCSB LT-3 | infra/modules/monitoring/main.tf |
| CTL-010 | Detection engineering | FIXTURE_VALIDATED | BSIG §30(2)2 | ISO A.8.16 | BSI DER.1.A6/A11 | MCSB LT-1 | artifacts/evidence/detection-test-results.json |
| CTL-011 | Incident response | FIXTURE_VALIDATED | BSIG §30(2)2 | ISO A.5.24-A.5.28 | BSI DER.2.1.A2/A7 | MCSB IR-1 | docs/incident-response/INCIDENT_RESPONSE_PLAN.md |
| CTL-012 | Business continuity and backup | FIXTURE_VALIDATED | BSIG §30(2)3 | ISO A.5.29/A.8.13 | BSI CON.3.A4/A15; DER.4.A10 | MCSB BR-1 | docs/operations/BACKUP_AND_RECOVERY.md |
| CTL-013 | Supplier security | FIXTURE_VALIDATED | BSIG §30(2)4 | ISO A.5.19-A.5.22 | BSI OPS.2.3.A2/A4 | MCSB GS-7 | docs/security/SUPPLIER_ACCESS_POLICY.md |
| CTL-014 | Secure development/CI | FIXTURE_VALIDATED | BSIG §30(2)5 | ISO A.8.25-A.8.31 | BSI CON.8.A5/A7/A10/A20 | MCSB DS-1 | .github/workflows/ci.yml |
| CTL-015 | Vulnerability management | FIXTURE_VALIDATED | BSIG §30(2)5 | ISO A.8.8 | BSI OPS.1.1.3.A1/A15 | MCSB PV-6 | docs/security/VULNERABILITY_MANAGEMENT_POLICY.md |
| CTL-016 | Cyber hygiene and training | UNAVAILABLE | BSIG §30(2)7 | ISO A.6.3 | BSI ORP.3.A4/A6 | — (no direct MCSB control) | docs/security/INFORMATION_SECURITY_POLICY.md |
| CTL-017 | Evidence sanitization | FIXTURE_VALIDATED | BSIG §30 governance | ISO A.5.33/A.8.11 | BSI CON.6.A1/A8 | MCSB DP-3 | docs/evidence/SANITIZATION_STANDARD.md |
| CTL-018 | Cost and lifecycle guard | FIXTURE_VALIDATED | BSIG proportionality | ISO A.5.31 | BSI ISMS.1.A15 | — (no direct MCSB control) | docs/cost/COST_GUARD.md |
| CTL-019 | Incident reporting decision | FIXTURE_VALIDATED | BSIG §§32-35 | ISO A.5.5/A.5.26 | BSI DER.2.1.A3/A9/A14 | MCSB IR-2 | docs/incident-response/COMMUNICATION_MATRIX.md |
| CTL-020 | Control evidence integrity | FIXTURE_VALIDATED | BSIG §30 governance | ISO A.5.35/A.5.36 | BSI ISMS.1.A13; OPS.1.1.2.A5 | — (no direct MCSB control) | artifacts/evidence/evidence-manifest.json |
