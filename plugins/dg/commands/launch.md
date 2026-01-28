# Launch Dagster Assets

This command guides you through materializing (launching) Dagster assets using the modern
`dg launch` CLI.

## Overview

The `dg launch` command is the modern, streamlined way to materialize assets in Dagster projects. It
replaces the legacy `dagster asset materialize` command with a simpler, more intuitive interface.

**Key Benefits:**

- Simpler syntax: `dg launch --assets my_asset` vs
  `python -m dagster asset materialize --select my_asset`
- Better asset selection syntax (tags, groups, kinds, patterns)
- Native support for partitions and partition ranges
- Seamless environment variable integration
- Works with both local and remote execution

---

## Quick Start

### Common Launch Patterns

```bash
# Single asset
dg launch --assets my_asset

# Multiple specific assets
dg launch --assets asset_1,asset_2,asset_3

# All assets
dg launch --assets "*"

# Assets by tag
dg launch --assets "tag:priority=high"

# Assets by group
dg launch --assets "group:sales_analytics"

# Assets by kind
dg launch --assets "kind:dbt"

# Specific job
dg launch --job my_daily_job

# With partition
dg launch --assets my_partitioned_asset --partition 2024-01-15

# Partition range (backfill)
dg launch --assets my_asset --partition-range "2024-01-01...2024-01-31"
```

---

## Asset Selection Syntax

The `--assets` flag accepts powerful selection patterns to target specific assets.

### Selection by Name

```bash
# Single asset by name
dg launch --assets customers

# Multiple assets by name
dg launch --assets customers,orders,products

# Wildcard patterns
dg launch --assets "customer*"        # All assets starting with "customer"
dg launch --assets "*_raw"            # All assets ending with "_raw"
dg launch --assets "staging_*_daily"  # Pattern matching
dg launch --assets "*"                # All assets
```

### Selection by Tag

Assets can be selected by their tags:

```bash
# Single tag
dg launch --assets "tag:priority=high"

# Multiple tags (AND logic)
dg launch --assets "tag:schedule=daily tag:domain=finance"

# Tag exists (any value)
dg launch --assets "tag:critical"
```

**Example asset with tags:**

```python
@dg.asset(
    tags={"priority": "high", "domain": "finance", "schedule": "daily"}
)
def financial_report():
    pass
```

### Selection by Group

```bash
# Single group
dg launch --assets "group:sales_analytics"

# Multiple groups
dg launch --assets "group:sales_analytics group:marketing"
```

**Example asset with group:**

```python
@dg.asset(group_name="sales_analytics")
def customer_revenue():
    pass
```

### Selection by Kind

```bash
# Single kind
dg launch --assets "kind:dbt"

# Multiple kinds
dg launch --assets "kind:dbt kind:python"
```

**Example asset with kinds:**

```python
@dg.asset(kinds={"snowflake", "python"})
def processed_data():
    pass
```

### Selection by Owner

```bash
# By owner email/tag
dg launch --assets "owner:team@company.com"
dg launch --assets "owner:data-engineering"
```

**Example asset with owner:**

```python
@dg.asset(owners=["team:data-engineering"])
def pipeline_asset():
    pass
```

### Complex Selection Patterns

Combine multiple selection criteria:

```bash
# AND logic (space-separated)
dg launch --assets "tag:priority=high kind:dbt"

# OR logic (multiple --assets flags or pipe)
# Note: This depends on your CLI version; typically use multiple invocations

# Exclude patterns (use asset selection negation if supported)
# Check `dg launch --help` for your version's syntax
```

---

## Partitions

Partitioned assets represent data that is logically divided by date, category, or other dimensions.

### Single Partition

Launch a specific partition:

```bash
# Date partition
dg launch --assets my_daily_asset --partition 2024-01-15

# Custom partition key
dg launch --assets my_asset --partition "region_us_west"
```

**Example daily partitioned asset:**

```python
from dagster import DailyPartitionsDefinition, asset

@asset(partitions_def=DailyPartitionsDefinition(start_date="2024-01-01"))
def daily_sales():
    pass
```

### Partition Ranges (Backfills)

Launch multiple partitions at once:

```bash
# Date range (inclusive)
dg launch --assets my_asset --partition-range "2024-01-01...2024-01-31"

# Recent partitions
dg launch --assets my_asset --partition-range "2024-01-01..."  # From date to latest

# Custom partition range
dg launch --assets my_asset --partition-range "Q1...Q4"
```

**Common backfill scenarios:**

```bash
# Backfill last 7 days
dg launch --assets daily_metrics --partition-range "2024-01-08...2024-01-15"

# Backfill entire year
dg launch --assets yearly_report --partition-range "2024-01-01...2024-12-31"

# Backfill multiple assets for same range
dg launch --assets "tag:schedule=daily" --partition-range "2024-01-01...2024-01-31"
```

### Static Partitions

For non-time-based partitions:

```bash
# Single static partition
dg launch --assets regional_data --partition "us_west"

# Launch multiple partitions (requires multiple commands)
dg launch --assets regional_data --partition "us_west"
dg launch --assets regional_data --partition "us_east"
```

**Example static partitioned asset:**

```python
from dagster import StaticPartitionsDefinition, asset

@asset(partitions_def=StaticPartitionsDefinition(["us_west", "us_east", "eu"]))
def regional_data():
    pass
```

### Multi-Dimensional Partitions

For assets with multiple partition dimensions (e.g., date + region):

```bash
# Check your Dagster version for multi-dimensional partition syntax
# Typically requires specifying each dimension
dg launch --assets my_asset --partition "2024-01-15|us_west"
```

---

## Configuration

Pass runtime configuration to your assets using `--config-json`.

### Inline JSON Configuration

```bash
# Simple config
dg launch --assets my_asset --config-json '{"ops": {"my_asset": {"config": {"param": "value"}}}}'

# Asset-level config
dg launch --assets my_asset --config-json '{"ops": {"my_asset": {"config": {"batch_size": 1000, "enable_validation": true}}}}'
```

### Configuration File

For complex configurations, use a JSON file:

```bash
# Create config file
cat > launch_config.json <<EOF
{
  "ops": {
    "my_asset": {
      "config": {
        "batch_size": 1000,
        "enable_validation": true,
        "source_table": "raw_customers"
      }
    }
  }
}
EOF

# Launch with config file
dg launch --assets my_asset --config-json "$(cat launch_config.json)"
```

### Configurable Assets Example

**Asset with config schema:**

```python
from dagster import asset, Config

class MyAssetConfig(Config):
    batch_size: int = 100
    enable_validation: bool = True
    source_table: str

@asset
def my_asset(config: MyAssetConfig):
    # Access config values
    batch_size = config.batch_size
    source = config.source_table
    pass
```

### Resource Configuration

Resources are configured via environment variables (see Environment Setup section below), not via
`--config-json`.

**Resource configuration happens in your code:**

```python
from dagster import ConfigurableResource, EnvVar

class DatabaseResource(ConfigurableResource):
    connection_string: str = EnvVar("DATABASE_URL")
    pool_size: int = EnvVar.int("DB_POOL_SIZE")
```

---

## Environment Variables

Assets and resources often require environment variables for configuration (API keys, database URLs,
etc.).

### Method 1: Direct uv with .env (Automatic)

If using `uv`, it automatically loads `.env` files:

```bash
# Create .env file
cat > .env <<EOF
DATABASE_URL=postgresql://localhost:5432/mydb
API_KEY=your-api-key-here
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
EOF

# Launch (automatically loads .env)
uv run dg launch --assets my_asset
```

### Method 2: Explicit Shell Sourcing (bash/zsh)

For non-uv environments or explicit control:

```bash
# Load .env into shell environment
set -a          # Automatically export all variables
source .env
set +a          # Turn off automatic export

# Launch with loaded environment
dg launch --assets my_asset
```

**One-liner version:**

```bash
set -a; source .env; set +a; dg launch --assets my_asset
```

### Method 3: Per-Environment Files

Manage multiple environments with separate .env files:

```bash
# Development
source .env.dev && dg launch --assets my_asset

# Staging
source .env.staging && dg launch --assets my_asset

# Production (typically not launched locally)
source .env.prod && dg launch --assets my_asset
```

**Directory structure:**

```
my_project/
├── .env              # Default (dev)
├── .env.dev          # Development
├── .env.staging      # Staging
├── .env.prod         # Production (sensitive, add to .gitignore!)
└── src/
```

### Method 4: Inline Environment Variables

For quick testing or single variables:

```bash
# Single variable
DATABASE_URL=postgresql://localhost:5432/mydb dg launch --assets my_asset

# Multiple variables
DATABASE_URL=postgresql://localhost:5432/mydb API_KEY=test-key dg launch --assets my_asset
```

### Environment Variable Best Practices

1. **Never commit secrets** - Add `.env*` to `.gitignore` (except `.env.example`)
2. **Use .env.example** - Template file with placeholder values
3. **Validate early** - Use `EnvVar` in resources to catch missing vars at definition load time
4. **Separate environments** - Use different .env files per environment
5. **Document requirements** - List all required variables in README

**Example .env.example:**

```bash
# Database Configuration
DATABASE_URL=postgresql://localhost:5432/mydb

# API Keys
API_KEY=your-api-key-here
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key

# Optional Settings
BATCH_SIZE=1000
ENABLE_DEBUG=false
```

---

## Job Execution

Execute predefined jobs that run multiple assets:

```bash
# Execute a job by name
dg launch --job my_daily_job

# Job with partition
dg launch --job my_job --partition 2024-01-15

# Job with config
dg launch --job my_job --config-json '{"ops": {...}}'
```

**Example job definition:**

```python
import dagster as dg

# Define a job that runs specific assets
my_daily_job = dg.define_asset_job(
    name="my_daily_job",
    selection="tag:schedule=daily"
)

# Register in Definitions
defs = dg.Definitions(
    assets=[...],
    jobs=[my_daily_job]
)
```

---

## Advanced Patterns

### PyCharm/IDE Integration

**Run Configuration in PyCharm:**

1. Create a new Python run configuration
2. **Script path**: Point to your Python executable
3. **Parameters**: `-m dagster_dg_cli.cli launch --assets my_asset`
4. **Environment file**: Select your `.env` file
5. **Working directory**: Your project root

**Alternative using uv:**

- **Program**: `/path/to/uv`
- **Parameters**: `run python -m dagster_dg_cli.cli launch --assets my_asset`
- **Environment file**: Your `.env` file (automatically loaded by uv)

### CI/CD Integration

**GitHub Actions example:**

```yaml
name: Launch Dagster Assets

on:
  schedule:
    - cron: "0 0 * * *" # Daily at midnight
  workflow_dispatch: # Manual trigger

jobs:
  launch:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: uv pip install -e .

      - name: Launch assets
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          API_KEY: ${{ secrets.API_KEY }}
        run: |
          uv run dg launch --assets "tag:schedule=daily"
```

### Testing Asset Materialization

Test that assets can materialize successfully:

```bash
# Quick test of single asset
dg launch --assets my_asset

# Test asset chain (dependencies)
dg launch --assets downstream_asset  # Automatically materializes upstream deps

# Dry-run validation (check definitions load)
dg check defs

# List assets before launching
dg list defs
```

### Selective Re-materialization

Re-run failed or stale assets:

```bash
# Re-run specific asset
dg launch --assets my_asset

# Re-run all assets with specific tag
dg launch --assets "tag:priority=high"

# Re-run failed partition
dg launch --assets my_asset --partition 2024-01-15
```

---

## Cloud/Remote Execution

When working with Dagster Cloud or remote run launchers, behavior differs:

### Dagster Cloud

The `dg launch` command works differently with Dagster Cloud:

```bash
# Local execution (default)
dg launch --assets my_asset

# Cloud execution (if configured)
# Requires Dagster Cloud deployment configured in your project
```

**Important Cloud Considerations:**

1. **Run Launcher Configuration**: Check your `dagster.yaml` or code location settings
2. **Environment Variables**: Managed through Cloud UI or deployment config, not local .env
3. **Secrets**: Use Cloud secrets manager, not local environment variables
4. **Permissions**: Ensure your Cloud API token has launch permissions

**Dagster Cloud Code Locations:**

If your project is deployed to Dagster Cloud as a code location, launches happen remotely:

```python
# dagster.yaml or code location config
run_launcher:
  module: dagster_cloud.workspace.user_code_launcher
  class: CloudRunLauncher
```

With this configuration:

- `dg launch` submits a run to Dagster Cloud
- Execution happens on Cloud infrastructure (not locally)
- Logs appear in Cloud UI
- Environment variables come from Cloud deployment config

**Hybrid Approach:**

For local development + Cloud production:

```bash
# Local testing (no cloud launcher)
dg launch --assets my_asset

# Cloud deployment (via CD pipeline)
# Typically use Dagster Cloud UI or API for production launches
```

### Custom Run Launchers

For custom run launchers (Kubernetes, Docker, etc.):

```bash
# Default: In-process launcher
dg launch --assets my_asset

# With custom launcher configured in dagster.yaml
# Check your project's run_launcher configuration
```

**Example Kubernetes Run Launcher:**

```yaml
# dagster.yaml
run_launcher:
  module: dagster_k8s
  class: K8sRunLauncher
  config:
    image: my-dagster-image:latest
    namespace: dagster-prod
```

With this launcher, `dg launch` creates Kubernetes jobs for each run.

---

## Troubleshooting

### Common Errors and Solutions

#### "No definitions found"

```bash
# Error
Error: No definitions found in the current project

# Solution: Verify definitions load
dg check defs

# Common causes:
# 1. Not in project root directory
# 2. definitions.py has syntax errors
# 3. Missing dependencies
```

#### "Asset not found"

```bash
# Error
Error: Asset "my_asset" not found

# Solution: List all available assets
dg list defs

# Verify asset is registered in Definitions
# Check spelling and ensure asset is imported
```

#### "Partition not found"

```bash
# Error
Error: Partition "2024-01-15" not found for asset "my_asset"

# Solution: Check partition definition
# 1. Verify asset has partitions_def
# 2. Ensure partition is within defined range
# 3. Check partition key format (date format, etc.)

# List asset details
dg list defs --json | grep -A 10 "my_asset"
```

#### "Missing environment variable"

```bash
# Error
dagster._core.errors.DagsterInvalidConfigError: Missing required environment variable: DATABASE_URL

# Solution: Ensure .env is loaded
set -a; source .env; set +a
dg launch --assets my_asset

# Or use uv (auto-loads .env)
uv run dg launch --assets my_asset

# Verify variable is set
echo $DATABASE_URL
```

#### "Config validation failed"

```bash
# Error
Error: Invalid configuration for asset "my_asset"

# Solution: Check config schema
# 1. Review asset's Config class definition
# 2. Ensure JSON structure matches
# 3. Verify data types (int vs string, etc.)

# Example correct config structure:
dg launch --assets my_asset --config-json '{
  "ops": {
    "my_asset": {
      "config": {
        "batch_size": 1000,
        "source_table": "customers"
      }
    }
  }
}'
```

#### "Resource initialization failed"

```bash
# Error
Error: Failed to initialize resource "database"

# Solution: Check resource configuration
# 1. Verify environment variables are set
# 2. Test connection manually (psql, curl, etc.)
# 3. Check resource ConfigurableResource implementation
# 4. Review error logs for specifics

# Debug resource loading
dg check defs  # Should catch resource issues early
```

#### "Job not found"

```bash
# Error
Error: Job "my_job" not found

# Solution: List available jobs
dg list defs  # Shows all jobs

# Ensure job is registered in Definitions
# Verify job name spelling
```

### Debug Mode

For detailed debug output:

```bash
# Enable debug logging (if supported by your version)
DAGSTER_DEBUG=1 dg launch --assets my_asset

# Or check logs after launch
dg logs <run_id>  # Use /dg:logs command for detailed log retrieval
```

### Testing Before Launch

Validate before launching:

```bash
# 1. Check definitions load
dg check defs

# 2. List all assets
dg list defs

# 3. Test in dev UI (optional)
dg dev  # Opens UI at http://localhost:3000
# Materialize assets via UI to see detailed logs
```

---

## Migration Guide

Migrating from legacy `dagster asset materialize` to modern `dg launch`.

### Command Mapping

| Legacy Command                                           | Modern Equivalent                                                     |
| -------------------------------------------------------- | --------------------------------------------------------------------- |
| `dagster asset materialize -a my_asset`                  | `dg launch --assets my_asset`                                         |
| `dagster asset materialize --select my_asset`            | `dg launch --assets my_asset`                                         |
| `dagster asset materialize -a asset1 -a asset2`          | `dg launch --assets asset1,asset2`                                    |
| `python -m dagster asset materialize -a my_asset`        | `dg launch --assets my_asset` or `uv run dg launch --assets my_asset` |
| `dagster asset materialize --select "tag:priority=high"` | `dg launch --assets "tag:priority=high"`                              |
| `dagster job execute -j my_job`                          | `dg launch --job my_job`                                              |

### Syntax Changes

**Legacy (dagster asset materialize):**

```bash
# Required full module invocation
python -m dagster asset materialize --select my_asset

# Verbose environment setup
set -a; source .env; set +a; python -m dagster asset materialize -a my_asset
```

**Modern (dg launch):**

```bash
# Simple, direct command
dg launch --assets my_asset

# Or with uv (auto-loads .env)
uv run dg launch --assets my_asset
```

### Feature Parity

All legacy features are supported in `dg launch`:

| Feature            | Legacy              | Modern              |
| ------------------ | ------------------- | ------------------- |
| Single asset       | `-a my_asset`       | `--assets my_asset` |
| Multiple assets    | `-a a1 -a a2`       | `--assets a1,a2`    |
| Selection patterns | `--select "tag:x"`  | `--assets "tag:x"`  |
| Partitions         | `--partition`       | `--partition`       |
| Partition ranges   | `--partition-range` | `--partition-range` |
| Config             | `--config`          | `--config-json`     |
| Jobs               | `-j my_job`         | `--job my_job`      |

### Migration Checklist

- [ ] Replace `python -m dagster asset materialize` with `dg launch`
- [ ] Change `-a` or `--select` flags to `--assets`
- [ ] Update CI/CD scripts to use `dg launch`
- [ ] Switch from `--config` to `--config-json` (JSON format)
- [ ] Update documentation and runbooks
- [ ] Test all asset selection patterns work with new syntax
- [ ] Verify environment variable loading with `uv run` or shell sourcing

### Benefits of Migration

1. **Simpler syntax** - Fewer characters, easier to remember
2. **Better environment handling** - uv auto-loads .env files
3. **Consistent CLI** - All dg commands use same patterns
4. **Modern features** - Access latest Dagster features faster
5. **Better error messages** - Clearer validation and debugging

---

## Related Commands

- `/dg:troubleshoot` - Debug failing runs with detailed analysis
- `/dg:logs` - Retrieve and display run logs
- `/dagster-conventions` - Learn asset patterns and best practices

## See Also

- [Asset Patterns Reference](../../dagster-conventions/skills/dagster-conventions/references/assets.md)
- [Automation Patterns](../../dagster-conventions/skills/dagster-conventions/references/automation.md)
- [Dagster CLI Documentation](https://docs.dagster.io/guides/cli)
