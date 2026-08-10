# Awesome Agentic Tech

A decision-oriented map of the open and publicly inspectable technology that can form the basis of modern agentic systems: runtimes, control planes, coding fleets, workflows, protocols, memory, knowledge graphs, retrieval, evaluation, observability, security, browser use, model infrastructure, voice, media and business operations.

This repository is not a star leaderboard. It asks:

> **What should we actually adopt, pilot, benchmark, watch or reject—and how do the pieces fit without creating five competing control planes?**

## Current snapshot

- **187** curated projects
- **182** at or above **10,000 GitHub stars**
- **5** lower-star strategic exceptions with a specific Rust/durability reason
- **30** primary categories
- GitHub metadata refreshed **2026-08-10** (selective refresh + OmO/pi admissions)
- Full machine-readable knowledge graph covering every project
- Premium operator UI: [`sites/atlas/index.html`](sites/atlas/index.html)

> [!CAUTION]
> Stars are a discovery signal, not proof of quality, security, maintenance, license or fit. Projects reported by GitHub as `NOASSERTION` or `OTHER` require manual license review and are not treated as verified open source here.

## Start here

| Artifact | Purpose |
|---|---|
| [**Agentic Atlas UI**](sites/atlas/index.html) | SOTA operator surface for humans + agents: taxonomy, stack, live catalog filters |
| [Harness Taxonomy A–F](docs/harness-taxonomy.md) | Classify coding CLIs vs meta-harnesses vs control planes vs frameworks |
| [Absorb Playbook](docs/absorb-playbook.md) | How to gain capability from the landscape without sprawl or second SSOTs |
| [Starlight Intelligence Network](docs/starlight-intelligence-network.md) | How catalog + Queen + SIS + arena form one network |
| [Agentic Tech Catalog](docs/catalog.md) | All projects, grouped and annotated with stars, language, license flag and recommendation |
| [Needs Map](docs/needs-map.md) | The full operational needs model and preferred foundation for each need |
| [Knowledge Graph](docs/knowledge-graph.md) | Architecture views plus JSON/CSV graph artifacts covering every project |
| [Paperclip × Hermes Assessment](docs/paperclip-hermes-assessment.md) | Install decision, overlap, integration, architecture, risks and safe pilot |
| [Control-plane Decision](docs/control-plane-decision.md) | Live Paperclip/Hermes evidence and the current adoption boundary |
| [Canonical Task Identity](docs/task-identity-contract.md) | One-task/one-scheduler contract across Hermes, GitHub, cron, swarm and future governance |
| [Operational Scorecard](reports/hermes-kanban-operational-scorecard-2026-07-18.json) | Sanitized evidence from the real three-card Hermes workflow and reconciliation pass |
| [Rust Landscape](docs/rust-landscape.md) | Rust shortlist and the direct answer on Rust Paperclip alternatives |
| [Inclusion Policy](docs/inclusion-policy.md) | Admission and evidence rules |
| [Landscape Map](docs/landscape-map.md) | Compact layer-oriented index |

## Recommended foundation for Frank's estate

```text
Human command center
  Hermes Agent + Starlight Queen
        |
Optional organizational governance pilot
  Paperclip
        |
Execution workers
  Hermes | Codex | Claude Code | OpenCode | Gemini CLI
        |
Durability and integration
  Hermes cron | Temporal/Trigger.dev | n8n/Activepieces
        |
Interoperability
  MCP | Agent Skills | AGENTS.md | A2A | AG-UI
        |
State and context
  Git/SSOT | Hermes memory | Graphiti | Qdrant when justified
        |
Trust
  tests/evals | promptfoo | SkillSpector | sandbox | secrets
        |
Model and creative infrastructure
  provider APIs | Ollama/llama.cpp/vLLM | ComfyUI | Remotion
```

The key design rule is **one accountable owner per layer**. A control plane coordinates; an execution runtime acts; Git/GitHub proves delivery; the fleet bus routes machines; provider billing proves spend. No new product gets to silently replace all four.

## Paperclip verdict

**The loopback smoke passed; credential wiring is on security hold.**

Paperclip is complementary to Hermes rather than a replacement. It ships native `hermes_local` and `hermes_gateway` adapters and adds company-level goals, org charts, issues, approvals, budgets, cost tracking and an operator board. Hermes remains the tool-using runtime and now has a live-verified durable Kanban baseline with idempotent creation, atomic claims, dependencies, heartbeats and completion evidence.

The pinned, loopback-only, telemetry-disabled Paperclip run returned HTTP 200 with nonempty bodies for API and UI checks. That tracked receipt is deliberately scoped as legacy reachability evidence; redirect outcome, service identity and target credential state were not established by it alone. The published package also pulls a high-severity `undici@5.29.0` finding through the required Cursor Cloud adapter. Paperclip remains stopped with no live credentials connected pending [upstream issue #9794](https://github.com/paperclipai/paperclip/issues/9794). Promotion also requires deterministic recovery, clean GitHub reconciliation, no duplicate dispatch and demonstrated governance value beyond Hermes Kanban.

Read the full [Paperclip × Hermes assessment](docs/paperclip-hermes-assessment.md) and [control-plane decision](docs/control-plane-decision.md).

## Is Paperclip's architecture “best”?

It is currently one of the best **fit-for-purpose organizational control planes** for this estate because:

- it separates control from agent execution;
- it has atomic work checkout, hierarchy, approvals and budgets;
- it supports multiple agent runtimes through adapters;
- Hermes integration is already upstream and built in;
- it offers conventional TypeScript/React/PostgreSQL operations.

It is not a universal agent foundation and it is not yet proven mature enough to replace the existing Starlight control plane. Its young age, very high change rate, large trusted surface and overlapping scheduler/task state require a bounded pilot.

## Is there a better Rust alternative?

**No complete one.** Rust is strongest in execution and infrastructure:

- Codex and Goose for coding/execution
- Vibe Kanban for a lightweight software-agent fleet board
- OpenFang and ZeroClaw for agent runtimes
- agent-browser and CubeSandbox for action/isolation
- Qdrant and memvid for state
- Candle and mistral.rs for inference
- Restate/Windmill-like systems for durable execution
- Rig and BAML for agent application development

None combines Paperclip's company model, goals, approvals, budget enforcement, task checkout, adapters, secrets and operator UI. The pragmatic architecture is **TypeScript control plane + Rust execution edges**, not a rewrite for its own sake.

## Data and automation

The human curation source is [`data/catalog-seed.json`](data/catalog-seed.json). Public GitHub metadata and all derived artifacts are reproducible:

```bash
python scripts/refresh_catalog.py
python scripts/build_knowledge_graph.py
python scripts/render_catalog.py
```

Generated outputs:

- [`data/projects.json`](data/projects.json)
- [`data/projects.csv`](data/projects.csv)
- [`data/knowledge-graph.json`](data/knowledge-graph.json)
- [`data/knowledge-graph-nodes.csv`](data/knowledge-graph-nodes.csv)
- [`data/knowledge-graph-edges.csv`](data/knowledge-graph-edges.csv)
- [`docs/catalog.md`](docs/catalog.md)
- [`docs/rust-landscape.md`](docs/rust-landscape.md)

## Recommendation vocabulary

| Status | Meaning |
|---|---|
| `adopt-core` | Existing core; protect and deepen |
| `adopt-standard` | Interoperability convention to follow |
| `adopt-adjacent` | Useful supporting primitive, added only where needed |
| `pilot` | Bounded, measured evaluation with promotion gates |
| `evaluate` | Strong candidate requiring architecture/security/license fit review |
| `benchmark` | Important comparison baseline, not necessarily an adoption target |
| `watch` | Relevant but no immediate gap justifies deployment |
| `reference` | Educational or historical architecture reference |
| `strategic-exception` | Below 10k stars but included for a specific architecture/Rust/durability reason |

## What this repo will not become

- a dump of every repository containing “agent”;
- a ranking based only on stars;
- a claim that source availability equals an OSI-approved license;
- a collection of copied marketing text;
- an instruction to install all listed systems;
- a second task, memory or control-plane source of truth.

## Contributing

Additions should update the seed, pass the 10k-star rule or justify a strategic exception, state the operational need, record the license signal and explain why the project changes an adoption decision. See [Inclusion Policy](docs/inclusion-policy.md).

## License

Repository content is dedicated to the public domain under [CC0 1.0](LICENSE). Each linked project retains its own license and terms.
