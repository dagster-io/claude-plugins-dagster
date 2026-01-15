# Prototype Dagster Implementation

You are helping a developer prototype a new Dagster implementation following best practices. The implementation requirements and working directory have been provided:
$ARGUMENTS

## Overview

This command guides you through building production-ready Dagster code with:
- Best practices from `dagster-conventions` skill
- Appropriate integrations from `dagster-integrations` skill
- Validation and testing at every step
- Components and Pythonic assets as appropriate

## Workflow

### Step 1: Understand Requirements & Plan

1. **Analyze the requirements** to determine:
   - What assets need to be created
   - What integrations are needed
   - Whether to use Components or Pythonic assets (or both)
   - Testing strategy

2. **Reference available integrations**:
   ```bash
   uv run dg docs integrations --json
   ```

   Also consult the `dagster-integrations` skill for finding appropriate integrations for the use case.

3. **Review current project structure**:
   ```bash
   uv run dg list defs
   uv run dg list components
   ```

### Step 2: Choose Implementation Approach

**Use Components when**:
- Implementing common patterns (dbt, Fivetran, Airbyte, dlt, Sling)
- Need declarative YAML configuration
- Want reusability across projects
- Building standardized data pipelines
- **For dbt**: Use remote Git repository configuration to avoid cloning projects locally

**Use Pythonic Assets when**:
- Custom business logic required
- Complex transformations
- One-off implementations
- Need fine-grained control

**Use Both**:
- Mix Components for standard patterns (e.g., dbt transformations)
- Use Pythonic assets for custom logic
- Merge definitions as shown in `dagster-conventions`

### Step 3: Implement with Best Practices

#### For Component-Based Implementation

1. **Scaffold the component** (if creating custom):
   ```bash
   uv run dg scaffold component ComponentName
   ```

2. **Create component definitions**:
   ```bash
   uv run dg scaffold defs my_module.components.ComponentName my_component
   ```

3. **Configure in YAML** (`defs/<component_name>.yaml`):
   - Set all required parameters
   - Reference environment variables appropriately
   - Configure component-specific settings
   - **For dbt components**: Prefer `repo_url` + `repo_relative_path` over `project_dir`

4. **Validate the component loads**:
   ```bash
   uv run dg check defs
   uv run dg list defs
   ```

5. **Modern Component Pattern with Dataclass** (for custom components):

When creating custom components, use the `@dataclass` decorator with `Resolvable` for automatic YAML schema generation:

```python
from dataclasses import dataclass, field
import dagster as dg
from dagster.components import Component, ComponentLoadContext, Resolvable

@dataclass
class CustomETLComponent(Component, Resolvable):
    """Custom ETL component with auto-generated YAML schema.

    All dataclass fields automatically become YAML-configurable via Resolvable.
    """

    # Required fields (no defaults)
    source_table: str
    destination_table: str
    transformation_sql: str

    # Optional fields with defaults
    enable_logging: bool = True
    batch_size: int = 1000

    # Collections use field(default_factory=...)
    custom_tags: list[str] = field(default_factory=list)

    def build_defs(self, context: ComponentLoadContext) -> dg.Definitions:
        """Build asset definitions for this component."""

        @dg.asset(
            key=dg.AssetKey([self.destination_table]),
            kinds={"postgres", "python"},  # ALWAYS include kinds
            tags={tag: "true" for tag in self.custom_tags},
        )
        def etl_asset(context: dg.AssetExecutionContext):
            if self.enable_logging:
                context.log.info(f"Processing {self.source_table} → {self.destination_table}")

            # ETL implementation
            # 1. Query source table
            # 2. Apply transformation_sql
            # 3. Load to destination table
            pass

        return dg.Definitions(assets=[etl_asset])
```

**Corresponding YAML configuration:**

```yaml
# defs/my_etl/defs.yaml
type: my_project.components.CustomETLComponent

attributes:
  source_table: "raw_orders"
  destination_table: "processed_orders"
  transformation_sql: "SELECT * FROM raw_orders WHERE status = 'complete'"
  enable_logging: true
  batch_size: 5000
  custom_tags: ["finance", "daily"]
```

**Key benefits of the dataclass pattern:**
- Fields automatically generate YAML schema via `Resolvable`
- Type hints provide validation
- Default values make fields optional
- Use `field(default_factory=list)` for mutable defaults (lists, dicts)
- Most Dagster integration components use this pattern

#### For Pythonic Asset Implementation

1. **Scaffold asset file**:
   ```bash
   uv run dg scaffold defs dagster.asset assets/<domain_name>.py
   ```

2. **Implement assets following conventions**:
   - Use `@dg.asset` decorator with metadata (group_name, owners, tags, kinds)
   - Define clear dependencies via function parameters
   - Use `ConfigurableResource` for external services
   - Add type hints and docstrings
   - Keep assets focused and composable

3. **Example multi-asset chain** (realistic 3-5 asset pipeline):

   ```python
   import dagster as dg
   from my_project.resources import DatabaseResource, S3Resource
   import pandas as pd

   # Asset 1: Raw data ingestion
   @dg.asset(
       group_name="sales_analytics",
       owners=["team:data-engineering"],
       tags={"priority": "high", "domain": "sales", "schedule": "daily"},
       kinds={"s3", "python"},  # ALWAYS include kinds
       description="Raw customer orders extracted from operational database",
   )
   def raw_customer_orders(database: DatabaseResource) -> pd.DataFrame:
       """Extract raw customer orders from operational DB."""
       query = "SELECT * FROM orders WHERE created_at >= CURRENT_DATE - INTERVAL '1 day'"
       return database.query(query)

   # Asset 2: Data cleaning/transformation
   @dg.asset(
       group_name="sales_analytics",
       owners=["team:data-engineering"],
       tags={"priority": "high", "domain": "sales", "schedule": "daily"},
       kinds={"python"},
       description="Cleaned orders with validation and deduplication",
   )
   def cleaned_orders(raw_customer_orders: pd.DataFrame) -> pd.DataFrame:
       """Clean and deduplicate order data."""
       # Remove duplicates
       df = raw_customer_orders.drop_duplicates(subset=["order_id"])

       # Validate required fields
       df = df.dropna(subset=["order_id", "customer_id", "amount"])

       # Standardize formats
       df["amount"] = df["amount"].astype(float)
       df["created_at"] = pd.to_datetime(df["created_at"])

       return df

   # Asset 3: Business logic/aggregation
   @dg.asset(
       group_name="sales_analytics",
       owners=["team:data-engineering"],
       tags={"priority": "high", "domain": "sales", "schedule": "daily"},
       kinds={"python"},
       description="Customer lifetime value aggregated by customer",
   )
   def customer_lifetime_value(cleaned_orders: pd.DataFrame) -> pd.DataFrame:
       """Calculate customer lifetime value metrics."""
       clv = cleaned_orders.groupby("customer_id").agg({
           "amount": "sum",
           "order_id": "count",
           "created_at": ["min", "max"]
       }).reset_index()

       clv.columns = ["customer_id", "total_revenue", "order_count", "first_order", "last_order"]
       clv["avg_order_value"] = clv["total_revenue"] / clv["order_count"]

       return clv

   # Asset 4: Enrichment with external data
   @dg.asset(
       group_name="sales_analytics",
       owners=["team:data-engineering"],
       tags={"priority": "high", "domain": "sales", "schedule": "daily"},
       kinds={"python", "snowflake"},
       description="CLV enriched with customer demographic data",
   )
   def enriched_customer_metrics(
       customer_lifetime_value: pd.DataFrame,
       database: DatabaseResource
   ) -> pd.DataFrame:
       """Enrich CLV metrics with customer demographic data."""
       # Join with customer demographics
       customers = database.query("SELECT customer_id, segment, region FROM customers")
       enriched = customer_lifetime_value.merge(customers, on="customer_id", how="left")

       return enriched

   # Asset 5: Output/export for downstream consumption
   @dg.asset(
       group_name="sales_analytics",
       owners=["team:data-engineering"],
       tags={"priority": "high", "domain": "sales", "schedule": "daily"},
       kinds={"s3", "python"},
       description="Customer metrics exported to S3 for BI tools",
   )
   def customer_metrics_export(
       enriched_customer_metrics: pd.DataFrame,
       s3: S3Resource
   ) -> None:
       """Export enriched metrics to S3 for Tableau/Looker consumption."""
       # Write to S3 as parquet
       s3.write_parquet(
           enriched_customer_metrics,
           bucket="analytics-exports",
           key="customer_metrics/latest.parquet"
       )
   ```

   **Key patterns demonstrated:**
   - **Clear asset chain**: raw → cleaned → aggregated → enriched → exported
   - **Always include `kinds`**: Helps with filtering and organization in Dagster UI
   - **Dependencies via parameters**: Each asset lists its dependencies as function parameters
   - **Descriptive names**: Nouns that describe the data output, not the action
   - **Consistent metadata**: Same group, owners, tags across related assets
   - **Type hints**: Specify return types for better IDE support and validation

4. **Create resources** (`resources.py`):
   ```python
   from dagster import ConfigurableResource, EnvVar

   class MyDatabaseResource(ConfigurableResource):
       connection_string: str = EnvVar("DATABASE_URL")

       def query(self, sql: str) -> list:
           # Implementation
           pass
   ```

5. **Register in definitions** (`definitions.py`):
   ```python
   from dagster import Definitions
   from dagster_dg import load_defs
   from my_project.defs.assets import customers, customer_metrics
   from my_project.defs.resources import MyDatabaseResource

   # Load component definitions
   component_defs = load_defs()

   # Define pythonic assets
   pythonic_defs = Definitions(
       assets=[customers, customer_metrics],
       resources={"database": MyDatabaseResource()},
   )

   # Merge together
   defs = Definitions.merge(component_defs, pythonic_defs)
   ```

## Critical: Design Asset Keys for Multi-Component Pipelines

When building multi-component pipelines (e.g., Fivetran → dbt → Hightouch), **asset keys must be designed so downstream components can reference them naturally**. This eliminates the need for per-asset configuration and makes your pipeline maintainable.

### Key Principle: Upstream Defines, Downstream Consumes

The upstream component should generate asset keys that downstream components naturally expect. This "configure once, apply to all" approach prevents configuration burden downstream.

### Common Downstream Integration Patterns

#### If dbt will consume your assets:

Use **flat, 2-level keys** like `["source_name", "table"]`:

```python
# GOOD: Flat 2-level keys
["fivetran_raw", "customers"]  # dbt: source('fivetran_raw', 'customers')
["api_data", "orders"]          # dbt: source('api_data', 'orders')

# AVOID: Deeply nested keys
["fivetran", "raw", "production", "customers"]  # Requires extra dbt config
```

**Why flat keys?** dbt sources expect 2-level structure:
```yaml
# sources.yml - works naturally with flat keys
sources:
  - name: fivetran_raw
    tables:
      - name: customers  # Matches ["fivetran_raw", "customers"]
      - name: orders     # Matches ["fivetran_raw", "orders"]
```

#### If custom Dagster assets will consume:

Match the key structure those assets expect in their `deps`:

```python
# Upstream component creates:
["raw", "customers"]

# Downstream asset references naturally:
@dg.asset(deps=[dg.AssetKey(["raw", "customers"])])
def processed_customers(): ...
```

#### If reverse ETL tools (Census, Hightouch) will consume:

Use simple model names from dbt (typically single-level keys):

```python
# dbt creates from model file names:
["customer_lifetime_value"]
["monthly_revenue_by_region"]

# Reverse ETL tools reference by model name directly
```

### Asset Key Anti-Patterns

❌ **Too deeply nested:**
```python
["company", "team", "project", "environment", "schema", "table"]
# Hard for downstream to reference, requires complex mapping
```

❌ **Inconsistent structure:**
```python
["raw", "customers"]           # 2 levels
["processed", "finance", "revenue"]  # 3 levels
# Confusing for consumers, unpredictable references
```

❌ **Generic names:**
```python
["data", "table1"]
["output", "result"]
# Not clear what system they're from, conflicts likely
```

✅ **Good patterns:**
```python
["source_system", "entity"]    # ["fivetran_raw", "customers"]
["integration", "object"]      # ["salesforce", "accounts"]
["stage", "table"]             # ["staging", "orders"]
```

### Verifying Asset Key Alignment

After implementing your components, verify dependencies are correct:

```bash
# Check that asset keys and dependencies align
uv run dg list defs --json | uv run python -c "
import sys, json
data = json.load(sys.stdin)
assets = data.get('assets', [])
print('Asset Dependencies:\n')
for asset in assets:
    key = asset.get('key', 'unknown')
    deps = asset.get('deps', [])
    if deps:
        print(f'{key}')
        for dep in deps:
            print(f'  ← {dep}')
    else:
        print(f'{key} (no dependencies)')
    print()
"
```

**What to verify:**
- ✅ Downstream assets list upstream assets in their `deps` array
- ✅ No missing dependencies (especially dbt models depending on sources)
- ✅ Keys are simple and descriptive (typically 2 levels)
- ✅ No duplicate keys with different structures

**Common issues:**
- **dbt models not depending on sources**: SQL must use `{{ source('source_name', 'table') }}`
- **Nested keys don't match dbt expectations**: Consider flattening (see advanced pattern below)
- **Reverse ETL can't find models**: Use simple model names that match dbt output

### Advanced: Override get_asset_spec() for Key Transformation

When subclassing existing integration components (like Fivetran, Sling), you can override `get_asset_spec()` to transform asset keys for better downstream compatibility.

**When to use this pattern:**
- Subclassing integration components that generate nested keys
- Need to flatten keys for dbt compatibility
- Want to apply consistent key structure across all assets from a component
- "Configure once, apply to all" - one override affects all generated assets

**Example: Flatten Fivetran keys for dbt**

Problem: Fivetran creates `["fivetran", "connector_id", "schema", "table"]` but dbt expects `["fivetran_raw", "table"]`.

Solution:

```python
from dagster_fivetran import FivetranAccountComponent
from dagster_fivetran.translator import FivetranConnectorTableProps
import dagster as dg

class CustomFivetranComponent(FivetranAccountComponent):
    """Fivetran component with flattened asset keys for dbt compatibility."""

    def get_asset_spec(self, props: FivetranConnectorTableProps) -> dg.AssetSpec:
        """Override to flatten asset keys for easier dbt integration."""
        base_spec = super().get_asset_spec(props)
        original_key = base_spec.key.path

        # Flatten nested key: ["fivetran", "connector", "schema", "table"]
        # becomes: ["fivetran_raw", "table"]
        table_name = original_key[-1]  # Get the last element (table name)
        flattened_key = dg.AssetKey(["fivetran_raw", table_name])

        return base_spec.replace_attributes(key=flattened_key)
```

**Result:** dbt sources work naturally without extra configuration:

```yaml
# sources.yml - no meta.dagster needed!
sources:
  - name: fivetran_raw
    tables:
      - name: customers  # Matches ["fivetran_raw", "customers"]
      - name: orders     # Matches ["fivetran_raw", "orders"]
```

**When NOT to override:**
- Using component directly (not subclassing) → Can't override
- Default keys already work for your pipeline → Keep it simple
- Only one or two assets need different keys → Configure individually instead

**Other use cases:**
- **Sling**: Flatten `["sling", "replication_name", "stream"]` → `["raw", "stream"]`
- **Custom components**: Apply consistent prefixing or namespacing
- **Multi-environment**: Add environment suffix like `_staging` or `_prod`

### Step 4: Add Automation

Choose the appropriate automation pattern based on requirements:

#### Declarative Automation (Recommended)

```python
from dagster import AutomationCondition

@dg.asset(
    automation_condition=AutomationCondition.on_missing()
    | AutomationCondition.on_cron("0 9 * * *")
)
def automated_asset() -> None:
    pass
```

#### Traditional Schedules

```bash
uv run dg scaffold defs dagster.schedule schedules.py
```

```python
import dagster as dg

my_schedule = dg.ScheduleDefinition(
    job=my_job,
    cron_schedule="0 0 * * *",  # Daily at midnight
)
```

#### Asset Selection-Based Scheduling (Recommended for Scale)

For larger projects, use **asset selection syntax** instead of hardcoded asset keys. This makes schedules maintainable as your project grows:

```python
from dataclasses import dataclass
import dagster as dg
from dagster.components import Component, ComponentLoadContext, Resolvable

@dataclass
class ScheduledJobComponent(Component, Resolvable):
    """Component for scheduling assets using flexible selection syntax."""

    job_name: str
    cron_schedule: str
    asset_selection: str  # Selection string using tags, groups, kinds, etc.

    def build_defs(self, context: ComponentLoadContext) -> dg.Definitions:
        """Build a scheduled job with flexible asset selection."""

        job = dg.define_asset_job(
            name=self.job_name,
            selection=self.asset_selection,
        )

        schedule = dg.ScheduleDefinition(
            job=job,
            cron_schedule=self.cron_schedule,
        )

        return dg.Definitions(schedules=[schedule], jobs=[job])
```

**YAML configuration examples:**

```yaml
# Daily finance job - selects by tags
type: my_project.components.ScheduledJobComponent
attributes:
  job_name: "daily_finance_job"
  cron_schedule: "0 6 * * *"  # 6 AM UTC daily
  asset_selection: "tag:schedule=daily tag:domain=finance"

---
# Hourly critical operations - selects by priority
type: my_project.components.ScheduledJobComponent
attributes:
  job_name: "hourly_ops_job"
  cron_schedule: "0 * * * *"  # Every hour
  asset_selection: "tag:priority=critical"

---
# Weekly analytics - selects by group
type: my_project.components.ScheduledJobComponent
attributes:
  job_name: "weekly_analytics_job"
  cron_schedule: "0 8 * * 1"  # Monday 8 AM UTC
  asset_selection: "group:sales_analytics"

---
# All dbt models - selects by kind
type: my_project.components.ScheduledJobComponent
attributes:
  job_name: "dbt_refresh_job"
  cron_schedule: "0 4 * * *"  # 4 AM UTC daily
  asset_selection: "kind:dbt"
```

**Asset selection patterns:**
- `tag:key=value` - Assets with specific tag
- `group:name` - Assets in a group
- `kind:type` - Assets of a kind (dbt, python, fivetran, etc.)
- `owner:email` - Assets owned by a team
- `*pattern*` - Key pattern matching
- Multiple conditions with spaces (AND) or `|` (OR)

**Benefits:**
- No hardcoded asset keys → easier maintenance
- Automatically includes new assets matching criteria
- Self-documenting: selection string shows what's scheduled
- Scales to hundreds of assets without config bloat

#### Sensors (Event-Driven)

```bash
uv run dg scaffold defs dagster.sensor sensors.py
```

### Step 5: Implement Testing

**Always include tests** following `dagster-conventions` testing patterns:

1. **Create test file** (`tests/test_<asset_name>.py`):
   ```python
   import dagster as dg
   from my_project.defs.assets import customers, customer_metrics
   from unittest.mock import Mock

   def test_customers_asset():
       """Test customers asset logic directly."""
       # Mock dependencies
       mock_database = Mock()
       mock_database.query.return_value = [{"id": 1, "name": "Test"}]

       # Test with dg.materialize
       result = dg.materialize(
           assets=[customers],
           resources={"database": mock_database},
       )

       assert result.success

   def test_customer_metrics_dependency():
       """Test customer_metrics depends on customers."""
       result = dg.materialize(
           assets=[customers, customer_metrics],
           resources={"database": Mock()},
       )

       assert result.success
       assert result.output_for_node("customer_metrics") is not None
   ```

2. **Add asset checks** for data quality:
   ```python
   @dg.asset_check(asset=customers)
   def customers_not_empty(customers):
       """Validate that customers table has data."""
       return dg.AssetCheckResult(
           passed=len(customers) > 0,
           metadata={"row_count": len(customers)},
       )
   ```

3. **Run tests**:
   ```bash
   pytest tests/
   ```

### Step 6: Validate Complete Implementation

Run comprehensive validation checks:

1. **Validate definitions load**:
   ```bash
   uv run dg check defs
   ```

2. **List all definitions** to verify assets are registered:
   ```bash
   uv run dg list defs
   ```

3. **Check components** (if using Components):
   ```bash
   uv run dg list components
   ```

4. **Test asset materialization** in dev mode:
   ```bash
   uv run dg launch --assets <asset_name>
   ```

5. **Run the test suite**:
   ```bash
   pytest tests/ -v
   ```

6. **Verify asset key alignment and dependencies**:

This is CRITICAL for multi-component pipelines. Verify that downstream assets properly depend on upstream assets:

```bash
# Visualize asset dependencies
uv run dg list defs --json | uv run python -c "
import sys, json
data = json.load(sys.stdin)
assets = data.get('assets', [])
print('Asset Dependencies:\n')
for asset in assets:
    key = asset.get('key', 'unknown')
    deps = asset.get('deps', [])
    if deps:
        print(f'{key}')
        for dep in deps:
            print(f'  ← {dep}')
    else:
        print(f'{key} (no dependencies)')
    print()
"
```

**What to verify:**
- ✅ Downstream assets list upstream assets in their `deps` array
- ✅ No missing dependencies (especially dbt models depending on sources)
- ✅ Asset keys are simple and descriptive (typically 2 levels: `["category", "name"]`)
- ✅ No duplicate asset keys with different structures

**Common issues and fixes:**

| Issue | Problem | Cause | Fix |
|-------|---------|-------|-----|
| **dbt models missing dependencies** | Staging models show no upstream deps | SQL doesn't use `{{ source('...') }}` | Add source references in SQL |
| **Asset keys don't match expectations** | Fivetran creates `["fivetran", "raw", "table"]` but dbt expects `["fivetran_raw", "table"]` | Default component keys too nested | Override `get_asset_spec()` to flatten (see Asset Key Design section) |
| **Reverse ETL missing deps** | Hightouch/Census can't find dbt models | Use simple model names or configure deps explicitly |
| **Duplicate keys** | Multiple components creating same key | Check key generation logic, ensure unique prefixes |

**If dependencies are missing**, refer back to the "Critical: Design Asset Keys for Multi-Component Pipelines" section above for guidance on fixing key alignment.

### Step 7: Documentation & Next Steps

1. **Document the implementation**:
   - Add clear docstrings to all assets
   - Document any custom components
   - Note any environment variables required
   - Explain the data flow

2. **Recommend next steps**:
   - Deploy to staging environment
   - Set up monitoring and alerting
   - Configure production resources
   - Enable automation conditions or schedules

## Key Principles

Throughout implementation, follow these principles from `dagster-conventions`:

- **Think in Assets**: Focus on *what* to produce, not *how* to execute
- **Environment Separation**: Use `ConfigurableResource` and `EnvVar` for configuration
- **Testing First**: Write tests alongside assets
- **Clear Naming**: Use nouns for assets (`customers`, not `load_customers`)
- **Proper Dependencies**: Use function parameters for asset dependencies
- **Metadata Rich**: Add owners, tags, groups, kinds to assets
- **Avoid Over-Engineering**: Keep it simple, don't add unnecessary abstractions

## Reference Documentation

Always cross-reference these resources:

- **Dagster API Reference**: https://docs.dagster.io/llms.txt for titles and descriptions
- **Full API Details**: https://docs.dagster.io/llms-full.txt for complete API information
- **Component Creation**: https://docs.dagster.io/guides/build/components/creating-new-components/creating-and-registering-a-component
- **Component Customization**: https://docs.dagster.io/guides/build/components/creating-new-components/component-customization

## Example Complete Implementation

For reference, here's a complete example structure showing all patterns:

```
my_project/
├── src/
│   └── my_project/
│       ├── definitions.py                    # Merge components + pythonic definitions
│       ├── defs/
│       │   ├── assets/
│       │   │   ├── __init__.py
│       │   │   └── sales_analytics.py        # Pythonic multi-asset chain (Phase 5)
│       │   ├── resources.py                  # Custom ConfigurableResource classes
│       │   ├── my_etl/                       # Custom component instance
│       │   │   └── defs.yaml                 # YAML config with dataclass fields
│       │   ├── daily_finance_job/            # Scheduled job with asset selection
│       │   │   └── defs.yaml
│       │   └── weekly_analytics_job/
│       │       └── defs.yaml
│       └── components/
│           ├── __init__.py
│           ├── custom_etl_component.py       # @dataclass + Resolvable pattern (Phase 1)
│           └── scheduled_job_component.py    # Asset selection-based scheduling (Phase 6)
└── tests/
    ├── test_sales_analytics.py               # Test multi-asset chains
    ├── test_custom_etl.py                    # Test custom components
    └── test_resources.py                     # Test resource configurations
```

**Key patterns integrated:**
- **Dataclass components** with auto-generated YAML schema
- **Multi-asset chains** (raw → cleaned → aggregated → enriched)
- **Asset key design** for dbt/downstream integration
- **Scheduled jobs** using asset selection syntax
- **Merged definitions** combining components and pythonic assets

## Validation Checklist

Before considering the prototype complete, ensure:

**Core Functionality:**
- [ ] All definitions load successfully (`dg check defs`)
- [ ] Assets appear in `dg list defs` output
- [ ] Tests pass (`pytest tests/`)
- [ ] At least one asset can be materialized (`dg launch --assets <name>`)

**Asset Quality:**
- [ ] All assets include `kinds` parameter (e.g., `kinds={"python", "snowflake"}`)
- [ ] Assets have proper metadata (owners, tags, groups)
- [ ] Asset names are descriptive nouns (data outputs, not actions)
- [ ] Resources use environment variables appropriately (`EnvVar`)

**Multi-Component Integration** (if using multiple components):
- [ ] Asset keys designed for downstream integration (see "Asset Key Design" section)
- [ ] Dependencies verified with JSON command (Step 6, item 6)
- [ ] Downstream assets list upstream assets in their `deps` array
- [ ] Asset keys are flat 2-level structure when consumed by dbt
- [ ] No missing dependencies between components

**Components** (if using custom components):
- [ ] Dataclass pattern with `@dataclass` + `Resolvable` for YAML schema generation
- [ ] All asset examples include `kinds` parameter

**Automation** (if using):
- [ ] Schedules/jobs use asset selection syntax (not hardcoded keys) for scalability
- [ ] Selection patterns tested with `dg list assets --job <job_name>`

**Documentation:**
- [ ] Documentation is clear and complete
- [ ] Appropriate integrations from `dagster-integrations` are used
- [ ] Best practices from `dagster-conventions` are followed

## Related Skills and Resources

For more specialized patterns and workflows, consider these complementary resources:

**Reusable Skills:**
- **dagster-conventions** - Comprehensive Dagster development conventions and best practices
- **dagster-integrations** - Index of 82+ Dagster integrations across cloud platforms, data warehouses, ETL tools, AI/ML, and more

**Composition Patterns:**
These skills can be combined with `/dg:prototype` for complete workflows:
- Initialize projects with proper structure
- Leverage existing integration components
- Create custom components with advanced patterns
- Implement flexible scheduling strategies

**Cross-References in This Guide:**
- For **asset key design**, see: "Critical: Design Asset Keys for Multi-Component Pipelines" section
- For **dependency verification**, see: Step 6, item 6 with JSON validation command
- For **dataclass components**, see: Step 3, item 5 "Modern Component Pattern with Dataclass"
- For **multi-asset chains**, see: Step 3, item 3 "Example multi-asset chain"
- For **scalable scheduling**, see: Step 4, "Asset Selection-Based Scheduling"
