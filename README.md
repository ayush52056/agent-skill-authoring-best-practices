# Agent Skill Authoring Best Practices

An evidence-based guide to creating Agent Skills that are easy to trigger,
efficient to run, safe to share, and simple to test.

This repository focuses only on skill authoring. It explains how to design,
write, evaluate, secure, and maintain skills. It is not a skill marketplace.

## Start here

1. Read the [authoring standard](docs/authoring-standard.md).
2. Choose an invocation policy using [invocation and portfolios](docs/invocation-and-portfolios.md).
3. Copy the [portable SKILL.md template](templates/SKILL.md).
4. Score the draft with the [quality rubric](docs/quality-rubric.md).
5. Run the [trigger](templates/trigger-evals.json) and [task](templates/task-eval.json) evaluations.
6. Apply the controls in [security and governance](docs/security-and-governance.md).
7. Review [how public sources became examples](docs/source-reviews.md).
8. Validate the package:

   ```text
   python scripts/validate_skill.py path/to/skill
   ```

See [examples/diagnose-test-failures](examples/diagnose-test-failures/SKILL.md)
for a compact worked example.

## The short version

A strong skill:

- Solve a recurring agent problem or provide knowledge the agent does not already have.
- Explain clearly what it does and when it should run.
- Put the most useful trigger words near the start of the description.
- Choose automatic or user-requested invocation based on risk.
- Give the agent a practical workflow instead of a long essay or persona.
- Use strict instructions only when the task needs them.
- Keep `SKILL.md` focused and load extra references only when needed.
- Use scripts for repeatable or fragile operations.
- Require proof before the agent reports completion.
- Compare results with and without the skill.
- Test nearby prompts, competing skills, and the real skill catalog.
- Review the skill like a software dependency.
- Re-test it after model, host, tool, or policy changes.
- Remove it when it no longer improves results.

## Repository map

```text
docs/
  authoring-standard.md        Canonical design and writing standard
  quality-rubric.md            Scored review rubric and hard gates
  evaluation.md                Trigger and task evaluation method
  invocation-and-portfolios.md Invocation policy and catalog design
  security-and-governance.md   Supply-chain and lifecycle controls
  evidence-map.md              Recommendation-to-source traceability
  source-reviews.md            Source patterns and how they were applied
examples/
  diagnose-test-failures/      Worked example with progressive disclosure
templates/
  SKILL.md                     Portable starter template
  trigger-evals.json           Trigger-suite starter fixture
  task-eval.json               Baseline and task-evaluation fixture
scripts/
  validate_skill.py            Lightweight structural validator
tests/
  test_validate_skill.py       Validator tests
SOURCES.md                     Primary sources and practitioner references
CONTRIBUTING.md                Evidence requirements for changes
```

## Scope and portability

The portable baseline follows the open Agent Skills convention: a skill is a
directory containing `SKILL.md` with `name` and `description` frontmatter, plus
optional `scripts/`, `references/`, and `assets/` resources. Host-specific
metadata can be added when required, but should not replace the portable core.

## Project standard

Popularity is not proof. A recommendation belongs here only when it has support
from an official specification, a trusted production implementation, published
research, or a repeatable evaluation. When sources disagree, the repository
explains the tradeoff instead of pretending that one rule fits every skill.

The [evidence map](docs/evidence-map.md) records the source, evidence level, and
limits for important recommendations. Use it to see whether a rule comes from a
format requirement, official guidance, published research, or practitioner
experience that still needs local testing.

## License

Licensed under the [Apache License 2.0](LICENSE).
