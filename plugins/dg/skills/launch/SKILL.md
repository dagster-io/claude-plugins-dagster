---
name: dg:launch
description:
  Launch (materialize) Dagster assets with comprehensive guidance on partitions, configuration,
  environment setup, and troubleshooting. Use when user wants to run, launch, materialize, or
  execute assets.
---

# Launch Dagster Assets Skill

This skill helps users launch (materialize) Dagster assets through natural language requests,
providing comprehensive guidance on asset selection, partitions, configuration, and environment
setup.

## When to Use This Skill

Auto-invoke when users say:

- "launch my assets"
- "run my assets"
- "materialize my asset"
- "execute my assets"
- "test my assets" (in the context of running them)
- "run the pipeline"
- "materialize [asset_name]"
- "launch [asset_name]"
- "run [asset_name]"
- "backfill my assets"
- "run my job"
- "execute job [job_name]"
- "how do I launch assets"
- "how do I run assets"
- "how do I materialize assets with partitions"
- "how do I pass config to assets"
- "help me launch assets with environment variables"

## When to Use This Skill vs. Others

| If User Says...                  | Use This Skill/Command | Why                              |
| -------------------------------- | ---------------------- | -------------------------------- |
| "launch my assets"               | `/dg:launch`           | Asset execution guidance needed  |
| "run my pipeline"                | `/dg:launch`           | Pipeline execution (assets)      |
| "materialize X"                  | `/dg:launch`           | Direct materialization request   |
| "backfill partitions"            | `/dg:launch`           | Partition range guidance needed  |
| "how do I launch with config"    | `/dg:launch`           | Config patterns needed           |
| "prototype a pipeline"           | `/dg:prototype`        | Need to build new assets first   |
| "best practices for assets"      | `/dagster-conventions` | Learning patterns, not executing |
| "test my assets" (writing tests) | `/dagster-conventions` | Testing patterns, not execution  |
| "test my assets" (run them)      | `/dg:launch`           | Execution/validation             |

## How It Works

When this skill is invoked:

1. **Identify the request type**:
   - Simple launch (single asset, multiple assets, all assets)
   - Job execution
   - Partition-based launch
   - Configuration-based launch
   - Environment setup question
   - Troubleshooting

2. **Extract specifics** from user request:
   - Asset names or selection patterns (tags, groups, kinds)
   - Partition keys or ranges
   - Configuration requirements
   - Environment variable needs

3. **Invoke the underlying command**: `/dg:launch` with extracted context

4. **Provide guidance** based on request complexity:
   - Simple launches: Direct command
   - Partitions: Show partition syntax and examples
   - Configuration: Show config structure and patterns
   - Environment: Show .env setup and uv patterns
   - Troubleshooting: Show debug steps

## Example Flows

### Simple Launch Request

```
User: "Launch my customers asset"
→ Provide command:
  dg launch --assets customers

→ Or with uv:
  uv run dg launch --assets customers
```

### Multiple Assets

```
User: "Run my sales pipeline assets"
→ Ask clarifying question if needed: "Do you want to run:
  1. All assets in a specific group? (e.g., group:sales_analytics)
  2. Assets with a specific tag? (e.g., tag:domain=sales)
  3. Specific asset names?"

→ Based on response, provide appropriate command:
  dg launch --assets "group:sales_analytics"
  # or
  dg launch --assets customers,orders,revenue
```

### Partition Launch

```
User: "Materialize my daily asset for yesterday"
→ Provide command with partition:
  dg launch --assets my_daily_asset --partition 2024-01-15

→ Show general partition pattern:
  dg launch --assets <asset_name> --partition <partition_key>
```

### Partition Backfill

```
User: "Backfill my assets for January"
→ Provide command with partition range:
  dg launch --assets my_asset --partition-range "2024-01-01...2024-01-31"

→ Explain:
  - This launches all partitions in the range
  - Date format depends on partition definition
  - Can combine with asset selection (tags, groups)
```

### Launch with Configuration

```
User: "Launch my asset with custom config"
→ Provide config pattern:
  dg launch --assets my_asset --config-json '{
    "ops": {
      "my_asset": {
        "config": {
          "batch_size": 1000,
          "enable_validation": true
        }
      }
    }
  }'

→ Suggest config file for complex configs:
  dg launch --assets my_asset --config-json "$(cat config.json)"
```

### Environment Variables

```
User: "How do I load environment variables for my assets?"
→ Explain:
  .env files are automatically loaded by Dagster.

  Use uv run for Python environment activation:
  uv run dg launch --assets my_asset
```

### Job Execution

```
User: "Run my daily job"
→ Provide job command:
  dg launch --job my_daily_job

→ If partitioned job:
  dg launch --job my_job --partition 2024-01-15
```

### Troubleshooting Request

```
User: "My asset launch is failing"
→ Provide troubleshooting steps:

  1. Verify definitions load:
     dg check defs

  2. List available assets:
     dg list defs

  3. Check environment variables:
     echo $DATABASE_URL  # Example
```

### Selection Syntax Questions

```
User: "How do I launch all dbt assets?"
→ Provide kind-based selection:
  dg launch --assets "kind:dbt"

User: "How do I launch high priority assets?"
→ Provide tag-based selection:
  dg launch --assets "tag:priority=high"

User: "Launch all assets in my sales group"
→ Provide group-based selection:
  dg launch --assets "group:sales_analytics"
```

### Vague Launch Request

```
User: "Help me launch my assets"
→ Ask clarifying questions:
  "I can help you launch assets. What would you like to do?

  Common options:
  - Launch specific asset(s) by name
  - Launch assets by tag, group, or kind
  - Launch all assets
  - Launch a specific partition
  - Backfill a partition range
  - Launch a predefined job

  Please specify which assets you want to launch."

→ Based on response, provide appropriate guidance
```

## Implementation Notes

- This skill is a thin wrapper that delegates to the `/dg:launch` command
- The command file at `commands/launch.md` contains comprehensive documentation
- For complex scenarios, reference the full command documentation
- Always provide working examples, not just explanations

## Guidance Priorities

When responding to launch requests, prioritize:

1. **Direct commands** - Provide copy-pasteable commands first
2. **Environment setup** - Ensure user knows how to load .env files
3. **Selection patterns** - Show tag/group/kind syntax for flexibility
4. **Partition guidance** - Explain single vs range clearly
5. **Configuration structure** - Show correct JSON structure for config
6. **Troubleshooting** - Point to validation and debugging steps
7. **Migration info** - If they mention old commands, show modern equivalent

## Common Patterns to Emphasize

### Asset Selection Hierarchy

Guide users toward maintainable selection patterns:

```bash
# Most maintainable (scales well)
dg launch --assets "tag:schedule=daily"
dg launch --assets "group:analytics"
dg launch --assets "kind:dbt"

# Specific (good for ad-hoc)
dg launch --assets customers,orders

# Wildcard (good for namespaces)
dg launch --assets "staging_*"

# All (use carefully)
dg launch --assets "*"
```

### Environment Variable Patterns

.env files are automatically loaded:

```bash
# Direct execution (Python env from project)
dg launch --assets my_asset

# With uv (activates Python environment)
uv run dg launch --assets my_asset
```

### Partition Patterns

Show both single and range clearly:

```bash
# Single partition
dg launch --assets my_asset --partition 2024-01-15

# Range (backfill)
dg launch --assets my_asset --partition-range "2024-01-01...2024-01-31"

# Combined with selection
dg launch --assets "tag:schedule=daily" --partition 2024-01-15
```

## Related Commands and Skills

### Before Launching

Users may need to:

- `/dg:prototype` - Build assets if they don't exist yet
- `/dg:create-project` - Initialize project structure
- `/dagster-conventions` - Learn asset patterns and best practices

### During Launch

- This skill (`/dg:launch`) - Execute assets

### After Launch

- `/dg:troubleshoot` - Debug failures
- `/dg:logs` - Retrieve detailed logs
- `/dagster-conventions` - Improve asset patterns based on issues

## What Gets Provided

When you invoke this skill, you'll receive:

1. **Direct commands** - Copy-pasteable dg launch commands
2. **Asset selection patterns** - Tag, group, kind, wildcard syntax
3. **Partition guidance** - Single partition and range examples
4. **Configuration structure** - JSON config format and examples
5. **Environment setup** - Note that .env files auto-load
6. **Troubleshooting steps** - Validation and debugging commands
7. **Cloud considerations** - Dagster Cloud and remote launcher behavior

## Full Documentation Reference

For comprehensive coverage of all launch features, the underlying command documentation covers:

- All CLI flags and options
- Complete asset selection syntax (tags, groups, kinds, owners, patterns)
- Partition types (daily, static, multi-dimensional)
- Configuration patterns (inline JSON, config files)
- Environment variable behavior (.env auto-loading)
- Job execution patterns
- Advanced patterns (IDE integration, CI/CD)
- Cloud/remote execution behavior
- Complete troubleshooting guide

Access the full documentation at: `commands/launch.md`
