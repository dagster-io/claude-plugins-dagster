# Asset Patterns Reference

## Pattern Summary

| Pattern | When to Use |
| ------- | ----------- |
| Basic `@dg.asset` | Simple one-to-one transformation |
| `@multi_asset` | Single operation produces multiple related assets |
| `@graph_asset` | Multiple steps needed to produce one asset |
| `@graph_multi_asset` | Complex pipeline producing multiple assets |
| Parameter-based dependency | Asset depends on another managed asset |
| `deps=` dependency | Asset depends on external or non-Python asset |
| Asset with metadata | Track runtime metrics (row counts, timestamps) |
| Asset groups | Organize related assets visually |
| Asset key prefixes | Namespace assets for multi-tenant or layered data |
| Partitioned assets | Time-series or categorical data splits |
| Asset with `code_version` | Track when asset logic changes |

---

## Launching Assets

Once you've defined assets, you'll need to materialize (launch) them. Use the modern `dg launch` command for all asset execution.

### Quick Launch Examples

```bash
# Single asset
dg launch --assets my_asset

# Multiple assets
dg launch --assets customers orders products

# All assets
dg launch --assets "*"

# Assets by tag
dg launch --assets "tag:priority=high"

# Assets by group
dg launch --assets "group:sales_analytics"

# Assets by kind
dg launch --assets "kind:dbt"
```

### With Environment Variables

Assets often need environment variables for resources (database URLs, API keys):

```bash
# Method 1: uv auto-loads .env
uv run dg launch --assets my_asset

# Method 2: Manual .env loading
set -a; source .env; set +a
dg launch --assets my_asset

# Method 3: Per-environment files
source .env.staging && dg launch --assets my_asset
```

### Partitioned Assets

For assets with partition definitions:

```bash
# Single partition
dg launch --assets my_daily_asset --partition 2024-01-15

# Partition range (backfill)
dg launch --assets my_asset --partition-range "2024-01-01:2024-01-31"

# Multiple partitioned assets
dg launch --assets "tag:schedule=daily" --partition 2024-01-15
```

### With Configuration

Pass runtime configuration to assets:

```bash
# Inline JSON config
dg launch --assets my_asset --config-json '{
  "ops": {
    "my_asset": {
      "config": {
        "batch_size": 1000,
        "enable_validation": true
      }
    }
  }
}'

# Config from file
dg launch --assets my_asset --config-json "$(cat config.json)"
```

### Testing Asset Materialization

Before deploying, test that assets materialize successfully:

```bash
# Validate definitions load
dg check defs

# List all assets
dg list defs

# Test single asset
dg launch --assets my_asset

# Test asset chain (materializes dependencies)
dg launch --assets downstream_asset
```

### Comprehensive Launch Documentation

For detailed coverage of all launch features, see:
- **`/dg:launch` command** - Complete guide to asset launching
- Partition patterns (daily, static, multi-dimensional)
- Configuration structure and patterns
- Environment variable methods
- Asset selection syntax reference
- Troubleshooting guide
- Migration from legacy `dagster asset materialize`

---

## Basic Asset Definition

```python
import dagster as dg

@dg.asset
def my_asset() -> None:
    """
    Docstring becomes the asset description in the UI.
    """
    # Your computation logic
    pass
```

**Key points**:
- Function name becomes the asset key
- Docstring becomes the description
- Return type annotation is optional but recommended

---

## Asset Dependencies

### Parameter-Based Dependencies

When an asset depends on another Dagster-managed asset, use parameters:

```python
@dg.asset
def upstream_asset() -> dict:
    return {"data": [1, 2, 3]}

@dg.asset
def downstream_asset(upstream_asset: dict) -> list:
    """
    Receives the return value of upstream_asset automatically.
    """
    return upstream_asset["data"]
```

**How it works**:
- Parameter name must match the upstream asset's function name
- Dagster automatically passes the materialized output
- Creates a visual dependency in the asset graph

### External Dependencies with `deps=`

When an asset depends on something not managed by Dagster or without a return value:

```python
@dg.asset(deps=["external_table", "raw_file"])
def processed_data() -> None:
    """
    Depends on external_table and raw_file but doesn't receive their values.
    """
    # Read from external sources directly
    pass
```

**Use `deps=` when**:
- The upstream asset doesn't return a value (returns `None`)
- The asset is external (file created by another process)
- You need loose coupling between assets

### Mixed Dependencies

Combine both patterns when needed:

```python
@dg.asset(deps=["raw_file"])
def enriched_data(reference_table: dict) -> dict:
    """
    Depends on:
    - raw_file (via deps=, doesn't receive value)
    - reference_table (via parameter, receives value)
    """
    # Read raw_file from disk, enrich with reference_table
    return {"enriched": reference_table}
```

---

## Asset Metadata

### Definition Metadata (Static)

Applied once when the asset is defined:

```python
@dg.asset(
    description="Detailed description for the UI",
    group_name="analytics",
    key_prefix=["warehouse", "staging"],
    owners=["team:data-engineering", "user@example.com"],
    tags={"priority": "high", "pii": "true", "domain": "sales"},
    code_version="1.2.0",
)
def my_asset() -> None:
    pass
```

**Best Practices for Metadata**:
- **owners**: Specify team (`team:name`) or individuals for accountability
- **tags**: Primary organizational mechanism—use liberally for filtering and grouping
- **code_version**: Track when asset logic changes for lineage and debugging
- **description**: Explain what the asset represents and its business purpose
- **group_name**: Visual organization in UI (use for layers or domains)
- **key_prefix**: Hierarchical namespacing for multi-tenant or layered architectures

### Materialization Metadata (Dynamic)

Captured each time the asset materializes:

```python
import dagster as dg

@dg.asset
def my_asset() -> dg.MaterializeResult:
    """Asset that reports metadata on each run."""
    data = fetch_data()
    row_count = len(data)

    # Save data...

    return dg.MaterializeResult(
        metadata={
            "row_count": dg.MetadataValue.int(row_count),
            "last_updated": dg.MetadataValue.text(str(datetime.now())),
            "sample_data": dg.MetadataValue.json(data[:5]),
        }
    )
```

### MetadataValue Types

| Type | Usage |
| ---- | ----- |
| `MetadataValue.int(n)` | Integer values (row counts) |
| `MetadataValue.float(n)` | Float values (percentages) |
| `MetadataValue.text(s)` | Short text values |
| `MetadataValue.json(obj)` | JSON-serializable objects |
| `MetadataValue.md(s)` | Markdown text |
| `MetadataValue.url(s)` | Clickable URLs |
| `MetadataValue.path(s)` | File paths |
| `MetadataValue.table(records)` | Tabular data |

---

## Asset Groups

Organize related assets visually in the UI:

```python
@dg.asset(group_name="raw_data")
def raw_orders() -> None:
    pass

@dg.asset(group_name="raw_data")
def raw_customers() -> None:
    pass

@dg.asset(group_name="analytics")
def daily_revenue(raw_orders) -> None:
    pass
```

**Best practices**:
- Group by data layer: `raw`, `staging`, `analytics`, `mart`
- Group by domain: `sales`, `marketing`, `finance`
- Group by source: `postgres`, `api`, `files`

---

## Asset Key Prefixes

Namespace assets for organization:

```python
@dg.asset(key_prefix=["warehouse", "raw"])
def orders() -> None:
    """Asset key becomes: warehouse/raw/orders"""
    pass

@dg.asset(key_prefix=["warehouse", "staging"])
def orders_cleaned() -> None:
    """Asset key becomes: warehouse/staging/orders_cleaned"""
    pass
```

**Use prefixes for**:
- Multi-tenant architectures
- Environment separation
- Data layer organization (bronze/silver/gold)

---

## Asset with Execution Context

Access runtime information during materialization:

```python
@dg.asset
def context_aware_asset(context: dg.AssetExecutionContext) -> None:
    context.log.info("Starting asset materialization")

    # Access asset key
    asset_key = context.asset_key

    # Access partition key (if partitioned)
    if context.has_partition_key:
        partition = context.partition_key
        context.log.info(f"Processing partition: {partition}")

    # Access run ID
    run_id = context.run_id
```

---

## Asset with Configuration

Make assets configurable at runtime:

```python
from dagster import Config

class MyAssetConfig(Config):
    limit: int = 100
    include_archived: bool = False
    source_path: str

@dg.asset
def configurable_asset(config: MyAssetConfig) -> None:
    """
    Run with specific configuration values.
    """
    data = load_data(
        path=config.source_path,
        limit=config.limit,
        include_archived=config.include_archived,
    )
```

---

## Asset Return Types

### Returning Data Directly

```python
@dg.asset
def returns_data() -> dict:
    return {"key": "value"}
```

### Returning MaterializeResult

```python
@dg.asset
def returns_result() -> dg.MaterializeResult:
    # Do work...
    return dg.MaterializeResult(
        metadata={"rows": 100}
    )
```

### Returning Output with Type

```python
from dagster import Output

@dg.asset
def returns_output() -> Output[dict]:
    data = {"key": "value"}
    return Output(
        value=data,
        metadata={"size": len(data)},
    )
```

---

## Multi-Asset Pattern

Define multiple assets from one function:

```python
from dagster import multi_asset, AssetOut

@multi_asset(
    outs={
        "users": AssetOut(),
        "orders": AssetOut(),
    }
)
def load_data():
    users_df = fetch_users()
    orders_df = fetch_orders()

    yield Output(users_df, output_name="users")
    yield Output(orders_df, output_name="orders")
```

**Use when**:
- One computation produces multiple logical assets
- Assets are always created together
- Shared setup is expensive

---

## Graph Assets

### @graph_asset Pattern

Use when multiple steps are needed to produce a single asset:

```python
from dagster import graph_asset, op

@op
def fetch_data() -> dict:
    return {"raw": [1, 2, 3]}

@op
def transform_data(data: dict) -> dict:
    return {"processed": [x * 2 for x in data["raw"]]}

@op
def validate_data(data: dict) -> dict:
    assert len(data["processed"]) > 0
    return data

@graph_asset
def complex_asset():
    """Encapsulates multi-step logic into a single asset."""
    raw = fetch_data()
    processed = transform_data(raw)
    return validate_data(processed)
```

**Use When**:
- Single asset requires multiple distinct steps
- You want to encapsulate complexity
- Testing individual steps is important
- Steps are reusable across multiple assets

### @graph_multi_asset Pattern

Use for complex pipelines producing multiple assets:

```python
from dagster import graph_multi_asset, AssetOut

@graph_multi_asset(
    outs={
        "users": AssetOut(),
        "orders": AssetOut(),
    }
)
def etl_pipeline():
    """Multi-step pipeline producing multiple assets."""
    raw_data = extract_from_api()
    cleaned = clean_data(raw_data)
    users_out = extract_users(cleaned)
    orders_out = extract_orders(cleaned)

    return {"users": users_out, "orders": orders_out}
```

**Use When**:
- Multiple assets require shared complex logic
- Steps are expensive and should be shared
- Better encapsulation than separate assets with deps

---

## Asset Factories

Generate similar assets programmatically:

```python
def create_table_asset(table_name: str, schema: str):
    @dg.asset(
        name=f"{schema}_{table_name}",
        group_name=schema,
    )
    def _asset() -> None:
        load_table(schema, table_name)

    return _asset

# Generate assets
customers = create_table_asset("customers", "sales")
products = create_table_asset("products", "catalog")
orders = create_table_asset("orders", "sales")
```

---

## Asset Selection Syntax

Select subsets of assets for materialization or job definition:

### Basic Selection

```python
from dagster import AssetSelection

# Select specific assets
AssetSelection.assets("asset_a", "asset_b", "asset_c")

# Select all assets
AssetSelection.all()

# Select by group
AssetSelection.groups("analytics", "raw_data")

# Select by key prefix
AssetSelection.key_prefixes(["warehouse", "staging"])

# Select by tag
AssetSelection.tag("priority", "high")
```

### Dependency-Based Selection

```python
# Select asset and all upstream dependencies
AssetSelection.assets("final_report").upstream()

# Select asset and all downstream dependencies
AssetSelection.assets("raw_data").downstream()

# Select asset and immediate upstream only
AssetSelection.assets("final_report").upstream(depth=1)
```

### Combining Selections

```python
# Union: assets in A OR B
selection_a | selection_b

# Intersection: assets in A AND B
selection_a & selection_b

# Difference: assets in A but not in B
selection_a - selection_b

# Example: All analytics assets except one
AssetSelection.groups("analytics") - AssetSelection.assets("excluded_asset")
```

### Using in Jobs

```python
import dagster as dg

analytics_job = dg.define_asset_job(
    name="analytics_job",
    selection=AssetSelection.groups("analytics").downstream(),
)
```

### Using in CLI

```bash
# Materialize specific assets
dg launch --assets asset_a,asset_b

# Materialize all assets
dg launch --assets "*"

# Materialize by group (requires selection in job)
dg launch --job analytics_job
```

---

## Common Anti-Patterns

| Anti-Pattern | Better Approach |
| ------------ | --------------- |
| `load_customers` (verb-based name) | `customers` (noun describing output) |
| Giant asset doing everything | Split into focused, composable assets |
| No type annotations | Add return type: `-> dict`, `-> None` |
| No docstring | Add description in docstring or `description=` |
| Ignoring `MaterializeResult` | Return metadata for observability |
| Hardcoded paths | Use configuration or environment variables |

---

## References

- [Assets API](https://docs.dagster.io/api/dagster/assets)
- [Asset Metadata](https://docs.dagster.io/guides/build/assets/metadata-and-tags)
- [Multi-Assets](https://docs.dagster.io/guides/build/assets/multi-assets)
