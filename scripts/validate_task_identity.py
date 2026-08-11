#!/usr/bin/env python3
"""Validate and optionally reconcile a control-plane task identity record."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

CANONICAL_ID = re.compile(r"^ctid:v1:[a-z0-9][a-z0-9-]{1,62}:[a-z0-9][a-z0-9-]{1,94}$")
TASK_ID = re.compile(r"^t_[a-f0-9]{8}$")
JOB_ID = re.compile(r"^[a-f0-9]{12}$")
ISSUE_URL = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/issues/([0-9]+)$")
ABSOLUTE_PATH = re.compile(
    r"(?:^|[\\s\"'(])(?:[A-Za-z]:[\\/]|/c/Users/|\\\\[^\\]+\\)",
    re.IGNORECASE,
)
SECRET_PATTERN = re.compile(
    r"(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)",
    re.IGNORECASE,
)
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "data" / "schemas" / "control-plane-task-identity.schema.json"


def repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def walk_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item)


def validate_record(record: dict[str, Any]) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    schema_validator = Draft202012Validator(schema, format_checker=FormatChecker())
    schema_errors = sorted(
        schema_validator.iter_errors(record),
        key=lambda error: [str(part) for part in error.absolute_path],
    )
    errors = [
        f"schema {'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in schema_errors
    ]
    if errors:
        return errors
    if record["schemaVersion"] != "starlight.control-plane-task-identity.v1":
        errors.append("unsupported schemaVersion")
    if not CANONICAL_ID.fullmatch(str(record["canonicalTaskId"])):
        errors.append("canonicalTaskId does not match ctid:v1:<scope>:<slug>")
    if str(record["canonicalTaskId"]).split(":")[2] != record["scope"]:
        errors.append("scope must be embedded in canonicalTaskId")
    try:
        datetime.fromisoformat(str(record["createdAt"]).replace("Z", "+00:00"))
    except ValueError:
        errors.append("createdAt must be an ISO-8601 timestamp")

    authority = record.get("authority") or {}
    expected_authority = {
        "taskState": "hermes-kanban",
        "deliveryEvidence": "git-github",
        "scheduler": "hermes-cron",
        "fleetRouting": "starlight-swarm",
    }
    if authority != expected_authority:
        errors.append("authority map does not match the v1 split")

    scheduler = record.get("scheduler") or {}
    if scheduler.get("owner") != "hermes-cron" or scheduler.get("mode") != "script-only":
        errors.append("scheduler must have one hermes-cron script-only owner")
    if not JOB_ID.fullmatch(str(scheduler.get("jobId", ""))):
        errors.append("scheduler.jobId must be a 12-character Hermes cron ID")
    if scheduler.get("duplicateDispatchPolicy") != "NOOP_DUPLICATE":
        errors.append("duplicateDispatchPolicy must be NOOP_DUPLICATE")

    systems = record.get("systems") or {}
    hermes = systems.get("hermes") or {}
    if not TASK_ID.fullmatch(str(hermes.get("taskId", ""))):
        errors.append("systems.hermes.taskId is invalid")
    if not hermes.get("board") or not hermes.get("tenant") or not hermes.get("profile"):
        errors.append("Hermes board, tenant, and profile are required")
    workflow_task_ids = hermes.get("workflowTaskIds") or []
    if hermes.get("taskId") not in workflow_task_ids:
        errors.append("systems.hermes.taskId must appear in workflowTaskIds")

    github = systems.get("github") or {}
    if github.get("deliveryRepository") != "frankxai/awesome-agent-operating-systems":
        errors.append("deliveryRepository must identify the canonical repo")
    issues = github.get("evidenceIssues") or []
    if not issues:
        errors.append("at least one GitHub evidence issue is required")
    for issue in issues:
        match = ISSUE_URL.fullmatch(str(issue.get("url", "")))
        if not match:
            errors.append("GitHub issue URL is invalid")
            continue
        url_repo = f"{match.group(1)}/{match.group(2)}"
        if url_repo.lower() != str(issue.get("repository", "")).lower():
            errors.append(f"GitHub URL/repository mismatch for {issue.get('url')}")
        if int(match.group(3)) != issue.get("number"):
            errors.append(f"GitHub URL/number mismatch for {issue.get('url')}")

    paperclip = systems.get("paperclip") or {}
    if paperclip.get("executionAuthority") is not False:
        errors.append("Paperclip executionAuthority must remain false")
    if paperclip.get("integrationStatus") not in {"not-integrated", "evaluation-only", "approved"}:
        errors.append("Paperclip integrationStatus is invalid")

    if not isinstance(record.get("artifacts"), list) or not record["artifacts"]:
        errors.append("at least one repository-relative artifact is required")
    for text in walk_strings(record):
        if ABSOLUTE_PATH.search(text):
            errors.append("record contains an absolute or network path")
            break
        if SECRET_PATTERN.search(text):
            errors.append("record contains a secret-like value")
            break
    return errors


def validate_scheduler_job(record: dict[str, Any], job: dict[str, Any], root: Path) -> None:
    scheduler = record["scheduler"]
    expected_workdir = (root / scheduler["workdir"]).resolve()
    actual_workdir = Path(str(job.get("workdir", ""))).resolve()
    if actual_workdir != expected_workdir:
        raise RuntimeError("Hermes cron owner workdir does not match the identity contract")
    if job.get("script") != scheduler["script"]:
        raise RuntimeError("Hermes cron owner script does not match the identity contract")
    if not job.get("no_agent"):
        raise RuntimeError("Hermes cron owner is not script-only")
    if not job.get("enabled"):
        raise RuntimeError("Hermes cron owner is disabled")


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


def run_json(command: list[str], *, cwd: Path, env: dict[str, str], timeout: int = 45) -> Any:
    executable = shutil.which(command[0], path=env.get("PATH"))
    if executable is None:
        raise RuntimeError(f"required command is unavailable: {command[0]}")
    result = subprocess.run(
        [executable, *command[1:]],
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"{command[0]} reconciliation command failed")
    return json.loads(result.stdout)


def reconcile_live(record: dict[str, Any], root: Path) -> dict[str, Any]:
    base_env = safe_environment()
    hermes_env = dict(base_env)
    hermes_env["HERMES_HOME"] = str((root / ".pilot-cache" / "hermes-home").resolve())
    hermes_ref = record["systems"]["hermes"]
    task = run_json(
        ["hermes", "kanban", "--board", hermes_ref["board"], "show", hermes_ref["taskId"], "--json"],
        cwd=root,
        env=hermes_env,
    )
    task_payload = task.get("task") or task
    if task_payload.get("id") != hermes_ref["taskId"]:
        raise RuntimeError("Hermes task ID did not reconcile")
    if task_payload.get("tenant") != hermes_ref["tenant"]:
        raise RuntimeError("Hermes tenant did not reconcile")

    issue_results = []
    for issue in record["systems"]["github"]["evidenceIssues"]:
        payload = run_json(
            ["gh", "issue", "view", str(issue["number"]), "--repo", issue["repository"], "--json", "number,state,url"],
            cwd=root,
            env=base_env,
        )
        if payload.get("url") != issue["url"]:
            raise RuntimeError(f"GitHub issue did not reconcile: {issue['repository']}#{issue['number']}")
        issue_results.append({"repository": issue["repository"], "number": issue["number"], "state": payload["state"]})

    registry_path = Path(base_env["LOCALAPPDATA"]) / "hermes" / "cron" / "jobs.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    jobs = registry.get("jobs") or []
    matching = [job for job in jobs if job.get("id") == record["scheduler"]["jobId"] or job.get("job_id") == record["scheduler"]["jobId"]]
    if len(matching) != 1:
        raise RuntimeError("Hermes cron job did not reconcile exactly once")
    job = matching[0]
    validate_scheduler_job(record, job, root)

    return {
        "canonicalTaskId": record["canonicalTaskId"],
        "hermes": {"taskId": task_payload["id"], "status": task_payload["status"], "tenant": task_payload["tenant"]},
        "github": issue_results,
        "scheduler": {
            "jobId": record["scheduler"]["jobId"],
            "enabled": bool(job.get("enabled")),
            "mode": "script-only",
            "script": job.get("script"),
            "workdir": record["scheduler"]["workdir"],
        },
        "paperclipExecutionAuthority": record["systems"]["paperclip"]["executionAuthority"],
        "swarm": "not-required-local-only" if record["systems"]["swarm"] is None else "linked",
        "reconciled": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    root = repository_root()
    record_path = args.record if args.record.is_absolute() else root / args.record
    try:
        record_path.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise SystemExit("identity record must remain inside the repository") from exc
    record = json.loads(record_path.read_text(encoding="utf-8"))
    errors = validate_record(record)
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        return 1
    result: dict[str, Any] = {"valid": True, "canonicalTaskId": record["canonicalTaskId"]}
    if args.live:
        result["live"] = reconcile_live(record, root)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
