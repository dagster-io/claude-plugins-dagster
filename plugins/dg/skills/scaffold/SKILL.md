---
name: dg:scaffold
description: Scaffold Dagster components, assets, schedules, sensors, and integrations. Use when user wants to create, scaffold, generate, or add components, assets, integrations (dbt, Fivetran, dlt, Sling), schedules, sensors, or custom component types.
---

# Scaffold Dagster Components and Code Skill

This skill helps users scaffold Dagster components, assets, schedules, sensors, and integrations through natural language requests, providing comprehensive guidance on component discovery, parameter configuration, and format selection.

## When to Use This Skill

Auto-invoke when users say:
- "create an asset called customers"
- "scaffold a dbt project"
- "add a Fivetran connector"
- "create a schedule"
- "scaffold a sensor"
- "add a dlt pipeline"
- "create a Sling replication"
- "scaffold an asset for sales data"
- "generate a daily schedule"
- "add a file watcher sensor"
- "create a custom component"
- "scaffold an inline component"
- "how do I scaffold X"
- "how do I create X component"

## When to Use This Skill vs. Others

| If User Says... | Use This Skill/Command | Why |
|----------------|------------------------|-----|
| "create an asset" | `/dg:scaffold` | Scaffolding new component |
| "scaffold a dbt project" | `/dg:scaffold` | Integration scaffolding |
| "add a Fivetran connector" | `/dg:scaffold` | Component creation |
| "show available components" | `/dg:list` | Discovery, not creation |
| "list my assets" | `/dg:list` | Inspection, not creation |
| "launch my assets" | `/dg:launch` | Execution, not creation |
| "prototype a pipeline" | `/dg:prototype` | Full implementation, not just scaffold |
| "create a project" | `/dg:create-project` | Project initialization |
| "best practices" | `/dagster-conventions` | Learning patterns |

## How It Works

When this skill is invoked:

1. **Identify the scaffold request type**:
   - Asset scaffolding
   - Schedule scaffolding
   - Sensor scaffolding
   - Integration scaffolding (dbt, Fivetran, dlt, Sling)
   - Inline component
   - Custom component type

2. **Extract specifics** from user request:
   - Component type (if mentioned)
   - Component name/path
   - Format preference (YAML vs Python)
   - Parameters (if provided)

3. **Guide discovery if needed**:
   - If component type unclear, suggest `dg list components`
   - Show available options for the integration type

4. **Provide appropriate command**:
   - `dg scaffold defs <component_type> <path>` - For components
   - `dg scaffold defs inline-component` - For custom inline components
   - `dg scaffold component` - For reusable component types

5. **Show parameter options** based on component type

## Example Flows

### Scaffold Basic Asset

```
User: "Create an asset called customers"
→ Provide command:
  dg scaffold defs dagster.asset customers --format python

→ Explain:
  Creates: defs/customers/defs.py with asset definition
  Edit the file to add your asset logic.
```

### Scaffold Asset with Path

```
User: "Create an asset called customers in the sales folder"
→ Provide command:
  dg scaffold defs dagster.asset sales/customers --format python

→ Explain:
  Creates: defs/sales/customers/defs.py
  Path structure helps organize related assets.
```

### Scaffold Schedule

```
User: "Create a daily schedule"
→ Ask for name:
  "What would you like to name the schedule?"

User: "daily_refresh"
→ Provide command:
  dg scaffold defs dagster.schedule daily_refresh --format python

→ Explain:
  Edit the generated schedule to set:
  - cron_schedule (e.g., "0 0 * * *" for daily at midnight)
  - job_name (which job to run)
```

### Scaffold Sensor

```
User: "Create a sensor to watch for files"
→ Ask for name:
  "What would you like to name the sensor?"

User: "file_watcher"
→ Provide command:
  dg scaffold defs dagster.sensor file_watcher --format python

→ Explain:
  Edit the generated sensor to implement your detection logic.
```

### Scaffold dbt Project

```
User: "Scaffold a dbt project"
→ Discover first:
  Let me help you scaffold a dbt integration.

  First, let's check available dbt components:
  dg list components --package dagster_dbt

→ Then scaffold:
  dg scaffold defs dagster_dbt.DbtProjectComponent dbt_project --json-params '{
    "project_dir": "./dbt_project",
    "target": "dev"
  }'

→ Explain:
  This creates the dbt integration at defs/dbt_project/
  Make sure your dbt project exists at ./dbt_project/
```

### Scaffold Fivetran Connector

```
User: "Add a Fivetran connector for Salesforce"
→ Provide command:
  dg scaffold defs fivetran.FivetranComponent salesforce --json-params '{
    "connector_id": "your_connector_id",
    "destination_id": "your_destination_id"
  }'

→ Explain:
  Get connector_id and destination_id from Fivetran UI.

  Then add to .env:
  FIVETRAN_API_KEY=your_key
  FIVETRAN_API_SECRET=your_secret
```

### Scaffold dlt Pipeline

```
User: "Create a dlt pipeline"
→ Ask for details:
  "What would you like to name the dlt pipeline?"

User: "github_data"
→ Provide command:
  dg scaffold defs dagster_dlt.DltResource github_data --json-params '{
    "pipeline_name": "github_to_snowflake",
    "dataset_name": "github_data"
  }'
```

### Scaffold Sling Replication

```
User: "Create a Sling replication from Postgres to Snowflake"
→ Provide command:
  dg scaffold defs sling.SlingReplicationComponent postgres_to_snowflake --json-params '{
    "source_connection": "POSTGRES",
    "target_connection": "SNOWFLAKE",
    "streams": [
      {
        "source_table": "public.customers",
        "target_table": "raw.customers"
      }
    ]
  }'

→ Explain:
  Configure connections in .env:
  SLING_POSTGRES=postgresql://...
  SLING_SNOWFLAKE=snowflake://...
```

### Scaffold Inline Component

```
User: "Create a custom component in my project"
→ Provide command:
  dg scaffold defs inline-component my_component --typename MyComponent

→ Explain:
  Creates:
  - defs/my_component/my_component.py (component class)
  - defs/my_component/defs.yaml (instance config)

  Edit the class to implement your build_defs() logic.
```

### Scaffold with Format Choice

```
User: "Create an asset with YAML configuration"
→ Provide command:
  dg scaffold defs dagster.asset my_asset --format yaml

→ Explain:
  YAML format: Creates defs.yaml with component configuration
  Python format: Creates defs.py with @dg.asset decorator

  Choose based on preference and complexity.
```

### Vague Scaffold Request

```
User: "I want to scaffold something"
→ Ask clarifying questions:
  "I can help you scaffold components. What would you like to create?

  Common options:
  - Assets (data pipelines)
  - Schedules (time-based automation)
  - Sensors (event-based automation)
  - Integrations:
    - dbt project
    - Fivetran connector
    - dlt pipeline
    - Sling replication
  - Custom components

  What would you like to scaffold?"

→ Based on response, provide appropriate command
```

### Discovery-First Workflow

```
User: "What integrations can I scaffold?"
→ Guide discovery:
  Let's discover what's available:
  dg list components

  For specific integration:
  dg list components --package dagster_dbt
  dg list components --package fivetran
  dg list components --package dagster_dlt
  dg list components --package sling

→ Follow up:
  Once you find the component type you want, scaffold it with:
  dg scaffold defs <component_type> <name>
```

### Unknown Component Type

```
User: "Scaffold a MyCustomThing"
→ Provide discovery:
  I'm not sure about that component type. Let's check:
  dg list components | grep -i "custom"

  Or list all available components:
  dg list components

→ Explain disambiguation:
  If you provide a partial match, dg will help you:
  dg scaffold defs custom my_instance

  Will prompt you to select from matching components.
```

### Bulk Scaffolding Request

```
User: "Create assets for customers, orders, and products"
→ Provide batch approach:
  You can scaffold multiple assets:

  dg scaffold defs dagster.asset sales/customers --format python
  dg scaffold defs dagster.asset sales/orders --format python
  dg scaffold defs dagster.asset sales/products --format python

→ Or show script:
  #!/bin/bash
  for asset in customers orders products; do
    dg scaffold defs dagster.asset "sales/$asset" --format python
  done
```

## Component Type Guide

### Core Dagster Components

**Assets:**
```bash
dg scaffold defs dagster.asset my_asset --format python
```

**Schedules:**
```bash
dg scaffold defs dagster.schedule daily_job --format python
```

**Sensors:**
```bash
dg scaffold defs dagster.sensor file_watcher --format python
```

### Integration Components

**dbt:**
```bash
dg scaffold defs dagster_dbt.DbtProjectComponent dbt_project --json-params '{
  "project_dir": "./dbt_project"
}'
```

**Fivetran:**
```bash
dg scaffold defs fivetran.FivetranComponent connector_name --json-params '{
  "connector_id": "abc123",
  "destination_id": "def456"
}'
```

**dlt:**
```bash
dg scaffold defs dagster_dlt.DltResource pipeline_name --json-params '{
  "pipeline_name": "my_pipeline"
}'
```

**Sling:**
```bash
dg scaffold defs sling.SlingReplicationComponent replication_name --json-params '{
  "source_connection": "SOURCE",
  "target_connection": "TARGET"
}'
```

## Parameter Strategies

### JSON Parameters (Recommended for Complex Configs)

```bash
dg scaffold defs fivetran.FivetranComponent my_connector --json-params '{
  "connector_id": "abc123",
  "destination_id": "def456",
  "poll_interval": "10m"
}'
```

**When to use:**
- Multiple parameters
- Nested structures
- Automation/scripting
- Complex configuration

### Individual Flags (For Simple Configs)

```bash
dg scaffold defs my_component.MyType instance \
  --param1 value1 \
  --param2 value2
```

**When to use:**
- Few simple parameters
- Interactive use
- Clear parameter names

**Important:** Cannot mix `--json-params` with individual flags.

## Format Selection Guide

### YAML Format (Default for Components)

```bash
dg scaffold defs dagster.asset my_asset --format yaml
```

**Creates:** `defs/my_asset/defs.yaml`
```yaml
component_type: dagster.asset
params:
  # Configuration here
```

**Best for:**
- Configuration-driven workflows
- Consistency across team
- Easier for non-Python users

### Python Format

```bash
dg scaffold defs dagster.asset my_asset --format python
```

**Creates:** `defs/my_asset/defs.py`
```python
import dagster as dg

@dg.asset
def my_asset():
    pass
```

**Best for:**
- Custom logic needed
- Python-first workflows
- Complex asset definitions

## Common Scaffolding Patterns

### By Domain

```bash
# Sales domain
dg scaffold defs dagster.asset sales/customers --format python
dg scaffold defs dagster.asset sales/orders --format python

# Marketing domain
dg scaffold defs dagster.asset marketing/campaigns --format python
dg scaffold defs dagster.asset marketing/leads --format python
```

### By Layer

```bash
# Raw layer (ingestion)
dg scaffold defs fivetran.FivetranComponent raw/salesforce
dg scaffold defs fivetran.FivetranComponent raw/hubspot

# Staging layer (transformation)
dg scaffold defs dagster_dbt.DbtProjectComponent staging/dbt_project

# Analytics layer (business logic)
dg scaffold defs dagster.asset analytics/customer_metrics --format python
```

### Full Project Setup

```bash
# 1. Create project
dg create project my_analytics

# 2. Scaffold integrations
dg scaffold defs dagster_dbt.DbtProjectComponent dbt_project
dg scaffold defs fivetran.FivetranComponent salesforce

# 3. Scaffold downstream assets
dg scaffold defs dagster.asset analytics/revenue --format python

# 4. Scaffold automation
dg scaffold defs dagster.schedule daily_refresh --format python

# 5. Verify
dg list defs
```

## Implementation Notes

- This skill is a thin wrapper that delegates to `/dg:scaffold` subcommands
- The command file at `commands/scaffold.md` contains comprehensive documentation
- **Dynamic command generation**: Available subcommands depend on installed packages
- Always encourage discovery before scaffolding (`dg list components`)
- Guide users through interactive disambiguation when needed
- Provide working examples with realistic parameters

## Guidance Priorities

When responding to scaffold requests, prioritize:

1. **Component discovery** - Guide users to find available component types first
2. **Direct commands** - Provide copy-pasteable scaffold commands
3. **Parameter guidance** - Show required and optional parameters
4. **Format selection** - Explain YAML vs Python trade-offs
5. **Post-scaffold steps** - Edit files, configure env vars, verify
6. **Path conventions** - Encourage organized directory structures
7. **Integration-specific setup** - API keys, connections, configuration files

## Common Patterns to Emphasize

### Discovery Before Scaffolding

Always encourage discovery first:
```bash
# 1. Discover
dg list components --package dagster_dbt

# 2. Scaffold
dg scaffold defs dagster_dbt.DbtProjectComponent my_dbt
```

### Organized Structure

Guide toward maintainable organization:
```
defs/
├── raw/              # Data ingestion
├── staging/          # Transformations
├── analytics/        # Business logic
└── automation/       # Schedules & sensors
```

### Complete Setup Workflow

Provide full context:
```bash
# 1. Scaffold component
dg scaffold defs fivetran.FivetranComponent salesforce --json-params '{...}'

# 2. Configure environment
echo "FIVETRAN_API_KEY=..." >> .env
echo "FIVETRAN_API_SECRET=..." >> .env

# 3. Verify
dg list defs
dg list envs

# 4. Test
dg launch --assets salesforce
```

## Related Commands and Skills

### Discovery Phase
- `/dg:list` - Discover available components before scaffolding

### Scaffolding Phase (This Skill)
- `/dg:scaffold` - Create components and code

### Validation Phase
- `/dg:list` - Verify scaffolded components appear
- `/dg:launch` - Test scaffolded assets

### Implementation Phase
- `/dg:prototype` - Full implementation with custom logic
- `/dagster-conventions` - Learn patterns for implementing assets

### Learning Phase
- `/dagster-integrations` - Understand integration patterns
- `/dignified-python` - Python code quality

## What Gets Provided

When you invoke this skill, you'll receive:

1. **Direct commands** - Copy-pasteable scaffold commands
2. **Component discovery guidance** - How to find available types
3. **Parameter examples** - Required and optional parameters
4. **Format recommendations** - YAML vs Python guidance
5. **Path conventions** - Organized directory structures
6. **Post-scaffold checklist** - Edit files, configure env vars, verify
7. **Integration-specific setup** - API keys, connections, configuration
8. **Next steps** - Link to verification and testing

## Full Documentation Reference

For comprehensive coverage of all scaffold features, the underlying command documentation covers:

- All subcommands (defs, inline-component, component, build-artifacts, github-actions)
- Dynamic command generation and discovery
- Component type guide (Dagster core, integrations)
- Format options (YAML vs Python)
- Parameter strategies (JSON vs individual flags)
- Interactive disambiguation flow
- Directory structure conventions
- Integration-specific examples (dbt, Fivetran, dlt, Sling)
- Advanced patterns (bulk scaffolding, automation, templating)
- Complete troubleshooting guide

Access the full documentation at: `commands/scaffold.md`
