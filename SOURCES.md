# Sources

This repository synthesizes guidance rather than copying any single source.
Primary standards and official implementations carry the most weight.
practitioner guidance and research are used to refine or challenge them.

Last reviewed: 2026-07-15.

## Research method and coverage

This is a systematic high-signal review, not a claim that every webpage or
GitHub repository on the internet has been read. Discovery covered:

- the open specification and official host documentation.
- first-party and widely used production skill repositories.
- senior engineers' implementation notes, talks, and authoring guides.
- empirical benchmark, maintenance, smell, retrieval, and security research.
- adjacent context-engineering and harness practices that transfer to skills.

A source is included when it contributes a portable requirement, a documented
host behavior, a reproducible implementation pattern, measured evidence, or a
clearly labeled tradeoff. Stars, search rank, and repetition are not sufficient.
Recommendations are mapped to their strongest supporting evidence in
[the evidence map](docs/evidence-map.md). Disagreements and study limitations are
preserved instead of averaged into false consensus.

## Open standard and official documentation

- [Agent Skills specification](https://agentskills.io/specification)
- [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices)
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI skills repository](https://github.com/openai/skills)
- [Anthropic: Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Anthropic: Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Anthropic skills repository](https://github.com/anthropics/skills)
- [GitHub Copilot: Add Agent Skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
- [GitHub Copilot SDK: Agent Skills](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/skills)
- [Microsoft Agent Framework: Agent Skills](https://learn.microsoft.com/en-us/agent-framework/agents/skills)
- [Cursor 2.4: Agent Skills](https://cursor.com/changelog/2-4)
- [Cursor: Agent best practices](https://cursor.com/blog/agent-best-practices)

## Production repositories

- [Google Gemini CLI skills](https://github.com/google-gemini/gemini-skills)
- [GitHub Awesome Copilot](https://github.com/github/awesome-copilot)
- [Microsoft Agent Skills](https://github.com/MicrosoftDocs/Agent-Skills)
- [NVIDIA skills](https://github.com/NVIDIA/skills)
- [NVIDIA SkillSpector](https://github.com/nvidia/skillspector)
- [Cloudflare skills](https://github.com/cloudflare/skills)
- [Cloudflare Agent Skills discovery RFC](https://github.com/cloudflare/agent-skills-discovery-rfc)
- [Vercel agent skills](https://github.com/vercel-labs/agent-skills)
- [Trail of Bits skills](https://github.com/trailofbits/skills)

## Practitioner implementations and writing

- [Matt Pocock: skills](https://github.com/mattpocock/skills)
- [Matt Pocock: Writing great skills](https://raw.githubusercontent.com/mattpocock/skills/main/skills/productivity/writing-great-skills/SKILL.md)
- [Jesse Vincent: Superpowers](https://github.com/obra/superpowers)
- [Jesse Vincent: Skills for Claude](https://blog.fsck.com/2025/10/16/skills-for-claude/)
- [Addy Osmani: Agent Skills](https://addyosmani.com/blog/agent-skills/)
- [Phil Schmid: 8 tips for writing effective Agent Skills](https://www.philschmid.de/agent-skills-tips)
- [Trail of Bits: Skill authoring guide](https://www.mintlify.com/trailofbits/skills/contributing/skill-authoring)
- [Minko Gechev: Skills best practices](https://github.com/mgechev/skills-best-practices)
- [Simon Willison: Agentic engineering patterns](https://simonwillison.net/guides/agentic-engineering-patterns/)
- [Thoughtworks: Context Engineering for Coding Agents](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html)
- [Thoughtworks: Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html)
- [Thoughtworks: Sensors for coding agents](https://martinfowler.com/articles/sensors-for-coding-agents.html)

## Empirical and security research

- [SkillsBench: Benchmarking how well agent skills work](https://arxiv.org/abs/2602.12670)
- [Skill Coverage: Measuring and improving instruction coverage](https://arxiv.org/abs/2606.20659)
- [How Well Do Agentic Skills Work in the Wild?](https://arxiv.org/abs/2604.04323)
- [SkillLearnBench](https://arxiv.org/abs/2604.20087)
- [From Anatomy to Smells: An Empirical Study of SKILL.md in Agent Skills](https://arxiv.org/abs/2607.01456)
- [From Registry to Repository: How AI Agent Skills Are Written, Adapted, and Maintained](https://arxiv.org/abs/2607.00911)
- [Security at Scale: An Empirical Study of Agent Skills](https://arxiv.org/abs/2601.10338)
- [Prompt Injection Attacks on Agent Skills](https://arxiv.org/abs/2510.26328)
- [Under the Hood of SKILL.md: Semantic Supply-chain Attacks on AI Agent Skill Registry](https://arxiv.org/abs/2605.11418)

## Evidence policy

- Prefer specifications and official documentation for compatibility claims.
- Prefer executable examples and measured evaluations for effectiveness claims.
- Treat stars, registry rank, anecdotes, and social-media consensus as discovery signals only.
- Label host-specific behavior instead of presenting it as a portable requirement.
- Record consequential claims in [the evidence map](docs/evidence-map.md) with a
  confidence level and qualification. A source list alone is not traceability.
- Preserve disagreements when evidence supports different choices under
  different risk, routing, or task conditions.
- Revisit guidance as agents, routing behavior, and the open specification evolve.
