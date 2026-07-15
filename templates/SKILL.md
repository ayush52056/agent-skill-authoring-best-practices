---
name: replace-with-verb-led-name
description: Perform the distinctive action on the relevant artifact and produce the concrete result. Use when users request the specific situations that should activate this skill, including realistic trigger wording.
---

# Skill title

## Inputs

- Identify the information and artifacts required to begin.
- Discover safe defaults when possible. Ask only for choices that materially change the result.
- Stop and report the missing requirement when proceeding would be unsafe.

## Outputs

- Name the files, decisions, reports, or external state this skill produces.
- State the format when it is part of correctness.
- Define what the skill deliberately does not produce or own.

## Workflow

1. Inspect the task, relevant local instructions, and current state.
2. Select the appropriate branch using explicit decision criteria.
3. Perform the smallest complete unit of work.
4. Validate that unit before continuing.
5. Repeat until the requested outcome is complete.

Use this ordered form only when sequence or checkpoints matter. For adaptable
work, replace it with a preferred outcome, constraints, decision criteria, and
validation. Keep one default path. Add only branches that change the result.

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

- Link and read the relevant file under `references/` only when its workflow branch needs it.
- Link and run the deterministic operation under `scripts/`. Declare its runtime dependencies and expected output.
- Reuse files in `assets/` when producing the associated output.

Delete resource entries and sections that the skill does not need. Keep detailed
schemas, catalogs, extended examples, and variant-specific instructions out of
this file and link them directly from here. Use forward-slash relative paths and
say whether each script should be executed or merely inspected.
