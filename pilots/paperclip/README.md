# Paperclip × Hermes bounded pilot

This harness evaluates Paperclip as an **organizational control plane** without making it a Starlight system of record or giving it live Hermes credentials.

## Current gate

**SMOKE PASSED / CREDENTIAL WIRING HOLD.** The pinned npm release ran successfully and its tarball matched the registry SHA-512 integrity value, but `npm audit --omit=dev` reported one high-severity vulnerable transitive package (`undici@5.29.0` through the unused Cursor Cloud adapter) plus five aggregate moderate findings. The clean-consumer result is reported in [paperclipai/paperclip#9794](https://github.com/paperclipai/paperclip/issues/9794). Keep the service stopped and credential-free until a patched release removes the finding.

## Isolation contract

| Boundary | Pilot value |
|---|---|
| Version | `paperclipai@2026.707.0` |
| Bind | `127.0.0.1:3100` only |
| Auth mode | `local_trusted` for local smoke only |
| Data | repo-local ignored `.pilot-cache/paperclip-data/` |
| Config | repo-local ignored `.pilot-cache/paperclip-data/config.json` |
| Telemetry | `PAPERCLIP_TELEMETRY_DISABLED=1`, `DO_NOT_TRACK=1`, `CI=true` |
| Credentials | none |
| Agents | onboarding metadata only; no live adapter probe or agent heartbeat |
| Hermes | inspect boundary only; do not enable adapter or task bridge |
| Worktrees | disabled / no execution workspace creation |
| Scheduling | no routines or heartbeats |
| Exposure | no LAN, tailnet, tunnel or public URL |

The cache and database are intentionally ignored by Git. Only this runbook and redacted, non-secret receipts are durable artifacts.

## Reproducible preparation

From the repository root:

```bash
mkdir -p .pilot-cache/runtime
cd .pilot-cache/runtime
npm init -y
npm install --ignore-scripts --save-exact paperclipai@2026.707.0
npm audit --omit=dev
```

The installation uses `--ignore-scripts` for initial inspection. The Windows embedded PostgreSQL package's only required lifecycle action hydrates packaged symlinks. Inspect the exact installed script before any targeted rebuild; do not enable all third-party lifecycle scripts blindly.

## Start the bounded smoke service

Use a tracked Hermes terminal background process, not `nohup`, a Startup item or a Windows service:

```bash
export PAPERCLIP_TELEMETRY_DISABLED=1
export DO_NOT_TRACK=1
export CI=true
export PAPERCLIP_SECRETS_STRICT_MODE=true
node .pilot-cache/runtime/node_modules/paperclipai/dist/index.js run \
  --config .pilot-cache/paperclip-data/config.json \
  --data-dir .pilot-cache/paperclip-data \
  --no-repair
```

Run `onboard --yes --bind loopback` only for first-time config generation. Before any subsequent start, verify `server.bind: loopback`, `server.host: 127.0.0.1`, `telemetry.enabled: false` and `secrets.strictMode: true` in the generated config. Paperclip serves its UI/API at `http://127.0.0.1:3100` and uses an embedded loopback PostgreSQL instance.

## Smoke validation

```bash
python scripts/paperclip_pilot_smoke.py \
  --base-url http://127.0.0.1:3100 \
  --receipt reports/paperclip-pilot-smoke-2026-07-18.json
```

The hardened script validates loopback resolution **before** connecting, connects to the validated literal address, disables proxies, forbids redirects, checks expected API/UI content types and service markers, and writes a bounded failure receipt on handled errors. It sends no credential headers; the target service's credential state is explicitly `not_assessed`.

The completed 2026-07-18 receipt predates those harness hardening changes and is intentionally scoped as a **legacy reachability receipt**: both loopback-resolved endpoints returned HTTP 200 with nonempty bodies. Separate browser inspection found no blocking console errors. Both tracked processes were then stopped and ports `3100` and `54329` were verified closed. The hardened harness passed local positive, redirect-blocking and invalid-target tests, but was not used to restart the security-blocked Paperclip service. Durable evidence is in:

- [`reports/paperclip-pilot-smoke-2026-07-18.json`](../../reports/paperclip-pilot-smoke-2026-07-18.json)
- [`reports/paperclip-pilot-security-2026-07-18.md`](../../reports/paperclip-pilot-security-2026-07-18.md)

Run the harness regression suite without starting Paperclip:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

## Windows secret ACL

Do not rely on Paperclip's POSIX mode warning as the Windows access-control source of truth. Inspect the ACL without reading file contents. In this pilot the generated `.env` and `master.key` inherited several unrelated application-package entries; both were hardened to explicit full control for the interactive owner, SYSTEM and Administrators only.

For any repeated or persistent pilot, create the data directory with a private ACL **before** onboarding so secret material never exists under broad inherited access.

## Hermes boundary

The pinned package includes both first-party adapters:

- `hermes_local`: starts `hermes chat -q` as a child process and can scan native Hermes skills.
- `hermes_gateway`: invokes an existing Hermes API server over HTTP/SSE and maps sessions by issue.

For Starlight, use `hermes_gateway` only after the audit gate clears. It preserves the running Hermes gateway boundary and avoids Paperclip spawning arbitrary local Hermes subprocesses. The eventual adapter must use:

- a dedicated API-server key, never copied from terminal output;
- loopback or TLS/private-network transport;
- `sessionKeyStrategy: issue`;
- a dedicated bounded Hermes Project/workdir;
- the `safe`, `file` and narrowly justified toolsets only;
- no Paperclip worktree mode on this BOUNDED-storage host;
- no Paperclip routine when an equivalent Hermes cron or swarm job already exists.

Do **not** expose the Hermes profile's general credentials or install the reverse task-bridge skill yet. If later enabled, use a `task_bridge`-scoped Paperclip key bound to one project or parent issue.

## Hermes control-plane baseline

Before adding another live board, the existing Hermes Kanban path was exercised in an isolated `HERMES_HOME`. Canonical task events and run records prove idempotent creation, competing-claim rejection, parent-gated claim denial, promotion after dependency completion, heartbeats, ownership and structured completion metadata. The harness uses an environment allowlist, invokes only `hermes kanban` commands, does not invoke gateway or dispatch commands and records `worker_pid: null`; activity outside that bounded command path remains `not_assessed` rather than asserted absent.

Run the reusable benchmark against a disposable board only:

```bash
python scripts/hermes_kanban_benchmark.py \
  --hermes-home .pilot-cache/hermes-home \
  --board paperclip-benchmark \
  --workspace .pilot-cache/hermes-workspace \
  --receipt reports/hermes-kanban-paperclip-benchmark-2026-07-18.json
```

The resulting decision is [Hermes Kanban first, Paperclip on security hold](../../docs/control-plane-decision.md). A current Hermes CLI issue causes a rejected competing claim to print an error but exit `0`; the benchmark treats atomic enforcement as passed while recording the false exit contract separately.

## Deterministic promotion watcher

The published-package gate is rechecked daily by one Hermes `no_agent` script owner. Each tick packs the exact published tarball, verifies SHA-512 integrity, installs a clean production consumer with lifecycle scripts and user npm credentials disabled, audits the resolved tree, and removes the temporary consumer. The fingerprint includes the audit result as well as upstream issue/release state, so advisory changes on an unchanged package version are detected; unchanged combined state emits no output.

Run it manually without starting Paperclip:

```bash
python scripts/control_plane_upstream_watch.py --force-audit
python scripts/validate_task_identity.py \
  data/control-plane-task-identities/paperclip-promotion-gate.json --live
```

The exact scheduler script/workdir and three Hermes workflow task IDs are bound in the [canonical identity record](../../data/control-plane-task-identities/paperclip-promotion-gate.json). Do not add a second Paperclip heartbeat, GitHub schedule, Windows task, or swarm dispatcher for this identity.

## Promotion gates

Move from smoke to a seven-day bounded workflow only when all are true:

1. Zero high/critical production dependency audit findings, or a documented upstream fix and safe compatible override.
2. Loopback-only binding is independently confirmed.
3. Telemetry remains disabled in environment and config.
4. A dedicated Hermes API key and bounded workdir exist.
5. One workflow has a written single-writer/single-scheduler contract.
6. Git/GitHub remains delivery truth; Paperclip is governance metadata only.
7. Stop/rollback is proven without touching the live Hermes gateway.

## Rollback

Stop the tracked Paperclip process. Preserve `.pilot-cache/paperclip-data/` until the evaluation decision is recorded. Removing the ignored cache/database is a separate destructive action and is not automated by this repository.
