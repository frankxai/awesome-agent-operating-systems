# Rust and Rust-backed Agentic Technology

Rust is strongest today in **execution edges**—coding agents, local runtimes, browser control, sandboxes, databases, inference and durable primitives—not in company-level governance control planes.

## Current shortlist

| Project | Stars | Language | License | Recommendation | Why it matters |
|---|---:|---|---|---|---|
| [farion1231/cc-switch](https://github.com/farion1231/cc-switch) | 118,326 | Rust | MIT | `evaluate` | Rust desktop switchboard across Hermes and major coding agents. |
| [openai/codex](https://github.com/openai/codex) | 99,131 | Rust | Apache-2.0 | `adopt-core` | Rust coding agent and primary implementation worker. |
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
| [windmill-labs/windmill](https://github.com/windmill-labs/windmill) | 17,178 | Rust | NOASSERTION ⚠ review | `evaluate` | Rust-backed scripts, workflows and internal tools. |
| [memvid/memvid](https://github.com/memvid/memvid) | 15,975 | Rust | Apache-2.0 | `evaluate` | Rust single-file serverless agent memory. |
| [TencentCloud/CubeSandbox](https://github.com/TencentCloud/CubeSandbox) | 10,383 | Rust | NOASSERTION ⚠ review | `evaluate` | Rust lightweight concurrent sandbox for agents. |
| [BoundaryML/baml](https://github.com/BoundaryML/baml) | 8,564 | Rust | Apache-2.0 | `strategic-exception` | Rust-backed programming language and type-safe boundary for agent applications even if below threshold. |
| [0xPlaygrounds/rig](https://github.com/0xPlaygrounds/rig) | 7,960 | Rust | MIT | `strategic-exception` | Rust agent application framework; direct code-first architecture benchmark even if below threshold. |
| [EricLBuehler/mistral.rs](https://github.com/EricLBuehler/mistral.rs) | 7,488 | Rust | MIT | `strategic-exception` | Rust local inference and serving; useful for sovereign runtime evaluation. |
| [restatedev/restate](https://github.com/restatedev/restate) | 4,175 | Rust | NOASSERTION ⚠ review | `strategic-exception` | Rust durable execution substrate for reliable agents even if below threshold. |

## Paperclip-alternative verdict

There is no feature-complete Rust substitute for Paperclip's combination of goals, org chart, issue checkout, approvals, budgets, cost accounting, adapter registry and operator UI. The closest Rust-backed options are narrower:

- **Vibe Kanban** — best lightweight coding-agent fleet board; strong pilot candidate for software-only lanes.
- **OpenFang / ZeroClaw / Goose** — execution runtimes, not governance planes.
- **Rig / BAML** — libraries and typed application boundaries, not operator products.
- **Restate / Windmill / Hatchet** — durable execution/workflow substrates, not agent-company management.
- **CubeSandbox / agent-browser / Qdrant** — excellent Rust edge primitives that can sit beneath Hermes or Paperclip.

A Rust rewrite of Paperclip would not currently improve Frank's bottleneck: orchestration correctness, identity, work ownership, approvals and evidence are more important than control-plane CPU throughput. Prefer a TypeScript control plane with Rust workers and infrastructure where isolation, latency or density matters.
