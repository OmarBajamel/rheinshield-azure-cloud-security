"""Create a short-lived cost attestation from Infracost JSON and an exact plan."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-infracost", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--output", default=ROOT / ".private" / "cost-estimate.json", type=Path)
    args = parser.parse_args()
    raw_path = args.raw_infracost.resolve()
    plan_path = args.plan.resolve()
    output_path = args.output.resolve()
    private_root = (ROOT / ".private").resolve()
    if private_root not in output_path.parents:
        raise SystemExit("Cost attestation must remain under the gitignored .private directory.")
    raw = json.loads(raw_path.read_text(encoding="utf-8-sig"))
    if raw.get("currency") != "EUR" or not isinstance(raw.get("projects"), list):
        raise SystemExit("Infracost JSON must explicitly use EUR and contain projects.")
    try:
        total = sum(
            (Decimal(str(project["breakdown"]["totalMonthlyCost"])) for project in raw["projects"]),
            Decimal("0"),
        )
    except (KeyError, InvalidOperation, TypeError) as exc:
        raise SystemExit("Infracost JSON has no valid project monthly-cost totals.") from exc
    if total <= 0:
        raise SystemExit("A positive machine-derived estimate is required.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    attestation = {
        "schemaVersion": "1.0.0",
        "status": "LIVE_VALIDATED",
        "source": "Infracost JSON",
        "sourceVersion": str(raw.get("version", "reported-by-source")),
        "generatedAt": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "currency": "EUR",
        "estimatedIncrementalCostEur": str(total.quantize(Decimal("0.01"))),
        "terraformPlanSha256": digest(plan_path),
        "rawInfracostSha256": digest(raw_path),
    }
    output_path.write_text(json.dumps(attestation, indent=2) + "\n", encoding="utf-8")
    print("Created a private, one-hour cost attestation bound to the exact Terraform plan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
