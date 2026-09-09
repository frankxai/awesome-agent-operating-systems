from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).parents[1] / "scripts" / "control_plane_upstream_watch.py"
SPEC = importlib.util.spec_from_file_location("control_plane_upstream_watch", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class NpmReleaseSnapshotTests(unittest.TestCase):
    def test_accepts_npm_multi_field_single_record_array(self) -> None:
        completed = type("Completed", (), {
            "stdout": '[{"version":"2026.722.0","dist.integrity":"sha512-example"}]'
        })()
        with patch.object(MODULE, "run_command", return_value=completed):
            self.assertEqual(
                MODULE.npm_release_snapshot(cwd=Path("."), env={}),
                {"version": "2026.722.0", "registryIntegrity": "sha512-example"},
            )

    def test_accepts_nested_dist_integrity_object(self) -> None:
        completed = type("Completed", (), {
            "stdout": '{"version":"2026.722.0","dist":{"integrity":"sha512-example"}}'
        })()
        with patch.object(MODULE, "run_command", return_value=completed):
            self.assertEqual(
                MODULE.npm_release_snapshot(cwd=Path("."), env={}),
                {"version": "2026.722.0", "registryIntegrity": "sha512-example"},
            )

    def test_accepts_npm_pack_package_keyed_object(self) -> None:
        payload = {
            "paperclipai": {
                "filename": "paperclipai-2026.722.0.tgz",
                "integrity": "sha512-example",
            }
        }
        self.assertEqual(
            MODULE._normalize_npm_pack_payload(payload),
            payload["paperclipai"],
        )


if __name__ == "__main__":
    unittest.main()