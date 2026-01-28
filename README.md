<div align="center">
  <img width="auto" height="38px" alt="dagster-hearts-claude" src="https://github.com/user-attachments/assets/b162dddf-6a7e-459e-be06-29d34d637650" />
</div>

# Dagster Claude Plugins

A collection of Claude Code plugins for building workflows and data pipelines using Dagster.

## Installation

Add this marketplace to Claude Code:

```
/plugin marketplace add dagster-io/dagster-claude-plugins
```

Install a plugin:

```
/plugin install dg@claude-plugins-dagster
```

To update your marketplace plugins:

```
/plugin marketplace update
```

## Plugins

### dg

Commands for building executing, and debugging Dagster projects.

Discover:
  - `/dg:list` - List and inspect Dagster definitions, components, environment variables, and project structure
    - `dg list defs` - Show all registered definitions (assets, jobs, schedules, sensors, resources)
    - `dg list components` - Discover available component types for scaffolding
    - `dg list envs` - Inspect environment variables and Dagster Plus secrets
    - `dg list projects` - List projects in workspace
    - Supports asset selection (tags, groups, kinds, patterns) and JSON output

Build:
  - `/dg:create-project <name>` - Create a new Dagster project with recommended structure
  - `/dg:create-workspace <name>` - Initialize a workspace for managing multiple projects
  - `/dg:scaffold` - Scaffold Dagster components, assets, schedules, sensors, and integrations
    - Dynamically discover and create component instances (assets, schedules, sensors)
    - Integrate with dbt, Fivetran, dlt, Sling, and other tools
    - Support for both YAML and Python formats
    - Interactive component type disambiguation
  - `/dg:prototype <requirements>` - Build production-ready Dagster implementations with best practices, testing, and validation

Execute:
  - `/dg:launch` - Launch (materialize) Dagster assets with comprehensive guidance on partitions, configuration, environment setup, and troubleshooting

Debug:
  - `/dg:logs <run-id> [level] [limit]` - Retrieve and display logs for a run
  - `/dg:troubleshoot <run-id>` - Debug failing runs by analyzing error logs

### dagster-conventions

Comprehensive Dagster development conventions and best practices.

This skill provides expert guidance for Dagster data orchestration including assets, resources, schedules, sensors, partitions, testing, and ETL patterns.

### dagster-integrations

Comprehensive index of 82+ Dagster integrations including cloud platforms, data warehouses, ETL tools, AI/ML, data quality, monitoring, and more.

This skill helps you discover and integrate with the right tools for your data pipelines.

### dignified-python

Production-tested Python coding standards with version-aware type annotations, LBYL exception handling, and modern typing patterns.

This skill provides comprehensive guidance for writing dignified Python code including:
- Automatic Python version detection (3.10-3.13)
- LBYL exception handling patterns
- Modern type syntax (list[str], str | None)
- Pathlib operations and ABC-based interfaces
- CLI patterns and subprocess handling
- API design and code organization best practices

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

<div align="center">
  <img alt="dagster logo" src="https://github.com/user-attachments/assets/6fbf8876-09b7-4f4a-8778-8c0bb00c5237" width="auto" height="16px">
</div>
