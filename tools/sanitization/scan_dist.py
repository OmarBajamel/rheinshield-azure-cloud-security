"""Scan the exact static bytes that will be uploaded to GitHub Pages."""
from __future__ import annotations

import hashlib
import ipaddress
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "dist"
TEXT_SUFFIXES = {".html", ".js", ".css", ".svg", ".txt", ".json", ".xml", ".webmanifest"}
PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "azure-secret": re.compile(r"(?i)(?:client_secret|password)\s*[=:]\s*[\"'][^\"']{8,}[\"']"),
    "email-or-upn": re.compile(r"\b[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,63}\b"),
    "bearer-token": re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{20,}"),
    "signed-url": re.compile(r"(?i)(?:[?&](?:sig|se|sp|sv|st)=)[^\s&#\"']+"),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
}
IPV4 = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if not DIST.is_dir():
        raise SystemExit("dist/ is missing; build before scanning the deployable artifact.")
    findings: list[dict[str, str]] = []
    files = sorted(path for path in DIST.rglob("*") if path.is_file())
    for path in files:
        relative = path.relative_to(DIST)
        label = str(relative).replace("\\", "/")
        if path.suffix.lower() in TEXT_SUFFIXES:
            value = path.read_text(encoding="utf-8")
            for rule, pattern in PATTERNS.items():
                for match in pattern.finditer(value):
                    matched = match.group(0).lower()
                    if rule == "email-or-upn" and matched.endswith((".invalid", "@example.com", "@example.org", "@example.net")):
                        continue
                    findings.append({"rule": rule, "path": label})
            for match in IPV4.finditer(value):
                try:
                    address = ipaddress.ip_address(match.group(0))
                except ValueError:
                    continue
                if address.is_global:
                    findings.append({"rule": "external-ipv4", "path": label})
        elif path.suffix.lower() == ".png":
            source = ROOT / "public" / relative
            if not source.is_file() or sha256(path) != sha256(source):
                findings.append({"rule": "unreviewed-binary", "path": label})
        else:
            findings.append({"rule": "unexpected-binary", "path": label})
    result = {
        "scanner": "rheinshield-pages-artifact-scan",
        "filesScanned": len(files),
        "findings": findings,
        "status": "PASS" if not findings else "FAIL",
    }
    output = ROOT / "artifacts" / "evidence" / "dist-scan.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
