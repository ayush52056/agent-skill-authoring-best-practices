# Skill Quality Rubric

Score a skill out of 100. Record evidence for every score; do not award points
for intention alone.

## Hard gates

A skill is not publishable regardless of score if any of these are true:

- malformed or missing `name` or `description` frontmatter;
- unreviewed executable code or hidden external side effects;
- destructive behavior without explicit scope, preview, and approval boundaries;
- no validation for a workflow that changes files or external state;
- bundled scripts fail their representative execution tests;
- licensing or provenance of copied material is unknown;
- evaluation shows no meaningful improvement over the no-skill baseline.

## Scoring

### Problem and scope — 15 points

- 5: based on documented prompts and observable failure modes;
- 5: owns one coherent workflow with explicit boundaries;
- 5: uses a skill instead of a better-suited instruction, tool, hook, or test.

### Trigger contract — 20 points

- 5: description front-loads a distinctive capability and artifact or action;
- 5: concrete activation contexts, boundaries, and invocation policy are justified;
- 5: positive prompts activate reliably in repeated supported-host trials;
- 5: adjacent negative, boundary, and portfolio-distractor prompts avoid unwanted activation.

### Workflow quality — 20 points

- 5: actions are ordered and written in imperative form;
- 5: meaningful branches have selection criteria;
- 5: stages have observable completion criteria;
- 5: predictable failures have safe recovery behavior.

### Context efficiency — 15 points

- 5: `SKILL.md` contains only the core workflow;
- 5: references are branch-specific, directly linked, non-duplicative, and observed in evaluation;
- 5: scripts and assets are used instead of repeatedly embedding large content.

### Reliability and evaluation — 15 points

- 5: realistic, held-out, repeated task evaluation is compared with a baseline across supported hosts/models;
- 5: validation evidence is required before completion;
- 5: scripts, critical branches, constraints, and failure paths have regression coverage.

### Safety and governance — 10 points

- 3: permissions and side effects follow least privilege;
- 3: instructions, code, dependencies, and external content are reviewed;
- 2: provenance, ownership, and update policy are recorded;
- 2: high-risk operations have previews, approvals, and fail-closed behavior.

### Maintainability — 5 points

- 2: package passes structural validation;
- 2: instructions have one source of truth and obsolete guidance is removed;
- 1: host extensions, freshness checks, ownership, and retirement criteria are documented.

## Interpretation

| Score | Decision |
|---|---|
| 90–100 | Strong candidate for broad use after all hard gates pass |
| 80–89 | Usable in a controlled rollout; address recorded weaknesses |
| 70–79 | Pilot only; revise before recommending |
| Below 70 | Do not publish |

A high score does not override a hard-gate failure. Re-score after meaningful
changes and retain prior evaluation artifacts to detect regressions.
