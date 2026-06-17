# Awesome Agent Operating Systems

[![Validate](https://github.com/frankxai/awesome-agent-operating-systems/actions/workflows/validate.yml/badge.svg)](https://github.com/frankxai/awesome-agent-operating-systems/actions/workflows/validate.yml)
[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![License: CC0](https://img.shields.io/badge/License-CC0-lightgrey.svg)](LICENSE)

A curated public index of agent operating systems, coding agents, MCP ecosystems, orchestration frameworks, memory layers, deployment surfaces, and managed-agent offerings.

This is an independent index. It does not claim ownership of Hermes Agent, OpenClaw, DeepAgents, Claude Code, Codex, LiteLLM, or any listed project.

## Companion Guides

- [Agentic Architecture Field Guide](https://github.com/frankxai/agentic-architecture-field-guide) - vendor-neutral "when to use what" architecture guide.
- [Starlight Agent Army Architecture](https://github.com/frankxai/starlight-agent-army-architecture) - Starlight-specific implementation playbook.
- [Awesome Hermes Agents](https://github.com/frankxai/awesome-hermes-agents) - Hermes-specific resources.

## Contents

- [Local Agent Runtimes](#local-agent-runtimes)
- [Coding Agents](#coding-agents)
- [Orchestration And Agent Harnesses](#orchestration-and-agent-harnesses)
- [MCP And Tool Protocols](#mcp-and-tool-protocols)
- [Skills, Rules, And Prompts](#skills-rules-and-prompts)
- [Memory And Provenance](#memory-and-provenance)
- [Dashboards And Cockpits](#dashboards-and-cockpits)
- [Safety And Evaluation](#safety-and-evaluation)
- [Deployment](#deployment)
- [Managed Offerings And Platforms](#managed-offerings-and-platforms)

## Local Agent Runtimes

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) - local-first agent by Nous Research with profiles, tools, and a durable kanban-style multi-agent board.
- [OpenClaw](https://github.com/openclaw/openclaw) - self-hosted gateway connecting chat apps and channel plugins to coding agents.
- [Deep Agents Code](https://docs.langchain.com/oss/python/deepagents/code/overview) - terminal coding agent built on the DeepAgents SDK.
- [Starlight Swarm](https://github.com/frankxai/starlight-swarm) - Starlight dashboard and audit surface for local swarms.

## Coding Agents

- [Codex](https://developers.openai.com/codex/) - OpenAI coding agent across CLI, app, cloud, GitHub, rules, skills, hooks, MCP, and worktrees.
- [Claude Code](https://code.claude.com/docs/) - Anthropic coding agent with CLAUDE.md, skills, MCP, subagents, and team workflows.
- [Aider](https://github.com/Aider-AI/aider) - terminal pair-programming agent.
- [OpenHands](https://github.com/All-Hands-AI/OpenHands) - open-source software development agent platform.
- [Continue](https://github.com/continuedev/continue) - open-source AI code assistant and IDE extension platform.

## Orchestration And Agent Harnesses

- [DeepAgents](https://github.com/langchain-ai/deepagents) - LangChain's batteries-included agent harness.
- [LangGraph](https://github.com/langchain-ai/langgraph) - graph runtime for durable agent workflows.
- [AutoGen](https://github.com/microsoft/autogen) - Microsoft framework for multi-agent applications.
- [CrewAI](https://github.com/crewAIInc/crewAI) - role-based multi-agent orchestration framework.
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) - SDK for building agentic systems.

## MCP And Tool Protocols

- [Model Context Protocol](https://modelcontextprotocol.io/) - open protocol for connecting agents to tools and data.
- [MCP servers](https://github.com/modelcontextprotocol/servers) - reference and community MCP servers.
- [mcp-doctor](https://github.com/frankxai/mcp-doctor) - local MCP and agent-environment audit tool.

## Skills, Rules, And Prompts

- [Claude Code skills](https://code.claude.com/docs/) - reusable workflows for Claude Code.
- [Codex skills, rules, hooks, and AGENTS.md](https://developers.openai.com/codex/) - repo and user-level operating instructions for Codex.
- [Starlight Agent Skills](https://github.com/frankxai/starlight-agent-skills) - Starlight-specific skill library.
- [Claude Skills Library](https://github.com/frankxai/claude-skills-library) - Claude-oriented skill patterns.

## Memory And Provenance

- [Letta](https://github.com/letta-ai/letta) - stateful agent memory platform.
- [Zep](https://www.getzep.com/) - memory layer for AI agents.
- [Mem0](https://github.com/mem0ai/mem0) - memory layer for personalized agents.
- [Starlight Intelligence System](https://github.com/frankxai/Starlight-Intelligence-System) - Starlight memory, provenance, health, and operating substrate.

## Dashboards And Cockpits

- [Hermes Cockpit](https://github.com/frankxai/hermes-cockpit) - local operator cockpit for Hermes profiles.
- [Deep Agents UI](https://github.com/langchain-ai/deep-agents-ui) - UI for DeepAgents workflows.
- [Starlight Command Center](https://github.com/frankxai/starlight-command-center) - Starlight command surface.

## Safety And Evaluation

- [OpenAI Evals](https://github.com/openai/evals) - evaluation framework.
- [LangSmith](https://www.langchain.com/langsmith) - observability and evaluation for agent runs.
- [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) - evaluation framework for large language models.

## Deployment

- [Vercel](https://vercel.com/docs) - web apps, APIs, workflows, storage, AI SDK, and deployment previews.
- [Railway](https://docs.railway.com/) - always-on services, containers, and simple managed infrastructure.
- [Cloudflare Workers](https://developers.cloudflare.com/workers/) - edge compute, Workers, Durable Objects, and static docs/apps.
- [LiteLLM](https://github.com/BerriAI/litellm) - model gateway, proxy, and provider routing layer.

## Managed Offerings And Platforms

- [Higgsfield](https://higgsfield.ai/) - managed creative AI platform; include here as a managed AI offering, not as a Hermes-based system unless upstream states that.
- [Vercel v0](https://v0.dev/) - managed UI/app generation surface.
- [Replit Agent](https://replit.com/ai) - managed agentic app-building environment.
- [Cursor](https://cursor.com/) - managed AI code editor.
- [Cognition Devin](https://devin.ai/) - managed software engineering agent.

## Contribution Rules

- Prefer official docs, GitHub repositories, or project-owned pages.
- Say what the project is good for; do not imply endorsement or ownership.
- Separate local-first runtimes from managed SaaS offerings.
- Keep Starlight opinions in the companion playbook, not in this neutral index.
