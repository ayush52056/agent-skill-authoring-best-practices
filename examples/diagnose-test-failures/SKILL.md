---
name: diagnose-test-failures
description: Diagnose failing or flaky automated tests by reproducing the failure, isolating the first causal error, and verifying the smallest corrective change. Use when tests fail locally or in CI, a user asks why a test suite is failing, or intermittent test behavior needs root-cause analysis.
---

# Diagnose test failures

## Workflow

1. Read repository instructions and identify the narrowest command that reproduces the reported failure.
2. Run that command without modifying code. Preserve the command, exit status, and first causal error rather than the final cascade of failures.
3. Classify the failure as environment, dependency, product-code, test-code, or intermittent behavior.
4. If the classification is unclear, reduce the test scope or add temporary observation without changing production behavior.
5. Explain the root cause with evidence that connects the failing assertion or exception to the responsible code path.
6. If the user requested a fix, make the smallest complete correction and avoid unrelated cleanup.
7. Re-run the original reproduction and the narrowest relevant surrounding suite.
8. Report the cause, changed files, commands run, outcomes, and any remaining uncertainty.

## Branches

- For intermittent failures, reproduce repeatedly and inspect shared state, order dependence, clocks, randomness, concurrency, and external services.
- For CI-only failures, compare runtime, operating system, environment, dependency resolution, permissions, paths, and service availability before changing application logic.
- For a large failure cascade, diagnose the earliest causal failure before addressing downstream symptoms.
- Read [references/failure-patterns.md](references/failure-patterns.md) only when initial evidence does not identify the failure class.

## Validation

- Require the original failing command to pass after a fix.
- Run relevant neighboring tests to detect overfitting.
- Confirm that a flaky test passes across repeated runs or report that reproducibility remains unproven.
- Never report a test failure as fixed when the failing test was skipped, weakened, or removed without an explicit requirement.
