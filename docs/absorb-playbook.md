# Absorb playbook — more capability without sprawl

**Goal:** Get more done by absorbing the best external tech *as patterns and bounded pilots*, not by installing every high-star repo.

## Doctrine

1. **Products over frameworks** for operations.
2. **One owner per layer** (see [needs-map.md](needs-map.md)).
3. **Pattern → skill/doc → optional pilot → promote only with evidence.**
4. **Disk BOUNDED/TIGHT:** no bulk clones or multi-worktree fanout for curiosity.
5. **Security intake** before any new MCP, control plane credentials, or broad host access.
6. **Maker ≠ checker** for anything that changes product or money posture.

## Already absorbed (keep compounding)

| Capability | Where it lives | Do not replace with |
|---|---|---|
| Human command + tools + cron + memory | Hermes Agent + Queen | OpenClaw as second gateway |
| Coding fleet routing | `coding-agents` skill + MCR | Random new CLI each week |
| Harness health R&D | `starlight/ops/model-arena` | Star charts alone |
| Task control | Hermes Kanban | Unpromoted Paperclip issues as SSOT |
| Shared skills/hooks | `starlight-agent-config` + SIS adapters | Per-agent snowflake configs only |
| Landscape decisions | this repo | Chat memory |

## Absorb now (pattern only — no install required)

| Source | Class | Steal | Estate landing zone |
|---|---|---|---|
| **oh-my-openagent** | B | Plan → execute → verified completion hooks; complex-repo memory | `coding-agents` references + model-arena EXTERNAL |
| **Ruflo** | B/C edge | Swarm role packs, federated memory metaphors | Queen swarm docs; never fleet bus replacement |
| **Aider** | A | Git-first discipline, repo map efficiency | Coding prompt templates |
| **OpenHands** | A | Sandbox operator UX, async coding loops | Future isolated runner design |
| **promptfoo** | Trust | Declarative eval suites | `starlight-evals` + arena task packs |
| **Langfuse / Opik** | Trust | Trace schema ideas | Hermes-native first; vendor only if gap measured |
| **hcom-style buses** | Interop | Cross-CLI messaging patterns | Existing swarm bus / ASPH |
| **Deep Agents / Dcode** | A/E | Batteries-included harness patterns | Optional worker lane after doctor green |

## Install / pilot ladder

### Tier 0 — already core (do more *with*, not *instead*)

- Hermes, Codex, Claude Code, OpenCode, Gemini/AGY, Grok Build (when green)
- Queen + swarm bus + model-arena cadence
- This atlas + taxonomy language in every agent prompt that touches tooling choice

### Tier 1 — bounded pilots (gates required)

| Pilot | Gate | Done-when |
|---|---|---|
| Paperclip | Clean package audit (no high undici/advisory), loopback-only, no business credentials, governance value beyond Kanban | Decision receipt + HOLD or promote |
| Graphiti | Controlled Git facts only; no secret transcript dump | Query demo + provenance |
| promptfoo suite | One domain pack (routing or smoke) | CI-local green pack |
| OmO (read-only study) | No default install on laptop; document hooks worth porting | Absorb note in EXTERNAL-LEARNING |

### Tier 2 — only when measured gap

- Temporal/Trigger.dev for product long-running jobs
- n8n/Activepieces for SaaS glue
- Stronger sandbox (E2B/Daytona/OpenSandbox) for untrusted code
- LiteLLM only if multi-app routing spend is opaque

### Tier 3 — research / architecture benchmarks

- Ruflo, LobeHub, Multica, Sim, DeerFlow, ZeroClaw
- LangGraph, AutoGen, CrewAI, Mastra, AgentScope
- Do **not** auto-install into the estate control plane

## Agent checklist before “install X”

```text
[ ] Named class A–F
[ ] Named layer owner it would touch
[ ] Existing estate coverage for that need (needs-map row)
[ ] Measured gap (receipt/date) — not FOMO
[ ] License + security posture known
[ ] Disk mode admits clone/install
[ ] Rollback plan
[ ] Where patterns land if we do NOT install
```

If any box fails → **document and absorb**, do not install.

## Human checklist before saying yes

- Does this reduce operator cognitive load or add a second cockpit?
- Does it create a second task/memory/gateway truth?
- Can we get 80% of the value as a skill/doc in 1 day?
- Who is the accountable human for production/public/spend gates?

## Convergence with live fleet R&D

```text
World catalog (this repo)
    ↓ class + priority
Absorb playbook (this file)
    ↓ pattern or pilot
model-arena smoke/domain evidence
    ↓ routing matrix
coding-agents MCR + Queen
    ↓
SIS / brand intelligence systems
```

## Fresh admissions (2026-08-10)

Added to catalog seed and live snapshot:

- `code-yeongyu/oh-my-openagent` — Class B meta-harness (evaluate)
- `can1357/oh-my-pi` — Class A terminal harness (evaluate)
- `earendil-works/pi` — Class A toolkit lineage (evaluate)

These expand **research surface**, not default runtime.

## Related UI

Open [`../sites/atlas/index.html`](../sites/atlas/index.html) for the operator/agent surface.
