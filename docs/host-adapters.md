# Portable Core and Host Adapters

Write the smallest portable skill first. Add host behavior only when it solves a
documented need. A host accepting extra fields does not make those fields part
of the portable Agent Skills contract.

## 1. Portable package

A portable skill is a directory containing `SKILL.md`. The frontmatter requires
`name` and `description`.

The open specification also defines these optional fields:

| Field | Use | Portability note |
|---|---|---|
| `license` | State the terms for the skill package | Use an SPDX identifier or a clear license reference when possible |
| `compatibility` | State environment, dependency, or access requirements | Keep it concise and test every claimed environment |
| `metadata` | Store string-to-string implementation metadata | Do not depend on unknown keys for core behavior |
| `allowed-tools` | Advertise or preapprove tools on supporting hosts | Experimental and security-sensitive because semantics differ by host |

Keep the portable package valid even when a host ignores every optional field.
Put UI labels, invocation controls, model selection, and tool bindings in a host
adapter when the host provides one.

### Package host differences without duplicating the workflow

Not every host reads a separate adapter file. Claude Code host controls are
frontmatter fields in `SKILL.md`, while OpenAI interface controls belong in
`agents/openai.yaml`. A single physical package therefore cannot always express
different invocation policies for every host.

Keep the portable body and shared metadata as the source of truth. At release
time, create a host package that adds only the documented host fields. A Claude
Code package may add Claude-specific frontmatter to its copy of `SKILL.md`. An
OpenAI package may add `agents/openai.yaml` without changing the portable
frontmatter. Validate the generated package on its target host and keep the
packaging step reproducible.

Do not invent a companion filename and assume a host will read it. If a host
does not document an adapter file, its supported extensions must appear where
that host expects them.

## 2. Claude Code adapter

Claude Code follows the open format and adds fields that control discovery,
invocation, arguments, execution context, permissions, and preprocessing.
These fields go directly in the Claude Code package's `SKILL.md` frontmatter.

| Field or feature | Purpose | Main caution |
|---|---|---|
| `when_to_use` | Add routing detail to the catalog entry | It shares the documented listing budget with `description` |
| `disable-model-invocation` | Require explicit user invocation | Use for costly, destructive, privileged, or timing-sensitive actions |
| `user-invocable` | Hide passive reference skills from the user menu | It does not create a security boundary |
| `argument-hint` and `arguments` | Define user-facing arguments | Validate expanded values before using them in commands |
| `context: fork` and `agent` | Run the skill as an isolated subagent task | The skill must contain a complete task because the fork lacks conversation history |
| `model` and `effort` | Override execution for the current turn | Test cost, availability, and behavior on every supported configuration |
| `paths` | Limit automatic activation by file patterns | Treat it as routing assistance, not access control |
| `hooks` | Enforce lifecycle behavior | Prefer hooks for invariants that must not rely on model compliance |
| `shell` | Choose the shell used by dynamic injection | Document platform requirements and quote safely |

Claude Code also supports dynamic context injection with shell commands embedded
in a skill. The command runs before the model sees the rendered instructions.
Use it only with fixed, reviewed commands and bounded output. Never interpolate
untrusted text into the command. Review the possibility of secret exposure and
document how administrators can disable skill shell execution.

In Claude Code, `allowed-tools` grants listed tools without another approval. It
does not restrict the agent to only those tools. Use permission deny rules or a
separate sandbox when actual restriction is required.

An invoked skill remains in conversation context. Current Claude Code guidance
says compaction may reattach the first 5,000 tokens of recent invoked skills
within a shared 25,000-token budget. Keep critical instructions near the start,
test multi-skill sessions, and do not assume every late section survives long
context churn.

## 3. OpenAI adapter

Keep portable instructions in `SKILL.md`. Use `agents/openai.yaml` for supported
OpenAI interface metadata and invocation policy. Common uses include:

- human-facing display name and short description.
- a default prompt for the interface.
- implicit invocation policy.
- declared MCP tool dependencies.

This minimal adapter allows automatic invocation and provides interface text:

```yaml
interface:
  display_name: "Diagnose test failures"
  short_description: "Find the cause of failing tests"
  default_prompt: "Use $diagnose-test-failures to find and verify the cause of the failing tests."
policy:
  allow_implicit_invocation: true
```

`policy.allow_implicit_invocation` defaults to `true`. Set it to `false` when
the skill should be available only through an explicit `$skill-name` request.
Automatic discovery still depends on installing a valid skill in a location the
host scans. The policy controls whether the installed skill may be invoked
implicitly. Quote string values and keep keys unquoted in this file.

Regenerate or review `agents/openai.yaml` whenever the portable name,
description, workflow, or dependencies change. Do not put interface-only fields
into portable frontmatter.

OpenAI currently maintains active examples in
[openai/plugins](https://github.com/openai/plugins). The older
[openai/skills](https://github.com/openai/skills) repository is deprecated and
should be treated as historical evidence.

## 4. GitHub Copilot adapter

GitHub supports project and personal skill locations across Copilot surfaces.
Use the current official documentation for supported paths and CLI behavior.

Before installation:

1. Preview the complete skill package.
2. Inspect scripts, references, network access, and preapproved tools.
3. Pin a reviewed tag or commit when reproducibility matters.
4. Retain provenance added by the installer.
5. Validate publishing with a dry run before distribution.

Treat public preview commands and behavior as changeable host features.

## 5. Adapter acceptance tests

For every host adapter, record:

- supported host and minimum version.
- discovery location and precedence.
- implicit and explicit invocation behavior.
- description truncation or catalog budget.
- permission meaning for every tool field.
- argument expansion and quoting behavior.
- resource path root.
- network and package-installation availability.
- behavior after context compaction.
- the exact evaluation revision that passed.

Use one trigger suite for each host, model, and invocation mode. Do not combine
implicit and explicit runs into one trigger rate. For an explicit-only package,
verify both that ordinary nearby requests do not invoke it and that an explicit
request does.

Remove a host claim when these checks are not maintained.

## Sources

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code Agent SDK skills](https://code.claude.com/docs/en/agent-sdk/skills)
- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)
- [GitHub Copilot Agent Skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
