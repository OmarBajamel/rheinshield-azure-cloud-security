"""Verify freshness, provenance, raw source, plan binding, currency, and cost ceiling."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--attestation", required=True, type=Path)
    parser.add_argument("--raw-infracost", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--max-eur", default="20")
    args = parser.parse_args()
    evidence = json.loads(args.attestation.read_text(encoding="utf-8-sig"))
    if evidence.get("status") != "LIVE_VALIDATED" or evidence.get("source") != "Infracost JSON" or evidence.get("currency") != "EUR":
        raise SystemExit("Cost evidence has invalid status, source, or currency.")
    generated = datetime.fromisoformat(str(evidence["generatedAt"]).replace("Z", "+00:00"))
    age = (datetime.now(UTC) - generated).total_seconds()
    if age < 0 or age > 3600:
        raise SystemExit("Cost evidence is stale; regenerate it from the current plan.")
    if evidence.get("terraformPlanSha256") != digest(args.plan):
        raise SystemExit("Cost evidence is not bound to the current Terraform plan.")
    if evidence.get("rawInfracostSha256") != digest(args.raw_infracost):
        raise SystemExit("Raw Infracost evidence hash does not match the attestation.")
    try:
        estimate = Decimal(str(evidence["estimatedIncrementalCostEur"]))
        ceiling = Decimal(args.max_eur)
    except (KeyError, InvalidOperation) as exc:
        raise SystemExit("Cost evidence has no valid numeric estimate.") from exc
    if estimate <= 0 or estimate > ceiling:
        raise SystemExit(f"Estimated incremental cost must be positive and <= EUR {ceiling}.")
    print(f"Cost gate PASS: EUR {estimate} <= EUR {ceiling}; exact plan and source hashes verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
