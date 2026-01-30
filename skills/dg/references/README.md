# Dagster CLI (dg) Reference Documentation

This directory contains comprehensive reference documentation for all `dg` CLI workflows.

## Table of Contents

### Project Setup
- **[create-project.md](./create-project.md)** - Create new Dagster projects
- **[create-workspace.md](./create-workspace.md)** - Create multi-project workspaces

### Component Generation
- **[scaffold.md](./scaffold.md)** - Scaffold components, assets, schedules, sensors, and integrations
  - Core components (assets, schedules, sensors)
  - Integration scaffolding (dbt, Fivetran, dlt, Sling)
  - Inline components
  - Component types
  - Format options (YAML vs Python)
  - Parameter strategies
  - Dynamic command discovery

### Execution
- **[launch.md](./launch.md)** - Launch (materialize) assets and execute jobs
  - Asset selection syntax (by name, tag, group, kind, owner)
  - Partitions and partition ranges (backfills)
  - Configuration and environment variables
  - Job execution
  - Cloud/remote execution

### Discovery
- **[list.md](./list.md)** - List definitions, components, and environment variables
  - `dg list defs` - All registered definitions
  - `dg list components` - Available component types
  - `dg list envs` - Environment variables
  - `dg list projects` - Workspace projects
  - `dg list component-tree` - Component hierarchy

### Monitoring
- **[logs.md](./logs.md)** - View run logs and execution output
  - Recent runs
  - Specific run logs
  - Follow live logs
  - Log level filtering
  - Step-specific logs
  - Compute logs

### Development
- **[prototype.md](./prototype.md)** - Generate production-ready asset implementations
  - Guided implementation workflow
  - Best practices integration
  - Full code generation (not just scaffolds)

### Debugging
- **[troubleshoot.md](./troubleshoot.md)** - Debug failed runs and issues
  - Failure analysis
  - Common error patterns
  - Solution recommendations
  - Component validation

## Quick Reference

### Common Commands

```bash
# Create new project
dg create project my_project

# Scaffold an asset
dg scaffold defs dagster.asset my_asset --format python

# Launch an asset
dg launch --assets my_asset

# List all definitions
dg list defs

# View logs
dg logs --follow

# Debug failures
dg troubleshoot
```

### Discovery-First Workflow

```bash
# 1. Discover available component types
dg list components

# 2. Filter by package
dg list components --package dagster_dbt

# 3. Scaffold with discovered type
dg scaffold defs dagster_dbt.DbtProjectComponent my_dbt

# 4. Verify it was created
dg list defs

# 5. Test execution
dg launch --assets my_dbt
```

### Complete Setup Workflow

```bash
# 1. Create project
dg create project analytics
cd analytics

# 2. Scaffold integrations
dg scaffold defs dagster_dbt.DbtProjectComponent dbt_project
dg scaffold defs fivetran.FivetranComponent salesforce --json-params '{...}'

# 3. Scaffold downstream assets
dg scaffold defs dagster.asset analytics/revenue --format python

# 4. Scaffold automation
dg scaffold defs dagster.schedule daily_refresh --format python

# 5. Configure environment
echo "FIVETRAN_API_KEY=..." >> .env
echo "FIVETRAN_API_SECRET=..." >> .env

# 6. Verify structure
dg list defs
dg list envs

# 7. Test execution
dg launch --assets revenue

# 8. View logs
dg logs --follow

# 9. Debug if needed
dg troubleshoot
```

## Navigation Tips

- Start with **create-project.md** or **create-workspace.md** for new setups
- Use **scaffold.md** for component creation (most comprehensive doc)
- Reference **launch.md** for execution patterns
- Consult **list.md** for discovery workflows
- Check **troubleshoot.md** when things go wrong
- Use **prototype.md** for full implementation guidance

## Related Skills

- **`/dagster-best-practices`** - Architectural guidance, asset patterns, automation strategies
- **`/dagster-integrations`** - Integration library catalog, implementation patterns
- **`/dignified-python`** - Python code quality standards

## Documentation Structure

Each reference document follows a consistent structure:

1. **Overview** - High-level explanation and key benefits
2. **Quick Start** - Common patterns and examples
3. **Detailed Documentation** - Comprehensive coverage of all options
4. **Use Cases** - Real-world scenarios and workflows
5. **Advanced Patterns** - Complex use cases and automation
6. **Troubleshooting** - Common errors and solutions
7. **Related Commands** - Cross-references to other workflows

## Getting Help

- Each command has `--help` flag: `dg <command> --help`
- Use `dg list components --help` to see component discovery options
- Reference full documentation in this directory for comprehensive guidance
- Cross-reference `/dagster-best-practices` for architectural decisions
- Cross-reference `/dagster-integrations` for integration-specific guidance
