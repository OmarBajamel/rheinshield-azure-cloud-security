"""Project-specific IaC security gate for RheinShield's non-negotiable controls."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
files = {str(path.relative_to(ROOT)).replace("\\", "/"): path.read_text(encoding="utf-8") for path in ROOT.glob("infra/**/*.tf")}
joined = "\n".join(files.values())

checks = [
    ("IAC-001", "Terraform versions are bounded", 'required_version = ">= 1.16.0, < 2.0.0"' in joined),
    ("IAC-002", "AzureRM provider is pinned to maintained minor", 'version = "~> 5.3"' in joined),
    ("IAC-003", "Lab has mandatory expiration tag", "ExpiresAt" in files["infra/lab/main.tf"]),
    ("IAC-004", "Lab resource groups use generated project names", "module.naming.names.resource_group_" in files["infra/lab/main.tf"]),
    ("IAC-005", "Administrative ports are denied from Internet", 'name                       = "Deny-Internet-Administrative-Ports"' in files["infra/modules/network/main.tf"] and 'access                     = "Deny"' in files["infra/modules/network/main.tf"]),
    ("IAC-006", "Storage public objects and shared keys are disabled", "allow_nested_items_to_be_public = false" in files["infra/modules/security/main.tf"] and "shared_access_key_enabled       = false" in files["infra/modules/security/main.tf"]),
    ("IAC-007", "Storage minimum TLS is explicit", 'min_tls_version                 = "TLS1_2"' in files["infra/modules/security/main.tf"]),
    ("IAC-008", "Key Vault uses RBAC and purge protection", "rbac_authorization_enabled    = true" in files["infra/modules/security/main.tf"] and "purge_protection_enabled      = true" in files["infra/modules/security/main.tf"]),
    ("IAC-009", "Workload uses user-assigned managed identity", 'type         = "UserAssigned"' in files["infra/modules/workload/main.tf"]),
    ("IAC-010", "Container App scales to zero and one", "min_replicas = 0" in files["infra/modules/workload/main.tf"] and "max_replicas = 1" in files["infra/modules/workload/main.tf"]),
    ("IAC-011", "Sentinel ingestion has a low daily cap", "daily_quota_gb      = 0.1" in files["infra/modules/monitoring/main.tf"]),
    ("IAC-012", "No long-lived Azure client secret variable", "client_secret" not in joined.lower()),
    ("IAC-013", "Only a dedicated RheinShield management-group ID can be accepted", "managementgroups/rheinshield-[a-z0-9-]+$" in files["infra/enterprise-reference/variables.tf"] and "lower(var.dedicated_parent_management_group_resource_id)" in files["infra/enterprise-reference/variables.tf"] and "explicitly dedicated" in files["infra/enterprise-reference/variables.tf"]),
    ("IAC-014", "Policy assignment is non-enforcing in lab", "enforce              = false" in files["infra/policies/main.tf"]),
]
results = [{"id": item[0], "control": item[1], "status": "PASS" if item[2] else "FAIL"} for item in checks]
summary = {"scanner":"rheinshield-iac-security", "checks":len(results), "passed":sum(r["status"] == "PASS" for r in results), "failed":sum(r["status"] == "FAIL" for r in results), "results":results}
(ROOT / "artifacts/evidence/iac-security-scan.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k:summary[k] for k in ("scanner","checks","passed","failed")}, indent=2))
raise SystemExit(1 if summary["failed"] else 0)
