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
  A --> K["Swarm Topology Standards"]
  B --> B1["Hermes Agent / OpenClaw / Paperclip"]
  C --> C1["Codex / Claude Code / Cline"]
  D --> D1["LangGraph / AutoGen / CrewAI / Mastra / Agno"]
  E --> E1["MCP servers / mcp-doctor"]
  F --> F1["Letta / Zep / Mem0 / SIS Memory"]
  G --> G1["Evals / promptfoo / AgentOps"]
  H --> H1["Vercel / Railway / Cloudflare"]
  I --> I1["v0 / Replit / Cursor / Devin / Lovable / Bolt"]
  K --> K1["Kings (policy locks)"]
  K --> K2["Queens (meta-orchestrators)"]
  K --> K3["Starlight Board / Model Council"]
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
