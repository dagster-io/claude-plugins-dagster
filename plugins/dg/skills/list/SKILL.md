---
name: dg:list
description: List and discover Dagster definitions, components, environment variables, and project structure. Use when user wants to see, list, show, inspect, or discover assets, jobs, schedules, sensors, resources, components, or environment variables.
---

# List Dagster Definitions and Components Skill

This skill helps users discover and inspect Dagster definitions, components, and project structure through natural language requests, providing comprehensive guidance on listing assets, finding components, and understanding their environment.

## When to Use This Skill

Auto-invoke when users say:
- "show me my assets"
- "list my assets"
- "what assets do I have"
- "show all my schedules"
- "list my dbt assets"
- "what jobs are defined"
- "show me assets in the sales group"
- "list high priority assets"
- "what components can I scaffold"
- "show available component types"
- "list environment variables"
- "what env vars do I need"
- "show my projects"
- "list all definitions"
- "what integrations are available"
- "show me the component tree"
- "what plugins are installed"

## When to Use This Skill vs. Others

| If User Says... | Use This Skill/Command | Why |
|----------------|------------------------|-----|
| "show me my assets" | `/dg:list` | Discovery/inspection needed |
| "list dbt assets" | `/dg:list` | Filter and display definitions |
| "what components can I scaffold" | `/dg:list` | Component discovery |
| "show environment variables" | `/dg:list` | Env var inspection |
| "launch my assets" | `/dg:launch` | Execution, not listing |
| "create an asset" | `/dg:scaffold` | Creation, not discovery |
| "prototype a pipeline" | `/dg:prototype` | Building new, not listing existing |
| "best practices for assets" | `/dagster-conventions` | Learning patterns |
| "how do integrations work" | `/dagster-integrations` | Integration guidance |

## How It Works

When this skill is invoked:

1. **Identify the list request type**:
   - List definitions (assets, jobs, schedules, sensors, resources)
   - List components (available component types)
   - List environment variables
   - List projects in workspace
   - List plugins/registry modules
   - Show component tree

2. **Extract specifics** from user request:
   - Definition type (assets, schedules, etc.)
   - Filter criteria (tags, groups, kinds, patterns)
   - Output format (table vs JSON)
   - Column customization

3. **Provide appropriate command**:
   - `dg list defs` - For definitions
   - `dg list components` - For component types
   - `dg list envs` - For environment variables
   - `dg list projects` - For workspace projects
   - `dg list registry-modules` - For plugins
   - `dg list component-tree` - For component hierarchy

4. **Show relevant filters and options** based on context

## Example Flows

### List All Definitions

```
User: "Show me my assets"
→ Provide command:
  dg list defs

→ Explain:
  This shows all registered definitions including assets, asset checks,
  jobs, schedules, sensors, and resources.
```

### List Filtered Assets

```
User: "List all dbt assets"
→ Provide command:
  dg list defs --assets "kind:dbt"

→ Explain:
  Uses asset selection syntax to filter by kind.
  Other filters available: tags, groups, owners, patterns.
```

```
User: "Show me high priority assets"
→ Provide command:
  dg list defs --assets "tag:priority=high"
```

```
User: "List assets in the sales group"
→ Provide command:
  dg list defs --assets "group:sales_analytics"
```

### Customize Columns

```
User: "Show me just the asset names and descriptions"
→ Provide command:
  dg list defs --columns key,description

→ Explain available columns:
  key, group, deps, kinds, description, tags, cron, is_executable
```

### List Components

```
User: "What components can I scaffold?"
→ Provide command:
  dg list components

→ Explain:
  Shows all available component types in your environment.
  Use these with `dg scaffold defs <component_type>`.
```

```
User: "What dbt components are available?"
→ Provide command:
  dg list components --package dagster_dbt

→ Explain:
  Filters components by package name.
```

### List Environment Variables

```
User: "Show me my environment variables"
→ Provide command:
  dg list envs

→ Explain:
  Shows variables from .env file and which components use them.
  If authenticated with Dagster Plus, also shows deployment scopes.
```

```
User: "What env vars do I need?"
→ Provide command:
  dg list envs

→ Explain:
  Check the "Value" column - empty means not set in .env.
  "Components" column shows which components require each variable.
```

### List Projects

```
User: "Show me all projects in this workspace"
→ Provide command:
  dg list projects

→ Explain:
  In a workspace: lists all project paths
  In a standalone project: outputs "."
```

### JSON Output

```
User: "Export my assets as JSON"
→ Provide command:
  dg list defs --json

→ Show example processing:
  # Save to file
  dg list defs --json > assets.json

  # Extract asset keys
  dg list defs --json | jq -r '.assets[].key'

  # Filter in jq
  dg list defs --json | jq '.assets[] | select(.group == "sales")'
```

### Component Discovery for Scaffolding

```
User: "What Fivetran components can I create?"
→ Provide command:
  dg list components --package fivetran

→ Follow up:
  Once you identify the component type, scaffold it with:
  dg scaffold defs fivetran.FivetranComponent my_connector
```

### Component Tree

```
User: "Show me the component structure"
→ Provide command:
  dg list component-tree

→ For file output:
  dg list component-tree --output-file component_tree.txt
```

### Vague List Request

```
User: "Show me what I have"
→ Ask clarifying questions:
  "I can help you list several things. What would you like to see?

  Common options:
  - Definitions (assets, jobs, schedules, sensors, resources)
  - Available component types (for scaffolding)
  - Environment variables
  - Projects in workspace
  - Installed plugins

  Please specify what you'd like to list."

→ Based on response, provide appropriate command
```

### Discovery Before Action

```
User: "I want to scaffold a dbt project"
→ Guide discovery first:
  First, let's check what dbt components are available:
  dg list components --package dagster_dbt

  Then you can scaffold the one you need:
  dg scaffold defs dagster_dbt.DbtProjectComponent my_dbt
```

## Asset Selection Syntax Guide

When users ask for filtered assets, explain the selection syntax:

### By Name
```bash
# Single asset
dg list defs --assets customers

# Multiple assets
dg list defs --assets customers,orders,products

# Wildcard patterns
dg list defs --assets "customer*"
dg list defs --assets "*_raw"
```

### By Tag
```bash
# Single tag
dg list defs --assets "tag:priority=high"

# Multiple tags (AND logic)
dg list defs --assets "tag:schedule=daily tag:domain=finance"
```

### By Group
```bash
dg list defs --assets "group:sales_analytics"
```

### By Kind
```bash
dg list defs --assets "kind:dbt"
dg list defs --assets "kind:python"
```

### By Owner
```bash
dg list defs --assets "owner:team@company.com"
```

### Combined
```bash
# High-priority dbt assets
dg list defs --assets "tag:priority=high kind:dbt"
```

## Common Use Case Patterns

### Pre-Launch Validation
```
User: "I want to make sure my assets are defined before launching"
→ Provide workflow:
  # 1. Check definitions load
  dg list defs

  # 2. Verify specific assets exist
  dg list defs --assets "tag:schedule=daily"

  # 3. Check environment variables
  dg list envs

  # 4. Then launch
  dg launch --assets "tag:schedule=daily"
```

### Integration Discovery
```
User: "What integrations do I have installed?"
→ Provide commands:
  # List all components
  dg list components

  # Filter by integration type
  dg list components --package dagster_dbt
  dg list components --package fivetran
  dg list components --package dagster_dlt

  # List installed plugins
  dg list registry-modules
```

### Asset Inventory
```
User: "Generate an asset report"
→ Provide JSON workflow:
  # Export all definitions
  dg list defs --json > asset_inventory.json

  # Process with jq
  dg list defs --json | jq -r '.assets[] | "\(.key),\(.group),\(.kinds | join("|"))"'
```

### Environment Audit
```
User: "Check if all my environment variables are set"
→ Provide command:
  dg list envs

→ Explain:
  - Checkmark (✓) in "Value" column = set in .env
  - Empty "Value" column = missing from .env
  - "Components" column shows which components need each variable
```

## Implementation Notes

- This skill is a thin wrapper that delegates to the `/dg:list` subcommands
- The command file at `commands/list.md` contains comprehensive documentation
- For complex filtering and JSON processing, reference the full command documentation
- Always provide working examples, not just explanations
- Guide users toward discoverable, maintainable patterns

## Guidance Priorities

When responding to list requests, prioritize:

1. **Identify what they want to list** - Definitions, components, env vars, or projects
2. **Provide direct command** - Copy-pasteable dg list command
3. **Show relevant filters** - Asset selection, package filters, column customization
4. **JSON output when needed** - For automation and scripting
5. **Discovery workflows** - Link listing to next actions (scaffold, launch)
6. **Troubleshooting** - Empty results, missing components, env var issues

## Common Patterns to Emphasize

### Discovery Before Action
Always encourage discovery before other operations:
```bash
# Before scaffolding
dg list components  # See what's available

# Before launching
dg list defs  # See what's defined

# Before configuration
dg list envs  # See what's needed
```

### Filter Hierarchy
Guide users toward maintainable filters:
```bash
# Most maintainable (scales well)
dg list defs --assets "tag:domain=sales"
dg list defs --assets "group:analytics"
dg list defs --assets "kind:dbt"

# Specific (good for ad-hoc)
dg list defs --assets customers,orders

# All (comprehensive view)
dg list defs
```

### JSON for Automation
Encourage JSON output for programmatic use:
```bash
# Export for processing
dg list defs --json

# Pipe to jq
dg list defs --json | jq '.assets[].key'

# Save to file
dg list defs --json > inventory.json
```

## Related Commands and Skills

### Discovery Phase (This Skill)
- `/dg:list` - Discover what exists

### Action Phase
- `/dg:scaffold` - Create based on what you discovered
- `/dg:launch` - Launch based on what you listed
- `/dg:prototype` - Build new assets

### Learning Phase
- `/dagster-conventions` - Learn patterns and best practices
- `/dagster-integrations` - Understand integrations

## What Gets Provided

When you invoke this skill, you'll receive:

1. **Direct commands** - Copy-pasteable dg list commands
2. **Filter syntax** - Asset selection patterns (tags, groups, kinds)
3. **Column customization** - Available columns and how to select them
4. **JSON output examples** - For automation and scripting
5. **Component discovery** - Finding available component types
6. **Environment inspection** - Checking env vars and Dagster Plus secrets
7. **Next steps** - Link to scaffold, launch, or other relevant actions

## Full Documentation Reference

For comprehensive coverage of all list features, the underlying command documentation covers:

- All subcommands (defs, components, envs, projects, registry-modules, component-tree)
- Complete asset selection syntax
- Column customization for definitions
- Package filtering for components
- JSON output formats and processing
- Dagster Plus integration for environment variables
- Advanced patterns (IDE integration, CI/CD, automation)
- Complete troubleshooting guide

Access the full documentation at: `commands/list.md`
