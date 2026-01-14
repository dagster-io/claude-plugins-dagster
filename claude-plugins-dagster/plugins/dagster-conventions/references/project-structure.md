# Project Structure Reference

## Pattern Summary

| Pattern | When to Use |
| ------- | ----------- |
| Single code location | Small to medium projects, single team |
| Multiple code locations | Large organizations, isolated dependencies |
| Components | Reusable integrations, declarative config |
| Module-based organization | Domain-driven project structure |

---

## Recommended Project Layout

### Standard Layout

```
my_project/
├── pyproject.toml              # Dependencies and dg config
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── definitions.py      # Main Definitions entry point
│       └── defs/
│           ├── __init__.py
│           ├── assets/
│           │   ├── __init__.py
│           │   ├── constants.py
│           │   ├── ingestion.py
│           │   └── analytics.py
│           ├── jobs.py
│           ├── schedules.py
│           ├── sensors.py
│           ├── partitions.py
│           └── resources.py
├── data/
│   ├── source/
│   ├── staging/
│   └── outputs/
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_assets.py
```

### With Components

```
my_project/
├── pyproject.toml
├── src/
│   └── my_project/
│       ├── definitions.py
│       └── defs/
│           ├── dashboard/          # Component: Looker integration
│           │   └── defs.yaml
│           ├── ingest_files/       # Component: Sling replication
│           │   ├── defs.yaml
│           │   └── replication.yaml
│           └── transform/          # Component: dbt project
│               └── defs.yaml
└── tests/
```

---

## Definitions Object

The `Definitions` object is the entry point for all Dagster objects.

### Modern Autoloading Pattern

```python
# src/my_project/definitions.py
from pathlib import Path
from dagster import definitions, load_from_defs_folder

@definitions
def defs():
    return load_from_defs_folder(project_root=Path(__file__).parent.parent.parent)
```

This pattern:
- Automatically loads all assets, jobs, schedules from `defs/`
- Uses `@definitions` decorator for discoverability
- Requires proper file placement in `defs/` directory

### Explicit Definitions Pattern

```python
# src/my_project/definitions.py
import dagster as dg

from my_project.defs.assets import ingestion, analytics
from my_project.defs.jobs import daily_job, weekly_job
from my_project.defs.schedules import daily_schedule
from my_project.defs.resources import database_resource

defs = dg.Definitions(
    assets=[
        *ingestion.assets,
        *analytics.assets,
    ],
    jobs=[daily_job, weekly_job],
    schedules=[daily_schedule],
    resources={"database": database_resource},
)
```

### Resource Definitions Pattern

```python
# src/my_project/defs/resources.py
import dagster as dg
from dagster_duckdb import DuckDBResource

database_resource = DuckDBResource(
    database=dg.EnvVar("DUCKDB_DATABASE")
)

@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "database": database_resource,
        }
    )
```

---

## Code Locations

### What is a Code Location?

A code location is:
1. A Python module containing a `Definitions` object
2. A Python environment that can load that module

### When to Use Multiple Code Locations

| Use Case | Benefit |
| -------- | ------- |
| Different teams | Independent deployments, isolated failures |
| Different Python versions | Legacy code alongside modern code |
| Different dependency versions | PyTorch v1 vs v2, pandas versions |
| Compliance separation | HIPAA, PCI data isolation |
| Functional separation | ETL vs ML vs BI layers |

### Code Location Configuration

```yaml
# workspace.yaml
load_from:
  - python_module: my_project.definitions
  - python_module: ml_project.definitions
  - python_module: etl_project.definitions
```

### Benefits of Code Locations

- **Isolation**: Failures in one location don't affect others
- **Independent deployment**: Teams deploy without coordination
- **Dependency flexibility**: Different packages per location
- **Single pane of glass**: All assets visible in one UI
- **Cross-location dependencies**: Assets can depend across locations

---

## dg CLI Scaffolding

### Create New Project

```bash
uvx create-dagster my_project
cd my_project
```

This creates:
- Virtual environment with uv
- Standard project layout
- pyproject.toml with Dagster dependencies
- definitions.py with autoloading

### Scaffold Dagster Objects

```bash
# Scaffold asset file
dg scaffold defs dagster.asset assets/new_asset.py

# Scaffold job
dg scaffold defs dagster.job jobs.py

# Scaffold schedule
dg scaffold defs dagster.schedule schedules.py

# Scaffold sensor
dg scaffold defs dagster.sensor sensors.py

# Scaffold resources
dg scaffold defs dagster.resources resources.py
```

### Validate Definitions

```bash
dg check defs
# Output: All components validated successfully.
# Output: All definitions loaded successfully.
```

### Development Server

```bash
dg dev
# Starts Dagster UI at http://localhost:3000
```

---

## pyproject.toml Configuration

### Basic Configuration

```toml
[project]
name = "my_project"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "dagster>=1.8.0",
    "dagster-duckdb",
]

[project.optional-dependencies]
dev = [
    "dagster-webserver",
    "pytest",
]

[tool.dg]
directory_type = "project"

[tool.dg.project]
root_module = "my_project"
registry_modules = [
    "my_project.components.*",
]
```

### With Components

```toml
[tool.dg]
directory_type = "project"

[tool.dg.project]
root_module = "my_project"
registry_modules = [
    "dagster.components.*",      # Built-in components
    "my_project.components.*",   # Custom components
]
```

---

## Components

Components are reusable, declarative building blocks for integrations.

### Component Structure

```
my_component/
├── defs.yaml       # Component configuration
└── (optional files)
```

### Sling Component Example

```yaml
# defs/ingest_files/defs.yaml
component: dagster_sling.SlingReplicationComponent

params:
  replication_config: replication.yaml
  sling:
    connections:
      - name: MY_POSTGRES
        type: postgres
        host: localhost
        port: 5432
        database: source_db
      - name: MY_DUCKDB
        type: duckdb
        connection_string: "duckdb:///data/staging/data.duckdb"
```

```yaml
# defs/ingest_files/replication.yaml
source: MY_POSTGRES
target: MY_DUCKDB

defaults:
  mode: full-refresh

streams:
  data.customers:
  data.products:
  data.orders:
```

### Component Best Practices

1. **Isolation**: Each component is self-contained
2. **Typed config**: Use config models for clear interfaces
3. **Composability**: Small, focused components that combine
4. **Versioning**: Track component changes
5. **Testing**: Validate components independently

---

## Module Organization

### Domain-Based Organization

```
defs/
├── assets/
│   ├── ingestion/      # Raw data ingestion
│   │   ├── __init__.py
│   │   ├── files.py
│   │   └── apis.py
│   ├── staging/        # Data cleaning
│   │   ├── __init__.py
│   │   └── transformations.py
│   └── analytics/      # Business metrics
│       ├── __init__.py
│       └── reports.py
├── jobs.py
├── schedules.py
└── resources.py
```

### Layer-Based Organization

```
defs/
├── bronze/            # Raw data layer
│   ├── __init__.py
│   └── ingestion.py
├── silver/            # Cleaned data layer
│   ├── __init__.py
│   └── cleaning.py
├── gold/              # Business layer
│   ├── __init__.py
│   └── metrics.py
└── automation/
    ├── jobs.py
    ├── schedules.py
    └── sensors.py
```

---

## Environment Configuration

### Environment Variables

```bash
# .env (not committed to git)
DUCKDB_DATABASE=data/staging/data.duckdb
SNOWFLAKE_ACCOUNT=myaccount
SNOWFLAKE_USER=myuser
SNOWFLAKE_PASSWORD=secret
```

### Loading in Dagster

```python
import dagster as dg

resource = MyResource(
    database=dg.EnvVar("DUCKDB_DATABASE"),
    api_key=dg.EnvVar("API_KEY"),
)
```

### Environment-Specific Config

```python
import os

if os.getenv("DAGSTER_ENV") == "production":
    database_path = "/data/prod/data.duckdb"
else:
    database_path = "data/staging/data.duckdb"
```

---

## Reloading Definitions

### When to Reload

Reload definitions when:
- Adding new assets, jobs, schedules, or sensors
- Modifying decorator arguments (`@dg.asset(...)`)
- Changing Definitions object

**Not required** when:
- Editing asset function logic (with `-e` install)
- Updating SQL queries inside assets
- Changing resource method implementations

### How to Reload

**UI**: Click "Reload Definitions" button

**CLI**:
```bash
dagster dev  # Restart for full reload
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Better Approach |
| ------------ | --------------- |
| All assets in one file | Organize by domain/layer |
| Hardcoded paths | Use constants or EnvVar |
| No definitions validation | Run `dg check defs` in CI |
| Mixing production/dev config | Use environment variables |
| Monolithic code location | Split by team/function as you grow |

---

## References

- [Project Structure](https://docs.dagster.io/guides/build/project-structure)
- [Code Locations](https://docs.dagster.io/guides/deploy/code-locations)
- [Components Guide](https://docs.dagster.io/guides/build/components)
- [dg CLI Reference](https://docs.dagster.io/api/clis/dg-cli/dg-cli-reference)

