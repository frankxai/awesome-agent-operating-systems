# Paperclip × Hermes Agent Assessment

**Decision (2026-07-18): the isolated smoke passed, but credential wiring is on security hold. Keep Hermes Kanban as the active task-control substrate and do not make Paperclip a Starlight system of record.**

Paperclip is not a replacement for Hermes Agent. It is a complementary **organizational control plane** that already ships native `hermes_local` and `hermes_gateway` adapters. Hermes remains the execution/runtime plane; Paperclip can add goals, org structure, issue ownership, approvals, budgets, cost rollups and an operator UI.

## Executive verdict

| Question | Answer |
|---|---|
| Install now? | **The pinned loopback smoke is complete. Keep it stopped and credential-free until the published-package audit is clean.** |
| Replace Hermes? | **No.** Hermes owns reasoning, tools, memory, skills, sessions, gateways, channels, cron and delegation. |
| Replace Starlight swarm/GitHub SSOT? | **Not yet.** Paperclip must prove lower coordination cost and clean Git/GitHub evidence before becoming authoritative. |
| Best integration | `hermes_gateway` for an already-running, separately governed Hermes runtime; `hermes_local` only for a same-host disposable worker. |
| Best immediate use | No live worker yet. Re-open only for one governance-only workflow after the dependency gate clears. |
| Rust alternative? | No feature-complete one. Rust options are stronger at execution edges than at company governance. See [Rust landscape](rust-landscape.md). |

## What each system should own

| Concern | Hermes Agent | Paperclip | Recommended owner |
|---|---:|---:|---|
| Interactive human assistant and channels | Strong | Not its purpose | Hermes |
| Tool execution, browser, terminal, files, web, media | Strong | Delegates via adapters | Hermes |
| Durable personal memory and session search | Strong | Run/task records, not equivalent | Hermes |
| Skills and procedural capability | Strong | Can surface/sync skills | Hermes as source; Paperclip as catalog/view |
| Sub-agent delegation | Native | Assigns work to organizational agents | Hermes inside one task; Paperclip across accountable workers |
| Cron and scheduled wakes | Native | Heartbeats/routines | One scheduler per workflow—never both |
| Goals, org chart and chain of command | Limited/custom | Core | Paperclip during pilot |
| Task checkout and concurrent ownership | Native durable Kanban with atomic claims | Atomic issue checkout | Hermes now; Paperclip only for an enrolled cross-runtime governance lane |
| Human approvals and plan confirmation | Chat/UI dependent | Core interaction/approval records | Paperclip for enrolled business workflows |
| Per-agent/company budgets and cost stops | Provider/tool dependent | Core monthly limits and auto-pause | Paperclip, reconciled with provider billing |
| Git/GitHub delivery evidence | Native tools and skills | Work context, not canonical code history | Git/GitHub |
| Multi-machine routing | Starlight swarm fabric | HTTP/gateway/SSH/sandbox targets | Existing swarm initially; Paperclip only after pilot proof |
| Telemetry and evaluation | Hermes status/tool surfaces | Run transcripts, feedback and training records | Both, with clear data boundaries |

## Where Paperclip advances the current estate

1. **Human legibility.** A visible company/agent/task graph is easier to inspect than a collection of sessions, cron jobs and bus messages.
2. **Atomic ownership across its own issue model.** Paperclip returns `409` when another agent owns work, but Hermes Kanban now provides the same core atomic-claim primitive locally. Paperclip must prove value at the organizational layer rather than merely duplicate this control.
3. **Governance.** Goals, parent/child issues, chain of command, approval cards and plan revisions make delegated work auditable.
4. **Budget enforcement.** Paperclip documents 80% warnings and 100% auto-pause at company and agent levels.
5. **Adapter-neutral fleet management.** The same board can invoke Hermes, Codex, Claude, Gemini, OpenCode, process and HTTP adapters.
6. **Native Hermes integration.** The built-in adapter can retain Hermes sessions, parse tool transcripts, expose Hermes skills and call an existing HTTP/SSE gateway.
7. **Decision-training evidence.** Recent upstream work includes operator decision examples, provenance and export for later evaluation/learning.

## Where it overlaps or creates risk

1. **Double scheduling:** Hermes cron, Starlight queues and Paperclip heartbeats can all wake the same logical worker. Assign exactly one scheduler to each workflow.
2. **Competing task SSOTs:** Paperclip issues, GitHub issues, session todos and the swarm bus can drift. During the pilot, Paperclip is the dispatch view; Git/GitHub remains delivery truth; the swarm bus remains machine-routing truth.
3. **Credential blast radius:** Paperclip injects decrypted secrets into agent processes. Any bound agent can read them. Use one-purpose credentials, strict secret refs and sandboxed profiles.
4. **Profile contamination:** `hermes_local` uses local Hermes state and skills. A pilot should use an isolated Hermes profile or `hermes_gateway` with bounded toolsets and workspace.
5. **Worktree/storage fan-out:** Paperclip supports execution workspaces and worktree mode, but these can multiply trees. Keep them disabled during the first laptop pilot.
6. **Telemetry:** Anonymized telemetry is enabled unless disabled. Set both `DO_NOT_TRACK=1` and `PAPERCLIP_TELEMETRY_DISABLED=1` for the evaluation.
7. **Fast-moving maturity:** The repository is young and high-churn. Treat upgrade, migration and compatibility risk as material.

## Live pilot evidence — 2026-07-18

### Paperclip smoke

The pinned `paperclipai@2026.707.0` npm tarball matched the registry SHA-512 value. A repo-local disposable runtime then started successfully with embedded PostgreSQL:

- UI and `/api/health` both returned HTTP 200 with nonempty bodies in the legacy reachability receipt; service identity, redirect behavior and target credential state were not established by that receipt alone;
- the API/UI listener was `127.0.0.1:3100` and PostgreSQL remained loopback-only;
- telemetry was disabled in both environment and config;
- strict secret mode was enabled for the final run;
- the first-party Hermes adapter appeared in onboarding;
- no adapter probe, agent heartbeat, routine, model credential or Hermes credential was authorized;
- both tracked processes exited and ports `3100` and `54329` were verified closed.

Evidence: [smoke receipt](../reports/paperclip-pilot-smoke-2026-07-18.json) and [security receipt](../reports/paperclip-pilot-security-2026-07-18.md).

### Security gate

A clean consumer install reported one high and five aggregate moderate production audit findings. The high finding is `undici@5.29.0`, reached through the required but unused Cursor Cloud adapter:

```text
paperclipai
└─ @paperclipai/server
   └─ @paperclipai/adapter-cursor-cloud
      └─ @cursor/sdk@1.0.23
         └─ @connectrpc/connect-node@1.7.0
            └─ undici@5.29.0
```

Current `master` locks `@cursor/sdk@1.0.19`, while the published adapter declares `^1.0.19`; clean npm consumers resolve `1.0.23`. This lock/publish gap is reported in [paperclipai/paperclip#9794](https://github.com/paperclipai/paperclip/issues/9794). Credentialed adoption remains blocked until a patched release passes a packed-tarball production audit.

The generated `.env` and `master.key` also inherited Windows ACL entries that were too broad for live credentials. They were hardened to Frank, SYSTEM and Administrators only. Any persistent deployment should begin in a pre-hardened private data directory.

### Hermes Kanban baseline

An isolated two-task Hermes Kanban benchmark passed idempotent creation, atomic competing-claim rejection, parent-gated claim denial, promotion after dependency completion, heartbeat recording, ownership history and structured completion metadata. These results are derived from canonical task events and run records, not hard-coded receipt fields. The harness uses an environment allowlist, supplies no credentials, invokes no gateway or dispatch command and records `worker_pid: null`; activity outside that bounded command path is explicitly `not_assessed`. See the [benchmark receipt](../reports/hermes-kanban-paperclip-benchmark-2026-07-18.json) and [control-plane decision](control-plane-decision.md).

One CLI defect surfaced: the competing claim was correctly rejected on stderr, but the top-level process returned exit status `0`. This is covered by [NousResearch/hermes-agent#62810](https://github.com/NousResearch/hermes-agent/issues/62810); the benchmark reproduction was added to that issue. Atomic enforcement passed, but shell automation must not trust the current exit status alone.

## Architecture assessment

### Strengths

- Clear **control-plane / execution-plane separation**: adapters invoke agents; Paperclip does not implement their reasoning runtime.
- Adapter contract separates server execution, UI transcript parsing and CLI formatting.
- Company-scoped entities and atomic single-assignee checkout provide understandable concurrency semantics.
- Embedded PostgreSQL/PGlite lowers local setup cost, while PostgreSQL and Drizzle offer a conventional migration path.
- REST plus HTTP/SSE gateway adapters make remote Hermes integration straightforward.
- Deployment modes separate loopback-local trust from authenticated private/public exposure.
- Secrets support encrypted local storage, external provider references, versioning, audit events and strict mode.
- Active CI surface includes CodeQL, OSV scanning, E2E, Docker, Kubernetes, release smoke and visual regression workflows.

### Weaknesses and open questions

- The TypeScript/Express monolith is pragmatic but is not a hardened distributed scheduler. Reliability depends on database and heartbeat semantics rather than a Temporal/Restate-class durable execution core.
- A control plane with plugins, arbitrary process adapters and credential injection has a large trusted-computing base.
- Embedded/local simplicity and internet-facing multi-user hardening are very different deployment classes; the latter needs a dedicated threat review.
- The adapter layer captures provider-reported cost, but provider invoices remain the financial source of truth.
- Rapid feature expansion raises schema migration, plugin compatibility and operational-change risk.
- GitHub popularity is exceptionally high for the project's age and should not substitute for code/security review.

### Maturity evidence snapshot

As of 2026-07-17, GitHub reports **74,039 stars**, **13,772 forks**, **2,124 open issues**, **2,784 open pull requests**, **4,263 closed pull requests** and 17 GitHub releases. The repository was created on 2026-03-02 and the latest npm release inspected was `paperclipai@2026.707.0` (MIT, Node 20+). The upstream default branch had 34 active GitHub workflows. Recent master runs showed mostly green Docker/release checks but also a release failure and a cancelled Docker run, reinforcing the need to pin and smoke-test a release rather than tracking master.

The very high contribution and issue velocity is both a strength and a risk: active development is undeniable, but stable operations are not yet proven over a long time horizon.

## Why a Rust rewrite is not the answer

Paperclip's current bottlenecks are coordination semantics, identity, approvals, durable state, adapter compatibility and operator UX—not CPU throughput. Node/TypeScript is an acceptable control-plane choice and aligns with the coding-agent ecosystem. Rust is more valuable below it:

- Codex, Goose or Hermes as execution workers
- agent-browser for browser automation
- CubeSandbox or other isolated workers
- Qdrant/memvid for state and retrieval
- Restate/Windmill-like durable execution components
- local inference through Candle/mistral.rs when sovereignty matters

There is no current Rust project with Paperclip's complete product surface. **Vibe Kanban** is the closest lightweight Rust-backed alternative for software-agent fleet work, but it does not replace goals, company hierarchy, budgets, approvals, secrets, general adapters or business workflows.

## Alternative matrix

Paperclip is not “the best architecture for all agentic needs.” It is the strongest current fit in this catalog for **governed multi-runtime work management with native Hermes integration**. Other systems are better in narrower layers:

| Candidate | Primary role | Strongest fit | Main gap versus Paperclip | Local posture |
|---|---|---|---|---|
| **Paperclip** | Organizational control plane | Goals, hierarchy, issue ownership, approvals, budgets, costs and multi-runtime adapters | Young/high-churn; overlaps existing task/scheduler SSOTs | **Pilot** |
| **LobeHub** | Chief-agent operator and interaction UI | Polished always-on human/agent team experience | GitHub license signal requires review; no proven Hermes-native boundary in this assessment | Evaluate UX, not as SSOT |
| **Ruflo** | Meta-harness and swarm coordination | Adaptive multi-agent orchestration across runtimes | Heavy overlap with Hermes delegation and Starlight swarm fabric | Architecture benchmark |
| **Multica** | Managed coding-agent teammates | Assigning and tracking software-agent work, compounding skills | Narrower business governance; license signal requires review | Evaluate software lane |
| **Sim** | Visual agent workforce builder | Visual workflows and deployable agent automation | Less focused on accountable org hierarchy and Git delivery | Evaluate builder UX |
| **Vibe Kanban** | Rust coding-fleet board | Lightweight parallel coding-agent work | Software-only; no general company/goals/budgets/approval plane | **Parallel pilot candidate** |
| **Superset / Gas Town** | Coding-fleet environments | Parallel repo work and developer supervision | Not general business-agent governance | Benchmark coding lane |
| **Temporal / Restate / Trigger.dev** | Durable execution substrates | Timers, retries, event histories and resilient workflows | Require building the operator/company product layer | Adopt only for product durability gaps |
| **n8n / Activepieces** | Business integration automation | Connectors, webhooks and human-readable workflows | Not a reasoning runtime or accountable agent organization | Adjacent integration fabric |
| **Hermes Agent** | Personal/general execution runtime and durable Kanban | Tools, skills, memory, sessions, channels, delegation, atomic claims, dependencies and task recovery | No native company/org hierarchy, approval board or company-level budget UI | **Keep core** |

The practical composition is therefore not “Paperclip everywhere.” It is **Hermes for execution and task control, Git/GitHub for delivery evidence, Starlight for fleet routing, and Paperclip only for bounded organizational governance if a later patched pilot wins**.

## Safe pilot design

**Do not use a global unpinned install.** The preferred evaluation shape is a pinned release in a disposable, loopback-only container or repo-local environment.

1. Pin `paperclipai@2026.707.0` (or a later release only after changelog and migration review).
2. Bind to loopback and use `local_trusted`; do not expose it to LAN, tailnet or the public internet.
3. Set `DO_NOT_TRACK=1` and `PAPERCLIP_TELEMETRY_DISABLED=1`.
4. Enable `PAPERCLIP_SECRETS_STRICT_MODE=true`; create no broad provider, GitHub or business credentials.
5. Create one evaluation company and one sandbox project with no production access.
6. Connect one isolated Hermes runtime through `hermes_gateway`; use a dedicated API key and bounded toolsets/workspace.
7. Keep Paperclip worktree mode and execution-workspace fan-out disabled.
8. Set a very small agent/company budget and preserve provider-side spend limits.
9. Exercise: assignment → checkout → tool run → comment → approval → completion → cost event → stop/resume.
10. Compare against the existing Hermes + Starlight bus + GitHub workflow on coordination overhead, duplicate work, operator clarity, recovery, cost accuracy and evidence quality.

The first smoke completed steps 1–5. The operator did not connect any Hermes, model-provider, GitHub or business credential. The tracked HTTP receipt establishes only loopback-resolved endpoint reachability; its target credential state and redirect outcome are `not_assessed`. Step 6 and all live execution remain blocked by the production dependency audit. The current operational decision is documented in [Control-plane decision: Hermes Kanban first, Paperclip on security hold](control-plane-decision.md).

### Promotion gates

Promote beyond sandbox only if all are true:

- no duplicate dispatch between Paperclip, Hermes cron and the swarm bus;
- task state reconciles cleanly with GitHub delivery evidence;
- restart and failed-run recovery are deterministic;
- secrets never appear in transcripts or exports;
- budget stops match provider-side usage closely enough for operations;
- the operator UI reduces, rather than adds, control-plane work;
- pinned upgrades and database backups restore cleanly;
- no internet exposure is needed, or a separate authenticated deployment threat review passes.

## Source evidence

- [Paperclip repository](https://github.com/paperclipai/paperclip)
- [Paperclip architecture](https://github.com/paperclipai/paperclip/blob/master/docs/start/architecture.md)
- [Paperclip Hermes adapter](https://github.com/paperclipai/paperclip/tree/master/packages/adapters/hermes)
- [Hermes adapter docs](https://docs.paperclip.ing/reference/adapters/hermes/)
- [Hermes gateway onboarding](https://github.com/paperclipai/paperclip/blob/master/doc/HERMES_GATEWAY_ONBOARDING.md)
- [Adapter overview](https://github.com/paperclipai/paperclip/blob/master/docs/adapters/overview.md)
- [Deployment modes](https://github.com/paperclipai/paperclip/blob/master/doc/DEPLOYMENT-MODES.md)
- [Secrets management](https://github.com/paperclipai/paperclip/blob/master/docs/deploy/secrets.md)
- [Costs and budgets](https://github.com/paperclipai/paperclip/blob/master/docs/guides/board-operator/costs-and-budgets.md)
- [Heartbeat protocol](https://github.com/paperclipai/paperclip/blob/master/docs/guides/agent-developer/heartbeat-protocol.md)
- [Paperclip npm package](https://www.npmjs.com/package/paperclipai)
- [Published-package dependency report](https://github.com/paperclipai/paperclip/issues/9794)
- [Hermes Agent](https://github.com/NousResearch/hermes-agent)
- [Hermes Agent documentation](https://hermes-agent.nousresearch.com/docs/)
- [Hermes CLI exit-status issue](https://github.com/NousResearch/hermes-agent/issues/62810)
