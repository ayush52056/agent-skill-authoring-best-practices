# Contributing

Keep this repository focused on evidence-backed skill-authoring practice.

## A change should include

- the concrete failure, risk, or compatibility requirement it addresses.
- the evidence supporting the recommendation.
- any tradeoff or host-specific limitation.
- an update to the relevant template, rubric, or evaluation when behavior changes.
- a source in `SOURCES.md` when the claim depends on external guidance.
- an evidence-level entry or updated qualification in `docs/evidence-map.md` for
  a consequential recommendation.
- a source-review entry that shows the useful example, our adoption, and its
  limit when a new source is added.

## Review rules

- Preserve one authoritative statement for each rule. Link instead of duplicating.
- Prefer concise instructions and examples over conceptual essays.
- Do not add a convention solely because a popular repository uses it.
- Separate portable requirements from optional host metadata.
- Add regression prompts or tests for corrected failures.
- Keep trigger and task fixtures machine-readable. Mark cases held out before tuning.
- Test portfolio collisions when a description or invocation policy changes.
- Separate measured findings from practitioner heuristics and report study scope.
- Mark direct excerpts clearly and keep them short. Prefer a paraphrase and a
  rewritten repository example when the exact wording is not necessary.
- Explain why an example demonstrates the rule. Do not add examples that only
  repeat the surrounding text.
- Remove superseded guidance in the same change.
- Review scripts and links as carefully as prose.

Run before submitting:

```text
python -m unittest discover -s tests -v
python scripts/validate_skill.py examples/diagnose-test-failures
```
