"""Tests for the read-only Coffee Cadence evidence collector."""

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


sys.dont_write_bytecode = True
SCRIPT_PATH = Path(__file__).resolve().parents[1] / "tools" / "coffee.py"
SPEC = importlib.util.spec_from_file_location("coffee", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load tools/coffee.py")
COFFEE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COFFEE)


class CoffeeCadenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.repository = Path(self.temporary_directory.name)
        (self.repository / "decisions").mkdir()
        (self.repository / "coding-notes").mkdir()
        (self.repository / "projects" / "vlog-ip").mkdir(parents=True)

        self.write("README.md", "# Test repository\n")
        self.write(
            "ROADMAP.md",
            "# Roadmap\n\n"
            "**Current focus:** [Vlog IP Project]"
            "(projects/vlog-ip/README.md)\n",
        )
        self.write("projects/vlog-ip/README.md", "# Vlog IP\n\n## Next step\n\nTest it.\n")
        self.write("decisions/README.md", "# Decision instructions\n")
        self.write("coding-notes/README.md", "# Coding note instructions\n")
        self.write("decisions/2026-08-01-first.md", "# First decision\n")

        self.git("init", "-q")
        self.git("config", "user.name", "Test User")
        self.git("config", "user.email", "test@example.com")
        self.git("add", ".")
        self.git("commit", "-qm", "Initial test state")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write(self, relative_path: str, content: str) -> None:
        path = self.repository / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def git(self, *arguments: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.repository), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def test_builds_expected_evidence_packet(self) -> None:
        evidence = COFFEE.build_evidence(self.repository)

        self.assertIn("# Coffee Evidence Packet", evidence)
        self.assertIn("projects/vlog-ip/README.md", evidence)
        self.assertIn("# Test repository", evidence)
        self.assertIn("Working tree clean.", evidence)

    def test_excludes_directory_readmes_and_reports_no_coding_note(self) -> None:
        evidence = COFFEE.build_evidence(self.repository)

        self.assertIn("# First decision", evidence)
        self.assertNotIn("# Decision instructions", evidence)
        self.assertNotIn("# Coding note instructions", evidence)
        self.assertIn("No coding note recorded yet.", evidence)

    def test_selects_latest_record_by_filename(self) -> None:
        self.write("decisions/2026-08-02-second.md", "# Second decision\n")
        self.write("coding-notes/2026-08-01-first.md", "# First note\n")
        self.write("coding-notes/2026-08-03-latest.md", "# Latest note\n")

        evidence = COFFEE.build_evidence(self.repository)

        self.assertIn("# Second decision", evidence)
        self.assertNotIn("# First decision", evidence)
        self.assertIn("# Latest note", evidence)
        self.assertNotIn("# First note", evidence)

    def test_reports_dirty_working_tree(self) -> None:
        self.write("README.md", "# Changed repository\n")

        evidence = COFFEE.build_evidence(self.repository)

        self.assertIn(" M README.md", evidence)

    def test_invalid_current_focus_fails_safely(self) -> None:
        self.write(
            "ROADMAP.md",
            "# Roadmap\n\n**Current focus:** [Missing](projects/missing/README.md)\n",
        )

        with self.assertRaises(COFFEE.CadenceError):
            COFFEE.build_evidence(self.repository)

    def test_missing_required_file_fails_safely(self) -> None:
        (self.repository / "README.md").unlink()

        with self.assertRaises(COFFEE.CadenceError):
            COFFEE.build_evidence(self.repository)

    def test_running_from_another_directory_uses_script_repository(self) -> None:
        with tempfile.TemporaryDirectory() as other_directory:
            result = subprocess.run(
                [sys.executable, "-B", str(SCRIPT_PATH)],
                cwd=other_directory,
                check=True,
                capture_output=True,
                text=True,
            )

        self.assertIn("# Coffee Evidence Packet", result.stdout)
        self.assertIn("projects/vlog-ip/README.md", result.stdout)

    def test_collection_does_not_change_working_tree(self) -> None:
        before = self.git("status", "--short")
        COFFEE.build_evidence(self.repository)
        after = self.git("status", "--short")

        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
