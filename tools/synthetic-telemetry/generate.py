#!/usr/bin/env python3
"""Generate deterministic 90-day RheinShield public-demo telemetry."""

from __future__ import annotations

import hashlib
import json
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "data" / "public-demo" / "telemetry.jsonl"
TIMELINE = ROOT / "data" / "public-demo" / "inc-001-timeline.json"
MANIFEST = ROOT / "artifacts" / "evidence" / "telemetry-manifest.json"
SEED = 20260829
START = datetime(2026, 6, 1, 0, 0, tzinfo=UTC)

USERS = ["analyst-01", "developer-02", "operator-03", "buyer-04", "supplier-05", "contractor-07"]
EVENTS = ["SigninSuccess", "OrderCreated", "ResourceRead", "KeyVaultSecretGet", "PolicyEvaluated", "BlobRead"]


def baseline_events(rng: random.Random) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for day in range(90):
        for index in range(8):
            timestamp = START + timedelta(days=day, minutes=75 * index + rng.randint(0, 40))
            rows.append({
                "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
                "event_id": f"evt-{day:03d}-{index:02d}",
                "category": rng.choice(EVENTS),
                "actor": rng.choice(USERS[:-1]),
                "resource": rng.choice(["order-api", "catalogue", "vault-public-alias", "storage-public-alias", "policy-baseline"]),
                "result": "Success",
                "severity": "Informational",
                "synthetic": True,
                "incident_id": None,
            })
    return rows


def incident_events() -> list[dict[str, object]]:
    base = datetime(2026, 8, 27, 7, 25, tzinfo=UTC)
    details = [
        (0, "PasswordSpray", "contractor-07", "Entra", "Medium", "12 failures across 6 accounts"),
        (6, "SuspiciousSignin", "contractor-07", "Entra", "High", "successful sign-in after failures"),
        (12, "ImpossibleTravel", "contractor-07", "Entra", "High", "synthetic 6,180 km in 1.2 hours"),
        (19, "PrivilegedRoleAssignment", "contractor-07", "Entra", "High", "eligible role activated"),
        (23, "ServicePrincipalCredentialAdded", "contractor-07", "workload-sp", "High", "credential fixture created"),
        (26, "ConditionalAccessChanged", "contractor-07", "ca-public-alias", "High", "report-only policy changed"),
        (30, "NSGRuleBroadened", "contractor-07", "nsg-public-alias", "High", "0.0.0.0/0 inbound fixture"),
        (33, "DiagnosticSettingDeleted", "contractor-07", "diag-public-alias", "High", "control-plane log fixture"),
        (36, "StoragePublicAccessEnabled", "contractor-07", "storage-public-alias", "High", "network default allow fixture"),
        (39, "KeyVaultEnumeration", "contractor-07", "vault-public-alias", "High", "34 operations across 14 aliases"),
        (42, "EncodedPowerShell", "host-fixture-01", "safe-process-fixture", "Medium", "non-executed encoded command fixture"),
        (45, "MassObjectDownload", "contractor-07", "storage-public-alias", "High", "126 synthetic objects"),
        (49, "UnfamiliarDeployment", "principal-fixture-09", "rg-public-alias", "Medium", "unexpected principal/location"),
        (53, "RepeatedDeniedOperations", "contractor-07", "AzureControlPlane", "Medium", "11 denied across 4 operations"),
        (6, "IncidentCreated", "sentinel-fixture", "INC-001", "High", "first alert opened the incident; subsequent rules were correlated"),
        (15, "AnalystAcknowledged", "analyst-01", "INC-001", "High", "triage started"),
        (42, "ContainmentRecommended", "analyst-01", "INC-001", "High", "dry-run change plan approved"),
        (63, "IncidentContained", "analyst-01", "INC-001", "Medium", "exercise containment complete"),
    ]
    return [{
        "timestamp": (base + timedelta(minutes=offset)).isoformat().replace("+00:00", "Z"),
        "event_id": f"inc001-{index + 1:02d}",
        "category": category,
        "actor": actor,
        "resource": resource,
        "result": "Success",
        "severity": severity,
        "detail": detail,
        "synthetic": True,
        "incident_id": "INC-001",
    } for index, (offset, category, actor, resource, severity, detail) in enumerate(details)]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    rng = random.Random(SEED)
    records = sorted(baseline_events(rng) + incident_events(), key=lambda row: str(row["timestamp"]))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in records), encoding="utf-8")
    timeline = {
        "incidentId": "INC-001",
        "title": "Compromised Privileged Contractor Account and Cloud Control Changes",
        "dataMode": "public-demo",
        "exerciseMetrics": {"mttdMinutes": 6, "mttaMinutes": 9, "mttrMinutes": 48},
        "events": incident_events(),
    }
    TIMELINE.write_text(json.dumps(timeline, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "schemaVersion": "1.0.0",
        "seed": SEED,
        "rangeStart": START.isoformat().replace("+00:00", "Z"),
        "rangeEnd": (START + timedelta(days=89, hours=23, minutes=59)).isoformat().replace("+00:00", "Z"),
        "baselineDays": 90,
        "baselineEvents": len(records) - len(incident_events()),
        "incidentEvents": len(incident_events()),
        "totalEvents": len(records),
        "dataClassification": "Synthetic",
        "output": str(OUTPUT.relative_to(ROOT)).replace("\\", "/"),
        "sha256": sha256(OUTPUT),
        "reproducible": True,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
