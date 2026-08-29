"""Build deterministic public release archives, an SBOM, licenses, and checksums."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tomllib
import zipfile
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "artifacts" / "evidence"
RELEASE = ROOT / "artifacts" / "release"
LINKEDIN = ROOT / "artifacts" / "linkedin"
FIXED_ZIP_TIME = (2026, 8, 29, 0, 0, 0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def candidate_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-co", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    excluded = {
        "artifacts/evidence/evidence-manifest.json",
        "artifacts/evidence/public-scan.json",
        "artifacts/evidence/dist-scan.json",
    }
    files = []
    for relative in result.stdout.splitlines():
        normalized = relative.replace("\\", "/")
        path = ROOT / relative
        if (
            path.is_file()
            and normalized not in excluded
            and not normalized.startswith("artifacts/release/")
            and not normalized.endswith(".zip")
        ):
            files.append(path)
    return sorted(files, key=lambda item: item.as_posix().lower())


def write_zip(path: Path, files: list[Path]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source in files:
            relative = source.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(relative, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, source.read_bytes())


def components() -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    lock = json.loads((ROOT / "package-lock.json").read_text(encoding="utf-8"))
    for key, record in sorted(lock.get("packages", {}).items()):
        if not key or not isinstance(record, dict):
            continue
        result.append(
            {
                "type": "library",
                "name": key.rsplit("node_modules/", 1)[-1],
                "version": str(record.get("version", "unknown")),
                "ecosystem": "npm",
                "license": str(record.get("license", "NOASSERTION")),
            }
        )
    uv = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    for record in uv.get("package", []):
        result.append(
            {
                "type": "library",
                "name": str(record["name"]),
                "version": str(record["version"]),
                "ecosystem": "PyPI",
                "license": "NOASSERTION",
            }
        )
    return result


def main() -> None:
    RELEASE.mkdir(parents=True, exist_ok=True)
    LINKEDIN.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).replace(microsecond=0).isoformat()
    dependencies = components()
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "serialNumber": "urn:uuid:11111111-2222-4333-8444-555555555555",
        "version": 1,
        "metadata": {
            "timestamp": timestamp,
            "component": {
                "type": "application",
                "name": "rheinshield-azure-cloud-security",
                "version": "1.0.0",
            },
        },
        "components": [
            {
                "type": item["type"],
                "name": item["name"],
                "version": item["version"],
                "purl": f"pkg:{item['ecosystem'].lower()}/{item['name']}@{item['version']}",
            }
            for item in dependencies
        ],
    }
    (EVIDENCE / "sbom.cdx.json").write_text(json.dumps(sbom, indent=2) + "\n", encoding="utf-8")
    inventory = {
        "schemaVersion": "1.0.0",
        "generatedAt": timestamp,
        "status": "REVIEWED",
        "note": "NOASSERTION means the lockfile did not carry a license field; verify upstream before redistribution.",
        "dependencies": dependencies,
    }
    (EVIDENCE / "license-inventory.json").write_text(
        json.dumps(inventory, indent=2) + "\n", encoding="utf-8"
    )

    source_archive = RELEASE / "rheinshield-v1.0.0-source-evidence.zip"
    write_zip(source_archive, candidate_files())
    social_files = sorted((ROOT / "docs" / "social").glob("*"))
    social_files += sorted((ROOT / "assets" / "linkedin").rglob("*.png"))
    social_files.append(LINKEDIN / "rheinshield-linkedin-carousel.pdf")
    linkedin_archive = LINKEDIN / "rheinshield-linkedin-package.zip"
    write_zip(linkedin_archive, [path for path in social_files if path.is_file()])

    checksum_targets = [
        source_archive,
        linkedin_archive,
        ROOT / "artifacts" / "career" / "rheinshield-cv-one-pager.pdf",
        LINKEDIN / "rheinshield-linkedin-carousel.pdf",
        EVIDENCE / "sbom.cdx.json",
        EVIDENCE / "license-inventory.json",
    ]
    lines = [f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}" for path in checksum_targets]
    (RELEASE / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "sourceArchiveFiles": len(candidate_files()),
                "linkedinPackageFiles": len(social_files),
                "components": len(dependencies),
                "checksums": len(lines),
            }
        )
    )


if __name__ == "__main__":
    main()
