# Monitoring Integrations

Observability platforms and metrics systems for tracking pipeline performance, health, and
operational metrics.

---

### Datadog

**Package:** `dagster-datadog` | **Support:** Dagster-supported

Send metrics, events, and logs to Datadog for comprehensive monitoring and observability.

**Use cases:**

- Track pipeline performance metrics
- Monitor asset materialization times
- Send custom metrics to Datadog
- Create dashboards for data operations

**Quick start:**

```python
from dagster_datadog import DatadogResource

datadog = DatadogResource(
    api_key=dg.EnvVar("DATADOG_API_KEY"),
    app_key=dg.EnvVar("DATADOG_APP_KEY")
)

@dg.asset
def monitored_asset(
    context: dg.AssetExecutionContext,
    datadog: DatadogResource
):
    import time
    start = time.time()

    # Process data
    result = process_data()

    # Send timing metric
    duration = time.time() - start
    datadog.get_client().metric.send(
        metric="dagster.asset.duration",
        points=[(time.time(), duration)],
        tags=[f"asset:{context.asset_key.path[-1]}"]
    )

    return result
```

**Docs:** https://docs.dagster.io/integrations/libraries/datadog

---

### Prometheus

**Package:** `dagster-prometheus` | **Support:** Dagster-supported

Export Dagster metrics to Prometheus for time-series monitoring.

**Use cases:**

- Expose Dagster metrics to Prometheus
- Create Grafana dashboards
- Monitor pipeline health over time
- Track asset materialization rates

**Quick start:**

```python
from dagster_prometheus import PrometheusResource

prometheus = PrometheusResource(
    gateway_url="http://localhost:9091"
)

@dg.asset
def track_metric(prometheus: PrometheusResource):
    from prometheus_client import Counter

    counter = Counter(
        "dagster_assets_materialized",
        "Number of assets materialized"
    )
    counter.inc()

    # Push to gateway
    prometheus.push_to_gateway(
        job="dagster_pipeline",
        registry=counter._registry
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/prometheus

---

### Papertrail

**Package:** `dagster-papertrail` | **Support:** Dagster-supported

Send logs to Papertrail for centralized log management.

**Use cases:**

- Centralize Dagster logs
- Search and filter pipeline logs
- Set up log-based alerts
- Long-term log retention

**Quick start:**

```python
from dagster_papertrail import PapertrailResource

papertrail = PapertrailResource(
    host="logs.papertrailapp.com",
    port=12345
)

@dg.asset
def logged_asset(
    context: dg.AssetExecutionContext,
    papertrail: PapertrailResource
):
    papertrail.log_message(
        f"Processing asset {context.asset_key}",
        level="INFO"
    )
    return process_data()
```

**Docs:** https://docs.dagster.io/integrations/libraries/papertrail

---

## Monitoring Tool Selection

| Tool           | Best For                    | Type             | Features                         |
| -------------- | --------------------------- | ---------------- | -------------------------------- |
| **Datadog**    | Comprehensive observability | APM/Metrics/Logs | Dashboards, alerts, tracing      |
| **Prometheus** | Time-series metrics         | Metrics          | Open-source, Grafana integration |
| **Papertrail** | Log aggregation             | Logging          | Search, retention, alerts        |

## Common Patterns

### Custom Metrics Tracking

```python
@dg.asset
def monitored_pipeline(
    context: dg.AssetExecutionContext,
    datadog: DatadogResource
):
    # Track custom business metrics
    datadog.get_client().metric.send(
        metric="business.records_processed",
        points=[(time.time(), record_count)],
        tags=["env:prod", "team:data"]
    )

    # Track data quality metrics
    datadog.get_client().metric.send(
        metric="data.quality.score",
        points=[(time.time(), quality_score)],
        tags=[f"asset:{context.asset_key.path[-1]}"]
    )
```

### Performance Monitoring

```python
@dg.asset
def timed_asset(
    context: dg.AssetExecutionContext,
    prometheus: PrometheusResource
):
    from prometheus_client import Histogram
    import time

    # Track execution time distribution
    duration_histogram = Histogram(
        "asset_duration_seconds",
        "Asset execution duration",
        buckets=[1, 5, 10, 30, 60, 300, 600]
    )

    start = time.time()
    result = process_data()
    duration = time.time() - start

    duration_histogram.observe(duration)
    prometheus.push_to_gateway(
        job="dagster_pipeline",
        registry=duration_histogram._registry
    )

    return result
```

### Log Aggregation

```python
@dg.asset
def logged_pipeline(
    context: dg.AssetExecutionContext,
    papertrail: PapertrailResource
):
    papertrail.log_message(
        f"Starting {context.asset_key}",
        level="INFO"
    )

    try:
        result = process_data()
        papertrail.log_message(
            f"Completed {context.asset_key}: {len(result)} records",
            level="INFO"
        )
        return result
    except Exception as e:
        papertrail.log_message(
            f"Failed {context.asset_key}: {e}",
            level="ERROR"
        )
        raise
```

### Health Dashboard Pattern

```python
@dg.asset
def health_metrics(datadog: DatadogResource):
    """Track overall pipeline health metrics"""

    # Asset freshness
    datadog.get_client().metric.send(
        metric="pipeline.assets.stale_count",
        points=[(time.time(), count_stale_assets())],
        tags=["env:prod"]
    )

    # Pipeline success rate
    datadog.get_client().metric.send(
        metric="pipeline.success_rate",
        points=[(time.time(), calculate_success_rate())],
        tags=["env:prod"]
    )

    # Data volume
    datadog.get_client().metric.send(
        metric="pipeline.data.volume_gb",
        points=[(time.time(), get_total_data_volume())],
        tags=["env:prod"]
    )
```

## Tips

- **Dashboards**: Create dashboards to visualize pipeline health at a glance
- **Metrics naming**: Use consistent naming conventions (e.g., `dagster.asset.duration`)
- **Tags**: Use tags to filter and aggregate metrics by environment, team, asset type
- **Baselines**: Establish baseline metrics to detect anomalies
- **SLOs**: Define Service Level Objectives for critical data pipelines
- **Retention**: Configure appropriate retention periods for logs and metrics
- **Costs**: Monitor observability tool costs - high cardinality tags can be expensive
- **Sampling**: For high-volume metrics, consider sampling to reduce costs
- **Integration**: Combine with alerting tools (Slack, PagerDuty) for complete observability
- **Documentation**: Document what each metric measures and when to be concerned
