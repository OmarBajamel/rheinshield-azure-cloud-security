import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[2]
ATTEST = ROOT / "tools" / "cost-gate" / "attest.py"
VERIFY = ROOT / "tools" / "cost-gate" / "verify.py"


def test_cost_attestation_binds_source_and_plan(tmp_path: Path):
    private = ROOT / ".private" / "pytest-cost-gate"
    private.mkdir(parents=True, exist_ok=True)
    raw = tmp_path / "infracost.json"
    plan = tmp_path / "rheinshield.tfplan"
    attestation = private / "cost-estimate.json"
    raw.write_text(
        json.dumps(
            {
                "currency": "EUR",
                "version": "test",
                "projects": [{"breakdown": {"totalMonthlyCost": "12.34"}}],
            }
        ),
        encoding="utf-8",
    )
    plan.write_bytes(b"immutable-test-plan")
    try:
        subprocess.run(
            [
                sys.executable,
                str(ATTEST),
                "--raw-infracost",
                str(raw),
                "--plan",
                str(plan),
                "--output",
                str(attestation),
            ],
            check=True,
        )
        subprocess.run(
            [
                sys.executable,
                str(VERIFY),
                "--attestation",
                str(attestation),
                "--raw-infracost",
                str(raw),
                "--plan",
                str(plan),
                "--max-eur",
                "20",
            ],
            check=True,
        )
        plan.write_bytes(b"changed-plan")
        failed = subprocess.run(
            [
                sys.executable,
                str(VERIFY),
                "--attestation",
                str(attestation),
                "--raw-infracost",
                str(raw),
                "--plan",
                str(plan),
                "--max-eur",
                "20",
            ],
            capture_output=True,
            text=True,
        )
        assert failed.returncode != 0
        assert "not bound" in failed.stderr
    finally:
        if attestation.exists():
            attestation.unlink()
        if private.exists():
            private.rmdir()
