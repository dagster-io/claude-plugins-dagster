# BI Integrations

Business intelligence and visualization platforms for data exploration, dashboards, and analytics.

---

### Looker
**Package:** `dagster-looker` | **Support:** Dagster-supported

Google's business intelligence platform for creating interactive dashboards and SQL-based analytics.

**Use cases:**
- Refresh Looker PDTs (persistent derived tables)
- Trigger Looker dashboard regeneration
- Integrate Looker explores with Dagster assets
- Schedule Looker report updates

**Quick start:**
```python
from dagster_looker import LookerResource

looker = LookerResource(
    base_url="https://company.looker.com",
    client_id=dg.EnvVar("LOOKER_CLIENT_ID"),
    client_secret=dg.EnvVar("LOOKER_CLIENT_SECRET")
)

@dg.asset
def refresh_looker_pdt(looker: LookerResource):
    # Refresh a persistent derived table
    looker.get_client().run_query(
        query_id="123",
        result_format="json"
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/looker

---

### Tableau
**Package:** `dagster-tableau` | **Support:** Dagster-supported

Interactive data visualization and dashboarding platform for business analytics.

**Use cases:**
- Refresh Tableau data sources
- Publish workbooks to Tableau Server
- Trigger extract refreshes
- Integrate with Tableau prep workflows

**Quick start:**
```python
from dagster_tableau import TableauResource

tableau = TableauResource(
    server_url="https://tableau.company.com",
    username=dg.EnvVar("TABLEAU_USER"),
    password=dg.EnvVar("TABLEAU_PASSWORD"),
    site_id="my_site"
)

@dg.asset
def refresh_tableau_datasource(tableau: TableauResource):
    # Refresh a Tableau data source
    tableau.refresh_datasource(
        datasource_id="abc-123-def"
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/tableau

---

### PowerBI
**Package:** `dagster-powerbi` | **Support:** Dagster-supported

Microsoft's business intelligence platform for creating reports and dashboards.

**Use cases:**
- Refresh PowerBI datasets
- Trigger PowerBI report generation
- Update PowerBI dataflows
- Schedule dashboard refreshes

**Quick start:**
```python
from dagster_powerbi import PowerBIResource

powerbi = PowerBIResource(
    client_id=dg.EnvVar("POWERBI_CLIENT_ID"),
    client_secret=dg.EnvVar("POWERBI_CLIENT_SECRET"),
    tenant_id=dg.EnvVar("POWERBI_TENANT_ID")
)

@dg.asset
def refresh_powerbi_dataset(powerbi: PowerBIResource):
    # Trigger dataset refresh
    powerbi.refresh_dataset(
        dataset_id="abc-123-def",
        workspace_id="workspace-456"
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/powerbi

---

### Sigma
**Package:** `dagster-sigma` | **Support:** Dagster-supported

Cloud-native analytics and BI platform with spreadsheet-like interface for data exploration.

**Use cases:**
- Refresh Sigma materialized datasets
- Trigger Sigma workbook updates
- Integrate with Sigma workflows
- Schedule data refreshes

**Quick start:**
```python
from dagster_sigma import SigmaResource

sigma = SigmaResource(
    base_url="https://app.sigmacomputing.com",
    client_id=dg.EnvVar("SIGMA_CLIENT_ID"),
    client_secret=dg.EnvVar("SIGMA_CLIENT_SECRET")
)

@dg.asset
def refresh_sigma_workbook(sigma: SigmaResource):
    # Trigger workbook refresh
    sigma.get_client().refresh_workbook(
        workbook_id="workbook-123"
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/sigma

---

### Hex
**Package:** `dagster-hex` | **Support:** Community-supported

Collaborative data notebooks platform combining SQL, Python, and visualizations.

**Use cases:**
- Run Hex projects from Dagster
- Schedule Hex notebook execution
- Pass data between Dagster and Hex
- Trigger Hex workflows

**Quick start:**
```python
from dagster_hex import HexResource

hex = HexResource(
    api_token=dg.EnvVar("HEX_API_TOKEN")
)

@dg.asset
def run_hex_project(hex: HexResource):
    # Trigger Hex project run
    run_id = hex.get_client().run_project(
        project_id="project-123",
        input_params={"date": "2024-01-01"}
    )
    return hex.wait_for_run(run_id)
```

**Docs:** https://docs.dagster.io/integrations/libraries/hex

---

### Evidence
**Package:** `dagster-evidence` | **Support:** Community-supported

Markdown-based BI tool for building data reports and dashboards with code.

**Use cases:**
- Generate Evidence reports from Dagster
- Build data-driven documentation
- Create automated reports
- Version-controlled analytics

**Quick start:**
```python
from dagster_evidence import EvidenceResource

evidence = EvidenceResource(
    project_dir="path/to/evidence/project"
)

@dg.asset
def generate_evidence_report(evidence: EvidenceResource):
    # Build Evidence project
    evidence.build()
```

**Docs:** https://docs.dagster.io/integrations/libraries/evidence

---

### Cube
**Package:** `dagster-cube` | **Support:** Community-supported

Semantic layer and headless BI platform for building consistent metrics across tools.

**Use cases:**
- Define metrics and dimensions
- Create semantic data models
- Power multiple BI tools from single definition
- API-first analytics

**Quick start:**
```python
from dagster_cube import CubeResource

cube = CubeResource(
    base_url="http://localhost:4000",
    api_token=dg.EnvVar("CUBE_API_TOKEN")
)

@dg.asset
def query_cube_metrics(cube: CubeResource):
    # Query Cube API
    result = cube.get_client().load({
        "measures": ["Orders.count"],
        "dimensions": ["Orders.status"]
    })
    return result
```

**Docs:** https://docs.dagster.io/integrations/libraries/cube

---

## BI Tool Selection

| Tool | Best For | Deployment | Complexity | Cost |
|------|----------|------------|------------|------|
| **Looker** | SQL-based analytics | Cloud | Medium | High |
| **Tableau** | Interactive viz | Cloud/Server | Medium | High |
| **PowerBI** | Microsoft ecosystem | Cloud/Desktop | Low | Medium |
| **Sigma** | Spreadsheet interface | Cloud | Low | Medium |
| **Hex** | Notebooks + BI | Cloud | Medium | Medium |
| **Evidence** | Code-first reports | Self-hosted | Low | Free |
| **Cube** | Semantic layer | Self-hosted/Cloud | High | Free/Paid |

## Common Patterns

### Data Refresh Pattern
```python
# Transform data in Dagster
@dg.asset
def analytics_table() -> pd.DataFrame:
    return transform_data()

# Load to warehouse
@dg.asset
def warehouse_table(
    analytics_table: pd.DataFrame,
    warehouse: WarehouseResource
):
    warehouse.write_dataframe(analytics_table, "analytics.summary")

# Refresh BI tool
@dg.asset
def refreshed_dashboard(
    warehouse_table,
    tableau: TableauResource
):
    tableau.refresh_datasource("dashboard-source-id")
```

### Scheduled Report Generation
```python
@dg.asset
def daily_report(hex: HexResource):
    # Run Hex notebook that generates report
    run_result = hex.get_client().run_project(
        project_id="daily-report",
        input_params={
            "report_date": datetime.now().strftime("%Y-%m-%d")
        }
    )
    return run_result

# Schedule daily
daily_schedule = dg.ScheduleDefinition(
    job=dg.define_asset_job("daily_report_job"),
    cron_schedule="0 8 * * *"  # 8 AM daily
)
```

### Multi-Tool Refresh
```python
@dg.asset
def core_data() -> pd.DataFrame:
    return load_and_transform_data()

@dg.asset
def refresh_all_bi_tools(
    core_data: pd.DataFrame,
    looker: LookerResource,
    tableau: TableauResource,
    powerbi: PowerBIResource
):
    # Refresh all BI tools after data update
    looker.refresh_pdt("pdt_name")
    tableau.refresh_datasource("datasource_id")
    powerbi.refresh_dataset("dataset_id")
```

## Tips

- **Timing**: Refresh BI tools after warehouse loads complete
- **Incremental**: Use incremental refreshes when possible to save time
- **Caching**: Be aware of BI tool caching - force refresh if needed
- **Dependencies**: Model BI refreshes as downstream assets
- **Testing**: Test BI integrations in dev environment first
- **Monitoring**: Alert on BI refresh failures
- **Semantic layer**: Consider Cube for consistent metrics across tools
- **Self-service**: Evidence and Hex enable analysts to own their reports
- **Costs**: Cloud BI tools can be expensive - monitor usage and seats
