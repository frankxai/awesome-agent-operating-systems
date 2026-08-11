#!/usr/bin/env python3
"""Render human-readable catalog views from data/projects.json."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "projects.json"
CATALOG_DOC = ROOT / "docs" / "catalog.md"
RUST_DOC = ROOT / "docs" / "rust-landscape.md"

CATEGORY_ORDER = [
    "control-plane", "coding-control-plane", "interaction-ui", "agent-runtime", "coding-agent",
    "agent-framework", "agent-builder", "structured-output", "agent-training", "durable-execution", "workflow-automation",
    "protocol", "tools-integration", "memory", "knowledge-graph", "rag-platform",
    "vector-database", "document-ingestion", "eval-security", "observability",
    "sandbox-security", "identity-secrets", "browser-computer-use", "model-gateway", "model-runtime",
    "voice-realtime", "creative-media", "data-integration", "domain-platform", "rust-runtime",
]


def star_text(stars: int) -> str:
    return f"{stars:,}"


def license_text(project: dict) -> str:
    license_id = project["license"]
    return f"{license_id} ⚠ review" if project["licenseReviewRequired"] else license_id


def project_table(projects: list[dict]) -> list[str]:
    lines = [
        "| Project | Stars | Language | License | Recommendation | Why it matters |",
        "|---|---:|---|---|---|---|",
    ]
    for project in sorted(projects, key=lambda item: (-item["stars"], item["repo"].lower())):
        description = project["why"].replace("|", "\\|")
        lines.append(
            f"| [{project['repo']}]({project['url']}) | {star_text(project['stars'])} | "
            f"{project['language'] or '—'} | {license_text(project)} | `{project['priority']}` | {description} |"
        )
    return lines


def render_catalog(catalog: dict) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for project in catalog["projects"]:
        grouped[project["category"]].append(project)

    counts = catalog["counts"]
    lines = [
        "# Agentic Tech Catalog",
        "",
        f"Snapshot: **{catalog['generatedAt']}** · **{counts['thresholdProjects']}** projects at or above "
        f"{catalog['starThreshold']:,} stars · **{counts['strategicExceptions']}** strategic exceptions · "
        f"**{counts['categories']}** categories.",
        "",
        "> Stars are a discovery filter, not a quality or adoption score. `NOASSERTION` and `OTHER` license values "
        "are not treated as verified open-source licenses and require manual review before reuse or deployment.",
        "",
        "The machine-readable source is [`data/projects.json`](../data/projects.json); regenerate with "
        "`python scripts/refresh_catalog.py && python scripts/render_catalog.py`.",
        "",
        "## Categories",
        "",
    ]
    for category in CATEGORY_ORDER:
        if category in grouped:
            lines.append(f"- [{category}](#{category}) ({len(grouped[category])})")
    for category in sorted(set(grouped) - set(CATEGORY_ORDER)):
        lines.append(f"- [{category}](#{category}) ({len(grouped[category])})")

    for category in CATEGORY_ORDER + sorted(set(grouped) - set(CATEGORY_ORDER)):
        if category not in grouped:
            continue
        lines.extend(["", f"## {category}", ""])
        lines.extend(project_table(grouped[category]))

    lines.extend([
        "",
        "## Selection and safety notes",
        "",
        "- A project appears once under its primary architectural role; many span multiple roles in practice.",
        "- The 10k-star threshold captures ecosystem signal but can lag technical quality and can be gamed.",
        "- `strategic-exception` is reserved for lower-star projects with a specific architecture, Rust, durability, or sovereignty reason.",
        "- Installation requires a separate security, license, activity, release, and operational-fit review.",
        "- Archived repositories and unresolved API failures fail catalog validation.",
        "",
    ])
    return "\n".join(lines)


def render_rust(catalog: dict) -> str:
    projects = [
        project for project in catalog["projects"]
        if project["language"] == "Rust" or project["category"] == "rust-runtime"
    ]
    lines = [
        "# Rust and Rust-backed Agentic Technology",
        "",
        "Rust is strongest today in **execution edges**—coding agents, local runtimes, browser control, sandboxes, "
        "databases, inference and durable primitives—not in company-level governance control planes.",
        "",
        "## Current shortlist",
        "",
        *project_table(projects),
        "",
        "## Paperclip-alternative verdict",
        "",
        "There is no feature-complete Rust substitute for Paperclip's combination of goals, org chart, issue checkout, "
        "approvals, budgets, cost accounting, adapter registry and operator UI. The closest Rust-backed options are narrower:",
        "",
        "- **Vibe Kanban** — best lightweight coding-agent fleet board; strong pilot candidate for software-only lanes.",
        "- **OpenFang / ZeroClaw / Goose** — execution runtimes, not governance planes.",
        "- **Rig / BAML** — libraries and typed application boundaries, not operator products.",
        "- **Restate / Windmill / Hatchet** — durable execution/workflow substrates, not agent-company management.",
        "- **CubeSandbox / agent-browser / Qdrant** — excellent Rust edge primitives that can sit beneath Hermes or Paperclip.",
        "",
        "A Rust rewrite of Paperclip would not currently improve Frank's bottleneck: orchestration correctness, identity, "
        "work ownership, approvals and evidence are more important than control-plane CPU throughput. Prefer a TypeScript "
        "control plane with Rust workers and infrastructure where isolation, latency or density matters.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    CATALOG_DOC.write_text(render_catalog(catalog), encoding="utf-8")
    RUST_DOC.write_text(render_rust(catalog), encoding="utf-8")
    print(f"rendered {CATALOG_DOC.relative_to(ROOT)} and {RUST_DOC.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
