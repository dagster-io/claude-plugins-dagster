# Automation Patterns Reference

## Pattern Summary

| Pattern | When to Use |
| ------- | ----------- |
| `ScheduleDefinition` | Fixed time intervals (daily, hourly, monthly) |
| `@dg.schedule` decorator | Custom schedule logic with dynamic job selection |
| `@dg.sensor` | Event-driven triggers (file changes, API updates) |
| `PartitionsDefinition` | Time-series or categorical data splits |
| Partitioned schedules | Automate partition materialization |

---

## Jobs

Jobs select which assets to materialize together:

### Basic Job Definition

```python
import dagster as dg

trip_update_job = dg.define_asset_job(
    name="trip_update_job",
    selection=["taxi_trips", "taxi_zones"],
)
```

### Asset Selection Patterns

```python
# Select specific assets
dg.AssetSelection.assets("asset_a", "asset_b")

# Select all assets
dg.AssetSelection.all()

# Select by group
dg.AssetSelection.groups("analytics")

# Select with dependencies
dg.AssetSelection.assets("final_report").upstream()  # Include upstream
dg.AssetSelection.assets("raw_data").downstream()    # Include downstream

# Combine selections
dg.AssetSelection.all() - dg.AssetSelection.assets("excluded_asset")
dg.AssetSelection.groups("a") | dg.AssetSelection.groups("b")  # Union
dg.AssetSelection.groups("a") & dg.AssetSelection.assets("specific")  # Intersection
```

### Job with Tags

```python
daily_job = dg.define_asset_job(
    name="daily_job",
    selection=dg.AssetSelection.all(),
    tags={"team": "data-eng", "priority": "high"},
)
```

---

## Schedules

### Basic Schedule

```python
import dagster as dg
from my_project.defs.jobs import trip_update_job

trip_update_schedule = dg.ScheduleDefinition(
    job=trip_update_job,
    cron_schedule="0 0 5 * *",  # 5th of each month at midnight
)
```

### Common Cron Patterns

| Pattern | Meaning |
| ------- | ------- |
| `* * * * *` | Every minute |
| `0 * * * *` | Every hour (at minute 0) |
| `0 0 * * *` | Daily at midnight |
| `0 6 * * *` | Daily at 6:00 AM |
| `0 0 * * 1` | Weekly on Monday at midnight |
| `0 0 * * 1-5` | Weekdays at midnight |
| `0 0 1 * *` | Monthly on the 1st at midnight |
| `0 0 5 * *` | Monthly on the 5th at midnight |
| `15 5 * * 1-5` | Weekdays at 5:15 AM |

**Tip**: Use [Crontab Guru](https://crontab.guru/) to create and test cron expressions.

### Schedule with Timezone

```python
my_schedule = dg.ScheduleDefinition(
    job=my_job,
    cron_schedule="0 9 * * *",  # 9:00 AM
    execution_timezone="America/New_York",
)
```

### Custom Schedule with Decorator

```python
@dg.schedule(cron_schedule="0 0 * * *", job=my_job)
def custom_schedule(context: dg.ScheduleEvaluationContext):
    """Schedule with custom logic."""
    scheduled_date = context.scheduled_execution_time.strftime("%Y-%m-%d")
    
    return dg.RunRequest(
        run_key=f"daily_{scheduled_date}",
        run_config={
            "ops": {
                "my_asset": {
                    "config": {"date": scheduled_date}
                }
            }
        },
    )
```

### Partitioned Schedule

Automatically run for new partitions:

```python
from my_project.defs.partitions import monthly_partition
from my_project.defs.jobs import partitioned_job

monthly_schedule = dg.build_schedule_from_partitioned_job(
    job=partitioned_job,
    description="Materializes data for the previous month",
)
```

---

## Sensors

### Sensor Anatomy

Sensors follow this lifecycle:
1. Read cursor (previous state)
2. Observe current state
3. Compare states and create run requests for changes
4. Update cursor

### Basic Sensor Pattern

```python
import dagster as dg
import json

@dg.sensor(job=my_job)
def file_sensor(context: dg.SensorEvaluationContext):
    # 1. Read cursor (previous state)
    previous_state = json.loads(context.cursor) if context.cursor else {}
    current_state = {}
    runs_to_request = []
    
    # 2. Observe current state
    for filepath in get_files_to_watch():
        last_modified = os.path.getmtime(filepath)
        filename = os.path.basename(filepath)
        current_state[filename] = last_modified
        
        # 3. Check for changes
        if filename not in previous_state or previous_state[filename] != last_modified:
            runs_to_request.append(dg.RunRequest(
                run_key=f"file_{filename}_{last_modified}",
                run_config={
                    "ops": {
                        "process_file": {
                            "config": {"filename": filename}
                        }
                    }
                }
            ))
    
    # 4. Return result with updated cursor
    return dg.SensorResult(
        run_requests=runs_to_request,
        cursor=json.dumps(current_state),
    )
```

### File Sensor

```python
import os
import json

@dg.sensor(job=adhoc_request_job)
def adhoc_request_sensor(context: dg.SensorEvaluationContext):
    PATH_TO_REQUESTS = os.path.join(
        os.path.dirname(__file__),
        "../../../data/requests",
    )
    
    previous_state = json.loads(context.cursor) if context.cursor else {}
    current_state = {}
    runs_to_request = []
    
    for filename in os.listdir(PATH_TO_REQUESTS):
        file_path = os.path.join(PATH_TO_REQUESTS, filename)
        if filename.endswith(".json") and os.path.isfile(file_path):
            last_modified = os.path.getmtime(file_path)
            current_state[filename] = last_modified
            
            if filename not in previous_state or previous_state[filename] != last_modified:
                with open(file_path, "r") as f:
                    request_config = json.load(f)
                
                runs_to_request.append(dg.RunRequest(
                    run_key=f"request_{filename}_{last_modified}",
                    run_config={
                        "ops": {
                            "adhoc_request": {
                                "config": {
                                    "filename": filename,
                                    **request_config
                                }
                            }
                        }
                    }
                ))
    
    return dg.SensorResult(
        run_requests=runs_to_request,
        cursor=json.dumps(current_state),
    )
```

### Asset Sensor

Trigger when another asset materializes:

```python
@dg.asset_sensor(asset_key=dg.AssetKey("upstream_asset"), job=downstream_job)
def upstream_sensor(context: dg.SensorEvaluationContext, asset_event):
    """Triggers when upstream_asset is materialized."""
    return dg.RunRequest(
        run_key=f"downstream_{asset_event.dagster_event.event_specific_data.materialization.run_id}",
    )
```

### Sensor with Skip Reason

```python
@dg.sensor(job=my_job, minimum_interval_seconds=60)
def conditional_sensor(context: dg.SensorEvaluationContext):
    new_files = check_for_new_files()
    
    if not new_files:
        return dg.SkipReason("No new files found")
    
    return dg.RunRequest(run_key=f"files_{len(new_files)}")
```

---

## Partitions

### Time-Based Partitions

```python
import dagster as dg

# Daily partitions
daily_partition = dg.DailyPartitionsDefinition(
    start_date="2023-01-01",
    end_date="2024-12-31",  # Optional
)

# Weekly partitions
weekly_partition = dg.WeeklyPartitionsDefinition(
    start_date="2023-01-01",
)

# Monthly partitions
monthly_partition = dg.MonthlyPartitionsDefinition(
    start_date="2023-01-01",
    end_date="2023-12-31",
)

# Hourly partitions
hourly_partition = dg.HourlyPartitionsDefinition(
    start_date="2023-01-01-00:00",
)
```

### Static Partitions

```python
# Fixed set of partitions
region_partition = dg.StaticPartitionsDefinition([
    "us-east",
    "us-west",
    "eu-west",
    "ap-south",
])

# Category partitions
category_partition = dg.StaticPartitionsDefinition([
    "electronics",
    "clothing",
    "home",
    "sports",
])
```

### Multi-Dimensional Partitions

```python
multi_partition = dg.MultiPartitionsDefinition({
    "date": dg.DailyPartitionsDefinition(start_date="2023-01-01"),
    "region": dg.StaticPartitionsDefinition(["us", "eu", "ap"]),
})

@dg.asset(partitions_def=multi_partition)
def multi_partitioned_asset(context: dg.AssetExecutionContext) -> None:
    partition_key = context.partition_key
    # partition_key is a MultiPartitionKey with .keys_by_dimension
    date = partition_key.keys_by_dimension["date"]
    region = partition_key.keys_by_dimension["region"]
```

### Using Partitions in Assets

```python
@dg.asset(partitions_def=monthly_partition)
def monthly_data(context: dg.AssetExecutionContext) -> None:
    """Process data for a specific month."""
    partition_date_str = context.partition_key  # "2023-01-01"
    month = partition_date_str[:-3]  # "2023-01"
    
    context.log.info(f"Processing partition: {month}")
    
    data = fetch_data_for_month(month)
    save_data(data, month)
```

### Partition Window Access

```python
@dg.asset(partitions_def=daily_partition)
def windowed_data(context: dg.AssetExecutionContext) -> None:
    """Access partition time window."""
    time_window = context.partition_time_window
    
    start = time_window.start  # datetime
    end = time_window.end      # datetime
    
    context.log.info(f"Processing from {start} to {end}")
```

---

## Partitioned Jobs

### Define Partitioned Job

```python
partitioned_job = dg.define_asset_job(
    name="partitioned_job",
    selection=["monthly_data"],
    partitions_def=monthly_partition,
)
```

### Run Specific Partition

```python
# In launchpad or programmatically
result = partitioned_job.execute_in_process(
    partition_key="2023-06-01",
)
```

---

## Backfills

Backfills materialize multiple partitions at once:

### UI Backfill
1. Navigate to the asset in the Dagster UI
2. Click "Materialize" dropdown
3. Select "Backfill"
4. Choose partition range

### Programmatic Backfill

```python
from dagster import DagsterInstance

instance = DagsterInstance.get()
instance.submit_run(
    partition_key="2023-01-01",
    job_name="partitioned_job",
)
```

---

## Combining Automation

### Partitioned Schedule

```python
# Create job with partition
monthly_job = dg.define_asset_job(
    name="monthly_job",
    selection=["monthly_data"],
    partitions_def=monthly_partition,
)

# Build schedule that runs for new partitions
monthly_schedule = dg.build_schedule_from_partitioned_job(
    job=monthly_job,
)
```

### Sensor with Partitions

```python
@dg.sensor(job=partitioned_job)
def partition_sensor(context: dg.SensorEvaluationContext):
    missing_partitions = get_missing_partitions()
    
    return [
        dg.RunRequest(
            run_key=f"backfill_{partition}",
            partition_key=partition,
        )
        for partition in missing_partitions
    ]
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Better Approach |
| ------------ | --------------- |
| No cursor in sensors | Always use cursor for state tracking |
| Polling too frequently | Set `minimum_interval_seconds` |
| Giant backfills at once | Use `max_runtime` on backfill policies |
| Hardcoded partition dates | Use dynamic start/end with constants |
| Ignoring timezone | Set `execution_timezone` on schedules |

---

## References

- [Schedules](https://docs.dagster.io/guides/automate/schedules)
- [Sensors](https://docs.dagster.io/guides/automate/sensors)
- [Partitions](https://docs.dagster.io/guides/build/partitions)
- [Asset Selection Syntax](https://docs.dagster.io/concepts/assets/asset-selection-syntax)

