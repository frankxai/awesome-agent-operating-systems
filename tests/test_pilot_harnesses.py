#!/usr/bin/env python3
"""Regression tests for the bounded Paperclip and Hermes pilot harnesses."""

from __future__ import annotations

import importlib.util
import copy
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest import mock
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMOKE_SCRIPT = ROOT / "scripts" / "paperclip_pilot_smoke.py"
KANBAN_SCRIPT = ROOT / "scripts" / "hermes_kanban_benchmark.py"
WATCHER_SCRIPT = ROOT / "scripts" / "control_plane_upstream_watch.py"
IDENTITY_SCRIPT = ROOT / "scripts" / "validate_task_identity.py"
SCORECARD_SCRIPT = ROOT / "scripts" / "build_control_plane_scorecard.py"
IDENTITY_RECORD = ROOT / "data" / "control-plane-task-identities" / "paperclip-promotion-gate.json"


def load_kanban_module():
    spec = importlib.util.spec_from_file_location("hermes_kanban_benchmark", KANBAN_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load Hermes benchmark module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_watcher_module():
    spec = importlib.util.spec_from_file_location("control_plane_upstream_watch", WATCHER_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load control-plane watcher module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GoodHandler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        return

    def do_GET(self):
        if self.path == "/api/health":
            body = json.dumps({"status": "ok"}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
        elif self.path == "/":
            body = b"<html><title>Paperclip</title></html>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
        else:
            self.send_error(404)
            return
        self.end_headers()
        self.wfile.write(body)


class RedirectHandler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        return

    def do_GET(self):
        self.send_response(302)
        self.send_header("Location", "http://example.com/")
        self.end_headers()


class PilotHarnessTests(unittest.TestCase):
    def run_smoke(self, handler, expected_code: int):
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as temporary_directory:
                receipt = Path(temporary_directory) / "receipt.json"
                result = subprocess.run(
                    [
                        sys.executable,
                        str(SMOKE_SCRIPT),
                        "--base-url",
                        f"http://127.0.0.1:{server.server_port}",
                        "--receipt",
                        str(receipt),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                payload = json.loads(receipt.read_text(encoding="utf-8"))
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
        self.assertEqual(expected_code, result.returncode)
        return payload

    def test_smoke_accepts_expected_loopback_service(self):
        receipt = self.run_smoke(GoodHandler, 0)
        self.assertEqual("passed", receipt["status"])
        self.assertTrue(receipt["passed"])
        self.assertTrue(receipt["loopbackOnly"])
        self.assertTrue(all(check["passed"] for check in receipt["checks"]))

    def test_smoke_blocks_redirect(self):
        receipt = self.run_smoke(RedirectHandler, 1)
        self.assertEqual("failed", receipt["status"])
        self.assertFalse(receipt["passed"])
        self.assertTrue(all(not check["redirect_followed"] for check in receipt["checks"]))
        self.assertTrue(all(check["status"] == 302 for check in receipt["checks"]))

    def test_smoke_rejects_non_loopback_before_request(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            receipt = Path(temporary_directory) / "receipt.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SMOKE_SCRIPT),
                    "--base-url",
                    "http://example.com",
                    "--receipt",
                    str(receipt),
                ],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            payload = json.loads(receipt.read_text(encoding="utf-8"))
        self.assertEqual(1, result.returncode)
        self.assertEqual("error", payload["status"])
        self.assertFalse(payload["passed"])
        self.assertNotIn("checks", payload)

    def test_kanban_rejects_workspace_outside_pilot_cache(self):
        receipt = ROOT / ".pilot-cache" / "test-kanban-path-rejection.json"
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(KANBAN_SCRIPT),
                    "--hermes-home",
                    str(ROOT / ".pilot-cache" / "hermes-home"),
                    "--board",
                    "paperclip-benchmark",
                    "--workspace",
                    str(ROOT.parent),
                    "--receipt",
                    str(receipt),
                ],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            payload = json.loads(receipt.read_text(encoding="utf-8"))
        finally:
            receipt.unlink(missing_ok=True)
        self.assertEqual(1, result.returncode)
        self.assertEqual("path_validation", payload["error"]["stage"])
        self.assertFalse(payload["passed"])

    def test_kanban_receipt_sanitizes_workspace_and_lock(self):
        module = load_kanban_module()
        payload = {
            "task": {"workspace_path": str(ROOT / ".pilot-cache" / "workspace")},
            "events": [{"kind": "claimed", "payload": {"lock": "host:123"}}],
        }
        sanitized = module.sanitize_task_payload(payload, ROOT)
        self.assertEqual(".pilot-cache/workspace", sanitized["task"]["workspace_path"])
        self.assertEqual(
            "[host-pid-redacted]", sanitized["events"][0]["payload"]["lock"]
        )
        self.assertEqual("host:123", payload["events"][0]["payload"]["lock"])

    def test_watcher_excludes_provider_credentials_from_subprocess_environment(self):
        module = load_watcher_module()
        with mock.patch.dict(
            os.environ,
            {
                "PATH": os.environ.get("PATH", ""),
                "GITHUB_TOKEN": "must-not-pass-through",
                "OPENAI_API_KEY": "must-not-pass-through",
                "NPM_TOKEN": "must-not-pass-through",
            },
            clear=True,
        ):
            environment = module.command_environment()

        self.assertIn("PATH", environment)
        self.assertNotIn("GITHUB_TOKEN", environment)
        self.assertNotIn("OPENAI_API_KEY", environment)
        self.assertNotIn("NPM_TOKEN", environment)

    def test_watcher_package_gate_holds_high_findings_and_known_undici(self):
        module = load_watcher_module()
        gate, reasons = module.package_gate(
            {"critical": 0, "high": 1, "moderate": 5},
            ["5.29.0"],
        )
        self.assertEqual("HOLD", gate)
        self.assertEqual(2, len(reasons))

    def test_watcher_package_gate_allows_zero_high_or_critical(self):
        module = load_watcher_module()
        gate, reasons = module.package_gate(
            {"critical": 0, "high": 0, "moderate": 2},
            ["6.21.1"],
        )
        self.assertEqual("PROMOTION_CANDIDATE", gate)
        self.assertEqual([], reasons)

    def test_watcher_rejects_state_outside_pilot_cache(self):
        module = load_watcher_module()
        with self.assertRaises(ValueError):
            module.require_cache_path(ROOT / "reports" / "state.json", ROOT, "state path")

    def test_identity_validator_enforces_published_schema(self):
        module = load_module("validate_task_identity", IDENTITY_SCRIPT)
        record = json.loads(IDENTITY_RECORD.read_text(encoding="utf-8"))
        record["systems"]["hermes"]["unexpected"] = True
        errors = module.validate_record(record)
        self.assertTrue(any("unexpected" in error for error in errors), errors)

    def test_identity_validator_rejects_malformed_issue_without_throwing(self):
        module = load_module("validate_task_identity", IDENTITY_SCRIPT)
        record = json.loads(IDENTITY_RECORD.read_text(encoding="utf-8"))
        record["systems"]["github"]["evidenceIssues"] = ["malformed"]
        errors = module.validate_record(record)
        self.assertTrue(errors)

    def test_scheduler_reconciliation_rejects_wrong_workdir(self):
        module = load_module("validate_task_identity", IDENTITY_SCRIPT)
        record = json.loads(IDENTITY_RECORD.read_text(encoding="utf-8"))
        job = {
            "id": record["scheduler"]["jobId"],
            "no_agent": True,
            "script": record["scheduler"]["script"],
            "workdir": str(ROOT.parent),
            "enabled": True,
        }
        with self.assertRaises(RuntimeError):
            module.validate_scheduler_job(record, job, ROOT)

    def test_scorecard_inputs_must_bind_to_identity(self):
        module = load_module("build_control_plane_scorecard", SCORECARD_SCRIPT)
        identity = json.loads(IDENTITY_RECORD.read_text(encoding="utf-8"))
        tasks = identity["systems"]["hermes"]["workflowTaskIds"]
        proof = {
            "canonicalTaskId": identity["canonicalTaskId"],
            "board": identity["systems"]["hermes"]["board"],
            "beforeCount": len(tasks),
            "afterCount": len(tasks),
            "replayTaskId": tasks[0],
            "idempotent": True,
        }
        self.assertTrue(module.scorecard_inputs_bound(identity, proof["board"], tasks, proof))
        wrong = copy.deepcopy(proof)
        wrong["canonicalTaskId"] = "ctid:v1:wrong-scope:wrong-task"
        self.assertFalse(module.scorecard_inputs_bound(identity, proof["board"], tasks, wrong))

    def test_watcher_fingerprint_changes_when_same_release_audit_changes(self):
        module = load_watcher_module()
        snapshot = {"paperclipRelease": {"version": "1.0.0"}}
        clean = {
            "version": "1.0.0",
            "registryIntegrity": "sha512-a",
            "computedIntegrity": "sha512-a",
            "integrityMatched": True,
            "productionVulnerabilities": {"critical": 0, "high": 0},
            "undiciVersions": ["7.0.0"],
            "promotionGate": "PROMOTION_CANDIDATE",
            "holdReasons": [],
        }
        vulnerable = copy.deepcopy(clean)
        vulnerable["productionVulnerabilities"]["high"] = 1
        vulnerable["promotionGate"] = "HOLD"
        vulnerable["holdReasons"] = ["1 high production vulnerability finding(s)"]
        self.assertNotEqual(
            module.state_fingerprint(module.fingerprint_payload(snapshot, clean)),
            module.state_fingerprint(module.fingerprint_payload(snapshot, vulnerable)),
        )


if __name__ == "__main__":
    unittest.main()
