#!/usr/bin/env python3
"""Regression tests for Atlas classification, actions and generated data."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
CATALOG = ROOT / "data" / "projects.json"
ATLAS_DATA = ROOT / "sites" / "atlas" / "atlas-data.js"


def load_module(name: str, filename: str):
    path = SCRIPTS / filename
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(SCRIPTS))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(SCRIPTS))
    return module


class AtlasPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.taxonomy = load_module("atlas_taxonomy", "taxonomy.py")
        cls.recommend = load_module("atlas_recommend", "absorb_recommend.py")
        cls.catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        cls.projects = cls.catalog["projects"]

    def test_every_catalog_category_and_priority_has_explicit_policy(self):
        self.assertEqual([], self.taxonomy.policy_issues(self.projects))
        self.assertTrue(all(self.taxonomy.class_of(project) != "·" for project in self.projects))
        self.assertTrue(all(self.taxonomy.action_of(project) for project in self.projects))

    def test_protocol_baselines_are_adopt_standard_not_watch(self):
        protocols = [p for p in self.projects if p["priority"] == "adopt-standard"]
        self.assertGreaterEqual(len(protocols), 1)
        self.assertTrue(all(self.taxonomy.action_of(p) == "ADOPT_STANDARD" for p in protocols))
        self.assertTrue(all(self.taxonomy.class_of(p) == "S" for p in protocols))

    def test_known_meta_harness_overrides_category(self):
        by_repo = {project["repo"]: project for project in self.projects}
        self.assertEqual("B", self.taxonomy.class_of(by_repo["ruvnet/ruflo"]))
        self.assertEqual("B", self.taxonomy.class_of(by_repo["code-yeongyu/oh-my-openagent"]))
        self.assertEqual("C", self.taxonomy.class_of(by_repo["paperclipai/paperclip"]))

    def test_recommend_cli_emits_adopt_standard_for_protocol_query(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "absorb_recommend.py"), "--need", "protocol", "--json", "--limit", "20"],
            capture_output=True,
            text=True,
            check=False,
            timeout=20,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        self.assertGreater(payload["count"], 0)
        self.assertTrue(any(row["action"] == "ADOPT_STANDARD" for row in payload["results"]))

    def test_generated_atlas_matches_catalog_and_has_no_unknown_class(self):
        prefix = "window.ATLAS_DATA = "
        text = ATLAS_DATA.read_text(encoding="utf-8")
        self.assertTrue(text.startswith(prefix))
        payload = json.loads(text.removeprefix(prefix).removesuffix(";\n"))
        self.assertEqual(len(self.projects), len(payload["projects"]))
        self.assertEqual(3, payload["version"])
        classes = {item["id"] for item in payload["classes"]}
        self.assertIn("S", classes)
        self.assertEqual(self.taxonomy.PRIORITY_ACTION, payload["absorbActions"])


if __name__ == "__main__":
    unittest.main()
