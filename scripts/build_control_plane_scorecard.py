#!/usr/bin/env python3
"""Build a sanitized scorecard for a bounded Hermes Kanban workflow."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_identity_validator(root: Path):
    path = root / "scripts" / "validate_task_identity.py"
    spec = importlib.util.spec_from_file_location("validate_task_identity", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load task identity validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def safe_environment() -> dict[str, str]:
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
        "USERPROFILE",
        "HOMEDRIVE",
        "HOMEPATH",
        "USERNAME",
        "TERM",
        "MSYSTEM",
    }
    return {key: value for key, value in os.environ.items() if key.upper() in allowed}


def run_json(command: list[str], *, cwd: Path, env: dict[str, str]) -> Any:
    executable = shutil.which(command[0], path=env.get("PATH"))
    if executable is None:
        raise RuntimeError(f"required command is unavailable: {command[0]}")
    result = subprocess.run(
        [executable, *command[1:]],
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"{command[0]} scorecard command failed")
    return json.loads(result.stdout)


def safe_task_summary(payload: dict[str, Any]) -> dict[str, Any]:
    task = payload.get("task") or payload
    events = payload.get("events") or []
    runs = payload.get("runs") or []
    event_counts = Counter(event.get("kind", "unknown") for event in events)
    return {
        "taskId": task["id"],
        "title": task["title"],
        "status": task["status"],
        "assignee": task.get("assignee"),
        "tenant": task.get("tenant"),
        "eventCounts": dict(sorted(event_counts.items())),
        "runCount": len(runs),
        "completedRunCount": sum(run.get("outcome") == "completed" for run in runs),
        "workerPidCount": sum(run.get("worker_pid") is not None for run in runs),
    }


def scorecard_inputs_bound(
    identity: dict[str, Any],
    board: str,
    task_ids: list[str],
    proof: dict[str, Any],
) -> bool:
    hermes = identity["systems"]["hermes"]
    expected_ids = hermes["workflowTaskIds"]
    return all(
        (
            board == hermes["board"],
            task_ids == expected_ids,
            len(set(task_ids)) == len(task_ids),
            proof.get("canonicalTaskId") == identity["canonicalTaskId"],
            proof.get("board") == board,
            proof.get("beforeCount") == len(task_ids),
            proof.get("afterCount") == len(task_ids),
            proof.get("replayTaskId") in task_ids,
            proof.get("idempotent") is True,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--board", required=True)
    parser.add_argument("--task-id", action="append", required=True)
    parser.add_argument("--identity", type=Path, required=True)
    parser.add_argument("--idempotency-proof", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    root = repository_root()
    receipt = args.receipt if args.receipt.is_absolute() else root / args.receipt
    identity_path = args.identity if args.identity.is_absolute() else root / args.identity
    proof_path = args.idempotency_proof if args.idempotency_proof.is_absolute() else root / args.idempotency_proof
    for path, label in ((receipt, "receipt"), (identity_path, "identity"), (proof_path, "proof")):
        try:
            path.resolve().relative_to(root.resolve())
        except ValueError as exc:
            raise SystemExit(f"{label} path must remain inside the repository") from exc

    identity = json.loads(identity_path.read_text(encoding="utf-8"))
    idempotency = json.loads(proof_path.read_text(encoding="utf-8"))
    validator = load_identity_validator(root)
    static_errors = validator.validate_record(identity)
    if static_errors:
        raise RuntimeError(f"identity validation failed: {static_errors}")
    if not scorecard_inputs_bound(identity, args.board, args.task_id, idempotency):
        raise RuntimeError("scorecard task IDs or idempotency evidence are not bound to the canonical identity")
    reconciliation = validator.reconcile_live(identity, root)

    env = safe_environment()
    env["HERMES_HOME"] = str((root / ".pilot-cache" / "hermes-home").resolve())
    tasks = [
        safe_task_summary(
            run_json(
                ["hermes", "kanban", "--board", args.board, "show", task_id, "--json"],
                cwd=root,
                env=env,
            )
        )
        for task_id in args.task_id
    ]
    job_id = identity["scheduler"]["jobId"]
    registry_path = Path(env["LOCALAPPDATA"]) / "hermes" / "cron" / "jobs.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    matching_jobs = [job for job in registry.get("jobs", []) if job.get("id") == job_id or job.get("job_id") == job_id]
    if len(matching_jobs) != 1:
        raise RuntimeError("scheduler owner did not reconcile exactly once")
    scheduler = matching_jobs[0]

    duplicate_run_candidates = sum(max(0, task["runCount"] - 1) for task in tasks)
    worker_pid_count = sum(task["workerPidCount"] for task in tasks)
    done_count = sum(task["status"] == "done" for task in tasks)
    promoted_count = sum(task["eventCounts"].get("promoted", 0) for task in tasks)
    heartbeats = sum(task["eventCounts"].get("heartbeat", 0) for task in tasks)
    all_verified = all(
        (
            done_count == len(tasks),
            idempotency.get("idempotent") is True,
            duplicate_run_candidates == 0,
            worker_pid_count == 0,
            reconciliation.get("reconciled") is True,
            scheduler.get("last_status") == "ok",
            scheduler.get("no_agent") is True,
            scheduler.get("enabled") is True,
            identity["systems"]["paperclip"]["executionAuthority"] is False,
        )
    )
    receipt_payload = {
        "schema": "hermes-kanban-operational-scorecard.v1",
        "generatedAt": utc_now(),
        "execution_status": "ok",
        "outcome_status": "VERIFIED" if all_verified else "HOLD",
        "canonicalTaskId": identity["canonicalTaskId"],
        "board": args.board,
        "tasks": tasks,
        "metrics": {
            "taskCount": len(tasks),
            "doneCount": done_count,
            "orphanedTaskCount": len(tasks) - done_count,
            "heartbeatEventCount": heartbeats,
            "dependencyPromotionEventCount": promoted_count,
            "duplicateRunCandidateCount": duplicate_run_candidates,
            "workerPidCount": worker_pid_count,
            "idempotencyReplayPreservedTaskCount": bool(idempotency.get("idempotent")),
            "githubReferencesReconciled": len(reconciliation.get("github") or []),
            "recoveryExercise": "not_assessed",
            "externalActivity": "not_assessed"
        },
        "scheduler": {
            "jobId": job_id,
            "ownerCount": len(matching_jobs),
            "enabled": bool(scheduler.get("enabled")),
            "mode": "script-only" if scheduler.get("no_agent") else "agent",
            "lastStatus": scheduler.get("last_status"),
            "schedule": scheduler.get("schedule"),
        },
        "authority": identity["authority"],
        "paperclip": {
            "integrationStatus": identity["systems"]["paperclip"]["integrationStatus"],
            "executionAuthority": identity["systems"]["paperclip"]["executionAuthority"],
            "publishedReleaseGate": "HOLD",
        },
        "reconciliation": reconciliation,
        "observationalLimits": [
            "No model worker PID was recorded for these manual Kanban runs.",
            "No recovery failure was injected; recovery remains not assessed.",
            "Activity outside the allowlisted workflow commands remains not assessed."
        ],
    }
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(receipt_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"receipt": receipt.relative_to(root).as_posix(), "outcome_status": receipt_payload["outcome_status"]}, indent=2))
    return 0 if all_verified else 1


if __name__ == "__main__":
    raise SystemExit(main())
