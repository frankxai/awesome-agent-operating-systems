# Inclusion Policy

This catalog is decision-oriented and curated. Inclusion means “worth structured evaluation,” not “approved,” “safe,” “open source,” or “recommended for installation.”

## Default admission rule

A project should satisfy all of these:

1. Publicly inspectable source and a stable GitHub repository.
2. Direct relevance to at least one need in the [Needs Map](needs-map.md).
3. Normally **10,000 or more GitHub stars** at the time of refresh.
4. A primary-source description, active repository metadata and a concrete reason it affects an architecture or adoption decision.
5. One primary category and one local recommendation in `data/catalog-seed.json`.

Stars are only a discovery filter. They do not prove technical quality, security, legitimacy, maintenance, license or fit.

## Strategic exceptions

Projects below 10,000 stars may be included only as `strategic-exception` when they provide a capability that popularity filtering would otherwise miss, such as:

- a modern Rust-native agent or inference architecture;
- a durable-execution primitive with strong agent fit;
- a protocol or standard that is more important than its repository audience;
- a uniquely relevant sovereignty, privacy or security primitive.

The seed entry must state the specific reason. “Promising,” “cool” or “new” is not enough.

## License gate

- GitHub SPDX values are recorded in the generated catalog.
- `NOASSERTION` and `OTHER` are marked `licenseReviewRequired=true`.
- Such projects may remain visible for evaluation, but this repository does **not** call them verified open source.
- Before code reuse, redistribution, deployment or commercial integration, inspect the exact license file and version-specific terms.
- Source-available, fair-code and open-core projects must be labeled honestly; public source is not synonymous with an OSI-approved license.

## Strong fit

- Agent runtimes and organizational control planes.
- Coding agents and coding-fleet managers.
- Agent frameworks, builders and durable workflow engines.
- MCP, A2A, Agent Skills, AGENTS.md and agent/UI protocols.
- Memory, knowledge graphs, RAG, ingestion and retrieval systems.
- Evaluation, red teaming, observability, secrets and sandboxes.
- Browser/computer use, voice and creative-media execution used by agents.
- Model gateways, local inference and serving infrastructure.
- Business/data platforms with direct value for agent-operated domains.

## Weak fit or exclusion

- Model weights or benchmark pages without an agent-system role.
- Prompt collections without operational behavior or evaluation evidence.
- Closed products whose architecture cannot be inspected, except in a clearly separated comparison appendix.
- Thin wrappers, clones or marketing pages with no distinct architecture.
- Archived projects, unless intentionally retained in a historical section.
- Projects with unverifiable claims, suspicious install paths or no meaningful maintenance evidence.
- Generic infrastructure whose connection to agentic operations is too broad (for example, listing every database or web framework).

## Required seed fields

Each `data/catalog-seed.json` entry must include:

- `repo` — canonical `owner/name`;
- `category` — primary architectural role;
- `priority` — local recommendation vocabulary from the README;
- `why` — one specific operational reason.

The refresh script adds stars, language, license signal, dates and repository state from GitHub.

## Removal and status changes

Remove or demote entries when a project is archived, abandoned, misleading, security-hostile, license-incompatible, superseded or no longer relevant. A major adoption change should be evidence-backed and update the needs map or assessment that depends on it.

## Verification

Run:

```bash
python scripts/refresh_catalog.py
python scripts/build_knowledge_graph.py
python scripts/render_catalog.py
python scripts/validate_repository.py
```

The refresh fails on archived repositories, unresolved API calls, unexpected sub-threshold entries or duplicate repositories.