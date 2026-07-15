from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_skill import validate  # noqa: E402


VALID_SKILL = """---
name: check-widget
description: Check widget packages for structural errors. Use when a user asks to validate or inspect a widget package.
---

# Check widgets

## Workflow

1. Inspect the widget.
2. Report structural errors.

## Validation

- Confirm that every required file exists.
"""


class ValidateSkillTests(unittest.TestCase):
    def write_skill(self, root: Path, name: str, content: str) -> Path:
        directory = root / name
        directory.mkdir()
        (directory / "SKILL.md").write_text(content, encoding="utf-8")
        return directory

    def test_valid_skill_has_no_issues(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            issues = validate(self.write_skill(Path(temporary), "check-widget", VALID_SKILL))
        self.assertEqual([], issues)

    def test_missing_frontmatter_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = self.write_skill(Path(temporary), "check-widget", "# No metadata\n")
            issues = validate(path)
        self.assertIn("frontmatter-missing", {issue.code for issue in issues})
        self.assertIn("name-missing", {issue.code for issue in issues})

    def test_invalid_name_and_directory_are_errors(self) -> None:
        content = VALID_SKILL.replace("name: check-widget", "name: Check_Widget")
        with tempfile.TemporaryDirectory() as temporary:
            issues = validate(self.write_skill(Path(temporary), "check-widget", content))
        codes = {issue.code for issue in issues}
        self.assertIn("name-format", codes)
        self.assertIn("directory-name", codes)

    def test_missing_local_link_is_an_error(self) -> None:
        content = VALID_SKILL + "\nRead [details](references/details.md).\n"
        with tempfile.TemporaryDirectory() as temporary:
            issues = validate(self.write_skill(Path(temporary), "check-widget", content))
        self.assertIn("broken-link", {issue.code for issue in issues})

    def test_unlinked_reference_is_a_warning(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = self.write_skill(Path(temporary), "check-widget", VALID_SKILL)
            references = path / "references"
            references.mkdir()
            (references / "details.md").write_text("# Details\n", encoding="utf-8")
            issues = validate(path)
        warning = next(issue for issue in issues if issue.code == "unlinked-reference")
        self.assertEqual("warning", warning.severity)

    def test_xml_tag_in_description_is_an_error(self) -> None:
        content = VALID_SKILL.replace("Check widget packages", "Check <widget> packages")
        with tempfile.TemporaryDirectory() as temporary:
            issues = validate(self.write_skill(Path(temporary), "check-widget", content))
        self.assertIn("description-xml", {issue.code for issue in issues})

    def test_vague_name_is_a_warning(self) -> None:
        content = VALID_SKILL.replace("name: check-widget", "name: tools")
        with tempfile.TemporaryDirectory() as temporary:
            issues = validate(self.write_skill(Path(temporary), "tools", content))
        self.assertIn("name-vague", {issue.code for issue in issues})

    def test_backslash_link_is_a_warning(self) -> None:
        content = VALID_SKILL + "\nRead [details](references\\details.md).\n"
        with tempfile.TemporaryDirectory() as temporary:
            issues = validate(self.write_skill(Path(temporary), "check-widget", content))
        self.assertIn("link-separator", {issue.code for issue in issues})


if __name__ == "__main__":
    unittest.main()
