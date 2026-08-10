#!/usr/bin/env python3
"""Validate catalog, graph, generated views and local documentation links."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_markdown_links(errors: list[str]) -> None:
    link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    for path in [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]:
        text = path.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip().split(" ", 1)[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = unquote(target.split("#", 1)[0])
            if not target_path:
                continue
            resolved = (path.parent / target_path).resolve()
            if not resolved.exists():
                fail(errors, f"broken local link in {path.relative_to(ROOT)}: {target}")


def main() -> int:
    errors: list[str] = []
    seed = json.loads((ROOT / "data" / "catalog-seed.json").read_text(encoding="utf-8"))
    catalog = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
    graph = json.loads((ROOT / "data" / "knowledge-graph.json").read_text(encoding="utf-8"))

    seed_repos = [item["repo"] for item in seed["projects"]]
    projects = catalog["projects"]
    catalog_repos = [item["repo"] for item in projects]
    if seed_repos != catalog_repos:
        fail(errors, "catalog project order/content does not match the seed")
    if len(seed_repos) != len(set(seed_repos)):
        fail(errors, "duplicate repositories in catalog seed")

    threshold = seed["starThreshold"]
    for project in projects:
        if project["stars"] < threshold and not project["strategicException"]:
            fail(errors, f"unexpected below-threshold project: {project['repo']}")
        if project["strategicException"] != (project["priority"] == "strategic-exception"):
            fail(errors, f"strategic-exception mismatch: {project['repo']}")
        expected_license_review = project["license"] in {"NOASSERTION", "OTHER"}
        if project["licenseReviewRequired"] != expected_license_review:
            fail(errors, f"license review flag mismatch: {project['repo']}")
        if project["archived"]:
            fail(errors, f"archived project in active catalog: {project['repo']}")

    validation = catalog["validation"]
    for field in ("apiFailures", "unexpectedBelowThreshold", "archived", "duplicateRepos"):
        if validation[field]:
            fail(errors, f"catalog validation.{field} is not empty: {validation[field]}")

    expected_counts = {
        "seeded": len(seed_repos),
        "resolved": len(projects),
        "thresholdProjects": sum(project["meetsStarThreshold"] for project in projects),
        "strategicExceptions": sum(project["strategicException"] for project in projects),
        "categories": len({project["category"] for project in projects}),
    }
    if catalog["counts"] != expected_counts:
        fail(errors, f"catalog counts mismatch: expected {expected_counts}, got {catalog['counts']}")

    project_nodes = [node for node in graph["nodes"] if node["type"] == "project"]
    graph_repos = [node["id"].removeprefix("project:") for node in project_nodes]
    if sorted(graph_repos) != sorted(catalog_repos):
        fail(errors, "knowledge graph does not contain exactly one node for every project")
    classified = {
        edge["source"].removeprefix("project:")
        for edge in graph["edges"]
        if edge["type"] == "classified-as"
    }
    recommended = {
        edge["source"].removeprefix("project:")
        for edge in graph["edges"]
        if edge["type"] == "recommended-as"
    }
    if classified != set(catalog_repos):
        fail(errors, "not every project has a classified-as edge")
    if recommended != set(catalog_repos):
        fail(errors, "not every project has a recommended-as edge")
    if graph["counts"] != {"nodes": len(graph["nodes"]), "edges": len(graph["edges"])}:
        fail(errors, "knowledge graph counts mismatch")

    with (ROOT / "data" / "projects.csv").open(encoding="utf-8", newline="") as handle:
        csv_repos = [row["repo"] for row in csv.DictReader(handle)]
    if csv_repos != catalog_repos:
        fail(errors, "projects.csv does not match projects.json")

    with (ROOT / "data" / "knowledge-graph-nodes.csv").open(encoding="utf-8", newline="") as handle:
        node_rows = list(csv.DictReader(handle))
    with (ROOT / "data" / "knowledge-graph-edges.csv").open(encoding="utf-8", newline="") as handle:
        edge_rows = list(csv.DictReader(handle))
    if len(node_rows) != len(graph["nodes"]):
        fail(errors, "knowledge-graph-nodes.csv row count mismatch")
    if len(edge_rows) != len(graph["edges"]):
        fail(errors, "knowledge-graph-edges.csv row count mismatch")

    rendered_catalog = (ROOT / "docs" / "catalog.md").read_text(encoding="utf-8")
    for repo in catalog_repos:
        if f"[{repo}](https://github.com/" not in rendered_catalog:
            fail(errors, f"project missing from rendered catalog: {repo}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for expected in (
        f"**{expected_counts['resolved']}** curated projects",
        f"**{expected_counts['thresholdProjects']}** at or above",
        f"**{expected_counts['strategicExceptions']}** lower-star strategic exceptions",
        f"**{expected_counts['categories']}** primary categories",
    ):
        if expected not in readme:
            fail(errors, f"README snapshot count is stale or missing: {expected}")

    priority_by_repo = {project["repo"]: project["priority"] for project in projects}
    if priority_by_repo.get("NousResearch/hermes-agent") != "adopt-core":
        fail(errors, "Hermes Agent must remain adopt-core unless the architecture decision changes")
    if priority_by_repo.get("paperclipai/paperclip") != "pilot":
        fail(errors, "Paperclip posture must remain pilot unless its assessment is updated")

    validate_markdown_links(errors)

    if errors:
        print("validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"validated {len(projects)} projects, {len(graph['nodes'])} graph nodes, "
        f"{len(graph['edges'])} graph edges and local documentation links"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
