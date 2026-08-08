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

    def test_portable_optional_fields_are_accepted(self) -> None:
        content = VALID_SKILL.replace(
            "description: Check widget packages",
            "license: Apache-2.0\ncompatibility: Requires Python 3.11 or later.\nmetadata:\n  version: \"1.0\"\ndescription: Check widget packages",
        )
        with tempfile.TemporaryDirectory() as temporary:
            issues = validate(self.write_skill(Path(temporary), "check-widget", content))
        self.assertEqual([], issues)

    def test_compatibility_length_is_an_error(self) -> None:
        content = VALID_SKILL.replace(
            "description: Check widget packages",
            f"compatibility: {'x' * 501}\ndescription: Check widget packages",
        )
        with tempfile.TemporaryDirectory() as temporary:
            issues = validate(self.write_skill(Path(temporary), "check-widget", content))
        self.assertIn("compatibility-length", {issue.code for issue in issues})

    def test_host_field_warns_only_for_portable_profile(self) -> None:
        content = VALID_SKILL.replace(
            "description: Check widget packages",
            "context: fork\ndescription: Check widget packages",
        )
        with tempfile.TemporaryDirectory() as temporary:
            path = self.write_skill(Path(temporary), "check-widget", content)
            portable = validate(path)
            claude = validate(path, profile="claude-code")
        self.assertIn("frontmatter-host-field", {issue.code for issue in portable})
        self.assertNotIn("frontmatter-host-field", {issue.code for issue in claude})

    def test_allowed_tools_requires_security_review(self) -> None:
        content = VALID_SKILL.replace(
            "description: Check widget packages",
            "allowed-tools: Bash(git status *)\ndescription: Check widget packages",
        )
        with tempfile.TemporaryDirectory() as temporary:
            issues = validate(self.write_skill(Path(temporary), "check-widget", content))
        codes = {issue.code for issue in issues}
        self.assertIn("allowed-tools-review", codes)
        self.assertNotIn("allowed-tools-broad", codes)

    def test_scoped_allowed_tools_list_is_not_reported_as_empty(self) -> None:
        content = VALID_SKILL.replace(
            "description: Check widget packages",
            "allowed-tools:\n  - Read\n  - Bash(git status *)\ndescription: Check widget packages",
        )
        with tempfile.TemporaryDirectory() as temporary:
            issues = validate(self.write_skill(Path(temporary), "check-widget", content))
        codes = {issue.code for issue in issues}
        self.assertIn("allowed-tools-review", codes)
        self.assertNotIn("allowed-tools-broad", codes)

    def test_dynamic_shell_injection_is_a_warning(self) -> None:
        content = VALID_SKILL + "\n## Current state\n\n!`git status --short`\n"
        with tempfile.TemporaryDirectory() as temporary:
            issues = validate(self.write_skill(Path(temporary), "check-widget", content))
        self.assertIn("dynamic-shell-injection", {issue.code for issue in issues})

    def test_link_outside_skill_is_a_warning(self) -> None:
        content = VALID_SKILL + "\nRead [shared guidance](../shared.md).\n"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "shared.md").write_text("# Shared\n", encoding="utf-8")
            issues = validate(self.write_skill(root, "check-widget", content))
        self.assertIn("link-outside-skill", {issue.code for issue in issues})


if __name__ == "__main__":
    unittest.main()
