#!/usr/bin/env python3
"""
Version bumping script for Dagster Skills monorepo.

Updates version in all plugin.json files and CHANGELOG.md.
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


def validate_version(version: str) -> bool:
    """
    Validate semantic versioning format (X.Y.Z or X.Y.Z-prerelease).

    Examples:
        - Valid: 0.0.1, 1.0.0, 2.1.3, 1.0.0-beta, 1.0.0-alpha.1
        - Invalid: 1.0, v1.0.0, 1.0.0.1
    """
    pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$"
    return bool(re.match(pattern, version))


def update_plugin_version(plugin_path: Path, version: str) -> None:
    """
    Update version field in a plugin.json file.

    Preserves JSON formatting (2-space indent, trailing newline).
    """
    with plugin_path.open() as f:
        data = json.load(f)

    data["version"] = version

    with plugin_path.open("w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def update_changelog(repo_root: Path, version: str) -> None:
    """
    Update CHANGELOG.md with new version.

    - Converts [Unreleased] section to [version] with today's date
    - Adds new empty [Unreleased] section at top
    - Updates comparison links at bottom
    """
    changelog_path = repo_root / "CHANGELOG.md"

    with changelog_path.open() as f:
        content = f.read()

    today = date.today().isoformat()

    # Check if there's content in the Unreleased section
    unreleased_pattern = r"## \[Unreleased\]\n\n(.*?)(?=\n## \[|\Z)"
    unreleased_match = re.search(unreleased_pattern, content, re.DOTALL)

    if not unreleased_match:
        print(
            "Error: Could not find [Unreleased] section in CHANGELOG.md",
            file=sys.stderr,
        )
        sys.exit(1)

    # Replace [Unreleased] header with new version
    content = re.sub(
        r"## \[Unreleased\]",
        f"## [Unreleased]\n\n### Added\n\n### Changed\n\n### Deprecated\n\n### Removed\n\n### Fixed\n\n### Security\n\n## [{version}] - {today}",
        content,
        count=1,
    )

    # Update comparison links at bottom
    # First, update the [Unreleased] comparison link
    content = re.sub(
        r"\[Unreleased\]: https://github\.com/dagster-io/skills/compare/v[\d.]+(?:-[a-zA-Z0-9.]+)?\.\.\.HEAD",
        f"[Unreleased]: https://github.com/dagster-io/skills/compare/v{version}...HEAD",
        content,
    )

    # Add new version comparison link before the last existing one
    # Find the last version link
    last_version_pattern = r"(\[\d+\.\d+\.\d+(?:-[a-zA-Z0-9.]+)?\]: https://github\.com/dagster-io/skills/releases/tag/v[\d.]+(?:-[a-zA-Z0-9.]+)?)\s*$"

    if re.search(last_version_pattern, content):
        content = re.sub(
            last_version_pattern,
            f"[{version}]: https://github.com/dagster-io/skills/releases/tag/v{version}\n\\1",
            content,
        )
    else:
        # If no version links exist yet, add one at the end
        content += f"\n[{version}]: https://github.com/dagster-io/skills/releases/tag/v{version}\n"

    with changelog_path.open("w") as f:
        f.write(content)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bump version across all plugin.json files and CHANGELOG.md"
    )
    parser.add_argument(
        "version", help="Semantic version to bump to (e.g., 0.0.2, 1.0.0, 1.0.0-beta)"
    )

    args = parser.parse_args()
    version = args.version

    # Validate version format
    if not validate_version(version):
        print(f"Error: Invalid version format: {version}", file=sys.stderr)
        print(
            "Version must follow semantic versioning (X.Y.Z or X.Y.Z-prerelease)",
            file=sys.stderr,
        )
        sys.exit(1)

    # Get repository root (script is in scripts/release/ subdirectory)
    repo_root = Path(__file__).parent.parent.parent

    # Find root-level plugin.json file
    plugin_file = repo_root / ".claude-plugin" / "plugin.json"

    if not plugin_file.exists():
        print(
            "Error: plugin.json not found at .claude-plugin/plugin.json",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Bumping version to {version}...")
    print()

    # Update plugin.json file
    update_plugin_version(plugin_file, version)
    print("✓ Updated .claude-plugin/plugin.json")

    # Update CHANGELOG.md
    update_changelog(repo_root, version)
    print("✓ Updated CHANGELOG.md")

    print()
    print("Version bump complete!")
    print()
    print("Next steps:")
    print("  1. Review the changes:")
    print("     git diff")
    print("  2. Commit the changes:")
    print(f'     git add -A && git commit -m "Bump version to {version}"')
    print("  3. Create and push a tag:")
    print(f'     git tag -a v{version} -m "Release {version}"')
    print("     git push origin master --tags")
    print("  4. Create a GitHub release manually or via workflow")


if __name__ == "__main__":
    main()
