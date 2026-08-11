# Paperclip pilot security receipt — 2026-07-18

## Scope

This receipt covers the disposable Windows pilot of `paperclipai@2026.707.0`. It records package integrity, the clean-consumer dependency tree, loopback and telemetry controls, local secret-file ACLs, upstream disclosure and shutdown state. No production credentials were supplied.

## Package integrity

The registry and downloaded tarball SHA-512 values matched exactly:

```text
sha512-ibgW6muVlzmZT3v4Qsi7MAuPYSlPHfUT2yowlHeLUTpfr1P4h4J4qRZPiGoMc2zyhieoSKKiE2XkDiMMPT3Y3w==
```

This proves the inspected tarball matches the npm registry metadata; it does not prove the package is free of vulnerabilities.

## Production dependency audit

A clean consumer install using `npm install --ignore-scripts --save-exact paperclipai@2026.707.0` followed by `npm audit --omit=dev` returned:

| Severity | Count |
|---|---:|
| Critical | 0 |
| High | 1 |
| Moderate | 5 |
| Low / info | 0 |

The high finding is `undici@5.29.0`. The aggregate path is:

```text
paperclipai@2026.707.0
└─ @paperclipai/server@2026.707.0
   └─ @paperclipai/adapter-cursor-cloud@2026.707.0
      └─ @cursor/sdk@1.0.23
         └─ @connectrpc/connect-node@1.7.0
            └─ undici@5.29.0
```

The adapter is installed even when Cursor Cloud is unused.

## Published-package / workspace-lock gap

Current Paperclip `master` declares `"@cursor/sdk": "^1.0.19"` and locks `@cursor/sdk@1.0.19`. That lock entry has no `@connectrpc/connect-node`; the current monorepo lock contains only `undici@7.24.4`.

A clean npm consumer is not constrained by the monorepo lock and resolves `@cursor/sdk@1.0.23`, introducing the vulnerable chain. Release validation therefore needs to install the packed npm tarball in a clean temporary project, not audit only the workspace lock.

Public upstream report: [paperclipai/paperclip#9794](https://github.com/paperclipai/paperclip/issues/9794).

## Runtime controls verified

- API/UI bound to `127.0.0.1:3100`.
- Embedded PostgreSQL bound only to loopback on port `54329`.
- `telemetry.enabled` was set to `false`.
- `PAPERCLIP_TELEMETRY_DISABLED=1`, `DO_NOT_TRACK=1` and `CI=true` were set.
- `PAPERCLIP_SECRETS_STRICT_MODE=true` and config `strictMode: true` were set for the final run.
- No LLM, Hermes, GitHub or business credential was connected.
- The Hermes adapter was inspected in the UI but its live probe and heartbeat were not run.
- API health and UI root returned HTTP 200 with nonempty bodies; see [`paperclip-pilot-smoke-2026-07-18.json`](paperclip-pilot-smoke-2026-07-18.json). That legacy receipt does not independently establish service identity, redirect outcome or the target service's credential state.

After independent review, the smoke harness was hardened to validate loopback before connecting, pin the connection to the validated literal address, disable proxies, forbid redirects, validate expected content and emit handled failure receipts. Positive, redirect-blocking and invalid-target mock tests in [`tests/test_pilot_harnesses.py`](../tests/test_pilot_harnesses.py) passed. The security-blocked Paperclip service was not restarted solely to regenerate the legacy receipt.

## Windows ACL result

Paperclip's POSIX-style permission check reported the generated key as mode `666`, but Windows access is governed by ACLs. The generated `.env` and `master.key` initially inherited several application-package and sandbox-group entries from the parent directory.

Both files were hardened to explicit full control for only:

- the interactive owner account
- `NT AUTHORITY\\SYSTEM`
- `BUILTIN\\Administrators`

No secret contents were read or recorded. A future persistent deployment should create its data directory under a pre-hardened private location rather than repairing inherited ACLs after onboarding.

## Shutdown and rollback

Both tracked Paperclip processes exited. Ports `3100` and `54329` were verified closed after shutdown. No Windows service, startup entry, global npm package, Hermes gateway change or production integration was created.

## Gate

**Credential wiring remains blocked.** Resume only after a patched Paperclip release has a clean packed-tarball production audit and the pilot uses a private data root with verified Windows ACLs from creation time.
