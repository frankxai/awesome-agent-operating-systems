#!/usr/bin/env python3
"""Build the machine-readable knowledge graph from the live catalog snapshot."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "projects.json"
GRAPH_PATH = ROOT / "data" / "knowledge-graph.json"
NODES_PATH = ROOT / "data" / "knowledge-graph-nodes.csv"
EDGES_PATH = ROOT / "data" / "knowledge-graph-edges.csv"

CATEGORY_NEEDS = {
    "control-plane": ("govern-work", "governance"),
    "coding-control-plane": ("govern-work", "governance"),
    "interaction-ui": ("interact-with-agents", "interaction"),
    "agent-runtime": ("execute-autonomously", "execution"),
    "coding-agent": ("ship-software", "execution"),
    "agent-framework": ("build-agent-systems", "development"),
    "rust-runtime": ("efficient-sovereign-runtime", "execution"),
    "durable-execution": ("run-reliably", "coordination"),
    "workflow-automation": ("automate-business", "coordination"),
    "agent-builder": ("build-agent-systems", "development"),
    "structured-output": ("build-agent-systems", "development"),
    "agent-training": ("learn-and-optimize", "trust"),
    "protocol": ("interoperate", "interoperability"),
    "tools-integration": ("interoperate", "interoperability"),
    "memory": ("remember-and-learn", "state"),
    "knowledge-graph": ("understand-connected-knowledge", "state"),
    "rag-platform": ("ground-in-evidence", "state"),
    "vector-database": ("ground-in-evidence", "state"),
    "document-ingestion": ("ground-in-evidence", "state"),
    "eval-security": ("measure-and-defend", "trust"),
    "observability": ("observe-and-improve", "trust"),
    "sandbox-security": ("contain-execution", "trust"),
    "identity-secrets": ("secure-identity-and-secrets", "trust"),
    "browser-computer-use": ("act-in-software", "interaction"),
    "model-runtime": ("access-models", "model-infrastructure"),
    "model-gateway": ("access-models", "model-infrastructure"),
    "voice-realtime": ("communicate-naturally", "interaction"),
    "creative-media": ("produce-media", "domain-systems"),
    "data-integration": ("connect-business-data", "domain-systems"),
    "domain-platform": ("operate-business-domains", "domain-systems"),
}

NEEDS = {
    "govern-work": "Goals, org charts, assignments, approvals, budgets and human oversight",
    "interact-with-agents": "Human command, collaboration and review surfaces for agents",
    "execute-autonomously": "Persistent agents that can reason, use tools and complete work",
    "ship-software": "Parallel coding, review, testing and repository delivery",
    "build-agent-systems": "Frameworks and builders for new agent products",
    "learn-and-optimize": "Training, reinforcement learning and measured agent improvement",
    "efficient-sovereign-runtime": "Fast local and Rust-native execution primitives",
    "run-reliably": "Durable, resumable and event-driven long-running jobs",
    "automate-business": "Cross-application business workflows and integrations",
    "interoperate": "Portable protocols, skills, tools and agent interfaces",
    "remember-and-learn": "Long-term memory, consolidation and reusable experience",
    "understand-connected-knowledge": "Temporal and semantic knowledge graphs",
    "ground-in-evidence": "Ingestion, retrieval, indexing and evidence-backed context",
    "measure-and-defend": "Evaluation, red teaming and security checks",
    "observe-and-improve": "Traces, cost, quality and production feedback loops",
    "contain-execution": "Sandboxes, least privilege and blast-radius control",
    "secure-identity-and-secrets": "Identity, authorization and controlled secret custody",
    "act-in-software": "Browser, desktop and computer-use automation",
    "access-models": "Local inference, serving, routing and provider abstraction",
    "communicate-naturally": "Realtime voice and multimodal interaction",
    "produce-media": "Repeatable image, video and creative production",
    "connect-business-data": "Connectors and controlled data movement",
    "operate-business-domains": "Finance, social, internal tools and vertical systems",
}


def main() -> int:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    nodes: list[dict[str, object]] = []
    edges: list[dict[str, str]] = []

    layers = sorted({layer for _, layer in CATEGORY_NEEDS.values()})
    for layer in layers:
        nodes.append({"id": f"layer:{layer}", "type": "layer", "label": layer})

    for need, description in NEEDS.items():
        nodes.append({"id": f"need:{need}", "type": "need", "label": need, "description": description})

    for category, (need, layer) in sorted(CATEGORY_NEEDS.items()):
        nodes.append({"id": f"category:{category}", "type": "category", "label": category})
        edges.append({"source": f"category:{category}", "target": f"need:{need}", "type": "serves"})
        edges.append({"source": f"need:{need}", "target": f"layer:{layer}", "type": "belongs-to"})

    for project in catalog["projects"]:
        project_id = f"project:{project['repo']}"
        nodes.append(
            {
                "id": project_id,
                "type": "project",
                "label": project["repo"],
                "url": project["url"],
                "stars": project["stars"],
                "language": project["language"],
                "license": project["license"],
                "priority": project["priority"],
            }
        )
        edges.append({"source": project_id, "target": f"category:{project['category']}", "type": "classified-as"})
        edges.append({"source": project_id, "target": f"priority:{project['priority']}", "type": "recommended-as"})

    priorities = sorted({project["priority"] for project in catalog["projects"]})
    for priority in priorities:
        nodes.append({"id": f"priority:{priority}", "type": "priority", "label": priority})

    unique_edges = []
    seen_edges: set[tuple[str, str, str]] = set()
    for edge in edges:
        key = (edge["source"], edge["target"], edge["type"])
        if key not in seen_edges:
            unique_edges.append(edge)
            seen_edges.add(key)

    graph = {
        "schema": "awesome-agentic-tech.knowledge-graph.v1",
        "generatedAt": catalog["generatedAt"],
        "sourceCatalog": "data/projects.json",
        "counts": {"nodes": len(nodes), "edges": len(unique_edges)},
        "nodes": nodes,
        "edges": unique_edges,
    }
    GRAPH_PATH.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    node_fields = ["id", "type", "label", "description", "url", "stars", "language", "license", "priority"]
    with NODES_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=node_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(nodes)

    with EDGES_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "type"])
        writer.writeheader()
        writer.writerows(unique_edges)

    print(json.dumps(graph["counts"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
