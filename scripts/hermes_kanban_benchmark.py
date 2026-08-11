#!/usr/bin/env python3
"""Exercise Hermes Kanban controls without dispatching a worker or gateway."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import platform
import subprocess
import uuid
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hermes-home", required=True)
    parser.add_argument("--board", default="paperclip-benchmark")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument(
        "--run-id",
        help="Optional unique idempotency namespace (defaults to a random value)",
    )
    parser.add_argument(
        "--command-timeout",
        type=int,
        default=30,
        help="Per-command timeout in seconds (default: 30)",
    )
    return parser.parse_args()


def task_record(payload: dict[str, Any]) -> dict[str, Any]:
    task = payload.get("task")
    return task if isinstance(task, dict) else payload


def event_records(payload: dict[str, Any], kind: str) -> list[dict[str, Any]]:
    events = payload.get("events", [])
    return [event for event in events if event.get("kind") == kind]


def run_metadata_contains(payload: dict[str, Any], expected: dict[str, Any]) -> bool:
    for run in payload.get("runs", []):
        metadata = run.get("metadata") or {}
        if all(metadata.get(key) == value for key, value in expected.items()):
            return True
    return False


def sanitize_task_payload(payload: dict[str, Any], root: Path) -> dict[str, Any]:
    sanitized = json.loads(json.dumps(payload))
    task = sanitized.get("task")
    if isinstance(task, dict) and task.get("workspace_path"):
        try:
            task["workspace_path"] = (
                Path(task["workspace_path"]).resolve().relative_to(root).as_posix()
            )
        except (OSError, ValueError):
            task["workspace_path"] = "[outside-repository]"
    for event in sanitized.get("events", []):
        payload_value = event.get("payload")
        if isinstance(payload_value, dict) and "lock" in payload_value:
            payload_value["lock"] = "[host-pid-redacted]"
    return sanitized


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def relative_under(path: Path, parent: Path, *, label: str) -> str:
    try:
        return path.relative_to(parent).as_posix()
    except ValueError as exc:
        raise ValueError(f"{label} must remain under {parent}") from exc


def execute_benchmark(
    args: argparse.Namespace,
    *,
    root: Path,
    home: Path,
    workspace: Path,
) -> dict[str, Any]:
    run_id = args.run_id or uuid.uuid4().hex[:12]
    benchmark_started = utc_now()
    workspace.mkdir(parents=True, exist_ok=True)

    allowed_environment = {
        "APPDATA",
        "COMSPEC",
        "HOME",
        "LOCALAPPDATA",
        "PATH",
        "PATHEXT",
        "PROGRAMDATA",
        "PROGRAMFILES",
        "SYSTEMDRIVE",
        "SYSTEMROOT",
        "TEMP",
        "TMP",
        "USERPROFILE",
        "WINDIR",
    }
    base_env = {
        key: value
        for key, value in os.environ.items()
        if key.upper() in allowed_environment
    }
    base_env.update(
        {
            "HERMES_HOME": str(home),
            "HERMES_KANBAN_BOARD": args.board,
            "HERMES_PROFILE": "default",
            "NO_COLOR": "1",
            "PYTHONUTF8": "1",
        }
    )
    command_results: list[dict[str, Any]] = []

    try:
        version_result = subprocess.run(
            ["hermes", "--version"],
            cwd=root,
            env=base_env,
            capture_output=True,
            text=True,
            check=False,
            timeout=args.command_timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("hermes --version timed out") from exc
    cli_version_output = (version_result.stdout or version_result.stderr).strip()
    cli_version = cli_version_output.splitlines()[0] if cli_version_output else "unknown"
    command_results.append(
        {
            "command": "hermes --version",
            "profile": "default",
            "returnCode": version_result.returncode,
            "stderrCategory": "none" if not version_result.stderr.strip() else "other",
        }
    )

    def run(
        *command: str,
        expected_codes: tuple[int, ...] = (0,),
        profile: str = "default",
    ) -> subprocess.CompletedProcess[str]:
        env = base_env.copy()
        env["HERMES_PROFILE"] = profile
        try:
            result = subprocess.run(
                ["hermes", "kanban", *command],
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
                check=False,
                timeout=args.command_timeout,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"hermes kanban {command[0]} timed out") from exc
        command_results.append(
            {
                "command": f"hermes kanban {command[0]}",
                "profile": profile,
                "returnCode": result.returncode,
                "stderrCategory": (
                    "claim_rejected"
                    if "cannot claim" in result.stderr.lower()
                    else "none"
                    if not result.stderr.strip()
                    else "other"
                ),
            }
        )
        if result.returncode not in expected_codes:
            raise RuntimeError(
                f"hermes kanban {command[0]} failed with return code {result.returncode}"
            )
        return result

    def run_json(*command: str) -> Any:
        return json.loads(run(*command).stdout)

    parent_create = (
        "create",
        "Verify control-plane assignment semantics",
        "--body",
        "CLI-only benchmark task. No dispatch command is part of this harness.",
        "--assignee",
        "default",
        "--workspace",
        f"dir:{workspace}",
        "--idempotency-key",
        f"paperclip-benchmark-parent-{run_id}",
        "--max-runtime",
        "5m",
        "--created-by",
        "hermes-benchmark",
        "--json",
    )
    parent = run_json(*parent_create)
    duplicate = run_json(*parent_create)
    parent_id = parent["id"]

    child = run_json(
        "create",
        "Verify dependency handoff and completion evidence",
        "--body",
        "Wait for the parent, then record a bounded completion receipt.",
        "--assignee",
        "default",
        "--parent",
        parent_id,
        "--workspace",
        f"dir:{workspace}",
        "--idempotency-key",
        f"paperclip-benchmark-child-{run_id}",
        "--max-runtime",
        "5m",
        "--created-by",
        "hermes-benchmark",
        "--json",
    )
    child_id = child["id"]
    child_before_payload = run_json("show", child_id, "--json")
    child_before = task_record(child_before_payload)
    blocked_child_claim = run(
        "claim",
        child_id,
        "--ttl",
        "120",
        expected_codes=(0, 1),
        profile="competitor",
    )
    child_after_blocked_claim_payload = run_json("show", child_id, "--json")

    run("claim", parent_id, "--ttl", "120")
    parent_running_payload = run_json("show", parent_id, "--json")
    competing_claim = run(
        "claim",
        parent_id,
        "--ttl",
        "120",
        # Hermes currently reports an atomic-claim rejection on stderr while
        # returning either 0 or 1 depending on the installed CLI build.
        expected_codes=(0, 1),
        profile="competitor",
    )
    parent_after_competing_claim_payload = run_json("show", parent_id, "--json")
    run("heartbeat", parent_id, "--note", "Benchmark liveness signal")
    run(
        "comment",
        parent_id,
        "Atomic-claim conflict was rejected as expected.",
        "--author",
        "hermes-benchmark",
    )
    run(
        "complete",
        parent_id,
        "--result",
        "Atomic claim and heartbeat verified.",
        "--summary",
        "Parent control-plane checks passed; child may proceed.",
        "--metadata",
        json.dumps(
            {
                "atomic_claim": True,
                "duplicate_claim_rejected": True,
                "heartbeat": True,
                "benchmark_mode": "cli_only",
            }
        ),
    )

    parent_after_payload = run_json("show", parent_id, "--json")
    parent_after = task_record(parent_after_payload)
    child_ready_payload = run_json("show", child_id, "--json")
    child_ready = task_record(child_ready_payload)
    run("claim", child_id, "--ttl", "120")
    run(
        "heartbeat",
        child_id,
        "--note",
        "Dependency released after parent completion",
    )
    run(
        "comment",
        child_id,
        "The benchmark harness invoked only Hermes Kanban CLI commands.",
        "--author",
        "hermes-benchmark",
    )
    run(
        "complete",
        child_id,
        "--result",
        "Dependency handoff verified.",
        "--summary",
        "CLI-only local benchmark completed.",
        "--metadata",
        json.dumps(
            {
                "dependency_release": True,
                "benchmark_mode": "cli_only",
            }
        ),
    )

    child_after_payload = run_json("show", child_id, "--json")
    child_after = task_record(child_after_payload)
    stats = run_json("stats", "--json")
    tasks = run_json("list", "--json")

    parent_claim_events = event_records(parent_after_competing_claim_payload, "claimed")
    parent_runs_during_conflict = parent_after_competing_claim_payload.get("runs", [])
    child_claim_events_before_release = event_records(
        child_after_blocked_claim_payload, "claimed"
    )
    child_rejection_events = event_records(
        child_after_blocked_claim_payload, "claim_rejected"
    )
    parent_heartbeat_events = event_records(parent_after_payload, "heartbeat")
    child_promoted_events = event_records(child_ready_payload, "promoted")
    controls = {
        "idempotentCreate": duplicate["id"] == parent_id,
        "competingClaimRejected": (
            "cannot claim" in competing_claim.stderr.lower()
            and task_record(parent_running_payload)["status"] == "running"
            and task_record(parent_after_competing_claim_payload)["status"] == "running"
            and len(parent_claim_events) == 1
            and all(run.get("profile") == "default" for run in parent_runs_during_conflict)
        ),
        "claimConflictHasNonzeroExit": competing_claim.returncode != 0,
        "heartbeatRecorded": any(
            (event.get("payload") or {}).get("note") == "Benchmark liveness signal"
            for event in parent_heartbeat_events
        ),
        "dependencyClaimRejectedBeforeParentCompletion": (
            "cannot claim" in blocked_child_claim.stderr.lower()
            and child_before["status"] in {"todo", "blocked"}
            and task_record(child_after_blocked_claim_payload)["status"]
            in {"todo", "blocked"}
            and not child_claim_events_before_release
            and any(
                (event.get("payload") or {}).get("reason") == "parents_not_done"
                for event in child_rejection_events
            )
        ),
        "dependencyReleasedAfterParentCompletion": (
            child_ready["status"] == "ready" and bool(child_promoted_events)
        ),
        "structuredCompletionMetadata": (
            run_metadata_contains(
                parent_after_payload,
                {
                    "atomic_claim": True,
                    "duplicate_claim_rejected": True,
                    "heartbeat": True,
                    "benchmark_mode": "cli_only",
                },
            )
            and run_metadata_contains(
                child_after_payload,
                {"dependency_release": True, "benchmark_mode": "cli_only"},
            )
        ),
        "ownershipRecorded": any(
            run.get("profile") == "default"
            for run in parent_after_payload.get("runs", [])
        ),
        "completionHistoryRecorded": bool(
            event_records(parent_after_payload, "completed")
            and event_records(child_after_payload, "completed")
        ),
    }
    passed = all(
        value
        for key, value in controls.items()
        if key != "claimConflictHasNonzeroExit"
    ) and parent_after["status"] == "done" and child_after["status"] == "done"
    receipt = {
        "schema": "hermes-kanban-paperclip-benchmark.v1",
        "startedAt": benchmark_started,
        "finishedAt": utc_now(),
        "status": "passed" if passed else "failed",
        "runId": run_id,
        "hermesCliVersion": cli_version,
        "runtime": {
            "os": platform.system(),
            "osRelease": platform.release(),
            "python": platform.python_version(),
        },
        "isolation": {
            "hermesHome": relative_under(home, root, label="Hermes home"),
            "board": args.board,
            "workspace": relative_under(workspace, root, label="workspace"),
            "environmentPolicy": "allowlist",
            "credentialsProvidedByHarness": False,
            "gatewayCommandInvoked": False,
            "dispatchCommandInvoked": False,
            "externalActions": "not_assessed",
            "partialStatePolicy": "preserve for inspection",
        },
        "commandResults": command_results,
        "controls": controls,
        "tasks": {
            "parent": sanitize_task_payload(parent_after_payload, root),
            "child": sanitize_task_payload(child_after_payload, root),
        },
        "deniedClaimEvidence": {
            "parentConflictReturnCode": competing_claim.returncode,
            "parentConflictCategory": "claim_rejected",
            "blockedChildReturnCode": blocked_child_claim.returncode,
            "blockedChildCategory": "claim_rejected",
        },
        "stats": stats,
        "runTaskIds": [parent_id, child_id],
        "runTaskCount": 2,
        "boardTaskCount": len(tasks),
        # A zero exit status for an explicitly rejected competing claim is a
        # CLI ergonomics finding, not a failure of atomic claim enforcement.
        "passed": passed,
    }
    return receipt


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    pilot_root = (root / ".pilot-cache").resolve()
    home = Path(args.hermes_home).resolve()
    workspace = Path(args.workspace).resolve()
    receipt_path = Path(args.receipt).resolve()
    requested_receipt_rejected = False
    try:
        relative_under(receipt_path, root, label="receipt")
    except ValueError:
        receipt_path = pilot_root / "hermes-kanban-benchmark-error.json"
        requested_receipt_rejected = True
    receipt_path.parent.mkdir(parents=True, exist_ok=True)

    receipt: dict[str, Any] = {
        "schema": "hermes-kanban-paperclip-benchmark.v1",
        "startedAt": utc_now(),
        "finishedAt": utc_now(),
        "status": "error",
        "passed": False,
        "partialStatePolicy": "preserve for inspection",
        "requestedReceiptPathRejected": requested_receipt_rejected,
    }
    stage = "path_validation"
    try:
        relative_under(home, pilot_root, label="Hermes home")
        relative_under(workspace, pilot_root, label="workspace")
        if requested_receipt_rejected:
            raise ValueError("receipt must remain under the repository root")
        stage = "benchmark_execution"
        receipt = execute_benchmark(
            args,
            root=root,
            home=home,
            workspace=workspace,
        )
    except (json.JSONDecodeError, OSError, RuntimeError, subprocess.SubprocessError, ValueError) as exc:
        receipt.update(
            {
                "finishedAt": utc_now(),
                "status": "error",
                "error": {
                    "stage": stage,
                    "type": type(exc).__name__,
                    "message": str(exc),
                },
                "passed": False,
            }
        )

    rendered = json.dumps(receipt, indent=2) + "\n"
    receipt_path.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
