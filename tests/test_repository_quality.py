from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`]*`")


class RepositoryQualityTests(unittest.TestCase):
    def markdown_files(self) -> list[Path]:
        return sorted(path for path in ROOT.rglob("*.md") if ".git" not in path.parts)

    def test_local_markdown_links_exist(self) -> None:
        missing: list[str] = []
        for path in self.markdown_files():
            text = path.read_text(encoding="utf-8")
            for raw_target in LINK_RE.findall(text):
                target = raw_target.strip().strip("<>").split("#", 1)[0]
                if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                    continue
                if not (path.parent / target).exists():
                    missing.append(f"{path.relative_to(ROOT)} -> {target}")
        self.assertEqual([], missing)

    def test_prose_avoids_project_style_violations(self) -> None:
        violations: list[str] = []
        for path in self.markdown_files():
            text = path.read_text(encoding="utf-8")
            prose = INLINE_CODE_RE.sub("", FENCED_CODE_RE.sub("", text))
            for character, label in ((";", "semicolon"), ("—", "em dash")):
                if character in prose:
                    violations.append(f"{path.relative_to(ROOT)} contains {label} in prose")
            if "�" in text or "â€" in text:
                violations.append(f"{path.relative_to(ROOT)} contains replacement or mojibake text")
        self.assertEqual([], violations)


if __name__ == "__main__":
    unittest.main()
