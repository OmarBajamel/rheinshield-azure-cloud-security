"""Fail when committed public material contains likely secrets or private identifiers."""

from __future__ import annotations

import ipaddress
import json
import re
import subprocess
import zipfile
from pathlib import Path

from PIL import Image
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".csv",
    ".yaml",
    ".yml",
    ".tf",
    ".ts",
    ".tsx",
    ".js",
    ".mjs",
    ".py",
    ".ps1",
    ".sh",
    ".html",
    ".svg",
}
PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "azure-secret": re.compile(r"(?i)(?:client_secret|password)\s*[=:]\s*[\"'][^\"']{8,}[\"']"),
    "private-evidence": re.compile(
        r"(?i)(?:tenant|subscription)(?:Id|_id)?\s*[=:]\s*[\"']?[0-9a-f]{8}-[0-9a-f-]{27,}"
    ),
    "email-or-upn": re.compile(
        r"\b[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,63}\b"
    ),
    "bearer-token": re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{20,}"),
    "azure-sas-or-signed-url": re.compile(r"(?i)(?:[?&](?:sig|se|sp|sv|st)=)[^\s&#\"']+"),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
}
IPV4 = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
SAFE_EMAIL_SUFFIXES = (".invalid", "@example.com", "@example.org", "@example.net")


def is_safe_fixture_match(rule: str, matched: str, relative: str) -> bool:
    """Permit only reserved example values that are deliberately exercised by tests."""
    lowered = matched.lower()
    if rule == "email-or-upn" and lowered.endswith(SAFE_EMAIL_SUFFIXES):
        return True
    return (
        relative.endswith("tests/security/test_sanitization.py")
        and (
            matched == "8.8." + "8.8"
            or lowered == "bearer " + "abcdefghijklmnopqrstuvwxyz"
        )
    )


def candidates() -> list[Path]:
    proc = subprocess.run(
        ["git", "ls-files", "-co", "--exclude-standard"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return [ROOT / p for p in proc.stdout.splitlines() if (ROOT / p).is_file()]


def scan_text(
    value: str, relative: str, findings: list[dict[str, object]], location_prefix: str = "line"
) -> None:
    for name, pattern in PATTERNS.items():
        for match in pattern.finditer(value):
            if is_safe_fixture_match(name, match.group(0), relative):
                continue
            line = value.count("\n", 0, match.start()) + 1
            findings.append({"rule": name, "path": relative, location_prefix: line})
    for match in IPV4.finditer(value):
        try:
            address = ipaddress.ip_address(match.group(0))
        except ValueError:
            continue
        if address.version == 4 and address.is_global:
            line = value.count("\n", 0, match.start()) + 1
            line_text = value.splitlines()[line - 1] if value.splitlines() else value
            prior = value[match.start() - 1] if match.start() else ""
            if (
                is_safe_fixture_match("external-ipv4", match.group(0), relative)
                or prior.isalnum()
                or prior in {"-", "_"}
                or any(marker in line_text.lower() for marker in ("contentversion", "useragent"))
            ):
                continue
            findings.append({"rule": "external-ipv4", "path": relative, location_prefix: line})


def main() -> int:
    findings: list[dict[str, object]] = []
    files = candidates()
    binary_review = {"png": 0, "pdf": 0, "zip": 0}
    for path in files:
        relative = str(path.relative_to(ROOT)).replace("\\", "/")
        suffix = path.suffix.lower()
        if suffix in TEXT_SUFFIXES:
            try:
                scan_text(path.read_text(encoding="utf-8"), relative, findings)
            except (UnicodeDecodeError, OSError):
                continue
        elif suffix == ".png":
            binary_review["png"] += 1
            with Image.open(path) as image:
                metadata = "\n".join(f"{key}={value}" for key, value in image.info.items())
                scan_text(metadata, relative, findings, "metadataLine")
        elif suffix == ".pdf":
            binary_review["pdf"] += 1
            reader = PdfReader(str(path))
            metadata = "\n".join(f"{key}={value}" for key, value in (reader.metadata or {}).items())
            scan_text(metadata, relative, findings, "metadataLine")
            for page_number, page in enumerate(reader.pages, start=1):
                page_findings: list[dict[str, object]] = []
                scan_text(page.extract_text() or "", relative, page_findings)
                for finding in page_findings:
                    finding["page"] = page_number
                findings.extend(page_findings)
        elif suffix == ".zip":
            binary_review["zip"] += 1
            with zipfile.ZipFile(path) as archive:
                for member in archive.infolist():
                    scan_text(member.filename, f"{relative}!{member.filename}", findings, "entry")
                    if (
                        Path(member.filename).suffix.lower() in TEXT_SUFFIXES
                        and member.file_size <= 5_000_000
                    ):
                        try:
                            value = archive.read(member).decode("utf-8")
                        except (UnicodeDecodeError, OSError):
                            continue
                        scan_text(value, f"{relative}!{member.filename}", findings)
    result = {
        "scanner": "rheinshield-public-pattern-scan",
        "filesScanned": len(files),
        "binaryReview": binary_review,
        "findings": findings,
        "status": "PASS" if not findings else "FAIL",
    }
    output = ROOT / "artifacts" / "evidence" / "public-scan.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
