"""Shared Atlas taxonomy and recommendation policy.

A–F describes harness layers. S is deliberately reserved for supporting
substrates (trust, memory, protocols, data, model infrastructure) that should
not be misrepresented as an execution harness.
"""
from __future__ import annotations

from typing import Any

HARNESS_CLASSES = {
    "A": "Coding CLI harness",
    "B": "Meta-harness / skill overlay",
    "C": "Org / company control plane",
    "D": "Agent frameworks (libraries)",
    "E": "General agent runtime / OS",
    "F": "Durable workflow engines",
    "S": "Supporting substrate (not a harness)",
}

CATEGORY_TO_CLASS = {
    "coding-agent": "A",
    "coding-control-plane": "B",
    "control-plane": "C",
    "agent-framework": "D",
    "agent-builder": "D",
    "structured-output": "D",
    "agent-training": "D",
    "agent-runtime": "E",
    "rust-runtime": "E",
    "interaction-ui": "E",
    "durable-execution": "F",
    "workflow-automation": "F",
    "browser-computer-use": "S",
    "creative-media": "S",
    "data-integration": "S",
    "document-ingestion": "S",
    "domain-platform": "S",
    "eval-security": "S",
    "identity-secrets": "S",
    "knowledge-graph": "S",
    "memory": "S",
    "model-gateway": "S",
    "model-runtime": "S",
    "observability": "S",
    "protocol": "S",
    "rag-platform": "S",
    "sandbox-security": "S",
    "tools-integration": "S",
    "vector-database": "S",
    "voice-realtime": "S",
}

# A category is only a starting point. These projects have a more precise
# architectural role than their historical catalog category communicates.
REPO_CLASS = {
    "code-yeongyu/oh-my-openagent": "B",
    "ruvnet/ruflo": "B",
    "HKUDS/OpenHarness": "B",
    "openai/symphony": "B",
    "stablyai/orca": "B",
    "gastownhall/gastown": "B",
    "superset-sh/superset": "B",
    "humanlayer/humanlayer": "B",
    "paperclipai/paperclip": "C",
    "langchain-ai/langgraph": "D",
    "microsoft/autogen": "D",
    "crewAIInc/crewAI": "D",
    "NousResearch/hermes-agent": "E",
    "openai/codex": "A",
    "anomalyco/opencode": "A",
    "can1357/oh-my-pi": "A",
    "earendil-works/pi": "A",
}

PRIORITY_ACTION = {
    "adopt-core": "USE_NOW",
    "adopt-standard": "ADOPT_STANDARD",
    "adopt-adjacent": "WIRE_WHEN_NEEDED",
    "pilot": "GATED_PILOT",
    "evaluate": "ABSORB_PATTERN",
    "benchmark": "RESEARCH_ONLY",
    "watch": "WATCH",
    "reference": "REFERENCE",
    "strategic-exception": "EXCEPTION_REVIEW",
}

INSTALL_HINT = {
    "USE_NOW": "Tier 0 worker or runtime. Use it before adding another control surface.",
    "ADOPT_STANDARD": "Portable baseline. Adopt in new work when it fits; do not force a migration.",
    "WIRE_WHEN_NEEDED": "Keep available; enable for a concrete workflow, not curiosity.",
    "GATED_PILOT": "Only after security, disk, owner, rollback and evidence gates. Not a default install.",
    "ABSORB_PATTERN": "Do not install by default. Port useful hooks, prompts or protocols into existing rails first.",
    "RESEARCH_ONLY": "Architecture benchmark. No production control-plane role.",
    "WATCH": "Track releases; no estate action yet.",
    "REFERENCE": "Historical or educational reference only.",
    "EXCEPTION_REVIEW": "Below star threshold for a recorded reason; requires explicit review.",
}


def class_of(project: dict[str, Any]) -> str:
    """Return a total taxonomy class for every valid catalog project."""
    repo = str(project.get("repo", ""))
    category = str(project.get("category", ""))
    return REPO_CLASS.get(repo) or CATEGORY_TO_CLASS.get(category, "S")


def action_of(project: dict[str, Any]) -> str:
    """Return the explicit action for a catalog project, never an implicit fallback."""
    priority = str(project.get("priority", ""))
    try:
        return PRIORITY_ACTION[priority]
    except KeyError as exc:
        raise ValueError(f"unknown catalog priority: {priority!r}") from exc


def policy_issues(projects: list[dict[str, Any]]) -> list[str]:
    """Validate taxonomy/action coverage for a live catalog."""
    errors: list[str] = []
    categories = {str(project.get("category", "")) for project in projects}
    priorities = {str(project.get("priority", "")) for project in projects}
    missing_categories = sorted(categories - set(CATEGORY_TO_CLASS))
    missing_priorities = sorted(priorities - set(PRIORITY_ACTION))
    if missing_categories:
        errors.append(f"unclassified catalog categories: {', '.join(missing_categories)}")
    if missing_priorities:
        errors.append(f"unmapped catalog priorities: {', '.join(missing_priorities)}")
    for project in projects:
        assigned = class_of(project)
        if assigned not in HARNESS_CLASSES:
            errors.append(f"invalid class {assigned!r} for {project.get('repo')}")
    return errors
