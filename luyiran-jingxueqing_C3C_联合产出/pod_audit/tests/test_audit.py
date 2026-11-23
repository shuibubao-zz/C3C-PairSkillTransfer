#!/usr/bin/env python3
"""验证规则确实抓得住 P27 材料中记录过的真实错误。"""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from audit import audit, load_json  # noqa: E402


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.rules = load_json(ROOT / "rules.json")
        self.before = load_json(ROOT / "sample_before.json")
        self.after = load_json(ROOT / "sample_after.json")

    def test_before_dataset_is_caught(self):
        report = audit(self.before, self.rules)
        self.assertFalse(report["pass"])
        rules_hit = {f["rule"] for f in report["findings"]}
        for expected in ["terminal_id.pattern", "credential_ref.forbidden",
                         "pod_status.allowed", "required_scenarios",
                         "login_step.required"]:
            self.assertIn(expected, rules_hit)
        self.assertGreaterEqual(report["finding_count"], 5)

    def test_after_dataset_is_clean(self):
        report = audit(self.after, self.rules)
        self.assertTrue(report["pass"])
        self.assertEqual(report["finding_count"], 0)

    def test_terminal_rule_accepts_correct_binding(self):
        data = {"drivers": [{"terminal": "PDA-SY-0001",
                             "credential_ref": "map://driver/D-SY-001"}]}
        report = audit(data, self.rules)
        self.assertTrue(all(f["rule"] != "terminal_id.pattern"
                            for f in report["findings"]))

    def test_legacy_credential_is_forbidden(self):
        data = {"drivers": [{"terminal": "PDA-SY-0001",
                             "credential_ref": "legacy-123456"}]}
        findings = audit(data, self.rules)["findings"]
        self.assertTrue(any(f["rule"] == "credential_ref.forbidden"
                            for f in findings))

    def test_login_step_required(self):
        data = {"test_cases": [{"id": "TC-X", "login_step": False}]}
        findings = audit(data, self.rules)["findings"]
        self.assertTrue(any(f["rule"] == "login_step.required"
                            for f in findings))

    def test_all_required_scenarios(self):
        data = {"scenarios": self.rules["required_scenarios"]}
        findings = audit(data, self.rules)["findings"]
        self.assertFalse(any(f["rule"] == "required_scenarios"
                             for f in findings))


if __name__ == "__main__":
    unittest.main(verbosity=2)
