# Agentic Technology Needs Map

This map starts from operational needs, not repository popularity. It defines the basis required for Frank's multi-brand, multi-machine agentic estate and maps each need to a **small preferred set** of projects from the larger [catalog](catalog.md).

## The needs

| # | Need | Required outcome | Preferred basis | Evaluate / benchmark | Avoid duplicating |
|---:|---|---|---|---|---|
| 1 | Human command center | One trusted conversational/operator front door across desktop, Telegram and web | **Hermes Agent** + existing Starlight Queen | OpenClaw, LobeHub | Multiple primary gateways receiving the same human message |
| 2 | Organizational control | Goals, accountable owners, hierarchy, approvals, budgets and visible work | **Hermes Kanban now; Paperclip after its security gate clears** | LobeHub, Ruflo, Multica, Sim | Paperclip issues + Hermes tasks + GitHub issues + bus messages all claiming to be task truth |
| 3 | Human agent UI | Inspect, converse with and review many models/agents in a controlled web surface | **Hermes Desktop** as primary | Open WebUI, LibreChat | A second UI becoming a second memory or gateway SSOT |
| 4 | Autonomous execution | Long-horizon tool use, skills, memory, sessions and subagents | **Hermes Agent** | DeerFlow, OpenFang, ZeroClaw, Goose | Replacing Hermes merely because another runtime is faster or more popular |
| 5 | Software delivery | Parallel agents that inspect, implement, test, review and ship through Git | **Codex + Claude Code + OpenCode + Gemini CLI** via existing coding-agent router | OpenHands, Aider, Cline, Continue, SWE-agent | Letting a fleet manager bypass repo instructions, CI or GitHub evidence |
| 6 | Coding-fleet coordination | Work isolation, branch/worktree lanes, progress visibility, conflict prevention | **Hermes Kanban** + existing Git worktrees + swarm bus | Vibe Kanban, Paperclip, Superset, Gas Town, Symphony, Orca, Paseo, HumanLayer | More than one dispatcher for the same worker/repo lane |
| 7 | Durable execution | Resume long jobs, retries, events, timers and failure recovery | Hermes cron for simple jobs; **Temporal/Trigger.dev/Conductor** for product workflows | Restate, Windmill, Hatchet, Prefect, Dagster | Using chat loops or polling as a workflow engine |
| 8 | Business automation | Connect SaaS, webhooks, sheets, CRM, finance and publishing | **n8n or Activepieces** as adjacent integration fabric | Sim, Automatisch, Huginn | Embedding every connector directly into the agent runtime |
| 9 | Interoperability | Portable tools, skills, agent calls and UI event streams | **MCP + Agent Skills + AGENTS.md + A2A** | AG-UI, mcp-use, Composio | Proprietary adapter logic when a stable protocol suffices |
| 10 | Memory and learning | Personal memory, session continuity, reusable procedures and feedback | **Hermes native memory/skills/session DB** | Letta, mem0, Hindsight, MemOS | A second automatic memory provider copying transcripts or secrets |
| 11 | Knowledge graph | Entity relationships, temporal facts, provenance and cross-domain recall | **Graphiti pilot** over Git/SSOT records | Cognee, GraphRAG, LightRAG | Treating generated summaries as authoritative facts |
| 12 | Evidence ingestion | Web, PDF, Office, OCR and structured extraction with provenance | **MarkItDown + Docling + Firecrawl** | MinerU, PaddleOCR, Unstructured, OpenDataLoader | Loading unlicensed or private data into public services |
| 13 | Retrieval/context | Hybrid/graph/vector retrieval for large controlled corpora | Existing FTS/Git first; **Qdrant only when scale requires it** | RAGFlow, PageIndex, OpenViking, Milvus, Weaviate | A vector database for every small text collection |
| 14 | Model access | Provider routing, fallback, local serving, budgets and observability | Hermes provider routing; **LiteLLM** only for shared service needs; **Ollama/llama.cpp** local | vLLM, SGLang, Portkey | Two independent model gateways obscuring spend and failure causes |
| 15 | Structured outputs | Typed, validated agent responses and tool boundaries | Native schemas first; **Instructor/Outlines** when provider-neutral constraints are needed | BAML | Free-form parsing for business-critical state changes |
| 16 | Agent training | Improve agents through datasets, feedback, RL and controlled experiments | Existing eval/experiment OS first | Agent Lightning, VERL, TRL | Training on unreviewed private traces or optimizing proxy metrics |
| 17 | Evaluation | Repeatable task suites, regressions, red teams and quality gates | **promptfoo** + repo tests/evals | DeepEval, Ragas, Opik | Judging agents by demos, stars or self-reported success |
| 18 | Observability | Tool traces, costs, latency, failures and outcome evidence | Hermes native traces initially; **Paperclip only after security clearance**, Langfuse or Opik if needed | SigNoz, OpenObserve, Phoenix | Exporting prompts, secrets or private paths by default |
| 19 | Security and containment | Least privilege, skill scanning and sandboxed execution | **SkillSpector + existing security intake + provider sandboxes** | OpenSandbox, E2B, Daytona, CubeSandbox, NemoClaw | Running downloaded agents/MCPs with broad host and business credentials |
| 20 | Identity and secrets | Scoped identities, short-lived credentials, encrypted configuration and audit | Existing vaults/policies; **SOPS/Infisical** only where they close a real gap | Casdoor | Giving a control plane broad business credentials or plaintext env values |
| 21 | Browser/computer use | Reliable browser diagnostics, browsing and desktop actions | **Hermes browser/computer-use + Chrome DevTools MCP** | agent-browser, Stagehand, browser-use, UI-TARS | Three browser runtimes acting on the same live session |
| 22 | Voice and realtime | Natural spoken command, transcription, streaming and interruption | Existing Hermes voice stack; **LiveKit Agents/Pipecat** for product surfaces | TEN Framework | Duplicating human Telegram/voice gateway receive on multiple machines |
| 23 | Creative production | Repeatable image/video/audio pipelines with brand and QA evidence | Existing brand image system + **ComfyUI/Remotion** | Hyperframes, OpenMontage | Generated media without source, prompt, crop and visual QA records |
| 24 | Data and vertical systems | Finance, social, internal tools and domain-specific operations | Existing Git SSOTs + **OpenBB/Postiz** where scoped | Airbyte, ToolJet, Budibase | A generic agent platform becoming the source of truth for regulated data |
| 25 | Multi-machine operation | Durable routing, machine ownership, health, handoff and no circular waits | Existing **Starlight swarm bus/fleet hub** | Paperclip gateways after pilot | Letting a product UI silently replace the fleet SSOT |
| 26 | Governance and evidence | Human gates for money, production, public sends, credentials, legal and brand identity | Existing estate policies + Git/GitHub; Paperclip approvals only after security clearance | Policy engines later | Autonomous claims without artifacts, tests, URLs or provider evidence |

## Recommended reference stack

```text
Human / channels
  Hermes Agent + Starlight Queen
       |
Task control
  Hermes Kanban
       |
Optional organizational governance (security hold, not SSOT)
  Paperclip after patched-release verification
       |
Execution workers
  Hermes | Codex | Claude Code | OpenCode | Gemini CLI
       |
Durability and integration
  Hermes cron | Temporal/Trigger.dev | n8n/Activepieces
       |
Protocols
  MCP | Agent Skills | AGENTS.md | A2A | AG-UI
       |
State and context
  Git/SSOT | Hermes memory | Graphiti | Qdrant (only when justified)
       |
Trust
  repo tests | promptfoo | SkillSpector | sandbox | secret manager
       |
Model and media infrastructure
  provider APIs | Ollama/llama.cpp/vLLM | ComfyUI | Remotion
```

## Adoption tiers

### Tier 0 — keep as the core

- Hermes Agent
- Starlight Queen/swarm bus/fleet hub
- Git, GitHub issues/PRs/CI and repository SSOTs
- Codex, Claude Code, OpenCode and Gemini CLI router
- current estate security, workspace and storage gates

### Tier 1 — bounded pilots or gated pilot candidates

- Paperclip for one accountable agent team **only after a patched release passes the clean-tarball audit**
- Vibe Kanban only if a software-only lane proves a gap Hermes Kanban does not cover
- Graphiti for a temporal knowledge graph over controlled Git records
- promptfoo for agent and prompt regression suites
- SkillSpector for third-party skill intake

### Tier 2 — add only when a measured gap appears

- Temporal/Trigger.dev/Conductor for product-grade durable workflows
- n8n or Activepieces for business connectors
- Langfuse or Opik for cross-runtime traces/evals
- OpenSandbox, E2B, Daytona or CubeSandbox for stronger isolation
- LiteLLM for centralized multi-app routing
- Qdrant for retrieval scale beyond FTS/Git

### Tier 3 — research and architecture benchmarks

- LobeHub, Ruflo, Multica, Sim
- oh-my-openagent, oh-my-pi, earendil-works/pi (Class B/A harness R&D — see [harness-taxonomy.md](harness-taxonomy.md))
- DeerFlow, OpenFang, ZeroClaw, Goose
- LangGraph, AutoGen, CrewAI, PydanticAI, Mastra, AgentScope, Agno
- Restate, Windmill, Hatchet
- Rig, BAML, mistral.rs and Candle

Operator UI for humans and agents: [`../sites/atlas/index.html`](../sites/atlas/index.html). Absorb ladder: [absorb-playbook.md](absorb-playbook.md).

## Decision rules

1. **One owner per layer.** Do not install two systems that both dispatch, schedule, remember or meter the same workload without an explicit boundary.
2. **Products over frameworks.** Prefer a working operator surface when the need is operations; prefer a library only when building a product.
3. **Evidence over stars.** Stars admit a project to research; tests, architecture, license, security and operating fit decide adoption.
4. **Rust where it pays.** Use Rust for local agents, sandboxes, browsers, databases, inference and durable workers—not as a rewrite mandate for every control plane.
5. **Git remains delivery truth.** Agent dashboards can coordinate, but commits, tests, PRs, CI and deployed artifacts prove work.
6. **Privacy by default.** Disable optional telemetry, keep credentials scoped and never auto-export private conversations or memory.
7. **Pilot before platform.** Every new control plane must win a bounded comparison against the existing Hermes/Starlight path before promotion.
