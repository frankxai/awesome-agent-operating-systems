# Harness taxonomy A–F

**Purpose:** Stop mixing different technology classes.  
**Audience:** humans (operators) and agents (routers).  
**SSOT companions:** [needs-map.md](needs-map.md), [landscape-map.md](landscape-map.md), [absorb-playbook.md](absorb-playbook.md), live UI `sites/atlas/`.

## Equation

> **Agent = Model + Harness**  
> The model writes. The harness supplies tools, memory, loops, sandboxes, permissions, and proof.

Not every popular “agent” project is the same kind of harness.

## Classes

| Class | Name | Job | Canonical examples | Estate posture |
|---|---|---|---|---|
| **A** | Coding CLI harness | Edit repos, run tools, ship via Git | Codex, Claude Code, OpenCode, Gemini CLI, Aider, OpenHands, oh-my-pi, pi | **Adopt-core workers** |
| **B** | Meta-harness / skill overlay | Swarms, hooks, memory, verified completion *on top of* A | oh-my-openagent, Ruflo (meta layer), OpenHarness | **Evaluate / absorb patterns** — never silent fleet SSOT |
| **C** | Org / company control plane | Goals, org charts, budgets, approvals, multi-agent company state | Paperclip, LobeHub, Multica, Sim | **Hermes Kanban live**; Paperclip pilot only after security gate |
| **D** | Agent frameworks (libraries) | Build product multi-agent graphs in code | LangGraph, AutoGen, CrewAI, Mastra, PydanticAI | **Embed in products** — not daily coding OS |
| **E** | General agent runtime / OS | Chat, tools, memory, cron, gateway, skills | Hermes Agent, OpenClaw, DeerFlow, Goose | **Hermes + Starlight Queen = Tier 0** |
| **F** | Durable workflow engines | Timers, retries, long jobs, SaaS integrations | Temporal, Trigger.dev, n8n, Activepieces | Hermes cron for simple; Temporal/n8n when product durability needs it |

## Classification rules (agents must follow)

1. **Name the class before install or spawn.** If unsure, default to “research only”.
2. **LangGraph / AutoGen / CrewAI are Class D**, not Class A CLI harnesses.
3. **Ruflo and oh-my-openagent are Class B** — they wrap or extend Class A; they do not replace Hermes Queen.
4. **Paperclip is Class C** — complementary governance UI/state, not the coding worker.
5. **One owner per layer.** Do not run two dispatchers, two memory providers, or two human gateways for the same workload.
6. **Stars admit research. Evidence admits routing.** Live evidence lives in Starlight `ops/model-arena/` and Git/PR/CI receipts.
7. **Proprietary peers** (Claude Code, Grok Build) appear on the live fleet roster even when not in this open catalog.

## Mapping open catalog categories → classes

| Catalog category | Default class |
|---|---|
| `coding-agent` | A |
| `coding-control-plane` | B (or C if org-fleet board) |
| `control-plane` | C |
| `agent-framework`, `agent-builder`, `structured-output` | D |
| `agent-runtime`, `rust-runtime`, `interaction-ui` | E |
| `durable-execution`, `workflow-automation` | F |

## Human 2-second read

- **What is this?** Decision atlas for agentic technology.
- **Who for?** Operators building multi-harness estates + agents that route work.
- **Primary object?** Classified project + recommended stack.
- **Next action?** Browse catalog → filter by priority → open absorb playbook.
- **Trust?** Needs map + control-plane decision + live Paperclip/Hermes receipts — not vibes.

## Related

- Live operator UI: [`../sites/atlas/index.html`](../sites/atlas/index.html)
- Starlight Intelligence Network: [starlight-intelligence-network.md](starlight-intelligence-network.md)
- Control-plane decision: [control-plane-decision.md](control-plane-decision.md)
