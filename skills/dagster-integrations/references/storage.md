# Storage Integrations

Data warehouses, databases, object storage, and table formats for persistent data storage and
analytics.

---

## Data Warehouses

### Snowflake

**Package:** `dagster-snowflake` | **Support:** Dagster-supported

Cloud data warehouse for storing and querying large-scale analytics data.

**Use cases:**

- Store processed analytics tables for BI tools
- Query large datasets with SQL
- Integrate with dbt for SQL transformations
- Use as persistent storage for Dagster assets

**Quick start:**

```python
from dagster_snowflake import SnowflakeResource
from dagster_snowflake_pandas import SnowflakePandasIOManager

snowflake = SnowflakeResource(
    account="abc12345.us-east-1",
    user=dg.EnvVar("SNOWFLAKE_USER"),
    password=dg.EnvVar("SNOWFLAKE_PASSWORD"),
    database="analytics",
    schema="public"
)

# Use as IO Manager to auto-save DataFrames
defs = dg.Definitions(
    assets=[...],
    resources={
        "snowflake": snowflake,
        "io_manager": SnowflakePandasIOManager(
            resource=snowflake
        )
    }
)
```

**Docs:** https://docs.dagster.io/integrations/libraries/snowflake

---

### BigQuery

**Package:** `dagster-gcp` | **Support:** Dagster-supported

Google's serverless data warehouse.

**Use cases:**

- Run SQL analytics on petabyte-scale data
- Store structured data for analysis
- Query data with standard SQL
- Integrate with GCP data pipeline

**Quick start:**

```python
from dagster_gcp import BigQueryResource
from dagster_gcp_pandas import BigQueryPandasIOManager

bigquery = BigQueryResource(
    project="my-project"
)

@dg.asset
def query_bigquery(bigquery: BigQueryResource):
    return bigquery.get_client().query(
        "SELECT * FROM `project.dataset.table` LIMIT 1000"
    ).to_dataframe()
```

**Docs:** https://docs.dagster.io/integrations/libraries/gcp

---

### DuckDB

**Package:** `dagster-duckdb` | **Support:** Dagster-supported

In-process SQL analytics database, excellent for local development and single-machine analytics.

**Use cases:**

- Local development without external database
- Fast SQL queries on parquet/CSV files
- Embedded analytics in applications
- Testing and prototyping

**Quick start:**

```python
from dagster_duckdb import DuckDBResource
from dagster_duckdb_pandas import DuckDBPandasIOManager

duckdb = DuckDBResource(database="analytics.duckdb")

# Use as IO Manager
defs = dg.Definitions(
    assets=[...],
    resources={
        "io_manager": DuckDBPandasIOManager(
            database="analytics.duckdb"
        )
    }
)
```

**Docs:** https://docs.dagster.io/integrations/libraries/duckdb

---

### Redshift

**Package:** `dagster-aws` | **Support:** Dagster-supported

AWS managed data warehouse based on PostgreSQL, optimized for OLAP workloads.

**Use cases:**

- Store large analytics datasets on AWS
- Query data with PostgreSQL-compatible SQL
- Integrate with AWS data ecosystem
- Run complex analytical queries

**Quick start:**

```python
from dagster_aws.redshift import RedshiftClientResource

redshift = RedshiftClientResource(
    cluster_identifier="my-cluster",
    db_name="analytics",
    db_user=dg.EnvVar("REDSHIFT_USER"),
    region_name="us-west-2"
)

@dg.asset
def redshift_query(redshift: RedshiftClientResource):
    result = redshift.get_client().execute_statement(
        Database="analytics",
        Sql="SELECT * FROM sales_summary"
    )
    return result
```

**Docs:** https://docs.dagster.io/integrations/libraries/aws

---

### Teradata

**Package:** `dagster-teradata` | **Support:** Community-supported

Enterprise data warehouse platform for large-scale analytics and parallel processing.

**Use cases:**

- Connect to enterprise Teradata deployments
- Execute parallel queries on large datasets
- Integrate Teradata with modern data stack
- Migrate from Teradata to cloud warehouses

**Quick start:**

```python
from dagster_teradata import TeradataResource

teradata = TeradataResource(
    host="teradata.company.com",
    user=dg.EnvVar("TERADATA_USER"),
    password=dg.EnvVar("TERADATA_PASSWORD")
)

@dg.asset
def teradata_data(teradata: TeradataResource):
    return teradata.execute_query(
        "SELECT * FROM enterprise_data"
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/teradata

---

## Relational Databases

### Postgres

**Package:** `dagster-postgres` | **Support:** Dagster-supported

⚠️ **Note:** The `dagster-postgres` package provides Dagster instance storage only (event logs, run
storage, schedule storage). For connecting to Postgres from your assets, create a custom resource
using the ConfigurableResource pattern.

**Use cases:**

- Dagster instance storage configuration (dagster.yaml)
- Custom Postgres connections for assets (via ConfigurableResource pattern)

**Quick start (custom resource pattern):**

```python
import psycopg2
from dagster import ConfigurableResource
import dg

class PostgresResource(ConfigurableResource):
    """Custom Postgres resource for asset data access."""
    host: str
    port: int = 5432
    user: str
    password: str
    database: str

    def get_connection(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )

# Usage in definitions
postgres = PostgresResource(
    host="localhost",
    port=5432,
    user=dg.EnvVar("POSTGRES_USER"),
    password=dg.EnvVar("POSTGRES_PASSWORD"),
    database="analytics"
)

@dg.asset
def postgres_table(postgres: PostgresResource):
    with postgres.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
```

**Docs:** https://docs.dagster.io/integrations/libraries/postgres

---

### MySQL

**Package:** `dagster-mysql` | **Support:** Dagster-supported

Popular open-source relational database management system.

**Use cases:**

- Web application databases
- Transactional workloads
- Legacy system integration
- Read replicas for analytics

**Quick start:**

```python
from dagster_mysql import MySQLResource

mysql = MySQLResource(
    host="localhost",
    port=3306,
    user=dg.EnvVar("MYSQL_USER"),
    password=dg.EnvVar("MYSQL_PASSWORD"),
    database="production"
)

@dg.asset
def mysql_data(mysql: MySQLResource):
    with mysql.get_connection() as conn:
        return pd.read_sql("SELECT * FROM orders", conn)
```

**Docs:** https://docs.dagster.io/integrations/libraries/mysql

---

## Vector Databases

### Weaviate

**Package:** `dagster-weaviate` | **Support:** Community-supported

Vector database for AI-powered search and semantic similarity.

**Use cases:**

- Store and search embeddings
- Semantic search applications
- Recommendation systems
- RAG (Retrieval Augmented Generation)

**Quick start:**

```python
from dagster_weaviate import WeaviateResource

weaviate = WeaviateResource(
    url="http://localhost:8080",
    auth_api_key=dg.EnvVar("WEAVIATE_API_KEY")
)

@dg.asset
def store_embeddings(
    embeddings: list[list[float]],
    weaviate: WeaviateResource
):
    client = weaviate.get_client()
    # Store vectors in Weaviate
    for i, vector in enumerate(embeddings):
        client.data_object.create(
            {"text": f"document_{i}"},
            "Document",
            vector=vector
        )
```

**Docs:** https://docs.dagster.io/integrations/libraries/weaviate

---

### Chroma

**Package:** `dagster-chroma` | **Support:** Community-supported

Open-source embedding database for AI applications and vector search.

**Use cases:**

- Store document embeddings
- Build RAG applications
- Semantic search
- AI memory systems

**Quick start:**

```python
from dagster_chroma import ChromaResource

chroma = ChromaResource(
    host="localhost",
    port=8000
)

@dg.asset
def chroma_collection(chroma: ChromaResource):
    client = chroma.get_client()
    collection = client.create_collection("documents")
    collection.add(
        documents=["doc1", "doc2"],
        embeddings=[[1, 2, 3], [4, 5, 6]],
        ids=["id1", "id2"]
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/chroma

---

### Qdrant

**Package:** `dagster-qdrant` | **Support:** Community-supported

High-performance vector similarity search engine.

**Use cases:**

- Large-scale vector search
- Recommendation engines
- Image similarity search
- Neural search applications

**Quick start:**

```python
from dagster_qdrant import QdrantResource

qdrant = QdrantResource(
    url="http://localhost:6333",
    api_key=dg.EnvVar("QDRANT_API_KEY")
)

@dg.asset
def qdrant_vectors(qdrant: QdrantResource):
    client = qdrant.get_client()
    # Create collection and add vectors
    client.create_collection(
        collection_name="documents",
        vectors_config={"size": 384, "distance": "Cosine"}
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/qdrant

---

## Table Formats & Storage Layers

### Delta Lake

**Package:** `dagster-deltalake` | **Support:** Community-supported

Open-source storage layer providing ACID transactions and time travel for data lakes.

**Use cases:**

- Reliable data lake storage with ACID guarantees
- Time travel and data versioning
- Schema evolution for data lakes
- Integration with Spark and Databricks

**Quick start:**

```python
from dagster_deltalake import DeltaTableResource

deltalake = DeltaTableResource(
    table_uri="s3://bucket/delta/table",
    storage_options={
        "AWS_ACCESS_KEY_ID": dg.EnvVar("AWS_KEY"),
        "AWS_SECRET_ACCESS_KEY": dg.EnvVar("AWS_SECRET")
    }
)

@dg.asset
def delta_table(deltalake: DeltaTableResource):
    delta = deltalake.load()
    return delta.to_pandas()
```

**Docs:** https://docs.dagster.io/integrations/libraries/deltalake

---

### Iceberg

**Package:** `dagster-iceberg` | **Support:** Community-supported

Apache Iceberg table format for large analytic datasets with schema evolution and partition
evolution.

**Use cases:**

- Manage large analytics tables in data lakes
- Schema and partition evolution
- Time travel queries
- Multi-engine table access (Spark, Trino, etc.)

**Quick start:**

```python
from dagster_iceberg import IcebergResource

iceberg = IcebergResource(
    catalog_uri="thrift://localhost:9083",
    warehouse="s3://my-bucket/warehouse"
)

@dg.asset
def iceberg_table(iceberg: IcebergResource):
    return iceberg.read_table(
        "database.table_name"
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/iceberg

---

## File & Object Storage

### LakeFS

**Package:** `lakefs-client` (use with custom resource) | **Support:** Community-supported

Git-like version control for data lakes with branching and merging.

**Use cases:**

- Version control for data lakes
- Data experimentation with branches
- Reproducible data pipelines
- Data rollback capabilities

**Quick start:**

```python
from dagster import ConfigurableResource
from lakefs_client import Configuration, LakeFSClient

class LakeFSResource(ConfigurableResource):
    """Custom LakeFS resource using lakefs-client SDK."""
    endpoint_url: str
    access_key_id: str
    secret_access_key: str

    def get_client(self) -> LakeFSClient:
        config = Configuration(
            host=self.endpoint_url,
            username=self.access_key_id,
            password=self.secret_access_key
        )
        return LakeFSClient(config)

lakefs = LakeFSResource(
    endpoint_url="http://localhost:8000",
    access_key_id=dg.EnvVar("LAKEFS_ACCESS_KEY"),
    secret_access_key=dg.EnvVar("LAKEFS_SECRET_KEY")
)

@dg.asset
def lakefs_data(lakefs: LakeFSResource):
    client = lakefs.get_client()
    # Use LakeFS SDK for operations
    # See LakeFS Python SDK documentation
```

**Docs:** https://docs.dagster.io/integrations/libraries/lakefs

---

### Obstore

**Package:** `dagster-obstore` | **Support:** Community-supported

Universal object store abstraction supporting S3, GCS, Azure, and local files.

**Use cases:**

- Cloud-agnostic object storage
- Unified API for multiple clouds
- Local development with production parity
- Multi-cloud deployments

**Quick start:**

```python
from dagster_obstore import ObstoreResource

obstore = ObstoreResource(
    store_url="s3://my-bucket/path"
    # or "gs://bucket", "az://container", "file:///local/path"
)

@dg.asset
def cloud_agnostic_storage(obstore: ObstoreResource):
    # Works with any cloud
    data = obstore.read("data.parquet")
    return pd.read_parquet(data)
```

**Docs:** https://docs.dagster.io/integrations/libraries/obstore

**Note**: For cloud-specific object storage (AWS S3, GCS, Azure Blob), see the Compute category's
cloud platform integrations.

---

## Metadata & Catalog

### DataHub

**Package:** `dagster-datahub` | **Support:** Dagster-supported

Metadata catalog for data discovery, lineage, and governance.

**Use cases:**

- Publish Dagster lineage to DataHub
- Data discovery and search
- Metadata management
- Data governance

**Quick start:**

```python
from dagster_datahub import DatahubRESTEmitterResource

datahub = DatahubRESTEmitterResource(
    connection="http://localhost:8080",
    token=dg.EnvVar("DATAHUB_TOKEN")
)

@dg.asset
def publish_to_datahub(datahub: DatahubRESTEmitterResource):
    # Get emitter to publish metadata to DataHub
    emitter = datahub.get_emitter()
    # Use DataHub SDK to create and emit metadata events
    # See DataHub documentation for specific metadata event creation
```

**Docs:** https://docs.dagster.io/integrations/libraries/datahub

---

## Storage Selection Guide

| Type                | Best For            | Examples                      | Scale        |
| ------------------- | ------------------- | ----------------------------- | ------------ |
| **Data Warehouses** | Analytical queries  | Snowflake, BigQuery, Redshift | Petabytes    |
| **Relational**      | Transactional data  | Postgres, MySQL               | Small-Large  |
| **Vector**          | Embeddings, AI      | Weaviate, Chroma, Qdrant      | Medium-Large |
| **Table Formats**   | Data lake tables    | Delta, Iceberg                | Large        |
| **Object Storage**  | Files, unstructured | S3, GCS, Azure Blob           | Any          |
| **Metadata**        | Catalogs, lineage   | DataHub                       | N/A          |

## Common Patterns

### Multi-Storage Pattern

```python
@dg.asset
def raw_data() -> pd.DataFrame:
    return extract_data()

@dg.asset
def warehouse_table(raw_data: pd.DataFrame, snowflake: SnowflakeResource):
    # Store in warehouse for analytics
    snowflake.write_dataframe(raw_data, "analytics.raw")

@dg.asset
def app_database(raw_data: pd.DataFrame, postgres: PostgresResource):
    # Store in Postgres for application
    postgres.write_dataframe(raw_data, "public.users")

@dg.asset
def search_index(raw_data: pd.DataFrame, weaviate: WeaviateResource):
    # Create search index
    weaviate.index_documents(raw_data)
```

### Local Development Pattern

Use DuckDB for local development and switch to production warehouse for deployment. This provides a
fast, free local environment that mirrors production schemas.
