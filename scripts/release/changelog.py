#!/usr/bin/env python3
"""
Extract a specific version section from CHANGELOG.md.

Used by GitHub Actions to generate release notes.
"""

import argparse
import re
import sys
from pathlib import Path


def extract_version_section(changelog_path: Path, version: str) -> str:
    """
    Extract the changelog section for a specific version.

    Returns the content between the version header and the next version header,
    with empty category headers removed.
    """
    with changelog_path.open() as f:
        content = f.read()

    # Pattern to match version section
    # Matches from "## [version]" to either next "## [" or end of file
    pattern = rf"## \[{re.escape(version)}\][^\n]*\n(.*?)(?=\n## \[|\Z)"
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        return ""

    section = match.group(1).strip()

    # Remove empty category headers (headers with no content before next header or end)
    # Matches "### Category\n\n" (followed by either another ### or end of section)
    section = re.sub(r"### [A-Za-z]+\n+(?=###|\Z)", "", section)

    # Clean up multiple consecutive newlines
    section = re.sub(r"\n{3,}", "\n\n", section)

    return section.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract changelog section for a specific version")
    parser.add_argument("version", help="Version to extract (e.g., 0.0.1, 1.0.0)")
    parser.add_argument(
        "--changelog",
        default="CHANGELOG.md",
        help="Path to CHANGELOG.md (default: CHANGELOG.md in repo root)",
    )

    args = parser.parse_args()

    # Get repository root (script is in scripts/release/ subdirectory)
    repo_root = Path(__file__).parent.parent.parent
    changelog_path = repo_root / args.changelog

    if not changelog_path.exists():
        print(f"Error: CHANGELOG.md not found at {changelog_path}", file=sys.stderr)
        sys.exit(1)

    section = extract_version_section(changelog_path, args.version)

    if not section:
        print(f"Error: Version {args.version} not found in CHANGELOG.md", file=sys.stderr)
        sys.exit(1)

    print(section)


if __name__ == "__main__":
    main()
