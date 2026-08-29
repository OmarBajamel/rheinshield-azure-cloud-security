#!/usr/bin/env python3
"""Offline validation and executable fixture tests for RheinShield Sentinel content.

The evaluator deliberately runs on a small normalized, table-independent fixture
contract. It does not execute KQL and must not be represented as live Microsoft
Sentinel validation or as a measure of production detection efficacy.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
SENTINEL = ROOT / "sentinel"
ARTIFACT = ROOT / "artifacts" / "evidence" / "detection-test-results.json"
MANIFEST = SENTINEL / "tests" / "fixtures" / "manifest.json"
FIXTURE_SEED = 20260829

REQUIRED_RULE_FIELDS = {
    "schema_version",
    "id",
    "name",
    "description",
    "version",
    "kind",
    "resource_type",
    "api_version",
    "enabled",
    "severity",
    "status",
    "required_data_sources",
    "query_frequency",
    "query_period",
    "trigger_operator",
    "trigger_threshold",
    "entity_mappings",
    "tactics",
    "techniques",
    "query",
    "false_positives",
    "tuning_guidance",
    "response_guidance",
    "fixture",
    "evaluator",
    "expected_test_result",
}


class ValidationFailure(Exception):
    """Raised for a content or fixture contract failure."""


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValidationFailure(f"{path}: YAML root must be a mapping")
    return value


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValidationFailure(f"{path}: JSON root must be an object")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _matches_any(value: str, candidates: tuple[str, ...]) -> bool:
    lowered = value.lower()
    return any(candidate.lower() in lowered for candidate in candidates)


def password_spray(row: dict[str, Any], _: dict[str, Any]) -> bool:
    return int(row["failed_attempts"]) >= 10 and int(row["targeted_accounts"]) >= 5


def success_after_failures(row: dict[str, Any], _: dict[str, Any]) -> bool:
    return row["failures"] >= 5 and row["success"] is True and 0 <= row["minutes_to_success"] <= 30


def impossible_travel(row: dict[str, Any], _: dict[str, Any]) -> bool:
    hours = float(row["elapsed_hours"])
    speed = float(row["distance_km"]) / hours if hours > 0 else math.inf
    return row["success"] is True and row["distance_km"] > 500 and speed > 900


def privileged_role_assignment(row: dict[str, Any], _: dict[str, Any]) -> bool:
    return row["result"].lower() == "success" and _matches_any(
        row["operation"],
        ("add member to role", "add eligible member to role", "add scoped member to role", "activate eligible assignment"),
    )


def service_principal_credential(row: dict[str, Any], _: dict[str, Any]) -> bool:
    if row["result"].lower() != "success":
        return False
    operation = row["operation"].lower()
    explicit = any(term in operation for term in ("add service principal credentials", "certificates and secrets", "federated identity credential"))
    properties = " ".join(row.get("modified_properties", [])).lower()
    update_with_credential = "update service principal" in operation and any(
        term in properties for term in ("keydescription", "passwordcredentials", "federatedidentitycredentials")
    )
    return explicit or update_with_credential


def conditional_access_change(row: dict[str, Any], _: dict[str, Any]) -> bool:
    operation = row["operation"].lower()
    return (
        row["result"].lower() == "success"
        and row["category"].lower() == "policy"
        and operation.startswith(("add", "update", "delete"))
        and any(term in operation for term in ("conditional access policy", "risk policy", "named location"))
    )


def unrestricted_inbound_rule(row: dict[str, Any], _: dict[str, Any]) -> bool:
    return (
        row["result"].lower() == "success"
        and row["direction"].lower() == "inbound"
        and row["source"] in {"*", "0.0.0.0/0", "::/0"}
        and row["access"].lower() == "allow"
    )


def monitoring_control_deleted(row: dict[str, Any], _: dict[str, Any]) -> bool:
    return row["result"].lower() == "success" and _matches_any(
        row["operation"],
        ("diagnosticsettings/delete", "pricings/delete", "dataexports/delete", "datacollectionrules/delete"),
    )


def storage_public_access(row: dict[str, Any], _: dict[str, Any]) -> bool:
    return row["result"].lower() == "success" and (
        row["allow_blob_public_access"] is True
        or row["public_network_access"].lower() == "enabled"
        or row["default_action"].lower() == "allow"
    )


def key_vault_access_spike(row: dict[str, Any], _: dict[str, Any]) -> bool:
    return (
        str(row["result"]).lower() == "success"
        and int(row["operation_count"]) >= 25
        and int(row["distinct_secrets"]) >= 10
    )


def encoded_powershell(row: dict[str, Any], _: dict[str, Any]) -> bool:
    if not row["process"].lower().endswith(("powershell.exe", "pwsh.exe")):
        return False
    command = row["command_line"].lower()
    switch = re.search(r"(?:^|\s)-(?:e|en|enc|enco|encod|encodedcommand)(?:\s|:|$)", command)
    return bool(switch) or "frombase64string" in command or "[char[]]" in command


def mass_object_download(row: dict[str, Any], _: dict[str, Any]) -> bool:
    return (
        200 <= row["status_code"] <= 299
        and row["operation"] in {"GetBlob", "GetBlobProperties", "ListBlobs"}
        and (row["distinct_objects"] >= 100 or row["bytes_returned"] >= 104857600)
    )


def unfamiliar_deployment_principal(row: dict[str, Any], fixture: dict[str, Any]) -> bool:
    if row["result"].lower() != "success" or "deployments/write" not in row["operation"].lower():
        return False
    matches = [item for item in fixture.get("approved", []) if item["principal"] == row["principal"]]
    return not matches or all(item["location"].lower() != row["location"].lower() for item in matches)


def repeated_denied_operations(row: dict[str, Any], _: dict[str, Any]) -> bool:
    return (
        row["result"].lower() == "failed"
        and row["substatus"].lower() in {"forbidden", "unauthorized", "authorizationfailed"}
        and row["denied_count"] >= 8
        and row["distinct_operations"] >= 3
    )


EVALUATORS: dict[str, Callable[[dict[str, Any], dict[str, Any]], bool]] = {
    name: value
    for name, value in globals().copy().items()
    if name
    in {
        "password_spray",
        "success_after_failures",
        "impossible_travel",
        "privileged_role_assignment",
        "service_principal_credential",
        "conditional_access_change",
        "unrestricted_inbound_rule",
        "monitoring_control_deleted",
        "storage_public_access",
        "key_vault_access_spike",
        "encoded_powershell",
        "mass_object_download",
        "unfamiliar_deployment_principal",
        "repeated_denied_operations",
    }
}


def validate_rule(path: Path, ids: set[str], names: set[str]) -> tuple[dict[str, Any], dict[str, Any]]:
    rule = _load_yaml(path)
    missing = REQUIRED_RULE_FIELDS - set(rule)
    if missing:
        raise ValidationFailure(f"{path}: missing fields {sorted(missing)}")
    try:
        uuid.UUID(str(rule["id"]))
    except ValueError as exc:
        raise ValidationFailure(f"{path}: id is not a UUID") from exc
    if rule["id"] in ids or rule["name"] in names:
        raise ValidationFailure(f"{path}: duplicate rule id or name")
    ids.add(rule["id"])
    names.add(rule["name"])
    if rule["kind"] != "Scheduled" or rule["enabled"] is not False:
        raise ValidationFailure(f"{path}: fixture-only rules must be Scheduled and disabled by default")
    if rule["resource_type"] != "Microsoft.SecurityInsights/alertRules" or str(rule["api_version"]) != "2025-09-01":
        raise ValidationFailure(f"{path}: analytics-rule resource type or API version is unsupported by this pack")
    if rule["status"] != "FIXTURE_VALIDATED" or rule["severity"] not in {"High", "Medium", "Low", "Informational"}:
        raise ValidationFailure(f"{path}: invalid status or severity")
    if not rule["required_data_sources"] or not rule["entity_mappings"]:
        raise ValidationFailure(f"{path}: data sources and entity mappings are required")
    if not all(re.fullmatch(r"T\d{4}(?:\.\d{3})?", str(item)) for item in rule["techniques"]):
        raise ValidationFailure(f"{path}: invalid MITRE technique identifier")
    query = rule["query"]
    if not isinstance(query, str) or "|" not in query or len(query.splitlines()) < 3 or "TODO" in query:
        raise ValidationFailure(f"{path}: KQL is empty, trivial, or contains a placeholder")
    if query.count("(") != query.count(")"):
        raise ValidationFailure(f"{path}: unbalanced parentheses in KQL")
    fixture_path = (path.parent / rule["fixture"]).resolve()
    if SENTINEL.resolve() not in fixture_path.parents or not fixture_path.is_file():
        raise ValidationFailure(f"{path}: fixture does not resolve inside sentinel or is missing")
    fixture = _load_json(fixture_path)
    if fixture.get("seed") != FIXTURE_SEED:
        raise ValidationFailure(f"{fixture_path}: unexpected deterministic seed")
    if fixture.get("expected") != rule["expected_test_result"]:
        raise ValidationFailure(f"{path}: fixture and rule expected results differ")
    evaluator = EVALUATORS.get(rule["evaluator"])
    if evaluator is None:
        raise ValidationFailure(f"{path}: unknown evaluator {rule['evaluator']}")
    baseline_alerts = sum(bool(evaluator(row, fixture)) for row in fixture["baseline"])
    malicious_alerts = sum(bool(evaluator(row, fixture)) for row in fixture["malicious"])
    actual = {"baseline_alerts": baseline_alerts, "malicious_alerts": malicious_alerts}
    if actual != rule["expected_test_result"]:
        raise ValidationFailure(f"{path}: expected {rule['expected_test_result']}, got {actual}")
    return rule, {
        "id": rule["id"],
        "name": rule["name"],
        "file": str(path.relative_to(ROOT)).replace("\\", "/"),
        "fixture": str(fixture_path.relative_to(ROOT)).replace("\\", "/"),
        "evaluator": rule["evaluator"],
        "baseline_alerts": baseline_alerts,
        "malicious_alerts": malicious_alerts,
        "result": "PASS",
    }


def validate_hunting_queries() -> list[str]:
    paths = sorted((SENTINEL / "hunting-queries").glob("*.yaml"))
    if len(paths) < 5:
        raise ValidationFailure("at least five hunting queries are required")
    ids: set[str] = set()
    for path in paths:
        item = _load_yaml(path)
        required = {"id", "name", "description", "status", "required_data_sources", "tactics", "techniques", "query"}
        if required - set(item) or item["status"] != "READY_NOT_AUTHENTICATED":
            raise ValidationFailure(f"{path}: invalid hunting-query metadata")
        uuid.UUID(str(item["id"]))
        if item["id"] in ids or "|" not in item["query"] or "TODO" in item["query"]:
            raise ValidationFailure(f"{path}: duplicate id or invalid KQL")
        ids.add(item["id"])
    return [str(path.relative_to(ROOT)).replace("\\", "/") for path in paths]


def validate_workbooks() -> list[str]:
    paths = sorted((SENTINEL / "workbooks").glob("*.json"))
    if len(paths) != 3:
        raise ValidationFailure("exactly three RheinShield workbook templates are expected")
    for path in paths:
        template = _load_json(path)
        resources = template.get("resources", [])
        if len(resources) != 1:
            raise ValidationFailure(f"{path}: expected one workbook resource")
        resource = resources[0]
        if resource.get("type") != "Microsoft.Insights/workbooks" or resource.get("apiVersion") != "2023-06-01":
            raise ValidationFailure(f"{path}: workbook resource type or API version is unsupported by this pack")
        notebook = json.loads(resource["properties"]["serializedData"])
        if notebook.get("version") != "Notebook/1.0":
            raise ValidationFailure(f"{path}: invalid workbook serialization version")
        queries = [item for item in notebook.get("items", []) if item.get("type") == 3]
        notices = [item for item in notebook.get("items", []) if item.get("type") == 1]
        if len(queries) < 5 or not notices or "Synthetic" not in notices[0]["content"]["json"]:
            raise ValidationFailure(f"{path}: workbook lacks required queries or synthetic-data notice")
        if any("|" not in item["content"].get("query", "") for item in queries):
            raise ValidationFailure(f"{path}: workbook contains an invalid query item")
    return [str(path.relative_to(ROOT)).replace("\\", "/") for path in paths]


def _balanced_bicep(text: str, path: Path) -> None:
    for opening, closing in (("{", "}"), ("[", "]"), ("(", ")")):
        if text.count(opening) != text.count(closing):
            raise ValidationFailure(f"{path}: unbalanced {opening}{closing}")


def validate_automation_rules() -> list[str]:
    paths = sorted((SENTINEL / "automation-rules").glob("*.bicep"))
    if len(paths) != 3:
        raise ValidationFailure("exactly three automation-rule templates are expected")
    for path in paths:
        text = path.read_text(encoding="utf-8")
        _balanced_bicep(text, path)
        required = ("Microsoft.SecurityInsights/automationRules@2025-09-01", "param automationEnabled bool = false", "AddIncidentTask")
        if not all(value in text for value in required) or "RunPlaybook" in text:
            raise ValidationFailure(f"{path}: invalid or unsafe automation-rule template")
    return [str(path.relative_to(ROOT)).replace("\\", "/") for path in paths]


def validate_playbooks() -> list[str]:
    paths = sorted((SENTINEL / "playbooks").glob("*.bicep"))
    if len(paths) != 3:
        raise ValidationFailure("exactly three playbook templates are expected")
    forbidden = ("ApiConnection", "HttpWebhook", "Send_email", "Microsoft.Web/connections", "roleAssignments")
    for path in paths:
        text = path.read_text(encoding="utf-8")
        _balanced_bicep(text, path)
        required = ("Microsoft.Logic/workflows@2019-05-01", "state: 'Disabled'", "dryRun: true", "externalSideEffects: false")
        if not all(value in text for value in required) or any(value in text for value in forbidden):
            raise ValidationFailure(f"{path}: playbook is not disabled, dry-run-only, or connector-free")
    return [str(path.relative_to(ROOT)).replace("\\", "/") for path in paths]


def validate_watchlist() -> list[str]:
    directory = SENTINEL / "watchlists"
    bicep = directory / "known-deployment-principals.bicep"
    csv_path = directory / "known-deployment-principals.csv"
    if not bicep.is_file() or not csv_path.is_file():
        raise ValidationFailure("RS013 requires the synthetic KnownDeploymentPrincipals watchlist")
    text = bicep.read_text(encoding="utf-8")
    _balanced_bicep(text, bicep)
    required = (
        "Microsoft.SecurityInsights/watchlists@2025-09-01",
        "watchlistAlias: 'KnownDeploymentPrincipals'",
        "itemsSearchKey: 'Principal'",
        "loadTextContent('known-deployment-principals.csv')",
        "'Synthetic'",
    )
    if not all(value in text for value in required):
        raise ValidationFailure("watchlist Bicep is missing its supported API, alias, search key, or synthetic label")
    lines = [line for line in csv_path.read_text(encoding="utf-8").splitlines() if line]
    if lines[0] != "Principal,Location,Environment,Owner,ExpiresAt" or len(lines) < 4:
        raise ValidationFailure("watchlist CSV has an invalid contract or too few synthetic entries")
    return [str(path.relative_to(ROOT)).replace("\\", "/") for path in (bicep, csv_path)]


def validate_docs() -> list[str]:
    expected = [
        "DETECTION_CATALOG.md",
        "MITRE_COVERAGE.md",
        "TUNING_REGISTER.md",
        "INCIDENT_TRIAGE_RUNBOOK.md",
        "SOAR_SAFETY.md",
        "DETECTION_TESTING.md",
        "API_VERSION_DECISIONS.md",
    ]
    paths = [ROOT / "docs" / "sentinel" / value for value in expected]
    missing = [str(path) for path in paths if not path.is_file() or path.stat().st_size < 200]
    if missing:
        raise ValidationFailure(f"missing or trivial Sentinel documentation: {missing}")
    return [str(path.relative_to(ROOT)).replace("\\", "/") for path in paths]


def validate_all() -> dict[str, Any]:
    rule_paths = sorted((SENTINEL / "analytics-rules").glob("*.yaml"))
    if len(rule_paths) != 14:
        raise ValidationFailure(f"expected 14 analytics rules, found {len(rule_paths)}")
    ids: set[str] = set()
    names: set[str] = set()
    rules: list[dict[str, Any]] = []
    tests: list[dict[str, Any]] = []
    for path in rule_paths:
        rule, result = validate_rule(path, ids, names)
        rules.append(rule)
        tests.append(result)
    tp = sum(item["malicious_alerts"] for item in tests)
    fp = sum(item["baseline_alerts"] for item in tests)
    fn = len(tests) - tp
    tn = len(tests) - fp
    hunting = validate_hunting_queries()
    workbooks = validate_workbooks()
    automation = validate_automation_rules()
    playbooks = validate_playbooks()
    watchlist = validate_watchlist()
    docs = validate_docs()
    fixture_paths = sorted((SENTINEL / "tests" / "fixtures").glob("rs*.json"))
    return {
        "schema_version": "1.0.0",
        "status": "FIXTURE_VALIDATED",
        "validation_mode": "offline normalized fixture evaluator",
        "live_validation": False,
        "production_efficacy_claim": False,
        "fixture_seed": FIXTURE_SEED,
        "summary": {
            "analytics_rules": len(rules),
            "rule_fixture_tests_passed": len(tests),
            "rule_fixture_tests_failed": 0,
            "baseline_cases": len(tests),
            "malicious_cases": len(tests),
            "true_positives": tp,
            "false_positives": fp,
            "true_negatives": tn,
            "false_negatives": fn,
            "fixture_precision": tp / (tp + fp) if tp + fp else 0,
            "fixture_recall": tp / (tp + fn) if tp + fn else 0,
            "hunting_queries": len(hunting),
            "workbooks": len(workbooks),
            "automation_rules": len(automation),
            "playbooks": len(playbooks),
            "watchlists": 1,
        },
        "rules": tests,
        "validated_content": {
            "hunting_queries": hunting,
            "workbooks": workbooks,
            "automation_rules": automation,
            "playbooks": playbooks,
            "watchlist": watchlist,
            "documentation": docs,
        },
        "fixtures": [
            {
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": _sha256(path),
            }
            for path in fixture_paths
        ],
    }


def _timestamp() -> str:
    epoch = os.getenv("SOURCE_DATE_EPOCH")
    moment = datetime.fromtimestamp(int(epoch), tz=UTC) if epoch else datetime.now(UTC)
    return moment.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_results(result: dict[str, Any]) -> None:
    output = {**result, "executed_at": _timestamp(), "harness": "tools/detection-test-harness/validate.py"}
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "schema_version": "1.0.0",
        "seed": FIXTURE_SEED,
        "dataset": "RheinShield compact normalized Sentinel fixtures",
        "data_classification": "Synthetic",
        "incident": "INC-001",
        "fixture_count": len(result["fixtures"]),
        "fixtures": result["fixtures"],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-results", action="store_true", help="write evidence only after every validation succeeds")
    args = parser.parse_args()
    try:
        result = validate_all()
        if args.write_results:
            write_results(result)
        print(json.dumps(result["summary"], indent=2))
        print("PASS: offline Sentinel content and fixture validation completed")
        return 0
    except (ValidationFailure, KeyError, TypeError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
