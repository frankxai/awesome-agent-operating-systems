#!/usr/bin/env python3
"""Refresh public GitHub metadata for the curated agentic-tech catalog.

Requires an authenticated GitHub CLI (`gh auth status`). The script reads only
`data/catalog-seed.json` and writes deterministic JSON/CSV snapshots in `data/`.
It never clones projects or executes third-party code.
"""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = ROOT / "data" / "catalog-seed.json"
JSON_PATH = ROOT / "data" / "projects.json"
CSV_PATH = ROOT / "data" / "projects.csv"


def gh_repo(repo: str) -> dict[str, Any]:
    process = subprocess.run(
        ["gh", "api", f"repos/{repo}"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if process.returncode != 0:
        detail = process.stderr.strip() or process.stdout.strip()
        raise RuntimeError(f"{repo}: {detail}")
    return json.loads(process.stdout)


def normalize(seed: dict[str, Any], remote: dict[str, Any], threshold: int) -> dict[str, Any]:
    license_data = remote.get("license") or {}
    license_id = license_data.get("spdx_id") or "NOASSERTION"
    stars = int(remote.get("stargazers_count") or 0)
    exception = seed["priority"] == "strategic-exception"
    return {
        "repo": remote["full_name"],
        "url": remote["html_url"],
        "description": (remote.get("description") or "").strip(),
        "category": seed["category"],
        "priority": seed["priority"],
        "why": str(seed["why"]).strip(),
        "stars": stars,
        "forks": int(remote.get("forks_count") or 0),
        "openIssues": int(remote.get("open_issues_count") or 0),
        "language": remote.get("language"),
        "license": license_id,
        "licenseReviewRequired": license_id in {"NOASSERTION", "OTHER"},
        "createdAt": remote.get("created_at"),
        "updatedAt": remote.get("updated_at"),
        "pushedAt": remote.get("pushed_at"),
        "defaultBranch": remote.get("default_branch"),
        "archived": bool(remote.get("archived")),
        "fork": bool(remote.get("fork")),
        "starThreshold": threshold,
        "meetsStarThreshold": stars >= threshold,
        "strategicException": exception,
    }


def main() -> int:
    seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    threshold = int(seed["starThreshold"])
    rows_by_repo: dict[str, dict[str, Any]] = {}
    failures: list[str] = []

    projects = seed["projects"]
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(gh_repo, item["repo"]): item for item in projects}
        for future in as_completed(futures):
            item = futures[future]
            try:
                rows_by_repo[item["repo"]] = normalize(item, future.result(), threshold)
            except Exception as exc:  # noqa: BLE001 - aggregate every public API failure
                failures.append(str(exc))

    rows = [rows_by_repo[item["repo"]] for item in projects if item["repo"] in rows_by_repo]
    below_threshold = [
        row["repo"]
        for row in rows
        if not row["meetsStarThreshold"] and not row["strategicException"]
    ]
    archived = [row["repo"] for row in rows if row["archived"]]
    duplicate_repos = sorted(
        {item["repo"] for item in projects if sum(p["repo"] == item["repo"] for p in projects) > 1}
    )

    snapshot = {
        "schema": "awesome-agentic-tech.catalog.v1",
        "generatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source": "GitHub REST API via authenticated gh CLI",
        "starThreshold": threshold,
        "selectionPolicy": {
            "rule": "Curated operational relevance first; normally 10,000+ stars and publicly inspectable source.",
            "exceptions": "Lower-star projects require priority=strategic-exception and a specific architectural reason.",
            "warning": "Stars are discovery signals, not quality, security, open-source license, or adoption verdicts. NOASSERTION/OTHER licenses require manual review.",
        },
        "counts": {
            "seeded": len(projects),
            "resolved": len(rows),
            "thresholdProjects": sum(row["meetsStarThreshold"] for row in rows),
            "strategicExceptions": sum(row["strategicException"] for row in rows),
            "categories": len({row["category"] for row in rows}),
        },
        "validation": {
            "apiFailures": sorted(failures),
            "unexpectedBelowThreshold": below_threshold,
            "archived": archived,
            "duplicateRepos": duplicate_repos,
        },
        "projects": rows,
    }

    JSON_PATH.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    fieldnames = [
        "repo", "url", "category", "priority", "stars", "language", "license", "licenseReviewRequired",
        "meetsStarThreshold", "strategicException", "updatedAt", "pushedAt", "why", "description",
    ]
    with CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps(snapshot["counts"], indent=2))
    if failures or below_threshold or archived or duplicate_repos:
        print(json.dumps(snapshot["validation"], indent=2), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
