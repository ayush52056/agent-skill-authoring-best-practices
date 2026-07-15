# Source Reviews and Examples

This review explains what each source contributed to the handbook. It also
shows how a useful source pattern becomes a practical example in this
repository.

Last reviewed: 2026-07-16.

## How to read this review

- **Source example or signal** describes a concrete pattern, example, or result
  found in the linked source.
- **Use in this repository** explains what we adopted and what we did not treat
  as a universal rule.
- Text in quotation marks is a short direct excerpt. Everything else is a
  paraphrase or our interpretation.
- Repository examples are rewritten for this guide. They are not copied skill
  files unless the text is clearly marked as a quotation.

## Contents

1. [Open standard and official documentation](#open-standard-and-official-documentation)
2. [Production repositories](#production-repositories)
3. [Practitioner implementations and writing](#practitioner-implementations-and-writing)
4. [Empirical and security research](#empirical-and-security-research)
5. [How source patterns become guide examples](#how-source-patterns-become-guide-examples)

## Open standard and official documentation

| Source | Source example or signal | Use in this repository |
|---|---|---|
| [Agent Skills specification](https://agentskills.io/specification) | The minimum package is `SKILL.md` with `name` and `description`. Its description rule says it “describes what the skill does and when to use it.” | Defines the portable package, metadata limits, relative paths, optional resource folders, and validation baseline. Host extensions stay outside the portable core. |
| [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices) | It contrasts a generic PDF explanation with a direct instruction to use `pdfplumber`, then use OCR for scanned files. It also gives `references/api-errors.md` as a conditional reference. | Supports concise instructions, one clear default, an escape path, conditional resource loading, output templates, checklists, and plan then validate then execute workflows. The tool choices in its PDF example are examples, not universal requirements. |
| [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills) | OpenAI says to “Front-load the key use case and trigger words.” Its sample `commit` skill stages changes in logical groups and keeps commits reviewable. | Supports front-loaded descriptions, explicit and implicit invocation, focused jobs, instruction-first skills, and host metadata in `agents/openai.yaml`. OpenAI-specific invocation fields are labeled as host features. |
| [OpenAI skills repository](https://github.com/openai/skills) | Focused packages such as `gh-fix-ci`, `pdf`, and `linear` combine a core workflow with task-specific resources. | Used as implementation evidence for narrow capabilities, direct resource routing, and deterministic helpers. Individual skill details are not copied into the portable template. |
| [Anthropic Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) | The overview explains progressive loading from metadata to instructions and then to resources. | Reinforces the three-level context model and the need to keep `SKILL.md` focused. Claude-specific locations and APIs are not portable rules. |
| [Anthropic skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Examples show a preferred tool with an OCR fallback, direct links to conditional references, and structured intermediate files before risky execution. | Supports calibrated freedom, examples, validation loops, useful errors, and plan then validate then execute. Exact tools and section names remain optional. |
| [Anthropic skills repository](https://github.com/anthropics/skills) | Document and artifact skills separate core instructions from references, scripts, and output assets. | Provides production examples of progressive disclosure and artifact validation. Each package has its own scope and license, so examples require source review before reuse. |
| [GitHub Copilot Add Agent Skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) | The `github-actions-failure-debugging` example summarizes failed logs before loading full logs. GitHub also says, “Always inspect the content of a skill before installation.” | Supports staged information loading, script review, source preview, version pinning, provenance, and caution around pre-approved shell access. GitHub directory locations and CLI commands are host-specific. |
| [GitHub Copilot SDK skills](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/skills) | The SDK exposes skill loading as an application feature rather than assuming every host discovers skills in the same way. | Supports testing every claimed host and documenting loader behavior. SDK code is not part of the portable skill format. |
| [Microsoft Agent Framework skills](https://learn.microsoft.com/en-us/agent-framework/agents/skills) | Its `expense-report` package uses `validate.py`, an on-demand policy FAQ, and an output template. The framework separates advertise, load, read, and run stages. | Provides a complete example of progressive disclosure and safe script runners. Microsoft provider APIs and its four-stage runtime are implementation details. |
| [Cursor 2.4 skills](https://cursor.com/changelog/2-4) | Cursor distinguishes always-on rules from skills used for dynamic context discovery and procedural instructions. | Supports choosing a skill only for conditional workflows. Cursor slash invocation and product behavior are host-specific. |
| [Cursor agent best practices](https://cursor.com/blog/agent-best-practices) | The guide emphasizes plans, feedback, tests, and review for agent work. | Supports short feedback loops and evidence before completion. These are adjacent agent practices, not skill format requirements. |

## Production repositories

| Source | Source example or signal | Use in this repository |
|---|---|---|
| [Google Gemini CLI skills](https://github.com/google-gemini/gemini-skills) | Separate skills cover general Gemini API development, live streaming, interactions, and video. The repository reports paired evaluation results for current API-code generation. | Shows how fast-changing SDK knowledge can be split by coherent API workflow and measured against a baseline. Reported results apply only to its tested models and tasks. |
| [GitHub Awesome Copilot](https://github.com/github/awesome-copilot) | The repository separates agents, instructions, skills, plugins, hooks, and workflows. It warns readers to inspect third-party contributions before installation. | Supports choosing the smallest correct extension type and treating popularity as discovery rather than proof. Community entries vary in quality. |
| [Microsoft Agent Skills](https://github.com/MicrosoftDocs/Agent-Skills) | Product skills package current Microsoft Learn guidance for specific Azure and Microsoft development tasks. | Shows the value of versioned product knowledge and official source links. It also motivates freshness checks because product documentation changes. |
| [NVIDIA skills](https://github.com/NVIDIA/skills) | The catalog organizes NVIDIA-specific workflows and identifies their publisher and source. | Supports publisher identity, provenance, product boundaries, and reviewed distribution. Publisher identity does not replace code and instruction review. |
| [NVIDIA SkillSpector](https://github.com/nvidia/skillspector) | The scanner checks skill packages for suspicious instructions, code, and dependency patterns. | Supports automated security screening as one review layer. Scanner output is a signal that needs human confirmation. |
| [Cloudflare skills](https://github.com/cloudflare/skills) | Cloudflare packages focused guidance for building on its platform rather than one broad web-development skill. | Supports product-specific skill boundaries and current platform references. Cloudflare commands are examples, not portable defaults. |
| [Cloudflare Agent Skills discovery RFC](https://github.com/cloudflare/agent-skills-discovery-rfc) | The proposal explores discovery through a standard well-known location. | Shows that discovery, distribution, and version metadata are separate concerns from writing `SKILL.md`. The proposal is experimental and is not treated as a required standard. |
| [Vercel agent skills](https://github.com/vercel-labs/agent-skills) | Skills focus on concrete frontend and platform workflows, with framework-specific examples. | Supports focused packages and examples grounded in a real toolchain. Framework preferences should be isolated from portable authoring advice. |
| [Trail of Bits skills](https://github.com/trailofbits/skills) | Security skills encode audit procedures, tool use, evidence collection, and explicit completion checks. | Supports low freedom for high-risk tasks, strong validation, and security-specific gotchas. Their strictness should not be copied into low-risk creative skills. |

## Practitioner implementations and writing

| Source | Source example or signal | Use in this repository |
|---|---|---|
| [Matt Pocock skills](https://github.com/mattpocock/skills) | The catalog separates user-invoked orchestrators from model-invoked disciplines and keeps workflows small and composable. | Supports deliberate invocation policy, portfolio boundaries, and routers only when users need them. The invocation field names are host-specific. |
| [Writing great skills](https://raw.githubusercontent.com/mattpocock/skills/main/skills/productivity/writing-great-skills/SKILL.md) | “A skill exists to wrangle determinism out of a stochastic system.” The guide treats every description word as catalog context cost. | Supports predictable process, leading trigger words, branch-based descriptions, and explicit context budgets. Its user-only metadata is not portable. |
| [Jesse Vincent Superpowers](https://github.com/obra/superpowers) | Skills encode repeatable engineering disciplines such as brainstorming, debugging, planning, and test-driven development. | Supports process-oriented skills, evidence gates, and corrections for repeated agent shortcuts. Strong process rules still require local evaluation. |
| [Jesse Vincent on Skills for Claude](https://blog.fsck.com/2025/10/16/skills-for-claude/) | The article presents skills as small folders that can load instructions and supporting files only when useful. | Supports progressive disclosure and packaging reusable process. Product behavior described in the article may have changed since publication. |
| [Addy Osmani on Agent Skills](https://addyosmani.com/blog/agent-skills/) | The article emphasizes process over persona, observable evidence, and designing from recurring failures. | Supports executable workflows, completion proof, and selective anti-rationalization. Practitioner experience is a hypothesis until local tests confirm it. |
| [Phil Schmid skill tips](https://www.philschmid.de/agent-skills-tips) | The guide recommends realistic positive and negative trigger examples and warns against over-prescribing tasks that need judgment. | Supports near-miss trigger suites and outcome-based instructions. Suggested prompt counts are starting points rather than formal thresholds. |
| [Trail of Bits authoring guide](https://www.mintlify.com/trailofbits/skills/contributing/skill-authoring) | The guide uses chronological workflows, explicit use boundaries, validation, and security checks for audit skills. | Supports ordered steps when sequence matters and strong review for security workflows. Routing boundaries still belong in metadata because the body loads later. |
| [Minko Gechev skill best practices](https://github.com/mgechev/skills-best-practices) | The repository demonstrates compact metadata, progressive disclosure, and evaluation-oriented authoring. | Supports keeping the core small and reviewing references as part of one package. Its recommendations are practitioner guidance rather than format requirements. |
| [Simon Willison agentic engineering patterns](https://simonwillison.net/guides/agentic-engineering-patterns/) | The patterns use short iterations, observable artifacts, tests, and review rather than trusting a single generated answer. | Supports validation loops and trace-based iteration. The source covers agentic engineering broadly, so we use it only for transferable workflow patterns. |
| [Thoughtworks context engineering](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html) | The article treats instructions, tools, and retrieved information as parts of one limited context environment. | Supports catalog budgeting and choosing between skills, repository instructions, and tools. It does not define Agent Skills metadata. |
| [Thoughtworks harness engineering](https://martinfowler.com/articles/harness-engineering.html) | The article favors fast, reliable feedback from tests, tools, and environment design. | Supports moving hard guarantees into linters, tests, policies, and scripts instead of relying only on prose. |
| [Thoughtworks maintainability sensors](https://martinfowler.com/articles/sensors-for-coding-agents.html) | Sensors turn architecture and maintainability expectations into feedback that an agent can act on. | Supports mechanical checks with clear errors and evidence-based completion. Sensor design remains project-specific. |

## Empirical and security research

| Source | Source example or signal | Use in this repository |
|---|---|---|
| [SkillsBench](https://arxiv.org/abs/2602.12670) | Version 4 reports 87 tasks across 8 domains. Curated skills increased average pass rate from 33.9% to 50.5% across 18 model and harness configurations. Focused skills with at most three modules performed better than larger bundles. | Supports paired no-skill baselines, focused packages, deterministic verifiers, and testing across configurations. The effect size is not assumed to transfer to another task. |
| [Skill Coverage](https://arxiv.org/abs/2606.20659) | Tested trajectories covered only 38.66% to 45.51% of extracted behavior constraints on average. Emphasizing failed constraints recovered some failed tasks. | Supports branch and behavior-constraint coverage rather than judging only the final output. Constraint extraction itself can be imperfect. |
| [Skills in realistic retrieval settings](https://arxiv.org/abs/2604.04323) | Agents retrieved from 34,000 public skills. Gains declined toward the no-skill baseline as selection conditions became more realistic. | Supports production-catalog distractors, collision testing, and catalog curation. Retrieval behavior depends on the tested model and selection system. |
| [SkillLearnBench](https://arxiv.org/abs/2604.20087) | The benchmark covers 20 verified tasks across 15 subdomains. Multiple rounds with external feedback improved skills, while self-feedback alone could drift. | Supports iteration from real traces and external verification. It does not show that automatic skill generation is reliable for every task. |
| [SKILL.md anatomy and smells](https://arxiv.org/abs/2607.01456) | The study reviewed 238 skills, derived a component taxonomy, and found automated smell signals in more than 99% of its dataset. | Supports explicit smell review and deleting accumulated guidance. Automated smell findings are not proof that a skill fails in practice. |
| [Registry to repository maintenance](https://arxiv.org/abs/2607.00911) | The study mined public and personal repositories. It found that reuse was often a one-time copy and later maintenance was mostly additive. | Supports provenance, local adaptation, ownership, and deletion during maintenance. Observed repository behavior is not automatically a best practice. |
| [Security vulnerabilities at scale](https://arxiv.org/abs/2601.10338) | The study analyzed 31,132 skills. Its detector flagged 26.1% for at least one vulnerability pattern and found scripts associated with higher odds of a flag. | Supports review of scripts, dependencies, permissions, and provenance. Detector findings are screening results, not confirmed malicious behavior. |
| [Prompt injection through skills](https://arxiv.org/abs/2510.26328) | The paper demonstrates hidden instructions in long skill files and referenced scripts, including attacks that reuse previously approved actions. | Supports reviewing every loaded resource, limiting standing approvals, and treating external text as data. Demonstrated attacks do not imply every long skill is malicious. |
| [Semantic supply-chain attacks](https://arxiv.org/abs/2605.11418) | The study shows that names, descriptions, and instructions can manipulate discovery, selection, and governance. | Supports treating descriptions as routing code, testing adversarial near misses, and rejecting keyword bait. Reported attack rates depend on the studied registries and models. |

## How source patterns become guide examples

### Example 1: turn a format rule into a useful description

The open specification requires a description that says what the skill does and
when to use it. OpenAI adds that important trigger words should come first.

Weak:

```yaml
description: Helps with CI.
```

Improved guide example:

```yaml
description: Diagnose failing GitHub Actions jobs by finding the first causal error and verifying a focused fix. Use when a pull request has failed CI checks, a workflow job is red, or the user asks why GitHub Actions failed.
```

The example combines the portable rule with OpenAI's catalog behavior. It does
not copy GitHub's longer failure-debugging workflow.

### Example 2: turn progressive disclosure into a routing instruction

Weak:

```markdown
See the references folder for more information.
```

Improved guide example:

```markdown
Read `references/api-errors.md` only after an API request returns a non-success status.
```

This pattern comes from the Agent Skills and Anthropic authoring guidance. The
new wording tells the agent both what to load and when to load it.

### Example 3: turn evaluation research into a release test

Weak:

```text
Run the skill once and check whether the answer looks correct.
```

Improved guide example:

```text
Run the same held-out task three times without the skill and three times with it.
Verify the final result and record whether each required workflow constraint was followed.
Repeat with the nearest competing skills installed.
```

SkillsBench motivates the paired baseline. Skill Coverage motivates checking
behavior constraints. The realistic retrieval study motivates competing-skill
tests.

### Example 4: turn security research into an installation gate

Weak:

```text
Install the popular skill because the repository has many stars.
```

Improved guide example:

```text
Preview SKILL.md, references, scripts, and dependencies before installation.
Record the reviewed commit SHA.
Keep shell approval interactive unless the exact script and its inputs were reviewed.
```

GitHub's installation warning supports preview and pinning. Security research
supports reviewing hidden resources and avoiding broad standing approval.
