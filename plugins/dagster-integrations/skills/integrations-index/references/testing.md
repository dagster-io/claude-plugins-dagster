# Testing Integrations

Data quality and testing frameworks for validation, schema compliance, and ensuring data pipeline
reliability.

---

### Great Expectations

**Package:** `dagster-ge` | **Support:** Dagster-supported

Data validation framework with expectations for testing data quality and generating documentation.

**Use cases:**

- Validate data quality with reusable expectations
- Test data for anomalies and schema violations
- Generate data quality documentation
- Monitor data quality over time

**Quick start:**

```python
from dagster_ge import ge_validation_factory
import great_expectations as ge

# Define expectations
@dg.asset
def validated_data():
    df = pd.read_csv("data.csv")

    # Create GE DataFrame
    ge_df = ge.from_pandas(df)

    # Add expectations
    ge_df.expect_column_values_to_not_be_null("user_id")
    ge_df.expect_column_values_to_be_between("age", 0, 120)
    ge_df.expect_column_values_to_be_in_set(
        "status", ["active", "inactive"]
    )

    # Validate
    validation_result = ge_df.validate()

    if not validation_result["success"]:
        raise ValueError("Data validation failed")

    return df
```

**Using validation factory:**

```python
# Create validation op from expectation suite
validation_op = ge_validation_factory(
    name="validate_users",
    datasource_name="my_datasource",
    suite_name="users.warning"
)

@dg.graph
def data_pipeline():
    data = extract_data()
    validated = validation_op(data)
    load_data(validated)
```

**Docs:** https://docs.dagster.io/integrations/libraries/great-expectations

**Key features:**

- 300+ built-in expectations
- Custom expectation development
- Data documentation generation
- Profiling and data discovery

---

### Pandera

**Package:** `dagster-pandera` | **Support:** Dagster-supported

Statistical data validation library for DataFrames with schema typing support.

**Use cases:**

- Type-safe DataFrame validation
- Statistical checks on data distributions
- Runtime schema enforcement
- Pandas and Polars DataFrame validation

**Quick start:**

```python
from dagster_pandera import pandera_schema_to_dagster_type
import pandera as pa

# Define Pandera schema
class UserSchema(pa.DataFrameModel):
    user_id: int = pa.Field(gt=0)
    email: str = pa.Field(str_matches=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: int = pa.Field(ge=0, le=120)
    signup_date: pa.DateTime

    @pa.check("age")
    def age_reasonable(cls, age_series):
        return age_series.mean() < 100

# Convert to Dagster type
UserDataFrame = pandera_schema_to_dagster_type(
    UserSchema,
    name="UserDataFrame"
)

@dg.asset
def validated_users() -> UserDataFrame:
    df = pd.read_csv("users.csv")
    # Validation happens automatically via type annotation
    return df
```

**Docs:** https://docs.dagster.io/integrations/libraries/pandera

**Key features:**

- Type annotations for DataFrames
- Statistical validation (mean, std, quantiles)
- Custom check functions
- Schema inference from DataFrames
- Pandas and Polars support

---

## Data Quality Tool Comparison

| Feature               | Great Expectations    | Pandera             |
| --------------------- | --------------------- | ------------------- |
| **Style**             | Expectation-based     | Schema-based        |
| **Typing**            | Runtime validation    | Type annotations    |
| **Complexity**        | More setup            | Simpler             |
| **Documentation**     | Auto-generated docs   | Code-first          |
| **Statistical tests** | Basic                 | Advanced            |
| **Best for**          | Enterprise validation | Type-safe pipelines |

## Common Patterns

### Basic Validation

```python
# Great Expectations
@dg.asset
def validated_data_ge():
    df = pd.read_csv("data.csv")
    ge_df = ge.from_pandas(df)

    ge_df.expect_column_values_to_not_be_null("id")
    ge_df.expect_column_values_to_be_unique("id")

    if not ge_df.validate()["success"]:
        raise ValueError("Validation failed")

    return df

# Pandera
@dg.asset
def validated_data_pandera() -> pa.typing.DataFrame[UserSchema]:
    df = pd.read_csv("data.csv")
    return df  # Automatic validation
```

### Conditional Validation

```python
# Pandera with custom checks
class SalesSchema(pa.DataFrameModel):
    date: pa.DateTime
    amount: float = pa.Field(gt=0)
    refunded: bool

    @pa.check("amount")
    def refund_amounts_negative(cls, amount_series, df):
        refunded_amounts = amount_series[df["refunded"]]
        return (refunded_amounts <= 0).all()
```

### Multi-Stage Validation

```python
@dg.asset
def raw_data() -> pd.DataFrame:
    return pd.read_csv("raw.csv")

@dg.asset
def schema_validated(raw_data: pd.DataFrame) -> UserDataFrame:
    # Schema validation via type annotation
    return raw_data

@dg.asset
def business_validated(schema_validated: UserDataFrame) -> pd.DataFrame:
    # Additional business rule validation
    ge_df = ge.from_pandas(schema_validated)
    ge_df.expect_column_pair_values_A_to_be_greater_than_B(
        "end_date", "start_date"
    )
    return schema_validated
```

## Tips

- **Early validation**: Validate data as soon as it enters your pipeline
- **Schema evolution**: Update schemas when data structure changes
- **Testing**: Test validation logic with both valid and invalid data
- **Performance**: Validation adds overhead - use sampling for large datasets
- **Documentation**: Use Great Expectations for auto-generated data docs
- **Type safety**: Use Pandera with type hints for better IDE support
- **Failed validations**: Decide whether to fail fast or log and continue
- **Monitoring**: Track validation failure rates over time
