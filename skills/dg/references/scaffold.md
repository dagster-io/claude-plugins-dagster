# Scaffold Dagster Components and Code

This command guides you through creating Dagster components, assets, schedules, sensors, and
integrations using the `dg scaffold` command group.

## Overview

The `dg scaffold` command group provides tools for generating Dagster code and component instances.
These commands create boilerplate code, configuration files, and directory structures following
Dagster best practices.

**Key Benefits:**

- Rapidly create component instances (assets, schedules, sensors, integrations)
- Dynamically discover available component types from your Python environment
- Support for both YAML and Python configuration formats
- Interactive disambiguation for partial matches
- Scaffolds follow project conventions automatically
- Integrate with dbt, Fivetran, dlt, Sling, and other tools

**What makes `scaffold defs` special:** The `dg scaffold defs` subcommands are **dynamically
generated** based on available component types in your Python environment. This means the available
commands depend on which Dagster packages you have installed.

---

## Quick Start

### Common Scaffold Patterns

```bash
# Discover available component types
dg list components

# Scaffold a basic asset
dg scaffold defs dagster.asset my_asset

# Scaffold a schedule
dg scaffold defs dagster.schedule daily_job

# Scaffold a dbt project
dg scaffold defs dagster_dbt.DbtProjectComponent my_dbt_project

# Scaffold with parameters (YAML format)
dg scaffold defs dagster.asset sales_data --format yaml

# Scaffold with parameters (Python format)
dg scaffold defs dagster.asset sales_data --format python

# Scaffold with JSON parameters
dg scaffold defs fivetran.FivetranComponent my_connector --json-params '{"connector_id": "abc123"}'

# Scaffold inline component (custom component in project)
dg scaffold defs inline-component my_component --typename MyComponent

# Scaffold reusable component type
dg scaffold component my_library_component
```

---

## Subcommands

The `dg scaffold` command group includes several subcommands for different scaffolding tasks.

### `dg scaffold defs <COMPONENT_TYPE>`

Scaffold a component instance. The available subcommands are **dynamically generated** based on
component types in your Python environment.

**Important:** You must first discover available component types using `dg list components` before
scaffolding.

#### Basic Usage

```bash
# General syntax
dg scaffold defs <COMPONENT_TYPE> <DEFS_PATH> [OPTIONS]

# Scaffold at specific path
dg scaffold defs dagster.asset sales/customers

# This creates: <project>/defs/sales/customers/
```

#### Common Component Types

**Dagster Core Components:**

```bash
# Asset
dg scaffold defs dagster.asset my_asset

# Schedule
dg scaffold defs dagster.schedule daily_refresh

# Sensor
dg scaffold defs dagster.sensor file_watcher
```

**dbt Integration:**

```bash
# dbt project component
dg scaffold defs dagster_dbt.DbtProjectComponent my_dbt

# Creates dbt integration with asset generation
```

**Fivetran Integration:**

```bash
# Fivetran connector
dg scaffold defs fivetran.FivetranComponent my_connector --json-params '{
  "connector_id": "connector_id_from_fivetran",
  "destination_id": "destination_id_from_fivetran"
}'
```

**dlt Integration:**

```bash
# dlt resource
dg scaffold defs dagster_dlt.DltResource my_pipeline
```

**Sling Integration:**

```bash
# Sling replication
dg scaffold defs sling.SlingReplicationComponent my_replication --json-params '{
  "source_connection": "MY_SOURCE",
  "target_connection": "MY_TARGET",
  "streams": []
}'
```

#### Dynamic Command Discovery

The `scaffold defs` command has special discovery behavior:

**1. Exact match:**

```bash
# Full typename (exact match)
dg scaffold defs dagster.asset my_asset
```

**2. Partial match with disambiguation:**

```bash
# Partial match - prompts for selection
dg scaffold defs dbt my_project

# Output:
# No exact match found for 'dbt'. Did you mean one of these?
# (1) dagster_dbt.DbtProjectComponent
# (2) dagster_dbt.DbtCliResource
# (n) quit
# Select an option (number): 1
```

**3. Short name aliases:**

```bash
# Some components have short aliases
dg scaffold defs asset my_asset       # Same as dagster.asset
dg scaffold defs schedule my_schedule # Same as dagster.schedule
dg scaffold defs sensor my_sensor     # Same as dagster.sensor
```

**4. Python reference resolution:**

```bash
# Can reference any Python object
dg scaffold defs my_package.MyCustomComponent instance_name
```

#### Format Options

Components can be scaffolded in YAML or Python format:

**YAML format (default for components):**

```bash
dg scaffold defs dagster.asset my_asset --format yaml
```

Creates `my_asset/defs.yaml`:

```yaml
component_type: dagster.asset
params:
  # Asset configuration parameters
```

**Python format:**

```bash
dg scaffold defs dagster.asset my_asset --format python
```

Creates `my_asset/defs.py`:

```python
import dagster as dg

@dg.asset
def my_asset():
    pass
```

#### Scaffold Parameters

Components can accept scaffold parameters in two ways:

**Option 1: JSON parameters (recommended for complex configs):**

```bash
dg scaffold defs fivetran.FivetranComponent my_connector --json-params '{
  "connector_id": "abc123",
  "destination_id": "def456",
  "poll_interval": "10m"
}'
```

**Option 2: Individual flags:**

```bash
# Each parameter as a flag (dynamically generated from component schema)
dg scaffold defs my_component.MyType instance \
  --param1 value1 \
  --param2 value2 \
  --param3 value3
```

**Important:** Cannot mix `--json-params` with individual parameter flags. Choose one method.

#### Directory Structure

Scaffolded components are created in the project's `defs` directory:

```
my_project/
├── defs/
│   ├── my_asset/                 # Component instance directory
│   │   └── defs.yaml             # Component configuration (YAML format)
│   │   # OR
│   │   └── defs.py               # Component definition (Python format)
│   ├── sales/
│   │   └── customers/
│   │       └── defs.yaml
│   └── integrations/
│       └── dbt_project/
│           └── defs.yaml
```

### `dg scaffold defs inline-component`

Scaffold an inline Python component within your project. Inline components are custom component
types defined directly in your project (not as separate packages).

**Basic usage:**

```bash
dg scaffold defs inline-component <PATH> --typename <NAME> [--superclass <CLASS>]
```

**Arguments:**

- `PATH` - Path for the component (relative to defs directory)
- `--typename` - Component typename (required)
- `--superclass` - Superclass for component (optional, defaults to `dg.Component`)

**Examples:**

**Simple inline component:**

```bash
dg scaffold defs inline-component my_component --typename MyComponent
```

Creates:

- `defs/my_component/my_component.py` - Component class definition
- `defs/my_component/defs.yaml` - Component instance configuration

```python
# my_component.py
import dagster as dg

class MyComponent(dg.Component):
    """My custom component."""

    def build_defs(self):
        # Your component logic
        return dg.Definitions(assets=[])
```

**Component with custom superclass:**

```bash
dg scaffold defs inline-component data_loader \
  --typename DataLoaderComponent \
  --superclass my_project.lib.BaseComponent
```

**Use cases:**

- Creating project-specific component types
- Encapsulating common patterns
- Building reusable abstractions within a project
- Prototyping before extracting to separate package

### `dg scaffold component <NAME>`

Create a reusable component type as a library module. This scaffolds a full component type structure
that can be used across projects or published as a package.

**Basic usage:**

```bash
dg scaffold component <NAME>
```

**Creates structure:**

```
<project>/
└── lib/
    └── <name>/
        ├── __init__.py
        ├── component.py        # Component class
        └── scaffolder.py       # Scaffolder (optional)
```

**Example:**

```bash
# Create custom component type
dg scaffold component api_poller

# Use in project
dg scaffold defs my_project.lib.api_poller.ApiPollerComponent my_api
```

**Use cases:**

- Building reusable component types for your organization
- Creating component libraries
- Developing Dagster integrations
- Sharing patterns across projects

### `dg scaffold build-artifacts` (Legacy)

Scaffold a Dockerfile for building Dagster projects or workspaces.

**Status:** Maintained for backward compatibility. **Recommendation:** Use
`dg plus deploy configure` instead for complete deployment setup.

**Basic usage:**

```bash
dg scaffold build-artifacts [--python-version <version>] [-y]
```

**Options:**

- `--python-version` - Python version (3.9, 3.10, 3.11, 3.12, 3.13)
- `-y, --yes` - Skip confirmation prompt

**Example:**

```bash
dg scaffold build-artifacts --python-version 3.11 -y
```

Creates `Dockerfile` in project root.

**Modern alternative:**

```bash
# Use dg plus deploy configure instead
dg plus deploy configure serverless
dg plus deploy configure hybrid
```

### `dg scaffold github-actions` (Legacy)

Scaffold a GitHub Actions workflow for Dagster project CI/CD.

**Status:** Maintained for backward compatibility. **Recommendation:** Use
`dg plus deploy configure --git-provider github` instead.

**Basic usage:**

```bash
dg scaffold github-actions
```

Creates `.github/workflows/dagster.yml`.

**Modern alternative:**

```bash
# Use dg plus deploy configure instead
dg plus deploy configure serverless --git-provider github
dg plus deploy configure hybrid --git-provider github
```

---

## Options and Flags

### `dg scaffold defs` Options

**`--format <yaml|python>`**

- Format of component configuration
- Choices: `yaml` (default for components), `python`
- Only applicable for component types

```bash
# YAML configuration
dg scaffold defs dagster.asset my_asset --format yaml

# Python definition
dg scaffold defs dagster.asset my_asset --format python
```

**`--json-params <json>`**

- JSON string of scaffold parameters
- Mutually exclusive with individual parameter flags
- Required format: Valid JSON object

```bash
dg scaffold defs fivetran.FivetranComponent my_connector --json-params '{
  "connector_id": "abc123",
  "destination_id": "def456"
}'
```

**Component-specific parameters:**

- Dynamically generated from component schema
- Displayed in `dg scaffold defs <type> --help`
- Can be passed as individual flags

```bash
# Example with hypothetical component
dg scaffold defs my_component.MyType instance \
  --param1 value1 \
  --param2 value2
```

### `dg scaffold defs inline-component` Options

**`--typename <name>` (required)**

- Component typename
- Used for class name and registration

**`--superclass <class>` (optional)**

- Superclass for the component
- Defaults to `dg.Component` if not specified
- Can reference custom base classes

```bash
dg scaffold defs inline-component my_comp \
  --typename MyComponent \
  --superclass my_project.lib.BaseComponent
```

### `dg scaffold build-artifacts` Options

**`--python-version <version>`**

- Python version for Docker image
- Choices: 3.9, 3.10, 3.11, 3.12, 3.13
- Defaults to current Python version

**`-y, --yes`**

- Skip confirmation prompt
- Useful for automation

---

## Use Cases

### Creating Assets

**Basic asset scaffolding:**

```bash
# Scaffold asset
dg scaffold defs dagster.asset sales/customers --format python

# Edit the generated file
# defs/sales/customers/defs.py
```

Generated Python asset:

```python
import dagster as dg

@dg.asset
def customers():
    """Asset description."""
    pass
```

**Asset with configuration:**

```bash
# Scaffold with YAML config
dg scaffold defs dagster.asset sales/customers --format yaml

# Edit configuration
# defs/sales/customers/defs.yaml
```

Generated YAML config:

```yaml
component_type: dagster.asset
params:
  key: customers
  group_name: sales
```

### Integrating with dbt

**Scaffold dbt project component:**

```bash
# Scaffold dbt integration
dg scaffold defs dagster_dbt.DbtProjectComponent dbt_project --json-params '{
  "project_dir": "./dbt_project",
  "target": "dev"
}'
```

**Directory structure:**

```
my_project/
├── defs/
│   └── dbt_project/
│       └── defs.yaml
└── dbt_project/          # Your dbt project directory
    ├── models/
    ├── dbt_project.yml
    └── profiles.yml
```

**Generated configuration:**

```yaml
component_type: dagster_dbt.DbtProjectComponent
params:
  project_dir: ./dbt_project
  target: dev
```

### Integrating with Fivetran

**Scaffold Fivetran connector:**

```bash
# Get connector_id and destination_id from Fivetran UI
dg scaffold defs fivetran.FivetranComponent salesforce --json-params '{
  "connector_id": "salesforce_connector_id",
  "destination_id": "snowflake_destination_id",
  "poll_interval": "5m"
}'
```

**Generated configuration:**

```yaml
component_type: fivetran.FivetranComponent
params:
  connector_id: salesforce_connector_id
  destination_id: snowflake_destination_id
  poll_interval: 5m
```

**Required environment variables:**

```bash
# Add to .env
FIVETRAN_API_KEY=your_api_key
FIVETRAN_API_SECRET=your_api_secret

# Verify with dg list envs
dg list envs
```

### Integrating with dlt

**Scaffold dlt resource:**

```bash
dg scaffold defs dagster_dlt.DltResource github_pipeline --json-params '{
  "pipeline_name": "github_to_snowflake",
  "dataset_name": "github_data"
}'
```

### Integrating with Sling

**Scaffold Sling replication:**

```bash
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
```

### Creating Schedules

**Scaffold schedule:**

```bash
dg scaffold defs dagster.schedule daily_refresh --format python
```

Generated schedule:

```python
import dagster as dg

@dg.schedule(
    cron_schedule="0 0 * * *",  # Daily at midnight
    job_name="my_job"
)
def daily_refresh():
    return {}
```

### Creating Sensors

**Scaffold sensor:**

```bash
dg scaffold defs dagster.sensor file_watcher --format python
```

Generated sensor:

```python
import dagster as dg

@dg.sensor(job_name="my_job")
def file_watcher(context):
    # Sensor logic
    pass
```

### Creating Custom Components

**Inline component for project:**

```bash
# Create inline component
dg scaffold defs inline-component api_loader --typename ApiLoaderComponent

# Edit component logic
# defs/api_loader/api_loader.py

# Use the component
# Reference it as my_project.defs.api_loader.ApiLoaderComponent
```

**Reusable component library:**

```bash
# Create component type
dg scaffold component api_poller

# Edit component in lib/api_poller/component.py

# Scaffold instances
dg scaffold defs my_project.lib.api_poller.ApiPollerComponent github_api
dg scaffold defs my_project.lib.api_poller.ApiPollerComponent slack_api
```

### Project Initialization Workflows

**New project with integrations:**

```bash
# Initialize project
dg create project my_analytics

cd my_analytics

# Scaffold dbt integration
dg scaffold defs dagster_dbt.DbtProjectComponent dbt_project

# Scaffold Fivetran connectors
dg scaffold defs fivetran.FivetranComponent salesforce --json-params '{...}'
dg scaffold defs fivetran.FivetranComponent hubspot --json-params '{...}'

# Scaffold downstream assets
dg scaffold defs dagster.asset analytics/customer_metrics --format python
dg scaffold defs dagster.asset analytics/sales_dashboard --format python

# Scaffold schedule
dg scaffold defs dagster.schedule daily_refresh --format python

# Verify structure
dg list defs
```

---

## Advanced Patterns

### Interactive Disambiguation

When you provide a partial component name, `dg scaffold` helps you find the right component:

**Example:**

```bash
$ dg scaffold defs dbt my_project

No exact match found for 'dbt'. Did you mean one of these?
(1) dagster_dbt.DbtProjectComponent
(2) dagster_dbt.DbtCliResource
(3) dagster_dbt.DbtManifestComponent
(n) quit
Select an option (number): 1

Using defs scaffolder: dagster_dbt.DbtProjectComponent
Scaffolding dagster_dbt.DbtProjectComponent at defs/my_project/
```

**Workflow:**

1. Provide partial match (e.g., "dbt")
2. System searches for matching component types
3. If multiple matches, presents interactive menu
4. Select the desired component
5. Scaffold proceeds with selected component

### Discovery-First Workflow

**Recommended workflow:**

```bash
# 1. Discover available components
dg list components

# 2. Filter by package if needed
dg list components --package dagster_dbt

# 3. Get component details (use --help with scaffold)
dg scaffold defs dagster_dbt.DbtProjectComponent --help

# 4. Scaffold with appropriate parameters
dg scaffold defs dagster_dbt.DbtProjectComponent my_dbt --json-params '{...}'
```

### Parameter Strategies

**Complex parameters with JSON:**

```bash
# Good for: Nested structures, many parameters, automation
dg scaffold defs sling.SlingReplicationComponent replication --json-params '{
  "source_connection": "POSTGRES",
  "target_connection": "SNOWFLAKE",
  "streams": [
    {"source_table": "public.users", "target_table": "raw.users"},
    {"source_table": "public.orders", "target_table": "raw.orders"}
  ],
  "mode": "incremental"
}'
```

**Individual flags for simple parameters:**

```bash
# Good for: Few parameters, interactive use
dg scaffold defs my_component.MyType instance \
  --source postgres \
  --target snowflake \
  --mode incremental
```

**Parameters from file:**

```bash
# Store parameters in file
cat > params.json <<EOF
{
  "connector_id": "abc123",
  "destination_id": "def456",
  "poll_interval": "10m"
}
EOF

# Use file contents
dg scaffold defs fivetran.FivetranComponent my_connector --json-params "$(cat params.json)"
```

### Scaffolding Patterns

**Convention: Group by domain:**

```
defs/
├── sales/           # Sales domain
│   ├── customers/
│   ├── orders/
│   └── revenue/
├── marketing/       # Marketing domain
│   ├── campaigns/
│   └── leads/
└── integrations/    # External integrations
    ├── fivetran/
    ├── dbt/
    └── sling/
```

**Convention: Group by layer:**

```
defs/
├── raw/            # Raw data ingestion
│   ├── fivetran_salesforce/
│   └── fivetran_hubspot/
├── staging/        # Staging transformations
│   └── dbt_project/
└── analytics/      # Analytics assets
    ├── customer_metrics/
    └── revenue_dashboard/
```

### IDE Integration

**VSCode snippet for scaffolding:**

Add to `.vscode/dagster.code-snippets`:

```json
{
  "Scaffold Dagster Asset": {
    "prefix": "dg-scaffold-asset",
    "body": ["dg scaffold defs dagster.asset ${1:path}/${2:name} --format python"],
    "description": "Scaffold a Dagster asset"
  },
  "Scaffold dbt Project": {
    "prefix": "dg-scaffold-dbt",
    "body": [
      "dg scaffold defs dagster_dbt.DbtProjectComponent ${1:name} --json-params '{\"project_dir\": \"${2:./dbt_project}\", \"target\": \"${3:dev}\"}'"
    ],
    "description": "Scaffold a dbt project component"
  }
}
```

### Automation and Scripting

**Bulk scaffolding:**

```bash
#!/bin/bash
# Scaffold multiple assets from list

assets=(
  "sales/customers"
  "sales/orders"
  "sales/products"
  "marketing/campaigns"
  "marketing/leads"
)

for asset in "${assets[@]}"; do
  echo "Scaffolding $asset..."
  dg scaffold defs dagster.asset "$asset" --format python
done

echo "Scaffolded ${#assets[@]} assets"
```

**Templated scaffolding:**

```bash
#!/bin/bash
# Scaffold with templated parameters

read -p "Fivetran Connector ID: " connector_id
read -p "Destination ID: " destination_id
read -p "Component name: " name

dg scaffold defs fivetran.FivetranComponent "$name" --json-params "{
  \"connector_id\": \"$connector_id\",
  \"destination_id\": \"$destination_id\",
  \"poll_interval\": \"10m\"
}"

echo "Scaffolded Fivetran component: $name"
```

**CI/CD scaffolding validation:**

```bash
#!/bin/bash
# Validate scaffolded components in CI

# Scaffold test component
dg scaffold defs dagster.asset test_asset --format python

# Verify definitions load
if dg list defs | grep -q "test_asset"; then
  echo "✓ Scaffold successful"
  exit 0
else
  echo "✗ Scaffold failed"
  exit 1
fi
```

---

## Output and Results

### Success Output

**Scaffolding asset:**

```bash
$ dg scaffold defs dagster.asset sales/customers --format python

Scaffolding dagster.asset at defs/sales/customers/
Created: defs/sales/customers/defs.py
```

**Scaffolding component with config:**

```bash
$ dg scaffold defs fivetran.FivetranComponent salesforce --json-params '{...}'

Scaffolding fivetran.FivetranComponent at defs/salesforce/
Created: defs/salesforce/defs.yaml
```

### Directory Structure Results

**After scaffolding assets:**

```
my_project/
├── defs/
│   ├── sales/
│   │   ├── customers/
│   │   │   └── defs.py        # Asset definition
│   │   └── orders/
│   │       └── defs.py
│   └── analytics/
│       └── metrics/
│           └── defs.yaml      # Component config
```

**After scaffolding integrations:**

```
my_project/
├── defs/
│   ├── fivetran_salesforce/
│   │   └── defs.yaml
│   ├── dbt_project/
│   │   └── defs.yaml
│   └── sling_replication/
│       └── defs.yaml
└── .env                       # Environment variables
```

### Post-Scaffold Checklist

After scaffolding, complete these steps:

**1. Edit generated files:**

```bash
# Edit asset logic
vim defs/sales/customers/defs.py

# Edit component config
vim defs/fivetran_salesforce/defs.yaml
```

**2. Configure environment variables:**

```bash
# Add required variables to .env
echo "FIVETRAN_API_KEY=your_key" >> .env
echo "FIVETRAN_API_SECRET=your_secret" >> .env

# Verify
dg list envs
```

**3. Validate definitions:**

```bash
# Check definitions load
dg list defs

# Verify specific asset
dg list defs --assets "customers"
```

**4. Test execution:**

```bash
# Launch asset
dg launch --assets customers

# Or use dev server
dg dev
```

---

## Troubleshooting

### Common Errors and Solutions

#### "Component type not found"

```bash
# Error
Error: Scaffoldable object type 'foo.bar' not found.

# Solution: List available components
dg list components

# Check spelling
dg list components | grep -i "foo"

# Verify package installation
pip list | grep dagster

# Install missing package
pip install dagster-foo
```

#### "Path already exists"

```bash
# Error
Error: Path 'defs/my_asset' already exists.

# Solution: Use different path
dg scaffold defs dagster.asset my_asset_v2

# Or remove existing path
rm -rf defs/my_asset
dg scaffold defs dagster.asset my_asset
```

#### "Invalid JSON parameters"

```bash
# Error
Error: Invalid JSON in --json-params

# Solution: Validate JSON
echo '{...}' | jq .

# Use proper quoting
dg scaffold defs my_component.MyType instance --json-params '{
  "key": "value"
}'

# Or use file
dg scaffold defs my_component.MyType instance --json-params "$(cat params.json)"
```

#### "Parameter validation failed"

```bash
# Error
Error validating scaffold parameters for 'fivetran.FivetranComponent':
{
  "connector_id": "field required"
}

# Solution: Check required parameters
dg scaffold defs fivetran.FivetranComponent --help

# Provide required parameters
dg scaffold defs fivetran.FivetranComponent my_connector --json-params '{
  "connector_id": "required_value",
  "destination_id": "required_value"
}'
```

#### "Cannot use --json-params with individual options"

```bash
# Error
Error: Detected params passed as both --json-params and individual options.

# Solution: Choose one method
# Either use --json-params:
dg scaffold defs my_component.MyType instance --json-params '{...}'

# Or use individual flags:
dg scaffold defs my_component.MyType instance --param1 value1 --param2 value2
```

#### "Not in project directory"

```bash
# Error
Error: Must be run inside a Dagster project directory.

# Solution: Navigate to project
cd /path/to/dagster/project

# Verify project structure
ls dg.toml pyproject.toml

# Or create project
dg create project my_project
cd my_project
```

### Debug Mode

**Get help for specific component:**

```bash
# Show component-specific help
dg scaffold defs dagster.asset --help
dg scaffold defs fivetran.FivetranComponent --help

# List available parameters
dg scaffold defs my_component.MyType --help
```

**Verify component discovery:**

```bash
# What components are available?
dg list components

# Is specific component registered?
dg list components | grep -i "mycomponent"

# What plugins are loaded?
dg list registry-modules
```

**Check generated files:**

```bash
# View generated file
cat defs/my_asset/defs.py

# Check file structure
tree defs/

# Validate definitions load
dg list defs
```

### Testing Scaffolded Components

**Validation workflow:**

```bash
# 1. Scaffold component
dg scaffold defs dagster.asset test_asset --format python

# 2. Check definitions load
dg list defs

# 3. Verify asset appears
dg list defs --assets "test_asset"

# 4. Try launching
dg launch --assets test_asset

# 5. Check in dev UI
dg dev
```

---

## Related Commands

- `/dg:list` - Discover available components before scaffolding
- `/dg:launch` - Launch scaffolded assets
- `/dagster-conventions` - Learn component patterns and best practices
- `/dagster-integrations` - Explore integration patterns

## See Also

- [Component Discovery](./list.md#dg-list-components)
- [Launch Command](./launch.md)
- [Asset Patterns Reference](../../dagster-conventions/skills/dagster-conventions/references/assets.md)
- [Dagster CLI Documentation](https://docs.dagster.io/guides/cli)
