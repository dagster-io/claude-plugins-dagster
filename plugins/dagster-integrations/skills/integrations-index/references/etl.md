# ETL Integrations

Extract, transform, and load tools for data ingestion, transformation, and orchestration.

---

### dbt
**Package:** `dagster-dbt` | **Support:** Dagster-supported

Transform data using SQL models with automatic dependency management, incremental updates, and testing. Component-based integration.

**Use cases:**
- SQL-based data transformations in warehouses
- Build dimensional models and data marts
- Test data quality with dbt tests
- Document data lineage and schemas

**Quick start (Component-based - Recommended):**
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

**Quick start (Pythonic):**
```python
from dagster_dbt import DbtProject, dbt_assets

# For local projects
my_project = DbtProject(project_dir="path/to/dbt/project")

# Create assets from dbt models
@dbt_assets(manifest=my_project.manifest_path)
def my_dbt_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

defs = dg.Definitions(
    assets=[my_dbt_assets],
    resources={
        "dbt": DbtCliResource(project_dir=my_project)
    }
)
```

**Docs:** https://docs.dagster.io/integrations/libraries/dbt

**Key features:**
- Component-based scaffolding with remote Git repositories
- Automatic asset creation from dbt models
- Incremental model support
- dbt test integration
- Support for both remote and local projects

---

### Fivetran
**Package:** `dagster-fivetran` | **Support:** Dagster-supported

Orchestrate Fivetran connectors for automated data ingestion from 400+ SaaS applications and databases. Component-based integration.

**Use cases:**
- Replicate data from SaaS tools (Salesforce, HubSpot, etc.)
- Sync databases to data warehouses
- Automated schema change detection
- Schedule data syncs with Dagster

**Quick start:**
```python
from dagster_fivetran import FivetranResource, fivetran_assets, load_fivetran_asset_specs

fivetran = FivetranResource(
    api_key=dg.EnvVar("FIVETRAN_API_KEY"),
    api_secret=dg.EnvVar("FIVETRAN_API_SECRET")
)

# Load all Fivetran connectors as assets
fivetran_specs = load_fivetran_asset_specs(fivetran)

defs = dg.Definitions(
    assets=[*fivetran_specs],
    resources={"fivetran": fivetran}
)
```

**Docs:** https://docs.dagster.io/integrations/libraries/fivetran

**Key features:**
- Component scaffolding with `dagster-fivetran project scaffold`
- Automatic connector discovery
- Sync monitoring and error handling
- Schema change tracking

---

### Airbyte
**Package:** `dagster-airbyte` | **Support:** Dagster-supported

Manage Airbyte connections for ELT data movement from various sources to destinations with open-source or cloud deployment.

**Use cases:**
- Open-source ELT pipelines
- Custom connector development
- Sync data between databases
- Extract data from APIs

**Quick start:**
```python
from dagster_airbyte import AirbyteResource, load_airbyte_asset_specs

airbyte = AirbyteResource(
    host="localhost",
    port="8000",
    username="airbyte",
    password=dg.EnvVar("AIRBYTE_PASSWORD")
)

# Load all Airbyte connections as assets
airbyte_specs = load_airbyte_asset_specs(airbyte)

defs = dg.Definitions(
    assets=[*airbyte_specs],
    resources={"airbyte": airbyte}
)
```

**Docs:** https://docs.dagster.io/integrations/libraries/airbyte

**Key features:**
- Automatic connection asset generation
- Sync status monitoring
- Error handling and retries
- Integration with Airbyte Cloud or OSS

---

### dlt
**Package:** `dagster-dlt` | **Support:** Dagster-supported

Python-based data loading tool for building ELT pipelines with schema evolution and data contracts. Component-based integration.

**Use cases:**
- Python-based data ingestion pipelines
- API data extraction with automatic schema inference
- Load data from custom sources
- Incremental loading with state management

**Quick start:**
```python
from dagster_dlt import DltResource, dlt_assets
import dlt

# Define dlt pipeline
@dlt.source
def my_source():
    @dlt.resource
    def my_data():
        yield [{"id": 1, "value": "a"}, {"id": 2, "value": "b"}]
    return my_data

# Create Dagster assets from dlt pipeline
@dlt_assets(
    dlt_source=my_source(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="my_pipeline",
        destination="duckdb",
        dataset_name="my_dataset"
    )
)
def my_dlt_assets(context: dg.AssetExecutionContext, dlt: DltResource):
    yield from dlt.run(context=context)

defs = dg.Definitions(
    assets=[my_dlt_assets],
    resources={"dlt": DltResource()}
)
```

**Docs:** https://docs.dagster.io/integrations/libraries/dlt

**Key features:**
- Component scaffolding with `dagster-dlt project scaffold`
- Automatic schema evolution
- State management for incremental loads
- Data validation and contracts

---

### Sling
**Package:** `dagster-sling` | **Support:** Dagster-supported

High-performance data replication tool for moving data between databases, data warehouses, and file systems. Component-based integration.

**Use cases:**
- Fast database-to-database replication
- Bulk data transfers
- File-to-database ingestion
- Cross-platform data movement

**Quick start:**
```python
from dagster_sling import SlingResource, sling_assets

# Define Sling replication config
replication_config = {
    "source": "POSTGRES",
    "target": "SNOWFLAKE",
    "streams": {
        "public.users": {
            "mode": "full-refresh",
            "object": "analytics.users"
        }
    }
}

@sling_assets(replication_config=replication_config)
def my_sling_assets(context: dg.AssetExecutionContext, sling: SlingResource):
    yield from sling.replicate(context=context)

defs = dg.Definitions(
    assets=[my_sling_assets],
    resources={
        "sling": SlingResource(
            connections=[
                {"name": "POSTGRES", "type": "postgres", ...},
                {"name": "SNOWFLAKE", "type": "snowflake", ...}
            ]
        )
    }
)
```

**Docs:** https://docs.dagster.io/integrations/libraries/sling

**Key features:**
- Component scaffolding with `dagster-sling project scaffold`
- High-performance bulk transfers
- Multiple source/destination support
- Incremental and full-refresh modes

---

### Meltano
**Package:** `dagster-meltano` | **Support:** Community-supported

ELT platform built on Singer taps and targets for the modern data stack.

**Use cases:**
- Singer tap orchestration
- Configuration-based ELT pipelines
- Open-source data integration
- Custom tap/target development

**Quick start:**
```python
from dagster_meltano import meltano_resource, meltano_run_op

meltano = meltano_resource.configured({
    "project_dir": "path/to/meltano/project"
})

@dg.op(required_resource_keys={"meltano"})
def run_meltano_pipeline(context):
    context.resources.meltano.run(
        "run", "tap-github", "target-postgres"
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/meltano

---

### Embedded ELT
**Package:** `dagster-embedded-elt` | **Support:** Dagster-supported

Framework for building embedded ELT pipelines with Sling directly in Python without external orchestration.

**Use cases:**
- Lightweight ELT without additional tools
- Python-based data replication
- Simple database sync jobs
- Embedded in existing Dagster pipelines

**Quick start:**
```python
from dagster_embedded_elt.sling import SlingResource, build_sling_asset

sling = SlingResource(
    connections=[
        {"name": "MY_POSTGRES", "type": "postgres", ...},
        {"name": "MY_DUCKDB", "type": "duckdb", ...}
    ]
)

asset_def = build_sling_asset(
    asset_spec=dg.AssetSpec(key="my_table"),
    source_stream="MY_POSTGRES.public.users",
    target_object="MY_DUCKDB.main.users",
    mode="full-refresh"
)

defs = dg.Definitions(
    assets=[asset_def],
    resources={"sling": sling}
)
```

**Docs:** https://docs.dagster.io/integrations/libraries/embedded-elt

---

### SFTP
**Package:** `dagster-sftp` | **Support:** Community-supported

Secure file transfer protocol integration for moving files between SFTP servers.

**Use cases:**
- Download files from SFTP servers
- Upload processed data to SFTP
- Integrate with legacy systems using SFTP
- Secure file transfers

**Quick start:**
```python
from dagster_sftp import SFTPResource

sftp = SFTPResource(
    host="sftp.example.com",
    username=dg.EnvVar("SFTP_USER"),
    password=dg.EnvVar("SFTP_PASSWORD")
)

@dg.asset
def sftp_file(sftp: SFTPResource):
    with sftp.get_connection() as client:
        client.get("/remote/file.csv", "/local/file.csv")
    return pd.read_csv("/local/file.csv")
```

**Docs:** https://docs.dagster.io/integrations/libraries/sftp

---

### PySpark
**Package:** `dagster-pyspark` | **Support:** Dagster-supported

Python API for Apache Spark enabling distributed data processing and transformation on large datasets across clusters.

**Use cases:**
- Process datasets too large for memory
- Distributed ETL transformations across clusters
- Large-scale data aggregations and joins
- Transform data at petabyte scale

**Quick start:**
```python
from dagster_pyspark import PySparkResource
from pyspark.sql import DataFrame

pyspark = PySparkResource(
    spark_config={
        "spark.executor.memory": "4g",
        "spark.executor.cores": "2"
    }
)

@dg.asset
def transform_large_dataset(pyspark: PySparkResource) -> DataFrame:
    spark = pyspark.spark_session
    df = spark.read.parquet("s3://bucket/large-dataset")
    return df.groupBy("category").agg({"amount": "sum"})
```

**Docs:** https://docs.dagster.io/integrations/libraries/pyspark

---

## ETL Tool Selection Guide

| Tool | Best For | Architecture | Complexity |
|------|----------|--------------|------------|
| **dbt** | SQL transformations | Transform-only | Medium |
| **Fivetran** | SaaS connectors (managed) | ELT (SaaS) | Low |
| **Airbyte** | Open-source ELT | ELT (OSS/SaaS) | Medium |
| **dlt** | Python-based extraction | EL (Python) | Medium |
| **Sling** | High-speed replication | EL (CLI) | Low |
| **Meltano** | Singer taps | ELT (OSS) | High |
| **PySpark** | Distributed ETL | Transformation | High |

## Component-Based Integration Pattern

Many ETL tools use Dagster's component-based pattern:

```bash
# 1. Scaffold the project
dagster-<tool> project scaffold --project-name my_project

# 2. Components auto-generate assets
# Project structure with YAML config
my_project/
  ├── components.yaml          # Defines component instances
  ├── lib/
  │   └── components/
  │       └── <tool>/
  │           └── config.yaml  # Tool-specific config
```

```python
# 3. Load in Dagster code
from dagster import Definitions
from my_project import defs as project_defs

defs = project_defs
```

## Tips

- **dbt**: Use `dbt_assets` for automatic asset generation from models
- **Fivetran/Airbyte**: Component scaffold auto-discovers connectors
- **dlt**: Great for custom API ingestion with automatic schema
- **Sling**: Fastest for bulk database transfers
- **PySpark**: Use for transformations too large for pandas/polars
- **Incremental**: Most tools support incremental loading for efficiency
