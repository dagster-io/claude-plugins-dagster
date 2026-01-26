---
name: integrations-index
description: Comprehensive index of 82+ Dagster integrations organized by official tags.yml taxonomy including AI (OpenAI, Anthropic), ETL (dbt, Fivetran, Airbyte, PySpark), Storage (Snowflake, BigQuery), Compute (AWS, Databricks, Spark), BI (Looker, Tableau), Monitoring, Alerting, and Testing. Use when discovering integrations or finding the right tool for a use case.
---

# Dagster Integrations Index

Navigate 82+ Dagster integrations organized by Dagster's official taxonomy. Find AI/ML tools, ETL platforms, data storage, compute services, BI tools, and monitoring integrations.

## When to Use This Skill vs. Others

| If User Says... | Use This Skill/Command | Why |
|----------------|------------------------|-----|
| "which integration for X" | `/dagster-integrations` | Need to discover appropriate integration |
| "does dagster support X" | `/dagster-integrations` | Check integration availability |
| "snowflake vs bigquery" | `/dagster-integrations` | Compare integrations in same category |
| "best practices for X" | `/dagster-conventions` | Implementation patterns needed |
| "implement X integration" | `/dg:prototype` | Ready to build with specific integration |
| "how do I use dbt" | `/dagster-conventions` (dbt section) | dbt-specific implementation patterns |
| "make this code better" | `/dignified-python` | Python code review needed |
| "create new project" | `/dg:create-project` | Project initialization needed |

## Quick Reference by Category

| Category | Count | Common Tools | Reference |
|----------|-------|--------------|-----------|
| **AI & ML** | 6 | OpenAI, Anthropic, MLflow, W&B | `references/ai.md` |
| **ETL/ELT** | 9 | dbt, Fivetran, Airbyte, PySpark | `references/etl.md` |
| **Storage** | 35+ | Snowflake, BigQuery, Postgres, DuckDB | `references/storage.md` |
| **Compute** | 15+ | AWS, Databricks, Spark, Docker, K8s | `references/compute.md` |
| **BI & Visualization** | 7 | Looker, Tableau, PowerBI, Sigma | `references/bi.md` |
| **Monitoring** | 3 | Datadog, Prometheus, Papertrail | `references/monitoring.md` |
| **Alerting** | 6 | Slack, PagerDuty, MS Teams, Twilio | `references/alerting.md` |
| **Testing** | 2 | Great Expectations, Pandera | `references/testing.md` |
| **Other** | 2+ | Pandas, Polars | `references/other.md` |

## Category Taxonomy

This index aligns with Dagster's official documentation taxonomy from tags.yml:

- **ai**: Artificial intelligence and machine learning integrations (LLM APIs, experiment tracking)
- **etl**: Extract, transform, and load tools including data replication and transformation frameworks
- **storage**: Databases, data warehouses, object storage, and table formats
- **compute**: Cloud platforms, container orchestration, and distributed processing frameworks
- **bi**: Business intelligence and visualization platforms
- **monitoring**: Observability platforms and metrics systems for tracking performance
- **alerting**: Notification and incident management systems for pipeline alerts
- **testing**: Data quality validation and testing frameworks
- **other**: Miscellaneous integrations including DataFrame libraries

**Note**: Support levels (dagster-supported, community-supported) are shown inline in each integration entry.

Last verified: 2026-01-14

## Top 10 Most Popular Integrations

### 1. dbt
Transform data using SQL models with automatic dependency management and incremental updates.
- **Package**: `dagster-dbt`
- **Docs**: https://docs.dagster.io/integrations/libraries/dbt

### 2. Snowflake
Cloud data warehouse for analytics with IO managers for pandas, polars, and pyspark DataFrames.
- **Package**: `dagster-snowflake`
- **Docs**: https://docs.dagster.io/integrations/libraries/snowflake

### 3. AWS
Comprehensive AWS services including S3, Athena, Glue, ECS, EMR, and more.
- **Package**: `dagster-aws`
- **Docs**: https://docs.dagster.io/integrations/libraries/aws

### 4. Databricks
Unified analytics platform with PipesDatabricksClient for running code on Databricks clusters.
- **Package**: `dagster-databricks`
- **Docs**: https://docs.dagster.io/integrations/libraries/databricks

### 5. Slack
Send notifications and alerts to Slack channels for pipeline monitoring.
- **Package**: `dagster-slack`
- **Docs**: https://docs.dagster.io/integrations/libraries/slack

### 6. Fivetran
Orchestrate Fivetran connectors for automated data ingestion from SaaS applications.
- **Package**: `dagster-fivetran`
- **Docs**: https://docs.dagster.io/integrations/libraries/fivetran

### 7. OpenAI
Integrate OpenAI API for LLM-powered data processing and AI workflows.
- **Package**: `dagster-openai`
- **Docs**: https://docs.dagster.io/integrations/libraries/openai

### 8. Airbyte
Manage Airbyte connections for ELT data movement from various sources.
- **Package**: `dagster-airbyte`
- **Docs**: https://docs.dagster.io/integrations/libraries/airbyte

### 9. Great Expectations
Validate data quality with test suites and expectations.
- **Package**: `dagster-ge`
- **Docs**: https://docs.dagster.io/integrations/libraries/great-expectations

### 10. PySpark
Run distributed data processing jobs using Apache Spark.
- **Package**: `dagster-pyspark`
- **Docs**: https://docs.dagster.io/integrations/libraries/pyspark

## Finding the Right Integration

### I need to...

**Load data from external sources**
- SaaS applications → [ETL](#etl) (Fivetran, Airbyte)
- Files/databases → [ETL](#etl) (dlt, Sling, Meltano)
- Cloud storage → [Storage](#storage) (S3, GCS, Azure Blob)

**Transform data**
- SQL transformations → [ETL](#etl) (dbt)
- Distributed transformations → [ETL](#etl) (PySpark)
- DataFrame operations → [Other](#other) (Pandas, Polars)
- Large-scale processing → [Compute](#compute) (Spark, Dask, Ray)

**Store data**
- Cloud data warehouse → [Storage](#storage) (Snowflake, BigQuery, Redshift)
- Relational database → [Storage](#storage) (Postgres, MySQL)
- File/object storage → [Storage](#storage) (S3, GCS, Azure, LakeFS)
- Analytics database → [Storage](#storage) (DuckDB)
- Vector embeddings → [Storage](#storage) (Weaviate, Chroma, Qdrant)

**Validate data quality**
- Schema validation → [Testing](#testing) (Pandera)
- Quality checks → [Testing](#testing) (Great Expectations)

**Run ML workloads**
- LLM integration → [AI](#ai) (OpenAI, Anthropic, Gemini)
- Experiment tracking → [AI](#ai) (MLflow, W&B)
- Distributed training → [Compute](#compute) (Ray, Spark)

**Execute computation**
- Cloud compute → [Compute](#compute) (AWS, Azure, GCP, Databricks)
- Containers → [Compute](#compute) (Docker, Kubernetes)
- Distributed processing → [Compute](#compute) (Spark, Dask, Ray)

**Monitor pipelines**
- Team notifications → [Alerting](#alerting) (Slack, MS Teams, PagerDuty)
- Metrics tracking → [Monitoring](#monitoring) (Datadog, Prometheus)
- Log aggregation → [Monitoring](#monitoring) (Papertrail)

**Visualize data**
- BI dashboards → [BI](#bi) (Looker, Tableau, PowerBI)
- Analytics platform → [BI](#bi) (Sigma, Hex, Evidence)

## Integration Categories

### AI & ML

Artificial intelligence and machine learning platforms, including LLM APIs and experiment tracking.

**Key integrations:**
- **OpenAI** - GPT models and embeddings API
- **Anthropic** - Claude AI models
- **Gemini** - Google's multimodal AI
- **MLflow** - Experiment tracking and model registry
- **Weights & Biases** - ML experiment tracking
- **NotDiamond** - LLM routing and optimization

See `references/ai.md` for all AI/ML integrations.

### ETL/ELT

Extract, transform, and load tools for data ingestion, transformation, and replication.

**Key integrations:**
- **dbt** - SQL-based transformation with automatic dependencies
- **Fivetran** - Automated SaaS data ingestion (component-based)
- **Airbyte** - Open-source ELT platform
- **dlt** - Python-based data loading (component-based)
- **Sling** - High-performance data replication (component-based)
- **PySpark** - Distributed data transformation
- **Meltano** - ELT for the modern data stack

See `references/etl.md` for all ETL/ELT integrations.

### Storage

Data warehouses, databases, object storage, vector databases, and table formats.

**Key integrations:**
- **Snowflake** - Cloud data warehouse with IO managers
- **BigQuery** - Google's serverless data warehouse
- **DuckDB** - In-process SQL analytics
- **Postgres** - Open-source relational database
- **Weaviate** - Vector database for AI search
- **Delta Lake** - ACID transactions for data lakes
- **DataHub** - Metadata catalog and lineage

See `references/storage.md` for all storage integrations.

### Compute

Cloud platforms, container orchestration, and distributed processing frameworks.

**Key integrations:**
- **AWS** - Cloud compute services (Glue, EMR, Lambda)
- **Databricks** - Unified analytics platform
- **GCP** - Google Cloud compute (Dataproc, Cloud Run)
- **Spark** - Distributed data processing engine
- **Dask** - Parallel computing framework
- **Docker** - Container execution with Pipes
- **Kubernetes** - Cloud-native orchestration
- **Ray** - Distributed computing for ML

See `references/compute.md` for all compute integrations.

### BI & Visualization

Business intelligence and visualization platforms for analytics and reporting.

**Key integrations:**
- **Looker** - Google's BI platform
- **Tableau** - Interactive dashboards
- **PowerBI** - Microsoft's BI tool
- **Sigma** - Cloud analytics platform
- **Hex** - Collaborative notebooks
- **Evidence** - Markdown-based BI
- **Cube** - Semantic layer platform

See `references/bi.md` for all BI integrations.

### Monitoring

Observability platforms and metrics systems for tracking pipeline performance.

**Key integrations:**
- **Datadog** - Comprehensive observability platform
- **Prometheus** - Time-series metrics collection
- **Papertrail** - Centralized log management

See `references/monitoring.md` for all monitoring integrations.

### Alerting

Notification and incident management systems for pipeline alerts.

**Key integrations:**
- **Slack** - Team messaging and alerts
- **PagerDuty** - Incident management for on-call
- **MS Teams** - Microsoft Teams notifications
- **Twilio** - SMS and voice notifications
- **Apprise** - Universal notification platform
- **DingTalk** - Team communication for Asian markets

See `references/alerting.md` for all alerting integrations.

### Testing

Data quality validation and testing frameworks for ensuring data reliability.

**Key integrations:**
- **Great Expectations** - Data validation with expectations
- **Pandera** - Statistical data validation for DataFrames

See `references/testing.md` for all testing integrations.

### Other

Miscellaneous integrations including DataFrame libraries and utility tools.

**Key integrations:**
- **Pandas** - In-memory DataFrame library
- **Polars** - Fast DataFrame library with columnar storage

See `references/other.md` for other integrations.

## References

Integration details are organized in the following files:

- **AI & ML**: `references/ai.md` - AI and ML platforms, LLM APIs, experiment tracking
- **ETL/ELT**: `references/etl.md` - Data ingestion, transformation, and replication tools
- **Storage**: `references/storage.md` - Warehouses, databases, object storage, vector DBs
- **Compute**: `references/compute.md` - Cloud platforms, containers, distributed processing
- **BI & Visualization**: `references/bi.md` - Business intelligence and analytics platforms
- **Monitoring**: `references/monitoring.md` - Observability and metrics systems
- **Alerting**: `references/alerting.md` - Notifications and incident management
- **Testing**: `references/testing.md` - Data quality and validation frameworks
- **Other**: `references/other.md` - DataFrame libraries and miscellaneous tools

## Using Integrations

Most Dagster integrations follow a common pattern:

1. **Install the package**:
   ```bash
   pip install dagster-<integration>
   ```

2. **Import and configure a resource**:
   ```python
   from dagster_<integration> import <Integration>Resource

   resource = <Integration>Resource(
       config_param=dg.EnvVar("ENV_VAR")
   )
   ```

3. **Use in your assets**:
   ```python
   @dg.asset
   def my_asset(integration: <Integration>Resource):
       # Use the integration
       pass
   ```

For component-based integrations (dbt, Fivetran, dlt, Sling), see the specific reference files for scaffolding and configuration patterns.
