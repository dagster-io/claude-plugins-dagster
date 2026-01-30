# Dagster Best Practices Reference Documentation

This directory contains expert guidance on Dagster patterns, architectural decisions, and production-ready development practices.

## Table of Contents

### Core Concepts
- **[assets.md](./assets.md)** - Asset design patterns and best practices
  - Basic asset patterns
  - Dependencies and lineage
  - Partitioned assets
  - Multi-assets
  - Asset organization (groups, metadata)
  - Asset testing

### Automation
- **[automation.md](./automation.md)** - Automation strategies and patterns
  - Declarative Automation (recommended modern approach)
  - Schedules (time-based automation)
  - Sensors (event-driven automation)
  - Partition automation
  - Backfills and historical data processing

### Resource Management
- **[resources.md](./resources.md)** - Resource patterns and dependency injection
  - Database connections
  - API clients
  - Environment configuration with EnvVar
  - Resource dependencies
  - Testing with mock resources

### Testing
- **[testing.md](./testing.md)** - Testing strategies for Dagster projects
  - Unit testing assets
  - Integration tests
  - Asset checks (data quality)
  - Testing with resources
  - Test fixtures and helpers

### ETL Patterns
- **[etl-patterns.md](./etl-patterns.md)** - ETL/ELT patterns and integration guidance
  - dbt integration patterns
  - dlt pipeline patterns
  - Sling replication patterns
  - Extract-Load-Transform (ELT)
  - Data quality and validation

### Project Organization
- **[project-structure.md](./project-structure.md)** - Project structure and organization
  - Single project layout
  - Workspace (multi-project) structure
  - Components vs definitions
  - Code locations
  - Directory conventions

## Quick Reference

### Core Philosophy

**Think in Assets**: Dagster is built around the asset abstraction—persistent objects like tables, files, or models that your pipeline produces.

- **Clear Lineage**: Explicit dependencies define data flow
- **Better Observability**: Track what data exists and how it was created
- **Improved Testability**: Assets are just Python functions
- **Declarative Pipelines**: Focus on _what_ to produce, not _how_ to execute

**Assets over Ops**: For most data pipelines, prefer assets over ops. Use ops only when the asset abstraction doesn't fit (non-data workflows, complex execution patterns).

**Environment Separation**: Use resources and `EnvVar` to maintain separate configurations for dev, staging, and production without code changes.

### Common Patterns

```python
# Basic asset
@dg.asset
def my_asset() -> None:
    """Asset description appears in the UI."""
    pass

# Asset with dependencies
@dg.asset(deps=[upstream_asset])
def downstream_asset():
    pass

# Asset with resource
@dg.asset
def database_asset(database: DatabaseResource):
    database.execute("SELECT ...")

# Partitioned asset
@dg.asset(partitions_def=DailyPartitionsDefinition(start_date="2024-01-01"))
def daily_data(context: AssetExecutionContext):
    partition_date = context.partition_key
    # Process data for partition_date

# Multi-asset
@dg.multi_asset(
    outs={
        "asset_a": AssetOut(),
        "asset_b": AssetOut(),
    }
)
def compute_multiple_assets():
    return value_a, value_b
```

### Automation Strategies

**Modern (Recommended): Declarative Automation**
```python
@dg.asset(
    automation_condition=AutomationCondition.on_cron("0 0 * * *")
)
def daily_asset():
    pass
```

**Traditional: Schedules**
```python
daily_job = dg.define_asset_job("daily_job", selection="tag:schedule=daily")

daily_schedule = dg.ScheduleDefinition(
    job=daily_job,
    cron_schedule="0 0 * * *"
)
```

**Event-Driven: Sensors**
```python
@dg.sensor(job_name="my_job")
def file_watcher_sensor(context):
    if new_file_exists():
        return RunRequest(...)
```

### Resource Patterns

```python
from dagster import ConfigurableResource, EnvVar

class DatabaseResource(ConfigurableResource):
    connection_string: str = EnvVar("DATABASE_URL")
    pool_size: int = EnvVar.int("DB_POOL_SIZE")

    def execute(self, query: str):
        # Connection logic here
        pass

# In Definitions
defs = dg.Definitions(
    assets=[...],
    resources={
        "database": DatabaseResource()
    }
)
```

### Testing Patterns

```python
import pytest
from dagster import materialize

def test_my_asset():
    # Arrange
    mock_resource = MockDatabase()

    # Act
    result = materialize(
        [my_asset],
        resources={"database": mock_resource}
    )

    # Assert
    assert result.success
```

## Navigation Tips

- Start with **assets.md** to understand asset design patterns
- Check **automation.md** for choosing between schedules, sensors, and declarative automation
- Reference **resources.md** for dependency injection and environment configuration
- Use **testing.md** for test strategies and data quality checks
- Consult **etl-patterns.md** for integration-specific patterns (dbt, dlt, Sling)
- Review **project-structure.md** for organizing larger projects

## Related Skills

- **`/dg`** - Execute CLI operations (create project, scaffold, launch, list, troubleshoot)
- **`/dagster-integrations`** - Discover integration libraries and implementation patterns
- **`/dignified-python`** - Python code quality standards

## Documentation Structure

Each reference document follows a consistent structure:

1. **Overview** - High-level concepts and philosophy
2. **Quick Reference** - Common patterns and examples
3. **Detailed Patterns** - Comprehensive coverage of approaches
4. **Best Practices** - Recommended patterns and anti-patterns
5. **Advanced Topics** - Complex use cases
6. **Real-World Examples** - Production-ready code samples
7. **Related Topics** - Cross-references to other sections

## When to Use Each Reference

| Question | Reference |
|----------|-----------|
| "How do I structure my assets?" | assets.md |
| "Should I use schedules or sensors?" | automation.md |
| "How do I connect to databases?" | resources.md |
| "How do I test my pipeline?" | testing.md |
| "How do I integrate dbt?" | etl-patterns.md |
| "How should I organize my project?" | project-structure.md |

## Cross-Skill Workflow

**Learning → Implementation:**
1. Use `/dagster-best-practices` to learn patterns
2. Use `/dg` to scaffold components following those patterns
3. Use `/dagster-integrations` to discover integration libraries
4. Use `/dignified-python` for Python code quality

**Example:**
```
User: "How should I structure my dbt integration?"
→ /dagster-best-practices (learn dbt patterns in etl-patterns.md)
→ /dg scaffold defs dagster_dbt.DbtProjectComponent my_dbt
→ Edit generated code following learned patterns
→ /dg launch --assets my_dbt (test it)
```
