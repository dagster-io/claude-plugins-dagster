## Usage

1. **Identify the scaffold request type**:
   - (MOST COMMON) Integration scaffolding
   - Asset, schedule, or sensor scaffolding ("python object" type)
   - Inline component
   - Custom component type

2. **Extract specifics** from user request:
   - Component type (if mentioned)
   - Component name/path
   - Format preference (YAML vs Python)
   - Parameters (if provided)

3. **Guide discovery if needed**:
   - If user indicates they want to integration with an external tool, use the `/dagster-integrations` skill to help find the right integration.
   - If no existing integration exists for their use case, guide them through creating either a new inline-component (if this is a one-off integration) or a new reusable component type (if they may need multiple instances of the same integration).

4. **Provide appropriate command**:
   - `dg scaffold defs <component_type> <path>` - For existing integration components
   - `dg scaffold defs <object_type> <name>.py` - For scaffolding a new python object (asset, schedule, sensor)
   - `dg scaffold defs inline-component <path>` - For custom inline components
   - `dg scaffold component <path>` - For creating a new reusable component type

## Integration Scaffolding

### Component Scaffolding

#### Example Queries:

- "I want to move data from s3 to Snowlake"
- "I want to setup my dbt project in Dagster"
- "I want to monitor my Fivetran connectors"

#### Workflow

Invoke the `/dagster-integrations` skill to help find an existing integration component that matches the user's use case.

##### Case: Found an existing component

Run the following command:

```bash
dg scaffold defs <component_type> <component_name> --json-params '{...}'
```

The format of the JSON parameters will depend on the component type. Based on the results of the `/dagster-integrations` skill, and any additional information provided by the user, determine the correct JSON parameters to use.

##### Case: No existing component found

Invoke the `/dg:prototype` skill to help create a new component.

## Python Object Scaffolding

IMPORTANT: For these scaffold commands, all filepaths must have a `.py` extension.

### Scaffold an Asset

#### Example Queries:

- "Create an asset called 'customers' in the sales folder"
- "Create an asset that fetches data from the API and saves it to the database"

#### Information to gather

1. Asset name (required)
2. Folder path (optional)
3. Function (optional) - if not specified, keep the body empty.

#### Workflow

Run the following command:

```bash
dg scaffold defs dagster.asset <asset_name>.py
```

Afterwards, if the user described what they wanted this asset to do, edit the file to implement the requested logic.

### Scaffold a Schedule

#### Example Queries:

- "Create a daily schedule called 'daily_refresh'"
- "Create a schedule that executes all the assets in the marketing group every hour"

#### Information to gather

1. Schedule name (required)
2. Cron schedule (required)
3. Target (required) - the job or selection of assets to run on this schedule

#### Workflow

Run the following command:

```bash
dg scaffold defs dagster.schedule <schedule_name>.py
```

Afterwards, edit the file to set the cron schedule and job or selection of assets to run on this schedule.

### Scaffold a Sensor

#### Example Queries:

- "Create a new sensor called 'file_watcher'"
- "Create a sensor that watches for new files in an s3 bucket and executes the assets in the marketing group"

#### Information to gather

1. Sensor name (required)
2. Target (required)
3. Function (optional) - if not specified, keep the body empty.

#### Workflow

Run the following command:

```bash
dg scaffold defs dagster.sensor <sensor_name>.py
```

Afterwards, edit the file to set the target of the sensor to the specified job or selection of assets. If the user described what they wanted this sensor to do, edit the file to implement the requested logic.

## Parameter Strategies

### JSON Parameters (Recommended for Complex Configs)

```bash
dg scaffold defs fivetran.FivetranComponent my_connector --json-params '{
  "connector_id": "abc123",
  "destination_id": "def456",
  "poll_interval": "10m"
}'
```

### Individual Flags (For Simple Configs)

```bash
dg scaffold defs my_component.MyType instance \
  --param1 value1 \
  --param2 value2
```

## Related Commands and Skills

### Discovery Phase

- `/dg:list` - Discover available components before scaffolding

### Validation Phase

- `/dg:list` - Verify scaffolded components appear
- `/dg:launch` - Test scaffolded assets

### Implementation Phase

- `/dg:prototype` - Full implementation with custom logic
- `/dagster-conventions` - Learn patterns for implementing assets

### Learning Phase

- `/dagster-integrations` - Understand integration patterns
- `/dignified-python` - Python code quality

## Validation

After scaffolding completes, encourage the user to invoke `dg list defs` to view the newly scaffolded definitions.
