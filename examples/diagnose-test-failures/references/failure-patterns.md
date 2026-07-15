# Failure-pattern reference

Use these patterns as hypotheses, not conclusions. Confirm each against logs,
code, and a reproduction.

## Environment

- different operating system, architecture, locale, timezone, encoding, or path separator.
- missing service, executable, environment variable, permission, or fixture.
- resource exhaustion or incompatible runtime version.

## Dependencies

- stale lockfile or cache.
- unpinned transitive version.
- generated artifact inconsistent with source.
- service or API behavior changed outside the repository.

## Product code

- regression at the first failing boundary.
- state leaking between requests or tests.
- asynchronous work not awaited.
- error swallowed and surfaced later as a secondary symptom.

## Test code

- assertion coupled to implementation rather than public behavior.
- fixture no longer represents a valid state.
- global state, test-order dependency, fixed port, or shared filesystem path.
- tautological mock that verifies its own setup instead of system behavior.

## Intermittent behavior

- unseeded randomness.
- real clock or timing threshold.
- race condition or eventual consistency.
- network dependency.
- unordered collection assumed to be stable.
