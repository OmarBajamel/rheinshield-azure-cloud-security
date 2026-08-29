"""Remove only reproducible RheinShield local build products."""
import argparse
import os
import shutil
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STANDARD_TARGETS = [
    "dist",
    "node_modules",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "playwright-report",
    "test-results",
    ".tmp-pdf-render",
    "infra/lab/.terraform",
    "infra/enterprise-reference/.terraform",
    "infra/policies/.terraform",
    ".tools/tf-plugin-cache",
]
TOOL_TARGETS = [".tools/terraform", ".tools/tflint"]
ARCHIVE_TARGETS = [".tools/terraform/terraform.zip", ".tools/tflint/tflint.zip"]


def remove_readonly(function, path, _error):
    os.chmod(path, stat.S_IWRITE)
    function(path)


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--tools-only", action="store_true", help="remove downloaded Terraform/TFLint binaries only")
parser.add_argument("--archives-only", action="store_true", help="remove downloaded tool archives but retain extracted binaries")
args = parser.parse_args()

targets = ARCHIVE_TARGETS if args.archives_only else TOOL_TARGETS if args.tools_only else STANDARD_TARGETS + TOOL_TARGETS
for relative in targets:
    target = (ROOT / relative).resolve()
    if ROOT.resolve() not in target.parents:
        raise RuntimeError(f"Unsafe clean target: {target}")
    if target.exists():
        if target.is_dir():
            shutil.rmtree(target, onexc=remove_readonly)
        else:
            target.unlink()
        print(f"removed {target.relative_to(ROOT)}")
