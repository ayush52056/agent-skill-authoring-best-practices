#!/usr/bin/env python3
"""Validate Agent Skill evaluation definitions and result artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    message: str


def _required(mapping: dict[str, Any], fields: tuple[str, ...], label: str) -> list[Issue]:
    return [
        Issue("error", "field-missing", f"{label} requires '{field}'.")
        for field in fields
        if field not in mapping
    ]


def _validate_trigger(data: dict[str, Any]) -> list[Issue]:
    issues = _required(
        data,
        ("skill", "status", "host", "model", "invocation_mode", "trials_per_case", "cases"),
        "Trigger suite",
    )
    if data.get("invocation_mode") not in {"implicit", "explicit"}:
        issues.append(
            Issue(
                "error",
                "invocation-mode",
                "Trigger suite invocation_mode must be 'implicit' or 'explicit'.",
            )
        )
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        return issues + [Issue("error", "cases", "Trigger suite requires a non-empty cases list.")]
    seen: set[str] = set()
    for index, case in enumerate(cases):
        label = f"Trigger case {index}"
        if not isinstance(case, dict):
            issues.append(Issue("error", "case-type", f"{label} must be an object."))
            continue
        issues.extend(_required(case, ("id", "group", "split", "prompt", "should_trigger", "observed_trials", "trigger_rate"), label))
        case_id = case.get("id")
        if case_id in seen:
            issues.append(Issue("error", "case-id", f"Duplicate trigger case id: {case_id}"))
        elif isinstance(case_id, str):
            seen.add(case_id)
        if case.get("group") not in {"positive", "negative", "boundary"}:
            issues.append(Issue("error", "case-group", f"{label} has an unsupported group."))
        if case.get("split") not in {"train", "validation", "final", "held-out"}:
            issues.append(Issue("error", "case-split", f"{label} has an unsupported split."))
        observations = case.get("observed_trials")
        if not isinstance(observations, list):
            issues.append(Issue("error", "observations", f"{label} observed_trials must be a list."))
        elif not observations and case.get("trigger_rate") is not None:
            issues.append(Issue("error", "trigger-rate", f"{label} cannot report a trigger rate without observations."))
    return issues


def _validate_task(data: dict[str, Any], path: Path) -> list[Issue]:
    issues = _required(data, ("skill", "status", "cases"), "Task suite")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        return issues + [Issue("error", "cases", "Task suite requires a non-empty cases list.")]
    for index, case in enumerate(cases):
        label = f"Task case {index}"
        if not isinstance(case, dict):
            issues.append(Issue("error", "case-type", f"{label} must be an object."))
            continue
        issues.extend(_required(case, ("id", "prompt", "verifier", "configurations", "trials_per_configuration"), label))
        configurations = case.get("configurations", [])
        labels = {item.get("label") for item in configurations if isinstance(item, dict)}
        if not {"baseline", "candidate"}.issubset(labels):
            issues.append(Issue("error", "paired-configurations", f"{label} requires baseline and candidate configurations."))
        if not isinstance(case.get("trials_per_configuration"), int) or case.get("trials_per_configuration", 0) < 1:
            issues.append(Issue("error", "trial-count", f"{label} requires at least one planned trial."))
        fixture = case.get("fixture")
        if isinstance(fixture, str) and "replace-with" not in fixture and not (path.parent / fixture).exists():
            issues.append(Issue("error", "fixture-missing", f"{label} fixture does not exist: {fixture}"))
    return issues


def _validate_grading(data: dict[str, Any]) -> list[Issue]:
    issues = _required(data, ("status", "expectations", "overall_passed"), "Grading result")
    expectations = data.get("expectations")
    if not isinstance(expectations, list) or not expectations:
        return issues + [Issue("error", "expectations", "Grading result requires expectations.")]
    completed = data.get("status") == "completed"
    for index, expectation in enumerate(expectations):
        if not isinstance(expectation, dict):
            issues.append(Issue("error", "expectation-type", f"Expectation {index} must be an object."))
            continue
        issues.extend(_required(expectation, ("text", "passed", "evidence"), f"Expectation {index}"))
        if completed and (not isinstance(expectation.get("passed"), bool) or not expectation.get("evidence")):
            issues.append(Issue("error", "grading-evidence", f"Completed expectation {index} requires a boolean result and evidence."))
    return issues


def _validate_benchmark(data: dict[str, Any]) -> list[Issue]:
    issues = _required(data, ("skill", "status", "configurations", "deltas"), "Benchmark")
    configurations = data.get("configurations")
    if not isinstance(configurations, list):
        return issues + [Issue("error", "configurations", "Benchmark configurations must be a list.")]
    if data.get("status") == "not-run":
        for item in configurations:
            if isinstance(item, dict) and item.get("run_count") != 0:
                issues.append(Issue("error", "unexecuted-runs", "A not-run benchmark cannot report completed runs."))
    elif data.get("status") == "completed":
        if not configurations or any(not isinstance(item, dict) or item.get("run_count", 0) < 1 for item in configurations):
            issues.append(Issue("error", "completed-runs", "A completed benchmark requires recorded runs for every configuration."))
    return issues


def validate_file(path: Path) -> list[Issue]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return [Issue("error", "encoding", f"Evaluation file must be valid UTF-8: {path}")]
    except json.JSONDecodeError as error:
        return [Issue("error", "json", f"Invalid JSON in {path}: {error}")]
    if not isinstance(data, dict):
        return [Issue("error", "root-type", f"Evaluation root must be an object: {path}")]
    if "cases" in data and any(isinstance(case, dict) and "should_trigger" in case for case in data.get("cases", [])):
        return _validate_trigger(data)
    if "cases" in data:
        return _validate_task(data, path)
    if "expectations" in data:
        return _validate_grading(data)
    if "configurations" in data and "deltas" in data:
        return _validate_benchmark(data)
    if path.name in {"timing.json", "feedback.json"}:
        return _required(data, ("status",), path.name)
    return [Issue("warning", "unknown-artifact", f"No evaluation schema recognized for {path}.")]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="JSON files or directories containing evaluation JSON")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args(argv)

    files: list[Path] = []
    for path in args.paths:
        files.extend(sorted(path.rglob("*.json")) if path.is_dir() else [path])
    issues: list[Issue] = []
    for path in files:
        for issue in validate_file(path):
            issues.append(issue)
            print(f"{issue.severity.upper():7} {issue.code} {path}: {issue.message}")
    errors = sum(issue.severity == "error" for issue in issues)
    warnings = sum(issue.severity == "warning" for issue in issues)
    print(f"Result: {len(files)} file(s), {errors} error(s), {warnings} warning(s)")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
