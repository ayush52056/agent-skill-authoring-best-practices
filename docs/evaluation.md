# Evaluating Agent Skills

Evaluation answers two separate questions:

1. Does the right skill load for the right request?
2. Once loaded, does it improve task outcomes enough to justify its context and risk?

## 1. Establish the baseline

Run representative tasks without the skill. Preserve the prompt, environment,
output, tool log, diff, checks, time, and approximate token use. Record the
specific failure the skill is expected to correct.

Do not write a skill around an imagined weakness when a current model already
handles the task reliably.

Freeze a held-out subset before substantial authoring. Do not tune the skill or
description directly against those cases.

## 2. Build a trigger suite

Maintain three prompt groups:

- **Positive:** diverse wording that should activate the skill.
- **Negative:** nearby tasks that should not activate it.
- **Boundary:** incomplete or ambiguous requests where activation is debatable.

Start with roughly 8 to 10 positive prompts and 8 to 10 negative or near-miss
prompts. Vary phrasing, detail, explicitness, paths, casual language, and common
typos. These are starting points, not universal sufficiency thresholds. Expand
the suite whenever a routing failure appears in real use. Negative cases must be
genuinely adjacent. Irrelevant prompts make precision look better than it is.

Split the initial suite before tuning. A useful starting split is 60% for
description refinement and 40% for validation. Run every query three times and
record the observed trigger rate. Select the best description by validation
performance, not by the score on prompts used to edit it. Finish with 5 to 10
fresh prompts that were not used during refinement.

Track:

- trigger recall: positive prompts activated / all positive prompts.
- trigger precision: correct activations / all activations.
- boundary decisions and the rationale for the expected behavior.

Optimize both precision and recall. Expanding the description to catch every
positive prompt may create costly over-triggering.

Run the suite with the skill alone, its closest competitors, and the realistic
production catalog. Record the selected skill and resources loaded. Use
[the trigger fixture](../templates/trigger-evals.json) to capture near misses,
competing skills, and held-out status.

Keep a separate trigger suite for each host, model, and invocation mode. An
implicit suite measures routing from natural-language requests. An explicit
suite measures direct invocation such as `$skill-name`. Combining them hides
whether discovery or execution caused a failure.

## 3. Evaluate execution

Cover:

- a normal successful path.
- missing or invalid inputs.
- unavailable tools or permissions.
- a failed validation step.
- a branch requiring judgment.
- the most consequential safety boundary.
- recovery from partial progress where applicable.

Use outcome measures appropriate to the workflow:

- task correctness.
- required checks passed.
- unsupported claims or missed defects.
- unnecessary file or external-state changes.
- recovery quality.
- time, tool calls, and context cost.
- human review effort.

Also score behavior coverage: whether every consequential constraint, branch,
approval boundary, and completion gate was exercised. A correct final artifact
can conceal a skipped safety step or a workflow that succeeds only by chance.

## 4. Prevent evaluation leakage

Give the evaluator the raw task and artifacts, not the intended diagnosis or
answer. Use a fresh context when possible. Do not leave expected outputs where
the agent can discover them. If independent reviewers are used, ask them to
judge the artifact against the task and rubric rather than confirm the author's
conclusion.

## 5. Compare variants

For meaningful changes, compare:

- no skill.
- current released skill.
- proposed skill.

Keep task inputs and environment equivalent. Review failures qualitatively.
Aggregate scores alone rarely explain whether the description, workflow,
reference routing, script, or validation gate caused the regression.

Run critical cases in fresh contexts for three to five trials per configuration,
or more when the result is highly variable or high-risk. Report distributions
and individual failures rather than only the best run.

For each task case, record the configurations, models, hosts, required behavior,
forbidden behavior, verifier, trial count, and retained evidence.

## 5A. Retain the evidence package

For every run, retain:

- the exact prompt, fixtures, environment, host, model, and skill revision.
- output artifacts and a tool or event trace.
- assertion results with evidence for each claim.
- duration, available token observations, and tool counts.
- human feedback for subjective quality.

Aggregate comparable runs into a versioned result and readable summary.
Report mean, variation, baseline delta, failures, and missing data.
Assertions that always pass with and without the skill are not discriminating.
Assertions that always fail may identify a broken task, verifier, or skill.

For subjective artifacts, use a blind comparison when practical. Hide which
condition produced each artifact and ask the reviewer to judge against the same
rubric. Mechanical assertions should use scripts instead of visual guessing.

## 6. Test the support matrix

For every claimed model and host, test:

- implicit and explicit invocation paths that are supported.
- the production skill catalog and nearest distractors.
- host-specific metadata, permissions, and dependency behavior.
- resource loading and relative path handling.
- the normal path and the highest-risk failure path.

Do not generalize a pass on one model or harness to another. If comprehensive
support is too expensive, narrow the documented support claim.

## 7. Test bundled resources

- Execute every critical script on representative valid and invalid inputs.
- Verify exit codes, errors, output stability, and side effects.
- Check that each reference is directly discoverable from `SKILL.md`.
- Confirm the agent loads a reference only on the branch that needs it.
- Verify each context pointer loads its reference only for the stated branch.
- Render or open generated artifacts when visual or structural quality matters.

## 8. Set release criteria

Define thresholds before reviewing results. A typical initial policy is:

- 90% or better positive-trigger recall.
- 95% or better precision on the maintained trigger suite.
- no hard-gate safety failures.
- all critical scripts and validation paths pass.
- a measurable task-quality improvement over the baseline.
- no regression on the held-out set or supported host/model matrix.
- acceptable collision rates in the production catalog.
- no material increase in unrelated changes or unsupported completion claims.

Adjust thresholds to risk. Security, deployment, and destructive workflows
should require stricter gates and human approval.

## 9. Iterate from traces

Classify every failure before editing:

- routing failure.
- missing knowledge.
- unclear step or branch.
- excessive freedom.
- excessive rigidity.
- missing validation.
- unsafe side effect.
- stale reference or script defect.

Make the smallest change that addresses the class, rerun the entire relevant
suite, and delete obsolete or duplicated guidance. Do not accumulate exceptions
without proving they improve the evaluation.

When pruning a suspected no-op, run an ablation without the disputed sentence or
reference. Delete it when repeated relevant cases show no useful behavior change.
A no-op judgment is specific to the tested model, host, catalog, and task set.

After material model, host, tool, dependency, or policy updates, rerun the
baseline and candidate. Retire or disable a skill that no longer provides a
repeatable net benefit.

## What current research adds

Published benchmarks reinforce the need for local evaluation rather than a
belief that more instructions always help. [SkillsBench](https://arxiv.org/abs/2602.12670)
reported an average improvement from curated skills, but some tasks regressed.
Focused packages also outperformed broad documentation in its tested settings.
The [Skill Coverage study](https://arxiv.org/abs/2606.20659) found that successful
trajectories often exercised only part of their skill constraints, motivating
explicit branch and behavior-coverage checks. A
[large-catalog retrieval study](https://arxiv.org/abs/2604.04323) found that
benefits eroded as realistic distractor pools grew. These findings are scoped to
their models, harnesses, and tasks. Use them to design tests, not as guaranteed
effect sizes for another system.

[SWE-Skills-Bench](https://arxiv.org/abs/2603.15401) found that many public
software-engineering skills did not improve pass rate, some added substantial
token cost, and a smaller specialized subset helped. The paper is a preprint,
but it reinforces a release rule already supported elsewhere: keep a skill only
when paired local evaluation shows a repeatable net benefit.
