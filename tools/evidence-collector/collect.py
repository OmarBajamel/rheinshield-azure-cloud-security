"""Build a hashed manifest for public RheinShield evidence."""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "artifacts" / "evidence"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def provenance(name: str) -> str:
    if name in {"lighthouse.json", "screenshot-manifest.json"}:
        return "local Chrome production-build verification"
    if name == "live-publication-validation.json":
        return "hosted GitHub Pages and public GitHub Actions browser verification"
    if name == "fresh-clone-validation.json":
        return "fresh public GitHub clone reproducibility gate"
    if name in {"public-scan.json", "dist-scan.json", "security-scan-summary.json"}:
        return "automated public-release security and privacy gate"
    if name in {"terraform-validation.json", "iac-security-scan.json"}:
        return "offline Terraform/TFLint/custom IaC validation"
    if name in {"detection-test-results.json", "sentinel-template-validation.json"}:
        return "deterministic Sentinel fixture and template validation"
    if name in {"telemetry-manifest.json", "risk-register.json", "risk-register.csv"}:
        return "fixed-seed public-demo generation"
    if name in {"sbom.cdx.json", "license-inventory.json"}:
        return "release dependency inventory from lockfiles"
    return "public-demo documentation or offline validation"


def main() -> None:
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    commit = revision.stdout.strip() if revision.returncode == 0 else "UNCOMMITTED"
    public_scan_path = EVIDENCE / "public-scan.json"
    public_scan = json.loads(public_scan_path.read_text(encoding="utf-8")) if public_scan_path.exists() else {"status": "UNAVAILABLE"}
    screenshot_path = EVIDENCE / "screenshot-manifest.json"
    screenshot_review: dict[str, object] = json.loads(screenshot_path.read_text(encoding="utf-8")) if screenshot_path.exists() else {"privacyReview": "UNAVAILABLE"}
    screenshot_items = cast(list[dict[str, object]], screenshot_review.get("items", []))
    screenshot_status = screenshot_review.get("privacyReview")
    if screenshot_status is None and screenshot_items:
        screenshot_status = "PASS" if all(item.get("privacyReview") == "PASS" for item in screenshot_items) else "UNAVAILABLE"
    privacy_review = "PASS" if public_scan.get("status") == "PASS" and screenshot_status == "PASS" else "UNAVAILABLE"
    items = []
    for path in sorted(EVIDENCE.glob("*")):
        if path.is_file() and path.name not in {"evidence-manifest.json", "redaction-report.json"}:
            items.append({"path": str(path.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(path), "bytes": path.stat().st_size, "provenance": provenance(path.name)})
    output = {"schemaVersion": "1.0.0", "generatedAt": datetime.now(UTC).replace(microsecond=0).isoformat(), "commitSha": commit, "classification": "Public/Synthetic", "privacyReview": privacy_review, "privacyEvidence": {"publicScan": public_scan.get("status"), "screenshotReview": screenshot_status}, "items": items}
    (EVIDENCE / "evidence-manifest.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"items": len(items), "privacyReview": privacy_review, "commitSha": commit}))


if __name__ == "__main__":
    main()
