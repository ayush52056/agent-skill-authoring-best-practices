# Agent Skill Authoring Standard

This is the normative handbook. The [evidence map](evidence-map.md) identifies
the source and confidence level behind consequential recommendations. Portable
format rules and host-specific behavior are intentionally separated.

## 1. Choose the right abstraction

Create a skill when at least one of these is true:

- agents repeatedly fail at a recognizable task;
- the workflow contains non-obvious ordering, branching, or recovery behavior;
- the task requires organization-, product-, or domain-specific knowledge;
- deterministic scripts, templates, or references should travel with the workflow;
- the capability should load only when relevant rather than remain in every prompt.

Do not create a skill merely to restate general model knowledge, establish a
persona, collect miscellaneous tips, or enforce a rule that a linter, test,
schema, permission boundary, or hook can enforce mechanically.

| Need | Preferred mechanism |
|---|---|
| Small convention relevant to almost every task | Repository instruction file |
| Conditional workflow or specialized knowledge | Skill |
| Current external facts or remote actions | Tool or MCP server |
| Deterministic repeated transformation | Script |
| Invariant that must never depend on model compliance | Test, linter, policy, or hook |
| Large independent task needing isolated context | Subagent or separate task |

## 2. Start from observed behavior

Before writing instructions, record concrete examples:

1. Prompts that should activate the skill.
2. Prompts that must not activate it.
3. A representative task the agent currently mishandles.
4. The observable failure: skipped validation, wrong order, unsafe action,
   missing domain fact, inconsistent format, or another specific defect.
5. Evidence that would demonstrate a corrected result.

If no failure, specialized knowledge, or reusable operation can be named, do not
add the skill yet.

## 3. Define a behavioral contract

Specify the skill before implementing it:

- **Inputs:** information and artifacts required to begin.
- **Outputs:** files, decisions, reports, or state the workflow produces.
- **Invariants:** conditions that must remain true throughout execution.
- **Workflow:** ordered steps and branches.
- **Validation:** evidence required before completion.
- **Failure behavior:** what to do when inputs, tools, permissions, or checks fail.
- **Boundaries:** adjacent tasks the skill intentionally does not own.

The contract should make the process predictable without forcing identical
outputs where project context requires judgment.

## 4. Define a precise trigger contract

The `description` is the primary routing interface. Write it before the body.
Include both the capability the skill provides and concrete contexts or user
intents that should activate it.

Prefer:

```yaml
description: Diagnose failing automated tests by reproducing failures, isolating the first causal error, and verifying the smallest corrective change. Use when tests fail locally or in CI, a test is flaky, or a user asks for root-cause analysis of a failing test suite.
```

Avoid:

```yaml
description: Helps with testing and code quality.
```

Trigger-writing rules:

- use terms users actually say;
- front-load the distinctive action, artifact, and trigger terms because hosts
  may shorten descriptions in a large catalog;
- keep one coherent intent per skill;
- include adjacent cases only when the same workflow handles them;
- avoid identity claims such as “expert,” promotional language, and duplicate synonyms;
- keep host-specific invocation syntax out of the portable description;
- evaluate exclusions with realistic negative and near-miss prompts instead of
  making the description enormous;
- compare the description against its closest competing skills, not in isolation.

## 5. Keep the package portable

Use this baseline structure:

```text
skill-name/
  SKILL.md
  scripts/       optional executable operations
  references/    optional details loaded only when needed
  assets/        optional templates or files used in outputs
```

Portable frontmatter requires:

```yaml
---
name: verb-led-skill-name
description: What the skill does. Use when the relevant trigger conditions occur.
---
```

Use lowercase letters, digits, and hyphens for `name`; keep it under 64
characters and match the containing directory. Prefer short, verb-led names.

Some hosts support additional frontmatter or UI metadata. Add it only for a
documented need, and keep the portable `name` and `description` valid.

Use forward slashes in relative resource links. Avoid absolute paths, local
machine assumptions, and deep reference chains.

## 5A. Choose invocation and portfolio boundaries

Decide whether the skill should be invoked implicitly, explicitly by a user, or
both. Prefer explicit invocation when false activation can cause destructive,
expensive, privileged, or production-impacting behavior. Host controls belong
in host-specific metadata and must not be presented as portable frontmatter.

Before adding a skill, identify its closest catalog neighbors. Consolidate
skills that own the same prompts and workflow; sharpen boundaries when nearby
prompts need different workflows. Test the skill inside the realistic catalog,
because routing performance in isolation does not predict performance among
distractors. Follow [invocation and portfolios](invocation-and-portfolios.md).

## 6. Write an executable workflow

Write instructions in imperative form. For every stage, tell the agent:

- what to inspect or change;
- how to choose between meaningful branches;
- what evidence confirms the stage is complete;
- what to do if the expected evidence is absent.

Give one preferred default path and only the branches that materially change
the result. Use ordered steps where order, branching, or checkpoints matter;
otherwise state the outcome, constraints, and validation without inventing a
rigid transcript. Explain why only when the reason helps the agent generalize or
resist a known failure. Provide an output template or input/output example when
format is part of correctness.

Prefer vertical slices that produce testable progress. Avoid long horizontal
phases that modify many components before any result can be checked.

Weak:

> Carefully review the implementation and ensure it follows best practices.

Strong:

> Inspect the changed public interfaces, run the narrowest affected tests, and
> report each unresolved failure with its command and first causal error.

Do not prescribe exact commands when the command depends on the repository and
the agent can discover it safely. Do prescribe or script commands when order,
flags, or data handling are fragile.

## 7. Match freedom to risk

Choose the narrowest degree of freedom that remains useful:

- **High freedom:** heuristics for research, design, or tasks with many valid approaches.
- **Medium freedom:** ordered workflow, pseudocode, parameterized commands, and decision tables.
- **Low freedom:** validated scripts, fixed gates, explicit approvals, and tightly constrained parameters.

Use low freedom for destructive actions, deployments, migrations, security,
cryptography, compliance, credential handling, and irreversible external state.
State required approvals and stop conditions explicitly.

## 8. Apply progressive disclosure

Treat context as a limited shared resource:

1. `name` and `description` advertise the skill.
2. `SKILL.md` supplies the core workflow after activation.
3. Resources supply branch-specific detail only when needed.

Keep `SKILL.md` below 500 lines and preferably well below 5,000 words. Move
large schemas, API documentation, catalogs, extended examples, and variant
instructions into `references/`. Link every reference directly from
`SKILL.md`, explain when to read it, and avoid chains where one reference only
points to another.

For reference files longer than 100 lines, include a table of contents or search
anchors. Do not duplicate the same rule in multiple files.

Observe which references the agent actually loads during evaluations. Promote
repeatedly required guidance into `SKILL.md`, improve routing for resources that
are needed but skipped, and delete resources that remain unused.

## 9. Use resources deliberately

### Scripts

Add a script when an operation is repeatedly rewritten, mechanically
verifiable, or too fragile for ad hoc generation. Scripts should:

- accept explicit inputs and validate them;
- produce stable, inspectable output;
- fail closed with useful errors that identify the failed input or check and a
  safe recovery action, rather than returning the problem to the model;
- avoid hidden network or filesystem side effects;
- preserve user data unless destructive behavior is explicitly requested;
- declare and verify runtime dependencies;
- justify consequential constants, limits, and defaults;
- document whether the agent should execute the script or inspect it as reference;
- be tested by execution, not merely reviewed as text.

For high-risk batch or destructive transformations, prefer
plan -> validate -> execute -> verify: first write a structured intermediate
artifact, validate it independently, then apply it and inspect the result.

### References

Add references for knowledge the agent may need to reason correctly but does not
need on every invocation. Put routing instructions in `SKILL.md`; put the detail
in the reference.

Do not freeze fast-changing facts into a skill when current official docs or a
tool can retrieve them safely. If legacy information is necessary, isolate it,
label the version or date, and define how freshness is checked.

### Assets

Add assets for files used in generated output: templates, boilerplate, icons,
fonts, or examples to copy and adapt. Do not load assets into context unless the
workflow requires their contents.

## 10. Require evidence before completion

Define “done” using observable evidence. Depending on the task, require:

- tests or checks and their exact outcomes;
- a rendered or opened artifact, not just successful file creation;
- an inspected diff;
- schema or syntax validation;
- a dry run or preview before an external mutation;
- explicit reporting of checks that could not be performed.

Never allow the skill to claim success solely because an action was attempted.
If validation cannot run, report the limitation and avoid upgrading an
unverified result to “complete.”

## 11. Handle failures and rationalizations

Document recovery paths for predictable failures: missing tools, invalid
inputs, unavailable services, permission denial, failing checks, and partial
state. For high-risk workflows, name common unsafe shortcuts and the required
response—for example, do not disable a security check merely to make a pipeline
green.

Use anti-rationalization language selectively. It is valuable when agents have
repeatedly skipped a critical gate, but excessive prohibitions waste context and
can make a skill rigid or noisy. Whenever possible, replace prose constraints
with mechanical enforcement.

## 12. Separate authoring from evaluation

Evaluate the skill on raw tasks without leaking the intended answer. Compare it
against a no-skill baseline. Include positive, negative, ambiguous, held-out, and
distractor trigger prompts, plus successful and failing execution paths. Run
multiple isolated trials for critical cases and cover every consequential branch
and behavioral constraint. Test every model, host, invocation path, and realistic
catalog configuration the skill claims to support. Preserve prompts, outputs,
logs, diffs, resource loads, and validation artifacts so regressions can be diagnosed.

Follow [evaluation.md](evaluation.md) for the complete method.

## 13. Maintain the skill as software

- version the skill with its scripts and references;
- record the origin and license of external material;
- review upstream changes before adoption;
- test after changing the name, description, workflow, or scripts;
- remove obsolete instructions instead of appending exceptions indefinitely;
- consolidate duplicated rules into one source of truth;
- update from real usage traces and documented failure modes;
- revalidate host-specific metadata when the portable skill changes.

Classify the skill as primarily a **capability skill** or **preference skill**.
Re-baseline capability skills after material model or tool upgrades and retire
them when they no longer improve results. Revalidate preference skills whenever
the team process or output contract changes. Either type must be re-tested after
host routing, permission, or execution semantics change.

## 14. Reject common skill smells

- broad descriptions that activate for unrelated tasks;
- generic leading words or keyword bait that compete for unrelated requests;
- “expert persona” prose without an operational workflow;
- a monolithic `SKILL.md` containing every reference and variant;
- rigid command transcripts with hardcoded local paths;
- too many equal options without a preferred default;
- unexplained magic constants or undeclared runtime dependencies;
- instructions that repeat facts the model already knows;
- steps without completion criteria;
- success claims without evidence;
- duplicated or contradictory rules;
- hidden side effects or implicit external mutations;
- references that are unlinked, deeply chained, or never loaded;
- stale version-specific facts with no freshness policy;
- scripts that were not executed during testing;
- instructions used where a test, policy, or hook should enforce the rule;
- endless additions made without deleting obsolete guidance;
- a large catalog of overlapping, unused, or no-longer-helpful skills.

## 15. Definition of ready

A skill is ready for use only when:

- its problem and boundary are supported by concrete examples;
- its trigger suite meets the agreed precision and recall targets;
- explicit or implicit invocation is justified and tested with portfolio distractors;
- its workflow produces a measurable improvement over the baseline;
- required validation and failure behavior work in realistic tests;
- bundled scripts execute successfully on representative inputs;
- security review covers instructions, code, dependencies, and side effects;
- the package passes structural validation;
- held-out repeated trials pass on every supported model and host;
- the freshness and retirement policy is documented;
- a maintainer and update path are known.
