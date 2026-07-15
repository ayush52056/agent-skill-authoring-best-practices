# Agent Skill Authoring Best Practices

An evidence-based, vendor-neutral guide for creating Agent Skills that trigger
reliably, use context efficiently, execute repeatable workflows, and produce
verifiable results.

This repository is deliberately narrow. It covers how to design, write,
evaluate, secure, and maintain skills. It is not a marketplace or a collection
of unrelated skills.

## Start here

1. Read the [authoring standard](docs/authoring-standard.md).
2. Choose an invocation policy using [invocation and portfolios](docs/invocation-and-portfolios.md).
3. Copy the [portable SKILL.md template](templates/SKILL.md).
4. Score the draft with the [quality rubric](docs/quality-rubric.md).
5. Run the [trigger](templates/trigger-evals.json) and [task](templates/task-eval.json) evaluations.
6. Apply the controls in [security and governance](docs/security-and-governance.md).
7. Validate the package:

   ```text
   python scripts/validate_skill.py path/to/skill
   ```

See [examples/diagnose-test-failures](examples/diagnose-test-failures/SKILL.md)
for a compact worked example.

## The short version

A strong skill:

- fixes a recurring, observed agent failure or packages genuinely specialized knowledge;
- has a narrow description that says what it does and when it should trigger;
- front-loads distinctive routing terms and chooses automatic versus explicit invocation deliberately;
- describes an actionable process instead of an essay or persona;
- assigns strictness in proportion to operational risk;
- keeps `SKILL.md` lean and loads references only when a branch needs them;
- uses scripts for deterministic, repeated, or fragile operations;
- requires observable evidence before reporting completion;
- is compared with a no-skill baseline on positive, negative, and boundary prompts;
- survives repeated held-out trials with neighboring skills and the real production catalog;
- is reviewed and governed like an executable software dependency;
- is re-tested after model, host, tool, or policy changes and retired when it stops adding value;
- improves from real failure traces instead of accumulating speculative rules.

## Repository map

```text
docs/
  authoring-standard.md       Canonical design and writing standard
  quality-rubric.md           Scored review rubric and hard gates
  evaluation.md               Trigger and task evaluation method
  invocation-and-portfolios.md Invocation policy and catalog design
  security-and-governance.md  Supply-chain and lifecycle controls
  evidence-map.md             Recommendation-to-source traceability
examples/
  diagnose-test-failures/     Worked example with progressive disclosure
templates/
  SKILL.md                    Portable starter template
  trigger-evals.json          Trigger-suite starter fixture
  task-eval.json              Baseline and task-evaluation fixture
scripts/
  validate_skill.py           Lightweight structural validator
tests/
  test_validate_skill.py      Validator tests
SOURCES.md                    Primary sources and practitioner references
CONTRIBUTING.md               Evidence requirements for changes
```

## Scope and portability

The portable baseline follows the open Agent Skills convention: a skill is a
directory containing `SKILL.md` with `name` and `description` frontmatter, plus
optional `scripts/`, `references/`, and `assets/` resources. Host-specific
metadata can be added when required, but should not replace the portable core.

## Project standard

Popularity is not treated as proof. Guidance belongs here when it is supported
by an official specification, a credible production implementation, empirical
evidence, or a reproducible evaluation. Conflicting recommendations are labeled
as tradeoffs rather than presented as universal rules.

The [evidence map](docs/evidence-map.md) records the level, source, and
qualification for consequential recommendations. It is the fastest way to
audit whether a rule is a format requirement, official guidance, an empirical
finding, or a practitioner pattern that still needs local proof.

## License

Licensed under the [Apache License 2.0](LICENSE).
