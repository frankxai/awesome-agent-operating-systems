# Awesome Agent Operating Systems

A researched index of agent operating systems, coding-agent runtimes, MCP, memory, orchestration, and deployment tools for AI agents in 2026.

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> Live URLs checked **2026-08-16**. Skills for those runtimes live in [awesome-hermes-agent-skills](https://github.com/frankxai/awesome-hermes-agent-skills).

---

## Earned skills (when the OS is not enough)

| Pack | Job |
| --- | --- |
| [agentskills/agentskills](https://github.com/agentskills/agentskills) | Portable `SKILL.md` spec |
| [obra/superpowers](https://github.com/obra/superpowers) | TDD, debug, review methodology |
| [garrytan/gstack](https://github.com/garrytan/gstack) | Product / design / QA operating loops |
| [anthropics/skills](https://github.com/anthropics/skills) | Official named examples |
| [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) | Scan a skill before install |

Do not treat a 1,000-skill catalog as an operating system. Safety gate: [QUALITY-AND-SAFETY.md](https://github.com/frankxai/awesome-hermes-agent-skills/blob/main/docs/QUALITY-AND-SAFETY.md).

## Contents

- [Agent Runtimes](#agent-runtimes)
- [Coding Agent IDEs](#coding-agent-ides)
- [Model Context Protocol (MCP)](#model-context-protocol-mcp)
- [Memory Systems](#memory-systems)
- [Orchestration Frameworks](#orchestration-frameworks)
- [Evaluation Harnesses](#evaluation-harnesses)
- [Deployment & Execution](#deployment--execution)
- [Agent Development Tools](#agent-development-tools)

---

## Agent Runtimes

Agent runtimes provide the execution loop, tool calling, and context management that power autonomous agents.

- **[Claude Code](https://code.claude.com/docs/en/agent-sdk/overview)** - Anthropic's reusable agent runtime with autonomous loop, context compaction, and MCP integration. Powers Claude Code CLI and Xcode integration. *Checked: 2026-08-16*

- **[OpenAI Codex](https://github.com/openai/codex)** - OpenAI's coding agent for terminal, desktop, and IDE. Parallel agents, MCP support, and cloud environments. Available via ChatGPT Plus/Pro. *Checked: 2026-08-16*

- **[Hermes Agent](https://hermes-agent.org/)** - Open-source persistent agent by Nous Research with learning loop, skill creation, and multi-platform messaging (Telegram, Discord, Slack). MIT licensed, runs on-prem. *Checked: 2026-08-16*

- **[OpenCode](https://opencode.ai/)** - Open-source terminal/desktop coding agent. Model-agnostic, LSP-enabled, supports 75+ LLM providers. 195k+ GitHub stars. *Checked: 2026-08-16*

- **[Replit Agent 4](https://replit.com/products/agent)** - Multi-artifact agent that builds web apps, mobile apps, and slides with parallel task execution and design canvas. Integrated testing via reflection loop. *Checked: 2026-08-16*

- **[Vercel Eve](https://vercel.com/eve)** - Framework for durable backend agents on Vercel. File-based agent authoring with instructions.md, tools/, and skills/ directories. *Checked: 2026-08-16*

---

## Coding Agent IDEs

IDEs and editors with built-in agentic capabilities.

- **[Cursor](https://www.cursor.com/)** - Agentic IDE built on VS Code. Agent Mode, background agents, parallel agents in cloud VMs. Plan/Debug/Design modes. MCP native. *Checked: 2026-08-16*

- **[Windsurf (Devin Desktop)](https://devin.ai/desktop)** - AI-native code editor with Cascade agent. Plan-then-execute architecture, semantic codebase indexing, autonomous terminal execution. Acquired by Cognition AI. *Checked: 2026-08-16*

- **[Aider](https://aider.chat/)** - Open-source terminal AI pair programmer. Git-native, model-agnostic (200+ LLMs), surgical diff edits with auto-commit. Apache-2.0 licensed. *Checked: 2026-08-16*

---

## Model Context Protocol (MCP)

MCP is the standard for connecting agents to external data sources and tools.

- **[MCP Registry](https://registry.modelcontextprotocol.io/)** - Official centralized registry for MCP servers. REST API for discovery, namespace verification via GitHub/DNS. 10k+ active servers. *Checked: 2026-08-16*

- **[MCP Specification](https://modelcontextprotocol.io/)** - Open protocol for connecting AI systems to data sources. Backed by Anthropic, GitHub, Microsoft. *Checked: 2026-08-16*

---

## Memory Systems

Memory layers enable agents to persist context across sessions.

- **[Mem0](https://mem0.ai/)** - Managed AI memory layer with token-efficient retrieval. Hybrid search (semantic + BM25 + entity). Benchmarked on LoCoMo, LongMemEval, BEAM. SOC 2, HIPAA compliant. *Checked: 2026-08-16*

- **[Engram](https://pubdb.com/paper/2606.09900)** - Open-source bi-temporal memory engine. Dual-process with async fact extraction and provenance chains. 83.6% on LongMemEval_S (vs 73.2% full-context baseline). *Checked: 2026-08-16*

- **[SYNAPSE](https://aclanthology.org/2026.findings-acl.1108.pdf)** - Episodic-semantic memory via spreading activation. Dynamic graph traversal, lateral inhibition, temporal decay. Outperforms SOTA on LoCoMo multi-hop reasoning. *Checked: 2026-08-16*

---

## Orchestration Frameworks

Frameworks for building and coordinating multi-agent systems.

- **[LangGraph](https://github.com/langchain-ai/langgraph)** - Production-grade stateful agent orchestration from LangChain. Directed cyclic graphs, checkpointing, human-in-the-loop. Industry standard for complex workflows. *Checked: 2026-08-16*

- **[CrewAI](https://github.com/crewaiinc/crewai/)** - Open-source Python framework for role-based agent teams. Crews (autonomous collaboration) + Flows (event-driven control). Fast prototyping for content and research. *Checked: 2026-08-16*

- **[AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)** - Autonomous agent platform with free-form loops. Research-focused, prioritizes autonomy over deterministic control. 165k+ GitHub stars. *Checked: 2026-08-16*

- **[Microsoft AutoGen / AG2](https://github.com/microsoft/autogen)** - Conversational multi-agent framework. Role-based GroupChat coordination for Azure environments. *Checked: 2026-08-16*

---

## Evaluation Harnesses

Benchmarks and tools for measuring agent performance.

- **[SWE-bench](https://www.swebench.com/)** - Standard for software engineering agents. 500 human-validated GitHub issues from Python repos. Top models reach ~80% on Verified, 58% on Pro. *Checked: 2026-08-16*

- **[GAIA](https://huggingface.co/gaia-benchmark)** - General AI assistant benchmark. 466 questions requiring reasoning, tool use, and multi-modality. 30-50 point gap between bare models and scaffolded systems. *Checked: 2026-08-16*

- **[Paean Harness](https://github.com/paean-ai/paean-harness)** - Framework-agnostic evaluation runner supporting SWE-bench, GAIA, USACO, AppWorld, tau-bench. Local or cloud execution with parallelization. *Checked: 2026-08-16*

- **[OSWorld](https://os-world.github.io/)** - Desktop computer-use benchmark for real OS-level tasks. 82.6% top score as of mid-2026. *Checked: 2026-08-16*

- **[Terminal-Bench](https://github.com/HarnessFix/HarnessFix)** - Linux CLI and infrastructure task benchmark for measuring shell automation capabilities. *Checked: 2026-08-16*

---

## Deployment & Execution

Platforms for running agents in production.

- **[Vercel](https://vercel.com/)** - Agentic infrastructure with Eve framework, Sandbox (secure microVMs), and AI Gateway (200+ models). Native for Next.js workflows. *Checked: 2026-08-16*

- **[Railway](https://railway.com/)** - Stateful backend hosting with MCP server for agent-driven deployment, env management, and logs. Managed Postgres/Redis/MySQL on private network. *Checked: 2026-08-16*

- **[Modal](https://modal.com/)** - Serverless Python execution with GPU support. gVisor sandboxing, container-based isolation. Ideal for ML/AI workloads. *Checked: 2026-08-16*

- **[E2B](https://e2b.dev/)** - Secure sandboxed environments for code execution. Firecracker microVMs, 24h sessions, native in OpenAI Agents SDK. Used by 88% of Fortune 100 for agentic workflows. *Checked: 2026-08-16*

- **[Fly.io](https://fly.io/)** - Multi-region container orchestration. Edge deployment, low-latency global distribution. *Checked: 2026-08-16*

- **[Render](https://render.com/)** - Unified cloud with static sites, web services, databases. Flat pricing, automatic deploys from Git. *Checked: 2026-08-16*

---

## Agent Development Tools

Tools and resources for building agents.

- **[frankxai/skills](https://github.com/frankxai/skills)** - AI agent skills for Claude Code, Cursor, and Codex. Install: `npx skills add frankxai/skills` *Checked: 2026-08-16*

- **[Starlight Intelligence System](https://github.com/frankxai/Starlight-Intelligence-System)** - Sovereign AI substrate for memory, orchestration, skills, and governance across multiple agent platforms. *Checked: 2026-08-16*

- **[Agent Client Protocol (ACP)](https://devin.ai/desktop)** - Protocol for multi-model, multi-agent interoperability in Devin Desktop (formerly Windsurf). *Checked: 2026-08-16*

---

## Contributing

Contributions welcome! Please ensure:

1. URLs are live and verified as of your submission date
2. Include a one-line description of why the tool matters
3. Add the date you verified the link (format: YYYY-MM-DD)
4. No marketing fluff or unverified claims
5. Open a pull request with your addition

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines.

---

## License

This list is dedicated to the public domain under [CC0 1.0](./LICENSE).

<div align="center">
  <sub>A researched index for AI architects building production agent systems.</sub>
</div>
