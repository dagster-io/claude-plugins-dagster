# Testing Patterns Reference

## Pattern Summary

| Pattern               | When to Use                     |
| --------------------- | ------------------------------- |
| Direct function test  | Simple asset with no resources  |
| Test with mock inputs | Asset with dependencies         |
| `dg.materialize()`    | Test asset graph execution      |
| Mocked resources      | Isolate from external services  |
| Integration tests     | Verify real service connections |
| Asset checks          | Runtime data validation         |

---

## Testing Workflow

Tests should focus on ensuring the logic of code when possible rather than testing Dagster
functionality.

### Testing Philosophy

Use a **defense-in-depth testing strategy** with multiple layers:

```
┌─────────────────────────────────────────────────────────┐
│  Layer 3: Integration & E2E Tests (20%)                 │  ← Real services, Docker, staging
├─────────────────────────────────────────────────────────┤
│  Layer 2: Asset Graph Tests (25%)                       │  ← dg.materialize() with mocks
├─────────────────────────────────────────────────────────┤
│  Layer 1: Direct Function Tests (55%)                   │  ← Call asset functions directly
└─────────────────────────────────────────────────────────┘
```

**Philosophy**: Test business logic extensively with fast, isolated tests. Use real implementations
sparingly for integration validation.

### Test Distribution

| Layer | Test Type               | Location                      | Portion |
| ----- | ----------------------- | ----------------------------- | ------- |
| 1     | Direct function tests   | `tests/unit/test_*.py`        | 55%     |
| 2     | Asset graph tests       | `tests/unit/test_*.py`        | 25%     |
| 3     | Integration & E2E tests | `tests/integration/test_*.py` | 20%     |

### Layer 1: Direct Function Tests (55%)

**Purpose**: Test asset business logic directly as Python functions.

**When to use**: For EVERY asset. This is the default testing approach.

**Why**: Fast, reliable, easy to debug. No Dagster overhead.

```python
# Asset under test
@dg.asset
def calculate_revenue(orders: list[dict]) -> float:
    return sum(order["price"] * order["quantity"] for order in orders)

# Direct function test - call the asset like a regular function
def test_calculate_revenue():
    mock_orders = [
        {"price": 10.0, "quantity": 2},
        {"price": 25.0, "quantity": 1},
    ]

    result = calculate_revenue(mock_orders)

    assert result == 45.0
```

**What to test at this layer**:

- Business logic and calculations
- Data transformations
- Edge cases (empty inputs, nulls, invalid data)
- Error conditions

**Characteristics**:

- Runs in milliseconds
- No Dagster context needed
- Provide mock inputs for upstream dependencies
- Test the function, not the framework

### Layer 2: Asset Graph Tests (25%)

**Purpose**: Test asset materialization, graph execution, and resource integration with mocked
resources.

**When to use**: When testing asset interactions, configs, or resource dependencies.

**Why**: Validates Dagster-specific behavior (context, configs, IO managers) without slow external
calls.

```python
def test_asset_graph_with_mocked_resource():
    mocked_db = Mock()
    mocked_db.query.return_value = [{"id": 1, "name": "Alice"}]

    result = dg.materialize(
        assets=[fetch_users, process_users],
        resources={"database": mocked_db},
    )

    assert result.success
    assert result.output_for_node("process_users") == [{"id": 1, "name": "ALICE"}]
```

**What to test at this layer**:

- Asset graph execution order
- Resource injection
- Run configs and asset configs
- Multi-asset interactions
- IO manager behavior
- Partitioned asset logic

**Characteristics**:

- Uses `dg.materialize()` or `build_asset_context()`
- Mock external resources (databases, APIs)
- Validates Dagster integration points
- Slower than Layer 1, but still fast (no I/O)

### Layer 3: Integration & E2E Tests (20%)

**Purpose**: Validate real resource connections, external system behavior, and end-to-end workflows.

**When to use**: For critical paths where mock behavior might diverge from reality, and for smoke
testing complete workflows.

**Why**: Catches issues that mocks miss (actual SQL syntax, API quirks, authentication, real system
interactions).

**Resource connection test**:

```python
@pytest.mark.integration
def test_snowflake_connection():
    """Integration test with real Snowflake (staging)."""
    resource = SnowflakeResource(
        account=dg.EnvVar("SNOWFLAKE_ACCOUNT"),
        user=dg.EnvVar("SNOWFLAKE_USERNAME"),
        password=dg.EnvVar("SNOWFLAKE_PASSWORD"),
        database="STAGING",
    )

    # Test actual connection works
    with resource.get_connection() as conn:
        result = conn.execute("SELECT 1").fetchone()
        assert result[0] == 1
```

**End-to-end pipeline test**:

```python
@pytest.mark.integration
def test_complete_etl_pipeline(docker_postgres):
    """E2E test: complete pipeline with real database."""
    result = dg.materialize(
        assets=[extract_orders, transform_orders, load_orders],
        resources={"database": docker_postgres},
    )

    assert result.success

    # Verify data actually landed
    with docker_postgres.get_connection() as conn:
        rows = conn.execute("SELECT COUNT(*) FROM orders").fetchone()
        assert rows[0] > 0
```

**What to test at this layer**:

- Database connection and query execution
- API authentication and response parsing
- Critical business workflows
- Data pipeline end-to-end correctness
- Production configuration validation

**Characteristics**:

- Requires environment setup (credentials, staging systems, Docker)
- Slower (seconds to minutes with real network calls)
- May be skipped in CI without proper environment
- Use pytest markers: `@pytest.mark.integration`
- Use sparingly as final validation

### Decision Tree: Where Should My Test Go?

```
┌─ I need to test...
│
├─ BUSINESS LOGIC in an asset (calculations, transformations)
│  └─> Layer 1: Direct function test
│
├─ ASSET INTERACTIONS (graph execution, dependencies)
│  └─> Layer 2: Asset graph test with mocked resources
│
├─ RESOURCE BEHAVIOR (configs, partitions, IO managers)
│  └─> Layer 2: Asset graph test with build_asset_context()
│
└─ REAL SERVICE CONNECTION or CRITICAL E2E WORKFLOW
   └─> Layer 3: Integration test (sparingly)
```

**Default**: Start with Layer 1 (direct function test). Only move up layers when you need to test
Dagster-specific behavior or real integrations.

### When NOT to Use Higher Layers

| Don't Use             | For                                | Instead Use                  |
| --------------------- | ---------------------------------- | ---------------------------- |
| Layer 2 (materialize) | Testing pure business logic        | Layer 1 (direct call)        |
| Layer 3 (integration) | Testing error handling             | Layer 1/2 with mocked errors |
| Layer 3 (integration) | Rapid iteration during development | Layer 1/2                    |
| Layer 3 (integration) | Testing edge cases                 | Layer 1 with mock inputs     |

### Test Speed Guidelines

| Layer | Expected Speed | If Slower, Consider         |
| ----- | -------------- | --------------------------- |
| 1     | < 100ms        | Check for hidden I/O        |
| 2     | < 500ms        | Mock expensive resources    |
| 3     | < 60s          | Parallelize or reduce scope |

---

## Unit Testing Assets

### Direct Function Testing

Assets are Python functions - test them directly:

```python
# src/my_project/defs/assets/population.py
@dg.asset
def state_population_file() -> list[dict]:
    file_path = Path(__file__).parent / "../data/ny.csv"
    with open(file_path) as file:
        reader = csv.DictReader(file)
        return [row for row in reader]
```

```python
# tests/unit/test_population.py
def test_state_population_file():
    result = population.state_population_file()

    assert len(result) == 3
    assert result[0] == {
        "City": "New York",
        "Population": "8804190",
    }
```

### Testing with Dependencies

Provide mock inputs for dependent assets:

```python
# Asset with dependency
@dg.asset
def total_population(state_population_file: list[dict]) -> int:
    return sum([int(x["Population"]) for x in state_population_file])
```

```python
# Test with controlled input
def test_total_population():
    mock_input = [
        {"City": "New York", "Population": "8804190"},
        {"City": "Buffalo", "Population": "278349"},
        {"City": "Yonkers", "Population": "211569"},
    ]

    result = total_population(mock_input)

    assert result == 9294108
```

---

## Testing with dg.materialize()

### Basic Materialization Test

```python
import dagster as dg
from my_project.defs.assets import population

def test_asset_materialization():
    result = dg.materialize(
        assets=[
            population.state_population_file,
            population.total_population,
        ]
    )

    assert result.success
```

### Accessing Asset Outputs

```python
def test_asset_outputs():
    result = dg.materialize(
        assets=[
            population.state_population_file,
            population.total_population,
        ]
    )

    assert result.success

    # Access individual outputs
    file_output = result.output_for_node("state_population_file")
    assert len(file_output) == 3

    total = result.output_for_node("total_population")
    assert total == 9294108
```

### Materialization with Resources

```python
def test_with_resources():
    result = dg.materialize(
        assets=[my_asset],
        resources={
            "database": DuckDBResource(database=":memory:"),
        },
    )

    assert result.success
```

### Materialization with Run Config

```python
from my_project.defs.assets import configurable_asset, StateConfig

def test_with_config():
    result = dg.materialize(
        assets=[configurable_asset],
        run_config=dg.RunConfig({
            "configurable_asset": StateConfig(name="ny", limit=100)
        }),
    )

    assert result.success
```

### Testing Assets with Context

Use `build_asset_context()` to create context for testing:

```python
import dagster as dg

def test_asset_with_context():
    """Test asset that requires AssetExecutionContext."""
    context = dg.build_asset_context(
        partition_key="2024-01-01",
        resources={"database": mock_database},
    )

    result = my_asset(context)
    assert result is not None
```

### Testing Multi-Assets with Mock IO Managers

```python
import dagster as dg

class MockIOManager(dg.IOManager):
    def __init__(self, mock_data):
        self.mock_data = mock_data

    def handle_output(self, context, obj):
        pass  # No-op for testing

    def load_input(self, context):
        return self.mock_data.get(context.asset_key.path[-1])

def test_multi_asset():
    mock_io = MockIOManager({"upstream_asset": {"data": [1, 2, 3]}})

    result = dg.materialize(
        assets=[my_multi_asset],
        resources={"io_manager": mock_io},
    )

    assert result.success
```

---

## Ephemeral instance

Some Dagster objects (such as sensors) rely on state in order to be tested correctly. Temporary
state can be maintained for tests with `dg.DagsterInstance.ephemeral()`.

To test a sensor that checks for new files:

```python
def check_for_new_files() -> list[str]:
    if random.random() > 0.5:
        return ["file1", "file2"]
    return []


@dg.sensor(
    name="my_sensor",
    job=jobs.my_job_configured,
    minimum_interval_seconds=5,
)
def my_sensor():
    new_files = check_for_new_files()
    # New files, run `my_job`
    if new_files:
        for filename in new_files:
            yield dg.RunRequest(run_key=filename)
    # No new files, skip the run and log the reason
    else:
        yield dg.SkipReason("No new files found")
```

There should be a test to confirm that sensor registers a `dg.RunRequest` when the sensor logic is
met and that there is a `dg.SkipReason` when the logic is not met:

```python
@patch("dagster_testing.defs.sensors.check_for_new_files", return_value=[])
def test_sensor_skip(mock_check_new_files):
    instance = dg.DagsterInstance.ephemeral()
    context = dg.build_sensor_context(instance=instance)
    assert sensors.my_sensor(context).__next__() == dg.SkipReason("No new files found")


@patch(
    "dagster_testing.defs.sensors.check_for_new_files",
    return_value=["test_file"],
)
def test_sensor_run(mock_check_new_files):
    instance = dg.DagsterInstance.ephemeral()
    context = dg.build_sensor_context(instance=instance)
    assert sensors.my_sensor(context).__next__() == dg.RunRequest(run_key="test_file")
```

---

## Components

Custom components can be tested using
`from dagster.components.testing.utils import create_defs_folder_sandbox`. This creates a temporary
component as if the user had run `dg scaffold defs` to initialize it.

This can be helpful when confirming the component schema when components have complex models:

```python
import dagster as dg

class Ingredient(dg.Model):
    name: str = dg.Field
    quantity: int = dg.Field
    unit: str = dg.Field

class Recipe(dg.Model):
    title: str = dg.Field
    serves: int = dg.Field
    prep_time: int = dg.Field
    cook_time: int = dg.Field
    ingredients: list[Ingredient] = dg.Field

class Cookbook(dg.Component, dg.Model, dg.Resolvable):
    cookbook_title: str = dg.Field
    recipes: list[Recipe]

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        ...
        return dg.Definitions(assets=[_asset])
```

This test will initialize the component and ensures that the correct Dagster objects are created:

```python
import dagster as dg
from dagster.components.testing.utils import create_defs_folder_sandbox

cookbook_yaml_config = {
    "type": "my_project.components.cookbook.Cookbook",
    "attributes": {
        "cookbook_title": "Test Cookbook",
        "recipes": [
            {
                "title": "Test Recipe",
                "serves": 4,
                "prep_time": 10,
                "cook_time": 15,
                "ingredients": [
                    {
                        "name": "Test Ingredient",
                        "quantity": 1,
                        "unit": "Test Unit"
                    }
                ],
            },
        ]
    }
}


def test_cookbook_component():
    with create_defs_folder_sandbox() as sandbox:
        defs_path = sandbox.scaffold_component(component_cls=Cookbook)
        sandbox.scaffold_component(
            component_cls=Cookbook,
            defs_path=defs_path,
            defs_yaml_contents=cookbook_yaml_config
        )

        # Check that all assets are created
        with sandbox.build_all_defs() as defs:
            assert defs.resolve_asset_graph().get_all_asset_keys() == {
                dg.AssetKey(["test_recipe"]),
            }
```

The asset can also be materialized for further testing:

```python
    result = dg.materialize(
        assets=[
            defs.get_assets_def(dg.AssetKey(["test_recipe"])),
        ],
    )
```

---

## Mocking

### Mocking External Services

```python
from unittest.mock import Mock, patch

@patch("requests.get")
def test_api_asset(mock_get):
    # Configure mock response
    mock_response = Mock()
    mock_response.json.return_value = {
        "cities": [
            {"city_name": "New York", "city_population": 8804190}
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Execute asset
    result = my_api_asset()

    # Verify results
    assert len(result) == 1
    assert result[0]["city"] == "New York"

    # Verify mock was called correctly
    mock_get.assert_called_once()
```

### Mocking Resources

Instead of mocking functions, mock the resource:

```python
def test_with_mocked_resource():
    # Create mock resource
    mocked_resource = Mock()
    mocked_resource.get_cities.return_value = [
        {"city": "Fakestown", "population": 42}
    ]

    # Pass mock to asset
    result = state_population_api_resource(mocked_resource)

    assert len(result) == 1
    assert result[0]["city"] == "Fakestown"
```

### Mocked Resources with Materialization

```python
def test_materialization_with_mocked_resource():
    mocked_resource = Mock()
    mocked_resource.get_cities.return_value = [
        {"city": "Fakestown", "population": 42}
    ]

    result = dg.materialize(
        assets=[
            state_population_api_resource,
            total_population_resource,
        ],
        resources={"state_population_resource": mocked_resource},
        run_config=dg.RunConfig({
            "state_population_api_resource": StateConfig(name="ny")
        }),
    )

    assert result.success
    assert result.output_for_node("state_population_api_resource") == [
        {"city": "Fakestown", "population": 42}
    ]
    assert result.output_for_node("total_population_resource") == 42
```

### When to Mock Functions vs Resources

| Mock Functions When             | Mock Resources When           |
| ------------------------------- | ----------------------------- |
| Testing resource implementation | Testing asset logic           |
| Need to verify call parameters  | Testing asset graph           |
| Resource has simple interface   | Resource has multiple methods |
| Testing error handling          | Testing happy path            |

---

## Integration Tests

### Test with Real Services

```python
from dagster import ConfigurableResource
import psycopg2

# Define custom Postgres resource (dagster-postgres only provides instance storage)
class PostgresResource(ConfigurableResource):
    """Custom Postgres resource for asset data access."""
    host: str
    port: int = 5432
    database: str
    user: str
    password: str

    def get_connection(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )

def test_database_integration():
    """Integration test with actual database."""
    postgres_resource = PostgresResource(
        host="localhost",
        port=5432,
        database="test_db",
        user="test_user",
        password="test_pass",
    )

    result = state_population_database(postgres_resource)

    assert len(result) > 0
```

### Test Resource with Different Config

```python
def test_snowflake_staging():
    """Use staging credentials for integration test."""
    staging_resource = SnowflakeResource(
        account=dg.EnvVar("SNOWFLAKE_ACCOUNT"),
        user=dg.EnvVar("SNOWFLAKE_USERNAME"),
        password=dg.EnvVar("SNOWFLAKE_PASSWORD"),
        database="STAGING",
        warehouse="STAGING_WAREHOUSE",
    )

    result = state_population_database(staging_resource)
    assert result.success
```

### Docker-Based Integration Tests

Use Docker Compose for isolated test environments:

```yaml
# tests/e2e/docker-compose.yaml
version: "3.8"
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_pass
    ports:
      - "5432:5432"
```

```python
# tests/e2e/conftest.py
import pytest
from dagster import ConfigurableResource
import psycopg2

# Define custom Postgres resource (dagster-postgres only provides instance storage)
class PostgresResource(ConfigurableResource):
    """Custom Postgres resource for asset data access."""
    host: str
    port: int = 5432
    database: str
    user: str
    password: str

    def get_connection(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )

@pytest.fixture(scope="session")
def postgres_resource():
    """Fixture that provides test database resource."""
    return PostgresResource(
        host="localhost",
        port=5432,
        database="test_db",
        user="test_user",
        password="test_pass",
    )

def test_with_postgres(postgres_resource):
    result = my_database_asset(postgres_resource)
    assert result.success
```

---

## Asset Checks

### Defining Asset Checks

```python
import dagster as dg

@dg.asset
def total_population(
    state_population_file: list[dict],
    state_population_api: list[dict],
) -> int:
    all_data = state_population_file + state_population_api
    return sum([int(x["Population"]) for x in all_data])

@dg.asset_check(asset=total_population)
def non_negative(total_population: int) -> dg.AssetCheckResult:
    """Verify population is never negative."""
    return dg.AssetCheckResult(
        passed=total_population > 0,
        metadata={"value": total_population},
    )
```

### Blocking Asset Checks

Use `blocking=True` to prevent downstream asset materialization on failure:

```python
@dg.asset_check(asset=raw_data, blocking=True)
def validate_schema(raw_data: list[dict]) -> dg.AssetCheckResult:
    """Block downstream processing if schema is invalid."""
    required_columns = {"id", "name", "email"}
    actual_columns = set(raw_data[0].keys()) if raw_data else set()

    passed = required_columns.issubset(actual_columns)

    return dg.AssetCheckResult(
        passed=passed,
        metadata={
            "required_columns": list(required_columns),
            "actual_columns": list(actual_columns),
        },
    )
```

**When to Use Blocking**:

- Schema validation before transformation
- Critical data quality checks
- Prerequisites for expensive downstream operations

### Asset Checks with Severity

```python
@dg.asset_check(asset=my_data)
def row_count_check(my_data: list) -> dg.AssetCheckResult:
    row_count = len(my_data)

    if row_count == 0:
        return dg.AssetCheckResult(
            passed=False,
            severity=dg.AssetCheckSeverity.ERROR,
            metadata={"row_count": 0},
        )
    elif row_count < 100:
        return dg.AssetCheckResult(
            passed=True,  # Warning, not failure
            severity=dg.AssetCheckSeverity.WARN,
            metadata={"row_count": row_count, "message": "Low row count"},
        )
    else:
        return dg.AssetCheckResult(
            passed=True,
            metadata={"row_count": row_count},
        )
```

### Testing Asset Checks

```python
def test_non_negative_check():
    # Test passing case
    result_pass = non_negative(10)
    assert result_pass.passed

    # Test failing case
    result_fail = non_negative(-10)
    assert not result_fail.passed
```

### Multiple Asset Checks

**Individual Checks**:

```python
@dg.asset_check(asset=customer_data)
def unique_ids(customer_data: list[dict]) -> dg.AssetCheckResult:
    ids = [row["id"] for row in customer_data]
    unique_count = len(set(ids))
    total_count = len(ids)

    return dg.AssetCheckResult(
        passed=unique_count == total_count,
        metadata={
            "unique_count": unique_count,
            "total_count": total_count,
            "duplicates": total_count - unique_count,
        },
    )

@dg.asset_check(asset=customer_data)
def no_null_emails(customer_data: list[dict]) -> dg.AssetCheckResult:
    null_emails = sum(1 for row in customer_data if row["email"] is None)

    return dg.AssetCheckResult(
        passed=null_emails == 0,
        metadata={"null_count": null_emails},
    )
```

**Multi-Asset Check (Efficient)**:

```python
import dagster as dg

@dg.multi_asset_check(
    specs=[
        dg.AssetCheckSpec(name="unique_ids", asset="customer_data"),
        dg.AssetCheckSpec(name="no_null_emails", asset="customer_data"),
    ]
)
def customer_data_checks(customer_data: list[dict]):
    """Run multiple checks in a single execution."""
    ids = [row["id"] for row in customer_data]
    unique_count = len(set(ids))
    total_count = len(ids)

    yield dg.AssetCheckResult(
        check_name="unique_ids",
        passed=unique_count == total_count,
        metadata={"duplicates": total_count - unique_count},
    )

    null_emails = sum(1 for row in customer_data if row["email"] is None)

    yield dg.AssetCheckResult(
        check_name="no_null_emails",
        passed=null_emails == 0,
        metadata={"null_count": null_emails},
    )
```

**Use `@multi_asset_check` when**:

- Multiple checks run on the same data
- Loading the asset is expensive
- Checks share computation logic

### Factory Pattern for Asset Checks

Generate asset checks programmatically:

```python
def create_not_null_check(asset_name: str, column: str):
    """Factory to create not-null checks for any column."""
    @dg.asset_check(asset=asset_name, name=f"{column}_not_null")
    def check_fn(asset_value: list[dict]) -> dg.AssetCheckResult:
        null_count = sum(1 for row in asset_value if row.get(column) is None)
        return dg.AssetCheckResult(
            passed=null_count == 0,
            metadata={"null_count": null_count, "column": column},
        )
    return check_fn

# Generate checks
email_check = create_not_null_check("customer_data", "email")
name_check = create_not_null_check("customer_data", "name")
```

---

## Pytest Fixtures

### Common Fixtures

```python
# tests/conftest.py
import pytest
import dagster as dg

@pytest.fixture
def sample_population_data():
    return [
        {"City": "New York", "Population": "8804190"},
        {"City": "Buffalo", "Population": "278349"},
        {"City": "Yonkers", "Population": "211569"},
    ]

@pytest.fixture
def mock_database_resource():
    from unittest.mock import Mock

    mock = Mock()
    mock.query.return_value = []
    return mock

@pytest.fixture
def test_resources():
    return {
        "database": DuckDBResource(database=":memory:"),
    }
```

### Using Fixtures in Tests

```python
def test_with_fixtures(sample_population_data, mock_database_resource):
    result = total_population(sample_population_data)
    assert result == 9294108
```

---

## Testing Definitions

### Validate Definitions Load

```python
def test_definitions_load():
    """Verify all definitions can be loaded without errors."""
    from my_project.definitions import defs

    # Check assets exist
    assert len(defs.get_all_asset_keys()) > 0

    # Check jobs exist
    assert len(defs.get_all_job_defs()) > 0
```

### Test Specific Assets Exist

```python
def test_required_assets_exist():
    from my_project.definitions import defs

    required_assets = [
        dg.AssetKey("raw_data"),
        dg.AssetKey("processed_data"),
        dg.AssetKey("final_report"),
    ]

    all_keys = defs.get_all_asset_keys()

    for asset in required_assets:
        assert asset in all_keys, f"Missing required asset: {asset}"
```

---

## Anti-Patterns to Avoid

| Anti-Pattern                   | Better Approach                           |
| ------------------------------ | ----------------------------------------- |
| Testing in production          | Use staging or mock resources             |
| No assertions beyond `success` | Use `output_for_node()` to verify outputs |
| Ignoring test isolation        | Each test should be independent           |
| Hardcoded test data paths      | Use fixtures and relative paths           |
| Skipping asset check tests     | Test checks like any other function       |

---

## References

- [Testing Assets](https://docs.dagster.io/guides/test/testing-assets)
- [Asset Checks](https://docs.dagster.io/guides/test/asset-checks)
- [Mocking Resources](https://docs.dagster.io/guides/test/mocking-resources)
