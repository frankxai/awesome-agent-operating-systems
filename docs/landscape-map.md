# Landscape Map

```mermaid
flowchart TB
  A["Agent OS"] --> B["Local runtimes"]
  A --> C["Coding agents"]
  A --> D["Harnesses"]
  A --> E["MCP and tools"]
  A --> F["Memory and provenance"]
  A --> G["Safety and evals"]
  A --> H["Deployment"]
  A --> I["Managed platforms"]
  B --> B1["Hermes Agent"]
  B --> B2["OpenClaw"]
  C --> C1["Codex"]
  C --> C2["Claude Code"]
  D --> D1["DeepAgents"]
  D --> D2["LangGraph"]
  E --> E1["MCP servers"]
  F --> F1["Letta / Zep / Mem0 / SIS"]
  G --> G1["Evals / promptfoo / Inspect"]
  H --> H1["Vercel / Railway / Cloudflare"]
  I --> I1["v0 / Replit / Cursor / Devin"]
```

## Layer Definitions

| Layer | Definition |
| --- | --- |
| Local runtime | Runs agent work on a user's machine or private infrastructure |
| Coding agent | Reads, edits, tests, and reviews code |
| Harness | Structures long-running or multi-agent execution |
| MCP/tool protocol | Connects models/agents to tools and data |
| Memory/provenance | Records state, recall, traces, and decisions |
| Safety/eval | Tests, constrains, or monitors agent behavior |
| Deployment | Hosts apps, APIs, gateways, dashboards, or workers |
| Managed platform | Productized agentic creation or operation surface |
