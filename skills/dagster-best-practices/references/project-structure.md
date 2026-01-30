# Project Structure Reference

## Pattern Summary

| Pattern                      | When to Use                                               |
| ---------------------------- | --------------------------------------------------------- |
| Single code location         | Small to medium projects, single team                     |
| Multiple code locations      | Large organizations, isolated dependencies                |
| Components                   | Standardized, repeatable patterns with declarative config |
| Pythonic assets + Components | Mix custom logic with standardized integrations           |
| Organize by technology       | Team focused on specific tech stacks                      |
| Organize by concept          | Business-context clarity across organization              |
| Module-based organization    | Domain-driven project structure                           |

**Modern Recommendation**: Use `create-dagster` with auto-discovery for new projects. Combine
components with pythonic assets using `Definitions.merge()`.

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

### Modern Autoloading Pattern (Recommended)

**Simple Auto-Discovery**:

```python
# src/my_project/definitions.py
from dagster import Definitions
from dagster_dg import load_defs

# Automatically discovers all definitions in defs/ folder
defs = Definitions.merge(
    load_defs()
)
```

**Combining Components with Pythonic Assets**:

```python
# src/my_project/definitions.py
from dagster import Definitions
from dagster_dg import load_defs
from my_project.assets import custom_assets

# Load component definitions from defs/
component_defs = load_defs()

# Define pythonic assets separately
pythonic_defs = Definitions(
    assets=custom_assets,
    resources={...}
)

# Merge them together
defs = Definitions.merge(component_defs, pythonic_defs)
```

**Benefits**:

- Automatically loads all components from `defs/` directory
- Zero boilerplate when adding new components
- Clean separation between components and custom assets
- Flexible resource sharing across both patterns

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

| Use Case                      | Benefit                                    |
| ----------------------------- | ------------------------------------------ |
| Different teams               | Independent deployments, isolated failures |
| Different Python versions     | Legacy code alongside modern code          |
| Different dependency versions | PyTorch v1 vs v2, pandas versions          |
| Compliance separation         | HIPAA, PCI data isolation                  |
| Functional separation         | ETL vs ML vs BI layers                     |

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

## Configuration Files

### pyproject.toml (Python Package + dg Config)

```toml
[project]
name = "my_project"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "dagster>=1.8.0",
    "dagster-duckdb",
    "dagster-dbt",
    "dagster-sling",
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
    "dagster.components.*",      # Built-in components (dbt, Sling, etc.)
    "my_project.components.*",   # Custom components
]
```

**Key Settings**:

- `directory_type`: "project" for dg-managed projects
- `root_module`: Python module containing definitions.py
- `registry_modules`: Where to discover components

### dg.toml (Workspace Configuration)

For managing multiple Dagster projects together:

```toml
# dg.toml (at workspace root)
[workspace]
projects = [
    "etl_project",
    "ml_project",
    "analytics_project",
]
```

**Use Cases**:

- Multiple teams with separate projects
- Shared dependencies across projects
- Organization-wide development
- Conflicting dependency requirements

### dagster.yaml (Instance Configuration)

```yaml
# dagster.yaml (at project root or ~/.dagster)
run_launcher:
  module: dagster.core.launcher
  class: DefaultRunLauncher

run_storage:
  module: dagster.core.storage.runs
  class: SqliteRunStorage
  config:
    base_dir: /var/dagster/storage

event_log_storage:
  module: dagster.core.storage.event_log
  class: SqliteEventLogStorage
  config:
    base_dir: /var/dagster/storage

schedule_storage:
  module: dagster.core.storage.schedules
  class: SqliteScheduleStorage
  config:
    base_dir: /var/dagster/storage
```

**Purpose**: Configure Dagster instance behavior (storage, compute, scheduling)

**Common Uses**:

- Storage configuration (SQLite, PostgreSQL)
- Run launcher settings (local, K8s, etc.)
- Compute log storage
- Scheduler configuration

---

## Components

**What are Components?** Reusable, declarative building blocks that generate `Definitions` from
configuration (YAML). Components standardize repetitive patterns and integrations without writing
Python code.

### When to Use Components

| Use Case                   | Example                                 |
| -------------------------- | --------------------------------------- |
| Standardized ETL patterns  | Multiple similar Sling replication jobs |
| External tool integration  | dbt, Sling, Fivetran                    |
| Repeatable patterns        | API ingestion with consistent structure |
| Non-engineer contributions | Analysts defining pipelines via config  |
| Reducing code duplication  | Same pattern repeated across teams      |

**Don't Use Components When**:

- Custom logic is complex and doesn't fit a template
- Pattern is used only once
- You need fine-grained control over execution

### Component Types

**Built-in Components** (from Dagster):

- `dagster_dbt.DbtProjectComponent`: dbt project integration
- `dagster_sling.SlingReplicationComponent`: Database replication
- Additional components for Fivetran, Airbyte, etc.

**Custom Components**: Create organization-specific patterns

### Component Structure

```
defs/
├── ingest_postgres/        # Component instance
│   ├── defs.yaml           # Component configuration
│   └── replication.yaml    # Additional config files
├── transform_dbt/
│   └── defs.yaml
└── shared_resources/       # Optional: shared resources
    └── defs.py
```

### Sling Component Example

```yaml
# defs/ingest_postgres/defs.yaml
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
# defs/ingest_postgres/replication.yaml
source: MY_POSTGRES
target: MY_DUCKDB

defaults:
  mode: full-refresh

streams:
  data.customers:
  data.products:
  data.orders:
```

### dbt Component Example

**Remote Git Repository (Recommended)**:

```yaml
# defs/transform/defs.yaml
type: dagster_dbt.DbtProjectComponent

attributes:
  project:
    repo_url: https://github.com/dagster-io/jaffle-platform.git
    repo_relative_path: jdbt
  dbt:
    target: dev
```

The remote configuration manages the dbt project as component state without requiring you to clone
the repository locally.

**For private repositories**, add token authentication:

```yaml
attributes:
  project:
    repo_url: https://github.com/your-org/dbt-project.git
    repo_relative_path: dbt
    token: "{{ env.GIT_TOKEN }}"
  dbt:
    target: dev
```

**Local Project (Alternative for Development)**:

```yaml
# defs/transform/defs.yaml
type: dagster_dbt.DbtProjectComponent

attributes:
  project:
    project_dir: ../../dbt_project
  dbt:
    target: dev
    profiles_dir: ~/.dbt
```

Use local configuration when actively developing dbt models or when the dbt project is colocated in
your Dagster repository.

### Combining Components with Pythonic Assets

```python
# src/my_project/definitions.py
from dagster import Definitions
from dagster_dg import load_defs

# Load component definitions
component_defs = load_defs()

# Define custom pythonic assets
from my_project.assets import custom_pipeline

pythonic_defs = Definitions(
    assets=[custom_pipeline],
    resources={...}
)

# Merge: components AND custom assets in one project
defs = Definitions.merge(component_defs, pythonic_defs)
```

### Component Best Practices

1. **Single Responsibility**: Each component handles one integration or pattern
2. **Typed Configuration**: Use structured YAML for validation
3. **Documentation**: Document component parameters and examples
4. **Testing**: Validate component configurations before deployment
5. **Versioning**: Pin component versions for stability
6. **Resource Sharing**: Share resources across components and pythonic assets

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

| Anti-Pattern                 | Better Approach                    |
| ---------------------------- | ---------------------------------- |
| All assets in one file       | Organize by domain/layer           |
| Hardcoded paths              | Use constants or EnvVar            |
| No definitions validation    | Run `dg check defs` in CI          |
| Mixing production/dev config | Use environment variables          |
| Monolithic code location     | Split by team/function as you grow |

---

## References

- [Project Structure](https://docs.dagster.io/guides/build/project-structure)
- [Code Locations](https://docs.dagster.io/guides/deploy/code-locations)
- [Components Guide](https://docs.dagster.io/guides/build/components)
- [dg CLI Reference](https://docs.dagster.io/api/clis/dg-cli/dg-cli-reference)
