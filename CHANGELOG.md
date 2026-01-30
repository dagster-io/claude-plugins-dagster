# Changelog

All notable changes to Dagster Skills will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.0.7] - 2026-01-30

### Added

- **all-skills**: Added frontmatter metadata to all SKILL.md files
  - Added `name`, `description`, and `references` fields to each skill
  - Enables better skill discovery and AI navigation
- **all-skills**: Added decision trees to all skills for workflow navigation
  - `/dg`: Workflow decision tree (create, scaffold, launch, list, logs, troubleshoot)
  - `/dagster-best-practices`: Architecture decision tree (assets, automation, resources, testing,
    ETL, structure)
  - `/dagster-integrations`: Integration discovery tree (by use case)
  - `/dignified-python`: Python pattern tree (type hints, exceptions, paths, CLI)
- **all-skills**: Added README.md navigation guides to all references/ directories
  - Created comprehensive table of contents for each skill's reference documentation
  - Added quick reference sections and navigation tips
  - Included cross-skill workflow guidance
- **root**: Added root-level `.claude-plugin/plugin.json` (v0.0.7)
  - Unified plugin configuration for all skills

### Changed

- 🔥 **BREAKING**: Consolidated 9 skills into 4 simple skills with flat structure (55% reduction)
  - Merged 6 separate `/dg:*` skills into single `/dg` skill with natural language invocation
  - Renamed `/dagster-conventions` → `/dagster-best-practices` for clearer purpose
  - Renamed `/integrations-index` → `/dagster-integrations` for better discoverability
  - Kept `/dignified-python` as general Python standards skill
- 🔥 **BREAKING**: Flattened directory structure from `plugins/*/skills/*/` to `skills/*/`
  - Removed nested plugin architecture in favor of simple flat structure
  - All skills now directly in `skills/` directory at repository root
  - Easier navigation and simpler mental model
- **dg**: Changed from 6 namespaced skills to 1 comprehensive skill
  - Replaced `/dg:create-project`, `/dg:create-workspace`, `/dg:scaffold`, `/dg:launch`,
    `/dg:list`, `/dg:prototype` with single `/dg` skill
  - Users now invoke with natural language: `/dg create a project` instead of `/dg:create-project`
  - All CLI documentation moved from `commands/` to `skills/dg/references/`
  - Added comprehensive decision tree for choosing right workflow
- **dg**: Enhanced SKILL.md with cross-references to other skills
  - Links to `/dagster-best-practices` for architectural guidance
  - Links to `/dagster-integrations` for integration discovery
  - Links to `/dignified-python` for Python code quality
- **dagster-best-practices**: Renamed and enhanced skill (formerly dagster-conventions)
  - Clearer name emphasizes architectural guidance over rules
  - Updated description to highlight decision-making and pattern selection
  - Added comprehensive decision tree for architecture choices
  - Added cross-references to other skills
- **dagster-integrations**: Renamed and enhanced skill (formerly integrations-index)
  - More discoverable name aligns with user expectations
  - Added integration discovery decision tree by use case
  - Added cross-references to other skills for implementation
- **dignified-python**: Reorganized reference structure
  - Created `references/versions/` subdirectory for Python version-specific docs
  - Created `references/advanced/` subdirectory for advanced topics
  - Clarified in description that it's general Python, not Dagster-specific
  - Updated navigation to new directory structure
- **docs**: Completely rewrote README.md for v0.0.7 structure
  - Added "What's New" section highlighting simplification
  - Added skills overview table with clear purpose statements
  - Added detailed skill documentation with natural language examples
  - Added usage examples and workflow patterns
  - Added comprehensive migration guide from v0.0.6
  - Added philosophy section ("At the end of the day it's all markdown")
  - Updated directory structure diagram
  - Added version history
- **docs**: Updated all skill descriptions to emphasize self-selection
  - Clear "When to Use This Skill" sections
  - Explicit cross-references to alternative skills
  - Natural language trigger phrases for auto-invocation
- **docs**: Rebranded from "Dagster Claude Plugins" to "Dagster Skills" (carried over from
  Unreleased)
  - Updated README.md title and subtitle to reflect multi-tool compatibility
  - Changed "Plugins" section to "Skills" throughout documentation
  - Updated CONTRIBUTING.md title and all references from "plugins" to "skills"
  - Added compatibility statement for Agent Skills-compatible tools
- **docs**: Added comprehensive multi-tool installation documentation (carried over from Unreleased)
  - Added "npx skills" installation method
  - Added manual installation instructions for OpenCode, OpenAI Codex, Pi Agent
  - Updated paths to reflect new flat structure

### Deprecated

- 🔥 **BREAKING**: Deprecated individual `/dg:*` namespaced skills in favor of single `/dg` skill
  - `/dg:create-project` → Use `/dg` with natural language
  - `/dg:create-workspace` → Use `/dg` with natural language
  - `/dg:scaffold` → Use `/dg` with natural language
  - `/dg:launch` → Use `/dg` with natural language
  - `/dg:list` → Use `/dg` with natural language
  - `/dg:prototype` → Use `/dg` with natural language
- 🔥 **BREAKING**: Deprecated old skill names
  - `/dagster-conventions` → Use `/dagster-best-practices`
  - `/integrations-index` → Use `/dagster-integrations`

### Removed

- **all-skills**: Removed `plugins/` directory and nested plugin architecture
  - Deleted `plugins/dg/.claude-plugin/plugin.json`
  - Deleted `plugins/dagster-conventions/.claude-plugin/plugin.json`
  - Deleted `plugins/dagster-integrations/.claude-plugin/plugin.json`
  - Deleted `plugins/dignified-python/.claude-plugin/plugin.json`
  - All content migrated to flat `skills/` structure
- **dg**: Removed `commands/` directory (merged into `skills/dg/references/`)

### Fixed

### Security

## [0.0.6] - 2026-01-29

### Added

- **dg**: `/dg:list` command and skill for discovering and inspecting Dagster definitions
  - Complete documentation for `dg list` CLI command group
  - `dg list defs` - List all registered definitions (assets, jobs, schedules, sensors, resources)
  - `dg list components` - Discover available component types for scaffolding
  - `dg list envs` - Inspect environment variables and Dagster Plus secrets
  - `dg list projects` - List projects in workspace
  - `dg list registry-modules` - List dg plugins
  - `dg list component-tree` - Show component hierarchy
  - Asset selection syntax (tags, groups, kinds, patterns)
  - Column customization for definitions
  - JSON output for automation and scripting
  - Natural language skill wrapper for conversational discovery
- **dg**: `/dg:scaffold` command and skill for scaffolding Dagster components and code
  - Complete documentation for `dg scaffold` CLI command group
  - `dg scaffold defs <component_type>` - Dynamically scaffold component instances
  - `dg scaffold defs inline-component` - Create custom inline components
  - `dg scaffold component` - Create reusable component types
  - Support for core Dagster components (assets, schedules, sensors)
  - Support for integrations (dbt, Fivetran, dlt, Sling)
  - Format options (YAML vs Python)
  - Parameter strategies (JSON params vs individual flags)
  - Interactive disambiguation for partial matches
  - Natural language skill wrapper for conversational scaffolding

### Changed

- **all-plugins**: Renamed repository from `dagster-claude-plugins` / `claude-plugins-dagster` to
  `skills`
  - Updated marketplace name from `dagster-claude-plugins` to `skills`
  - Updated package name from `claude-plugins-dagster` to `skills`
  - Updated all GitHub URLs from `dagster-io/claude-plugins-dagster` to `dagster-io/skills`
  - Updated installation commands: `/plugin marketplace add dagster-io/skills` and
    `/plugin install dg@skills`
- **all-plugins**: Reformatted all markdown documentation files to meet linting standards
  - Fixed trailing whitespace and end-of-file formatting
  - Applied consistent markdown formatting with Prettier
  - Updated Python release scripts to use `Path.open()` per dignified-python standards

### Deprecated

### Removed

### Fixed

### Security

## [0.0.5] - 2026-01-28

### Added

### Changed

### Deprecated

### Removed

### Fixed

- **dg**: Fixed `dg launch` documentation to use comma-separated asset syntax
  - Updated SKILL.md and launch.md to show correct syntax: `--assets asset1,asset2,asset3`
  - Previous incorrect examples showed space-separated: `--assets asset1 asset2 asset3`
  - Verified against actual CLI implementation in dagster repository
  - Selection patterns (tags, groups, kinds) preserved correctly

### Security

## [0.0.4] - 2026-01-28

### Added

- **dagster-integrations**: Added comprehensive audit summary document (AUDIT_SUMMARY.md)
  - Documents all 82+ integration verifications
  - Lists critical fixes applied and remaining work

### Changed

- **dagster-integrations**: Updated storage.md integration examples
  - Improved Postgres section with ConfigurableResource pattern and instance storage clarification
  - Updated Delta Lake to use correct `DeltaTableResource` API
  - Enhanced Redshift example with `RedshiftClientResource`
  - Improved DataHub example with correct `DatahubRESTEmitterResource`
  - Updated LakeFS to show custom resource pattern with lakefs-client SDK

### Deprecated

### Removed

- **dagster-integrations**: Removed fabricated integrations from storage.md
  - Removed MongoDB section (dagster-mongo package doesn't exist)
  - Removed Atlan section (Dagster+ cloud CLI feature, not a Python library)
  - Removed Secoda section (no library integration exists)

### Fixed

- **dagster-integrations**: Fixed critical PostgresResource hallucinations across multiple files
  - storage.md: Replaced fabricated dagster-postgres resource API with custom ConfigurableResource
    pattern
  - Fixed 5 support level misclassifications:
    - dagster-looker: Community-supported → Dagster-supported
    - dagster-sigma: Community-supported → Dagster-supported
    - dagster-polars: Dagster-supported → Community-supported
    - dagster-wandb: Dagster-supported → Community-supported
    - dagster-papertrail: Community-supported → Dagster-supported
- **dagster-conventions**: Fixed PostgresResource hallucinations in resources.md
  - Updated factory pattern example with custom PostgresResource definition
- **dagster-conventions**: Fixed PostgresResource hallucinations in testing.md
  - Updated test examples with custom ConfigurableResource implementations
- **dagster-integrations**: Fixed other.md Polars integration
  - Removed non-existent `PolarsDataFrame` import
  - Corrected support level to Community-supported

### Security

## [0.0.3] - 2026-01-28

### Added

### Changed

- **dg**: Simplified `/dg:launch` skill documentation
  - Clarified that `.env` files are automatically loaded by Dagster
  - Updated partition range syntax to use `...` instead of `:` (e.g., `2024-01-01...2024-01-31`)
  - Streamlined environment variable setup instructions
  - Removed references to deprecated troubleshooting commands
- **dagster-integrations**: Streamlined integrations-index skill documentation
  - Removed "Top 10 Most Popular Integrations" section
  - Updated last verified date to 2026-01-27
- **dagster-conventions**: Updated skill documentation
- Added `.claude/skills/` to `.gitignore`

### Deprecated

### Removed

### Fixed

### Security

## [0.0.2] - 2026-01-26

### Added

- **dg**: `/dg:launch` command and skill for comprehensive asset launching
  - Complete documentation for `dg launch` CLI command
  - Asset selection patterns (tags, groups, kinds, wildcards)
  - Partition support (single partition, partition ranges/backfills)
  - Configuration patterns (inline JSON, config files)
  - Environment variable setup (uv auto-loading, shell sourcing, per-environment)
  - Job execution patterns
  - Advanced patterns (IDE integration, CI/CD)
  - Cloud/remote execution guidance
  - Troubleshooting guide for common launch failures
  - Migration guide from legacy `dagster asset materialize` to `dg launch`
- **dagster-conventions**: Expanded CLI Quick Reference with partition and config examples
- **dagster-conventions**: Added "Launching Assets" section to assets reference
- **README**: Added `/dg:launch` command to dg plugin documentation with new "Execute" section

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.0.1] - 2026-01-26

### Added

- Initial release of Dagster Claude Plugins marketplace
- **dg**: CLI commands for Dagster development
  - `/dg:create-project` - Scaffold new Dagster projects
  - `/dg:create-workspace` - Initialize multi-project workspaces
  - `/dg:prototype` - Build production-ready implementations with testing
  - `/dg:logs` - Retrieve and display run logs
  - `/dg:troubleshoot` - Debug failing runs with analysis
- **dagster-conventions**: Expert guidance for Dagster development
  - Asset patterns, resources, schedules, sensors
  - Partitions, testing, and ETL best practices
- **dagster-integrations**: Comprehensive integration index
  - 82+ integrations across AI, ETL, storage, compute, BI
  - Organized by official tags.yml taxonomy
- **dignified-python**: Production-tested Python standards
  - Version-aware type annotations (Python 3.10-3.13)
  - LBYL exception handling patterns
  - Modern type syntax (list[str], str | None)
  - Pathlib operations and ABC-based interfaces

[Unreleased]: https://github.com/dagster-io/skills/compare/v0.0.7...HEAD
[0.0.7]: https://github.com/dagster-io/skills/releases/tag/v0.0.7
[0.0.6]: https://github.com/dagster-io/skills/releases/tag/v0.0.6
[0.0.5]: https://github.com/dagster-io/skills/releases/tag/v0.0.5
[0.0.4]: https://github.com/dagster-io/skills/releases/tag/v0.0.4
[0.0.3]: https://github.com/dagster-io/skills/releases/tag/v0.0.3
[0.0.2]: https://github.com/dagster-io/skills/releases/tag/v0.0.2
[0.0.1]: https://github.com/dagster-io/skills/releases/tag/v0.0.1
