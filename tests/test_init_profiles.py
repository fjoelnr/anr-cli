from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from anr.init import run_init


class InitProfilesTest(unittest.TestCase):
    def test_run_init_with_platformio_profile_writes_profile_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_path = Path(tmp_dir)

            exit_code = run_init(project_path, profile="platformio-iot")

            self.assertEqual(exit_code, 0)
            self.assertTrue((project_path / "AGENTS.md").exists())
            self.assertTrue((project_path / ".agents" / "context-index.md").exists())
            self.assertTrue((project_path / "anr.yaml").exists())
            self.assertTrue((project_path / "anr.profile.yaml").exists())
            self.assertTrue((project_path / "docs" / "hardware.md").exists())
            self.assertTrue((project_path / "docs" / "verification.md").exists())
            self.assertTrue((project_path / "docs" / "operations.md").exists())
            self.assertTrue((project_path / "docs" / "topic-contracts.md").exists())

            agents_text = (project_path / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("<!-- ANR PROFILE START -->", agents_text)
            self.assertIn("platformio-iot", agents_text)

            profile_manifest = (project_path / "anr.profile.yaml").read_text(encoding="utf-8")
            self.assertIn("profile_id: platformio-iot", profile_manifest)
            self.assertIn("category: firmware", profile_manifest)

    def test_run_init_keeps_existing_profile_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_path = Path(tmp_dir)
            existing_doc = project_path / "docs" / "verification.md"
            existing_doc.parent.mkdir(parents=True, exist_ok=True)
            existing_doc.write_text("# Existing Verification\n", encoding="utf-8")

            exit_code = run_init(project_path, profile="platformio-iot")

            self.assertEqual(exit_code, 0)
            self.assertEqual(existing_doc.read_text(encoding="utf-8"), "# Existing Verification\n")

    def test_run_init_rejects_unknown_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = run_init(Path(tmp_dir), profile="unknown-profile")

            self.assertEqual(exit_code, 1)
            self.assertIn("Unknown stack profile", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
