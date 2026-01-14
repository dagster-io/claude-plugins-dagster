# Testing Patterns Reference

## Pattern Summary

| Pattern | When to Use |
| ------- | ----------- |
| Direct function test | Simple asset with no resources |
| Test with mock inputs | Asset with dependencies |
| `dg.materialize()` | Test asset graph execution |
| Mocked resources | Isolate from external services |
| Integration tests | Verify real service connections |
| Asset checks | Runtime data validation |

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
# tests/test_population.py
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

| Mock Functions When | Mock Resources When |
| ------------------- | ------------------- |
| Testing resource implementation | Testing asset logic |
| Need to verify call parameters | Testing asset graph |
| Resource has simple interface | Resource has multiple methods |
| Testing error handling | Testing happy path |

---

## Integration Tests

### Test with Real Services

```python
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
# tests/docker-compose.yaml
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
# tests/conftest.py
import pytest

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

| Anti-Pattern | Better Approach |
| ------------ | --------------- |
| Testing in production | Use staging or mock resources |
| No assertions beyond `success` | Use `output_for_node()` to verify outputs |
| Ignoring test isolation | Each test should be independent |
| Hardcoded test data paths | Use fixtures and relative paths |
| Skipping asset check tests | Test checks like any other function |

---

## References

- [Testing Assets](https://docs.dagster.io/guides/test/testing-assets)
- [Asset Checks](https://docs.dagster.io/guides/test/asset-checks)
- [Mocking Resources](https://docs.dagster.io/guides/test/mocking-resources)

