import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).parents[2]
path = ROOT / "tools" / "compliance-export" / "generate.py"
spec = importlib.util.spec_from_file_location("compliance_export", path)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_registers_are_complete_and_consistent() -> None:
    assert module.main() == 0
    risks = json.loads((ROOT / "artifacts/evidence/risk-register.json").read_text(encoding="utf-8"))["risks"]
    controls = json.loads((ROOT / "artifacts/evidence/control-evidence-matrix.json").read_text(encoding="utf-8"))["controls"]
    assert len(risks) >= 25
    assert len({item["id"] for item in risks}) == len(risks)
    assert all(item["inherentScore"] == item["likelihood"] * item["impact"] for item in risks)
    assert all(item["residualScore"] <= item["inherentScore"] for item in risks)
    assert len(controls) >= 20
    assert all(item["evidence"] for item in controls)
