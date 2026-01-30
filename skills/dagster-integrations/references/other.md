# Other Integrations

Miscellaneous integrations that don't fit into other categories, including DataFrame libraries and
utility tools.

---

## DataFrame Libraries

### Pandas

**Package:** `dagster-pandas` | **Support:** Dagster-supported

In-memory DataFrame library for data manipulation and analysis with type validation.

**Use cases:**

- Small to medium dataset transformations
- Data cleaning and preparation
- Exploratory data analysis
- CSV/Excel file processing

**Quick start:**

```python
from dagster_pandas import PandasColumn, create_dagster_pandas_dataframe_type
import pandas as pd

# Define DataFrame schema
EventDataFrame = create_dagster_pandas_dataframe_type(
    name="EventDataFrame",
    columns=[
        PandasColumn.integer_column("user_id", min_value=0),
        PandasColumn.string_column("event_type"),
        PandasColumn.datetime_column("timestamp")
    ]
)

@dg.asset
def events() -> EventDataFrame:
    return pd.DataFrame({
        "user_id": [1, 2, 3],
        "event_type": ["click", "view", "click"],
        "timestamp": pd.date_range("2024-01-01", periods=3)
    })
```

**Docs:** https://docs.dagster.io/integrations/libraries/pandas

---

### Polars

**Package:** `dagster-polars` | **Support:** Community-supported

Fast DataFrame library with columnar storage and lazy evaluation, often 5-10x faster than pandas.

**Use cases:**

- Fast in-memory transformations
- Processing medium to large datasets
- Lazy evaluation for query optimization
- Alternative to pandas with better performance

**Quick start:**

```python
import polars as pl

@dg.asset
def polars_transform() -> pl.DataFrame:
    return pl.DataFrame({
        "a": [1, 2, 3],
        "b": [4, 5, 6]
    }).with_columns(
        (pl.col("a") * pl.col("b")).alias("product")
    )

# Use lazy evaluation for large datasets
@dg.asset
def lazy_polars() -> pl.LazyFrame:
    return (
        pl.scan_parquet("large-file.parquet")
        .filter(pl.col("value") > 100)
        .group_by("category")
        .agg(pl.col("amount").sum())
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/polars

---

## DataFrame Library Comparison

| Feature             | Pandas              | Polars                   |
| ------------------- | ------------------- | ------------------------ |
| **Performance**     | Good                | Excellent (5-10x faster) |
| **Memory usage**    | Higher              | Lower (columnar)         |
| **API**             | Mature, widely used | Modern, Rust-based       |
| **Lazy evaluation** | No                  | Yes                      |
| **Best for**        | < 10GB datasets     | < 100GB datasets         |
| **Learning curve**  | Low (widely known)  | Low-Medium               |
| **Ecosystem**       | Extensive           | Growing                  |

## Common Patterns

### In-Memory DataFrame Processing

```python
@dg.asset
def load_data() -> pd.DataFrame:
    return pd.read_csv("input.csv")

@dg.asset
def transform_data(load_data: pd.DataFrame) -> pd.DataFrame:
    return load_data[load_data["value"] > 100].groupby("category").sum()

@dg.asset
def save_data(transform_data: pd.DataFrame):
    transform_data.to_parquet("output.parquet")
```

### Type-Safe DataFrames

```python
# Using Dagster's pandas type system
UserDataFrame = create_dagster_pandas_dataframe_type(
    name="UserDataFrame",
    columns=[
        PandasColumn.integer_column("id"),
        PandasColumn.string_column("name"),
        PandasColumn.categorical_column("status", categories=["active", "inactive"])
    ]
)

@dg.asset
def validated_users() -> UserDataFrame:
    df = pd.read_csv("users.csv")
    # Type validation happens automatically
    return df
```

### Lazy Evaluation with Polars

```python
@dg.asset
def lazy_pipeline() -> pl.DataFrame:
    # Build query plan without executing
    lazy_df = (
        pl.scan_parquet("large_data.parquet")
        .filter(pl.col("date") >= "2024-01-01")
        .group_by("category")
        .agg([
            pl.col("amount").sum().alias("total"),
            pl.col("amount").mean().alias("average")
        ])
    )

    # Execute query plan efficiently
    return lazy_df.collect()
```

### Migrating from Pandas to Polars

```python
# Pandas version
@dg.asset
def pandas_transform() -> pd.DataFrame:
    df = pd.read_csv("data.csv")
    return df[df["value"] > 100].groupby("category")["amount"].sum()

# Polars equivalent (faster)
@dg.asset
def polars_transform() -> pl.DataFrame:
    df = pl.read_csv("data.csv")
    return (
        df.filter(pl.col("value") > 100)
        .group_by("category")
        .agg(pl.col("amount").sum())
    )
```

## Tips

### For Pandas:

- **Memory**: Monitor memory usage for datasets > 1GB
- **Dtypes**: Specify dtypes when reading CSVs to save memory
- **Chunking**: Use `chunksize` parameter for large CSV files
- **Vectorization**: Use vectorized operations instead of loops
- **Copy vs View**: Be aware of whether operations return copies or views

### For Polars:

- **Lazy evaluation**: Use `scan_*` methods for large files
- **Streaming**: Enable streaming mode for larger-than-memory datasets
- **Expressions**: Learn Polars expression API for optimal performance
- **Migration**: Most pandas operations have direct Polars equivalents
- **Type system**: Polars has stricter types - embrace them for better performance

### General:

- **Start with Pandas**: If you're familiar with pandas, start there
- **Upgrade to Polars**: When performance becomes an issue, consider migrating
- **File formats**: Use Parquet over CSV for better performance
- **Profiling**: Profile your code to identify bottlenecks
- **Testing**: Test with small datasets locally, scale up in production
