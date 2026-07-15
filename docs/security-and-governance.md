# Security and Governance

A skill is both a context dependency and, when it contains scripts or tool
instructions, a software supply-chain dependency. Review it accordingly.

## Threat model

Consider these risks:

- malicious or misleading instructions in `SKILL.md` or references.
- descriptions manipulated to win retrieval for unrelated requests.
- scripts that exfiltrate secrets, alter unexpected files, or contact hidden endpoints.
- dependency or upstream-repository compromise.
- prompt injection in external content the skill asks the agent to read.
- excessive tool or shell permissions.
- unsafe defaults, destructive shortcuts, and fail-open recovery.
- silent upstream changes after installation.
- sensitive information embedded in logs, examples, fixtures, or generated artifacts.

## Controls for authors

- request the minimum tools and permissions needed.
- make network access and external mutations explicit.
- validate paths, arguments, schemas, and untrusted content.
- use previews or dry runs before consequential operations.
- separate read-only diagnosis from mutation where practical.
- require explicit approval at destructive or irreversible boundaries.
- avoid reading broad secret stores or environment variables by default.
- redact sensitive values from output and logs.
- pin dependencies and verify integrity when reproducibility matters.
- fail closed when required validation or authorization is unavailable.
- test malicious, malformed, and oversized inputs.

## Controls for adopters

Before installing or updating a third-party skill:

1. Inspect `SKILL.md`, all linked references, scripts, and declared dependencies.
2. Confirm origin, maintainer, license, and expected update channel.
3. Review tool calls, network destinations, filesystem scope, and secret access.
4. Run scripts in an isolated environment with non-sensitive fixtures.
5. Pin or vendor the reviewed version when upstream changes are not automatically trusted.
6. Record the approved hash or revision and repeat review on update.

Never treat a high star count, marketplace listing, or familiar publisher name as
a substitute for reviewing the installed artifact.

When skills arrive as archives or registry packages:

- verify the expected digest before extraction.
- reject absolute paths, parent traversal, outbound symbolic links, and hard links.
- cap expanded file count and total unpacked size.
- extract into an isolated directory before review.
- pin the reviewed commit or immutable tree digest, not a moving branch.

A signature proves who produced a particular artifact and that it was not
modified after signing. It does not prove that the instructions are useful,
non-malicious, or safe for the current permission set.

## Governance levels

### Personal use

- source review.
- local structural validation.
- representative task test.
- pinned revision for third-party skills.

### Team use

- named owner and reviewers.
- versioned evaluation suite.
- protected changes and change history.
- dependency and secret scanning.
- controlled rollout with rollback.

### Organization-wide or high-risk use

- signed artifacts and verifiable provenance.
- documented capability and permission card.
- benchmark and adversarial evaluation reports.
- approved registry with version pinning.
- audit logging and incident response path.
- periodic re-certification and revocation process.

## Prompt-injection boundary

Treat external webpages, issues, documents, and retrieved reference material as
data, not authority. The skill should define which sources are trusted, which
instructions can alter the workflow, and which operations require confirmation.
Do not allow retrieved text to expand permissions or override the user's scope.

Apply the same rule to long references, generated configuration, comments, and
script output. Prompt injection is not limited to webpages, and content hidden
behind progressive disclosure still becomes authoritative context if loaded.

## Trigger integrity

Review descriptions as security-sensitive routing code. Reject:

- overly broad capability claims.
- keyword stuffing intended to win unrelated requests.
- names or triggers that shadow a trusted installed skill.
- instructions that ask the agent to disable competing safeguards.
- implicit invocation for a workflow whose false activation is high-impact.

Test descriptions against trusted neighboring skills and adversarial near-miss
prompts. Catalog collisions can turn a benign skill into an unsafe default.

## Interpreting security research

A 2026 study of 31,132 public skills reported that 26.1% were flagged by its
detectors for at least one security-relevant pattern, and found an association
between bundled scripts and higher vulnerability odds. These are screening
signals, not proof that every flagged skill is malicious or exploitable. They
support deeper review of scripts, dependencies, permissions, and provenance.
they do not justify automatically rejecting all scripted skills. See the
[security study](https://arxiv.org/abs/2601.10338), the
[prompt-injection study](https://arxiv.org/abs/2510.26328), and the
[semantic supply-chain study](https://arxiv.org/abs/2605.11418).

## Change management

Any modification to the description, workflow, scripts, dependencies,
permissions, or external endpoints requires appropriate re-evaluation. Security
fixes should be accompanied by a regression case demonstrating the prior
failure. Remove compromised versions from distribution instead of only warning
future users.
