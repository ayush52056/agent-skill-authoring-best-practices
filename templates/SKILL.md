---
name: replace-with-verb-led-name
description: Perform the distinctive action on the relevant artifact and produce the concrete result. Use when users request the specific situations that should activate this skill, including realistic trigger wording.
---

# Skill title

## Workflow

1. Inspect the task, relevant local instructions, and current state.
2. Select the appropriate branch using explicit decision criteria.
3. Perform the smallest complete unit of work.
4. Validate that unit before continuing.
5. Repeat until the requested outcome is complete.

Use this ordered form only when sequence or checkpoints matter. For adaptable
work, replace it with a preferred outcome, constraints, decision criteria, and
validation. Keep one default path. Add only branches that change the result.
End every stage with a checkable completion criterion. When the stage promises
coverage, make the criterion exhaustive enough to reveal omissions.

## Validation

- Run the checks that directly prove the requested outcome.
- Inspect generated or modified artifacts when command success is insufficient.
- Report unresolved failures and checks that could not run.
- Do not claim completion without the required evidence.

## Safety and failure handling

- Preserve unrelated user changes and data.
- Preview consequential external or destructive actions and obtain required approval.
- Fail closed when permissions, inputs, or validation are insufficient.
- Do not weaken checks merely to produce a passing result.

## Resources

- Link each reference directly, name what it contains, and state the exact
  workflow branch that should load it.
- Link and run the deterministic operation under `scripts/`. Declare its runtime dependencies and expected output.
- Reuse files in `assets/` when producing the associated output.

Delete this section when the skill does not need bundled resources.
