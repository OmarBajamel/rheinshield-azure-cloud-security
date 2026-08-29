import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import render_arm  # noqa: E402
import validate  # noqa: E402


class SentinelContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = validate.validate_all()

    def test_all_fourteen_detection_fixtures_pass(self) -> None:
        self.assertEqual(self.result["summary"]["analytics_rules"], 14)
        self.assertEqual(self.result["summary"]["rule_fixture_tests_passed"], 14)
        self.assertEqual(self.result["summary"]["false_positives"], 0)
        self.assertEqual(self.result["summary"]["false_negatives"], 0)

    def test_required_content_counts(self) -> None:
        summary = self.result["summary"]
        self.assertGreaterEqual(summary["hunting_queries"], 5)
        self.assertEqual(summary["workbooks"], 3)
        self.assertEqual(summary["automation_rules"], 3)
        self.assertEqual(summary["playbooks"], 3)
        self.assertEqual(summary["watchlists"], 1)

    def test_hunts_are_structural_only_without_live_sentinel(self) -> None:
        for path in (validate.SENTINEL / "hunting-queries").glob("*.yaml"):
            self.assertEqual(validate._load_yaml(path)["status"], "READY_NOT_AUTHENTICATED")

    def test_result_is_honest_about_validation_scope(self) -> None:
        self.assertEqual(self.result["status"], "FIXTURE_VALIDATED")
        self.assertFalse(self.result["live_validation"])
        self.assertFalse(self.result["production_efficacy_claim"])

    def test_arm_renderer_preserves_safe_rule_contract(self) -> None:
        template = render_arm.render()
        self.assertEqual(len(template["resources"]), 14)
        self.assertTrue(all(resource["apiVersion"] == "2025-09-01" for resource in template["resources"]))
        self.assertTrue(all(resource["properties"]["enabled"] is False for resource in template["resources"]))
        self.assertEqual(len({resource["name"] for resource in template["resources"]}), 14)


if __name__ == "__main__":
    unittest.main()
