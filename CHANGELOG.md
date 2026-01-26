# Changelog

All notable changes to the Dagster Claude Plugins will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/dagster-io/claude-plugins-dagster/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/dagster-io/claude-plugins-dagster/releases/tag/v0.0.1
