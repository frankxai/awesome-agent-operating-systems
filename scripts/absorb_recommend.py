#!/usr/bin/env python3
"""Recommend absorb / pilot / refuse / install from the curated catalog.

No network. No installs. Reads data/projects.json + optional need keyword.

Examples:
  python scripts/absorb_recommend.py --need coding
  python scripts/absorb_recommend.py --need control-plane --limit 12
  python scripts/absorb_recommend.py --class A --priority adopt-core
  python scripts/absorb_recommend.py --repo code-yeongyu/oh-my-openagent
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from taxonomy import INSTALL_HINT, PRIORITY_ACTION, action_of, class_of, policy_issues

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "projects.json"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--need", default="", help="keyword filter against category/why/description/repo")
    ap.add_argument("--class", dest="klass", default="", help="taxonomy class A-F")
    ap.add_argument("--priority", default="", help="catalog priority")
    ap.add_argument("--repo", default="", help="exact repo full_name")
    ap.add_argument("--limit", type=int, default=15)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    projects = catalog["projects"]
    errors = policy_issues(projects)
    if errors:
        ap.error("catalog policy invalid: " + "; ".join(errors))

    out = []
    need = args.need.lower().strip()
    for p in projects:
        if args.repo and p["repo"] != args.repo:
            continue
        klass = class_of(p)
        if args.klass and klass.upper() != args.klass.upper():
            continue
        if args.priority and p["priority"] != args.priority:
            continue
        if need:
            blob = " ".join(
                [
                    p.get("repo", ""),
                    p.get("category", ""),
                    p.get("why", ""),
                    p.get("description", ""),
                    p.get("priority", ""),
                    klass,
                ]
            ).lower()
            if need not in blob:
                continue
        action = action_of(p)
        # Hard refuse double control planes for evaluate-class C when Hermes owns layer
        note = INSTALL_HINT[action]
        if p["repo"] == "paperclipai/paperclip":
            note += " Current estate: SECURITY HOLD; Hermes Kanban is task SSOT."
        if klass == "D" and action in {"USE_NOW", "WIRE_WHEN_NEEDED"}:
            note += " Class D = product library only, never fleet OS."
        if klass == "B" and action == "ABSORB_PATTERN":
            note += " Land in coding-agents references + Queen roles."

        out.append(
            {
                "repo": p["repo"],
                "class": klass,
                "priority": p["priority"],
                "action": action,
                "stars": p["stars"],
                "why": p["why"],
                "note": note,
                "url": p["url"],
            }
        )

    # sort: action severity then stars
    order = list(dict.fromkeys(PRIORITY_ACTION.values()))
    out.sort(key=lambda r: (order.index(r["action"]) if r["action"] in order else 99, -r["stars"]))
    out = out[: max(1, args.limit)]

    if args.json:
        json.dump({"count": len(out), "results": out}, sys.stdout, indent=2)
        print()
        return 0

    if not out:
        print("No matches. Try broader --need or omit filters.")
        return 1

    print(f"# Absorb recommendations ({len(out)})")
    print(f"# catalog generatedAt={catalog.get('generatedAt')}")
    print()
    for r in out:
        print(f"## {r['repo']}")
        print(f"- class: {r['class']} · priority: {r['priority']} · stars: {r['stars']:,}")
        print(f"- action: **{r['action']}**")
        print(f"- why: {r['why']}")
        print(f"- note: {r['note']}")
        print(f"- url: {r['url']}")
        print()
    print("---")
    print("Doctrine: stars admit research; evidence admits routing; one owner per layer.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
