# Dagster Integrations Reference Documentation

This directory contains a comprehensive catalog of 82+ Dagster integrations organized by category.

## Table of Contents

### Integration Categories

- **[ai.md](./ai.md)** - AI & ML platforms (6 integrations)
  - LLM APIs: OpenAI, Anthropic, Gemini
  - Experiment tracking: MLflow, W&B
  - LLM routing: NotDiamond

- **[etl.md](./etl.md)** - ETL/ELT tools (9 integrations)
  - Transformation: dbt, PySpark
  - Replication: Fivetran, Airbyte, Sling, Meltano
  - Data loading: dlt
  - Automation: Prefect

- **[storage.md](./storage.md)** - Data storage (35+ integrations)
  - Cloud warehouses: Snowflake, BigQuery, Redshift
  - Databases: Postgres, MySQL, MongoDB, DuckDB
  - Object storage: S3, GCS, Azure Blob, LakeFS
  - Vector databases: Weaviate, Chroma, Qdrant, Pinecone
  - Table formats: Delta Lake, Iceberg, Hudi

- **[compute.md](./compute.md)** - Compute platforms (15+ integrations)
  - Cloud: AWS, Azure, GCP, Databricks
  - Containers: Docker, Kubernetes
  - Distributed: Spark, Dask, Ray
  - Workflow: Celery, Dagster Cloud

- **[bi.md](./bi.md)** - BI & Visualization (7 integrations)
  - Traditional BI: Looker, Tableau, PowerBI, Mode
  - Modern analytics: Sigma, Hex, Evidence

- **[monitoring.md](./monitoring.md)** - Monitoring & Observability (3 integrations)
  - Metrics: Datadog, Prometheus
  - Logs: Papertrail

- **[alerting.md](./alerting.md)** - Alerting & Notifications (6 integrations)
  - Chat: Slack, MS Teams, Discord
  - Incident: PagerDuty, Opsgenie
  - SMS: Twilio

- **[testing.md](./testing.md)** - Data Quality & Testing (2 integrations)
  - Quality checks: Great Expectations
  - Schema validation: Pandera

- **[other.md](./other.md)** - Miscellaneous (2+ integrations)
  - DataFrame libraries: Pandas, Polars

## Quick Reference by Category

| Category | Count | Common Tools | Use When |
|----------|-------|--------------|----------|
| **AI & ML** | 6 | OpenAI, Anthropic, MLflow | LLM integration, experiment tracking |
| **ETL/ELT** | 9 | dbt, Fivetran, Airbyte, dlt | Data ingestion, transformation |
| **Storage** | 35+ | Snowflake, BigQuery, Postgres | Data warehousing, databases |
| **Compute** | 15+ | AWS, Databricks, Spark | Cloud compute, distributed processing |
| **BI** | 7 | Looker, Tableau, PowerBI | Data visualization, dashboards |
| **Monitoring** | 3 | Datadog, Prometheus | Metrics, observability |
| **Alerting** | 6 | Slack, PagerDuty, MS Teams | Notifications, incident management |
| **Testing** | 2 | Great Expectations, Pandera | Data quality, validation |
| **Other** | 2+ | Pandas, Polars | DataFrame operations |

## Finding the Right Integration

### By Use Case

**Data Ingestion:**
- SaaS → Fivetran, Airbyte (etl.md)
- Databases → dlt, Sling (etl.md)
- APIs → Custom Python with Pandas (other.md)

**Data Transformation:**
- SQL → dbt (etl.md)
- Distributed → PySpark (etl.md)
- Local → Pandas, Polars (other.md)

**Data Storage:**
- Cloud warehouse → Snowflake, BigQuery, Redshift (storage.md)
- OLTP database → Postgres, MySQL (storage.md)
- Object storage → S3, GCS, Azure (storage.md)
- Analytics → DuckDB (storage.md)

**ML/AI:**
- LLMs → OpenAI, Anthropic (ai.md)
- Experiment tracking → MLflow, W&B (ai.md)
- Vector search → Weaviate, Chroma (storage.md)

**Orchestration:**
- Cloud → Databricks, AWS Batch (compute.md)
- Containers → Kubernetes, Docker (compute.md)
- Distributed → Spark, Dask, Ray (compute.md)

**Observability:**
- Alerts → Slack, PagerDuty (alerting.md)
- Metrics → Datadog, Prometheus (monitoring.md)
- Data quality → Great Expectations, Pandera (testing.md)

**Visualization:**
- Traditional BI → Looker, Tableau, PowerBI (bi.md)
- Modern analytics → Sigma, Hex (bi.md)

## Integration Support Levels

Integrations are marked with support levels:

- **dagster-supported**: Officially supported by Dagster Labs
- **community-supported**: Maintained by community contributors

Check each integration entry for its support level.

## Using Integrations

### Discovery Workflow

```bash
# 1. Find integration in this catalog
# Check references/ files by category

# 2. List available components
dg list components --package <integration-name>

# 3. Scaffold integration
dg scaffold defs <component-type> <name>

# 4. Configure environment
# Add required env vars to .env

# 5. Verify integration loads
dg list defs

# 6. Test execution
dg launch --assets <name>
```

### Example: Adding dbt Integration

```bash
# 1. Discover in etl.md → find dagster_dbt

# 2. List dbt components
dg list components --package dagster_dbt

# 3. Scaffold dbt integration
dg scaffold defs dagster_dbt.DbtProjectComponent dbt_project --json-params '{
  "project_dir": "./dbt_project",
  "target": "dev"
}'

# 4. Configure (if needed)
# dbt uses profiles.yml for configuration

# 5. Verify
dg list defs

# 6. Launch
dg launch --assets dbt_project
```

## Navigation Tips

- **Start broad**: Check category summaries in SKILL.md
- **Narrow down**: Open specific category reference (e.g., etl.md)
- **Compare options**: Each reference lists multiple tools in the category
- **Check support**: Look for "dagster-supported" vs "community-supported"
- **Scaffold**: Use `/dg` to scaffold discovered integrations

## Related Skills

- **`/dg`** - Scaffold integrations, list components, launch assets
- **`/dagster-best-practices`** - Integration patterns and best practices
- **`/dignified-python`** - Python code quality standards

## Documentation Structure

Each integration category file contains:

1. **Overview** - Category description and taxonomy
2. **Integration List** - All integrations with:
   - Name and package
   - Support level
   - Use case description
   - Key features
   - PyPI link
   - Component type (if applicable)
3. **Comparison Guide** - When to choose which tool
4. **Related Categories** - Cross-references

## Taxonomy

This catalog aligns with Dagster's official documentation taxonomy:

- **ai**: Artificial intelligence and machine learning
- **etl**: Extract, transform, and load tools
- **storage**: Databases, warehouses, object storage
- **compute**: Cloud platforms, distributed processing
- **bi**: Business intelligence and visualization
- **monitoring**: Observability and metrics
- **alerting**: Notifications and incident management
- **testing**: Data quality and validation
- **other**: Miscellaneous tools

Last verified: 2026-01-27

## Cross-Skill Workflow

**Discovery → Implementation:**
1. Use `/dagster-integrations` to find the right tool
2. Use `/dagster-best-practices` to learn patterns
3. Use `/dg` to scaffold the integration
4. Implement following learned patterns

**Example:**
```
User: "How do I load data from Salesforce?"
→ /dagster-integrations → references/etl.md → Find Fivetran
→ /dg list components --package fivetran
→ /dg scaffold defs fivetran.FivetranComponent salesforce
→ Configure API keys in .env
→ /dg launch --assets salesforce
```
