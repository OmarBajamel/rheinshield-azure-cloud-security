#!/usr/bin/env python3
"""Generate the auditable RheinShield risk and control-evidence registers."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

RISK_ROWS = [
    ("RSK-001","Entra tenant","Identity","Password spray compromises a contractor","Supplier MFA/device boundary is insufficient","CA templates; RS001/RS002",4,5,"Mitigate","Phishing-resistant MFA and contractor review",8,"IAM Lead","2026-09-30","sentinel/analytics-rules/rs001-password-spray.yaml"),
    ("RSK-002","Privileged groups","Identity","Excessive privilege enables control changes","Standing membership or weak activation governance","RBAC matrix; audit fixtures",4,5,"Mitigate","PIM approval, 4h activation, SoD",6,"CISO","2026-10-31","identity/pim/pim-design.json"),
    ("RSK-003","Emergency access","Identity","Break-glass credential misuse","Infrequent testing and broad exclusion","Monitored design; dual control",2,5,"Mitigate","Quarterly sign-in/test review",5,"IAM Lead","2026-11-30","docs/identity/PRIVILEGED_ACCESS_RUNBOOK.md"),
    ("RSK-004","Guest/supplier identities","Supplier integration","Orphaned access persists","Sponsor or expiry is missing","JML workflow; access review design",4,4,"Mitigate","Automated expiry and quarterly review",6,"Supplier Manager","2026-10-15","identity/access-reviews/access-review-design.json"),
    ("RSK-005","GitHub OIDC identity","CI/CD","Repository/workflow compromise obtains Azure role","Trust subject or environment scope is too broad","OIDC design; protected environment",3,5,"Mitigate","Immutable subject, branch protection, short scope",5,"DevSecOps Lead","2026-09-30","docs/identity/OIDC_FEDERATION.md"),
    ("RSK-006","Terraform state","Cloud delivery","State reveals configuration or enables takeover","Weak backend access/versioning","Private ignored local state; backend design",3,5,"Mitigate","Project state vault, RBAC, versioning, lock",5,"Platform Owner","2026-10-31","infra/bootstrap/README.md"),
    ("RSK-007","Hub/spoke networks","Order processing","Unrestricted inbound exposes administrative services","NSG rule is broadened","RSP-010/RSP-011; RS007",3,5,"Mitigate","Deny policy after lab impact test",5,"Network Lead","2026-09-30","infra/policies/controls.json"),
    ("RSK-008","Key Vault","Order processing","Secret enumeration supports further compromise","Excess identity access or network-path misconfiguration","RBAC, purge protection, private endpoint, RS010",3,5,"Mitigate","Live DNS/path validation and access review",6,"Platform Owner","2026-10-31","infra/modules/security/main.tf"),
    ("RSK-009","Evidence storage","Audit readiness","Public/shared-key storage exposes evidence","Network or authorization control drifts","Public/shared-key disabled; private endpoint; RSP-006/RSP-007/RSP-014",3,5,"Mitigate","Live path test and policy compliance evidence",5,"GRC Lead","2026-09-30","infra/policies/controls.json"),
    ("RSK-010","Log Analytics","Security operations","Ingestion stops without timely detection","Diagnostic setting deletion or quota exhaustion","RS008; freshness dashboard",4,5,"Mitigate","Protected settings, ingestion alerts, secondary evidence",7,"SOC Lead","2026-09-30","sentinel/analytics-rules/rs008-monitoring-control-deleted.yaml"),
    ("RSK-011","Sentinel analytics","Security operations","Detection gaps miss relevant attack paths","Schema drift, disabled rule, missing connector","14-rule pack; fixture harness",4,4,"Mitigate","Canary KQL and connector freshness review",6,"Detection Lead","2026-10-15","artifacts/evidence/detection-test-results.json"),
    ("RSK-012","SOAR playbooks","Incident response","Automation causes unsafe containment","Broad permissions or unreviewed side effects","Disabled connector-free dry-run playbooks",3,5,"Avoid","Keep dry-run; approve dedicated lab activation",3,"SOC Lead","2026-09-30","docs/sentinel/SOAR_SAFETY.md"),
    ("RSK-013","Order API","Order processing","Input abuse affects availability/integrity","Missing validation or rate limit","Pydantic validation; headers; rate limiter",3,4,"Mitigate","Gateway throttling and telemetry in live lab",5,"Workload Owner","2026-10-31","apps/secure-workload/tests/test_api.py"),
    ("RSK-014","Container image","Cloud delivery","Vulnerable dependency is deployed","Unscanned or mutable base/dependency","Pinned app deps; CI scan design",3,5,"Mitigate","Trivy/SBOM/signature gate",5,"DevSecOps Lead","2026-09-30","docs/testing/TEST_STRATEGY.md"),
    ("RSK-015","Application logs","Security operations","Sensitive data appears in telemetry","Over-logging inputs/identities","Synthetic-only logger; sanitizer",3,4,"Mitigate","Structured allow-list logging and privacy tests",4,"DPO","2026-09-30","docs/evidence/SANITIZATION_STANDARD.md"),
    ("RSK-016","Backup catalogue","Business continuity","Backup cannot be restored","Restore tests absent or credentials unavailable","BIA; recovery runbook",3,5,"Mitigate","Quarterly isolated restore test",7,"Operations Lead","2026-11-30","docs/operations/BACKUP_AND_RECOVERY.md"),
    ("RSK-017","Order database","Order processing","Ransomware/corruption causes prolonged outage","Recovery isolation or RPO is insufficient","IaC, backup design, incident plan",3,5,"Mitigate","Immutable backup and recovery exercise",6,"Data Owner","2026-11-30","docs/scenario/BUSINESS_IMPACT_ANALYSIS.md"),
    ("RSK-018","Supplier API","Supplier integration","Compromised supplier sends unauthorized changes","Partner authentication and transaction validation weak","Identity boundary; logging",4,4,"Mitigate","mTLS/API claims, anomaly detection, contract controls",7,"Supplier Manager","2026-12-15","docs/security/SUPPLIER_ACCESS_POLICY.md"),
    ("RSK-019","Policy initiative","Cloud governance","Misconfiguration is deployed outside guardrails","Policy assignment missing or Audit-only","14-control baseline",3,4,"Mitigate","Staged Deny after exceptions/remediation",5,"Cloud Governance","2026-10-31","docs/security/POLICY_BASELINE.md"),
    ("RSK-020","Azure subscription","Cost operations","Compromise or error creates uncontrolled spend","No quota/lifetime enforcement","EUR20 guard; expiry tags; max replicas",3,4,"Mitigate","Budget alert and automated expiry cleanup",4,"FinOps Owner","2026-09-30","docs/cost/COST_GUARD.md"),
    ("RSK-021","Marketplace edge","Marketplace","Regional or platform failure stops service","Single-region lab differs from production reference","BIA; paired-region design",3,5,"Mitigate","Production zone/region architecture and exercise",7,"CIO","2026-12-31","docs/architecture/ARCHITECTURE.md"),
    ("RSK-022","Incident process","Incident response","Slow ownership delays containment","Unclear severity/decision rights","IR plan; communication matrix",3,5,"Mitigate","Tabletop and on-call evidence",5,"CISO","2026-10-31","docs/incident-response/INCIDENT_RESPONSE_PLAN.md"),
    ("RSK-023","Regulatory reporting","Governance","Material incident is reported late or inaccurately","Applicability/severity decision is unclear","German source register; communication matrix",3,5,"Mitigate","Counsel-reviewed decision tree and exercise",6,"Legal/Compliance","2026-10-31","docs/compliance/NIS2_APPLICABILITY_ASSESSMENT_DE.md"),
    ("RSK-024","Public repository","Portfolio publication","Secret or tenant identifier is published","Raw evidence enters Git history or screenshot","Ignore rules; sanitizer; release scan",3,5,"Avoid","Pre-push PII/history/bundle/screenshot gate",3,"Project Owner","2026-08-29","docs/evidence/SANITIZATION_STANDARD.md"),
    ("RSK-025","Control evidence","Audit readiness","Evidence is stale, incomplete or not traceable","Manual collection and unclear provenance","Manifest, hashes, capability matrix",4,4,"Mitigate","Automated collector and quarterly control review",6,"GRC Lead","2026-10-31","artifacts/evidence/evidence-manifest.json"),
    ("RSK-026","Customer support","Customer support","Support agent over-accesses account context","Role bundles or exports are excessive","RBAC/JML/data classification",3,4,"Mitigate","Field-level access and sampling review",5,"Support Director","2026-11-30","docs/scenario/DATA_CLASSIFICATION.md"),
    ("RSK-027","Workload identity","Order processing","Managed identity receives broad control-plane access","Role assigned above project vault/resource group","Narrow role matrix; Terraform scope",3,5,"Mitigate","Permission diff and access review",4,"Platform Owner","2026-10-15","infra/modules/security/main.tf"),
]

CONTROLS = [
    ("CTL-001","Asset inventory and ownership","FIXTURE_VALIDATED","BSIG §30(2)1","ISO A.5.9","BSI ORP.1.A2","MCSB AM-1","docs/scenario/ASSET_INVENTORY.md"),
    ("CTL-002","Risk method and treatment","FIXTURE_VALIDATED","BSIG §30(1)","ISO 6.1 / A.5.4","BSI ISMS.1.A7/A10","— (no direct MCSB control)","docs/compliance/RISK_REGISTER.md"),
    ("CTL-003","Identity and least privilege","READY_NOT_AUTHENTICATED","BSIG §30(2)9","ISO A.5.15/A.5.18","BSI ORP.4.A2/A4","MCSB PA-1","docs/identity/RBAC_MATRIX.md"),
    ("CTL-004","Strong authentication","READY_LICENSE_REQUIRED","BSIG §30(2)10","ISO A.8.5","BSI ORP.4.A21","MCSB IM-6","identity/conditional-access/policies.json"),
    ("CTL-005","Workload identity/OIDC","READY_NOT_AUTHENTICATED","BSIG §30(2)5/9","ISO A.5.16/A.8.2","BSI ORP.4.A13/A15","MCSB IM-3","docs/identity/OIDC_FEDERATION.md"),
    ("CTL-006","Network segmentation","PLAN_VALIDATED","BSIG §30(2)1","ISO A.8.20/A.8.22","BSI NET.1.1.A4/A22","MCSB NS-1","infra/modules/network/main.tf"),
    ("CTL-007","Secrets and cryptography","PLAN_VALIDATED","BSIG §30(2)8","ISO A.8.24","BSI CON.1.A1/A4","MCSB DP-5","infra/modules/security/main.tf"),
    ("CTL-008","Secure configuration policy","FIXTURE_VALIDATED","BSIG §30(2)1/4","ISO A.8.9","BSI OPS.1.1.2.A7/A11","MCSB PV-2","infra/policies/controls.json"),
    ("CTL-009","Central logging","PLAN_VALIDATED","BSIG §30(2)1/2","ISO A.8.15","BSI OPS.1.1.5.A3/A6","MCSB LT-3","infra/modules/monitoring/main.tf"),
    ("CTL-010","Detection engineering","FIXTURE_VALIDATED","BSIG §30(2)2","ISO A.8.16","BSI DER.1.A6/A11","MCSB LT-1","artifacts/evidence/detection-test-results.json"),
    ("CTL-011","Incident response","FIXTURE_VALIDATED","BSIG §30(2)2","ISO A.5.24-A.5.28","BSI DER.2.1.A2/A7","MCSB IR-1","docs/incident-response/INCIDENT_RESPONSE_PLAN.md"),
    ("CTL-012","Business continuity and backup","PLAN_VALIDATED","BSIG §30(2)3","ISO A.5.29/A.8.13","BSI CON.3.A4/A15; DER.4.A10","MCSB BR-1","docs/operations/BACKUP_AND_RECOVERY.md"),
    ("CTL-013","Supplier security","PLAN_VALIDATED","BSIG §30(2)4","ISO A.5.19-A.5.22","BSI OPS.2.3.A2/A4","— (no direct MCSB control)","docs/security/SUPPLIER_ACCESS_POLICY.md"),
    ("CTL-014","Secure development/CI","PLAN_VALIDATED","BSIG §30(2)5","ISO A.8.25-A.8.31","BSI CON.8.A5/A7/A10/A20","MCSB DS-2/DS-3/DS-4",".github/workflows/ci.yml"),
    ("CTL-015","Vulnerability management","FIXTURE_VALIDATED","BSIG §30(2)5","ISO A.8.8","BSI OPS.1.1.3.A1/A15","MCSB PV-6","docs/security/VULNERABILITY_MANAGEMENT_POLICY.md"),
    ("CTL-016","Cyber hygiene and training","UNAVAILABLE","BSIG §30(2)7","ISO A.6.3","BSI ORP.3.A4/A6","— (no direct MCSB control)","docs/security/INFORMATION_SECURITY_POLICY.md"),
    ("CTL-017","Evidence sanitization","FIXTURE_VALIDATED","BSIG §30 governance","ISO A.5.33/A.8.11","BSI CON.6.A1/A8","— (no direct MCSB control)","docs/evidence/SANITIZATION_STANDARD.md"),
    ("CTL-018","Cost and lifecycle guard","FIXTURE_VALIDATED","BSIG proportionality","ISO A.5.31","BSI ISMS.1.A15","— (no direct MCSB control)","docs/cost/COST_GUARD.md"),
    ("CTL-019","Incident reporting decision","PLAN_VALIDATED","BSIG §§32-35","ISO A.5.5/A.5.26","BSI DER.2.1.A3/A9/A14","MCSB IR-2","docs/incident-response/COMMUNICATION_MATRIX.md"),
    ("CTL-020","Control evidence integrity","FIXTURE_VALIDATED","BSIG §30 governance","ISO A.5.35/A.5.36","BSI ISMS.1.A13; OPS.1.1.2.A5","— (no direct MCSB control)","artifacts/evidence/evidence-manifest.json"),
]

def risk_level(score: int) -> str:
    return "Critical" if score >= 20 else "High" if score >= 12 else "Medium" if score >= 6 else "Low"

def main() -> int:
    evidence_dir = ROOT / "artifacts" / "evidence"
    docs_dir = ROOT / "docs" / "compliance"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)
    risks = []
    for row in RISK_ROWS:
        rid, asset, process, threat, vuln, existing, likelihood, impact, treatment, planned, residual, owner, due, evidence = row
        score = likelihood * impact
        risks.append({"id":rid,"asset":asset,"businessProcess":process,"threat":threat,"vulnerability":vuln,"existingControls":existing,"likelihood":likelihood,"impact":impact,"inherentScore":score,"inherentLevel":risk_level(score),"treatment":treatment,"plannedControls":planned,"residualScore":residual,"residualLevel":risk_level(residual),"owner":owner,"dueDate":due,"evidence":evidence,"reviewStatus":"OPEN"})
    (evidence_dir / "risk-register.json").write_text(json.dumps({"schemaVersion":"1.0.0","dataMode":"public-demo","risks":risks}, indent=2) + "\n", encoding="utf-8")
    with (evidence_dir / "risk-register.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=risks[0].keys())
        writer.writeheader()
        writer.writerows(risks)
    header = "# Risk register\n\nSynthetic scenario register; it is not a statement of real-company risk or compliance. Scoring is defined in `RISK_METHODOLOGY.md`.\n\n| ID | Asset / process | Threat and vulnerability | Inherent | Treatment / planned control | Residual | Owner / due | Evidence |\n|---|---|---|---:|---|---:|---|---|\n"
    lines = [f"| {r['id']} | {r['asset']} / {r['businessProcess']} | {r['threat']}; {r['vulnerability']} | {r['inherentScore']} {r['inherentLevel']} | {r['treatment']}: {r['plannedControls']} | {r['residualScore']} {r['residualLevel']} | {r['owner']} / {r['dueDate']} | `{r['evidence']}` |" for r in risks]
    (docs_dir / "RISK_REGISTER.md").write_text(header + "\n".join(lines) + "\n", encoding="utf-8")
    controls = [{"id":c[0],"control":c[1],"status":c[2],"nis2Bsig":c[3],"iso27001":c[4],"bsiGrundschutz":c[5],"mcsb":c[6],"evidence":c[7]} for c in CONTROLS]
    (evidence_dir / "control-evidence-matrix.json").write_text(json.dumps({"schemaVersion":"1.0.0","controls":controls}, indent=2) + "\n", encoding="utf-8")
    cheader = "# Control evidence matrix\n\nMappings are concise, educational cross-references; they do not confer certification or legal compliance. BSI requirement IDs were verified against the official Edition 2023 compendium; a dash in MCSB means no direct control was asserted.\n\n| ID | Control | Status | NIS2/BSIG | ISO 27001:2022 | BSI IT-Grundschutz Edition 2023 | MCSB v1 | Evidence |\n|---|---|---|---|---|---|---|---|\n"
    clines = ["| " + " | ".join(c) + " |" for c in CONTROLS]
    (docs_dir / "CONTROL_EVIDENCE_MATRIX.md").write_text(cheader + "\n".join(clines) + "\n", encoding="utf-8")
    print(json.dumps({"risks":len(risks),"controls":len(controls),"status":"FIXTURE_VALIDATED"}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
