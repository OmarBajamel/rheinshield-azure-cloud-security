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
GENERATED_EVIDENCE = {
    "artifacts/evidence/dist-scan.json",
    "artifacts/evidence/evidence-manifest.json",
    "artifacts/evidence/license-inventory.json",
    "artifacts/evidence/public-scan.json",
    "artifacts/evidence/sbom.cdx.json",
    "artifacts/evidence/security-scan-summary.json",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(*arguments: str) -> str:
    result = subprocess.run(  # noqa: S603 - fixed executable with internal arguments only
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def require_clean_source() -> tuple[str, str]:
    status = git("status", "--porcelain=v1", "--untracked-files=all")
    if status:
        raise SystemExit(
            "Release source must be a committed, clean revision. Commit or remove all changes "
            "before building generated release assets."
        )
    return git("rev-parse", "HEAD"), git("rev-parse", "HEAD^{tree}")


def candidate_files() -> list[Path]:
    tracked = git("ls-files")
    files = []
    for relative in tracked.splitlines():
        normalized = relative.replace("\\", "/")
        path = ROOT / relative
        if (
            path.is_file()
            and normalized not in GENERATED_EVIDENCE
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
    source_commit, source_tree = require_clean_source()
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
    source_files = candidate_files()
    write_zip(source_archive, source_files)
    social_files = sorted((ROOT / "docs" / "social").glob("*"))
    social_files += sorted((ROOT / "assets" / "linkedin").rglob("*.png"))
    social_files.append(LINKEDIN / "rheinshield-linkedin-carousel.pdf")
    linkedin_archive = LINKEDIN / "rheinshield-linkedin-package.zip"
    write_zip(linkedin_archive, [path for path in social_files if path.is_file()])

    provenance = {
        "schemaVersion": "1.0.0",
        "generatedAt": timestamp,
        "sourceCommit": source_commit,
        "sourceTree": source_tree,
        "sourceState": "CLEAN",
        "sourceArchiveFiles": len(source_files),
        "sourceArchiveSha256": sha256(source_archive),
        "mutableGeneratedEvidenceExcludedFromSourceArchive": sorted(GENERATED_EVIDENCE),
    }
    provenance_path = RELEASE / "build-provenance.json"
    provenance_path.write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")

    checksum_targets = [
        source_archive,
        linkedin_archive,
        ROOT / "artifacts" / "career" / "rheinshield-cv-one-pager.pdf",
        LINKEDIN / "rheinshield-linkedin-carousel.pdf",
        EVIDENCE / "sbom.cdx.json",
        EVIDENCE / "license-inventory.json",
        provenance_path,
    ]
    lines = [f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}" for path in checksum_targets]
    (RELEASE / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "sourceArchiveFiles": len(source_files),
                "linkedinPackageFiles": len(social_files),
                "components": len(dependencies),
                "checksums": len(lines),
            }
        )
    )


if __name__ == "__main__":
    main()
