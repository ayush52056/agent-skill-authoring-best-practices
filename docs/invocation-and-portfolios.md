# Invocation and Skill Portfolios

A skill can be well written and still perform poorly inside a large catalog.
Routing quality depends on the skill, the other installed skills, the host, and
the amount of catalog metadata placed in the model's initial context. Treat the
installed portfolio as a product with its own budget and evaluations.

## 1. Choose the invocation policy

Decide whether a skill should be discovered automatically, invoked explicitly,
or support both. This decision is portable; the field or command that implements
it is host-specific.

| Policy | Prefer when | Main risk | Required evaluation |
|---|---|---|---|
| Implicit | Users should not need to know the skill exists and false activation is cheap | Over-triggering, catalog cost, unexpected behavior | Positive, negative, near-miss, and distractor prompts |
| Explicit | The operation is high-risk, expensive, rare, or intentionally user-controlled | Users may forget the skill or use the wrong one | Discoverability and correct-use tests |
| Both | Routine discovery is useful but expert users also need deterministic selection | Two entry paths can drift | Test both paths against the same task contract |

Prefer explicit invocation for destructive operations, production changes,
security-sensitive review, costly external calls, or any workflow where a false
positive is materially worse than a missed activation. Explicit invocation does
not remove the need for a precise description: the catalog and user still need
to understand the skill.

For example, Codex can disable implicit invocation with host metadata in
`agents/openai.yaml`. Other hosts expose different controls. Keep these files
beside, not inside, the portable contract unless the open specification adopts
the field.

## 2. Budget the catalog

Hosts commonly expose skill names and descriptions before a skill is selected.
That catalog competes with the task, repository instructions, and tool metadata
for context. Some hosts truncate descriptions or omit entries once their catalog
budget is exhausted.

- front-load distinctive capability and trigger terms;
- keep descriptions specific and remove repeated synonyms;
- install only skills relevant to the current environment;
- disable, group, or retire low-value skills;
- avoid duplicate names and overlapping trigger contracts;
- measure routing with the actual portfolio, not an isolated skill list.

Do not treat a maximum description length as a target. Shorter is useful only
when it still separates the skill from its closest alternatives.

## 3. Prevent collisions and trigger abuse

For every new skill, list its nearest neighbors and answer:

1. Which prompts belong uniquely to this skill?
2. Which prompts belong to a neighboring skill?
3. Which prompts need clarification, composition, or explicit selection?
4. Would the same user wording activate more than one description?
5. Does the description contain broad keywords that are not necessary to its workflow?

Do not make descriptions artificially broad or repeat popular keywords to win
selection. This is both a quality defect and a supply-chain risk. If two skills
share most positive prompts, consolidate them or establish an explicit boundary.

## 4. Evaluate with distractors

Run the trigger suite in at least these configurations:

1. the skill alone;
2. the skill with its closest competing skills;
3. the realistic production catalog;
4. an oversized or adversarial catalog when broad distribution is expected.

Record which skill loaded, which resources were read, and whether an unneeded
skill changed the result. Add every real collision as a held-out regression case.
Use [the trigger evaluation template](../templates/trigger-evals.json) to retain
the expected skill and competing skill for each prompt.

## 5. Compose only when the boundary is real

Prefer independent skills with clean trigger contracts. Add a router or
orchestrator only when users regularly need a stable multi-skill sequence and
direct descriptions cannot express the choice reliably.

A router must:

- own only selection and sequencing, not duplicate child instructions;
- identify the inputs and outputs passed between child skills;
- stop on ambiguous or unsafe branches;
- add less context and failure surface than it removes;
- have its own routing, branch, and partial-failure evaluations.

If the router becomes a catalog inside a skill, split or remove it.

## 6. Manage the portfolio lifecycle

Track at least: owner, purpose, invocation policy, closest competitors,
supported hosts/models, last evaluation, approved revision, and retirement rule.

Distinguish:

- **capability skills**, which teach a model or tool a workflow it may eventually
  perform reliably without help; and
- **preference skills**, which encode organization-specific process or output
  choices and remain relevant even as models improve.

Re-run baselines after material model, host, tool, or repository changes. Remove
or disable a capability skill when it no longer improves outcomes, and update a
preference skill when the underlying policy changes. A smaller, differentiated
portfolio is usually easier to route, review, and secure.

## Sources

See the catalog, invocation, routing, and retirement entries in the
[evidence map](evidence-map.md). Host-specific controls should always be checked
against the current official documentation.
