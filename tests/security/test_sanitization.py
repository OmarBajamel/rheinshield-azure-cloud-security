import importlib.util
from pathlib import Path

MODULE = Path(__file__).parents[2] / "tools" / "sanitization" / "sanitize.py"
spec = importlib.util.spec_from_file_location("sanitize", MODULE)
sanitize = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(sanitize)


def test_sanitizes_private_values():
    private_id = "11111111" + "-2222-3333-4444-555555555555"
    raw = f"tenantId={private_id} user@corp.invalid 8.8.8.8 Bearer abcdefghijklmnopqrstuvwxyz"
    clean, report = sanitize.sanitize_text(raw)
    assert "11111111" not in clean
    assert "user@corp.invalid" not in clean
    assert "8.8.8.8" not in clean
    assert "abcdefghijklmnopqrstuvwxyz" not in clean
    assert len(report) == 4


def test_preserves_documentation_examples():
    clean, report = sanitize.sanitize_text("reviewer@example.com 10.2.3.4 192.168.4.5")
    assert clean == "reviewer@example.com 10.2.3.4 192.168.4.5"
    assert not report
