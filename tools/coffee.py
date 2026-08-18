#!/usr/bin/env python3
"""Collect read-only repository evidence for the Coffee Cadence workflow."""

from pathlib import Path
import re
import subprocess
import sys
from typing import Optional


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CURRENT_FOCUS_PATTERN = re.compile(
    r"^\*\*Current focus:\*\*\s+\[[^\]]+\]\(([^)]+)\)\s*$",
    re.MULTILINE,
)


class CadenceError(Exception):
    """Raised when required repository evidence cannot be collected safely."""


def read_required(path: Path) -> str:
    """Read a required UTF-8 file or raise a clear cadence error."""
    if not path.is_file():
        raise CadenceError(f"Required file is missing: {path}")
    return path.read_text(encoding="utf-8").strip()


def latest_record(directory: Path) -> Optional[Path]:
    """Return the newest Markdown record by filename, excluding README.md."""
    if not directory.is_dir():
        return None
    records = sorted(
        path
        for path in directory.glob("*.md")
        if path.name.lower() != "readme.md"
    )
    return records[-1] if records else None


def run_git(repository_root: Path, *arguments: str) -> str:
    """Run a read-only Git command without invoking a shell."""
    result = subprocess.run(
        ["git", "-C", str(repository_root), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or "Git command failed."
        raise CadenceError(message)
    return result.stdout.rstrip()


def verify_repository(repository_root: Path) -> None:
    """Confirm that the script belongs to the Git repository it is reading."""
    discovered_root = Path(
        run_git(repository_root, "rev-parse", "--show-toplevel")
    ).resolve()
    if discovered_root != repository_root.resolve():
        raise CadenceError(
            f"Expected repository root {repository_root}, found {discovered_root}."
        )


def current_project(repository_root: Path, roadmap: str) -> Path:
    """Resolve the repository-relative project path declared in ROADMAP.md."""
    match = CURRENT_FOCUS_PATTERN.search(roadmap)
    if match is None:
        raise CadenceError("ROADMAP.md does not declare a valid Current focus.")

    relative_path = Path(match.group(1))
    if relative_path.is_absolute():
        raise CadenceError("Current focus must use a repository-relative path.")

    resolved_path = (repository_root / relative_path).resolve()
    try:
        resolved_path.relative_to(repository_root.resolve())
    except ValueError as error:
        raise CadenceError("Current focus points outside the repository.") from error

    if not resolved_path.is_file():
        raise CadenceError(f"Current focus file is missing: {relative_path}")
    return resolved_path


def source_section(
    title: str, repository_root: Path, path: Path, content: str
) -> str:
    """Render one source and its repository-relative path as Markdown."""
    relative_path = path.relative_to(repository_root)
    return f"## {title}\n\nSource: `{relative_path}`\n\n{content}"


def optional_record_section(
    title: str,
    repository_root: Path,
    directory_name: str,
    missing_message: str,
) -> str:
    """Render the latest optional record or an explicit missing-data message."""
    record = latest_record(repository_root / directory_name)
    if record is None:
        return f"## {title}\n\n{missing_message}"
    return source_section(title, repository_root, record, read_required(record))


def build_evidence(repository_root: Path) -> str:
    """Build the complete Markdown evidence packet without changing the repository."""
    repository_root = repository_root.resolve()
    verify_repository(repository_root)

    readme_path = repository_root / "README.md"
    roadmap_path = repository_root / "ROADMAP.md"
    readme = read_required(readme_path)
    roadmap = read_required(roadmap_path)
    project_path = current_project(repository_root, roadmap)
    project = read_required(project_path)

    latest_commit = run_git(repository_root, "log", "-1", "--oneline")
    working_tree = run_git(repository_root, "status", "--short") or "Working tree clean."

    sections = [
        "# Coffee Evidence Packet",
        (
            "## Current focus\n\n"
            f"Source: `ROADMAP.md`\n\n"
            f"Project file: `{project_path.relative_to(repository_root)}`"
        ),
        (
            "## Git state\n\n"
            f"Latest commit: `{latest_commit}`\n\n"
            "Working tree:\n\n"
            f"```text\n{working_tree}\n```"
        ),
        source_section("Repository overview", repository_root, readme_path, readme),
        source_section("Roadmap", repository_root, roadmap_path, roadmap),
        source_section("Current project", repository_root, project_path, project),
        optional_record_section(
            "Latest decision",
            repository_root,
            "decisions",
            "No decision record recorded yet.",
        ),
        optional_record_section(
            "Latest coding note",
            repository_root,
            "coding-notes",
            "No coding note recorded yet.",
        ),
    ]
    return "\n\n".join(sections) + "\n"


def main() -> int:
    """Print the evidence packet, returning a nonzero status for required failures."""
    try:
        print(build_evidence(REPOSITORY_ROOT), end="")
    except CadenceError as error:
        print(f"Coffee Cadence error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
