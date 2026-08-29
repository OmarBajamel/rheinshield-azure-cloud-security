import hashlib
import importlib.util
from pathlib import Path

ROOT = Path(__file__).parents[2]
MODULE_PATH = ROOT / "tools" / "synthetic-telemetry" / "generate.py"
spec = importlib.util.spec_from_file_location("telemetry_generator", MODULE_PATH)
assert spec and spec.loader
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


def test_generator_is_deterministic() -> None:
    assert generator.main() == 0
    first = hashlib.sha256(generator.OUTPUT.read_bytes()).hexdigest()
    assert generator.main() == 0
    second = hashlib.sha256(generator.OUTPUT.read_bytes()).hexdigest()
    assert first == second


def test_covers_90_days_and_all_anomalies() -> None:
    baseline = generator.baseline_events(__import__("random").Random(generator.SEED))
    incident = generator.incident_events()
    assert len({row["timestamp"][:10] for row in baseline}) == 90
    assert len(incident) == 18
    assert {row["category"] for row in incident}.issuperset({"PasswordSpray", "KeyVaultEnumeration", "MassObjectDownload", "IncidentContained"})
