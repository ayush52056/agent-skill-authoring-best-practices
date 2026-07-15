# Evidence Map

This file connects the repository's recommendations to public evidence. It
separates portable requirements from vendor behavior and distinguishes measured
results from practitioner judgment.

Last reviewed: 2026-07-15.

## Evidence levels

- **Required:** part of the open format or a named host's documented contract.
- **Strong:** repeated across official guidance and production implementations.
- **Empirical:** supported by a published evaluation. Scope is limited to that study.
- **Practice:** credible production or senior-practitioner experience, but not universal.
- **Experimental:** promising pattern that should be evaluated locally before adoption.

## Practice-to-source map

| Practice | Level | Main evidence | Qualification |
|---|---|---|---|
| Use a directory with `SKILL.md`, `name`, and `description` | Required | [Agent Skills specification](https://agentskills.io/specification), [OpenAI](https://learn.chatgpt.com/docs/build-skills), [Anthropic](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), [GitHub](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) | Optional frontmatter differs by host. |
| Put capability and trigger conditions in `description` | Strong | [OpenAI](https://learn.chatgpt.com/docs/build-skills), [Anthropic authoring guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [GitHub](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) | Body-only trigger sections cannot help initial selection. |
| Front-load distinctive trigger terms | Strong | [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills), [Matt Pocock](https://raw.githubusercontent.com/mattpocock/skills/main/skills/productivity/writing-great-skills/SKILL.md) | Particularly important when a host truncates catalog descriptions. |
| Evaluate positive, negative, and near-miss triggers | Strong | [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md), [Phil Schmid](https://www.philschmid.de/agent-skills-tips), [Trail of Bits](https://www.mintlify.com/trailofbits/skills/contributing/skill-authoring) | Use realistic prompts, not obviously irrelevant negatives. |
| Choose implicit or explicit invocation deliberately | Practice | [OpenAI optional metadata](https://learn.chatgpt.com/docs/build-skills), [Matt Pocock](https://raw.githubusercontent.com/mattpocock/skills/main/skills/productivity/writing-great-skills/SKILL.md), [Thoughtworks](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html) | Field names are host-specific. The design decision is portable. |
| Keep each skill focused and the installed catalog curated | Strong + Empirical | [OpenAI](https://learn.chatgpt.com/docs/build-skills), [SkillsBench](https://arxiv.org/abs/2602.12670), [realistic retrieval study](https://arxiv.org/abs/2604.04323) | SkillsBench found focused packages more effective. Large noisy retrieval pools reduced gains. |
| Prefer progressive disclosure over monolithic documentation | Strong + Empirical | [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices), [Anthropic](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [SkillsBench](https://arxiv.org/abs/2602.12670) | Link resources directly from `SKILL.md` and say when to load them. |
| Write processes, decisions, and completion criteria instead of essays | Strong | [OpenAI](https://learn.chatgpt.com/docs/build-skills), [Addy Osmani](https://addyosmani.com/blog/agent-skills/), [Trail of Bits](https://www.mintlify.com/trailofbits/skills/contributing/skill-authoring) | Reference-only skills are valid when the reference itself changes behavior. |
| Match prescriptiveness to task risk | Strong | [Anthropic](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [Trail of Bits](https://www.mintlify.com/trailofbits/skills/contributing/skill-authoring), [Phil Schmid](https://www.philschmid.de/agent-skills-tips) | Fragile ordering belongs in scripts when possible. |
| Provide concrete examples and output templates when format matters | Strong | [Anthropic](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [Trail of Bits](https://www.mintlify.com/trailofbits/skills/contributing/skill-authoring) | Examples must not overfit the skill to one fixture. |
| Explain consequential constraints and tradeoffs | Practice | [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md), [Phil Schmid](https://www.philschmid.de/agent-skills-tips), [Trail of Bits](https://www.mintlify.com/trailofbits/skills/contributing/skill-authoring) | Omit explanations that do not change decisions. |
| Use scripts for deterministic, repeated, or fragile operations | Strong | [OpenAI](https://learn.chatgpt.com/docs/build-skills), [Anthropic](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [GitHub](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) | Instruction-only should remain the default. |
| Use structured intermediate artifacts for high-risk operations | Practice | [Anthropic plan-validate-execute guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Most useful for batch, destructive, or complex transformations. |
| Build evaluations before extensive instructions | Strong + Empirical | [Anthropic](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [SkillsBench](https://arxiv.org/abs/2602.12670) | Self-generated skills showed no average benefit in SkillsBench. Human curation and verification remain necessary. |
| Compare against a no-skill baseline | Empirical | [SkillsBench](https://arxiv.org/abs/2602.12670), [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | Some benchmark tasks became worse with a skill, so presence alone is not evidence of value. |
| Run repeated, isolated trials and retain held-out cases | Practice | [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md), [Phil Schmid](https://www.philschmid.de/agent-skills-tips) | Scale trial count to risk and cost. |
| Test outcomes and behavior-constraint coverage | Empirical | [Skill Coverage](https://arxiv.org/abs/2606.20659) | Passing one task does not show that every important branch or instruction was exercised. |
| Test every supported model and host | Strong | [Anthropic](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [GitHub SDK guidance](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/skills) | Prompt interpretation and supported metadata differ across hosts. |
| Retire skills that no longer improve the baseline | Practice + Empirical | [Phil Schmid](https://www.philschmid.de/agent-skills-tips), [SkillsBench](https://arxiv.org/abs/2602.12670) | Re-test capability skills after major model or tool upgrades. |
| Treat skills as executable supply-chain dependencies | Strong + Empirical | [GitHub security warning](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills), [security study](https://arxiv.org/abs/2601.10338), [prompt-injection study](https://arxiv.org/abs/2510.26328) | Review instructions, references, scripts, dependencies, permissions, and updates. |
| Record provenance, pin reviewed revisions, and verify artifacts | Strong | [GitHub CLI skill provenance](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills), [NVIDIA verified skills](https://github.com/NVIDIA/skills), [Cloudflare discovery RFC](https://github.com/cloudflare/agent-skills-discovery-rfc) | Signing proves origin and integrity, not usefulness or safety. |
| Use anti-rationalization rebuttals only for observed critical shortcuts | Practice | [Addy Osmani](https://addyosmani.com/blog/agent-skills/), [Trail of Bits](https://www.mintlify.com/trailofbits/skills/contributing/skill-authoring) | Overuse adds noise and rigidity. Mechanical gates are stronger. |
| Use router skills only when composition earns its routing cost | Experimental | [Matt Pocock](https://raw.githubusercontent.com/mattpocock/skills/main/skills/productivity/writing-great-skills/SKILL.md), [Addy Osmani](https://addyosmani.com/blog/agent-skills/), [Minko Gechev](https://github.com/mgechev/skills-best-practices) | Large routers can recreate the context and retrieval problems skills are meant to solve. |

## Documented disagreements

### Numbered procedures versus outcome constraints

Some production guides favor chronological numbered workflows. Others warn that
over-prescription prevents adaptation. The repository resolves this by requiring
ordered steps only where order, branching, or checkpoints matter. Otherwise,
state the outcome, constraints, and validation. Move truly fragile sequences to
a deterministic script.

### Trigger exclusions in metadata versus the body

Official routing behavior makes `description` the only reliable pre-activation
place for trigger boundaries. Some security teams also repeat “When NOT to Use”
inside the body as an operational reminder. Repetition is justified only when it
changes behavior after activation. It does not repair a bad routing description.

### Aggressive automatic invocation versus manual invocation

Some frameworks intentionally make descriptions “pushy” to counter
under-triggering. Other practitioners prefer user-invoked skills to eliminate
catalog context and accidental activation. Choose from measured routing results,
workflow risk, and whether autonomous discovery is actually required.

### Router skills

Routers can reduce the human memory burden of many manual skills and coordinate
multi-stage workflows. They also add another selection layer and can become
monolithic. Adopt one only after direct descriptions or explicit invocation have
failed at the required scale.

## Research limitations

- Agent Skills are a young ecosystem. Most empirical studies were published in 2026.
- Results depend on model, harness, task, catalog, and verifier quality.
- Repository popularity and install count are discovery signals, not quality evidence.
- Automated smell and vulnerability detectors have false positives and negatives.
- A recommendation remains provisional until it improves the target skill's own evaluations.
