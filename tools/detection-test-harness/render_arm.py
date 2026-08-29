#!/usr/bin/env python3
"""Render the YAML analytics-rule source of truth into an ARM deployment template."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "sentinel" / "analytics-rules"


def _entity_mappings(rule: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "entityType": mapping["entity_type"],
            "fieldMappings": [
                {
                    "identifier": field["identifier"],
                    "columnName": field["column_name"],
                }
                for field in mapping["field_mappings"]
            ],
        }
        for mapping in rule["entity_mappings"]
    ]


def render() -> dict[str, Any]:
    resources: list[dict[str, Any]] = []
    for path in sorted(RULES.glob("*.yaml")):
        with path.open("r", encoding="utf-8") as handle:
            rule = yaml.safe_load(handle)
        resources.append(
            {
                "scope": "[format('Microsoft.OperationalInsights/workspaces/{0}', parameters('workspaceName'))]",
                "type": rule["resource_type"],
                "apiVersion": rule["api_version"],
                "name": rule["id"],
                "kind": rule["kind"],
                "properties": {
                    "displayName": rule["name"],
                    "description": rule["description"],
                    "enabled": rule["enabled"],
                    "severity": rule["severity"],
                    "query": rule["query"],
                    "queryFrequency": rule["query_frequency"],
                    "queryPeriod": rule["query_period"],
                    "triggerOperator": rule["trigger_operator"],
                    "triggerThreshold": rule["trigger_threshold"],
                    "suppressionEnabled": rule["suppression_enabled"],
                    "suppressionDuration": rule["suppression_duration"],
                    "tactics": rule["tactics"],
                    "techniques": rule["techniques"],
                    "entityMappings": _entity_mappings(rule),
                    "eventGroupingSettings": {"aggregationKind": "SingleAlert"},
                    "incidentConfiguration": {
                        "createIncident": True,
                        "groupingConfiguration": {
                            "enabled": True,
                            "reopenClosedIncident": False,
                            "lookbackDuration": "PT5H",
                            "matchingMethod": "AllEntities",
                            "groupByEntities": [],
                            "groupByAlertDetails": [],
                            "groupByCustomDetails": [],
                        },
                    },
                },
            }
        )
    return {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "metadata": {
            "generator": "tools/detection-test-harness/render_arm.py",
            "status": "PLAN_VALIDATED",
            "note": "Generated rules remain disabled. Deployment does not establish connector availability or live validation.",
        },
        "parameters": {
            "workspaceName": {
                "type": "string",
                "metadata": {"description": "Existing Log Analytics workspace with Microsoft Sentinel enabled."},
            }
        },
        "resources": resources,
        "outputs": {"analyticsRuleCount": {"type": "int", "value": len(resources)}},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="output path; stdout is used when omitted")
    args = parser.parse_args()
    payload = json.dumps(render(), indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
