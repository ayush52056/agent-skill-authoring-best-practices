#!/usr/bin/env python3
"""Validate the portable structure and common quality signals of an Agent Skill."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
XML_TAG_RE = re.compile(r"<[^>]+>")
VAGUE_NAMES = {"helper", "helpers", "misc", "skill", "tools", "utilities", "utils"}


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    message: str


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, list[Issue]]:
    """Parse the top-level scalar subset needed for portable skill metadata."""
    lines = text.splitlines()
    issues: list[Issue] = []
    if not lines or lines[0].strip() != "---":
        return {}, text, [Issue("error", "frontmatter-missing", "SKILL.md must start with YAML frontmatter delimited by ---.")]

    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, "", [Issue("error", "frontmatter-unclosed", "YAML frontmatter has no closing --- delimiter.")]

    data: dict[str, str] = {}
    block_key: str | None = None
    block_parts: list[str] = []

    def finish_block() -> None:
        nonlocal block_key, block_parts
        if block_key is not None:
            data[block_key] = " ".join(part for part in block_parts if part).strip()
        block_key = None
        block_parts = []

    for number, raw in enumerate(lines[1:end], start=2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[:1].isspace():
            if block_key is not None:
                block_parts.append(raw.strip())
            continue
        finish_block()
        if ":" not in raw:
            issues.append(Issue("error", "frontmatter-syntax", f"Frontmatter line {number} is not a key-value pair."))
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            issues.append(Issue("error", "frontmatter-key", f"Frontmatter line {number} has an empty key."))
        elif key in data:
            issues.append(Issue("error", "frontmatter-duplicate", f"Frontmatter key '{key}' is duplicated."))
        elif value in {">", "|", ">-", "|-"}:
            block_key = key
        else:
            data[key] = _unquote(value)
    finish_block()

    body = "\n".join(lines[end + 1 :]).strip()
    return data, body, issues


def _check_links(skill_file: Path, body: str) -> list[Issue]:
    issues: list[Issue] = []
    linked_paths: set[Path] = set()
    for target in LINK_RE.findall(body):
        target = target.strip().split("#", 1)[0]
        if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            continue
        if "\\" in target:
            issues.append(Issue("warning", "link-separator", f"Use forward slashes in portable local links: {target}"))
        path = (skill_file.parent / target).resolve()
        linked_paths.add(path)
        if not path.exists():
            issues.append(Issue("error", "broken-link", f"Linked local resource does not exist: {target}"))

    references = skill_file.parent / "references"
    if references.is_dir():
        for path in references.rglob("*"):
            if path.is_file() and path.resolve() not in linked_paths:
                relative = path.relative_to(skill_file.parent)
                issues.append(Issue("warning", "unlinked-reference", f"Reference is not linked directly from SKILL.md: {relative}"))
    return issues


def validate(path: Path) -> list[Issue]:
    skill_file = path / "SKILL.md" if path.is_dir() else path
    if not skill_file.is_file():
        return [Issue("error", "skill-file-missing", f"SKILL.md not found at {skill_file}")]

    try:
        text = skill_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [Issue("error", "encoding", "SKILL.md must be valid UTF-8.")]

    metadata, body, issues = parse_frontmatter(text)
    name = metadata.get("name", "").strip()
    description = metadata.get("description", "").strip()

    if not name:
        issues.append(Issue("error", "name-missing", "Frontmatter requires a non-empty name."))
    else:
        if len(name) > 64:
            issues.append(Issue("error", "name-length", "Name must be 64 characters or fewer."))
        if not NAME_RE.fullmatch(name):
            issues.append(Issue("error", "name-format", "Name must contain lowercase letters, digits, and single hyphens only."))
        if XML_TAG_RE.search(name):
            issues.append(Issue("error", "name-xml", "Name must not contain XML tags."))
        if name in VAGUE_NAMES:
            issues.append(Issue("warning", "name-vague", "Name is too generic to distinguish this skill in a catalog."))
        if skill_file.parent.name != name:
            issues.append(Issue("error", "directory-name", f"Skill directory '{skill_file.parent.name}' must match name '{name}'."))

    if not description:
        issues.append(Issue("error", "description-missing", "Frontmatter requires a non-empty description."))
    else:
        if len(description) > 1024:
            issues.append(Issue("error", "description-length", "Description must be 1,024 characters or fewer."))
        if len(description) < 40:
            issues.append(Issue("warning", "description-thin", "Description may be too short to communicate capability and triggers."))
        if "use when" not in description.lower():
            issues.append(Issue("warning", "trigger-missing", "Description should state concrete 'Use when' trigger conditions."))
        if XML_TAG_RE.search(description):
            issues.append(Issue("error", "description-xml", "Description must not contain XML tags."))

    if not body:
        issues.append(Issue("error", "body-missing", "SKILL.md requires an instruction body."))
    else:
        line_count = len(text.splitlines())
        word_count = len(re.findall(r"\S+", body))
        if line_count > 500:
            issues.append(Issue("warning", "body-lines", f"SKILL.md has {line_count} lines; use progressive disclosure below 500 lines."))
        if word_count > 5000:
            issues.append(Issue("warning", "body-words", f"SKILL.md has {word_count} body words; move details to references."))
        headings = {match.group(1).strip().lower() for match in re.finditer(r"^#{1,6}\s+(.+)$", body, re.MULTILINE)}
        if not any("workflow" in heading or "process" in heading for heading in headings):
            issues.append(Issue("warning", "workflow-section", "Consider an explicit Workflow or Process section."))
        if not any("validation" in heading or "verification" in heading for heading in headings):
            issues.append(Issue("warning", "validation-section", "Consider an explicit Validation or Verification section."))
        issues.extend(_check_links(skill_file, body))

    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Skill directory or SKILL.md path")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args(argv)

    issues = validate(args.path)
    for issue in issues:
        print(f"{issue.severity.upper():7} {issue.code}: {issue.message}")

    errors = sum(issue.severity == "error" for issue in issues)
    warnings = sum(issue.severity == "warning" for issue in issues)
    print(f"Result: {errors} error(s), {warnings} warning(s)")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
