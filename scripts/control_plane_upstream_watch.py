#!/usr/bin/env python3
"""Watch upstream control-plane promotion gates without starting any service.

The script is suitable for a Hermes ``no_agent`` cron job. It prints nothing
when public upstream state and the clean-consumer audit are unchanged. Every
check packs and audits the exact published tarball in an ignored temporary
directory with lifecycle scripts and user npm credentials disabled.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PAPERCLIP_REPO = "paperclipai/paperclip"
PAPERCLIP_ISSUE = 9794
HERMES_REPO = "NousResearch/hermes-agent"
HERMES_ISSUE = 62810
VERSION_PATTERN = re.compile(r"^[0-9A-Za-z][0-9A-Za-z._+-]{0,79}$")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def require_cache_path(path: Path, repo_root: Path, label: str) -> Path:
    resolved = path.resolve()
    cache_root = (repo_root / ".pilot-cache").resolve()
    try:
        resolved.relative_to(cache_root)
    except ValueError as exc:
        raise ValueError(f"{label} must remain under repository .pilot-cache") from exc
    return resolved


def command_environment(*, npm_user_config: Path | None = None) -> dict[str, str]:
    allowed = {
        "PATH",
        "PATHEXT",
        "SYSTEMROOT",
        "WINDIR",
        "COMSPEC",
        "TEMP",
        "TMP",
        "LOCALAPPDATA",
        "APPDATA",
        "PROGRAMDATA",
        "PROGRAMFILES",
        "PROGRAMFILES(X86)",
        "PROGRAMW6432",
        "HOMEDRIVE",
        "HOMEPATH",
        "USERPROFILE",
        "USERNAME",
        "TERM",
        "MSYSTEM",
    }
    env = {key: value for key, value in os.environ.items() if key.upper() in allowed}
    env.update(
        {
            "CI": "true",
            "DO_NOT_TRACK": "1",
            "NPM_CONFIG_REGISTRY": "https://registry.npmjs.org/",
            "NPM_CONFIG_UPDATE_NOTIFIER": "false",
            "NPM_CONFIG_FUND": "false",
            "NPM_CONFIG_AUDIT": "false",
        }
    )
    if npm_user_config is not None:
        env["NPM_CONFIG_USERCONFIG"] = str(npm_user_config)
    return env


def run_command(
    command: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    timeout: int,
    allow_failure: bool = False,
) -> subprocess.CompletedProcess[str]:
    executable = shutil.which(command[0], path=env.get("PATH"))
    if executable is None:
        raise RuntimeError(f"required command is unavailable: {command[0]}")
    resolved_command = [executable, *command[1:]]
    result = subprocess.run(
        resolved_command,
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0 and not allow_failure:
        detail = (result.stderr or result.stdout or "command failed").strip().splitlines()
        raise RuntimeError(f"{command[0]} command failed: {detail[-1] if detail else 'unknown error'}")
    return result


def issue_snapshot(repo: str, number: int, *, cwd: Path, env: dict[str, str]) -> dict[str, Any]:
    owner, name = repo.split("/", 1)
    query = """
query($owner:String!,$name:String!,$number:Int!){
  repository(owner:$owner,name:$name){
    issue(number:$number){
      number title url state updatedAt
      comments(last:1){totalCount nodes{createdAt author{login}}}
    }
  }
}
""".strip()
    result = run_command(
        [
            "gh",
            "api",
            "graphql",
            "-f",
            f"query={query}",
            "-F",
            f"owner={owner}",
            "-F",
            f"name={name}",
            "-F",
            f"number={number}",
        ],
        cwd=cwd,
        env=env,
        timeout=45,
    )
    payload = json.loads(result.stdout)
    issue = payload["data"]["repository"]["issue"]
    comments = issue.get("comments") or {}
    nodes = comments.get("nodes") or []
    latest = nodes[-1] if nodes else None
    return {
        "repo": repo,
        "number": issue["number"],
        "title": issue["title"],
        "url": issue["url"],
        "state": issue["state"],
        "updatedAt": issue["updatedAt"],
        "commentCount": int(comments.get("totalCount", 0)),
        "latestComment": (
            {
                "createdAt": latest.get("createdAt"),
                "author": (latest.get("author") or {}).get("login"),
            }
            if latest
            else None
        ),
    }


def npm_release_snapshot(*, cwd: Path, env: dict[str, str]) -> dict[str, str]:
    result = run_command(
        ["npm", "view", "paperclipai@latest", "version", "dist.integrity", "--json"],
        cwd=cwd,
        env=env,
        timeout=45,
    )
    payload = json.loads(result.stdout)
    version = str(payload["version"])
    if not VERSION_PATTERN.fullmatch(version):
        raise ValueError("npm returned an unsafe Paperclip version string")
    return {"version": version, "registryIntegrity": str(payload["dist.integrity"])}


def collect_package_versions(node: Any, package_name: str, found: set[str]) -> None:
    if isinstance(node, dict):
        if node.get("name") == package_name and isinstance(node.get("version"), str):
            found.add(node["version"])
        dependencies = node.get("dependencies")
        if isinstance(dependencies, dict):
            for name, dependency in dependencies.items():
                if name == package_name and isinstance(dependency, dict) and isinstance(dependency.get("version"), str):
                    found.add(dependency["version"])
                collect_package_versions(dependency, package_name, found)
    elif isinstance(node, list):
        for item in node:
            collect_package_versions(item, package_name, found)


def package_gate(vulnerabilities: dict[str, Any], undici_versions: list[str]) -> tuple[str, list[str]]:
    critical = int(vulnerabilities.get("critical", 0))
    high = int(vulnerabilities.get("high", 0))
    reasons: list[str] = []
    if critical:
        reasons.append(f"{critical} critical production vulnerability finding(s)")
    if high:
        reasons.append(f"{high} high production vulnerability finding(s)")
    if "5.29.0" in undici_versions:
        reasons.append("consumer tree still resolves undici@5.29.0")
    return ("HOLD", reasons) if reasons else ("PROMOTION_CANDIDATE", [])


def audit_paperclip_release(
    release: dict[str, str],
    *,
    cache_root: Path,
    env: dict[str, str],
) -> dict[str, Any]:
    version = release["version"]
    with tempfile.TemporaryDirectory(prefix="paperclip-audit-", dir=cache_root) as temporary:
        temp_root = Path(temporary)
        empty_npmrc = temp_root / "empty.npmrc"
        empty_npmrc.write_text("registry=https://registry.npmjs.org/\n", encoding="utf-8")
        npm_env = dict(env)
        npm_env["NPM_CONFIG_USERCONFIG"] = str(empty_npmrc)

        packed = run_command(
            ["npm", "pack", f"paperclipai@{version}", "--json", "--ignore-scripts"],
            cwd=temp_root,
            env=npm_env,
            timeout=120,
        )
        pack_payload = json.loads(packed.stdout)
        if not isinstance(pack_payload, list) or len(pack_payload) != 1:
            raise RuntimeError("npm pack did not return exactly one artifact")
        pack_info = pack_payload[0]
        tarball = temp_root / pack_info["filename"]
        digest = base64.b64encode(hashlib.sha512(tarball.read_bytes()).digest()).decode("ascii")
        computed_integrity = f"sha512-{digest}"
        registry_integrity = release["registryIntegrity"]
        if computed_integrity != registry_integrity:
            raise RuntimeError("packed tarball integrity does not match npm registry metadata")

        install_root = temp_root / "consumer"
        install_root.mkdir()
        (install_root / "package.json").write_text(
            json.dumps(
                {
                    "name": "paperclip-release-gate",
                    "private": True,
                    "version": "0.0.0",
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        run_command(
            [
                "npm",
                "install",
                str(tarball),
                "--ignore-scripts",
                "--package-lock=true",
                "--no-fund",
                "--no-update-notifier",
                "--audit=false",
            ],
            cwd=install_root,
            env=npm_env,
            timeout=240,
        )
        audit_result = run_command(
            ["npm", "audit", "--omit=dev", "--json"],
            cwd=install_root,
            env=npm_env,
            timeout=180,
            allow_failure=True,
        )
        audit_payload = json.loads(audit_result.stdout)
        vulnerabilities = dict((audit_payload.get("metadata") or {}).get("vulnerabilities") or {})

        tree_result = run_command(
            ["npm", "ls", "undici", "--all", "--json"],
            cwd=install_root,
            env=npm_env,
            timeout=60,
            allow_failure=True,
        )
        tree_payload = json.loads(tree_result.stdout or "{}")
        versions: set[str] = set()
        collect_package_versions(tree_payload, "undici", versions)
        undici_versions = sorted(versions)
        gate, reasons = package_gate(vulnerabilities, undici_versions)

        return {
            "schema": "paperclip-published-release-gate.v1",
            "checkedAt": utc_now(),
            "package": "paperclipai",
            "version": version,
            "registryIntegrity": registry_integrity,
            "computedIntegrity": computed_integrity,
            "integrityMatched": True,
            "installLifecycleScripts": "disabled",
            "npmUserConfig": "empty-disposable-config",
            "productionAuditExitCode": audit_result.returncode,
            "productionVulnerabilities": vulnerabilities,
            "undiciVersions": undici_versions,
            "promotionGate": gate,
            "holdReasons": reasons,
            "serviceStarted": False,
            "credentialsSupplied": False,
            "temporaryConsumerRemovedAfterCheck": True,
        }


def fingerprint_payload(snapshot: dict[str, Any], audit: dict[str, Any]) -> dict[str, Any]:
    return {
        "snapshot": {key: value for key, value in snapshot.items() if key != "checkedAt"},
        "audit": {
            key: audit.get(key)
            for key in (
                "version",
                "registryIntegrity",
                "computedIntegrity",
                "integrityMatched",
                "productionVulnerabilities",
                "undiciVersions",
                "promotionGate",
                "holdReasons",
            )
        },
    }


def state_fingerprint(snapshot: dict[str, Any]) -> str:
    canonical = json.dumps(snapshot, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def render_notification(snapshot: dict[str, Any], audit: dict[str, Any] | None, *, initial: bool) -> str:
    paperclip_issue = snapshot["paperclipIssue"]
    hermes_issue = snapshot["hermesIssue"]
    release = snapshot["paperclipRelease"]
    lines = ["Control-plane upstream promotion-gate update:"]
    lines.append(
        f"- Paperclip #{paperclip_issue['number']}: {paperclip_issue['state']} "
        f"({paperclip_issue['commentCount']} comment(s)) — {paperclip_issue['url']}"
    )
    lines.append(f"- Latest Paperclip npm release: {release['version']}")
    if audit:
        counts = audit["productionVulnerabilities"]
        lines.append(
            f"- Published-package gate: {audit['promotionGate']} "
            f"(critical={counts.get('critical', 0)}, high={counts.get('high', 0)}, "
            f"moderate={counts.get('moderate', 0)}; undici={','.join(audit['undiciVersions']) or 'none'})"
        )
    lines.append(
        f"- Hermes #{hermes_issue['number']}: {hermes_issue['state']} "
        f"({hermes_issue['commentCount']} comment(s)) — {hermes_issue['url']}"
    )
    if initial:
        lines.append("- Baseline established; future unchanged checks stay silent.")
    lines.append("- No service, gateway, worker, credential wiring, or production change was started.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", default=".pilot-cache/control-plane-watch/state.json")
    parser.add_argument("--report-dir", default=".pilot-cache/control-plane-watch/reports")
    parser.add_argument("--force-audit", action="store_true")
    parser.add_argument("--emit-initial", action="store_true")
    args = parser.parse_args()

    root = repository_root()
    state_path = require_cache_path(root / args.state, root, "state path")
    report_dir = require_cache_path(root / args.report_dir, root, "report directory")
    cache_root = require_cache_path(root / ".pilot-cache" / "control-plane-watch", root, "cache root")
    cache_root.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    empty_npmrc = cache_root / "empty.npmrc"
    empty_npmrc.write_text("registry=https://registry.npmjs.org/\n", encoding="utf-8")
    env = command_environment(npm_user_config=empty_npmrc)

    previous = load_state(state_path)
    snapshot = {
        "schema": "control-plane-upstream-watch-state.v1",
        "checkedAt": utc_now(),
        "paperclipIssue": issue_snapshot(PAPERCLIP_REPO, PAPERCLIP_ISSUE, cwd=root, env=env),
        "hermesIssue": issue_snapshot(HERMES_REPO, HERMES_ISSUE, cwd=root, env=env),
        "paperclipRelease": npm_release_snapshot(cwd=root, env=env),
    }
    audit = audit_paperclip_release(snapshot["paperclipRelease"], cache_root=cache_root, env=env)
    atomic_write_json(report_dir / f"paperclip-{audit['version']}.json", audit)
    fingerprint = state_fingerprint(fingerprint_payload(snapshot, audit))
    initial = not previous
    changed = fingerprint != previous.get("fingerprint")

    state_payload = {
        "schema": "control-plane-upstream-watch-state.v1",
        "updatedAt": utc_now(),
        "fingerprint": fingerprint,
        "snapshot": snapshot,
        "latestAuditReport": f"paperclip-{snapshot['paperclipRelease']['version']}.json" if audit else None,
        "execution_status": "ok",
        "outcome_status": audit["promotionGate"] if audit else "OBSERVED",
    }
    atomic_write_json(state_path, state_payload)

    if changed and (not initial or args.emit_initial):
        print(render_notification(snapshot, audit, initial=initial))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
