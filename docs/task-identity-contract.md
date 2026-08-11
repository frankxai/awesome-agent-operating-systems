# Canonical Control-Plane Task Identity

## Purpose

One unit of work must retain one stable identity while different systems provide different bounded functions. A task must not become four unrelated cards merely because Hermes, GitHub, the Starlight swarm, and a future governance shell can all describe it.

The machine-readable contract is [`data/schemas/control-plane-task-identity.schema.json`](../data/schemas/control-plane-task-identity.schema.json). Install the validation dependency and run the fail-closed validator with:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_task_identity.py data/control-plane-task-identities/paperclip-promotion-gate.json
```

The CLI applies the published JSON Schema first and then the cross-field semantic invariants that JSON Schema cannot express, such as scope identity, exact issue URLs, workflow-task membership, and Paperclip execution authority. Add `--live` to verify the linked Hermes task, GitHub issues, and exact Hermes cron script/workdir against their current systems.

## Authority split

| Concern | Authority | Rule |
|---|---|---|
| Task state and dependency graph | Hermes Kanban | One canonical Hermes task ID owns local queue state. |
| Software-delivery evidence | Git/GitHub | Commits, checks, issues, and pull requests are delivery evidence. |
| Recurring trigger | Hermes cron | Exactly one job ID owns the schedule. |
| Multi-machine routing | Starlight swarm | Optional; `null` for a machine-local task. If present, the durable swarm job ID is recorded. |
| Organizational governance | Paperclip | Optional. It receives no execution authority while `integrationStatus` is `not-integrated` or `evaluation-only`. |

The authority map is intentionally asymmetric. A GitHub issue does not schedule work. A cron trigger does not become task state. A Paperclip issue does not become dispatch authority. A swarm envelope does not replace delivery evidence.

## Canonical identifier

Format:

```text
ctid:v1:<scope>:<stable-slug>
```

Example:

```text
ctid:v1:agentic-tech-landscape:paperclip-promotion-gate
```

The identifier is durable across retries, comments, scheduler ticks, and replacement release candidates. An idempotency key prevents duplicate task creation inside the authoritative queue.

## Single-scheduler invariant

Every identity record contains one scheduler owner, one concrete job ID, the exact script basename, and a repository-relative workdir. For the current control-plane watcher:

- owner: `hermes-cron`
- mode: `script-only`
- script: `control-plane-upstream-promotion-gates.py`
- workdir: `.`
- duplicate-dispatch policy: `NOOP_DUPLICATE`

The watcher performs deterministic public-source checks. It does not start Paperclip, a Hermes gateway, a Kanban dispatcher, a model worker, or a Starlight peer lane. A Paperclip heartbeat, second Hermes cron, GitHub schedule, or Windows scheduled task for the same identity would violate the contract.

## State reconciliation

A reconciliation pass checks references; it does not force all systems into the same status vocabulary.

1. Validate the identity shape and reject absolute paths, credentials, or secret-like values.
2. Confirm the Hermes task exists on the named board and matches the recorded tenant.
3. Confirm each GitHub issue exists at the exact repository and issue number.
4. Confirm the one Hermes cron job exists and remains script-only with the expected project workdir.
5. Confirm Paperclip has `executionAuthority: false` while it is not integrated.
6. Treat `swarm: null` as correct for a local-only job; do not manufacture a peer envelope.

## Promotion policy

Paperclip remains `not-integrated` until all of these are true:

1. A newly published exact tarball passes integrity verification.
2. Its clean installed production tree has zero high and zero critical findings.
3. The hardened loopback smoke passes against the exact release.
4. The operator approves credential wiring through `hermes_gateway`.
5. A separate scheduler-ownership review proves no duplicate dispatcher.

A release watcher may report `PROMOTION_CANDIDATE`; it cannot grant production authority by itself.
