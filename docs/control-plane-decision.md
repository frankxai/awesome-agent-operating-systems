# Control-plane decision: Hermes Kanban first, Paperclip on security hold

**Decision date:** 2026-07-18  
**Estate decision:** keep Hermes Kanban as the default local task-control substrate. Keep Paperclip stopped and credential-free until its published package clears the security gate and a governance-only experiment proves value beyond Hermes.

## Evidence used

This is not a feature-list comparison. It combines two isolated executions:

1. Paperclip's pinned package started successfully on loopback; its API and UI returned HTTP 200 and its built-in Hermes adapter was visible. The tracked HTTP receipt is scoped to legacy endpoint reachability; browser inspection and CLI health are separate observations.
2. Hermes Kanban completed a two-task benchmark in an isolated `HERMES_HOME` using an environment allowlist. The harness supplied no credentials, invoked no gateway or dispatch command and recorded `worker_pid: null`; external activity outside the bounded command path is `not_assessed`.

Receipts:

- [`paperclip-pilot-smoke-2026-07-18.json`](../reports/paperclip-pilot-smoke-2026-07-18.json)
- [`paperclip-pilot-security-2026-07-18.md`](../reports/paperclip-pilot-security-2026-07-18.md)
- [`hermes-kanban-paperclip-benchmark-2026-07-18.json`](../reports/hermes-kanban-paperclip-benchmark-2026-07-18.json)
- [`hermes-kanban-operational-scorecard-2026-07-18.json`](../reports/hermes-kanban-operational-scorecard-2026-07-18.json)
- [`paperclip-published-release-gate-2026-07-18.json`](../reports/paperclip-published-release-gate-2026-07-18.json)

## Implemented operational control

The decision has now been exercised as a bounded three-card Hermes workflow rather than left as a recommendation. All three cards completed with claim, heartbeat, comment, dependency-promotion, and completion evidence; idempotency replay preserved a three-card board and returned the existing task. No model worker PID was observed.

The canonical identity is [`ctid:v1:agentic-tech-landscape:paperclip-promotion-gate`](../data/control-plane-task-identities/paperclip-promotion-gate.json). Its fail-closed validator reconciles the exact Hermes board/tasks, both upstream GitHub issues, and the enabled script-only Hermes cron owner. The daily watcher performs a fresh clean-consumer audit even when the package version is unchanged, stays silent when the combined upstream-and-audit fingerprint is unchanged, and starts no service, gateway, worker, or production action.

Paperclip remains `not-integrated` with `executionAuthority: false`. The current fresh audit still resolves `undici@5.29.0` and therefore remains `HOLD`.

## Proven control baseline

| Control | Hermes Kanban live evidence | Paperclip evidence in this pilot |
|---|---|---|
| Durable local task state | Passed | Service/database started; issue workflow not executed |
| Idempotent task creation | Passed | Not exercised |
| Atomic competing claim rejection | Passed | Documented/source-backed; not exercised through API |
| Parent-gated claim denial and dependency release | Passed from `claim_rejected`, `promoted` and final task events | Product capability; not exercised |
| Heartbeat/liveness event | Passed | Coordinator started; no agent heartbeat authorized |
| Structured completion metadata | Passed | Product capability; not exercised |
| Board lifecycle without a dispatch command | Passed; command log contains only Kanban operations and runs record `worker_pid: null` | Service required |
| Company hierarchy and org chart | Not a Hermes Kanban goal | Native Paperclip differentiator |
| Approval cards and plan revisions | External/custom in Hermes | Native Paperclip differentiator |
| Company/agent budget policy and rollups | Provider/custom in Hermes | Native Paperclip differentiator |
| Multi-runtime operator UI | Limited | Native Paperclip differentiator |

Hermes therefore already covers the task-control primitives that originally motivated part of the Paperclip evaluation. Paperclip must be justified by its **organizational governance**, not by claiming basic task persistence, dependencies, atomic ownership or heartbeat support are missing.

## Hermes finding

A competing claim was correctly rejected, proving atomic enforcement. However, the installed top-level CLI returned exit status `0` while writing `cannot claim ... status=running` to stderr. That makes shell automation unable to distinguish success from rejection without parsing text.

This is an instance of the existing generic CLI return-value issue [NousResearch/hermes-agent#62810](https://github.com/NousResearch/hermes-agent/issues/62810). The benchmark reproduction was added as [a public comment](https://github.com/NousResearch/hermes-agent/issues/62810#issuecomment-5008690983). The receipt records `claimConflictHasNonzeroExit: false` while still passing the underlying atomicity control.

## Paperclip finding

Paperclip is operationally viable on Windows but the current published package fails the credentialed-adoption gate:

- one high and five aggregate moderate production audit findings;
- required installation of the unused Cursor Cloud adapter;
- a workspace-lock/published-package resolution gap;
- generated secret files inherited ACL entries that were too broad for live credentials until manually hardened.

The clean-consumer dependency report is [paperclipai/paperclip#9794](https://github.com/paperclipai/paperclip/issues/9794).

## Decision rules

### Use Hermes Kanban now for

- local and multi-profile task queues;
- atomic claims and stale-claim recovery;
- dependencies, heartbeats, completion evidence and dispatcher ownership;
- work tied directly to Hermes sessions, profiles and bounded workspaces.

### Re-open the Paperclip pilot only for

- company/portfolio hierarchy that operators actually use;
- approval and plan-revision workflows requiring an auditable UI;
- per-agent/company budget policy and cost rollups;
- cross-runtime governance where Hermes is one worker among several.

Do not re-open it merely to obtain another kanban board.

## Next bounded experiment

After an upstream patched release:

1. Repeat the packed-tarball integrity and production audit in a clean cache.
2. Start Paperclip from a pre-hardened private Windows data directory.
3. Use one non-production governance record with **no autonomous heartbeat**.
4. Mirror the same two-task dependency workflow in Hermes and Paperclip.
5. Measure operator actions, time-to-recovery, duplicate-state reconciliation and evidence clarity.
6. Connect a dedicated `hermes_gateway` only if Paperclip materially wins on governance overhead.

## What not to add yet

- No Paperclip production credentials.
- No Paperclip routine overlapping Hermes cron or the Starlight swarm bus.
- No Paperclip-managed worktree fan-out.
- No second live coding-fleet board such as Vibe Kanban until a software-only lane demonstrates a gap Hermes Kanban cannot cover.
- No durable execution substrate such as Restate until an actual restart/recovery failure requires it.

This keeps the estate's control-plane count flat while preserving a clear path to adopt Paperclip for the capabilities that are genuinely differentiated.
