"""Sanitize RheinShield evidence while preserving stable public aliases."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

RULES = [
    ("tenant-id", re.compile(r"(?i)(tenant(?:Id|_id)?[\"' :=]+)[0-9a-f]{8}-[0-9a-f-]{27,}"), r"\1TENANT-REDACTED"),
    ("subscription-id", re.compile(r"(?i)(subscription(?:Id|_id)?[\"' :=]+)[0-9a-f]{8}-[0-9a-f-]{27,}"), r"\1SUBSCRIPTION-REDACTED"),
    ("email", re.compile(r"(?i)\b[A-Z0-9._%+-]+@(?!example\.(?:com|org|net)\b)[A-Z0-9.-]+\.[A-Z]{2,}\b"), "IDENTITY-REDACTED"),
    ("ipv4", re.compile(r"\b(?!(?:10|127|192\.168)\.)(?:\d{1,3}\.){3}\d{1,3}\b"), "IP-REDACTED"),
    ("bearer-token", re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/=-]{16,}"), "Bearer TOKEN-REDACTED"),
    ("signed-query", re.compile(r"(?i)([?&](?:sig|token|code|secret)=)[^&\s\"']+"), r"\1REDACTED"),
]


def sanitize_text(value: str) -> tuple[str, list[dict[str, Any]]]:
    report: list[dict[str, Any]] = []
    for name, pattern, replacement in RULES:
        value, count = pattern.subn(replacement, value)
        if count:
            report.append({"rule": name, "replacements": count})
    return value, report


def sanitize_file(source: Path, target: Path) -> dict[str, Any]:
    clean, rules = sanitize_text(source.read_text(encoding="utf-8"))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(clean, encoding="utf-8")
    return {"source": str(source), "output": str(target), "rules": rules, "sha256": hashlib.sha256(clean.encode()).hexdigest()}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = sanitize_file(args.source, args.target)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))
