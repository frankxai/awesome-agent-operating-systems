#!/usr/bin/env python3
"""Regenerate sites/atlas/atlas-data.js from data/projects.json."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from taxonomy import PRIORITY_ACTION, action_of, class_of, policy_issues

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "projects.json"
OUT = ROOT / "sites" / "atlas" / "atlas-data.js"

CLASSES = [
    {
        "id": "A",
        "name": "Coding CLI harness",
        "job": "Edit repos, run tools, ship through Git",
        "examples": [
            "openai/codex",
            "anomalyco/opencode",
            "google-gemini/gemini-cli",
            "Aider-AI/aider",
            "OpenHands/OpenHands",
            "can1357/oh-my-pi",
            "earendil-works/pi",
        ],
        "not": "Not a company board. Not a Python multi-agent library.",
        "estate": "Primary workers: Codex · Claude Code · Grok Build · OpenCode · AGY/Gemini",
    },
    {
        "id": "B",
        "name": "Meta-harness / skill overlay",
        "job": "Swarm memory, hooks, plugins, verified completion on top of Class A",
        "examples": [
            "code-yeongyu/oh-my-openagent",
            "ruvnet/ruflo",
            "HKUDS/OpenHarness",
        ],
        "not": "Does not replace Hermes Queen or Git evidence.",
        "estate": "Absorb patterns; pilot only for a measured gap",
    },
    {
        "id": "C",
        "name": "Org / company control plane",
        "job": "Goals, org charts, budgets, approvals, multi-agent company state",
        "examples": [
            "paperclipai/paperclip",
            "lobehub/lobehub",
            "multica-ai/multica",
            "simstudioai/sim",
        ],
        "not": "Not the coding worker. Not task SSOT until promoted.",
        "estate": "Paperclip = security HOLD; Hermes Kanban = live task control",
    },
    {
        "id": "D",
        "name": "Agent frameworks (libraries)",
        "job": "Build product agent graphs inside applications",
        "examples": [
            "langchain-ai/langgraph",
            "microsoft/autogen",
            "crewAIInc/crewAI",
            "mastra-ai/mastra",
            "pydantic/pydantic-ai",
        ],
        "not": "Not daily coding CLIs. Not fleet OS.",
        "estate": "Embed in products when needed; never as second control plane",
    },
    {
        "id": "E",
        "name": "General agent runtime / OS",
        "job": "Chat, tools, memory, cron, gateway, skills — full operator surface",
        "examples": [
            "NousResearch/hermes-agent",
            "openclaw/openclaw",
            "bytedance/deer-flow",
            "aaif-goose/goose",
        ],
        "not": "One primary human gateway.",
        "estate": "Hermes Agent + Starlight Queen = Tier 0 core",
    },
    {
        "id": "F",
        "name": "Durable workflow engines",
        "job": "Timers, retries, long jobs, business integrations",
        "examples": [
            "temporalio/temporal",
            "triggerdotdev/trigger.dev",
            "n8n-io/n8n",
            "activepieces/activepieces",
        ],
        "not": "Not chat loops as workflow engines.",
        "estate": "Hermes cron simple; Temporal/n8n when product durability needs it",
    },
    {
        "id": "S",
        "name": "Supporting substrate (not a harness)",
        "job": "Protocols, trust, memory, retrieval, model infrastructure, and integration primitives",
        "examples": [
            "a2aproject/A2A",
            "agentskills/agentskills",
            "modelcontextprotocol/servers",
            "promptfoo/promptfoo",
            "Graphite/graphite",
        ],
        "not": "Not an execution harness or a second control plane.",
        "estate": "Adopt standards deliberately; wire security and data components only behind explicit gates",
    },
]


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    errors = policy_issues(catalog["projects"])
    if errors:
        raise ValueError("catalog taxonomy policy invalid: " + "; ".join(errors))
    slim = []
    for p in catalog["projects"]:
        slim.append(
            {
                "repo": p["repo"],
                "class": class_of(p),
                "action": action_of(p),
                "url": p["url"],
                "name": p["repo"].split("/")[-1],
                "owner": p["repo"].split("/")[0],
                "description": p.get("description") or "",
                "category": p["category"],
                "priority": p["priority"],
                "why": p["why"],
                "stars": p["stars"],
                "language": p.get("language") or "—",
                "license": p["license"],
                "licenseReview": p["licenseReviewRequired"],
            }
        )

    atlas = {
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "title": "Starlight Agentic Atlas",
        "subtitle": "Operator surface for humans and agents — classify, route, absorb, prove",
        "version": 3,
        "counts": catalog["counts"],
        "classes": CLASSES,
        "stack": {
            "human": "Hermes Agent + Starlight Queen",
            "taskControl": "Hermes Kanban (live) · Paperclip after security gate",
            "workers": [
                "Hermes",
                "Codex CLI",
                "Claude Code",
                "OpenCode",
                "Gemini CLI / AGY",
                "Grok Build",
            ],
            "durability": "Hermes cron · Temporal/Trigger.dev · n8n/Activepieces",
            "interop": ["MCP", "Agent Skills", "AGENTS.md", "A2A", "AG-UI"],
            "state": "Git/SSOT · Hermes memory · Graphiti · Qdrant when justified",
            "trust": "tests/evals · promptfoo · SkillSpector · sandbox · secrets",
            "rule": "One accountable owner per layer. Stars admit research. Evidence admits routing.",
        },
        "humanJobs": [
            {
                "title": "Command",
                "detail": "One trusted front door across desktop and Telegram",
            },
            {
                "title": "Decide",
                "detail": "Human gates for money, production, public, credentials, brand",
            },
            {
                "title": "See truth",
                "detail": "Board, receipts, costs, and Git evidence — not agent self-reports",
            },
            {
                "title": "Feel calm",
                "detail": "Premium clarity: hierarchy, restraint, fast first read",
            },
        ],
        "agentJobs": [
            {
                "title": "Route",
                "detail": "Class A–F taxonomy + needs map before spawn",
            },
            {
                "title": "Execute",
                "detail": "Bounded workspace, path ban, maker≠checker",
            },
            {
                "title": "Prove",
                "detail": "Artifacts, tests, PR/CI, HTTP — or HOLD",
            },
            {
                "title": "Absorb",
                "detail": "Pattern into skills/docs; never silent second SSOT",
            },
        ],
        "projects": slim,
        "priorityOrder": [
            "adopt-core",
            "adopt-adjacent",
            "pilot",
            "evaluate",
            "benchmark",
            "watch",
            "reference",
            "strategic-exception",
        ],
        "categoryLabels": {
            "control-plane": "Control plane",
            "coding-control-plane": "Coding control / meta-harness",
            "coding-agent": "Coding agent",
            "agent-runtime": "Agent runtime",
            "agent-framework": "Agent framework",
            "rust-runtime": "Rust runtime",
            "interaction-ui": "Interaction UI",
            "durable-execution": "Durable execution",
            "workflow-automation": "Workflow automation",
            "memory": "Memory",
            "protocol": "Protocol",
            "eval-security": "Eval & security",
            "observability": "Observability",
            "creative-media": "Creative media",
            "browser-computer-use": "Browser / computer use",
            "model-runtime": "Model runtime",
            "model-gateway": "Model gateway",
            "voice-realtime": "Voice realtime",
            "domain-platform": "Domain platform",
            "agent-builder": "Agent builder",
            "agent-training": "Agent training",
            "data-integration": "Data integration",
            "document-ingestion": "Document ingestion",
            "identity-secrets": "Identity & secrets",
            "knowledge-graph": "Knowledge graph",
            "rag-platform": "RAG platform",
            "sandbox-security": "Sandbox & security",
            "tools-integration": "Tools & integration",
            "vector-database": "Vector database",
        },
        "absorbActions": PRIORITY_ACTION,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        "window.ATLAS_DATA = "
        + json.dumps(atlas, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT.relative_to(ROOT)} projects={len(slim)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
