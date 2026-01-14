# Resource Patterns Reference

## Pattern Summary

| Pattern | When to Use |
| ------- | ----------- |
| Built-in resource | Database/service with Dagster integration (DuckDB, Snowflake, etc.) |
| Custom `ConfigurableResource` | Custom API clients, services, or shared logic |
| `EnvVar` configuration | Secrets, environment-specific values |
| Resource with methods | Complex services with multiple operations |
| Nested resources | Resources that depend on other resources |

---

## Using Built-in Resources

Dagster provides pre-built resources for common services:

### DuckDB Resource

```python
from dagster_duckdb import DuckDBResource
import dagster as dg

database_resource = DuckDBResource(
    database=dg.EnvVar("DUCKDB_DATABASE")
)

@dg.definitions
def resources():
    return dg.Definitions(
        resources={"database": database_resource}
    )
```

**Using in assets:**

```python
from dagster_duckdb import DuckDBResource

@dg.asset(deps=["raw_data"])
def processed_data(database: DuckDBResource) -> None:
    query = """
        CREATE OR REPLACE TABLE processed AS
        SELECT * FROM raw_data WHERE status = 'active'
    """
    with database.get_connection() as conn:
        conn.execute(query)
```

### Common Built-in Resources

| Package | Resource | Use Case |
| ------- | -------- | -------- |
| `dagster_duckdb` | `DuckDBResource` | Local/embedded analytics |
| `dagster_snowflake` | `SnowflakeResource` | Snowflake data warehouse |
| `dagster_gcp` | `BigQueryResource` | Google BigQuery |
| `dagster_aws` | `S3Resource` | AWS S3 storage |
| `dagster_dbt` | `DbtCliResource` | dbt transformations |
| `dagster_dlt` | `DagsterDltResource` | dlt pipelines |
| `dagster_sling` | `SlingResource` | Database replication |

---

## Custom ConfigurableResource

Create custom resources for APIs and services:

### Basic API Resource

```python
import dagster as dg
import requests

class NASAResource(dg.ConfigurableResource):
    api_key: str
    base_url: str = "https://api.nasa.gov"
    
    def get_near_earth_asteroids(self, start_date: str, end_date: str) -> list:
        url = f"{self.base_url}/neo/rest/v1/feed"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "api_key": self.api_key,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()["near_earth_objects"][start_date]
```

### Resource with Multiple Methods

```python
class DatabaseClient(dg.ConfigurableResource):
    connection_string: str
    schema: str = "public"
    
    def query(self, sql: str) -> list[dict]:
        """Execute a query and return results."""
        # Implementation
        pass
    
    def execute(self, sql: str) -> None:
        """Execute a statement without returning results."""
        pass
    
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists."""
        pass
```

---

## Configuration with EnvVar

Use `EnvVar` for secrets and environment-specific values:

```python
import dagster as dg

class APIResource(dg.ConfigurableResource):
    api_key: str
    environment: str = "production"

# In definitions
@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "api": APIResource(
                api_key=dg.EnvVar("API_KEY"),
                environment=dg.EnvVar("ENVIRONMENT"),
            ),
        },
    )
```

### EnvVar vs os.getenv

| Feature | `dg.EnvVar` | `os.getenv` |
| ------- | ----------- | ----------- |
| When evaluated | At run start | At code location load |
| Dynamic updates | Yes | No (requires restart) |
| UI visibility | Shown in resource config | Not visible |
| Best for | Production secrets | Development defaults |

---

## Registering Resources

### Modern Pattern with @definitions

```python
# src/my_project/defs/resources.py
import dagster as dg
from dagster_duckdb import DuckDBResource

database = DuckDBResource(database=dg.EnvVar("DUCKDB_DATABASE"))

@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "database": database,
            "api": MyAPIResource(api_key=dg.EnvVar("API_KEY")),
        },
    )
```

### Traditional Pattern

```python
# src/my_project/definitions.py
import dagster as dg

defs = dg.Definitions(
    assets=[...],
    resources={
        "database": DuckDBResource(...),
        "api": MyAPIResource(...),
    },
)
```

---

## Using Resources in Assets

### Type-Annotated Parameter

```python
@dg.asset
def my_asset(database: DuckDBResource) -> None:
    """
    The parameter name must match the resource key in Definitions.
    The type annotation tells Dagster this is a resource, not an asset.
    """
    with database.get_connection() as conn:
        conn.execute("SELECT 1")
```

### Multiple Resources

```python
@dg.asset
def my_asset(
    database: DuckDBResource,
    api: NASAResource,
) -> None:
    """Asset using multiple resources."""
    data = api.get_near_earth_asteroids("2024-01-01", "2024-01-07")
    with database.get_connection() as conn:
        # Load data into database
        pass
```

### Resource with Context

```python
@dg.asset
def my_asset(
    context: dg.AssetExecutionContext,
    database: DuckDBResource,
) -> None:
    """Combine context logging with resource usage."""
    context.log.info("Starting data load")
    with database.get_connection() as conn:
        result = conn.execute("SELECT COUNT(*) FROM table")
        context.log.info(f"Processed {result.fetchone()[0]} rows")
```

---

## Resource Lifecycle

### Context Manager Pattern

Many resources support context managers for proper cleanup:

```python
@dg.asset
def my_asset(database: DuckDBResource) -> None:
    # Connection automatically closed when exiting 'with' block
    with database.get_connection() as conn:
        conn.execute("INSERT INTO table VALUES (1, 2, 3)")
```

### Manual Connection Management

For resources that don't use context managers:

```python
class MyResource(dg.ConfigurableResource):
    connection_string: str
    
    def connect(self):
        return create_connection(self.connection_string)
    
    def close(self, conn):
        conn.close()

@dg.asset
def my_asset(my_resource: MyResource) -> None:
    conn = my_resource.connect()
    try:
        # Do work
        pass
    finally:
        my_resource.close(conn)
```

---

## Nested Resources

Resources that depend on other resources:

```python
class AuthResource(dg.ConfigurableResource):
    api_key: str
    
    def get_token(self) -> str:
        # Authentication logic
        return f"Bearer {self.api_key}"

class DataAPIResource(dg.ConfigurableResource):
    auth: AuthResource
    base_url: str
    
    def fetch_data(self, endpoint: str) -> dict:
        headers = {"Authorization": self.auth.get_token()}
        response = requests.get(f"{self.base_url}/{endpoint}", headers=headers)
        return response.json()

# In definitions
@dg.definitions
def resources():
    auth = AuthResource(api_key=dg.EnvVar("API_KEY"))
    return dg.Definitions(
        resources={
            "auth": auth,
            "data_api": DataAPIResource(auth=auth, base_url="https://api.example.com"),
        },
    )
```

---

## Testing Resources

### Mock Resources

```python
from unittest.mock import Mock

def test_asset_with_mocked_resource():
    mocked_database = Mock()
    mocked_database.get_connection.return_value.__enter__ = Mock(
        return_value=Mock(execute=Mock(return_value=[{"id": 1}]))
    )
    mocked_database.get_connection.return_value.__exit__ = Mock(return_value=None)
    
    result = dg.materialize(
        assets=[my_asset],
        resources={"database": mocked_database},
    )
    assert result.success
```

### Test Resource Implementation

```python
class TestDatabaseResource(dg.ConfigurableResource):
    """In-memory database for testing."""
    
    def get_connection(self):
        return sqlite3.connect(":memory:")

# Use in tests
def test_with_test_resource():
    result = dg.materialize(
        assets=[my_asset],
        resources={"database": TestDatabaseResource()},
    )
    assert result.success
```

---

## Common Patterns

### Retry Logic in Resources

```python
import time

class RobustAPIResource(dg.ConfigurableResource):
    api_key: str
    max_retries: int = 3
    retry_delay: float = 1.0
    
    def _request_with_retry(self, url: str, params: dict) -> dict:
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(self.retry_delay * (attempt + 1))
```

### Caching in Resources

```python
from functools import lru_cache

class CachedAPIResource(dg.ConfigurableResource):
    api_key: str
    
    @lru_cache(maxsize=100)
    def get_reference_data(self, key: str) -> dict:
        """Cached lookup for reference data."""
        response = requests.get(f"https://api.example.com/ref/{key}")
        return response.json()
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Better Approach |
| ------------ | --------------- |
| Hardcoded credentials | Use `dg.EnvVar("SECRET")` |
| Creating connections in assets | Use resources for connection management |
| No type annotation on resource params | Always type: `database: DuckDBResource` |
| Global connection objects | Pass resources as parameters |
| Ignoring cleanup | Use context managers or explicit close |

---

## References

- [Resources API](https://docs.dagster.io/api/dagster/resources)
- [ConfigurableResource](https://docs.dagster.io/guides/build/external-resources)
- [Built-in Integrations](https://docs.dagster.io/integrations)

