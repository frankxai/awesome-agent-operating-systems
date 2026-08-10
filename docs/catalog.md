# Agentic Tech Catalog

Snapshot: **2026-08-10T20:10:10.676305Z** · **182** projects at or above 10,000 stars · **5** strategic exceptions · **30** categories.

> Stars are a discovery filter, not a quality or adoption score. `NOASSERTION` and `OTHER` license values are not treated as verified open-source licenses and require manual review before reuse or deployment.

The machine-readable source is [`data/projects.json`](../data/projects.json); regenerate with `python scripts/refresh_catalog.py && python scripts/render_catalog.py`.

## Categories

- [control-plane](#control-plane) (5)
- [coding-control-plane](#coding-control-plane) (7)
- [interaction-ui](#interaction-ui) (2)
- [agent-runtime](#agent-runtime) (8)
- [coding-agent](#coding-agent) (16)
- [agent-framework](#agent-framework) (19)
- [agent-builder](#agent-builder) (5)
- [structured-output](#structured-output) (2)
- [agent-training](#agent-training) (3)
- [durable-execution](#durable-execution) (7)
- [workflow-automation](#workflow-automation) (4)
- [protocol](#protocol) (10)
- [tools-integration](#tools-integration) (5)
- [memory](#memory) (6)
- [knowledge-graph](#knowledge-graph) (4)
- [rag-platform](#rag-platform) (4)
- [vector-database](#vector-database) (2)
- [document-ingestion](#document-ingestion) (8)
- [eval-security](#eval-security) (4)
- [observability](#observability) (6)
- [sandbox-security](#sandbox-security) (4)
- [identity-secrets](#identity-secrets) (3)
- [browser-computer-use](#browser-computer-use) (9)
- [model-gateway](#model-gateway) (2)
- [model-runtime](#model-runtime) (11)
- [voice-realtime](#voice-realtime) (3)
- [creative-media](#creative-media) (4)
- [data-integration](#data-integration) (1)
- [domain-platform](#domain-platform) (4)
- [rust-runtime](#rust-runtime) (19)

## control-plane

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [lobehub/lobehub](https://github.com/lobehub/lobehub) | 80,426 | TypeScript | NOASSERTION ⚠ review | `evaluate` | Chief-agent-operator UX and always-on agent team surface. |
| [paperclipai/paperclip](https://github.com/paperclipai/paperclip) | 74,039 | TypeScript | MIT | `pilot` | Company-level orchestration, goals, budgets, approvals, issue checkout and native Hermes adapters. |
| [ruvnet/ruflo](https://github.com/ruvnet/ruflo) | 64,839 | TypeScript | MIT | `evaluate` | Meta-harness for swarms, adaptive memory and multi-agent coordination. |
| [multica-ai/multica](https://github.com/multica-ai/multica) | 40,914 | Go | NOASSERTION ⚠ review | `evaluate` | Managed coding-agent teammates with task and skill compounding surfaces. |
| [simstudioai/sim](https://github.com/simstudioai/sim) | 29,124 | TypeScript | Apache-2.0 | `evaluate` | Visual deployment and orchestration layer for agent workforces. |

## coding-control-plane

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) | 67,632 | TypeScript | NOASSERTION ⚠ review | `evaluate` | High-signal meta-harness for complex codebases on Codex and OpenCode; absorb hooks, planning, and verified-completion patterns without replacing Hermes Queen. |
| [openai/symphony](https://github.com/openai/symphony) | 26,010 | Elixir | Apache-2.0 | `evaluate` | Isolated autonomous implementation runs driven by project work. |
| [stablyai/orca](https://github.com/stablyai/orca) | 21,068 | TypeScript | MIT | `evaluate` | Agent development environment for fleets across desktop and mobile. |
| [gastownhall/gastown](https://github.com/gastownhall/gastown) | 17,077 | Go | MIT | `evaluate` | Go multi-agent workspace manager. |
| [superset-sh/superset](https://github.com/superset-sh/superset) | 12,475 | TypeScript | NOASSERTION ⚠ review | `evaluate` | Desktop code editor for parallel coding-agent armies. |
| [humanlayer/humanlayer](https://github.com/humanlayer/humanlayer) | 11,123 | TypeScript | NOASSERTION ⚠ review | `evaluate` | Human-in-the-loop workflows for hard coding-agent tasks. |
| [getpaseo/paseo](https://github.com/getpaseo/paseo) | 10,585 | TypeScript | NOASSERTION ⚠ review | `watch` | Multi-coding-agent orchestration across desktop and mobile. |

## interaction-ui

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [open-webui/open-webui](https://github.com/open-webui/open-webui) | 145,770 | Python | NOASSERTION ⚠ review | `benchmark` | Widely adopted self-hosted human interface for models and agent tools. |
| [danny-avila/LibreChat](https://github.com/danny-avila/LibreChat) | 40,863 | TypeScript | MIT | `evaluate` | Multi-user self-hosted chat, agents, MCP, tools and authentication surface. |

## agent-runtime

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [openclaw/openclaw](https://github.com/openclaw/openclaw) | 383,276 | TypeScript | NOASSERTION ⚠ review | `benchmark` | Largest personal-agent/runtime ecosystem and gateway reference. |
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | 216,395 | Python | MIT | `adopt-core` | Personal execution runtime, memory, skills, tools, gateways, cron and delegation. |
| [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) | 185,586 | Python | NOASSERTION ⚠ review | `benchmark` | Historically influential autonomous-agent platform and current architecture benchmark. |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 77,287 | Python | MIT | `evaluate` | Long-horizon super-agent with sandbox, memory, tools, skills and gateway. |
| [HKUDS/nanobot](https://github.com/HKUDS/nanobot) | 45,816 | Python | MIT | `watch` | Lightweight multi-channel agent runtime. |
| [elizaOS/eliza](https://github.com/elizaOS/eliza) | 18,756 | TypeScript | MIT | `watch` | Plugin-oriented agent OS and community ecosystem. |
| [agent0ai/agent-zero](https://github.com/agent0ai/agent-zero) | 18,444 | Python | NOASSERTION ⚠ review | `watch` | General-purpose autonomous agent framework. |
| [HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness) | 14,882 | Python | MIT | `watch` | Open agent harness with personal-agent layer. |

## coding-agent

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [anomalyco/opencode](https://github.com/anomalyco/opencode) | 186,893 | TypeScript | MIT | `adopt-core` | Provider-neutral open coding agent and ACP/MCP benchmark. |
| [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | 106,035 | TypeScript | Apache-2.0 | `adopt-core` | Gemini terminal agent and large-context worker. |
| [openai/codex](https://github.com/openai/codex) | 99,131 | Rust | Apache-2.0 | `adopt-core` | Rust coding agent and primary implementation worker. |
| [earendil-works/pi](https://github.com/earendil-works/pi) | 86,599 | TypeScript | MIT | `evaluate` | Unified LLM API + agent loop + TUI coding CLI toolkit; source lineage for several modern terminal harnesses. |
| [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | 81,106 | Python | NOASSERTION ⚠ review | `evaluate` | End-to-end software-development agent with sandboxed execution and operator UI. |
| [cline/cline](https://github.com/cline/cline) | 64,743 | TypeScript | Apache-2.0 | `evaluate` | IDE, CLI and SDK coding-agent surface. |
| [Aider-AI/aider](https://github.com/Aider-AI/aider) | 47,462 | Python | Apache-2.0 | `evaluate` | Mature terminal pair-programming agent with strong Git integration. |
| [continuedev/continue](https://github.com/continuedev/continue) | 34,937 | TypeScript | Apache-2.0 | `evaluate` | Open coding agent with IDE integration. |
| [charmbracelet/crush](https://github.com/charmbracelet/crush) | 26,592 | Go | NOASSERTION ⚠ review | `watch` | Go terminal coding agent with strong local UX. |
| [Kilo-Org/kilocode](https://github.com/Kilo-Org/kilocode) | 26,332 | TypeScript | MIT | `watch` | Multi-surface agentic engineering platform. |
| [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) | 26,084 | TypeScript | Apache-2.0 | `evaluate` | Open terminal coding agent and model-diversity lane. |
| [can1357/oh-my-pi](https://github.com/can1357/oh-my-pi) | 23,575 | TypeScript | MIT | `evaluate` | Terminal coding harness with hash-anchored edits, LSP, subagents and browser; useful architecture benchmark for edit safety. |
| [SWE-agent/SWE-agent](https://github.com/SWE-agent/SWE-agent) | 19,839 | Python | MIT | `benchmark` | Issue-to-patch research agent and SWE-bench architecture reference. |
| [plandex-ai/plandex](https://github.com/plandex-ai/plandex) | 15,532 | Go | MIT | `watch` | Large-project coding agent and planning benchmark. |
| [bytedance/trae-agent](https://github.com/bytedance/trae-agent) | 11,856 | Python | MIT | `watch` | General software-engineering agent. |
| [langchain-ai/open-swe](https://github.com/langchain-ai/open-swe) | 10,323 | Python | MIT | `watch` | Asynchronous coding-agent architecture reference. |

## agent-framework

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | 142,003 | Python | MIT | `benchmark` | Broad agent engineering ecosystem and integrations. |
| [FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT) | 69,413 | Python | MIT | `benchmark` | Software-company multi-agent pattern reference. |
| [microsoft/autogen](https://github.com/microsoft/autogen) | 59,796 | Python | CC-BY-4.0 | `benchmark` | Multi-agent framework and research reference. |
| [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | 55,695 | Python | MIT | `benchmark` | Role-oriented multi-agent orchestration. |
| [run-llama/llama_index](https://github.com/run-llama/llama_index) | 50,913 | Python | MIT | `evaluate` | Document agents, indexing and context engineering. |
| [agno-agi/agno](https://github.com/agno-agi/agno) | 41,208 | Python | Apache-2.0 | `evaluate` | Build, run and manage agent platforms. |
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | 37,515 | Python | MIT | `evaluate` | Durable graph/state-machine execution for agents. |
| [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel) | 28,323 | C# | MIT | `evaluate` | Enterprise multi-language agent and plugin framework. |
| [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | 27,981 | Python | Apache-2.0 | `evaluate` | Observable and trustworthy agent framework. |
| [openai/openai-agents-python](https://github.com/openai/openai-agents-python) | 27,975 | Python | MIT | `evaluate` | Lightweight multi-agent and handoff framework. |
| [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) | 26,375 | Python | MIT | `evaluate` | Batteries-included long-horizon agent harness. |
| [mastra-ai/mastra](https://github.com/mastra-ai/mastra) | 26,294 | TypeScript | NOASSERTION ⚠ review | `evaluate` | Modern TypeScript agent application framework. |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | 25,925 | MDX | Apache-2.0 | `evaluate` | Explicit production pipelines and agent workflows. |
| [openai/swarm](https://github.com/openai/swarm) | 21,805 | Python | MIT | `reference` | Educational handoff/orchestration patterns; not a production foundation. |
| [google/adk-python](https://github.com/google/adk-python) | 20,645 | Python | Apache-2.0 | `evaluate` | Code-first build, evaluate and deploy toolkit. |
| [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) | 18,624 | Python | MIT | `evaluate` | Typed Python agent framework with strong schema discipline. |
| [camel-ai/camel](https://github.com/camel-ai/camel) | 17,414 | Python | Apache-2.0 | `benchmark` | Research-heavy multi-agent framework. |
| [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | 12,184 | Python | MIT | `watch` | Microsoft Python/.NET agent framework successor surface. |
| [The-Pocket/PocketFlow](https://github.com/The-Pocket/PocketFlow) | 10,988 | Python | MIT | `watch` | Minimal framework useful as a complexity baseline. |

## agent-builder

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [langgenius/dify](https://github.com/langgenius/dify) | 149,167 | TypeScript | NOASSERTION ⚠ review | `evaluate` | Production agentic workflow and application platform. |
| [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise) | 54,695 | TypeScript | NOASSERTION ⚠ review | `evaluate` | Visual agent builder. |
| [labring/FastGPT](https://github.com/labring/FastGPT) | 29,014 | TypeScript | NOASSERTION ⚠ review | `watch` | Knowledge, RAG and visual workflow platform. |
| [1Panel-dev/MaxKB](https://github.com/1Panel-dev/MaxKB) | 22,117 | Python | GPL-3.0 | `watch` | Enterprise agent builder. |
| [coze-dev/coze-studio](https://github.com/coze-dev/coze-studio) | 21,185 | TypeScript | Apache-2.0 | `watch` | All-in-one visual agent development platform. |

## structured-output

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [dottxt-ai/outlines](https://github.com/dottxt-ai/outlines) | 14,532 | Python | Apache-2.0 | `evaluate` | Constrained generation and structured-output primitives. |
| [567-labs/instructor](https://github.com/567-labs/instructor) | 13,552 | Python | MIT | `adopt-adjacent` | Typed structured outputs across model providers. |

## agent-training

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [verl-project/verl](https://github.com/verl-project/verl) | 22,517 | Python | Apache-2.0 | `benchmark` | Scalable reinforcement-learning post-training infrastructure. |
| [huggingface/trl](https://github.com/huggingface/trl) | 18,862 | Python | Apache-2.0 | `benchmark` | Widely used transformer reinforcement-learning toolkit. |
| [microsoft/agent-lightning](https://github.com/microsoft/agent-lightning) | 17,395 | Python | MIT | `evaluate` | Agent-agnostic reinforcement-learning and training framework. |

## durable-execution

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [conductor-oss/conductor](https://github.com/conductor-oss/conductor) | 32,007 | Java | Apache-2.0 | `evaluate` | Durable event-driven workflow engine for agentic work. |
| [PrefectHQ/prefect](https://github.com/PrefectHQ/prefect) | 23,417 | Python | Apache-2.0 | `watch` | Python workflow orchestration with strong observability. |
| [temporalio/temporal](https://github.com/temporalio/temporal) | 21,695 | Go | MIT | `evaluate` | Battle-tested durable execution substrate. |
| [windmill-labs/windmill](https://github.com/windmill-labs/windmill) | 17,178 | Rust | NOASSERTION ⚠ review | `evaluate` | Rust-backed scripts, workflows and internal tools. |
| [dagster-io/dagster](https://github.com/dagster-io/dagster) | 15,856 | Python | Apache-2.0 | `watch` | Asset-aware data and automation orchestration. |
| [triggerdotdev/trigger.dev](https://github.com/triggerdotdev/trigger.dev) | 15,677 | TypeScript | Apache-2.0 | `evaluate` | Long-running TypeScript agent jobs and workflows. |
| [hatchet-dev/hatchet](https://github.com/hatchet-dev/hatchet) | 7,518 | Go | MIT | `strategic-exception` | Modern durable task queue with agent workflow fit even if below threshold. |

## workflow-automation

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [n8n-io/n8n](https://github.com/n8n-io/n8n) | 196,830 | TypeScript | NOASSERTION ⚠ review | `adopt-adjacent` | Human-readable business automation and integration fabric; fair-code licensing caveat. |
| [huginn/huginn](https://github.com/huginn/huginn) | 49,631 | Ruby | MIT | `reference` | Long-lived monitor-and-act agent pattern. |
| [activepieces/activepieces](https://github.com/activepieces/activepieces) | 23,309 | TypeScript | NOASSERTION ⚠ review | `evaluate` | Open workflow automation with agents and MCPs. |
| [automatisch/automatisch](https://github.com/automatisch/automatisch) | 13,887 | JavaScript | NOASSERTION ⚠ review | `watch` | Open-source Zapier alternative. |

## protocol

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | 88,587 | TypeScript | NOASSERTION ⚠ review | `adopt-standard` | Reference MCP servers and ecosystem signal. |
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | 26,420 | TypeScript | NOASSERTION ⚠ review | `evaluate` | Open skill installer and distribution conventions. |
| [PrefectHQ/fastmcp](https://github.com/PrefectHQ/fastmcp) | 26,242 | Python | Apache-2.0 | `adopt-standard` | High-level Python framework for MCP servers and clients. |
| [a2aproject/A2A](https://github.com/a2aproject/A2A) | 24,837 | Shell | Apache-2.0 | `adopt-standard` | Agent-to-agent interoperability protocol. |
| [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | 23,644 | Python | MIT | `adopt-standard` | Official Python MCP SDK. |
| [agentskills/agentskills](https://github.com/agentskills/agentskills) | 23,140 | Python | Apache-2.0 | `adopt-standard` | Portable Agent Skills specification. |
| [agentsmd/agents.md](https://github.com/agentsmd/agents.md) | 23,069 | TypeScript | MIT | `adopt-standard` | Portable repository guidance format for coding agents. |
| [ag-ui-protocol/ag-ui](https://github.com/ag-ui-protocol/ag-ui) | 14,789 | TypeScript | MIT | `evaluate` | Agent-to-frontend interaction protocol. |
| [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk) | 12,877 | TypeScript | NOASSERTION ⚠ review | `adopt-standard` | Official TypeScript MCP SDK. |
| [mcp-use/mcp-use](https://github.com/mcp-use/mcp-use) | 10,326 | TypeScript | MIT | `evaluate` | Full-stack MCP application and server framework. |

## tools-integration

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | 47,095 | TypeScript | Apache-2.0 | `adopt-adjacent` | Browser diagnostics and automation for coding agents. |
| [github/github-mcp-server](https://github.com/github/github-mcp-server) | 31,517 | Go | MIT | `adopt-adjacent` | Official GitHub MCP server for repository and delivery operations. |
| [ComposioHQ/composio](https://github.com/ComposioHQ/composio) | 29,269 | TypeScript | MIT | `evaluate` | Large authenticated tool catalog, search and sandboxed workbench. |
| [oraios/serena](https://github.com/oraios/serena) | 26,550 | Python | MIT | `evaluate` | Semantic code retrieval/editing MCP toolkit. |
| [googleapis/mcp-toolbox](https://github.com/googleapis/mcp-toolbox) | 15,970 | Go | Apache-2.0 | `evaluate` | Database MCP server and governance patterns. |

## memory

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | 61,071 | TypeScript | Apache-2.0 | `evaluate` | General agent memory layer. |
| [khoj-ai/khoj](https://github.com/khoj-ai/khoj) | 35,835 | Python | AGPL-3.0 | `evaluate` | Self-hosted second brain, agents and scheduled automation. |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | 26,887 | Python | AGPL-3.0 | `watch` | Context database unifying memory, RAG and skills. |
| [letta-ai/letta](https://github.com/letta-ai/letta) | 23,831 | Python | Apache-2.0 | `evaluate` | Stateful agents and memory architecture. |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | 18,517 | Python | MIT | `evaluate` | Agent memory with learning and consolidation. |
| [MemTensor/MemOS](https://github.com/MemTensor/MemOS) | 10,252 | TypeScript | Apache-2.0 | `watch` | Self-evolving memory OS and cross-task skill reuse. |

## knowledge-graph

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) | 37,768 | Python | MIT | `evaluate` | Simple graph-oriented RAG. |
| [microsoft/graphrag](https://github.com/microsoft/graphrag) | 34,485 | Python | MIT | `evaluate` | Graph-based RAG reference architecture. |
| [getzep/graphiti](https://github.com/getzep/graphiti) | 28,845 | Python | Apache-2.0 | `pilot` | Temporal real-time knowledge graphs for agents. |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | 27,983 | Python | Apache-2.0 | `evaluate` | Self-hosted knowledge-graph memory platform. |

## rag-platform

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | 85,296 | Go | Apache-2.0 | `evaluate` | Document ingestion, RAG and agent context layer. |
| [Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm) | 63,449 | JavaScript | MIT | `watch` | Local-first agent and knowledge workspace. |
| [VectifyAI/PageIndex](https://github.com/VectifyAI/PageIndex) | 34,080 | Python | MIT | `evaluate` | Reasoning-based vectorless document index. |
| [onyx-dot-app/onyx](https://github.com/onyx-dot-app/onyx) | 30,948 | Python | NOASSERTION ⚠ review | `evaluate` | Enterprise search and AI platform. |

## vector-database

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [milvus-io/milvus](https://github.com/milvus-io/milvus) | 45,258 | Go | Apache-2.0 | `benchmark` | Large-scale cloud-native vector database. |
| [weaviate/weaviate](https://github.com/weaviate/weaviate) | 16,606 | Go | BSD-3-Clause | `benchmark` | Object-plus-vector database with hybrid search. |

## document-ingestion

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [microsoft/markitdown](https://github.com/microsoft/markitdown) | 166,850 | Python | MIT | `adopt-adjacent` | Convert common files to LLM-ready markdown. |
| [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) | 152,357 | TypeScript | AGPL-3.0 | `evaluate` | Web data extraction for agents and RAG. |
| [PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | 85,716 | Python | Apache-2.0 | `evaluate` | Multilingual OCR and document structure extraction. |
| [opendatalab/MinerU](https://github.com/opendatalab/MinerU) | 74,937 | Python | NOASSERTION ⚠ review | `evaluate` | Complex PDF and Office conversion to markdown/JSON. |
| [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai) | 73,079 | Python | Apache-2.0 | `evaluate` | LLM-friendly crawling and structured web extraction. |
| [docling-project/docling](https://github.com/docling-project/docling) | 63,367 | Python | MIT | `evaluate` | Structured document conversion and parsing. |
| [opendataloader-project/opendataloader-pdf](https://github.com/opendataloader-project/opendataloader-pdf) | 27,418 | Java | Apache-2.0 | `watch` | AI-ready PDF parser. |
| [Unstructured-IO/unstructured](https://github.com/Unstructured-IO/unstructured) | 15,151 | HTML | Apache-2.0 | `evaluate` | Document ETL and partitioning for RAG pipelines. |

## eval-security

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | 23,365 | TypeScript | MIT | `adopt-core` | Prompt, agent and RAG evaluation plus red teaming. |
| [confident-ai/deepeval](https://github.com/confident-ai/deepeval) | 16,918 | Python | Apache-2.0 | `evaluate` | LLM and agent evaluation framework. |
| [vibrantlabsai/ragas](https://github.com/vibrantlabsai/ragas) | 14,885 | Python | Apache-2.0 | `evaluate` | RAG and agent evaluation toolkit. |
| [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) | 13,348 | Python | Apache-2.0 | `adopt-adjacent` | Security scanner for agent skills. |

## observability

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [langfuse/langfuse](https://github.com/langfuse/langfuse) | 31,343 | TypeScript | NOASSERTION ⚠ review | `evaluate` | Open LLM engineering, traces, prompts and evaluations. |
| [SigNoz/signoz](https://github.com/SigNoz/signoz) | 30,329 | TypeScript | NOASSERTION ⚠ review | `evaluate` | OpenTelemetry-native full-stack observability. |
| [comet-ml/opik](https://github.com/comet-ml/opik) | 20,655 | Python | Apache-2.0 | `evaluate` | Tracing, evaluation and production monitoring for agent workflows. |
| [openobserve/openobserve](https://github.com/openobserve/openobserve) | 20,199 | TypeScript | AGPL-3.0 | `evaluate` | High-performance logs, metrics, traces and LLM observability. |
| [raga-ai-hub/RagaAI-Catalyst](https://github.com/raga-ai-hub/RagaAI-Catalyst) | 16,145 | Python | Apache-2.0 | `watch` | Agent tracing, evaluation and monitoring. |
| [Arize-ai/phoenix](https://github.com/Arize-ai/phoenix) | 10,600 | Python | NOASSERTION ⚠ review | `evaluate` | Open tracing and evaluation platform for AI and agent systems. |

## sandbox-security

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [daytonaio/daytona](https://github.com/daytonaio/daytona) | 72,267 | — | NOASSERTION ⚠ review | `evaluate` | Secure ephemeral development and agent execution environments. |
| [NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw) | 21,816 | TypeScript | Apache-2.0 | `evaluate` | Hardened agent execution patterns in NVIDIA OpenShell. |
| [e2b-dev/E2B](https://github.com/e2b-dev/E2B) | 13,018 | Python | Apache-2.0 | `evaluate` | Cloud sandboxes designed for agent code execution. |
| [opensandbox-group/OpenSandbox](https://github.com/opensandbox-group/OpenSandbox) | 12,047 | Python | Apache-2.0 | `evaluate` | Secure extensible sandbox runtime for agents. |

## identity-secrets

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [Infisical/infisical](https://github.com/Infisical/infisical) | 28,147 | TypeScript | NOASSERTION ⚠ review | `adopt-adjacent` | Open secrets, certificates and privileged-access management platform; license review required. |
| [getsops/sops](https://github.com/getsops/sops) | 22,526 | Go | MPL-2.0 | `adopt-adjacent` | Encrypted configuration and secret-file management with cloud KMS support. |
| [casdoor/casdoor](https://github.com/casdoor/casdoor) | 13,965 | Go | Apache-2.0 | `evaluate` | Agent-first IAM and MCP/LLM gateway with broad identity protocols. |

## browser-computer-use

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | 105,256 | Python | MIT | `evaluate` | Browser-use framework for agents. |
| [bytedance/UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop) | 38,073 | TypeScript | Apache-2.0 | `evaluate` | Multimodal computer-use agent stack. |
| [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) | 35,206 | TypeScript | Apache-2.0 | `adopt-adjacent` | Official Playwright MCP server for browser automation. |
| [microsoft/OmniParser](https://github.com/microsoft/OmniParser) | 25,165 | Jupyter Notebook | CC-BY-4.0 | `evaluate` | Visual screen parsing for GUI and computer-use agents. |
| [apify/crawlee](https://github.com/apify/crawlee) | 24,775 | TypeScript | Apache-2.0 | `evaluate` | Reliable crawling and browser automation substrate. |
| [browserbase/stagehand](https://github.com/browserbase/stagehand) | 23,547 | TypeScript | MIT | `evaluate` | Browser-agent SDK with reliable action primitives. |
| [Skyvern-AI/skyvern](https://github.com/Skyvern-AI/skyvern) | 22,478 | Python | AGPL-3.0 | `evaluate` | AI-driven browser workflow automation with an operator platform. |
| [browseros-ai/BrowserOS](https://github.com/browseros-ai/BrowserOS) | 12,288 | TypeScript | AGPL-3.0 | `watch` | Open agentic browser. |
| [simular-ai/Agent-S](https://github.com/simular-ai/Agent-S) | 12,029 | Python | Apache-2.0 | `watch` | General computer-use framework. |

## model-gateway

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [BerriAI/litellm](https://github.com/BerriAI/litellm) | 53,874 | Python | NOASSERTION ⚠ review | `evaluate` | Provider gateway, routing, budgets and OpenAI-compatible proxy. |
| [Portkey-AI/gateway](https://github.com/Portkey-AI/gateway) | 12,458 | TypeScript | MIT | `evaluate` | AI gateway with routing and guardrail integrations. |

## model-runtime

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [ollama/ollama](https://github.com/ollama/ollama) | 176,329 | Go | MIT | `adopt-adjacent` | Default local-model runtime and OpenAI-compatible serving. |
| [huggingface/transformers](https://github.com/huggingface/transformers) | 162,689 | Python | Apache-2.0 | `reference` | Model definition, training and inference ecosystem. |
| [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | 120,728 | C++ | MIT | `benchmark` | Portable local inference foundation. |
| [vllm-project/vllm](https://github.com/vllm-project/vllm) | 86,518 | Python | Apache-2.0 | `evaluate` | High-throughput model serving. |
| [mudler/LocalAI](https://github.com/mudler/LocalAI) | 47,598 | Go | MIT | `evaluate` | Local multi-modal OpenAI-compatible inference engine across commodity hardware. |
| [exo-explore/exo](https://github.com/exo-explore/exo) | 46,343 | Python | Apache-2.0 | `watch` | Distributed local inference across heterogeneous personal devices. |
| [microsoft/BitNet](https://github.com/microsoft/BitNet) | 39,746 | C++ | MIT | `watch` | 1-bit model inference research and runtime. |
| [lm-sys/FastChat](https://github.com/lm-sys/FastChat) | 39,489 | Python | Apache-2.0 | `reference` | Training, serving and evaluation architecture behind early open chat systems. |
| [sgl-project/sglang](https://github.com/sgl-project/sglang) | 30,413 | Python | Apache-2.0 | `evaluate` | High-performance LLM and multimodal serving. |
| [ml-explore/mlx](https://github.com/ml-explore/mlx) | 27,576 | C++ | MIT | `watch` | Apple-silicon array and model runtime for sovereign local execution. |
| [mlc-ai/web-llm](https://github.com/mlc-ai/web-llm) | 18,380 | TypeScript | Apache-2.0 | `watch` | In-browser model inference. |

## voice-realtime

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [pipecat-ai/pipecat](https://github.com/pipecat-ai/pipecat) | 13,517 | Python | BSD-2-Clause | `evaluate` | Realtime voice and multimodal agent pipelines. |
| [livekit/agents](https://github.com/livekit/agents) | 11,406 | Python | Apache-2.0 | `evaluate` | Realtime voice and multimodal agent framework. |
| [TEN-framework/ten-framework](https://github.com/TEN-framework/ten-framework) | 10,907 | Python | NOASSERTION ⚠ review | `evaluate` | Conversational voice-agent framework. |

## creative-media

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [Comfy-Org/ComfyUI](https://github.com/Comfy-Org/ComfyUI) | 121,163 | Python | GPL-3.0 | `adopt-adjacent` | Node-based generative media execution substrate. |
| [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | 53,513 | TypeScript | NOASSERTION ⚠ review | `adopt-adjacent` | Code-native video rendering for repeatable agent outputs. |
| [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) | 39,485 | Python | AGPL-3.0 | `evaluate` | Agentic video production system and skills library. |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | 35,927 | TypeScript | Apache-2.0 | `evaluate` | Agent-oriented HTML-to-video renderer. |

## data-integration

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [airbytehq/airbyte](https://github.com/airbytehq/airbyte) | 21,645 | Python | NOASSERTION ⚠ review | `evaluate` | Large connector fabric for agent data movement. |

## domain-platform

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [OpenBB-finance/OpenBB](https://github.com/OpenBB-finance/OpenBB) | 70,702 | Python | NOASSERTION ⚠ review | `evaluate` | Open financial data platform for analyst and investor agents. |
| [ToolJet/ToolJet](https://github.com/ToolJet/ToolJet) | 38,223 | JavaScript | AGPL-3.0 | `watch` | Internal tools and business apps for human-agent operations. |
| [gitroomhq/postiz-app](https://github.com/gitroomhq/postiz-app) | 33,435 | TypeScript | AGPL-3.0 | `evaluate` | Agentic social publishing and scheduling surface. |
| [Budibase/budibase](https://github.com/Budibase/budibase) | 28,127 | TypeScript | NOASSERTION ⚠ review | `watch` | Operational apps, automations and agent surfaces. |

## rust-runtime

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [farion1231/cc-switch](https://github.com/farion1231/cc-switch) | 118,326 | Rust | MIT | `evaluate` | Rust desktop switchboard across Hermes and major coding agents. |
| [openinterpreter/openinterpreter](https://github.com/openinterpreter/openinterpreter) | 66,279 | Rust | Apache-2.0 | `benchmark` | Local open-model coding and computer-use agent. |
| [aaif-goose/goose](https://github.com/aaif-goose/goose) | 51,234 | Rust | Apache-2.0 | `evaluate` | Rust extensible execution agent and MCP host. |
| [Hmbown/CodeWhale](https://github.com/Hmbown/CodeWhale) | 39,894 | Rust | MIT | `watch` | Community Rust agent harness. |
| [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | 38,655 | Rust | Apache-2.0 | `adopt-adjacent` | Rust browser automation CLI designed for agents. |
| [TabbyML/tabby](https://github.com/TabbyML/tabby) | 33,721 | Rust | NOASSERTION ⚠ review | `evaluate` | Rust self-hosted coding-assistant platform for local and enterprise evaluation. |
| [qdrant/qdrant](https://github.com/qdrant/qdrant) | 33,354 | Rust | Apache-2.0 | `adopt-adjacent` | Rust vector database for retrieval workloads. |
| [zeroclaw-labs/zeroclaw](https://github.com/zeroclaw-labs/zeroclaw) | 32,284 | Rust | Apache-2.0 | `evaluate` | Rust personal-assistant infrastructure; useful efficiency benchmark. |
| [BloopAI/vibe-kanban](https://github.com/BloopAI/vibe-kanban) | 27,420 | Rust | Apache-2.0 | `pilot` | Rust coding-agent fleet board; narrower and lighter than Paperclip. |
| [huggingface/candle](https://github.com/huggingface/candle) | 20,682 | Rust | Apache-2.0 | `evaluate` | Rust ML and inference framework. |
| [screenpipe/screenpipe](https://github.com/screenpipe/screenpipe) | 20,233 | Rust | NOASSERTION ⚠ review | `evaluate` | Rust local work capture substrate for private memory and agents. |
| [h4ckf0r0day/obscura](https://github.com/h4ckf0r0day/obscura) | 19,367 | Rust | Apache-2.0 | `watch` | Rust headless browser for agents and scraping. |
| [RightNow-AI/openfang](https://github.com/RightNow-AI/openfang) | 18,025 | Rust | Apache-2.0 | `evaluate` | Rust agent operating system; architecture benchmark, not a Paperclip equivalent. |
| [memvid/memvid](https://github.com/memvid/memvid) | 15,975 | Rust | Apache-2.0 | `evaluate` | Rust single-file serverless agent memory. |
| [TencentCloud/CubeSandbox](https://github.com/TencentCloud/CubeSandbox) | 10,383 | Rust | NOASSERTION ⚠ review | `evaluate` | Rust lightweight concurrent sandbox for agents. |
| [BoundaryML/baml](https://github.com/BoundaryML/baml) | 8,564 | Rust | Apache-2.0 | `strategic-exception` | Rust-backed programming language and type-safe boundary for agent applications even if below threshold. |
| [0xPlaygrounds/rig](https://github.com/0xPlaygrounds/rig) | 7,960 | Rust | MIT | `strategic-exception` | Rust agent application framework; direct code-first architecture benchmark even if below threshold. |
| [EricLBuehler/mistral.rs](https://github.com/EricLBuehler/mistral.rs) | 7,488 | Rust | MIT | `strategic-exception` | Rust local inference and serving; useful for sovereign runtime evaluation. |
| [restatedev/restate](https://github.com/restatedev/restate) | 4,175 | Rust | NOASSERTION ⚠ review | `strategic-exception` | Rust durable execution substrate for reliable agents even if below threshold. |

## Selection and safety notes

- A project appears once under its primary architectural role; many span multiple roles in practice.
- The 10k-star threshold captures ecosystem signal but can lag technical quality and can be gamed.
- `strategic-exception` is reserved for lower-star projects with a specific architecture, Rust, durability, or sovereignty reason.
- Installation requires a separate security, license, activity, release, and operational-fit review.
- Archived repositories and unresolved API failures fail catalog validation.
