# Contributing to Dagster Claude Plugins

Thank you for your interest in contributing to Dagster Claude Plugins! This document provides
guidelines and instructions for contributing to this monorepo.

## Development Setup

This repository contains Claude plugins for Dagster development. Each plugin is located in the
`plugins/` directory:

- `dg` - CLI commands for Dagster development
- `dagster-conventions` - Best practices and conventions
- `dagster-integrations` - Integration index
- `dignified-python` - Python coding standards

### Local Development

1. Clone the repository:

   ```bash
   git clone https://github.com/dagster-io/claude-plugins-dagster.git
   cd claude-plugins-dagster
   ```

2. Make your changes to the relevant plugin(s)

3. Test your changes locally using Claude Code

## Making Changes

### Adding Features or Fixes

1. **Create a branch** for your changes:

   ```bash
   git checkout -b your-feature-name
   ```

2. **Make your changes** to the relevant plugin(s)

3. **Update CHANGELOG.md** - Add your changes under the `[Unreleased]` section:

   ```markdown
   ## [Unreleased]

   ### Added

   - **plugin-name**: Description of new feature

   ### Fixed

   - **plugin-name**: Description of bug fix

   ### Changed

   - **plugin-name**: Description of modification
   ```

   Use the appropriate category:
   - **Added** - New features, new plugin capabilities
   - **Changed** - Changes to existing functionality
   - **Deprecated** - Features that will be removed in future versions
   - **Removed** - Removed features
   - **Fixed** - Bug fixes
   - **Security** - Security improvements or fixes

4. **Commit your changes**:

   ```bash
   git add -A
   git commit -m "Description of your changes"
   ```

5. **Push and create a pull request**:
   ```bash
   git push origin your-feature-name
   ```

## Release Procedure

This repository uses a monorepo versioning system where all plugins share the same version number.
Releases are managed through an automated GitHub Actions workflow.

### Overview

- **Versioning**: All plugins share a single version (e.g., 0.0.1)
- **Semantic Versioning**: We follow [semver](https://semver.org/) (MAJOR.MINOR.PATCH)
- **Manual Releases**: Releases are triggered manually via GitHub Actions
- **Changelog**: All changes are tracked in CHANGELOG.md

### Semantic Versioning Guidelines

Choose the appropriate version bump based on the changes:

- **Patch (0.0.X)** - Bug fixes, documentation updates, small tweaks
  - Example: `0.0.1` → `0.0.2`
  - No new features, no breaking changes

- **Minor (0.X.0)** - New features, backward-compatible changes
  - Example: `0.0.2` → `0.1.0`
  - New plugin capabilities, new commands
  - Existing functionality continues to work

- **Major (X.0.0)** - Breaking changes
  - Example: `0.9.0` → `1.0.0`
  - Changes that break existing functionality
  - Removal of deprecated features

- **Pre-release (X.Y.Z-suffix)** - Beta/alpha versions
  - Example: `1.0.0-beta`, `2.0.0-alpha.1`
  - For testing before stable release

### Updating CHANGELOG.md During Development

As you make changes, add entries to the `[Unreleased]` section of CHANGELOG.md:

```markdown
## [Unreleased]

### Added

- **dg**: New `/dg:analyze` command for pipeline analysis
- **dagster-conventions**: Added guidance for multi-asset definitions

### Fixed

- **dignified-python**: Fixed type annotation examples for Python 3.13

### Changed

- **dagster-integrations**: Updated integration count to 90+
```

**Tips:**

- Prefix each entry with the plugin name in bold: `**plugin-name**:`
- Write clear, concise descriptions
- Use present tense ("Add" not "Added")
- Update CHANGELOG.md in the same PR as your changes

### Step-by-Step Release Process

Only repository maintainers can create releases. Follow these steps:

#### 1. Review Unreleased Changes

Check the `[Unreleased]` section in CHANGELOG.md to see what changes will be included in the
release.

#### 2. Decide on Version Number

Based on the changes, choose the appropriate version number following semantic versioning:

- Are there breaking changes? → Major version bump
- Are there new features? → Minor version bump
- Only bug fixes or small updates? → Patch version bump

#### 3. Trigger the Release Workflow

1. Navigate to the [Actions tab](https://github.com/dagster-io/claude-plugins-dagster/actions)
2. Click on "Release" in the left sidebar
3. Click "Run workflow" button
4. Enter the version number (e.g., `0.0.2`, `1.0.0`, or `1.0.0-beta`)
5. Click "Run workflow"

#### 4. Monitor Workflow Execution

The workflow will:

1. ✓ Validate the version format
2. ✓ Check that the tag doesn't already exist
3. ✓ Update all plugin.json files with the new version
4. ✓ Update CHANGELOG.md (move [Unreleased] to versioned section)
5. ✓ Extract changelog notes for the release
6. ✓ Commit changes to master
7. ✓ Create and push git tag `vX.Y.Z`
8. ✓ Create GitHub release with changelog notes

The workflow takes approximately 1-2 minutes to complete.

#### 5. Verify the Release

After the workflow completes:

1. **Check GitHub Releases**:
   - Visit: https://github.com/dagster-io/claude-plugins-dagster/releases
   - Verify the new release appears with correct version and notes

2. **Verify plugin.json files**:

   ```bash
   git pull origin master
   cat plugins/dg/.claude-plugin/plugin.json
   # Check that "version" field matches the release
   ```

3. **Verify CHANGELOG.md**:

   ```bash
   cat CHANGELOG.md
   # Check that:
   # - [Unreleased] section is empty
   # - New version section exists with today's date
   # - Comparison links are updated
   ```

4. **Verify Git tag**:
   ```bash
   git tag -l "v*"
   # Should show your new version
   ```

### Verification Checklist

After a release, verify:

- [ ] GitHub release created at https://github.com/dagster-io/claude-plugins-dagster/releases
- [ ] Release notes match CHANGELOG.md section
- [ ] All 4 plugin.json files updated to new version
- [ ] CHANGELOG.md has new version section with today's date
- [ ] [Unreleased] section is reset with empty categories
- [ ] Git tag `vX.Y.Z` exists and points to correct commit
- [ ] Comparison links in CHANGELOG.md work correctly

### Troubleshooting

#### "Tag already exists" error

**Problem**: The version tag already exists in the repository.

**Solution**: Choose a different version number or delete the existing tag if it was created by
mistake:

```bash
git tag -d v0.0.2
git push origin :refs/tags/v0.0.2
```

#### "Invalid version format" error

**Problem**: The version doesn't follow semantic versioning.

**Solution**: Use format `X.Y.Z` (e.g., `0.0.2`) or `X.Y.Z-prerelease` (e.g., `1.0.0-beta`).

#### Workflow fails during commit/push

**Problem**: Git operations failed (rare).

**Solution**:

1. Check the workflow logs for specific error
2. Ensure no one else is releasing simultaneously
3. Re-run the workflow

#### Release notes are empty or incorrect

**Problem**: The CHANGELOG.md section for that version is missing or malformed.

**Solution**:

1. Check CHANGELOG.md format
2. Ensure version header is: `## [X.Y.Z] - YYYY-MM-DD`
3. If needed, edit the GitHub release manually to fix notes

### Local Testing (Optional)

Before triggering the workflow, you can test the version bump locally:

```bash
# Create a test branch
git checkout -b test-release

# Run the bump script
python scripts/release/bump.py 0.0.2

# Review changes
git diff

# Verify CHANGELOG.md
cat CHANGELOG.md

# Verify plugin versions
cat plugins/dg/.claude-plugin/plugin.json

# Clean up (don't commit)
git checkout master
git branch -D test-release
```

## Code Quality

This repository uses automated linting and formatting tools to maintain code quality and
consistency. All pull requests must pass linting checks in CI.

### Quick Start with Make

The repository includes a Makefile for common development tasks:

```bash
make help      # Show available commands
make install   # Install pre-commit hooks
make lint      # Run all linting checks
make format    # Auto-fix formatting issues
make clean     # Clean up cache and temporary files
```

### Setup Pre-commit Hooks

Install and enable pre-commit hooks to automatically check your changes before committing:

```bash
# Using Make (recommended)
make install
```

Or manually:

```bash
# Install pre-commit (requires Python 3.11+)
pip install pre-commit

# Install git hooks
pre-commit install
```

Now pre-commit will run automatically on `git commit`. The hooks will:

- Check and format markdown files
- Lint and format Python code
- Validate JSON and YAML syntax
- Remove trailing whitespace and fix line endings

### Running Linters Manually

To run all linters on all files:

```bash
make lint
```

Or directly with pre-commit:

```bash
pre-commit run --all-files
```

To run linters on specific files:

```bash
pre-commit run --files path/to/file.md path/to/script.py
```

### Auto-fixing Issues

Most linting issues can be automatically fixed:

**Auto-fix all files:**

```bash
make format
```

**Or manually:**

Markdown formatting:

```bash
npx prettier --write "**/*.md"
```

Python formatting:

```bash
ruff format scripts/
ruff check --fix scripts/
```

### Linting Tools Used

- **markdownlint-cli2**: Semantic/structural markdown rules
- **Prettier**: Automated markdown formatting
- **Ruff**: Python linting and formatting (replaces Black, isort, Flake8)
- **pre-commit-hooks**: JSON/YAML validation, trailing whitespace, etc.

### CI Requirements

All pull requests must pass the linting workflow in GitHub Actions. The workflow runs:

```bash
pre-commit run --all-files
```

If the linting check fails:

1. Run `pre-commit run --all-files` locally to see the errors
2. Fix the issues (many can be auto-fixed)
3. Commit the fixes and push again

You can view the linting workflow status in the "Checks" tab of your pull request.

## Code Standards

### Python Code

For Python code in plugins, follow the **dignified-python** standards:

- Use type annotations with modern syntax (`list[str]`, `str | None`)
- Follow LBYL (Look Before You Leap) exception handling
- Use pathlib for file operations
- Use ABC-based interfaces for abstractions

All Python code is automatically checked with Ruff (linting + formatting).

### Documentation

- Keep documentation clear and concise
- Include examples where helpful
- Update CHANGELOG.md with all changes
- All markdown is automatically formatted with Prettier and checked with markdownlint

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove)
- Reference issue numbers if applicable

## Questions?

If you have questions or need help:

- Open an issue on GitHub
- Check existing issues and discussions

Thank you for contributing to Dagster Claude Plugins!
