# List Dagster Definitions and Components

This command guides you through discovering and inspecting Dagster definitions, components, and environment variables using the `dg list` command group.

## Overview

The `dg list` command group provides tools for discovery and inspection of your Dagster project. Use these commands to see what assets, jobs, schedules, sensors, and resources are registered, discover available component types, check environment variables, and understand your project structure.

**Key Benefits:**
- Discover all registered definitions (assets, jobs, schedules, sensors, resources)
- Find available component types for scaffolding
- Inspect environment variables and Dagster Plus secrets
- Understand project and workspace structure
- Export data as JSON for scripting and automation
- Filter and customize output columns

---

## Quick Start

### Common List Patterns

```bash
# List all definitions in project
dg list defs

# List definitions as JSON
dg list defs --json

# List only specific assets
dg list defs --assets "tag:priority=high"

# Customize columns for assets
dg list defs --columns key,group,kinds,description

# List available component types
dg list components

# List environment variables
dg list envs

# List projects in workspace
dg list projects

# List registered plugins
dg list registry-modules

# Show component tree
dg list component-tree
```

---

## Subcommands

The `dg list` command group includes six specialized subcommands for different discovery tasks.

### `dg list defs`

List all registered Dagster definitions in your project, including assets, asset checks, jobs, schedules, sensors, and resources.

**Basic usage:**
```bash
# List all definitions with default columns
dg list defs

# List as JSON (for scripting)
dg list defs --json

# List from specific path
dg list defs --path ./my_project/defs

# Filter assets by selection
dg list defs --assets "tag:priority=high"
dg list defs --assets "kind:dbt"
dg list defs --assets "group:sales_analytics"
```

**Output sections:**
- **Assets** - Data assets with metadata
- **Asset Checks** - Data quality checks
- **Jobs** - Executable jobs
- **Schedules** - Time-based automation
- **Sensors** - Event-based automation
- **Resources** - Shared resources

**Default columns for assets:**
- `key` - Asset key/name
- `group` - Asset group membership
- `deps` - Upstream dependencies
- `kinds` - Asset kinds (dbt, python, etc.)
- `description` - Asset description
- `cron` - Schedule cron expression (for schedules)

**Example output:**
```
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Section     ┃ Definitions ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ Assets      │ ┏━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━┓
│             │ ┃ Key           ┃ Group    ┃ Deps    ┃ Kinds ┃ Description   ┃
│             │ ┡━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━┩
│             │ │ customers     │ sales    │         │ dbt   │ Customer data │
│             │ │ orders        │ sales    │ customers│ python│ Order records │
│             │ └───────────────┴──────────┴─────────┴───────┴───────────────┘
│ Schedules   │ ┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
│             │ ┃ Key           ┃ Cron       ┃
│             │ ┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│             │ │ daily_refresh │ 0 0 * * *  │
│             │ └───────────────┴────────────┘
└─────────────┴────────────────────────────────┘
```

### `dg list components`

List all available Dagster component types that can be scaffolded in your Python environment.

**Basic usage:**
```bash
# List all components
dg list components

# Filter by package
dg list components --package dagster
dg list components --package dagster_dbt

# Output as JSON
dg list components --json
```

**Common component types:**
- `dagster.asset` - Basic Dagster asset
- `dagster.schedule` - Time-based schedule
- `dagster.sensor` - Event-driven sensor
- `dagster_dbt.DbtProjectComponent` - dbt project integration
- `fivetran.FivetranComponent` - Fivetran connector
- `dagster_dlt.DltResource` - dlt data pipeline
- `sling.SlingReplicationComponent` - Sling data replication

**Example output:**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Key                           ┃ Summary                       ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ dagster.asset                 │ A basic Dagster asset         │
│ dagster.schedule              │ A time-based schedule         │
│ dagster_dbt.DbtProjectComponent│ A dbt project component      │
│ fivetran.FivetranComponent    │ Fivetran connector component  │
└───────────────────────────────┴───────────────────────────────┘
```

**Use with scaffold:**
```bash
# First, discover available components
dg list components --package dagster_dbt

# Then scaffold the component
dg scaffold defs dagster_dbt.DbtProjectComponent my_dbt_project
```

### `dg list envs`

List environment variables from the `.env` file and show which components require them. When authenticated with Dagster Plus, also shows which deployment scopes have values set.

**Basic usage:**
```bash
# List environment variables
dg list envs
```

**Output columns:**
- **Env Var** - Variable name
- **Value** - Checkmark (✓) if set in local .env file
- **Components** - Which component instances use this variable
- **Dev** - (Dagster Plus only) Set in local deployment scope
- **Branch** - (Dagster Plus only) Set in branch deployment scope
- **Full** - (Dagster Plus only) Set in full deployment scope

**Example output (without Dagster Plus):**
```
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Env Var           ┃ Value ┃ Components   ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━┩
│ DATABASE_URL      │ ✓     │ postgres     │
│ FIVETRAN_API_KEY  │ ✓     │ fivetran     │
│ FIVETRAN_API_SECRET│ ✓    │ fivetran     │
│ DBT_PROJECT_DIR   │       │ dbt          │
└───────────────────┴───────┴──────────────┘
```

**Example output (with Dagster Plus):**
```
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━┳━━━━━━━━┳━━━━━━┓
┃ Env Var           ┃ Value ┃ Components   ┃ Dev ┃ Branch ┃ Full ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━━╇━━━━━━┩
│ DATABASE_URL      │ ✓     │ postgres     │ ✓   │ ✓      │ ✓    │
│ FIVETRAN_API_KEY  │ ✓     │ fivetran     │ ✓   │ ✓      │ ✓    │
│ FIVETRAN_API_SECRET│ ✓    │ fivetran     │ ✓   │ ✓      │ ✓    │
│ DBT_PROJECT_DIR   │       │ dbt          │     │        │      │
└───────────────────┴───────┴──────────────┴─────┴────────┴──────┘
```

**Use cases:**
- Identify missing environment variables before launch
- Verify Dagster Plus secrets are configured
- Audit which components require which variables
- Generate environment variable documentation

### `dg list projects`

List projects in the current workspace, or emit the current project directory if in a standalone project.

**Basic usage:**
```bash
# In a workspace: lists all project paths
dg list projects

# In a standalone project: outputs "."
dg list projects
```

**Example output (in workspace):**
```
./project_a
./project_b
./analytics
./etl
```

**Example output (in standalone project):**
```
.
```

**Use cases:**
- CI/CD scripts that need to iterate over all projects
- Workspace validation
- Multi-project automation

**CI/CD example:**
```bash
# Run tests for all projects in workspace
for project in $(dg list projects); do
  echo "Testing $project"
  cd "$project" && uv run pytest
done
```

### `dg list registry-modules`

List all registered dg plugins (registry modules) in the current Python environment.

**Basic usage:**
```bash
# List all plugins
dg list registry-modules

# Output as JSON
dg list registry-modules --json
```

**Example output:**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Module                    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ dagster                   │
│ dagster_dbt               │
│ dagster_fivetran          │
│ dagster_dlt               │
│ sling                     │
└───────────────────────────┘
```

**Use cases:**
- Verify plugin installation
- Audit available integrations
- Debug component discovery issues
- Generate plugin documentation

### `dg list component-tree`

Display a hierarchical tree view of component instances in the current project.

**Basic usage:**
```bash
# Print tree to stdout
dg list component-tree

# Write tree to file
dg list component-tree --output-file component_tree.txt
```

**Example output:**
```
my_project/
├── defs/
│   ├── dbt_project/
│   │   └── DbtProjectComponent
│   ├── fivetran_connector/
│   │   └── FivetranComponent
│   └── sales_assets/
│       ├── customers (asset)
│       └── orders (asset)
```

**Use cases:**
- Visualize project structure
- Document component organization
- Debug component hierarchy issues
- Understand component relationships

---

## Options and Flags

### Common Options (All Subcommands)

**`--target-path <path>`**
- Specify directory context for the command
- Typically a folder with `dg.toml` or `pyproject.toml`
- Default: Current working directory

```bash
dg list defs --target-path /path/to/project
```

**`--verbose`**
- Enable verbose output for debugging
- Shows additional diagnostic information

```bash
dg list defs --verbose
```

### `dg list defs` Options

**`--json`**
- Output as JSON instead of formatted table
- Useful for scripting and automation

```bash
dg list defs --json
```

**`-p, --path <path>`**
- Path to specific definitions to list
- Filter definitions by directory

```bash
dg list defs --path ./my_project/defs/sales
```

**`-a, --assets <selection>`**
- Asset selection to filter results
- Uses same syntax as `dg launch --assets`
- Supports tags, groups, kinds, owners, patterns

```bash
# By tag
dg list defs --assets "tag:priority=high"

# By group
dg list defs --assets "group:sales_analytics"

# By kind
dg list defs --assets "kind:dbt"

# By name pattern
dg list defs --assets "customer*"

# Multiple criteria (AND logic)
dg list defs --assets "tag:priority=high kind:dbt"
```

**`-c, --columns <columns>`**
- Customize displayed columns
- Can be comma-separated list or multiple flags
- Available columns: `key`, `group`, `deps`, `kinds`, `description`, `tags`, `cron`, `is_executable`
- Default: `key`, `group`, `deps`, `kinds`, `description`, `cron`

```bash
# Comma-separated
dg list defs --columns key,group,description

# Multiple flags
dg list defs -c key -c group -c kinds -c description

# Show all available columns
dg list defs -c key -c group -c deps -c kinds -c description -c tags -c is_executable
```

**Column availability by definition type:**
- Assets: `key`, `group`, `deps`, `kinds`, `description`, `tags`, `is_executable`
- Asset Checks: `key`, `deps`, `description`
- Jobs: `key`, `description`
- Schedules: `key`, `cron`
- Sensors: `key`
- Resources: `key`

### `dg list components` Options

**`-p, --package <package>`**
- Filter components by package name
- Supports dot-separated module names for finer granularity

```bash
# Top-level package
dg list components --package dagster

# Specific submodule
dg list components --package dagster_dbt
```

**`--json`**
- Output as JSON instead of table

```bash
dg list components --json
```

### `dg list registry-modules` Options

**`--json`**
- Output as JSON instead of table

```bash
dg list registry-modules --json
```

### `dg list component-tree` Options

**`--output-file <file>`**
- Write tree to file instead of stdout
- Useful for documentation generation

```bash
dg list component-tree --output-file docs/component_tree.txt
```

---

## Asset Selection Syntax

The `--assets` flag in `dg list defs` uses the same powerful selection syntax as `dg launch`.

### Selection by Name

```bash
# Single asset
dg list defs --assets customers

# Multiple assets
dg list defs --assets customers,orders,products

# Wildcard patterns
dg list defs --assets "customer*"        # Assets starting with "customer"
dg list defs --assets "*_raw"            # Assets ending with "_raw"
dg list defs --assets "*"                # All assets
```

### Selection by Tag

```bash
# Single tag
dg list defs --assets "tag:priority=high"

# Multiple tags (AND logic)
dg list defs --assets "tag:schedule=daily tag:domain=finance"

# Tag exists (any value)
dg list defs --assets "tag:critical"
```

### Selection by Group

```bash
# Single group
dg list defs --assets "group:sales_analytics"

# Multiple groups
dg list defs --assets "group:sales_analytics group:marketing"
```

### Selection by Kind

```bash
# Single kind
dg list defs --assets "kind:dbt"

# Multiple kinds
dg list defs --assets "kind:dbt kind:python"
```

### Selection by Owner

```bash
# By owner
dg list defs --assets "owner:team@company.com"
dg list defs --assets "owner:data-engineering"
```

### Complex Selection

Combine multiple criteria using space-separated selectors (AND logic):

```bash
# High-priority dbt assets
dg list defs --assets "tag:priority=high kind:dbt"

# Sales analytics Python assets
dg list defs --assets "group:sales_analytics kind:python"
```

---

## Use Cases

### Discovery: Finding What Exists

**Explore project definitions:**
```bash
# See everything registered
dg list defs

# Focus on assets only
dg list defs --columns key,group,kinds,description

# Find dbt assets
dg list defs --assets "kind:dbt"

# Find high-priority work
dg list defs --assets "tag:priority=high"
```

**Discover available components:**
```bash
# What component types can I scaffold?
dg list components

# What dbt components are available?
dg list components --package dagster_dbt

# What integrations do I have?
dg list components | grep -i "fivetran\|airbyte\|dlt"
```

### Validation: Pre-Flight Checks

**Before launching assets:**
```bash
# Verify definitions load
dg list defs

# Check specific assets exist
dg list defs --assets "tag:schedule=daily"

# Verify environment variables
dg list envs
```

**CI/CD validation:**
```bash
#!/bin/bash
# Validate all projects in workspace

for project in $(dg list projects); do
  echo "Validating $project..."

  cd "$project"

  # Check definitions load
  if ! dg list defs > /dev/null 2>&1; then
    echo "ERROR: Definitions failed to load in $project"
    exit 1
  fi

  # Check for missing environment variables
  missing_vars=$(dg list envs | grep -c "^[A-Z_].*│\s*│")
  if [ "$missing_vars" -gt 0 ]; then
    echo "WARNING: $missing_vars environment variables not set in $project"
  fi

  echo "✓ $project validated"
done
```

### Automation: Scripting with JSON

**Generate asset inventory:**
```bash
# Export all assets as JSON
dg list defs --json > asset_inventory.json

# Extract asset keys
dg list defs --json | jq -r '.assets[].key'

# Find assets without descriptions
dg list defs --json | jq -r '.assets[] | select(.description == null) | .key'

# Group assets by kind
dg list defs --json | jq -r '.assets | group_by(.kinds[]) | map({kind: .[0].kinds[0], count: length})'
```

**Generate documentation:**
```bash
#!/bin/bash
# Generate markdown documentation from definitions

echo "# Asset Inventory" > assets.md
echo "" >> assets.md

# Get all assets as JSON
assets=$(dg list defs --json | jq -r '.assets')

# Generate markdown table
echo "| Asset | Group | Kinds | Description |" >> assets.md
echo "|-------|-------|-------|-------------|" >> assets.md

echo "$assets" | jq -r '.[] | "| \(.key) | \(.group // "N/A") | \(.kinds | join(", ")) | \(.description // "No description") |"' >> assets.md

echo "Documentation generated: assets.md"
```

**Monitor environment variables:**
```bash
# Check if all required variables are set
dg list envs --json | jq -r '.[] | select(.value == "") | .env_var'

# Compare local vs Dagster Plus
dg list envs | grep "DATABASE_URL"
```

### Debugging: Understanding Issues

**Component discovery issues:**
```bash
# What plugins are registered?
dg list registry-modules

# Are my components visible?
dg list components --package my_company

# Component tree structure
dg list component-tree
```

**Asset dependency visualization:**
```bash
# Show asset dependencies
dg list defs --columns key,deps

# Find assets without dependencies (source assets)
dg list defs --json | jq -r '.assets[] | select(.deps | length == 0) | .key'

# Find assets with many dependencies
dg list defs --json | jq -r '.assets[] | select(.deps | length > 5) | "\(.key): \(.deps | length) deps"'
```

### Documentation: Generating References

**Component catalog:**
```bash
# Generate component reference
dg list components --json | jq -r '.[] | "## \(.key)\n\n\(.summary)\n"' > components.md
```

**Environment variable reference:**
```bash
# Document required variables
echo "# Environment Variables" > env_vars.md
dg list envs | grep "✓" | awk '{print "- `" $1 "` - Used by: " $3}'  >> env_vars.md
```

---

## Advanced Patterns

### IDE Integration

**PyCharm External Tool:**

Create external tool to list definitions:
1. Settings → Tools → External Tools → Add
2. **Program**: `dg` (or `/path/to/dg`)
3. **Arguments**: `list defs --columns key,group,kinds,description`
4. **Working directory**: `$ProjectFileDir$`

**VSCode Task:**

Add to `.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "List Dagster Definitions",
      "type": "shell",
      "command": "dg list defs",
      "problemMatcher": [],
      "group": "none"
    },
    {
      "label": "List Dagster Components",
      "type": "shell",
      "command": "dg list components",
      "problemMatcher": [],
      "group": "none"
    }
  ]
}
```

### JSON Processing with jq

**Filter and transform:**
```bash
# Assets by group
dg list defs --json | jq '.assets | group_by(.group) | map({group: .[0].group, assets: map(.key)})'

# Assets with specific tag
dg list defs --json | jq '.assets[] | select(.tags[] | contains("priority=high"))'

# Schedule summary
dg list defs --json | jq '.schedules | map({name: .name, cron: .cron_schedule})'
```

**Generate reports:**
```bash
# Asset counts by kind
dg list defs --json | jq -r '
  .assets
  | map(.kinds[])
  | group_by(.)
  | map({kind: .[0], count: length})
  | .[]
  | "\(.kind): \(.count)"
'

# Assets without descriptions
dg list defs --json | jq -r '
  .assets
  | map(select(.description == null or .description == ""))
  | length
' | xargs -I {} echo "Assets without descriptions: {}"
```

### CI/CD Integration

**GitHub Actions:**
```yaml
name: Validate Definitions

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: uv pip install -e .

      - name: Validate definitions load
        run: dg list defs

      - name: Check for missing descriptions
        run: |
          missing=$(dg list defs --json | jq '.assets | map(select(.description == null or .description == "")) | length')
          if [ "$missing" -gt 0 ]; then
            echo "WARNING: $missing assets without descriptions"
          fi

      - name: Generate asset inventory
        run: dg list defs --json > asset_inventory.json

      - name: Upload inventory
        uses: actions/upload-artifact@v3
        with:
          name: asset-inventory
          path: asset_inventory.json
```

**GitLab CI:**
```yaml
validate_definitions:
  stage: test
  script:
    - pip install uv
    - uv pip install -e .
    - dg list defs
    - dg list envs
  artifacts:
    reports:
      dotenv: .env
```

### Workspace Automation

**Iterate over all projects:**
```bash
#!/bin/bash
# Run command for each project

for project in $(dg list projects); do
  echo "Processing $project..."
  cd "$project" || continue

  # Your commands here
  dg list defs --columns key,group

  cd - > /dev/null
done
```

**Aggregate statistics:**
```bash
#!/bin/bash
# Count assets across all projects

total_assets=0
total_schedules=0

for project in $(dg list projects); do
  cd "$project" || continue

  assets=$(dg list defs --json | jq '.assets | length')
  schedules=$(dg list defs --json | jq '.schedules | length')

  total_assets=$((total_assets + assets))
  total_schedules=$((total_schedules + schedules))

  echo "$project: $assets assets, $schedules schedules"

  cd - > /dev/null
done

echo ""
echo "Total: $total_assets assets, $total_schedules schedules"
```

---

## Output Formats

### Table Output

Default output is a formatted table with borders and styling:

```
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Section     ┃ Definitions ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ Assets      │ ...table... │
│ Schedules   │ ...table... │
└─────────────┴─────────────┘
```

**Characteristics:**
- Human-readable formatting
- Nested tables for sections
- Truncated descriptions (max 100 characters)
- Colored output (when terminal supports it)

### JSON Output

Use `--json` flag for machine-readable output:

```json
{
  "assets": [
    {
      "key": "customers",
      "group": "sales",
      "deps": [],
      "kinds": ["dbt"],
      "description": "Customer data",
      "tags": ["priority:high", "schedule:daily"],
      "is_executable": true
    }
  ],
  "asset_checks": [],
  "jobs": [],
  "schedules": [
    {
      "name": "daily_refresh",
      "cron_schedule": "0 0 * * *"
    }
  ],
  "sensors": [],
  "resources": []
}
```

**Characteristics:**
- Complete data (no truncation)
- Parseable with `jq`, `python`, etc.
- Suitable for automation
- No color formatting

**Processing JSON output:**
```bash
# Pretty print
dg list defs --json | jq '.'

# Extract specific fields
dg list defs --json | jq '.assets[].key'

# Filter and transform
dg list defs --json | jq '.assets[] | select(.group == "sales")'
```

---

## Troubleshooting

### Common Errors and Solutions

#### "No definitions found"

```bash
# Error
No definitions are defined for this project.

# Solution: Check definitions load
dg check defs

# Common causes:
# 1. Not in project directory
# 2. Definitions have syntax errors
# 3. Missing __init__.py files
# 4. Import errors in definitions
```

#### "Component type not found"

```bash
# Error
Component type 'foo.bar' not found

# Solution: List available components
dg list components

# Check if package is installed
dg list registry-modules

# Verify plugin installation
pip list | grep dagster
```

#### Empty output for `dg list envs`

```bash
# Output
No environment variables are defined for this project.

# Possible causes:
# 1. No .env file exists
# 2. No components require environment variables
# 3. .env file is empty

# Solution: Check for .env file
ls -la .env

# Create .env if missing
touch .env
```

#### "Failed to load definitions"

```bash
# Error during dg list defs
Error: Failed to load definitions

# Solution: Use verbose mode
dg list defs --verbose

# Check for import errors
python -c "from my_project.defs import defs"

# Validate syntax
dg check defs
```

#### Permission denied accessing Dagster Plus

```bash
# Error during dg list envs (with Plus integration)
Error: Permission denied

# Solution: Verify authentication
dagster-plus auth list

# Re-authenticate if needed
dagster-plus auth login

# Check organization configuration
cat ~/.dagster/dagster-plus.yaml
```

### Debug Mode

**Enable verbose output:**
```bash
# Show detailed information
dg list defs --verbose

# Check environment
env | grep DAGSTER

# Verify context
dg check defs
```

**Diagnose component discovery:**
```bash
# What plugins are loaded?
dg list registry-modules --verbose

# What components are available?
dg list components --verbose

# Is my custom component registered?
dg list components | grep -i "my_component"
```

### Testing Before Production

**Validate in CI:**
```bash
# Check definitions load
dg list defs || exit 1

# Verify required assets exist
dg list defs --assets "tag:critical" || exit 1

# Check environment variables
missing=$(dg list envs | grep -c "│\s*│")
if [ "$missing" -gt 0 ]; then
  echo "WARNING: Missing environment variables"
fi
```

---

## Related Commands

- `/dg:launch` - Materialize assets discovered with `dg list defs`
- `/dg:scaffold` - Scaffold components discovered with `dg list components`
- `/dagster-conventions` - Learn asset patterns and best practices
- `/dagster-integrations` - Explore available integrations

## See Also

- [Asset Patterns Reference](../../dagster-conventions/skills/dagster-conventions/references/assets.md)
- [Component Scaffolding](./scaffold.md)
- [Launch Command](./launch.md)
- [Dagster CLI Documentation](https://docs.dagster.io/guides/cli)
