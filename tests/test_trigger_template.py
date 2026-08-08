from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "trigger-evals.json"
sys.path.insert(0, str(ROOT / "scripts"))

from validate_evaluation import validate_file  # noqa: E402


class TriggerTemplateTests(unittest.TestCase):
    def test_template_parses_and_passes_validation(self) -> None:
        json.loads(TEMPLATE.read_text(encoding="utf-8"))
        self.assertEqual([], validate_file(TEMPLATE))

    def test_template_is_an_unexecuted_definition(self) -> None:
        data = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        self.assertEqual("definition-only", data["status"])
        self.assertIn(data["invocation_mode"], {"implicit", "explicit"})
        self.assertTrue(data["host"])
        self.assertTrue(data["model"])
        self.assertTrue(data["cases"])
        for case in data["cases"]:
            self.assertEqual([], case["observed_trials"])
            self.assertIsNone(case["trigger_rate"])

    def test_unknown_invocation_mode_is_rejected(self) -> None:
        data = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        data["invocation_mode"] = "both"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trigger-evals.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            codes = {issue.code for issue in validate_file(path)}
        self.assertIn("invocation-mode", codes)


if __name__ == "__main__":
    unittest.main()
